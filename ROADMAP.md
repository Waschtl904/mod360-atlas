# Roadmap

## Phase 0 — Governance and reproducibility

- [x] repository structure and status system
- [x] deterministic atlas generator
- [x] exhaustive Core verifier
- [x] claim registry expanded to 25 Core claims
- [x] novelty ledger separated from mathematical verification
- [x] citation/contribution/security files retained
- [x] CI line endings normalized for deterministic CSV regeneration

## Phase A — Complete static atlas

- [x] generate all 360 residue rows with CRT, gcd, unit order, powers, regular/nilpotent tags
- [x] generate all 24 GCD strata
- [x] add ideal/annihilator lattice table
- [x] identify the 24 GCD shells as ideal-generator shells
- [x] connect ring annihilator duality with additive Fourier orthogonality
- [ ] add compressed support-sector multiplication tables
- [ ] add subgroup lattice of \(U(360)\)

## Phase B — Primes and composites

- [x] MOD-30 wheel and 12 lifts
- [x] exact admissibility formula for finite prime-offset patterns
- [x] exponent-gcd classification of possible unit residues of factorizations
- [ ] prime-square, semiprime, squarefree, \(\omega\), and \(\Omega\) atlases
- [ ] compare theoretical residue support with actual primes/semiprimes up to controlled cutoffs
- [ ] build prime-gap relation atlas by \(\gcd(h,360)\)

## Phase C — Dynamics

- [x] power-image sizes through exponent 24
- [ ] full functional graphs for \(x^2,x^3,x^5,x^6,x^{12},x^{13}\)
- [ ] fiber-size stratification by GCD/support sector
- [ ] translation-plus-power maps and exact ranks

## Phase D — Harmonic and graph structure

- [x] GCD relation graphs and Ramanujan eigenvalues
- [x] identify ideal annihilator with additive-character orthogonal complement
- [ ] full 24x24 Bose–Mesner/intersection-number table
- [ ] compare additive Fourier strata with multiplicative character strata
- [ ] Gauss-sum bridge between additive and multiplicative characters

## Phase E — Discovery program

- [ ] identify quantities not forced by CRT, the unit-group isomorphism type, ideal duality, or simple sieve admissibility
- [ ] re-audit historical double-hexagon/affine/operator findings
- [ ] run targeted prior-art searches only after a theorem is isolated

## Release criteria

A release requires regenerated data with zero diff, a green exhaustive verifier, updated claims/status, documented open questions, and a frozen prior-art snapshot.
