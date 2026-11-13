# Versionsverlauf

Änderungen erscheinen hier nach Version. Die GitHub-Releases enthalten dieselben Hinweise.

## [0.2.0](https://github.com/TylonHH/dhl-packstation-availability/compare/v0.1.1...v0.2.0) (2026-11-13)

### Neue Funktionen

- Packstationen mit fünfstelliger Postleitzahl und dreistelliger Stationsnummer hinzufügen.
- Mehrere Stationen als eigene Einträge mit getrennten Endpunkten und Sensoren nutzen.
- Führende Null der Postleitzahl bei der Eingabe behalten und nur für den DHL-Aufruf entfernen.

### Kompatibilität

- Bereits eingerichtete Stationen funktionieren ohne erneute Einrichtung weiter.

## [0.1.1](https://github.com/TylonHH/dhl-packstation-availability/compare/v0.1.0...v0.1.1) (2026-11-13)

### Darstellung

- Eigenständiges Symbol für Home Assistant ergänzt.
- Beschreibung im Einrichtungsdialog auf Deutsch und Englisch erweitert.
- Anleitung zur Anzeige in HACS und Home Assistant ergänzt.

## [0.1.0](https://github.com/TylonHH/dhl-packstation-availability/releases/tag/v0.1.0) (2026-11-13)

### Erste Version

- Freie Fächer je Größe S, M, L und XL sowie Gesamtzahl als Home-Assistant-Sensoren.
- Einrichtung per Postfinder-ID und Aktualisierung alle 15 Minuten.
- HACS-Installation, deutsche Anleitung und MIT-Lizenz.

Der DHL-Postfinder-Endpunkt ist undokumentiert. Verfügbarkeit und Datenformat können sich ändern.
