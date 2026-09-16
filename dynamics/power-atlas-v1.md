# Vollständiger Potenzatlas MOD 360 — V1

**Gegenstand:** `P_k(x) = x^k mod 360`, alle 360 Restklassen, alle positiven
Exponenten. Es geht nicht um Potenzieren modulo einer veränderlichen Zahl.
Basis ist Core V3 am Commit `762e42d0931cba5e56e236c3ceb62dfeed2e1cee`.
Diese Erweiterung ist ein eigenständiges Review-Modul, keine Core-Promotion.
Die Primzahlpotenzdaten sind auf `1 <= n <= 1.000.000` begrenzt.

## Register dieses Moduls

Die IDs 030–032 bleiben für den getrennten Zählungs-PR reserviert. Die folgenden
IDs werden hier erstmals vorgeschlagen; das bestehende Root-Register bleibt
bis zur kontrollierten Integration unverändert. Status `K + V360` bedeutet
klassische Spezialisierung mit exakter Rechnung, nicht weltweite Neuheit.

| ID | Aussage | Evidenz | Beweis / Prüfung |
|---|---|---|---|
| M360-033 | Genau 14 positive Potenzabbildungen, mit den Vertretern 1–14 und expliziter Kompositionstafel | E3 + E2 | Abschnitt 2; 70.560 Kompositionsprüfungen |
| M360-034 | Für jedes k gilt P_k^4 = P_k^2 als Kompositionsidentität: höchstens zwei Vorschritte, Zyklenlänge 1 oder 2; fünf idempotente Abbildungen | E3 + E2 | Abschnitt 3 |
| M360-035 | Vollständige Graph-/Fasertaxonomie: 14 verschiedene Graphentypen auf R, 12 auf den Einheiten | E2 + E3 | Abschnitte 4–5; vollständige Tabellen und lokale Formel |
| M360-036 | Alle P_k mit k >= 3 faktorisieren über rho(x)=x^13; x^2-x^14 ist genau für 90 Klassen gleich 180, sonst 0 | E3 + E2 | Abschnitt 6 |
| M360-037 | Exakte Übertragung der Primzahlzählung über Potenzfasern; 236 echte Primzahlpotenzen bis 10^6, davon 200 mit Basis >5 | E3 für die Identität; E2 für den Datensatz | Abschnitt 7; 6.480 Restklassenprüfungen |

Alle fünf Einträge: `K + V360`, kein `NEW`, kein externes E4-Review behauptet.

## 1. Drei verschiedene Operationen

Für ein festes a ist die gewöhnliche Potenzfolge `a,a^2,a^3,...` nicht die
Iteration einer festen Abbildung `P_k`. Letztere ist

```math
P_k^{\circ t}(a)=a^{k^t}\pmod{360}\qquad(t\ge0).
```

`P_k^{\circ0}` ist die Identität. Auf Einheiten hat die gewöhnliche Potenzfolge
eine Periode, die 12 teilt. Wiederholtes Quadrieren hat dagegen Exponenten
`1,2,4,8,16,...`, nicht `1,2,3,...`.

Beispiel: `7 -> 49 -> 241 -> 121 -> 241 -> ...` beim Quadrieren. Trotzdem ist
`7^12 = 1 (mod 360)`. Es gibt keinen Widerspruch und keinen Primzahltest.

## 2. Genau 14 Abbildungen, nicht unendlich viele

Für jedes x gilt

```math
x^{m+12}=x^m\pmod{360}\qquad(m\ge3).
```

**Beweis.** Modulo 8 verschwindet der Nicht-Einheitenanteil ab der dritten
Potenz; modulo 9 bereits ab der zweiten; modulo 5 bereits ab der ersten.
Auf den jeweiligen Einheiten sind die Exponenten 2,6,4 ausreichend, und alle
teilen 12. CRT ergibt die Behauptung gleichzeitig für jede Restklasse.

Definiere `nu(k)=k` für k=1,2 und `nu(k)=3+((k-3) mod 12)` für k>=3. Dann

```math
P_k=P_{\nu(k)},\qquad P_i\circ P_j=P_{\nu(ij)}.
```

Die 12 stabilen Vertreter 3–14 sind verschieden, da 7 die Ordnung 12 hat:
seine Potenzen unterscheiden alle Exponenten modulo 12. P_1 kann nur mit
P_13 und P_2 nur mit P_14 zusammenfallen; die Einheiten schließen alle anderen
Möglichkeiten aus. Modulo 8 unterscheiden jedoch x=2 die Paare 1/13 und
2/14: `2^1=2`, `2^13=0`, `2^2=4`, `2^14=0 (mod 8)`. Somit genau 14.

`composition.csv` enthält das vollständige kommutative 14-Elemente-Monoid
unter Komposition. Exponent 0 und negative Exponenten gehören nicht dazu.

## 3. Universelle Zweischritt-/Zweizyklus-Regel

Setze F=P_k. Dann gilt für alle positiven k

```math
F^{\circ4}=F^{\circ2}.
```

**Beweis.** Für k>=2 sind k^2 und k^4 mindestens 3 und
`k^4-k^2 = k^2(k-1)(k+1)` ist durch 12 teilbar: den Faktor 3 liefert eine der
drei aufeinanderfolgenden Zahlen k-1,k,k+1; den Faktor 4 liefert bei geradem
k sein Quadrat, bei ungeradem k das Produkt der Nachbarn. Abschnitt 2 genügt.
Für k=1 gilt die Identität unmittelbar.

Für y=F^2(x) folgt F^2(y)=y. Also liegt jedes x spätestens nach zwei Anwendungen
auf einem Fixpunkt oder Zweierzyklus. Das gilt für **alle 360 Klassen**.

Ferner ist F^2 selbst idempotent und bildet auf die gesamte Menge der
periodischen Punkte ab. Die fünf idempotenten Abbildungen sind genau
`P_1,P_4,P_9,P_12,P_13` (Kompositionstafel oder Lösung von nu(k^2)=k).
Ihre Bildgrößen sind 360,16,75,8,175. Nicht mit den acht idempotenten
**Ringelementen** verwechseln: hier sprechen wir von Abbildungen.

## 4. Vollständige Übersicht

Vorschritte = minimale Zahl von Anwendungen bis zum Eintritt in einen Zyklus.
Die Spalte Zweierzyklen zählt Zyklen, nicht die darin enthaltenen Punkte.

| k | Bildgröße | Fixpunkte | Zweierzyklen | max. Vorschritte |
|---:|---:|---:|---:|---:|
| 1 | 360 | 360 | 0 | 0 |
| 2 | 36 | 8 | 4 | 2 |
| 3 | 75 | 45 | 15 | 1 |
| 4 | 16 | 16 | 0 | 1 |
| 5 | 175 | 75 | 50 | 1 |
| 6 | 12 | 8 | 0 | 2 |
| 7 | 175 | 105 | 35 | 1 |
| 8 | 16 | 8 | 4 | 1 |
| 9 | 75 | 75 | 0 | 1 |
| 10 | 24 | 16 | 0 | 2 |
| 11 | 175 | 45 | 65 | 1 |
| 12 | 8 | 8 | 0 | 1 |
| 13 | 175 | 175 | 0 | 1 |
| 14 | 24 | 8 | 4 | 2 |

Jedes Paar (Bildgröße, Fixpunktzahl) ist verschieden. Da beide Größen bei
Graphisomorphie erhalten bleiben, sind die 14 gerichteten Graphen auch ohne
Restklassenbeschriftung paarweise nicht isomorph. Auf U(360) gibt es 12 Typen:
P_1=P_13 und P_2=P_14; die 12 verbleibenden Paare (Einheitenbildgröße,
Einheitenfixpunktzahl) sind verschieden. Damit sind OQ-005/OQ-009 für positive
Potenzabbildungen auf R bzw. U(360) in diesem Modul beantwortet; andere
Dynamiken oder ein darüber hinausgehender Neuheitsanspruch folgen nicht.

## 5. Exakte lokale Formel, nicht nur ein Graphprogramm

Modulo p^e, für k>=2, sei ein Nicht-Einheitselement ungleich 0 von Bewertung
v. Seine Eintrittszeit in den Fixpunkt 0 ist das kleinste t>=0 mit `v*k^t>=e`.
Für 0 selbst ist t=0. Für eine lokale Einheit der multiplikativen Ordnung d
schreibe `d=d_parallel*d_perp`, wobei d_parallel alle Primfaktorpotenzen von d
enthält, deren Primzahl k teilt, und gcd(d_perp,k)=1. Dann

```math
\mu=\min\{t\ge0:d_{\parallel}\mid k^t\},\qquad
\lambda=\operatorname{ord}_{d_{\perp}}(k),
```

mit `ord_1(k)=1`. Denn die Gleichheit zweier Iterierter ist genau
`d | k^t(k^ell-1)`. Die ersten Faktoren müssen durch k^t vernichtet werden;
auf dem teilerfremden Anteil bleibt die angegebene Ordnung.
Global ist mu das Maximum der drei lokalen Eintrittszeiten und lambda das
kgV der drei lokalen Perioden. Für k=1 ist überall mu=0, lambda=1.
Diese Formel wird separat gegen jeden der 5.040 Graphdatensätze geprüft.

Für die Potenzfasern gilt die CRT-Produktformel: Die Zahl der Wurzeln von y
ist das Produkt der drei lokalen Wurzelzahlen. Auf den Einheiten ist jeder
nichtleere Potenzfaser gleich groß, nämlich

```math
|\ker P_k|=\gcd(k,2)^2\gcd(k,6)\gcd(k,4),\qquad
|P_k(U(360))|=96/|\ker P_k|.
```

Das folgt aus `U(360) = C_2 x C_2 x C_6 x C_4`; jede nichtleere Faser eines
Gruppenhomomorphismus ist eine Kernnebenklasse. Auf dem gesamten Ring sind
die Fasern im Allgemeinen nicht gleich groß; der volle Export listet jede.

## 6. Was die beiden zusätzlichen Abbildungen speichern

Die bereits im Core verwendete Zerlegung ist `x=r+n`, mit `r=x^13`, `rn=0`
und `n^3=0`. Hieraus folgt direkt

```math
x^k=r^k\quad(k\ge3),\qquad x^2=r^2+n^2=x^{14}+n^2.
```

Sie erklärt, warum alle stabilen Potenzabbildungen durch das 175-elementige
reguläre Skelett faktorisieren. Nur P_1 und P_2 bewahren zusätzliche nilpotente
Information. Für das zweite Stück gilt sogar

```math
x^2-x^{14}\equiv
\begin{cases}180,&x\equiv2\pmod4,\\0,&\text{sonst}\end{cases}\pmod{360}.
```

**Beweis.** Modulo 9 und 5 sind die beiden Potenzen gleich. Modulo 8 besteht
genau bei Bewertung v_2(x)=1 eine Differenz 4; sonst ist sie 0. Die eindeutige
CRT-Hebung von (4,0,0) ist 180. Genau 90 der 360 Klassen sind 2 modulo 4.
Dies ist eine konkrete Spezialisierung der Schicht `N^2=(180)`, kein
unerklärter numerischer Zufall. Sie erklärt auch den Unterschied zwischen
P_2 (36 Bildpunkte) und P_14 (24), obwohl beide auf allen Einheiten gleich sind.

## 7. Primzahlpotenzen: exakt über die Fasern zählen

Für X>=1, e>=1, definiere Pi_e(X;r) als Zahl der Primzahlen p mit
`p^e<=X` und `p^e=r (mod 360)`. Dann gilt auf **allen** Restklassen

```math
\Pi_e(X;r)=\sum_{\substack{0\le a<360\\P_e(a)=r}}
\pi(\lfloor X^{1/e}\rfloor;360,a).
```

**Beweis.** Partitioniere die Primzahlbasen nach ihrem Rest a. Auf jeder
Klasse ist P_e konstant; die Größengrenze ist genau die ganzzahlige e-te
Wurzel. Damit zählt jede Primzahlbasis genau einmal. Für Einheitenziele
tragen nur Einheitenbasen bei; für die übrigen Klassen sind die natürlichen
Primzahlbasen 2,3,5 explizit zu berücksichtigen.

**Achtung:** Für die Restklassenabbildung darf e durch nu(e) ersetzt werden,
aber niemals für die Grenze X^(1/e). P_15=P_3 bedeutet nicht, dass p^15 und
p^3 bei gleicher Zahlengrenze gleich häufig sind.

Die Daten enthalten alle 236 echten Primzahlpotenzen `p^e<=10^6`, e>=2,
mit Zeugen `(n,p,e,n mod 360)`. 200 haben Basis >5, 36 eine Basis aus 2,3,5.
Pro Exponent: 168 Quadrate, 25 Kuben, 11 vierte, 6 fünfte, je 4 sechste und
siebte, 3 achte, je 2 neunte bis zwölfte und je 1 dreizehnte bis neunzehnte
Potenz. Höhere fehlen, da `2^20>10^6`. Die Werte sind endlich, keine Asymptotik.

Die 165 Quadrate mit Basis >5 verteilen sich auf das Quadrathexagon als
`1:27, 49:28, 121:27, 169:30, 241:24, 289:29`. Diese Unterschiede kommen von
der gezählten Primzahlbasis, nicht von unterschiedlichen abstrakten
Fasergrößen: jede der sechs Einheitenfasern besitzt genau 16 Klassen.

## 8. Daten und Reproduktion

```bash
python exact/generate_power_atlas.py --check
python exact/verify_power_atlas.py --check
python exact/generate_power_atlas.py --export /tmp/mod360-power-atlas
```

Im Repo: `data/power-atlas-v1/maps.csv` enthält jede gerichtete Kante aller
14 Graphen, `summary.csv` die Zusammenfassung, `composition.csv` die gesamte
Komposition und die beiden Primzahlpotenzdateien die Zählung plus alle Zeugen.
Der Export ergänzt `expanded-atlas.json`: alle Fasern (auch leere), alle
kanonisch rotierten Zyklen und pro Startklasse Eintrittszeit, Periode,
ersten Zykluspunkt und Zyklusminimum. Damit sind die Zuführungswege durch
die Kanten und Eintrittsdaten vollständig bestimmt, nicht nur durch Summen.

Der Generator nutzt direkte modulare Potenzen und Pfadlisten. Der getrennte
Verifier verwendet CRT mit wiederholter Multiplikation, Floyd-Zyklensuche
und zusätzlich die lokale Bewertungs-/Ordnungsformel. Die Primzahlbasen
werden einmal gesiebt und einmal durch Probedivision konstruiert. Kein
Float, kein Statistikmodell und kein Import aus dem Zählungs-PR nötig.
Das Zertifikat bindet beide Programme, fünf CSVs und den vollständigen
JSON-Export per SHA-256. Zwei Programme desselben Assistenten sind kein E4.

## 9. Literatur und Neuheit

Die Literatur wurde hier gezielt zur Einordnung konsultiert, nicht als
Ersatz der vorstehenden Beweise. Nur die Abstracts/Publikationsseiten der
beiden Arbeiten wurden für diese Einordnung gelesen; kein Volltextaudit.

- Yangjiang Wei, Gaohua Tang (2015), *The iteration digraphs of finite
  commutative rings*, Turkish Journal of Mathematics 39, 872–883.
  https://journals.tubitak.gov.tr/math/vol39/iss6/8/ ; DOI 10.3906/mat-1503-2.
  Untersucht genau gerichtete Iterationsgraphen von a -> a^k auf endlichen Ringen.
- Amplify Sawkmie, Madan Mohan Singh (2018), *On the uniqueness of the
  factorization of power digraphs modulo n*, Rend. Sem. Mat. Univ. Padova 140,
  185–219. https://ems.press/journals/rsmup/articles/15870 ; DOI 10.4171/RSMUP/8.
  Die Publikationsseite beschreibt CRT-Zerlegung und Isomorphiefragen.
- NIST DLMF 27.2, eindeutige Primfaktorzerlegung und Euler–Fermat:
  https://dlmf.nist.gov/27.2 .

Abruf: 2026-09-16. Kein weltweiter Neuheitsanspruch. Der Gewinn ist eine
vollständige, überprüfbare MOD-360-Spezialisierung und ihre Verbindung mit
konkreten Primzahlpotenzen. Historische Operatorbehauptungen bleiben getrennt.
