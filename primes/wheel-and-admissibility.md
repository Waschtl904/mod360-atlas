# Prime-capable classes, wheel geometry, and admissibility

For primes \(p>5\), a MOD-360 residue must be a unit. Prime-capability therefore depends only on reduction modulo 30.

The eight wheel classes are

\[
1,7,11,13,17,19,23,29\pmod{30}.
\]

Each has 12 lifts modulo 360, giving 96 prime-capable classes.

The cyclic MOD-30 wheel gaps are

\[
6,4,2,4,2,4,6,2.
\]

Across the 96 lifted classes this gives 36 gaps of size 2, 36 of size 4, and 24 of size 6.

## Exact finite admissibility count

For a finite offset set \(H=\{h_1,\dots,h_m\}\), define

\[
\nu_p(H)=|\{h_i\bmod p\}|.
\]

The number of starting residues \(r\bmod360\) for which every \(r+h_i\) is coprime to 360 is

\[
A_{360}(H)=12\prod_{p\in\{2,3,5\}}(p-\nu_p(H)).
\]

This is a pure CRT/sieve statement. It makes no claim about how often all entries are simultaneously prime.

For pairs \(H=\{0,h\}\):

- odd \(h\): 0 admissible starts;
- \(2\mid h,\ 3\nmid h,\ 5\nmid h\): 36;
- \(6\mid h,\ 5\nmid h\): 72;
- \(10\mid h,\ 3\nmid h\): 48;
- \(30\mid h\): 96.
