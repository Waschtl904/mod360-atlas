# mod360-atlas

Ein reproduzierbarer mathematischer Atlas des Rings `Z/360Z`, seiner Restklassen, Strukturen und arithmetischen Muster.

> **Arbeitsprinzip:** Exakte Rechnung ist nicht dasselbe wie mathematische Neuheit. Jede Aussage erhält eine überprüfbare Claim-ID, einen Status und — falls nötig — einen getrennten Prior-Art-Eintrag.

## Warum 360?

`360 = 2^3 · 3^2 · 5` verbindet mehrere Primzahlpotenzen, besitzt viele Teiler und zerfällt durch den chinesischen Restsatz als

`Z/360Z ≅ Z/8Z × Z/9Z × Z/5Z`.

Dadurch eignet sich der Modul für lokale–globale Vergleiche, Einheitengruppen, Potenzabbildungen, Idempotente, Nilpotente, Graphen und primzahlbezogene Restklassenmuster.

## Statussystem

| Code | Bedeutung |
|---|---|
| `K` | Bekannt oder klassisch; Literaturbeleg erforderlich |
| `V360` | Durch exakte Rechnung speziell für Modul 360 verifiziert |
| `NH` | Neu innerhalb unserer Untersuchung; keine externe Neuheitsbehauptung |
| `?[O]` | Offen, ob die Aussage in der Literatur bereits vorkommt |
| `NEW` | Erst nach dokumentiertem Prior-Art-Audit zulässig |

Statuscodes dürfen kombiniert werden, etwa `K + V360`. `NH` und `NEW` sind ausdrücklich nicht synonym.

## Einstieg

1. Lies [STATUS.md](STATUS.md) und [CLAIMS.md](CLAIMS.md).
2. Erzeuge den maschinenlesbaren Atlas mit `python exact/generate_atlas.py`.
3. Prüfe die Baseline-Claims mit `python exact/verify_claims.py`.
4. Lege Beobachtungen zuerst unter `discoveries/candidates/` ab.
5. Verschiebe sie erst nach Beweis, Reproduktion und Statusprüfung nach `discoveries/verified/`.

## Struktur

- `atlas/` — alle 360 Restklassen und Ringstruktur
- `units/` — Einheitengruppe, Untergruppen und Potenzbilder
- `primes/` — primzahlfähige Klassen, Radgeometrie und Primzahlmuster
- `composites/` — Semiprime, Quadratfreiheit und Faktorisierungsreste
- `dynamics/` — Potenz- und affine Dynamik
- `harmonic/` — Fourieranalysis und arithmetische Summen
- `galois/` — zyklotomische und Frobenius-Perspektiven
- `graphs/` — relationale und Cayley-Graphen
- `exact/` — deterministische Programme und Zertifikate
- `literature/` — Prior Art und Quellenprotokoll
- `discoveries/` — Kandidaten und verifizierte Resultate

## Reproduzierbarkeit

Die Referenzskripte verwenden ausschließlich die Python-Standardbibliothek. Generierte Daten müssen aus dem Commit reproduzierbar sein; Zertifikate dokumentieren Programmversion, Parameter und geprüfte Assertions.

## Zitierweise

Bis eine formelle Veröffentlichung und ein archivierter Release existieren, bitte Repository-URL, Commit-SHA und Abrufdatum angeben.
