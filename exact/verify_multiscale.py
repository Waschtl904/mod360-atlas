#!/usr/bin/env python3
"""Different-algorithm checker for fixed MOD-360 multiscale counts.

Eratosthenes flags, unordered prime-pair enumeration and square-divisor
exclusion; no SPF recurrence or generator import. Fraction-based identities.
Default/--check is read-only. --write explicitly replaces the certificate.
"""
from __future__ import annotations
import argparse
from bisect import bisect_right
from collections import Counter
import csv
from fractions import Fraction as F
import hashlib
import json
from math import gcd, isqrt
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data' / 'multiscale-v1'
CERT = ROOT / 'certificates' / 'multiscale-v1.json'
BOUNDS = (36_000, 360_000, 3_600_000)
BASE = ('primes', 'semiprimes', 'squarefree', 'prime_squares')
METRICS = ('primes', 'composites', 'semiprimes', 'distinct_semiprimes', 'prime_squares', 'squarefree')


def need(ok: bool, text: str) -> None:
    if not ok:
        raise RuntimeError(text)


def independent_census(bounds: tuple[int, ...]) -> dict:
    limit = bounds[-1]
    prime = bytearray(b'\x01')*(limit+1)
    prime[0] = prime[1] = 0
    for p in range(2, isqrt(limit)+1):
        if prime[p]:
            prime[p*p:limit+1:p] = b'\x00'*((limit-p*p)//p+1)
    ps = [p for p in range(2, limit+1) if prime[p]]
    sf = bytearray(b'\x01')*(limit+1)
    sf[0] = 0
    for p in ps:
        if p*p > limit:
            break
        sf[p*p:limit+1:p*p] = b'\x00'*(limit//(p*p))
    result = {b: {key: [0]*360 for key in BASE} for b in bounds}
    for b in bounds:
        for r in range(360):
            first = r or 360
            result[b]['primes'][r] = sum(prime[first:b+1:360])
            result[b]['squarefree'][r] = sum(sf[first:b+1:360])
        for p in ps:
            if p*p > b:
                break
            result[b]['prime_squares'][p*p % 360] += 1
    for i, p in enumerate(ps):
        if p*p > limit:
            break
        for j in range(i, bisect_right(ps, limit//p)):
            n = p*ps[j]
            for b in bounds:
                if n <= b:
                    result[b]['semiprimes'][n % 360] += 1
    # Third implementation for small cases: trial division, directly classify.
    for n in range(1, min(limit, 10_000)+1):
        factors, x, d = [], n, 2
        while d*d <= x:
            while x % d == 0:
                factors.append(d)
                x //= d
            d += 1
        if x > 1:
            factors.append(x)
        need(bool(prime[n]) == (len(factors) == 1), f'trial primality {n}')
        need(bool(sf[n]) == (len(set(factors)) == len(factors)), f'trial squarefree {n}')
    return result


def independent_stats(v: list[int]) -> dict:
    u = [r for r in range(360) if gcd(r, 360) == 1]
    # CRT square criterion, not the generator's square-image enumeration.
    q = [r for r in u if r % 8 == 1 and r % 9 in (1, 4, 7) and r % 5 in (1, 4)]
    a = [r for r in u if r % 30 in (1, 19)]
    need(len(q) == 6 and len(a) == 24 and set(q) <= set(a), 'square/family sets')
    t, qt, at = sum(v[r] for r in u), sum(v[r] for r in q), sum(v[r] for r in a)
    family = Counter()
    for r in u:
        family[r % 30] += v[r]
    # Numerator forms differ from the centered-sum implementation.
    energy = F(96*sum(v[r]**2 for r in u)-t*t, 96)
    fine_energy = F(12*sum(v[r]**2 for r in u)-sum(z*z for z in family.values()), 12)
    coarse_energy = F(8*sum(z*z for z in family.values())-t*t, 96)
    delta, fine, coarse = F(t-16*qt, 90), F(at-4*qt, 18), F(t-4*at, 72)
    need(delta == F(4, 5)*(fine+coarse), 'matched-family contrast identity')
    need(energy == fine_energy+coarse_energy, 'energy identity')
    lo, hi = min(v[r] for r in u), max(v[r] for r in u)
    return {'total_all': sum(v), 'total_units': t, 'square_total': qt, 'family_A_total': at,
            'delta': str(delta), 'delta_fine': str(fine), 'delta_coarse': str(coarse),
            'energy': str(energy), 'energy_fine': str(fine_energy),
            'energy_coarse': str(coarse_energy),
            'fine_energy_share': str(fine_energy/energy) if energy else 'NA',
            'min': lo, 'max': hi,
            'min_residues': ';'.join(str(r) for r in u if v[r] == lo),
            'max_residues': ';'.join(str(r) for r in u if v[r] == hi)}


def check_counts(rows: list[dict], expected: dict, bounds: tuple[int, ...]) -> None:
    fields = ['r']+[f'{key}_{b}' for b in bounds for key in BASE]
    need(len(rows) == 360 and list(rows[0]) == fields, 'count table schema')
    for r, row in enumerate(rows):
        need(int(row['r']) == r, 'residue labels')
        for b in bounds:
            for key in BASE:
                need(int(row[f'{key}_{b}']) == expected[b][key][r],
                     f'independent count mismatch: r={r}, {key}, X={b}')


def verify() -> dict:
    expected = independent_census(BOUNDS)
    with (DATA/'counts.csv').open(newline='') as handle:
        rows = list(csv.DictReader(handle))
    check_counts(rows, expected, BOUNDS)
    # Deliberately alter a datum: fail on mathematics, before certificate hashes.
    altered = [dict(v) for v in rows]
    altered[49]['primes_36000'] = str(int(altered[49]['primes_36000'])+1)
    try:
        check_counts(altered, expected, BOUNDS)
    except RuntimeError as exc:
        need('independent count mismatch' in str(exc), 'unexpected mutation failure')
    else:
        raise RuntimeError('mutation survived')
    with (DATA/'comparisons.csv').open(newline='') as handle:
        comparisons = list(csv.DictReader(handle))
    need(len(comparisons) == 36, 'comparison count')
    expected_fields = ['kind','lower_exclusive','upper_inclusive','metric']+list(independent_stats([0]*360))
    need(list(comparisons[0]) == expected_fields, 'comparison schema')
    index, full_views = 0, []
    u = [r for r in range(360) if gcd(r,360) == 1]
    squares = {r*r % 360 for r in u}
    for kind in ('cumulative', 'interval'):
        for i, hi in enumerate(BOUNDS):
            lo = BOUNDS[i-1] if kind == 'interval' and i else 0
            exposure = (hi-lo)//360
            values = {key: [expected[hi][key][r]-(expected[lo][key][r] if lo else 0)
                            for r in range(360)] for key in BASE}
            values['distinct_semiprimes'] = [s-q for s,q in zip(values['semiprimes'], values['prime_squares'])]
            values['composites'] = [exposure-values['primes'][r]-int(lo == 0 and r == 1) for r in range(360)]
            need(sum(values['composites'])+sum(values['primes'])+int(lo == 0) == hi-lo, 'integer partition')
            need(all(values['prime_squares'][r] == 0 for r in u if r not in squares), 'prime-square support')
            need(all(v >= 0 for seq in values.values() for v in seq), 'negative count')
            details = {}
            for metric in METRICS:
                stats = independent_stats(values[metric])
                wanted = {'kind':kind, 'lower_exclusive':str(lo), 'upper_inclusive':str(hi), 'metric':metric}
                wanted.update({k:str(v) for k,v in stats.items()})
                need(comparisons[index] == wanted, f'comparison mismatch {kind}/{hi}/{metric}')
                index += 1
                families = {s:sum(values[metric][r] for r in u if r % 30 == s)
                            for s in range(30) if gcd(s,30) == 1}
                residuals = [[r, 12*values[metric][r]-families[r % 30]] for r in u]
                need(all(sum(z for r,z in residuals if r % 30 == s) == 0 for s in families), 'fiber zero sum')
                details[metric] = {'counts_all_360':values[metric], 'family_totals':families,
                                   'fine_residual_numerators_denominator_12':residuals}
            sq = sum(values['prime_squares'][r] for r in u)
            need(F(independent_stats(values['distinct_semiprimes'])['delta']) ==
                 F(independent_stats(values['semiprimes'])['delta'])+F(sq,6), 'square-removal identity')
            full_views.append({'kind':kind,'lower_exclusive':lo,'upper_inclusive':hi,
                               'exposure_per_residue':exposure,'metrics':details})
    full = {'schema':'mod360-multiscale-expanded-v1','modulus':360,'bounds':BOUNDS,'windows':full_views}
    full_bytes = (json.dumps(full, sort_keys=True, separators=(',',':'))+'\n').encode()
    # Check complete generator exports including fine 12-lift residual vectors.
    with tempfile.TemporaryDirectory() as folder:
        dest = Path(folder)
        subprocess.run([sys.executable,str(ROOT/'exact/generate_multiscale.py'),
                        '--export',str(dest)],check=True,stdout=subprocess.DEVNULL)
        for name in ('counts.csv','comparisons.csv'):
            need((DATA/name).read_bytes() == (dest/name).read_bytes(), f'regenerated {name}')
        need(full_bytes == (dest/'expanded.json').read_bytes(), 'full export')
        # A small independent boundary run, including 360 and 361 in adjacent blocks.
        small = (360,720,1080)
        subprocess.run([sys.executable,str(ROOT/'exact/generate_multiscale.py'),
                        '--bounds','360,720,1080','--export',str(dest)],
                       check=True,stdout=subprocess.DEVNULL)
        with (dest/'counts.csv').open(newline='') as handle:
            check_counts(list(csv.DictReader(handle)),independent_census(small),small)
        invalid = subprocess.run([sys.executable,str(ROOT/'exact/generate_multiscale.py'),
                                  '--bounds','361','--export',str(dest)],
                                 stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        need(invalid.returncode != 0, 'invalid non-block bound accepted')
    paths = [ROOT/'exact'/name for name in ('generate_multiscale.py','verify_multiscale.py')]
    paths += [DATA/name for name in ('counts.csv','comparisons.csv')]
    return {'schema':'mod360-multiscale-certificate-v1','status':'PASS','modulus':360,
            'bounds':list(BOUNDS),'interval_convention':'lower exclusive, upper inclusive',
            'independent_external_review':False,
            'checks':{'raw_count_cells':4320,'comparison_rows':36,'fine_residual_entries':3456,
                      'trial_division_bound':10000,'boundary_bounds':[360,720,1080],
                      'mutated_prime_count_rejected':True,'non_block_bound_rejected':True},
            'expanded_sha256':hashlib.sha256(full_bytes).hexdigest(),
            'sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--check',action='store_true')
    group.add_argument('--write',action='store_true')
    args = parser.parse_args()
    result = verify()
    content = (json.dumps(result,indent=2,sort_keys=True)+'\n').encode()
    if args.write:
        CERT.parent.mkdir(parents=True,exist_ok=True)
        CERT.write_bytes(content)
    else:
        need(CERT.is_file() and CERT.read_bytes() == content, 'certificate mismatch')
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__ == '__main__':
    main()
