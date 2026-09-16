#!/usr/bin/env python3
"""Generate a deterministic atlas for Z/360Z using only the standard library."""

from __future__ import annotations

import csv
import json
from math import gcd
from pathlib import Path

MODULUS = 360
OUT_DIR = Path(__file__).resolve().parents[1] / "atlas" / "000-359"


def is_idempotent(a: int) -> bool:
    return pow(a, 2, MODULUS) == a


def nilpotency_index(a: int) -> int | None:
    x = a % MODULUS
    for k in range(1, 13):
        if x == 0:
            return k
        x = (x * a) % MODULUS
    return None


def regular_witness(a: int) -> int | None:
    for x in range(MODULUS):
        if (a * a * x - a) % MODULUS == 0:
            return x
    return None


def multiplicative_order(a: int) -> int | None:
    if gcd(a, MODULUS) != 1:
        return None
    x = 1
    for k in range(1, 13):
        x = (x * a) % MODULUS
        if x == 1:
            return k
    raise RuntimeError(f"order bound failed for {a}")


def record(a: int) -> dict[str, object]:
    witness = regular_witness(a)
    return {
        "residue": a,
        "gcd_360": gcd(a, MODULUS),
        "mod_8": a % 8,
        "mod_9": a % 9,
        "mod_5": a % 5,
        "unit": gcd(a, MODULUS) == 1,
        "prime_capable_gt_5": gcd(a, MODULUS) == 1,
        "idempotent": is_idempotent(a),
        "nilpotency_index": nilpotency_index(a),
        "von_neumann_regular": witness is not None,
        "regular_witness": witness,
        "multiplicative_order": multiplicative_order(a),
        "square": pow(a, 2, MODULUS),
        "cube": pow(a, 3, MODULUS),
    }


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = [record(a) for a in range(MODULUS)]
    json_path = OUT_DIR / "atlas.json"
    csv_path = OUT_DIR / "atlas.csv"

    json_path.write_text(
        json.dumps({"modulus": MODULUS, "records": rows}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} records to {json_path} and {csv_path}")


if __name__ == "__main__":
    main()
