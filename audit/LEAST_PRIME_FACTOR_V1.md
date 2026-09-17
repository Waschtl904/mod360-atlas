# Auditauftrag: Zerlegung nach kleinstem Primfaktor

Basis dieser gestapelten Fortsetzung:
PR #3 / `research/multiscale-v1-2026-09-17`,
Head `713f3f78b0d0feb3d32efeadc0bf40c9d7ffd0f2`.

Kein Merge, keine Core-Promotion, keine Änderung der alten PR-Heads.

## Tatsächlich lokal durchgeführt

Auf einem getrennten lokalen Arbeitsbaum wurden ausgeführt:

```bash
python exact/generate_least_prime_factor.py --write
python exact/generate_least_prime_factor.py --check
python exact/verify_least_prime_factor.py
```

Ergebnis: Generator `WROTE`, anschließender Byte-Check `MATCH`, unabhängiger
Verifier `PASS`.

Die lokale Eltern-Datei `data/multiscale-v1/counts.csv` wurde für diesen
Vorabtest aus der bereits gelesenen PR-#3-Zähldefinition rekonstruiert.
Der Remote-Branch muss deshalb zusätzlich in GitHub Actions gegen die
**tatsächlich eingecheckte** PR-#3-Datei laufen; lokaler PASS und Remote-CI
sind strikt getrennte Evidenz.

## Was der Verifier unabhängig macht

Der Generator zählt Primpaare direkt:

\[
5<p<q,\qquad L<pq\le H.
\]

Der Verifier zählt dagegen ganze Zahlen `n` bis 3.600.000, baut eine
Smallest-Prime-Factor-Tabelle und akzeptiert `n` genau dann, wenn der kleinste
Primfaktor `p>5`, der Kofaktor `q` prim und `p<q` ist.

Der Verifier importiert keinen Generatorcode. Er prüft:

1. jede `p`-Zeile und alle 96 Unit-Restklassen;
2. die Summen gegen die PR-#3-Vektoren `semiprimes-prime_squares`;
3. alle sechs bekannten rationalen Kontraste;
4. `Q`, `A\Q`, `U\A` jeder Zeile;
5. die natürliche Schranke `sqrt(36000)` im mittleren Fenster;
6. sämtliche Mittelintervall-Diagnosen;
7. SHA-256 der kompakten Datentabellen und des vollständigen 96-Klassen-Exports;
8. einen gezielten Mutationstest.

## Zuerst angreifen

1. Off-by-one in `L < pq <= H`, insbesondere `L//p`.
2. Ist `p` wirklich der kleinere **Primfaktor**, nicht nur irgendein Teiler?
3. Doppeltzählung von `pq` und `qp`.
4. Ausschluss von `p^2` und von Faktoren 2,3,5.
5. Vollständige 96er-Vektorgleichheit gegen PR #3, nicht nur Gesamtsummen.
6. `p<=189` versus `p>189`: `sqrt(36000)` ist nicht ganzzahlig; es gibt keinen
   Primfaktor 189/190. Der erste obere Primwert ist 191.
7. Keine Interpretation von `-7/2` und `+19/5` als asymptotische Aussage.
8. Die Familie `{1,19}` modulo 30 ist durch das bereits verwendete `A`
   vorgegeben; sie wurde nicht nach den neuen Daten ausgesucht.
9. Die neun 36.000er-Blöcke sind Diagnose, kein präregistrierter Test.
10. Zwei Programme desselben Assistenten sind kein externes E4-Review.

## Erwartete Mittelintervallzahlen

Gesamt:

`39883 = 2491 + 7460 + 29932`,
`Delta=3/10`, `Delta_fine=-13/18`, `Delta_coarse=79/72`.

Natürliche Untergrenzenregime:

- `p<=189`: 33.381 Produkte, `Delta=-7/2`, fein `-73/18`, grob `-23/72`.
- `p>189`: 6.502 Produkte, `Delta=19/5`, fein `10/3`, grob `17/12`.

MOD-30-Faktorgruppen:

- `p mod30 in {1,19}`: `Delta=29/45`, fein `-7/3`, grob `113/36`.
- Komplement: `Delta=-31/90`, fein `29/18`, grob `-49/24`.

Diese Zahlen müssen sich jeweils exakt zur bekannten Gesamtreihe addieren.

## Evidenzstatus

Die endlichen Identitäten sind `V360`. Die Diagnose M360-043/044 wird als
`NH` nur im projekinternen Sinn vorgeschlagen. Kein Literatur-Neuheitsaudit,
kein `NEW`, keine Signifikanz- oder Dichteaussage.
