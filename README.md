# MOD 360 Atlas

A cumulative, reproducible research atlas for the arithmetic, algebra, prime-capable residue classes, composite-factorization patterns, dynamics, harmonic structure, and exploratory geometry of

\[
\mathbb Z/360\mathbb Z,\qquad 360=2^3\cdot3^2\cdot5.
\]

> **Working principle:** exact computation is not the same as mathematical novelty. Every promoted statement receives a claim ID, an evidence level, a status, and—where needed—a separate prior-art record.

## Goal

The goal is **completeness first, discovery second**:

1. organize the known structure of modulo 360 without treating it as uninteresting;
2. understand all 360 residue classes, not only the 96 units;
3. place primes and non-primes in the same structural atlas;
4. separate consequences of CRT, finite-group theory and sieving from genuinely additional phenomena;
5. preserve every promising observation, but promote only audited claims.

This repository does **not** claim a connection to the Riemann Hypothesis or Object X. Any future bridge must be stated and proved separately.

## Two-level picture

The first structural split is

\[
\mathbb Z/360\mathbb Z \longrightarrow \mathbb Z/30\mathbb Z.
\]

The nilradical is

\[
N=(30),\quad |N|=12,\quad N^2=(180),\quad N^3=0,
\]

so

\[
(\mathbb Z/360\mathbb Z)/N\cong\mathbb Z/30\mathbb Z.
\]

Thus MOD 30 controls coarse divisibility by \(2,3,5\), while MOD 360 adds the finer \(2^3\)- and \(3^2\)-depth.

For primes \(p>5\), prime-capability is exactly \(\gcd(r,360)=1\), equivalently \(\gcd(r,30)=1\). The 96 prime-capable MOD-360 classes are therefore 12 lifts of the 8 MOD-30 wheel classes.

## Status and evidence

Status codes:

- `K` — known/classical;
- `V360` — exact for modulus 360;
- `NH` — new within this investigation only;
- `?[O]` — literature novelty unresolved;
- `NEW` — only after documented prior-art audit and independent review;
- `RE-AUDIT` — historical finding preserved but not in the current Core.

Evidence levels run from `E0` (informal observation) to `E4` (independently reproduced/reviewed). See `STATUS.md`.

## Core headline facts

\[
U(360)\cong C_{12}\times C_2^3,\qquad |U(360)|=96.
\]

The square image is

\[
U(360)^2=\{1,49,121,169,241,289\}\cong C_6.
\]

The regular skeleton is

\[
M=\operatorname{im}(x\mapsto x^{13})=\operatorname{Reg}(\mathbb Z/360\mathbb Z),\qquad |M|=175.
\]

Every residue has the exact decomposition

\[
x=x^{13}+(x-x^{13}),\qquad x-x^{13}\in(30),\qquad x^{13}(x-x^{13})=0.
\]

The 24 divisors of 360 index both point strata \(\{x:\gcd(x,360)=d\}\) and affine relation strata \(\{(x,y):\gcd(x-y,360)=d\}\). The relation layer is diagonalized by additive Fourier characters with Ramanujan-sum eigenvalues.

## Repository map

- `atlas/` — GCD strata, MOD-30 depth, regular/nilpotent structure, class-level material.
- `units/` — unit group, power images, square hexagon, congruence hexagon.
- `primes/` — wheel geometry, admissibility, prime-gap residue constraints.
- `composites/` — factorization-exponent taxonomy and future composite atlases.
- `dynamics/` — power maps and functional-graph questions.
- `harmonic/` — additive Fourier/GCD graphs/Ramanujan sums.
- `galois/` — cyclotomic and Frobenius interpretation of the square quotient.
- `graphs/` — graph-oriented extensions and relation schemes.
- `discoveries/` — candidates and historical findings, conservatively labelled.
- `exact/` — dependency-free exact verifiers and atlas generators.
- `data/` — generated tables.
- `certificates/` — reproducible machine-readable outputs.
- `literature/` — prior-art ledger.

## Start here

1. Read `STATUS.md` and `CLAIMS.md`.
2. Rebuild the generated atlas: `python exact/generate_atlas.py`.
3. Run the exhaustive Core verifier: `python exact/verify_core.py`.
4. Put observations into `discoveries/` before promoting them to theorem-level claims.
5. Use `NOVELTY_LEDGER.md` for novelty work; do not infer novelty from exact verification.

## Reproduce

```bash
python exact/generate_atlas.py
python exact/verify_core.py
git diff --exit-code -- data certificates
```

The reference scripts use only the Python standard library.

## Citation

Until a formal release is archived, cite the repository URL together with the exact commit SHA and access date. `CITATION.cff` is retained as the machine-readable citation record.
