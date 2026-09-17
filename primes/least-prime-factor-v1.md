# MOD 360: Zerlegung von `pq` nach dem kleineren Primfaktor

**Stand 2026-09-17.** Gestapelte Forschungsfortsetzung auf dem exakten Head von
PR #3 (`713f3f78b0d0feb3d32efeadc0bf40c9d7ffd0f2`). Der Modul bleibt 360.
PR #3 wird nicht verschoben, nicht gemergt und nicht in den Core promoviert.

## 1. Frage

PR #3 fand für Produkte zweier **verschiedener** Primzahlen im mittleren Fenster

\[
(36\,000,360\,000]
\]

gleichzeitig

\[
\Delta=3/10>0,\qquad
\Delta_{\rm fein}=-13/18<0,\qquad
\Delta_{\rm grob}=79/72>0.
\]

Die neue Rechnung zerlegt exakt, woher diese Gegenrichtung kommt.

Für einen festen kleineren Primfaktor \(p>5\) definieren wir

\[
c_{p;(L,H]}(r)=
\#\{q\ {\rm prim}: p<q,\ L<pq\le H,\ pq\equiv r\pmod{360}\}.
\]

Da \(p,q>5\), liegt jedes Produkt in einer der 96 Einheitenklassen. Für jede
Referenzansicht gilt die **exakte Vektoridentität**

\[
T_{(L,H]}(r)=\sum_p c_{p;(L,H]}(r)
\]

für alle \(r\in U(360)\), wobei \(T\) der bereits in PR #3 gespeicherte
Zählvektor `distinct_semiprimes` ist.

Die zulässigen \(q\) erfüllen exakt

\[
q>\max\!\left(p,\left\lfloor\frac Lp\right\rfloor\right),
\qquad
q\le\left\lfloor\frac Hp\right\rfloor .
\]

Damit ist die Zerlegung disjunkt: jede Zahl \(pq\) mit \(p<q\) besitzt genau
einen kleineren Primfaktor \(p\).

## 2. Reproduktion des vorhandenen Moduls

Die Summe der `p`-Zeilen reproduziert für alle 96 Einheitenklassen die
PR-#3-Vektoren, nicht nur deren Gesamtsumme. Daraus folgen exakt wieder:

| Ansicht | Delta | Delta fein | Delta grob |
|---|---:|---:|---:|
| kumulativ bis 36.000 | 82/45 | 37/18 | 2/9 |
| kumulativ bis 360.000 | 191/90 | 4/3 | 95/72 |
| kumulativ bis 3.600.000 | 623/90 | 85/9 | -19/24 |
| (0,36.000] | 82/45 | 37/18 | 2/9 |
| (36.000,360.000] | 3/10 | -13/18 | 79/72 |
| (360.000,3.600.000] | 24/5 | 73/9 | -19/9 |

Das ist ein Anschlusscheck an PR #3, keine neue asymptotische Aussage.

## 3. Goldnugget im mittleren Fenster: eine natürliche Grenzlinie

Für \(L=36\,000\) liegt

\[
\sqrt L\approx189.736.
\]

Daher trennen sich die kleineren Primfaktoren ohne frei gewählten Schwellenwert:

- für `p<=189` (tatsächlich höchstens 181) ist die Untergrenze `pq>36000`
  aktiv und erzwingt `q>36000/p`;
- für `p>=191` folgt `pq>36000` bereits aus `q>p`, weil `p^2>36000`.

Die exakten Beiträge sind:

| p-Regime | # p | Produkte | Q | A\Q | U\A | Delta | Delta fein | Delta grob |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| p<=189 | 39 | 33.381 | 2.106 | 6.245 | 25.030 | -7/2 | -73/18 | -23/72 |
| p>189 | 67 | 6.502 | 385 | 1.215 | 4.902 | +19/5 | +10/3 | +17/12 |
| Summe | 106 | 39.883 | 2.491 | 7.460 | 29.932 | +3/10 | -13/18 | +79/72 |

Das kleine positive Gesamt-\(\Delta=3/10\) ist also **kein gleichförmiger
Effekt über die kleineren Faktoren**. Der große, zahlenmäßig dominierende
Bereich `p<=189` zeigt sogar die Gegenrichtung `-7/2`; der kürzere Schwanz
`p>=191` überkompensiert ihn knapp mit `+19/5`.

Auch der feine Kontrast wird verständlicher: `-73/18 + 10/3 = -13/18`.
Die Gegenrichtung im feinen Vergleich bleibt übrig, weil die positive
Schwanzkorrektur nicht groß genug ist.

Diese Schnittstelle entsteht aus der Geometrie des Hyperbelstreifens
`L < p q <= H` zusammen mit `p<q`; sie ist keine nachträglich optimierte
Datenschwelle.

## 4. Zweiter Mechanismus: die Wahl der groben MOD-30-Familien

Setze im Einheitenrad modulo 30

\[
H=\{1,19\}.
\]

Dies ist eine Untergruppe der Ordnung 2, denn \(19^2\equiv1\pmod{30}\).
Die in PR #3 verwendete Menge \(A\) besteht genau aus den MOD-360-Hebungen
dieser beiden groben Klassen.

Teilt man nun nach der MOD-30-Klasse des **kleineren Faktors** \(p\), ergibt
sich im mittleren Fenster:

| p-Familie | # p | Produkte | Delta | Delta fein | Delta grob |
|---|---:|---:|---:|---:|---:|
| p mod 30 in {1,19} | 22 | 7.098 | +29/45 | -7/3 | +113/36 |
| p mod 30 außerhalb {1,19} | 84 | 32.785 | -31/90 | +29/18 | -49/24 |
| Summe | 106 | 39.883 | +3/10 | -13/18 | +79/72 |

Damit kommt der **positive grobe Beitrag vollständig aus einer starken
Gegenüberlagerung**: Faktoren \(p\in H\) liefern `+113/36`, die übrigen sechs
MOD-30-Familien zusammen `-49/24`.

Das ist algebraisch sinnvoll zu lesen, ohne daraus einen Primzahlsatz zu machen.
Für festes \(p\bmod30=s\) gilt

\[
pq\bmod30\in H
\iff
q\bmod30\in s^{-1}H.
\]

Multiplikation mit \(s\) permutiert die acht Einheitenklassen modulo 30.
Der grobe Kontrast misst daher endliche Ungleichgewichte der zulässigen
`q`-Intervalle zwischen diesen Zweierkosets; er ist nicht von der feinen
Hebungsstruktur allein zu trennen.

## 5. Beide Mechanismen gleichzeitig

Die 2x2-Zerlegung zeigt, dass Größen- und Familienmechanismus sich überlagern:

| Regime | Delta | Delta fein | Delta grob |
|---|---:|---:|---:|
| p<=189 und p mod30 in {1,19} | -19/45 | -41/18 | +7/4 |
| p<=189 und p mod30 außerhalb | -277/90 | -16/9 | -149/72 |
| p>189 und p mod30 in {1,19} | +16/15 | -1/18 | +25/18 |
| p>189 und p mod30 außerhalb | +41/15 | +61/18 | +1/36 |

Besonders wichtig: Es gibt **keine** einfache Aussage „kleine Primfaktoren
verursachen den positiven Bias“. Im Gegenteil. Der natürliche untere Bereich
ist global negativ. Positiv wird das Gesamt-\(\Delta\) erst durch die
`p>sqrt(36000)`-Schicht.

## 6. Einzelne stärkere Beiträge

Im mittleren Fenster sind die stärksten negativen Beiträge zu
\(\Delta_{\rm fein}\) unter anderem

`p=17: -5/3`, `p=31: -11/9`, `p=53: -17/18`,
`p=13: -13/18`, `p=211: -2/3`.

Die stärksten positiven Beiträge umfassen

`p=251: +8/9`, `p=7: +13/18`, `p=137: +11/18`,
`p=71: +5/9`.

Diese Rangliste ist **diagnostisch**, nicht als dauerhafte Eigenschaft eines
bestimmten Primfaktors zu interpretieren.

## 7. Produktgrößen allein erklären die Richtung nicht

Das mittlere Fenster wurde zusätzlich in die neun natürlichen Blöcke der Länge
36.000 zerlegt. Die Vorzeichen wechseln mehrfach. Beispiele:

- `(36.000,72.000]`: Delta `13/10`, fein `19/18`;
- `(108.000,144.000]`: Delta `-52/45`, fein `-19/18`;
- `(180.000,216.000]`: Delta `-23/9`, fein `-41/18`;
- `(252.000,288.000]`: Delta `4/9`, fein `13/9`;
- `(324.000,360.000]`: Delta `-179/90`, fein `-5/2`.

Eine einzelne Produktgrößenzone trägt die Gegenrichtung also nicht allein.
Die nach \(p\) definierte natürliche Hyperbel-/Diagonal-Schnittstelle ist
informativer als eine bloße Unterteilung der Produktachse.

## 8. Daten und unabhängige Gegenprüfung

`data/least-prime-factor-v1/by-p-summary.csv` enthält für jede tatsächlich
auftretende `p`-Schicht und jede der sechs Ansichten `Q`, `A\Q`, `U\A` sowie
`Delta`, `Delta_fine`, `Delta_coarse`. Die vollständigen **96** Beiträge pro
`p` werden deterministisch als `by-p-residues.csv` exportiert und ihr SHA-256
ist im Zertifikat gebunden:

```bash
python exact/generate_least_prime_factor.py --export /tmp/mod360-lpf
```

`middle-diagnostics.csv` enthält die natürlichen Regime, MOD-30-Familien,
deren 2x2-Kreuzung, alle acht einzelnen MOD-30-Faktorfamilien und die neun
36.000er-Produktblöcke.

Zwei getrennte Algorithmen werden verwendet:

1. Generator: Eratosthenes + direkte Enumeration ungeordneter Primpaare `p<q`.
2. Verifier: SPF-Tabelle + Scan aller ganzen Zahlen bis 3.600.000; `n=p*q`
   wird über kleinsten Primfaktor und primen Kofaktor erkannt.

Beide prüfen zusätzlich die vollständigen 96er-Vektoren gegen
`data/multiscale-v1/counts.csv`. Der Verifier importiert den Generator nicht.

```bash
python exact/generate_least_prime_factor.py --check
python exact/verify_least_prime_factor.py
```

## 9. Vorgeschlagene Modul-Claims

Diese IDs werden nur in diesem gestapelten Forschungsmodul vorgeschlagen,
nicht in `CLAIMS.md` auf main eingetragen.

- **M360-042 — V360, E2:** An den sechs Referenzansichten zerlegt die Summe
  über den kleineren Primfaktor \(p>5\) den vollständigen 96-Klassenvektor
  der verschiedenen Semiprime exakt und reproduziert die PR-#3-Kontraste.
- **M360-043 — V360 + NH, E2 + E3 (endliche Diagnose):** Im mittleren Fenster
  trennt \(p\le\lfloor\sqrt{36000}\rfloor\) exakt den Bereich mit aktiver
  unterer Produktgrenze vom Bereich, in dem `q>p` die Untergrenze bereits
  garantiert; die beiden Beiträge zu Delta sind `-7/2` und `+19/5`.
- **M360-044 — V360 + NH, E2 (endliche Diagnose):** Die Zerlegung nach
  `p mod30 in {1,19}` versus Komplement liefert im mittleren Fenster die oben
  dokumentierten exakten Grob-/Feinbeiträge.

`NH` bedeutet nur „zuerst in diesem Projekt isoliert“. Es gibt hier **keinen**
`NEW`- oder Asymptotikclaim und keinen Objekt-X-/RH-Bezug.
