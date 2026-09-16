# Multiplicative shell and factorization baseline modulo 360

Let

\[
R=\mathbb Z/360\mathbb Z,
\qquad
C_d=\{x\in R:\gcd(x,360)=d\},\quad d\mid360.
\]

The classes `C_d` are simultaneously unit-multiplication orbits and associate classes. This note records the exact multiplicative baseline that must be removed before interpreting any residue bias among composite integers.

## 1. The 24-shell multiplication monoid

For every `d,e|360`, define

\[
d\odot e=\gcd(de,360).
\]

Then

\[
\boxed{C_d C_e=C_{d\odot e}.}
\]

Write

\[
d=2^a3^b5^c,
\qquad
0\le a\le3,
\quad0\le b\le2,
\quad0\le c\le1.
\]

The operation is capped valuation addition:

\[
(a,b,c)\odot(a',b',c')
=
(\min(a+a',3),\min(b+b',2),\min(c+c',1)).
\]

Thus the multiplicative monoid of residue classes modulo unit multiplication is exactly the 24-point truncated valuation box.

### Proof

If `x in C_d` and `y in C_e`, write `x=du`, `y=ev` up to associates, with `u,v` units in the appropriate strong-associate sense. Multiplication adds local prime valuations until the modulus exponent is reached, so

\[
\gcd(xy,360)=\gcd(de,360).
\]

Conversely all elements with that gcd are unit multiples of one another, so the target shell is filled completely.

## 2. Uniform shell-factorization multiplicity

Put

\[
g=\gcd(de,360).
\]

The product map

\[
C_d\times C_e\longrightarrow C_g,
\qquad(x,y)\longmapsto xy
\]

is surjective. The unit group acts transitively on `C_g` and transports fibers bijectively. Therefore every target `z in C_g` has the same number of ordered preimages. Since

\[
|C_t|=\varphi(360/t),
\]

that number is

\[
\boxed{
N_{d,e}
=
\frac{\varphi(360/d)\,\varphi(360/e)}
     {\varphi(360/g)}.
}
\]

For `r` prescribed shells `C_{d_1},...,C_{d_r}`, let

\[
g=\gcd(d_1d_2\cdots d_r,360).
\]

Then each `z in C_g` has exactly

\[
\boxed{
N_{d_1,\dots,d_r}
=
\frac{\prod_i \varphi(360/d_i)}{\varphi(360/g)}
}
\]

ordered residue factorizations with factor `i` in `C_{d_i}`.

This is the correct finite-ring null model for factorization counts.

## 3. Unit factors: why raw composite counts can look deceptively uniform

For `d=e=1`,

\[
g=1,
\qquad
N_{1,1}=96.
\]

So every unit residue modulo 360 has exactly 96 ordered factorizations into two unit residue classes. More generally, multiplying by a unit shell does not favor any member of the target shell.

Therefore any empirical bias among actual semiprimes or products of genuine primes cannot be attributed merely to the abstract multiplication table of `U(360)`; it must come from restrictions on which integers/factors are admitted (prime condition, size cutoff, ordering, repeated factors, etc.).

## 4. Natural primes versus prime elements of the residue ring

Two notions must never be conflated.

### Natural-integer primes

Every ordinary prime `p>5` satisfies

\[
p\bmod360\in C_1=U(360).
\]

Thus `C_1` is the set of **prime-capable residue classes** for large ordinary primes.

### Prime/irreducible elements inside the ring `R`

Classical factorization theory for `Z/nZ` gives:

\[
\boxed{
\text{ring prime/strong irreducible shells}
=C_2\cup C_3\cup C_5.
}
\]

For `360=2^3 3^2 5`, very strong irreducibles occur only for the prime divisors whose exponent in 360 is at least two:

\[
\boxed{
C_2\cup C_3.
}
\]

So ordinary primes `>5` live in the **unit shell**, while prime elements of the finite ring live in three **nonunit shells**. The terminology must remain separated throughout the atlas.

## 5. Irreducible factorization-length classification

Let `x` be a nonzero nonunit and `d=gcd(x,360)`. Write

\[
d=2^a3^b5^c,
\qquad
\Omega(d)=a+b+c.
\]

Specializing the factorization theorem of Baeth--Burns--Mixco, the factorization is unique up to associates and permutation exactly when every prime divisor of 360 still divides `360/d`. For MOD 360 this gives

\[
\boxed{d\in\{2,3,4,6,12\}.}
\]

For those shells the irreducible factorization length is exactly `Omega(d)`. For every other nonzero nonunit shell,

\[
\boxed{L_R(x)=[\Omega(d),\infty).}
\]

The zero shell `C_360={0}` is kept separate from this statement.

## 6. Research use

This layer gives us three increasingly restrictive baselines:

1. **shell support:** which gcd class a product can occupy;
2. **uniform residue multiplicity:** how many residue-level factorizations every target receives;
3. **actual arithmetic data:** what remains after requiring factors to be genuine primes/semiprimes within a size range.

Only the third layer can exhibit a prime-distribution effect not already forced by the finite ring.
