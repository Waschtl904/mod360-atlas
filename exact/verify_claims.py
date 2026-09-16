#!/usr/bin/env python3
"""Exhaustively verify the initial finite claims for modulus 360."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from math import gcd
from pathlib import Path

MODULUS = 360
CERT_DIR = Path(__file__).resolve().parent / "certificates"


def units() -> list[int]:
    return [a for a in range(MODULUS) if gcd(a, MODULUS) == 1]


def is_nilpotent(a: int) -> bool:
    x = a % MODULUS
    for _ in range(1, 13):
        if x == 0:
            return True
        x = (x * a) % MODULUS
    return False


def is_regular(a: int) -> bool:
    return any((a * a * x - a) % MODULUS == 0 for x in range(MODULUS))


def multiplicative_order(a: int) -> int:
    x = 1
    for k in range(1, 13):
        x = (x * a) % MODULUS
        if x == 1:
            return k
    raise AssertionError(f"No order found for unit {a}")


def lcm(a: int, b: int) -> int:
    return a * b // gcd(a, b)


def verify() -> dict[str, object]:
    us = units()
    crt_tuples = {(a % 8, a % 9, a % 5) for a in range(MODULUS)}
    idempotents = [a for a in range(MODULUS) if pow(a, 2, MODULUS) == a]
    nilpotents = [a for a in range(MODULUS) if is_nilpotent(a)]
    regular = [a for a in range(MODULUS) if is_regular(a)]
    exponent = 1
    for a in us:
        exponent = lcm(exponent, multiplicative_order(a))

    assertions = {
        "M360-001_phi": len(us) == 96,
        "M360-002_crt_bijection": len(crt_tuples) == 360,
        "M360-003_idempotents": len(idempotents) == 8,
        "M360-004_nilpotents": len(nilpotents) == 12,
        "M360-005_unit_exponent": exponent == 12 and all(pow(a, 12, MODULUS) == 1 for a in us),
        "M360-006_regular_elements": len(regular) == 175,
    }
    if not all(assertions.values()):
        raise AssertionError(assertions)

    return {
        "schema": 1,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "modulus": MODULUS,
        "method": "exhaustive enumeration",
        "assertions": assertions,
        "values": {
            "unit_count": len(us),
            "crt_tuple_count": len(crt_tuples),
            "idempotents": idempotents,
            "nilpotents": nilpotents,
            "unit_group_exponent": exponent,
            "regular_element_count": len(regular),
        },
    }


def main() -> None:
    result = verify()
    canonical = json.dumps(result, indent=2, sort_keys=True) + "\n"
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    result["sha256_without_digest"] = digest
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    target = CERT_DIR / "baseline-claims.json"
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"All claims verified; certificate written to {target}")


if __name__ == "__main__":
    main()
