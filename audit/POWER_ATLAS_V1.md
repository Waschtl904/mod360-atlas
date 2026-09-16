# Review: vollständiger MOD-360-Potenzatlas V1

Basis: `762e42d0931cba5e56e236c3ceb62dfeed2e1cee`.
Eigenständiger Branch gegen main; PR #1 (Integer Census) bleibt unangetastet.
Keine neue Behauptung zur Riemannschen Vermutung oder zu Objekt X.

## Lesereihenfolge

1. `dynamics/power-atlas-v1.md`: Definitionen, fünf vorgeschlagene Claims M360-033–037, Beweise und Literaturabgrenzung.
2. `data/power-atlas-v1/summary.csv` und `composition.csv`.
3. `exact/generate_power_atlas.py`, anschließend `exact/verify_power_atlas.py`.
4. `certificates/power-atlas-v1.json` und die vollständigen CSVs.

## Tatsächlich lokal ausgeführt

- Generator `--check`: MATCH, unveränderte Tabellen.
- Verifier `--check`: PASS; alle 5.040 Vertexdatensätze und 70.560 Kompositionsfälle.
- Drei Wege für die Dynamik: direkte Pfadlisten, CRT/Floyd und lokale Bewertungs-/Ordnungsformel.
- Primzahlpotenzen: Sieb versus Probedivision, 236 konkrete Zeugen und 6.480 Zählzellen.
- Mutationstest in einer temporären Kopie: Generator auf falsches Bild `P_k(0)=1` geändert und sämtliche Tabellen daraus regeneriert. Der getrennte Verifier verwirft dies mit `RuntimeError: CRT maps`. Also nicht bloß ein Prüfsummenvergleich gegen dieselben falschen Daten.

Diese Tests sind Programme desselben Assistenten, kein unabhängiges externes E4-Review.
GitHub-CI am veröffentlichten Commit muss separat gelesen werden; der Status in
einer eingecheckten JSON-Datei allein beweist keinen ausgeführten CI-Lauf.

## Angriffsstellen

- Gewöhnliche Potenzfolge versus Iteration: a^(k^t), nicht a^(kt).
- Exponent 0 ist ausgeschlossen; k=1 muss als Identität separat stimmen.
- Globale Periodizität erst ab Exponent 3; Ausnahmen 1/13 und 2/14 prüfen.
- In F^4=F^2 bezeichnet die Hochzahl Komposition, nicht punktweise Potenz.
- Vorschritte exakt minimal, Zyklen kanonisch rotiert, Fixpunkte versus Zweierzykluspunkte nicht verwechseln.
- Gleich große Bilder allein beweisen keine Graphisomorphie. Hier unterscheiden bereits die Paare Bildgröße/Fixpunktzahl sämtliche Typen.
- Unterscheidung zwischen fünf idempotenten Abbildungen und acht idempotenten Ringelementen.
- In der Primzahlpotenz-Zählformel den tatsächlichen Exponenten in der Größengrenze behalten; nur die Residuenabbildung periodisch reduzieren.
- Kleine Primzahlen 2,3,5 und alle 360 Zielklassen einbeziehen.
- Literatur wurde anhand der Abstracts eingeordnet; keine Behauptung eines vollständigen Neuheitsaudits.

## Reproduktion ohne Schreibzugriff

```bash
python exact/generate_power_atlas.py --check
python exact/verify_power_atlas.py --check
```

Vollständiger Export: `python exact/generate_power_atlas.py --export /tmp/mod360-power-atlas`.
Kein automatischer Merge und keine automatische Registry-/Core-Promotion.
