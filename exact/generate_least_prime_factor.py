#!/usr/bin/env python3
"""Exact decomposition of distinct semiprimes pq (5<p<q) by the smaller prime p.

The modulus stays 360.  Reference views are exactly the cumulative bounds
36,000 / 360,000 / 3,600,000 and the corresponding disjoint intervals from
the multiscale-v1 module.  Default/--check is read-only; --write regenerates
the committed tables.
"""
from __future__ import annotations

import argparse
import bisect
import csv
import hashlib
import io
import json
from collections import defaultdict
from fractions import Fraction
from math import gcd, isqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "least-prime-factor-v1"
CERT = ROOT / "certificates" / "least-prime-factor-v1.json"
PARENT = ROOT / "data" / "multiscale-v1" / "counts.csv"

BOUNDS = (36_000, 360_000, 3_600_000)
UNITS = tuple(r for r in range(360) if gcd(r, 360) == 1)
UIDX = {r: i for i, r in enumerate(UNITS)}
Q = frozenset({1, 49, 121, 169, 241, 289})
A = frozenset(r for r in UNITS if r % 30 in (1, 19))
H30 = frozenset((1, 19))

EXPECTED = {
    ("cumulative", 0, 36_000): ("82/45", "37/18", "2/9"),
    ("cumulative", 0, 360_000): ("191/90", "4/3", "95/72"),
    ("cumulative", 0, 3_600_000): ("623/90", "85/9", "-19/24"),
    ("interval", 0, 36_000): ("82/45", "37/18", "2/9"),
    ("interval", 36_000, 360_000): ("3/10", "-13/18", "79/72"),
    ("interval", 360_000, 3_600_000): ("24/5", "73/9", "-19/9"),
}


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def primes_upto(limit: int) -> list[int]:
    """Algorithm A: Eratosthenes plus explicit prime-pair enumeration."""
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for p in range(2, isqrt(limit) + 1):
        if sieve[p]:
            sieve[p*p:limit+1:p] = b"\x00" * (((limit - p*p) // p) + 1)
    return [n for n in range(2, limit + 1) if sieve[n]]


def contrast(v: list[int]) -> tuple[Fraction, Fraction, Fraction, tuple[int, int, int, int]]:
    q = sum(v[UIDX[r]] for r in Q)
    amq = sum(v[UIDX[r]] for r in A - Q)
    uma = sum(v[UIDX[r]] for r in set(UNITS) - A)
    total = q + amq + uma
    delta = Fraction(amq + uma, 90) - Fraction(q, 6)
    fine = Fraction(amq, 18) - Fraction(q, 6)
    coarse = Fraction(uma, 72) - Fraction(q + amq, 24)
    require(delta == Fraction(4, 5) * (fine + coarse), "contrast identity failed")
    return delta, fine, coarse, (total, q, amq, uma)


def rows_for_window(primes: list[int], lo: int, hi: int) -> dict[int, list[int]]:
    """Enumerate each unordered pair once, indexed by its smaller prime p."""
    out: dict[int, list[int]] = {}
    for p in primes:
        if p <= 5:
            continue
        if p * p >= hi:
            break
        # q>p, lo < p*q <= hi.
        left = bisect.bisect_right(primes, max(p, lo // p))
        right = bisect.bisect_right(primes, hi // p)
        if left >= right:
            continue
        vec = [0] * len(UNITS)
        for q in primes[left:right]:
            n = p * q
            require(lo < n <= hi and p < q, "pair boundary/order failure")
            r = n % 360
            require(r in UIDX, "p,q>5 product must be a unit modulo 360")
            vec[UIDX[r]] += 1
        if any(vec):
            out[p] = vec
    return out


def all_views(primes: list[int]) -> dict[tuple[str, int, int], dict[int, list[int]]]:
    views = {}
    for hi in BOUNDS:
        views[("cumulative", 0, hi)] = rows_for_window(primes, 0, hi)
    prev = 0
    for hi in BOUNDS:
        views[("interval", prev, hi)] = rows_for_window(primes, prev, hi)
        prev = hi
    return views


def sum_vectors(rows: dict[int, list[int]], predicate=lambda p: True) -> list[int]:
    out = [0] * len(UNITS)
    for p, vec in rows.items():
        if predicate(p):
            for i, n in enumerate(vec):
                out[i] += n
    return out


def read_parent_vectors() -> dict[int, list[int]]:
    require(PARENT.is_file(), f"missing parent data: {PARENT}")
    with PARENT.open(newline="", encoding="utf-8") as f:
        records = list(csv.DictReader(f))
    require(len(records) == 360, "parent counts.csv must have 360 rows")
    result = {}
    for b in BOUNDS:
        sem = f"semiprimes_{b}"
        sq = f"prime_squares_{b}"
        require(sem in records[0] and sq in records[0], f"parent columns missing for {b}")
        result[b] = [int(records[r][sem]) - int(records[r][sq]) for r in UNITS]
    return result


def parent_window(parent: dict[int, list[int]], lo: int, hi: int) -> list[int]:
    return [parent[hi][i] - (parent[lo][i] if lo else 0) for i in range(len(UNITS))]


def check_parent(views: dict, parent: dict[int, list[int]]) -> None:
    for key, rows in views.items():
        kind, lo, hi = key
        total = sum_vectors(rows)
        require(total == parent_window(parent, lo, hi),
                f"full 96-class vector mismatch against multiscale-v1: {key}")
        d, f, c, _ = contrast(total)
        expected = EXPECTED[key]
        require((str(d), str(f), str(c)) == expected,
                f"contrast mismatch {key}: {(d, f, c)} != {expected}")


def csv_bytes(header: list[str], rows: list[list[object]]) -> bytes:
    s = io.StringIO(newline="")
    w = csv.writer(s, lineterminator="\n")
    w.writerow(header)
    w.writerows(rows)
    return s.getvalue().encode()


def render_by_p(views: dict, include_residues: bool) -> bytes:
    header = [
        "kind", "lower_exclusive", "upper_inclusive", "p", "p_mod30",
        "total_units", "q_total", "a_minus_q_total", "u_minus_a_total",
        "delta", "delta_fine", "delta_coarse",
    ]
    if include_residues:
        header += [f"r{r:03d}" for r in UNITS]
    body = []
    for key in (("cumulative", 0, 36_000), ("cumulative", 0, 360_000),
                ("cumulative", 0, 3_600_000), ("interval", 0, 36_000),
                ("interval", 36_000, 360_000), ("interval", 360_000, 3_600_000)):
        kind, lo, hi = key
        for p in sorted(views[key]):
            vec = views[key][p]
            d, f, c, (t, q, amq, uma) = contrast(vec)
            row = [kind, lo, hi, p, p % 30, t, q, amq, uma,
                   str(d), str(f), str(c)]
            if include_residues:
                row += vec
            body.append(row)
    return csv_bytes(header, body)

def diag_row(group_type: str, group: str, rows: dict[int, list[int]],
             predicate=lambda p: True) -> list[object]:
    selected = [p for p in rows if predicate(p)]
    vec = sum_vectors(rows, predicate)
    d, f, c, (t, q, amq, uma) = contrast(vec)
    return [group_type, group, len(selected), t, q, amq, uma, str(d), str(f), str(c)]


def render_middle_diagnostics(views: dict, primes: list[int]) -> bytes:
    key = ("interval", 36_000, 360_000)
    rows = views[key]
    body = [diag_row("all", "middle interval", rows)]

    cut = isqrt(36_000)  # 189; next prime is 191.
    body += [
        diag_row("lower-bound regime", f"p<={cut}", rows, lambda p: p <= cut),
        diag_row("lower-bound regime", f"p>{cut}", rows, lambda p: p > cut),
        diag_row("factor MOD30 family", "p mod30 in {1,19}", rows,
                 lambda p: p % 30 in H30),
        diag_row("factor MOD30 family", "p mod30 outside {1,19}", rows,
                 lambda p: p % 30 not in H30),
    ]
    for active_name, active in ((f"p<={cut}", lambda p: p <= cut),
                                (f"p>{cut}", lambda p: p > cut)):
        for fam_name, fam in (("p mod30 in {1,19}", lambda p: p % 30 in H30),
                              ("p mod30 outside {1,19}", lambda p: p % 30 not in H30)):
            body.append(diag_row("cross", active_name + " & " + fam_name, rows,
                                 lambda p, a=active, b=fam: a(p) and b(p)))
    for s in (1, 7, 11, 13, 17, 19, 23, 29):
        body.append(diag_row("p mod30", str(s), rows, lambda p, s=s: p % 30 == s))

    # Natural 36,000-wide product blocks partition the middle interval.
    for lo in range(36_000, 360_000, 36_000):
        hi = lo + 36_000
        block = rows_for_window(primes, lo, hi)
        body.append(diag_row("product block", f"({lo},{hi}]", block))

    return csv_bytes(
        ["group_type", "group", "p_count", "total_units", "q_total",
         "a_minus_q_total", "u_minus_a_total", "delta", "delta_fine", "delta_coarse"],
        body,
    )


def certificate(tables: dict[str, bytes], expanded: bytes, expanded_rows: int) -> bytes:
    payload = {
        "schema": "mod360-least-prime-factor-v1",
        "modulus": 360,
        "bounds": list(BOUNDS),
        "pair_condition": "5 < p < q prime; lo < p*q <= hi",
        "unit_residues": list(UNITS),
        "square_hexagon": sorted(Q),
        "family_A": sorted(A),
        "files": {name: hashlib.sha256(data).hexdigest() for name, data in sorted(tables.items())},
        "expanded_by_p_residues_sha256": hashlib.sha256(expanded).hexdigest(),
        "expanded_rows": expanded_rows,
        "parent": "data/multiscale-v1/counts.csv",
        "expected_contrasts": {
            "|".join(map(str, k)): list(v) for k, v in sorted(EXPECTED.items())
        },
    }
    return (json.dumps(payload, sort_keys=True, indent=2) + "\n").encode()

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--export", type=Path)
    args = ap.parse_args()

    primes = primes_upto(BOUNDS[-1])
    views = all_views(primes)
    parent = read_parent_vectors()
    check_parent(views, parent)

    summary = render_by_p(views, include_residues=False)
    expanded = render_by_p(views, include_residues=True)
    tables = {
        "by-p-summary.csv": summary,
        "middle-diagnostics.csv": render_middle_diagnostics(views, primes),
    }
    cert = certificate(tables, expanded, sum(len(rows) for rows in views.values()))

    if args.export is not None:
        args.export.mkdir(parents=True, exist_ok=True)
        for name, data in tables.items():
            (args.export / name).write_bytes(data)
        (args.export / "by-p-residues.csv").write_bytes(expanded)
        (args.export / "certificate.json").write_bytes(cert)
        print("LEAST-PRIME-FACTOR: EXPORTED")
    elif args.write:
        OUT.mkdir(parents=True, exist_ok=True)
        CERT.parent.mkdir(parents=True, exist_ok=True)
        for name, data in tables.items():
            (OUT / name).write_bytes(data)
        CERT.write_bytes(cert)
        old = OUT / "by-p.csv"
        if old.exists():
            old.unlink()
        print("LEAST-PRIME-FACTOR: WROTE")
    else:
        for name, data in tables.items():
            require((OUT / name).is_file() and (OUT / name).read_bytes() == data,
                    f"artifact mismatch: {name}")
        require(CERT.is_file() and CERT.read_bytes() == cert, "certificate mismatch")
        print("LEAST-PRIME-FACTOR: MATCH")


if __name__ == "__main__":
    main()
