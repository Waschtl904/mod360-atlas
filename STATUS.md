# Status

## Zulässige Codes

| Code | Definition | Mindestnachweis |
|---|---|---|
| `K` | Bekannt/klassisch | belastbarer Literaturbeleg |
| `V360` | exakt für 360 verifiziert | deterministischer Test oder vollständiger Beweis |
| `NH` | erstmals in diesem Projekt beobachtet | datierter Kandidat mit reproduzierbaren Daten |
| `?[O]` | Literaturstatus offen | dokumentierte, aber unvollständige Suche |
| `NEW` | nach Audit als neu eingestuft | abgeschlossenes Prior-Art-Protokoll und unabhängige Prüfung |

## Kombinationsregeln

- `K + V360`: klassisches Resultat, zusätzlich für 360 rechnerisch geprüft.
- `NH + V360 + ?[O]`: projektintern neue, exakt geprüfte Beobachtung mit offenem Literaturstatus.
- `NEW + V360`: zulässig, wenn sowohl mathematische Prüfung als auch Prior-Art-Audit abgeschlossen sind.
- `NH` allein behauptet niemals wissenschaftliche Neuheit.
- `?[O]` darf nicht stillschweigend zu `NEW` werden.

## Evidenzstufen

| Stufe | Bedeutung |
|---|---|
| `E0` | informelle Beobachtung |
| `E1` | reproduzierbares Experiment |
| `E2` | exhaustive endliche Verifikation |
| `E3` | mathematischer Beweis |
| `E4` | unabhängig reproduziert oder begutachtet |

## Claim-Pflichtfelder

Jeder Claim enthält: ID, präzise Aussage, Status, Evidenzstufe, Scope, Methode, Artefakt/Beweis, Literaturverweis, Autor und Datum.
