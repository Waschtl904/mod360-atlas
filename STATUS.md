# Status

## Allowed status codes

| Code | Definition | Minimum support |
|---|---|---|
| `K` | known/classical | reliable literature or standard theorem |
| `V360` | exact statement verified for modulus 360 | deterministic exhaustive test or complete proof |
| `NH` | first isolated in this project | dated reproducible project record |
| `?[O]` | literature novelty unresolved | documented but incomplete prior-art search |
| `NEW` | promoted after novelty audit | completed prior-art protocol and independent review |
| `RE-AUDIT` | historical finding preserved but not yet promoted into current Core | clean re-verification required |

## Evidence levels

| Level | Meaning |
|---|---|
| `E0` | informal observation |
| `E1` | reproducible experiment |
| `E2` | exhaustive finite verification |
| `E3` | mathematical proof |
| `E4` | independently reproduced or reviewed |

## V2 Core

The following layers are currently in the reproducible Core:

- CRT decomposition modulo \(8,9,5\).
- 24 GCD point strata.
- 24 affine difference/relation strata.
- complete 24-ideal lattice and annihilator involution.
- identification of GCD shells with ideal-generator shells.
- equality of ring annihilator and additive-Fourier orthogonal complement for the ideal lattice.
- direct-summand/idempotent Boolean sublattice of size 8.
- Jacobson-radical / socle and maximal/minimal annihilator pairing.
- MOD-30 quotient and 12-fold nilpotent depth.
- unit-group order statistics and power images.
- square hexagon \(Q=U(360)^2\).
- congruence/square-zero hexagon \(C=1+(60)\).
- regular skeleton \(M=\operatorname{im}x^{13}\), size 175.
- support idempotents from \(x^{12}\).
- MOD-30 prime wheel and exact tuple-admissibility count.
- composite exponent-gcd residue taxonomy.
- additive Fourier diagonalization of GCD relation graphs.
- sextic square-quotient/Frobenius field description.

The deterministic certificate for this layer is `certificates/core-v2.json`.

## Preserved but not yet promoted

See `discoveries/HISTORICAL_FINDINGS.md` for earlier findings awaiting clean re-audit, including affine regularized symmetries and operator-algebra experiments.

## Object-X firewall

No direct MOD-360 \(\Rightarrow\) Object-X/RH bridge is claimed. MOD 360 is currently treated as an independent structural laboratory.
