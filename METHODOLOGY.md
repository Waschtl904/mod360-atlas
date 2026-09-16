# Methodology

## Research rule

The poster, diagram, hexagon, or numerical pattern is never the theorem. The workflow is:

1. **enumerate exactly**;
2. **identify the invariant**;
3. **derive a proof from CRT/group/ring theory when possible**;
4. **mark what is classical**;
5. **only then ask what remains unexplained**;
6. **audit novelty separately from correctness**.

## Prime firewall

A residue class is not itself “prime”. For \(r\bmod360\):

- `prime-capable` means \(\gcd(r,360)=1\);
- actual prime occurrence is an analytic/statistical question about integers in that progression;
- classes not coprime to 360 contain no primes greater than 5.

Statements about wheel admissibility are **sieve statements**, not predictions of actual prime frequency.

## Novelty firewall

No result is called literature-new merely because we did not immediately find it in a search. The repository separates:

- mathematical verification;
- new synthesis in this project;
- prior-art status.

## Exactness

Whenever a claim is finite, we prefer exhaustive integer arithmetic over floating point. The current core verifier enumerates all 360 residues where appropriate.
