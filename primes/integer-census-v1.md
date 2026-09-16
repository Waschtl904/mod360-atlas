# Positive-integer census V1: beyond the wheel

**Scope:** modulus 360 throughout; positive integers `1 <= n <= 1,000,000`.
This is a finite, exhaustive dataset and a reviewable extension to Core V3,
not an asymptotic theorem, a new sieve algorithm, or an Object-X/RH claim.

## 1. What this layer adds

Core V3 supplies the 24 ideal/GCD shells and the uniform **abstract residue**
factorization baseline (`M360-019` through `M360-029`). This layer instead
counts **actual positive integers**, with their natural prime factorizations.
The fixed modulus is not enlarged: congruences modulo a trial prime below
are only coordinates for locating its multiples inside a MOD-360 column.

Each of the 360 rows in [residues.csv](../data/integer-census-v1/residues.csv)
contains exposure, primes, composites, squarefree integers, semiprimes,
prime squares, proper prime powers, sums of omega/Omega, and first witnesses.
[summary.json](../data/integer-census-v1/summary.json) adds the global joint
omega/Omega histogram and the eight 12-lift MOD-30 fibers. It does not yet
contain a separate joint histogram for each residue.
[least-factors.json](../data/integer-census-v1/least-factors.json) partitions
composites by their smallest prime factor, both globally and within unit classes.

## 2. Definitions and exact partition

For `n = product p_i^e_i > 1`, define `omega(n) = number of distinct p_i` and
`Omega(n) = sum e_i`; both are zero at 1. This is the natural-integer
factorization, **not** irreducibility in `Z/360Z`.

- Prime: `Omega = 1`; composite: `Omega >= 2`.
- Semiprime: `Omega = 2`, including `p^2` as well as distinct `pq`.
- Squarefree: `omega = Omega`, including 1 by convention.
- Prime square: `omega = 1, Omega = 2`.
- Proper prime power: `omega = 1, Omega >= 2`; primes themselves are excluded.

Zero is excluded from the integer window; row 0 counts positive multiples
of 360. A first-witness entry 0 means none **within this window**, not a proof
of nonexistence. Only `one`, `primes`, and `composites` form a disjoint partition.
All other named categories can overlap.

For `0 <= r < 360`, write `E_X(r)` for the number of positive integers at most
`X` congruent to `r`. Then

```math
E_X(0)=\lfloor X/360\rfloor,\qquad
E_X(r)=\max(0,1+\lfloor(X-r)/360\rfloor)\quad(1\le r<360).
```

With `P_X(r)` and `C_X(r)` the prime/composite counts,

```math
E_X(r)=\mathbf1_{r=1}+P_X(r)+C_X(r)\qquad(X\ge1).
```

Thus a reverse prime/composite count trend is largely an identity, not an
independent discovery. Unequal row exposures must also be accounted for.

## 3. M360-030: exact composite positions inside a fixed column

Let `gcd(r,360)=1`, `n=r+360k >= 2`, and let `p>5` be prime. Since 360 is
invertible modulo `p`,

```math
p\mid(r+360k)\quad\Longleftrightarrow\quad
k\equiv-r\,360^{-1}\pmod p.
```

For a fixed bound `X`, define `S_(p,r)(X)` by this congruence together with
`p^2 <= r+360k <= X` and `k >= 0`. Then the composite positions in column
`r` are exactly

```math
\bigcup_{\substack{5<p\le\sqrt X\\p\ \mathrm{prime}}}S_{p,r}(X).
```

**Proof.** A composite integer has a least prime divisor `p <= sqrt(n)`.
For a unit column this prime exceeds 5, so the displayed congruence and
`n >= p^2` hold. Conversely every member of `S_(p,r)` is divisible by `p`
and at least `p^2`, hence composite. The threshold is essential: without it
the prime `p` itself could incorrectly be removed.

Processing primes in increasing order and assigning each integer to the
first set that contains it gives a disjoint smallest-factor partition:

```math
B_{p,r}=S_{p,r}\setminus\bigcup_{5<q<p,\ q\ \mathrm{prime}}S_{q,r}.
```

The verifier checks all 15,840 `(p,r)` progressions for `X=10^6` and compares
every unit-class integer against a separately constructed smallest-factor
label. This is a specialization of classical exact sieving, not a new algorithm.

### Example: column 1

For `p=7`, `360^-1 = 5 (mod 7)`, hence `k=2 (mod 7)` locates its multiples.
In particular, `721=1+360*2=7*103` is removed. The first positions illustrate
why a residue class is never itself a prime/composite label:

| k | n = 1 + 360k | Classification |
|---:|---:|---|
| 0 | 1 | neither prime nor composite |
| 1 | 361 | `19^2` |
| 2 | 721 | `7*103` |
| 3 | 1081 | `23*47` |
| 4 | 1441 | `11*131` |
| 5 | 1801 | prime |

## 4. M360-032: an exact semiprime counting bridge

For a unit residue `r`, let `P_2(X;r)` count integers `pq <= X` in that
class, where `p <= q` are primes (equality allowed). Define
`pi(Y;360,a) = number of primes <= Y congruent to a modulo 360`.
Then

```math
P_2(X;r)=\sum_{\substack{5<p\le\sqrt X\\p\ \mathrm{prime}}}
\left[\pi(\lfloor X/p\rfloor;360,rp^{-1})-
\pi(p-1;360,rp^{-1})\right].
```

**Proof.** A unit semiprime has both factors greater than 5. Its unique
unordered factorization can be ordered as `p <= q`; the bound on `p` and
the congruence `q = r p^-1 (mod 360)` follow. The difference of prime counts
restricts `q` to `[p, floor(X/p)]`. This counts squares once and distinct
products once, with no appeal to an assumed uniform prime distribution.

This makes the distinction from the 96 abstract ordered factorizations
`ab=r` explicit: actual integer factorizations are weighted by prime
occurrence and by size constraints. The formula is elementary; no novelty
claim is made for it. All 96 unit rows are checked against the formula.

## 5. M360-031: measured reference window

| Count, `1 <= n <= 10^6` | All rows | 96 unit rows | 264 nonunit rows |
|---|---:|---:|---:|
| Integers | 1000000 | 266666 | 733334 |
| One | 1 | 1 | 0 |
| Primes | 78498 | 78495 | 3 |
| Composites | 921501 | 188170 | 733331 |
| Semiprimes | 210035 | 121851 | 88184 |
| Squarefree (including 1) | 607926 | 253302 | 354624 |
| Prime squares | 168 | 165 | 3 |
| Proper prime powers | 236 | 200 | 36 |

The three primes in nonunit rows are 2, 3 and 5. Every unit row has both a
prime witness and a composite witness within this window. Every one of
the 360 rows has a composite witness.

Among unit rows, prime counts range from 785 (residue 49) to 842 (residue
281). These are observations at this bound, **not** proof of a preferred
residue class, persistent bias, non-randomness, or literature novelty.
The 12-lift vectors and their exact MOD-30 aggregation are in `summary.json`.
For example, column 1 contains 820 primes and 1957 composites, plus 1.

## 6. Reproduction and audit limits

```bash
python exact/generate_integer_census.py --check
python exact/verify_integer_census.py --check
```

Both default to checking without writing. After an intentional source/data
change, regenerate explicitly using the corresponding `--write` commands.
The default bound is `10^6`; `--limit` on the generator is for controlled
experiments, not a silent change to the reference window.

Algorithm A uses a smallest-prime-factor sieve and recurrence formulas.
Algorithm B uses an Eratosthenes bit sieve and prime/prime-power divisor
incidence. Every row and all 1,000,000 integers are cross-checked.
Semiprimes are also reconstructed by enumerating `p <= q` and by the unit
progression formula above. Trial division checks integers 1 through 10,000.
The certificate hashes both source scripts and all three data files.

Two different implementations by the same assistant are **not independent
external review (`E4`)**. Current evidence is `E2`, plus the elementary proofs
above (`E3`). Core V3 remains unchanged; this is a separate reviewable layer.

## 7. Prior art and next questions

Primary reference anchors, consulted 2026-09-16:

- NIST, Dictionary of Algorithms and Data Structures, *sieve of Eratosthenes*:
  https://xlinux.nist.gov/dads/HTML/sieve.html
- NIST DLMF, section 27.2, unique prime-power factorization and arithmetic
  functions: https://dlmf.nist.gov/27.2 (DLMF writes `nu` for our `omega`).

The algorithm and its arithmetic foundation are classical. The contribution
here is a reproducible MOD-360 dataset joined to the existing atlas.
No `NEW` or worldwide novelty promotion is requested.

OQ-003 and OQ-006 remain open beyond this first finite window: compare multiple
bounds, normalize unequal exposures and known power-image constraints, and
separate stable phenomena from cutoff effects. Prime gaps, Carmichael numbers,
and residue-wise full omega/Omega histograms are not yet covered here.
