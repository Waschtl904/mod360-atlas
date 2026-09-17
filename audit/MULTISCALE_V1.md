# Auditauftrag: Mehrbereichsvergleich MOD 360

Basis: `762e42d0931cba5e56e236c3ceb62dfeed2e1cee`, live am 2026-09-17 gelesen.
Neue getrennte Schicht; main, PR #1 und PR #2 werden nicht verändert.
Kein Merge und keine automatische Core-/Registry-Promotion.

## Tatsächlich lokal durchgeführt

Generator `--write` und getrennte Verifikation `--write` erfolgreich; anschließend
beide read-only `--check`-Befehle erfolgreich. Referenzgrenzen 36.000/360.000/
3.600.000; alle 4.320 Rohzählzellen und 36 Auswertungszeilen stimmen.
Der Verifier führt selbst Boundary- und Mutationstests aus. Die kleine Grenze
361 muss abgelehnt werden (nur volle 360er-Blöcke); die Datenmutation +1 bei
Primzahlen in Klasse 49 wird durch erneute Zählung erkannt, nicht erst durch Hashes.
Der vollständige Export einschließlich der 3.456 feinen Residuen wird ebenfalls
rekonstruiert und gehasht. Die ausgedehnte Prim-/Kompositzählung von PR #1 ist
kein Import und keine Laufzeitabhängigkeit dieses Moduls.

## Zuerst angreifen

1. Unterschied 360 Restklassen / 96 Unit-Klassen; verschiedene Nenner 6/90 und 6/18.
2. Endpunktkonvention (lo,hi], gleiche Exposition und Ausnahme der Zahl 1.
3. Ungeordnete Primpaare: p² einmal, pq einmal; p<q sind nicht verschiedene Primreste.
4. Unit-Quadrate sitzen in Q, aber Zahlen pq mit p<q können dort ebenfalls sitzen.
5. Delta nach Entfernen der Quadrate: Vorzeichen und Faktor 1/6 kontrollieren.
6. Zwei grobe Vergleichsfamilien (1 und 19 mod 30): je drei Q-Hebungen; Faktor 4/5.
7. Feines Gegenbeispiel im mittleren disjunkten Bereich: -13/18 darf nicht fehlen.
8. 88 feine gegen 7 zentrierte grobe Freiheitsgrade: keine Signifikanz aus Energieanteilen.
9. Mehrere Cutoffs sind weder unabhängige Stichproben noch logarithmische Dichte.
10. Zahlengrenzen waren vorab gewählt, Zusatzdiagnosen nicht statistisch präregistriert.

## Reproduktion

```bash
python exact/generate_multiscale.py --check
python exact/verify_multiscale.py --check
```

Beide verwenden nur die Standardbibliothek. Der Verifier regeneriert zusätzlich
in temporären Ordnern, überschreibt aber keine versionierten Daten. Das Zertifikat
ist deterministisch und enthält keine Laufzeit- oder Datumsfelder.
Der tatsächliche Actions-Status gehört in einen verifizierten PR-Kommentar,
nicht als vorweggenommenes PASS in diese Datei. Kein E4-Neuheitsaudit behauptet.
