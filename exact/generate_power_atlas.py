#!/usr/bin/env python3
"""MOD-360 power maps: exact finite atlas, positive exponents only.

Default/--check: compare committed compact tables, without modifying them.
--write: explicitly replace compact tables. --export DIR: write the full atlas
(including all fibers, cycles and vertex orbits) into a separate directory.
Only the Python standard library is used; no network calls.
"""
from __future__ import annotations
import argparse
from collections import Counter
import csv
import io
import json
from math import gcd, isqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'power-atlas-v1'
MOD = 360
LIMIT = 1_000_000
UNITS = [a for a in range(MOD) if gcd(a, MOD) == 1]


def require(test: bool, message: str) -> None:
    if not test:
        raise RuntimeError(message)


def representative(k: int) -> int:
    if k < 1:
        raise ValueError('positive exponents only')
    return k if k <= 2 else 3 + (k - 3) % 12


def encode_csv(header: list, rows: list) -> bytes:
    stream = io.StringIO(newline='')
    writer = csv.writer(stream, lineterminator='\n')
    writer.writerow(header)
    writer.writerows(rows)
    return stream.getvalue().encode('utf-8')


def walk(f: list[int], start: int) -> tuple[list, list]:
    path, positions = [], {}
    x = start
    while x not in positions:
        positions[x] = len(path)
        path.append(x)
        x = f[x]
    mu = positions[x]
    cycle = path[mu:]
    j = cycle.index(min(cycle))
    canonical = cycle[j:] + cycle[:j]
    return [start, mu, len(cycle), x, min(cycle)], canonical


def analyze(k: int) -> dict:
    f = [pow(a, k, MOD) for a in range(MOD)]
    fibers = [[] for _ in range(MOD)]
    for a, b in enumerate(f):
        fibers[b].append(a)
    nodes, cycles = [], set()
    for a in range(MOD):
        row, cycle = walk(f, a)
        nodes.append(row)
        cycles.add(tuple(cycle))
    unit_fibers = Counter(f[a] for a in UNITS)
    require(len(set(unit_fibers.values())) == 1, 'nonuniform unit fibers')
    summary = [k, len(set(f)), len(unit_fibers), next(iter(unit_fibers.values())),
               sum(a == f[a] for a in range(MOD)), sum(len(c) == 2 for c in cycles),
               sum(len(c) for c in cycles), max(row[1] for row in nodes)]
    summary += [sum(row[1] == h for row in nodes) for h in range(3)]
    summary += [sum(a == f[a] for a in UNITS)]
    return {'k': k, 'successors': f, 'fibers': fibers, 'nodes': nodes,
            'cycles': [list(c) for c in sorted(cycles)], 'summary': summary,
            'fiber_size_histogram': sorted(Counter(map(len, fibers)).items())}


def build() -> tuple[dict[str, bytes], bytes]:
    maps = [analyze(k) for k in range(1, 15)]
    maps_csv = encode_csv(['r'] + [f'k{k}' for k in range(1, 15)],
                         [[a] + [m['successors'][a] for m in maps] for a in range(MOD)])
    columns = ['k', 'image', 'unit_image', 'unit_fiber', 'fixed_points',
               'two_cycles', 'periodic_points', 'max_tail', 'tail_0', 'tail_1', 'tail_2',
               'unit_fixed_points']
    summary_csv = encode_csv(columns, [m['summary'] for m in maps])
    comp_csv = encode_csv(['k'] + [f'k{j}' for j in range(1, 15)],
                         [[k] + [representative(k*j) for j in range(1, 15)] for k in range(1, 15)])
    # Proper prime powers p^e <= LIMIT, e >= 2, hence p <= sqrt(LIMIT).
    bound = isqrt(LIMIT)
    prime = bytearray(b'\x01') * (bound + 1)
    prime[0] = prime[1] = 0
    for p in range(2, isqrt(bound) + 1):
        if prime[p]:
            prime[p*p:bound+1:p] = b'\x00' * ((bound-p*p)//p + 1)
    witnesses = []
    for p in range(2, bound + 1):
        if not prime[p]:
            continue
        value, e = p*p, 2
        while value <= LIMIT:
            witnesses.append([value, p, e, value % MOD])
            value *= p
            e += 1
    witnesses.sort()
    power_rows = []
    e = 2
    while 2**e <= LIMIT:
        selected = [v for v in witnesses if v[2] == e]
        power_rows.append([e, representative(e), len(selected),
                           sum(v[1] > 5 for v in selected)])
        e += 1
    tables = {'maps.csv': maps_csv, 'summary.csv': summary_csv,
              'composition.csv': comp_csv,
              'prime-power-witnesses.csv': encode_csv(['n', 'prime', 'exponent', 'residue'], witnesses),
              'prime-powers.csv': encode_csv(['exponent', 'map_representative', 'all', 'p_gt_5'], power_rows)}
    full = {'schema': 'mod360-power-atlas-v1', 'modulus': MOD,
            'positive_exponent_representatives': list(range(1, 15)),
            'node_columns': ['r', 'tail', 'period', 'first_cycle_vertex', 'cycle_minimum'],
            'prime_power_bound': LIMIT, 'maps': maps}
    expanded = (json.dumps(full, sort_keys=True, separators=(',', ':')) + '\n').encode()
    return tables, expanded


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    mode.add_argument('--export', type=Path)
    args = parser.parse_args()
    tables, expanded = build()
    if args.export is not None:
        args.export.mkdir(parents=True, exist_ok=True)
        for name, data in tables.items():
            (args.export / name).write_bytes(data)
        (args.export / 'expanded-atlas.json').write_bytes(expanded)
    elif args.write:
        OUT.mkdir(parents=True, exist_ok=True)
        for name, data in tables.items():
            (OUT / name).write_bytes(data)
    else:
        for name, data in tables.items():
            require((OUT / name).is_file() and (OUT / name).read_bytes() == data,
                    f'table mismatch: {name}')
    print('POWER ATLAS: 14 maps, 5040 vertex records; ' +
          ('EXPORTED' if args.export is not None else 'WROTE' if args.write else 'MATCH'))


if __name__ == '__main__':
    main()
