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

## Status rule

`NH` means only “new in this investigation”. It is not a literature novelty claim. Promotion to `NEW` requires the separate process in `NOVELTY_LEDGER.md`.
