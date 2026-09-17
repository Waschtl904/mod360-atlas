#!/usr/bin/env python3
"""Independent verifier for least-prime-factor-v1.

Algorithm B scans integers with a smallest-prime-factor table.  It does not
import the generator and does not enumerate prime pairs as its counting engine.
"""
from __future__ import annotations

import csv
import hashlib
import json
from array import array
from collections import defaultdict
from fractions import Fraction
from math import gcd, isqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "least-prime-factor-v1"
CERT = ROOT / "certificates" / "least-prime-factor-v1.json"
PARENT = ROOT / "data" / "multiscale-v1" / "counts.csv"

BOUNDS = (36_000, 360_000, 3_600_000)
UNITS = tuple(r for r in range(360) if gcd(r, 360) == 1)
UIDX = {r: i for i, r in enumerate(UNITS)}
Q = frozenset((1, 49, 121, 169, 241, 289))
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


def spf_table(limit: int) -> array:
    """Smallest-prime-factor table for direct integer classification."""
    spf = array("I", [0]) * (limit + 1)
    for p in range(2, limit + 1):
        if spf[p] == 0:
            spf[p] = p
            if p <= isqrt(limit):
                for n in range(p * p, limit + 1, p):
                    if spf[n] == 0:
                        spf[n] = p
    return spf


def contrast(v: list[int]) -> tuple[str, str, str, tuple[int, int, int, int]]:
    q = sum(v[UIDX[r]] for r in Q)
    amq = sum(v[UIDX[r]] for r in A - Q)
    uma = sum(v[UIDX[r]] for r in set(UNITS) - A)
    total = q + amq + uma
    d = Fraction(amq + uma, 90) - Fraction(q, 6)
    f = Fraction(amq, 18) - Fraction(q, 6)
    c = Fraction(uma, 72) - Fraction(q + amq, 24)
    require(d == Fraction(4, 5) * (f + c), "contrast identity")
    return str(d), str(f), str(c), (total, q, amq, uma)


def build_views() -> dict[tuple[str, int, int], dict[int, list[int]]]:
    """Scan n once; classify n=p*q by its least prime p and prime cofactor q."""
    limit = BOUNDS[-1]
    spf = spf_table(limit)
    views = {
        ("cumulative", 0, 36_000): defaultdict(lambda: [0] * len(UNITS)),
        ("cumulative", 0, 360_000): defaultdict(lambda: [0] * len(UNITS)),
        ("cumulative", 0, 3_600_000): defaultdict(lambda: [0] * len(UNITS)),
        ("interval", 0, 36_000): defaultdict(lambda: [0] * len(UNITS)),
        ("interval", 36_000, 360_000): defaultdict(lambda: [0] * len(UNITS)),
        ("interval", 360_000, 3_600_000): defaultdict(lambda: [0] * len(UNITS)),
    }
    for n in range(2, limit + 1):
        p = spf[n]
        q = n // p
        if p <= 5 or not (p < q) or q < 2 or spf[q] != q:
            continue
        r = n % 360
        require(r in UIDX, "unit residue expected")
        idx = UIDX[r]
        for hi in BOUNDS:
            if n <= hi:
                views[("cumulative", 0, hi)][p][idx] += 1
        if n <= 36_000:
            ikey = ("interval", 0, 36_000)
        elif n <= 360_000:
            ikey = ("interval", 36_000, 360_000)
        else:
            ikey = ("interval", 360_000, 3_600_000)
        views[ikey][p][idx] += 1
    return {k: dict(v) for k, v in views.items()}


def sum_vectors(rows: dict[int, list[int]], pred=lambda p: True) -> list[int]:
    out = [0] * len(UNITS)
    for p, vec in rows.items():
        if pred(p):
            for i, x in enumerate(vec):
                out[i] += x
    return out


def read_committed_summary() -> dict[tuple[str, int, int], dict[int, tuple[str, ...]]]:
    path = DATA / "by-p-summary.csv"
    require(path.is_file(), "missing by-p-summary.csv")
    result = defaultdict(dict)
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            key = (row["kind"], int(row["lower_exclusive"]), int(row["upper_inclusive"]))
            p = int(row["p"])
            vals = (row["p_mod30"], row["total_units"], row["q_total"],
                    row["a_minus_q_total"], row["u_minus_a_total"],
                    row["delta"], row["delta_fine"], row["delta_coarse"])
            require(p not in result[key], "duplicate p row")
            result[key][p] = vals
    return dict(result)


def computed_summary(views: dict) -> dict[tuple[str, int, int], dict[int, tuple[str, ...]]]:
    out = {}
    for key, rows in views.items():
        dst = {}
        for p, vec in rows.items():
            d, fi, co, (t, q, amq, uma) = contrast(vec)
            dst[p] = (str(p % 30), str(t), str(q), str(amq), str(uma), d, fi, co)
        out[key] = dst
    return out


def expanded_bytes(views: dict) -> bytes:
    import io
    header = [
        "kind", "lower_exclusive", "upper_inclusive", "p", "p_mod30",
        "total_units", "q_total", "a_minus_q_total", "u_minus_a_total",
        "delta", "delta_fine", "delta_coarse",
    ] + [f"r{r:03d}" for r in UNITS]
    s = io.StringIO(newline="")
    w = csv.writer(s, lineterminator="\n")
    w.writerow(header)
    order = (("cumulative", 0, 36_000), ("cumulative", 0, 360_000),
             ("cumulative", 0, 3_600_000), ("interval", 0, 36_000),
             ("interval", 36_000, 360_000), ("interval", 360_000, 3_600_000))
    for key in order:
        kind, lo, hi = key
        for p in sorted(views[key]):
            vec = views[key][p]
            d, fi, co, (t, q, amq, uma) = contrast(vec)
            w.writerow([kind, lo, hi, p, p % 30, t, q, amq, uma, d, fi, co, *vec])
    return s.getvalue().encode()

def read_parent() -> dict[int, list[int]]:
    with PARENT.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    require(len(rows) == 360, "parent row count")
    out = {}
    for b in BOUNDS:
        out[b] = [
            int(rows[r][f"semiprimes_{b}"]) - int(rows[r][f"prime_squares_{b}"])
            for r in UNITS
        ]
    return out


def parent_window(parent: dict[int, list[int]], lo: int, hi: int) -> list[int]:
    return [parent[hi][i] - (parent[lo][i] if lo else 0) for i in range(len(UNITS))]


def expected_diag_rows(views: dict) -> list[list[str]]:
    rows = views[("interval", 36_000, 360_000)]
    out = []

    def add(gt: str, name: str, pred=lambda p: True) -> None:
        ps = [p for p in rows if pred(p)]
        v = sum_vectors(rows, pred)
        d, f, c, (t, q, amq, uma) = contrast(v)
        out.append([gt, name, str(len(ps)), str(t), str(q), str(amq), str(uma), d, f, c])

    cut = isqrt(36_000)
    add("all", "middle interval")
    add("lower-bound regime", f"p<={cut}", lambda p: p <= cut)
    add("lower-bound regime", f"p>{cut}", lambda p: p > cut)
    add("factor MOD30 family", "p mod30 in {1,19}", lambda p: p % 30 in H30)
    add("factor MOD30 family", "p mod30 outside {1,19}", lambda p: p % 30 not in H30)
    for an, apred in ((f"p<={cut}", lambda p: p <= cut), (f"p>{cut}", lambda p: p > cut)):
        for fn, fpred in (("p mod30 in {1,19}", lambda p: p % 30 in H30),
                          ("p mod30 outside {1,19}", lambda p: p % 30 not in H30)):
            add("cross", an + " & " + fn, lambda p, a=apred, b=fpred: a(p) and b(p))
    for s in (1, 7, 11, 13, 17, 19, 23, 29):
        add("p mod30", str(s), lambda p, s=s: p % 30 == s)

    # Product blocks are verified directly from the integer scan, not reconstructed
    # from the whole middle interval.
    for lo in range(36_000, 360_000, 36_000):
        hi = lo + 36_000
        block = defaultdict(lambda: [0] * len(UNITS))
        # We can reuse the already-built interval views only if we know n; rebuild a
        # local SPF scan for these diagnostic rows below in verify_diagnostics().
        out.append(["product block", f"({lo},{hi}]", "__DEFER__", "", "", "", "", "", "", ""])
    return out


def product_block_rows() -> dict[str, list[str]]:
    limit = 360_000
    spf = spf_table(limit)
    blocks = {f"({lo},{lo+36_000}]": defaultdict(lambda: [0] * len(UNITS))
              for lo in range(36_000, 360_000, 36_000)}
    for n in range(36_001, 360_001):
        p = spf[n]
        q = n // p
        if p <= 5 or not (p < q) or spf[q] != q:
            continue
        lo = ((n - 1) // 36_000) * 36_000
        if lo < 36_000:
            continue
        name = f"({lo},{lo+36_000}]"
        blocks[name][p][UIDX[n % 360]] += 1
    out = {}
    for name, rows in blocks.items():
        v = sum_vectors(dict(rows))
        d, f, c, (t, q, amq, uma) = contrast(v)
        out[name] = [str(len(rows)), str(t), str(q), str(amq), str(uma), d, f, c]
    return out


def verify_diagnostics(views: dict) -> None:
    path = DATA / "middle-diagnostics.csv"
    with path.open(newline="", encoding="utf-8") as f:
        committed = [row for row in csv.DictReader(f)]
    base_expected = expected_diag_rows(views)
    block = product_block_rows()
    require(len(committed) == len(base_expected), "diagnostic row count")
    for got, exp in zip(committed, base_expected):
        prefix = [got["group_type"], got["group"]]
        require(prefix == exp[:2], f"diagnostic ordering/key mismatch: {prefix} != {exp[:2]}")
        if got["group_type"] == "product block":
            vals = block[got["group"]]
            exp = [got["group_type"], got["group"], *vals]
        gotvals = [got["group_type"], got["group"], got["p_count"], got["total_units"],
                   got["q_total"], got["a_minus_q_total"], got["u_minus_a_total"],
                   got["delta"], got["delta_fine"], got["delta_coarse"]]
        require(gotvals == exp, f"diagnostic mismatch: {got['group_type']} {got['group']}")


def verify_certificate(views: dict) -> None:
    with CERT.open(encoding="utf-8") as f:
        cert = json.load(f)
    require(cert["schema"] == "mod360-least-prime-factor-v1", "certificate schema")
    for name in ("by-p-summary.csv", "middle-diagnostics.csv"):
        raw = (DATA / name).read_bytes()
        require(hashlib.sha256(raw).hexdigest() == cert["files"][name], f"hash mismatch {name}")
    expanded = expanded_bytes(views)
    require(hashlib.sha256(expanded).hexdigest() == cert["expanded_by_p_residues_sha256"],
            "expanded 96-residue table hash mismatch")
    require(sum(len(rows) for rows in views.values()) == cert["expanded_rows"],
            "expanded row count mismatch")

def main() -> None:
    computed = build_views()
    committed = read_committed_summary()
    summary = computed_summary(computed)
    require(set(computed) == set(EXPECTED) == set(committed), "view keys mismatch")
    require(summary == committed, "per-p summary mismatch")

    parent = read_parent()
    for key in EXPECTED:
        v = sum_vectors(computed[key])
        kind, lo, hi = key
        require(v == parent_window(parent, lo, hi), f"parent 96-vector mismatch: {key}")
        d, f, c, _ = contrast(v)
        require((d, f, c) == EXPECTED[key], f"aggregate contrast mismatch: {key}")

    # Natural lower-bound split: p<=sqrt(lo) iff lo/p >= p for the middle window.
    require(isqrt(36_000) == 189 and 189 * 189 <= 36_000 < 190 * 190, "sqrt boundary")
    require(all(p <= 189 or p >= 191 for p in computed[("interval", 36_000, 360_000)]),
            "unexpected prime boundary")

    verify_diagnostics(computed)
    verify_certificate(computed)

    # Mutation rejection: a single changed residue must alter the bound expanded table.
    key = ("interval", 36_000, 360_000)
    p = min(computed[key])
    mutated = {k: {pp: vv[:] for pp, vv in rows.items()} for k, rows in computed.items()}
    original_hash = hashlib.sha256(expanded_bytes(computed)).hexdigest()
    mutated[key][p][0] += 1
    require(hashlib.sha256(expanded_bytes(mutated)).hexdigest() != original_hash,
            "mutation test failed")

    print("LEAST-PRIME-FACTOR VERIFY: PASS")


if __name__ == "__main__":
    main()
