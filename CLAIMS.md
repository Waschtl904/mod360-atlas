# Claims Registry

This register is the canonical overview. Detailed proofs, generated tables, or certificates are linked rather than duplicated here.

| ID | Statement | Status | Evidence | Reproduction |
|---|---|---|---|---|
| M360-001 | \(\mathbb Z/360\cong\mathbb Z/8\times\mathbb Z/9\times\mathbb Z/5\) | `K + V360` | `E3` | `exact/verify_core.py` |
| M360-002 | There are 24 GCD strata \(C_d=\{x:\gcd(x,360)=d\}\), with \(|C_d|=\varphi(360/d)\) | `K + V360` | `E2 + E3` | exhaustive + proof |
| M360-003 | Affine ordered-pair orbits under \(x\mapsto ux+a\) are exactly classified by \(\gcd(x-y,360)\) | `K + V360` | `E2 + E3` | exhaustive + proof |
| M360-004 | The nilradical is \(N=(30)\), with \(N^2=(180)\), \(N^3=0\), and \(R/N\cong\mathbb Z/30\) | `K + V360` | `E2 + E3` | exact |
| M360-005 | \(U(360)\cong C_{12}\times C_2^3\); the counts of elements of orders \(1,2,3,4,6,12\) are \(1,15,2,16,30,32\) | `K + V360` | `E2 + E3` | exhaustive |
| M360-006 | \(U(360)^2=\{1,49,121,169,241,289\}\cong C_6\) | `K + V360` | `E2` | exhaustive |
| M360-007 | \(K=\ker(U(360)\to U(30))=1+(30)\cong C_6\times C_2\), and for every unit \(u\), \(u+(30)=uK\) | `V360 + NH + ?[O]` | `E2 + E3` | exhaustive + algebra |
| M360-008 | In the depth coordinate \(1+30j\), multiplication is \(j\star k=j+k+6jk\pmod{12}\) | `V360 + NH + ?[O]` | `E2 + E3` | algebra + exhaustive |
| M360-009 | \(C=1+(60)\cong C_6\); on this six-element layer the depth twist vanishes because \((60)^2=0\) | `V360 + NH + ?[O]` | `E2 + E3` | exact |
| M360-010 | For \(Q=U(360)^2\) and \(C=1+(60)\), \(Q\cap C=\{1,121,241\}\cong C_3\) | `V360 + NH + ?[O]` | `E2` | exhaustive |
| M360-011 | The regular skeleton is \(M=\operatorname{im}(x\mapsto x^{13})=\operatorname{Reg}(R)\), with \(|M|=175\) | `K + V360` | `E2 + E3` | exhaustive + CRT |
| M360-012 | Every residue has the exact decomposition \(x=x^{13}+n\), with \(n\in(30)\) and \(x^{13}n=0\) | `V360 + NH + ?[O]` | `E2` | exhaustive |
| M360-013 | \(x^{12}\) is an idempotent support projector and assumes exactly 8 values | `K + V360` | `E2 + E3` | exhaustive |
| M360-014 | The 96 prime-capable MOD-360 classes are exactly 12 lifts of the 8 units modulo 30 | `K + V360` | `E3` | exact |
| M360-015 | For a finite offset set \(H\), the number of MOD-360 starts for which all shifts avoid divisibility by \(2,3,5\) is \(A_{360}(H)=12\prod_{p\in\{2,3,5\}}(p-\nu_p(H))\) | `K + V360` | `E2 + E3` | CRT + exhaustive tests |
| M360-016 | For unit-factor exponents \(e_i\), the possible residues of \(\prod p_i^{e_i}\) form \(G^\delta\), where \(\delta=\gcd(e_1,\dots,e_s,12)\) | `K + V360` | `E2 + E3` | group theorem + power images |
| M360-017 | The GCD relation graph indexed by \(d\mid360\) has additive-Fourier eigenvalues \(c_{360/d}(k)\) | `K + V360` | `E3` | finite Fourier identity |
| M360-018 | The fixed field of the square kernel is \(\mathbb Q(\zeta_9)^+\mathbb Q(\sqrt5)\), of degree 6, with quotient group \(C_6\) | `K + V360` | `E3` | CRT/Galois proof |
| M360-019 | The ideals of \(R=\mathbb Z/360\mathbb Z\) are exactly \(I_d=(d)\) for \(d\mid360\); \(|I_d|=360/d\), \(R/I_d\cong\mathbb Z/d\mathbb Z\), and the ideal lattice is the reversed divisor box \(C_4\times C_3\times C_2\) | `K + V360` | `E2 + E3` | `data/ideal-lattice.csv` + proof |
| M360-020 | The GCD shell \(C_d\) is exactly the set of elements generating the ideal \(I_d\). For \(x\in C_d\), \(\operatorname{Ann}(x)=I_{360/d}\), \(|\operatorname{Ann}(x)|=d\), and \(|Rx|\,|\operatorname{Ann}(x)|=360\) | `K + V360` | `E2 + E3` | exhaustive + elementary ideal proof |
| M360-021 | \(\operatorname{Ann}(I_d)=I_{360/d}\); under the canonical additive character pairing, the Fourier orthogonal complement also satisfies \(I_d^\perp=I_{360/d}\) | `K + V360` | `E2 + E3` | exhaustive + character proof |
| M360-022 | Ideal arithmetic is \(I_d+I_e=I_{\gcd(d,e)}\), \(I_d\cap I_e=I_{\operatorname{lcm}(d,e)}\), and \(I_dI_e=I_{\gcd(de,360)}\); annihilator duality exchanges sums and intersections | `K + V360` | `E2 + E3` | exhaustive + divisor proof |
| M360-023 | Exactly 8 ideals are direct summands: those with \(\gcd(d,360/d)=1\). They are precisely the idempotent-generated ideals, and if \(e\) generates \(I_d\), then \(1-e\) generates \(\operatorname{Ann}(I_d)\) | `K + V360` | `E2 + E3` | exhaustive + CRT proof |
| M360-024 | The Jacobson radical/nilradical is \(J=(30)\), its annihilator is the socle \((12)\), and the maximal ideals \((2),(3),(5)\) are annhhilator-dual to the minimal nonzero ideals \((180),(120),(72)\) | `K + V360` | `E2 + E3` | exhaustive + finite-ring proof |
| M360-025 | For every ordered pair \((x,y)\), if \(d=\gcd(x-y,360)\), then \(x-y\) generates \(I_d\), has additive order \(360/d\), and has annihilator size \(d\). Thus the 24 affine pair-relations are exactly the 24 ideal-generator shells of differences | `K + V360` | `E2 + E3` | exhaustive + M360-020 |

| M360-026 | The 24 GCD shells form the unit-orbit quotient monoid under multiplication: for `d,e|360`, `C_d C_e = C_g` with `g=gcd(de,360)`; in valuation coordinates this is capped addition | `K + V360` | `E2 + E3` | exhaustive + associate/CRT proof |
| M360-027 | For `g=gcd(de,360)`, every `z in C_g` has the same number `phi(360/d) phi(360/e) / phi(360/g)` of ordered shell factorizations `z=xy`, `x in C_d`, `y in C_e`; the analogous r-factor formula follows by induction | `K + V360` | `E2 + E3` | exhaustive + transitive unit action |
| M360-028 | Natural-prime capability and ring-theoretic primality are different: natural primes `>5` can occur only in `C_1`, while prime/(strong) irreducible elements of `R` are exactly `C_2 union C_3 union C_5`; very strong irreducibles are exactly `C_2 union C_3` | `K + V360` | `E2 + E3` | exhaustive + Baeth--Burns--Mixco |
| M360-029 | For nonzero nonunits in `C_d`, irreducible factorization is unique up to associates/permutation exactly for `d in {2,3,4,6,12}`, with length `Omega(d)`; every other nonzero nonunit shell has length set `[Omega(d), infinity)` | `K + V360` | `E3` | specialization of Baeth--Burns--Mixco Cor. 3.5 |

## Status rule

`NH` means only “new in this investigation”. It is not a literature novelty claim. Promotion to `NEW` requires the separate process in `NOVELTY_LEDGER.md`.

## Finite-window extension (separate from Core V3)

These entries do not promote the historical operator candidates or change Core V3.
The mathematical identities are classical elementary specializations; dataset
counts assert only the explicitly bounded window. No independent external review
(`E4`) or literature-novelty (`NEW`) claim is made.

| ID | Statement | Status | Evidence | Reproduction / proof |
|---|---|---|---|---|
| M360-030 | In a unit MOD-360 column `n=r+360k`, the composites `2<=n<=X` are exactly the union over primes `5<p<=sqrt(X)` of `k=-r*360^-1 (mod p)` with `p^2<=n<=X`; processing primes increasingly gives the disjoint least-factor partition | `K + V360` | `E3`; `E2` at `X=10^6` | [proof](primes/integer-census-v1.md#3-m360-030-exact-composite-positions-inside-a-fixed-column), `exact/verify_integer_census.py` |
| M360-031 | The census on positive integers `1..1000000` has 360 exactly verified rows: 78498 primes, 921501 composites, one exceptional integer 1, 210035 semiprimes, 607926 squarefree integers including 1; all categories and witnesses are defined in the dataset documentation | `V360` (finite dataset only) | `E2`, different algorithms; not `E4` | [data and conventions](primes/integer-census-v1.md#5-m360-031-measured-reference-window), `certificates/integer-census-v1.json` |
| M360-032 | For a unit residue `r`, its semiprime count equals the sum over primes `5<p<=sqrt(X)` of `pi(floor(X/p);360,r*p^-1)-pi(p-1;360,r*p^-1)`, counting `p<=q` and including squares once | `K + V360` | `E3`; `E2` at `X=10^6` | [proof](primes/integer-census-v1.md#4-m360-032-an-exact-semiprime-counting-bridge), `exact/verify_integer_census.py` |
