# 24 GCD Strata

Because

\[
360=2^3 3^2 5,
\]

a residue has truncated valuation coordinates

\[
v_2\in\{0,1,2,\ge3\},\qquad
v_3\in\{0,1,\ge2\},\qquad
v_5\in\{0,\ge1\},
\]

hence \(4\cdot3\cdot2=24\) GCD types.

For every divisor \(d\mid360\),

\[
C_d=\{x\bmod360:\gcd(x,360)=d\}=d\,U(360/d)
\]

(with the natural interpretation for \(d=360\)), and

\[
|C_d|=\varphi(360/d).
\]

The same divisors classify affine ordered-pair relations:

\[
R_d=\{(x,y):\gcd(y-x,360)=d\}.
\]

Translations reduce a pair to \((0,y-x)\); unit scalings act transitively on every fixed-GCD difference stratum. Therefore the affine group \(R\rtimes U(360)\) has exactly 24 ordered-pair orbit types.

Generated tables: `data/gcd-strata.csv`, `data/relation-strata.csv`.
