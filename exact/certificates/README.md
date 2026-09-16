# Zertifikate

Dieser Ordner enthält maschinenlesbare Nachweise aus deterministischen Prüfungen.

## Mindestfelder

- Claim-ID
- Modul und Parameter
- Methode und Programmversion
- UTC-Zeitstempel
- geprüfte Werte und Assertions
- kryptografische Prüfsumme, soweit sinnvoll

Erzeuge das Baseline-Zertifikat mit:

```bash
python exact/verify_claims.py
```
