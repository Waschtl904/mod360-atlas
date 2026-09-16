#!/usr/bin/env python3
"""Verify the MOD-360 integer census with a different exact algorithm.

Uses an Eratosthenes bit sieve and prime-power divisor incidence, NOT the
smallest-factor recurrences of the generator. No external Python packages.
"""
from __future__ import annotations
import argparse
from array import array
from bisect import bisect_left, bisect_right
from collections import Counter
import csv
import hashlib
import json
from math import gcd, isqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'integer-census-v1'
CERT = ROOT / 'certificates' / 'integer-census-v1.json'


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def verify() -> dict:
    summary = json.loads((OUT / 'summary.json').read_text())
    least = json.loads((OUT / 'least-factors.json').read_text())
    with (OUT / 'residues.csv').open(newline='') as handle:
        rows = [{k: int(v) for k, v in row.items()} for row in csv.DictReader(handle)]
    X = summary['upper_inclusive']
    require(isinstance(X, int) and 1 <= X <= 10_000_000, 'invalid window')
    require(summary['lower_inclusive'] == 1 and summary['modulus'] == 360, 'wrong scope')
    require(len(rows) == 360 and [v['r'] for v in rows] == list(range(360)), 'row labels')
    require(summary['source_sha256'] == hashlib.sha256(
        (ROOT / 'exact' / 'generate_integer_census.py').read_bytes()).hexdigest(), 'generator source hash')
    # Algorithm B: ordinary prime flags; no SPF table is imported or reused.
    prime = bytearray(b'\x01') * (X + 1)
    prime[0] = prime[1] = 0
    for p in range(2, isqrt(X) + 1):
        if prime[p]:
            prime[p*p:X+1:p] = b'\x00' * ((X - p*p)//p + 1)
    ps = [p for p in range(2, X + 1) if prime[p]]
    w, W = bytearray(X + 1), bytearray(X + 1)
    squarefree = bytearray(b'\x01') * (X + 1)
    proper_powers, squares = set(), set()
    least_label = array('I', [0]) * (X + 1)
    for p in ps:
        for n in range(p, X + 1, p):
            w[n] += 1
            if not least_label[n]:
                least_label[n] = p
        power = p
        while power <= X:
            for n in range(power, X + 1, power):
                W[n] += 1
            if power > p:
                proper_powers.add(power)
            power *= p
        if p*p <= X:
            squares.add(p*p)
            squarefree[p*p:X+1:p*p] = b'\x00' * (X//(p*p))
    actual = [{key: 0 for key in row} for row in rows]
    joint: Counter[tuple[int, int]] = Counter()
    lpf_all: Counter[int] = Counter()
    lpf_unit: Counter[int] = Counter()
    for r, row in enumerate(actual):
        row.update(r=r, gcd=gcd(r, 360))
    for n in range(1, X + 1):
        row = actual[n % 360]
        comp = n > 1 and not prime[n]
        row['integers'] += 1
        row['one'] += int(n == 1)
        row['primes'] += prime[n]
        row['composites'] += int(comp)
        row['squarefree'] += squarefree[n]
        row['semiprimes'] += int(W[n] == 2)
        row['prime_squares'] += int(n in squares)
        row['proper_prime_powers'] += int(n in proper_powers)
        row['omega_sum'] += w[n]
        row['Omega_sum'] += W[n]
        if prime[n] and not row['first_prime']:
            row['first_prime'] = n
        if comp:
            if not row['first_composite']:
                row['first_composite'] = n
            lpf_all[least_label[n]] += 1
            if row['gcd'] == 1:
                lpf_unit[least_label[n]] += 1
        joint[w[n], W[n]] += 1
        require(bool(prime[n]) == (W[n] == 1), f'prime/Omega at {n}')
        require(bool(squarefree[n]) == (w[n] == W[n]), f'squarefree at {n}')
    require(rows == actual, 'row-by-row independent reconstruction')
    for r, row in enumerate(rows):
        expected = X//360 if r == 0 else (0 if X < r else (X-r)//360 + 1)
        require(row['integers'] == expected, f'exposure at residue {r}')
        require(row['one'] + row['primes'] + row['composites'] == expected, f'partition at {r}')
    keys = ('integers','one','primes','composites','squarefree','semiprimes',
            'prime_squares','proper_prime_powers','omega_sum','Omega_sum')
    for label in ('all', 'units', 'nonunits'):
        selected = [v for v in rows if label == 'all' or (v['gcd'] == 1) == (label == 'units')]
        require(summary['groups'][label] == {k: sum(v[k] for v in selected) for k in keys}, label)
    require(summary['counted_rows'] == 360 and summary['missing_first_witness_sentinel'] == 0, 'schema metadata')
    require(summary['squarefree_includes_one'] and summary['proper_prime_powers_exclude_primes'], 'category conventions')
    require(summary['joint_omega_Omega'] == [[a,b,c] for (a,b),c in sorted(joint.items())], 'joint histogram')
    require(least['upper_inclusive'] == X, 'LPF window')
    require(least['all'] == [[p,c] for p,c in sorted(lpf_all.items())], 'all LPF counts')
    require(least['units'] == [[p,c] for p,c in sorted(lpf_unit.items())], 'unit LPF counts')
    for fiber in summary['unit_fibers_mod30']:
        rs = list(range(fiber['mod30'], 360, 30))
        vals = [rows[r]['primes'] for r in rs]
        require(fiber == {'mod30':rs[0], 'residues':rs, 'prime_counts_by_depth':vals,
                         'prime_total':sum(vals), 'prime_min':min(vals), 'prime_max':max(vals),
                         'semiprime_counts_by_depth':[rows[r]['semiprimes'] for r in rs]}, 'fiber')
    require([v['mod30'] for v in summary['unit_fibers_mod30']] == [1,7,11,13,17,19,23,29], 'eight fibers')
    # Third path for semiprimes: enumerate p <= q, pq <= X, once each.
    pq_counts = [0]*360
    for i, p in enumerate(ps):
        if p*p > X:
            break
        for q in ps[i:bisect_right(ps, X//p)]:
            pq_counts[p*q % 360] += 1
    require(pq_counts == [v['semiprimes'] for v in rows], 'unordered-prime-pair semiprime counts')
    # Unit-class formula using prime progressions; independent of the pq loop.
    by_r = [[] for _ in range(360)]
    for p in ps:
        by_r[p % 360].append(p)
    unit_formula = [0]*360
    for p in ps:
        if p*p > X:
            break
        if p <= 5:
            continue
        inv = pow(p, -1, 360)
        for r in range(360):
            if gcd(r, 360) == 1:
                seq = by_r[r*inv % 360]
                unit_formula[r] += bisect_right(seq, X//p) - bisect_left(seq, p)
    require(all(unit_formula[r] == pq_counts[r] for r in range(360) if gcd(r,360)==1), 'unit semiprime formula')
    # Exact sieving within each fixed 360-column; do not mistake p for composite.
    labels = array('I', [0]) * (X + 1)
    progressions = 0
    for p in ps:
        if p*p > X:
            break
        if p <= 5:
            continue
        inv = pow(360, -1, p)
        for r in range(360):
            if gcd(r,360) != 1:
                continue
            k0 = (-r*inv) % p
            lo = max(0, (p*p-r+359)//360)
            hi = (X-r)//360
            start = lo + (k0-lo) % p
            for k in range(start, hi+1, p):
                n = r+360*k
                require(n % p == 0 and n >= p*p, 'bad progression')
                if not labels[n]:
                    labels[n] = p
            progressions += 1
    for n in range(2, X+1):
        if gcd(n,360) == 1:
            require(labels[n] == (0 if prime[n] else least_label[n]), f'least-factor progression at {n}')
    # Trial division sanity path, including 1 and small square boundaries.
    trial_bound = min(X, 10_000)
    for n in range(1, trial_bound+1):
        require(bool(prime[n]) == (n >= 2 and all(n % d for d in range(2,isqrt(n)+1))), f'trial {n}')
    paths = [ROOT/'exact'/name for name in ('generate_integer_census.py','verify_integer_census.py')]
    paths += [OUT/name for name in ('residues.csv','summary.json','least-factors.json')]
    return {'schema': 'mod360-integer-census-certificate-v1', 'status':'PASS',
            'scope': {'modulus':360, 'lower_inclusive':1, 'upper_inclusive':X},
            'independent_algorithms_not_independent_review': True,
            'checks': {'residue_rows':360, 'integers_cross_checked':X,
                       'trial_division_integers':trial_bound,
                       'least_factor_progressions':progressions,
                       'semiprime_methods':3},
            'sha256': {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    args = parser.parse_args()
    report = verify()
    content = (json.dumps(report, indent=2, sort_keys=True)+'\n').encode()
    if args.write:
        CERT.parent.mkdir(parents=True, exist_ok=True)
        CERT.write_bytes(content)
    else:
        require(CERT.exists() and CERT.read_bytes() == content, 'certificate mismatch')
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
