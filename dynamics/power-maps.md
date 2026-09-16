# Power-map dynamics

For the full ring \(R=\mathbb Z/360\mathbb Z\), exact image sizes for \(x\mapsto x^k\), \(k=1,\ldots,24\), are

```text
k:     1   2  3  4   5  6   7  8  9 10  11 12  13 14 15 16  17 18 19 20 21 22 23 24
|R^k|:360 36 75 16 175 12 175 16 75 24 175  8 175 24 75 16 175 12 175 16 75 24 175  8
```

For \(k\ge3\), the image size depends only on \(\gcd(k,12)\):

- gcd 1: 175;
- gcd 2: 24;
- gcd 3: 75;
- gcd 4: 16;
- gcd 6: 12;
- gcd 12: 8.

The exceptional exponents 1 and 2 retain additional nilpotent information.

A full functional-graph classification (cycles, trees, preperiods, fiber profiles) remains on the roadmap.

## Review extension, 2026-09-16

The [complete power atlas V1](power-atlas-v1.md) now supplies that classification
as a separate review module: all 14 positive power maps, every edge/fiber/cycle,
a local orbit formula, the universal two-step/two-cycle rule, and an exact
prime-power counting bridge. Core V3 and the historical findings are not promoted
or rewritten by this addition.
