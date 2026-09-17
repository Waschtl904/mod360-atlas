#!/usr/bin/env python3
"""Fixed-modulus, equal-exposure MOD-360 census at three prescribed bounds.

Only stdlib. Default/--check compares committed bytes. --write explicitly
regenerates reference tables. --export DIR optionally accepts --bounds.
Finite deterministic counts and rational contrasts; no probability model.
"""
from __future__ import annotations
import argparse
from array import array
from fractions import Fraction
import csv
import io
import json
from math import gcd, isqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'multiscale-v1'
BOUNDS = (36_000, 360_000, 3_600_000)
BASE = ('primes', 'semiprimes', 'squarefree', 'prime_squares')
METRICS = ('primes', 'composites', 'semiprimes', 'distinct_semiprimes',
           'prime_squares', 'squarefree')
UNITS = [r for r in range(360) if gcd(r, 360) == 1]
Q = {a*a % 360 for a in UNITS}
A = [r for r in UNITS if r % 30 in (1, 19)]
FAMILIES = {s: [r for r in UNITS if r % 30 == s]
            for s in range(30) if gcd(s, 30) == 1}


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def validate(bounds: tuple[int, ...]) -> None:
    if not bounds or tuple(sorted(set(bounds))) != bounds or any(
            b <= 0 or b % 360 or b > 10_000_000 for b in bounds):
        raise ValueError('bounds must be increasing positive multiples of 360 <= 10000000')


def census(bounds: tuple[int, ...]) -> dict:
    """Algorithm A: SPF recurrence; no imported data or prime lists."""
    validate(bounds)
    limit = bounds[-1]
    spf = array('I', [0]) * (limit + 1)
    for p in range(2, limit + 1):
        if spf[p] == 0:
            spf[p] = p
            if p <= isqrt(limit):
                for n in range(p*p, limit + 1, p):
                    if spf[n] == 0:
                        spf[n] = p
    sf = bytearray(limit + 1)
    sf[1] = 1
    counts = {key: [0]*360 for key in BASE}
    snapshots = {}
    stops = set(bounds)
    for n in range(1, limit + 1):
        p = spf[n]
        m = n // p if n > 1 else 0
        if n > 1:
            sf[n] = sf[m] and m % p != 0
        r = n % 360
        counts['primes'][r] += int(n > 1 and p == n)
        counts['semiprimes'][r] += int(m >= 2 and spf[m] == m)
        counts['prime_squares'][r] += int(n > 1 and p == m)
        counts['squarefree'][r] += sf[n]
        if n in stops:
            snapshots[n] = {key: val[:] for key, val in counts.items()}
    return snapshots


def window(snapshots: dict, lo: int, hi: int) -> dict:
    rows = {key: [snapshots[hi][key][r] - (snapshots[lo][key][r] if lo else 0)
                  for r in range(360)] for key in BASE}
    exposure = (hi-lo)//360
    rows['composites'] = [exposure - rows['primes'][r] - int(lo == 0 and r == 1)
                          for r in range(360)]
    rows['distinct_semiprimes'] = [s-q for s, q in zip(rows['semiprimes'], rows['prime_squares'])]
    require(all(n >= 0 for val in rows.values() for n in val), 'negative count')
    return rows


def contrast(v: list[int]) -> dict:
    total, q, a = sum(v[r] for r in UNITS), sum(v[r] for r in Q), sum(v[r] for r in A)
    delta = Fraction(total-q, 90) - Fraction(q, 6)
    fine = Fraction(a-q, 18) - Fraction(q, 6)
    coarse = Fraction(total-a, 72) - Fraction(a, 24)
    require(delta == Fraction(4, 5)*(fine+coarse), 'contrast decomposition')
    family = {s: sum(v[r] for r in rs) for s, rs in FAMILIES.items()}
    mean = Fraction(total, 96)
    energy = sum((Fraction(v[r])-mean)**2 for r in UNITS)
    fine_energy = sum((Fraction(v[r])-Fraction(family[r % 30], 12))**2 for r in UNITS)
    coarse_energy = sum(12*(Fraction(t, 12)-mean)**2 for t in family.values())
    require(energy == fine_energy + coarse_energy, 'orthogonal decomposition')
    least, most = min(v[r] for r in UNITS), max(v[r] for r in UNITS)
    return {'total_all': sum(v), 'total_units': total, 'square_total': q, 'family_A_total': a,
            'delta': str(delta), 'delta_fine': str(fine), 'delta_coarse': str(coarse),
            'energy': str(energy), 'energy_fine': str(fine_energy),
            'energy_coarse': str(coarse_energy),
            'fine_energy_share': str(fine_energy/energy) if energy else 'NA',
            'min': least, 'max': most,
            'min_residues': ';'.join(str(r) for r in UNITS if v[r] == least),
            'max_residues': ';'.join(str(r) for r in UNITS if v[r] == most)}


def encode_csv(header: list, rows: list) -> bytes:
    stream = io.StringIO(newline='')
    writer = csv.writer(stream, lineterminator='\n')
    writer.writerow(header)
    writer.writerows(rows)
    return stream.getvalue().encode()


def render(snapshots: dict, bounds: tuple[int, ...]) -> tuple[dict, bytes]:
    counts = encode_csv(['r']+[f'{key}_{b}' for b in bounds for key in BASE],
                        [[r]+[snapshots[b][key][r] for b in bounds for key in BASE] for r in range(360)])
    comparisons, expanded = [], []
    keys = list(contrast([0]*360))
    for kind in ('cumulative', 'interval'):
        for i, hi in enumerate(bounds):
            lo = bounds[i-1] if kind == 'interval' and i else 0
            values = window(snapshots, lo, hi)
            details = {}
            for key in METRICS:
                stats = contrast(values[key])
                comparisons.append([kind, lo, hi, key]+[stats[k] for k in keys])
                family = {s: sum(values[key][r] for r in rs) for s, rs in FAMILIES.items()}
                d12 = [[r, 12*values[key][r]-family[r % 30]] for r in UNITS]
                require(all(sum(v for r, v in d12 if r % 30 == s) == 0 for s in FAMILIES), 'zero fiber sum')
                details[key] = {'counts_all_360': values[key], 'family_totals': family,
                                'fine_residual_numerators_denominator_12': d12}
            sq = sum(values['prime_squares'][r] for r in UNITS)
            require(Fraction(contrast(values['distinct_semiprimes'])['delta']) ==
                    Fraction(contrast(values['semiprimes'])['delta']) + Fraction(sq, 6), 'square correction')
            expanded.append({'kind': kind, 'lower_exclusive': lo, 'upper_inclusive': hi,
                             'exposure_per_residue': (hi-lo)//360, 'metrics': details})
    tables = {'counts.csv': counts,
              'comparisons.csv': encode_csv(['kind','lower_exclusive','upper_inclusive','metric']+keys, comparisons)}
    export = (json.dumps({'schema': 'mod360-multiscale-expanded-v1', 'modulus': 360,
                         'bounds': bounds, 'windows': expanded}, sort_keys=True, separators=(',', ':'))+'\n').encode()
    return tables, export


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--check', action='store_true')
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--export', type=Path)
    parser.add_argument('--bounds', default=','.join(map(str, BOUNDS)))
    args = parser.parse_args()
    bounds = tuple(int(v) for v in args.bounds.split(','))
    validate(bounds)
    if bounds != BOUNDS and args.export is None:
        parser.error('custom bounds require --export; reference data are fixed')
    tables, expanded = render(census(bounds), bounds)
    if args.export is not None or args.write:
        dest = args.export if args.export is not None else OUT
        dest.mkdir(parents=True, exist_ok=True)
        for name, content in tables.items():
            (dest/name).write_bytes(content)
        if args.export is not None:
            (dest/'expanded.json').write_bytes(expanded)
    else:
        for name, content in tables.items():
            require((OUT/name).is_file() and (OUT/name).read_bytes() == content, f'artifact mismatch: {name}')
    print('MULTISCALE: ' + ('EXPORTED' if args.export is not None else 'WROTE' if args.write else 'MATCH'))


if __name__ == '__main__':
    main()
