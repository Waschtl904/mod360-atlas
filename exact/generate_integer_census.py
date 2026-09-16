#!/usr/bin/env python3
"""Exact census of positive integers in fixed MOD-360 classes (stdlib only).

Default: check committed artifacts without modifying them. Use --write explicitly.
No primality probability, asymptotic assertion, or literature-novelty claim.
"""
from __future__ import annotations
import argparse
from array import array
from collections import Counter
import csv
import hashlib
import io
import json
from math import gcd, isqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'integer-census-v1'
MODULUS = 360
FIELDS = ('r', 'gcd', 'integers', 'one', 'primes', 'composites', 'squarefree',
          'semiprimes', 'prime_squares', 'proper_prime_powers',
          'omega_sum', 'Omega_sum', 'first_prime', 'first_composite')
COUNTS = FIELDS[2:12]


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode('utf-8')


def build(limit: int) -> dict[str, bytes]:
    if not 1 <= limit <= 10_000_000:
        raise ValueError('limit must be between 1 and 10000000')
    # Algorithm A: smallest-prime-factor sieve plus exact recurrences.
    spf = array('I', [0]) * (limit + 1)
    for p in range(2, limit + 1):
        if spf[p] == 0:
            spf[p] = p
            if p <= isqrt(limit):
                for n in range(p*p, limit + 1, p):
                    if spf[n] == 0:
                        spf[n] = p
    omega, big = bytearray(limit + 1), bytearray(limit + 1)
    rows = []
    for r in range(MODULUS):
        row = {key: 0 for key in FIELDS}
        row.update(r=r, gcd=gcd(r, MODULUS))
        rows.append(row)
    profile: Counter[tuple[int, int]] = Counter()
    lpf: Counter[int] = Counter()
    lpf_units: Counter[int] = Counter()
    for n in range(1, limit + 1):
        if n > 1:
            p, m = spf[n], n // spf[n]
            omega[n] = omega[m] + int(m % p != 0)
            big[n] = big[m] + 1
        w, W = omega[n], big[n]
        prime, composite = W == 1, W >= 2
        row = rows[n % MODULUS]
        row['integers'] += 1
        row['one'] += int(n == 1)
        row['primes'] += int(prime)
        row['composites'] += int(composite)
        row['squarefree'] += int(w == W)  # includes 1 by convention
        row['semiprimes'] += int(W == 2)
        row['prime_squares'] += int(W == 2 and w == 1)
        row['proper_prime_powers'] += int(w == 1 and W >= 2)
        row['omega_sum'] += w
        row['Omega_sum'] += W
        if prime and not row['first_prime']:
            row['first_prime'] = n
        if composite:
            if not row['first_composite']:
                row['first_composite'] = n
            lpf[spf[n]] += 1
            if row['gcd'] == 1:
                lpf_units[spf[n]] += 1
        profile[w, W] += 1
    stream = io.StringIO(newline='')
    writer = csv.DictWriter(stream, fieldnames=FIELDS, lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
    groups = {}
    for label, selected in (
        ('all', rows), ('units', [v for v in rows if v['gcd'] == 1]),
        ('nonunits', [v for v in rows if v['gcd'] != 1])):
        groups[label] = {key: sum(v[key] for v in selected) for key in COUNTS}
    fibers = []
    for s in range(30):
        if gcd(s, 30) != 1:
            continue
        rs = list(range(s, MODULUS, 30))
        vals = [rows[r]['primes'] for r in rs]
        fibers.append({'mod30': s, 'residues': rs,
                       'prime_counts_by_depth': vals,
                       'prime_total': sum(vals),
                       'prime_min': min(vals), 'prime_max': max(vals),
                       'semiprime_counts_by_depth': [rows[r]['semiprimes'] for r in rs]})
    summary = {
        'schema': 'mod360-positive-integer-census-v1',
        'modulus': MODULUS, 'lower_inclusive': 1, 'upper_inclusive': limit,
        'counted_rows': MODULUS, 'groups': groups, 'unit_fibers_mod30': fibers,
        'interpretation': 'Exact finite window only; categories overlap except one/primes/composites.',
        'missing_first_witness_sentinel': 0,
        'squarefree_includes_one': True,
        'proper_prime_powers_exclude_primes': True,
        'joint_omega_Omega': [[w, W, count] for (w, W), count in sorted(profile.items())],
        'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    factors = {
        'schema': 'mod360-least-prime-factor-v1', 'upper_inclusive': limit,
        'scope': 'Composite positive integers only; each integer counted once.',
        'all': [[p, count] for p, count in sorted(lpf.items())],
        'units': [[p, count] for p, count in sorted(lpf_units.items())],
    }
    return {'residues.csv': stream.getvalue().encode('utf-8'),
            'summary.json': json_bytes(summary), 'least-factors.json': json_bytes(factors)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--limit', type=int, default=1_000_000)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    args = parser.parse_args()
    artifacts = build(args.limit)
    for name, content in artifacts.items():
        path = OUT / name
        if args.write:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
        elif not path.exists() or path.read_bytes() != content:
            raise SystemExit(f'Artifact mismatch: {path}; inspect before regenerating with --write')
    print(f'CENSUS {"WROTE" if args.write else "MATCH"}: 1..{args.limit}, 360 rows')


if __name__ == '__main__':
    main()
