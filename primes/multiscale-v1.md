# MOD 360: Mehrbereichsvergleich mit Quadrat- und Hebungskontrolle

**Stand 2026-09-17.** Eigenständiges Review-Modul auf Core V3, Basis
`762e42d0931cba5e56e236c3ceb62dfeed2e1cee`. Der Modul bleibt 360.
PR #1 (Millionenzählung) und PR #2 (Potenzatlas) werden nicht verändert oder
als bereits gemergt vorausgesetzt. Keine automatische Core-/Registry-Promotion.

## 1. Vorgegebene Grenzen und Aussagebereich

Untersucht werden die bereits vor dieser Rechnung gewählten Grenzen
`36.000, 360.000, 3.600.000`, jeweils kumulativ und als disjunkte Intervalle
`(0,36000]`, `(36000,360000]`, `(360000,3600000]`.
Alle Intervallenden sind Vielfache von 360. Daher enthält jede der 360
Restklassen genau `(hi-lo)/360` positive Zahlen im jeweiligen Intervall.
Der kumulative erste Bereich und das erste Intervall sind identische Daten,
nicht zwei unabhängige Beobachtungen. Auch die kumulativen Bereiche sind
verschachtelt, nicht statistisch unabhängig.

Die Rohdaten enthalten Primzahlen, Semiprimzahlen, quadratfreie Zahlen und
Primzahlquadrate in **allen 360 Klassen**. Abgeleitet werden Komposita und
Semiprimzahlen mit verschiedenen Primfaktoren. Die Kontrastanalysen beziehen
sich ausdrücklich auf die **96 Einheitenklassen**.

Konventionen: 0 ist ausgeschlossen. 1 ist weder prim noch komposit, aber
quadratfrei. Semiprim bedeutet `pq` mit `p<=q`, einschließlich `p^2`.
`distinct_semiprimes` bedeutet `p<q`, nicht verschiedene *Restklassen* der
Primfaktoren. Ein solches Produkt kann durchaus im Quadrathexagon liegen.
Beispiel: `721=7*103=1 mod 360`.

## 2. Referenzzählungen

| Obergrenze | Zahlen pro Klasse | Primzahlen gesamt | Komposita gesamt | Semiprimzahlen gesamt | Quadratfreie inkl. 1 |
|---:|---:|---:|---:|---:|---:|
| 36.000 | 100 | 3.824 | 32.175 | 8.861 | 21.885 |
| 360.000 | 1.000 | 30.757 | 329.242 | 79.161 | 218.866 |
| 3.600.000 | 10.000 | 256.726 | 3.343.273 | 715.106 | 2.188.544 |

In jedem kumulativen Bereich liegen genau drei Primzahlen außerhalb der
Einheitenklassen: 2,3,5. Die Bestände sonstiger Kategorien überlappen.
Für jede Klasse gilt die exakte Partition
`exposure = primes + composites + one`, mit `one=1` nur für Klasse 1 und lo=0.
Eine Gegenbewegung von Prim- und Kompositzahlen allein ist keine Entdeckung.

## 3. Der Vergleich muss nach Gruppengröße normiert werden

Sei `U=U(360)` und

```math
Q=U^2=\{1,49,121,169,241,289\},\qquad |Q|=6,\quad |U\setminus Q|=90.
```

Für einen Zählvektor `v(r)` auf U definieren wir den Kontrast

```math
\Delta(v)=\frac{\sum_{r\in U\setminus Q}v(r)}{90}
          -\frac{\sum_{r\in Q}v(r)}{6}.
```

Positiv bedeutet: im Mittel **pro Restklasse** mehr in U\Q als in Q.
Negativ bedeutet einen Vorteil der sechs Quadratklassen. Dies sind mittlere
Anzahlen im gewählten endlichen Bereich, keine Wahrscheinlichkeiten oder
Signifikanzwerte. Bei Vergleich verschiedener Bereichslängen kann zusätzlich
durch die gemeinsame Exposition geteilt werden; dadurch ändert sich das
Vorzeichen nicht. Die unterschiedlichen Gesamtzahlen 6 versus 90 werden
niemals unnormalisiert als Präferenz interpretiert.

| Obergrenze | Delta Primzahlen | Delta Semiprimzahlen inkl. p² | Delta nur pq mit p<q |
|---:|---:|---:|---:|
| 36.000 | 317/90 ≈ +3,522 | -421/90 ≈ -4,678 | 82/45 ≈ +1,822 |
| 360.000 | 473/45 ≈ +10,511 | -1399/90 ≈ -15,544 | 191/90 ≈ +2,122 |
| 3.600.000 | 2323/90 ≈ +25,811 | -1841/45 ≈ -40,911 | 623/90 ≈ +6,922 |

Alle Brüche sind exakt; die Dezimalwerte dienen nur der Lesbarkeit.
Die umgekehrte Richtung für alle Semiprimzahlen und Primzahlen ist nicht als
neue Gesetzmäßigkeit zu verbuchen (Literatur siehe Abschnitt 9).

### Ein vollständig erklärbarer Anteil

Schreibe S für Semiprimzahlen, T für Produkte verschiedener Primzahlen und
B für Primzahlquadrate. Dann `S=T+B`. Alle Quadrate mit Basis p>5 liegen in Q.
Daher gilt für jeden kumulativen Bereich X (und mit Differenzen für Intervalle)

```math
\Delta(T;X)=\Delta(S;X)+\frac{\#\{p>5:p\text{ prim},\ p^2\le X\}}6.
```

**Beweis:** Außerhalb Q fällt beim Entfernen der Quadrate kein Unit-Zählwert
weg; die Gesamtsumme auf Q fällt genau um die Zahl dieser Quadrate. Einsetzen
in die Definition von Delta liefert die Formel. Dies benutzt nur die bereits
bekannte Potenzbildstruktur, keine Hypothese über Primzahlverteilung.

Die drei Quadratbeiträge sind `39/6,106/6,287/6`. Sie überkompensieren den
negativen Semiprim-Kontrast in allen drei kumulativen Bereichen. Bei 3.600.000:
Q enthält 27.047 Semiprimzahlen; nach Entfernen von 287 Quadraten bleiben
26.760, also exakt 4.460 pro Klasse. Die übrigen 90 Klassen enthalten 402.023,
also 4.466,922… pro Klasse. **Die gemessene Richtungsumkehr ist arithmetisch
vollständig nachvollziehbar, aber kein Satz über alle zukünftigen X.**

## 4. Getrennte Intervalle statt nur wachsender Gesamtsummen

| Intervall (lo,hi] | Delta Primzahlen | Delta Semiprimzahlen | Delta nur pq mit p<q |
|---|---:|---:|---:|
| (0,36.000] | 317/90 | -421/90 | 82/45 |
| (36.000,360.000] | 629/90 | -163/15 | 3/10 |
| (360.000,3.600.000] | 153/10 | -761/30 | 24/5 |

Auch hier sind die Vorzeichen gleichgerichtet wie in der kumulativen Tabelle.
Das sind drei vorgegebene disjunkte Bereiche, keine Messung logarithmischer
Dichten und keine Aussage, dass die Richtung zwischen den Grenzen nie wechselt.

Einzelne Spitzenplätze sind nicht stabil: Bei den kumulativen Primzahlen
führen Klasse 127 (46), dann 127/197/311 gemeinsam (334), dann Klasse 313
(2.725). Sämtliche Gleichstände werden in `comparisons.csv` erfasst. Allein
aufgrund eines solchen Rangplatzes wird keine Klasse als dauerhaft bevorzugt
bezeichnet.

## 5. Eine zweite Kontrolle: passende MOD-30-Familien

Q liegt nur in den groben Familien `1 mod 30` und `19 mod 30`, jeweils mit
drei von zwölf Hebungen. Der Vergleich Q gegen sämtliche übrigen 90 Klassen
mischt deshalb grobe und feine Unterschiede.

Setze `A={r in U:r mod 30 in {1,19}}`, also `|A|=24` und `|A\Q|=18`. Definiere

```math
\Delta_{\rm fein}(v)=\frac{\sum_{A\setminus Q}v}{18}-\frac{\sum_Qv}{6},
\qquad
\Delta_{\rm grob}(v)=\frac{\sum_{U\setminus A}v}{72}-\frac{\sum_Av}{24}.
```

Dann gilt für **jeden** Zählvektor, ohne statistische Annahme,

```math
\boxed{\Delta(v)=\frac45\bigl(\Delta_{\rm fein}(v)+\Delta_{\rm grob}(v)\bigr).}
```

**Beweis:** Mit `t=sum_U v`, `a=sum_A v`, `q=sum_Q v` lauten die drei
Kontraste `(t-16q)/90`, `(a-4q)/18`, `(t-4a)/72`. Einsetzen ergibt die Identität.

| Kumulativ bis | Fein: Primzahlen | Fein: Semiprimzahlen | Fein: nur pq mit p<q |
|---:|---:|---:|---:|
| 36.000 | 61/18 | -40/9 | 37/18 |
| 360.000 | 34/3 | -49/3 | 4/3 |
| 3.600.000 | 226/9 | -691/18 | 85/9 |

**Wichtige Gegenkontrolle:** Im mittleren disjunkten Intervall
`(36.000,360.000]` ist der feine Kontrast für `p<q` dagegen **-13/18**, obwohl
der globale Kontrast +3/10 ist. Der grobe Beitrag +79/72 überwiegt dort.
Es wäre falsch, aus den positiven kumulativen Tabellen eine ausnahmslose
feine Richtung abzuleiten. Das Modul speichert diese Gegenbeobachtung ebenso
wie die bestätigenden Beispiele.

## 6. Vollständige Grob-/Feinzerlegung der zwölf Hebungen

Für `s in U(30)` sei `t_s=sum_{r=s mod 30}v(r)` und `t=sum_U v`. Definiere

```math
D_r=v(r)-t_{r\bmod30}/12.
```

Jede Familie hat exakt `sum D_r=0`. Die Daten exportieren die ganzzahligen
Zähler `12 v(r)-t_s`, niemals gerundete Residuen.
Es gilt die orthogonale Zerlegung der quadratischen Abweichung

```math
\sum_{r\in U}(v(r)-t/96)^2
=\sum_{s\in U(30)}12(t_s/12-t/96)^2+\sum_{r\in U}D_r^2.
```

**Beweis:** Schreibe `v(r)-t/96=D_r+(t_s/12-t/96)`. Beim Quadrieren verschwindet
jeder Kreuzterm, weil die zwölf D_r in einer Familie zu null summieren.

Für Primzahlen entfällt in den kumulativen Fenstern rund 97,88 %, 97,88 %,
96,19 % der gesamten quadratischen Abweichung auf die feine Komponente.
**Das allein ist kein Beweis einer Anomalie:** Die feine Untermenge hat 88
Freiheitsgrade, die zentrierte grobe Komponente nur 7. Es wird hier kein
stochastisches Nullmodell vorausgesetzt oder getestet. Große Anteile dürfen
nicht als Neuheits- oder Signifikanznachweis verwendet werden.

## 7. Reproduktion und Dateien

```bash
python exact/generate_multiscale.py --check
python exact/verify_multiscale.py --check
python exact/generate_multiscale.py --export /tmp/mod360-multiscale
```

Default/`--check` verändert keine versionierten Dateien. `--write` ist eine
explizite Regeneration. Andere Grenzen sind nur mit `--export` erlaubt und
müssen wachsende positive Vielfache von 360 bis 10.000.000 sein.

- `data/multiscale-v1/counts.csv`: 360 Zeilen, vier Rohzählungen an drei Grenzen.
- `data/multiscale-v1/comparisons.csv`: 36 Vergleiche, rationale Kontraste,
  quadratische Abweichungen, Extremwerte und **alle** zugehörigen Klassen.
- Der Export `expanded.json` ergänzt sämtliche 360er-Zählvektoren,
  MOD-30-Familientotale und 3.456 feine Residuen für sechs Kategorien/sechs
  Bereichsansichten. Der erste Bereich ist absichtlich in beiden Ansichten vorhanden.
- `certificates/multiscale-v1.json` bindet Programme, Tabellen und vollen Export.

Algorithmus A: SPF-Sieb und Rekurrenz für Quadratfreiheit. Algorithmus B:
Eratosthenes-Sieb, Enumeration ungeordneter Primpaare und Ausschluss von
Quadratteilern. Keine gemeinsamen Zähllisten oder Generatorimporte.
Alle **4.320 Rohzählzellen**, **36 Vergleiche** und **3.456 feinen Residuen**
werden gegengeprüft; Probedivision prüft zusätzlich Prim- und Quadratfreiheit
bis 10.000. Der Verifier testet die Grenzen 360/720/1080, lehnt 361 als
nicht blockvollständig ab und muss eine absichtlich verfälschte Primzählung
mathematisch zurückweisen. Diese Tests sind im Verifier und damit in der CI,
nicht bloß eine nachträgliche Beschreibung lokaler Versuche.

Zwei Implementierungen desselben Assistenten sind kein externes E4-Gutachten.
Ein eingechecktes PASS-Zertifikat allein ist kein Nachweis eines Actions-Laufs.

## 8. Modulregister (nur vorgeschlagen, nicht im Core promoviert)

| ID | Aussage | Status / Evidenz |
|---|---|---|
| M360-038 | Exakter Mehrbereichsdatensatz an den drei vorgegebenen Grenzen, mit gleicher Exposition aller 360 Klassen | V360, E2; nur diese endlichen Fenster |
| M360-039 | Delta(p<q)=Delta(p<=q)+Zahl der Unit-Primzahlquadrate/6 | K + V360, E3; E2 in den Referenzbereichen |
| M360-040 | Exakte Grob-/Fein-Kontrastzerlegung Delta=4/5(Delta_fein+Delta_grob) für Q innerhalb der beiden MOD-30-Familien | K + V360, E3 + E2 |
| M360-041 | Orthogonale Familie-/Hebungszerlegung der quadratischen Abweichung auf U(360) | K + V360, E3 + E2 |

Die IDs 030–037 bleiben für die früheren getrennten Module reserviert.
Keine Behauptung weltweiter Neuheit, keine Objekt-X-/RH-Brücke.

## 9. Literatur und Grenzen der Einordnung

Zur Einordnung wurden am 2026-09-17 die Publikationsseiten/Abstracts folgender
Primärarbeiten gelesen, kein Volltext-Neuheitsaudit:

- Michael Rubinstein, Peter Sarnak, *Chebyshev's Bias* (1994), Experimental
  Mathematics 3(3), 173–197, DOI 10.1080/10586458.1994.10504289.
  https://collaborate.princeton.edu/en/publications/chebyshevs-bias/
- Kevin Ford, Jason Sneed, *Chebyshev's bias for products of two primes*,
  arXiv:0908.0093 (2009); Experimental Mathematics 19(4), 385–398 (2010),
  DOI 10.1080/10586458.2010.10390630.
  https://arxiv.org/abs/0908.0093

Ford–Sneed untersuchen eine umgekehrte Bias-Richtung bei Produkten zweier
Primzahlen unter Annahmen über Dirichlet-L-Nullstellen. Das zeigt, dass die
allgemeine Richtung bereits Gegenstand etablierter Forschung ist. Es ist
**kein Beweis unserer speziellen, über viele Klassen gemittelten endlichen
Tabellen** und ersetzt nicht ihre direkte Nachrechnung. Unsere Zählungen und
Identitäten benötigen diese Hypothesen nicht; sie beweisen umgekehrt keine
entsprechenden asymptotischen Sätze oder logarithmischen Dichten.

Die zusätzliche Trennung p²/pq und die passenden MOD-30-Vergleichsfamilien
wurden nach der ersten Rechnung als diagnostische Kontrollen ergänzt; sie
werden nicht als vorab registrierter statistischer Test dargestellt. Das
Quadrathexagon und die drei Zahlengrenzen selbst waren zuvor festgelegt.
