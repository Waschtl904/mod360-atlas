# Novelty Ledger

This ledger records novelty work only. Mathematical verification is tracked separately in `CLAIMS.md` and `exact/`.

## Clearly classical / prior art

- CRT decomposition and unit-group structure.
- regular residues modulo \(n\) and their count.
- wheel sieving modulo 30/360.
- power images in finite abelian groups.
- GCD-defined circulant graphs and Ramanujan-sum spectra.
- cyclotomic fixed fields and Frobenius classes.

## Project-level syntheses, not novelty claims

The following are useful syntheses in this investigation but are **not** currently claimed to be new to mathematics:

- viewing MOD 360 as MOD 30 plus a 12-element nilpotent depth;
- identifying the same 12-element unit fiber simultaneously as additive coset \(u+(30)\) and multiplicative coset \(u(1+(30))\);
- the depth-coordinate multiplication law \(j\star k=j+k+6jk\pmod{12}\);
- organizing prime-capability, factorization-exponent support, square hexagon, and nilpotent depth in one atlas;
- using the same 24 divisors to organize both points by \(\gcd(x,360)\) and affine pair-relations by \(\gcd(x-y,360)\).

## Claims requiring targeted novelty audit

| Claim-ID | Current code | Search target | Status |
|---|---|---|---|
| M360-007 | `V360 + NH + ?[O]` | additive/multiplicative coincidence of the 12-element unit fiber | open |
| M360-008 | `V360 + NH + ?[O]` | explicit depth law \(j\star k=j+k+6jk\) and general formulations | open |
| M360-009 | `V360 + NH + ?[O]` | square-zero six-layer interpretation | open |
| M360-010 | `V360 + NH + ?[O]` | double-hexagon intersection formulation | open |
| M360-012 | `V360 + NH + ?[O]` | canonical \(x^{13}\)+nilpotent orthogonal-product decomposition | open |

Historical operator/affine formulations under `discoveries/` remain `RE-AUDIT` until mathematical and prior-art audits are complete.

## Audit protocol before `NEW`

1. Normalize the theorem statement and list synonyms/generalizations.
2. Check standard texts/handbooks and general theorems that may contain the claim as a special case.
3. Search MathSciNet, zbMATH, arXiv, Google Scholar, and relevant full-text sources where accessible.
4. Follow backward and forward citations of close results.
5. Record dates, databases, queries, positive hits, and negative-search limitations.
6. Obtain at least one independent mathematical review.
7. Only then consider promotion to `NEW`.

Every `NEW` promotion needs its own dated section with theorem wording, audit scope, possible counter-prior-art, rationale, and residual uncertainty.
