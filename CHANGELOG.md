# Versionsverlauf

Änderungen erscheinen hier nach Version. Die GitHub-Releases enthalten dieselben Hinweise.

## [0.3.0](https://github.com/TylonHH/dhl-packstation-availability/compare/v0.2.4...v0.3.0) (2026-11-21)


### Neue Funktionen

* support DHL DeinFach lockers ([#11](https://github.com/TylonHH/dhl-packstation-availability/issues/11)) ([8ded788](https://github.com/TylonHH/dhl-packstation-availability/commit/8ded788fe2a091af753a15f21747303dbe1b3cf6))

## [0.2.4](https://github.com/TylonHH/dhl-packstation-availability/compare/v0.2.3...v0.2.4) (2026-11-19)


### Fehlerbehebungen

* show numeric history and link to public station details ([#7](https://github.com/TylonHH/dhl-packstation-availability/issues/7)) ([24b57f6](https://github.com/TylonHH/dhl-packstation-availability/commit/24b57f63b132198aa57b21a394961b5dcfaef714))

## [0.2.3](https://github.com/TylonHH/dhl-packstation-availability/compare/v0.2.2...v0.2.3) (2026-11-18)

### Dashboard-Beispiele mit Mushroom

- **Horizontal:** Kompakte S/M/L/XL-Chips, die bei wenig Platz automatisch umbrechen.
- **Vertikal:** Vier Kacheln in zwei Spalten; die Spaltenzahl lässt sich auf eine oder vier ändern.
- Beide Varianten zeigen freie Fächer, Gesamtzahl, Adresse und den DHL-Datenstand. Unbekannte Werte bleiben von `0` unterscheidbar; nach 30 Minuten ohne neue Quelldaten erscheint eine Warnung.
- Anleitung zum Einsetzen der eigenen Sensoren und Einfügen als manuelle Dashboard-Karte. Keine zusätzlichen Helfer, keine Layout Card und kein Card Mod erforderlich. Die Beispiele wurden mit Mushroom v5.2.3 geprüft.

### Beispiele verwenden

Mushroom über HACS installieren, die fünf Beispiel-Entitätsnamen durch die eigenen DHL-Sensoren ersetzen und die vollständige YAML-Datei als manuelle Karte einfügen:

- [Horizontale Karte](https://github.com/TylonHH/dhl-packstation-availability/blob/v0.2.3/examples/mushroom/horizontal.yaml)
- [Vertikale Karte](https://github.com/TylonHH/dhl-packstation-availability/blob/v0.2.3/examples/mushroom/vertical.yaml)
- [Anleitung und Entitätszuordnung](https://github.com/TylonHH/dhl-packstation-availability/blob/v0.2.3/examples/mushroom/README.md)

Die Karten werden nicht automatisch im Dashboard angelegt. Dieses Release ergänzt Beispiele und Dokumentation; die Abfrage der DHL-Daten und bestehende Entitäten bleiben unverändert. Historische Maximalwerte und eine Erkennung vermuteter Leerungen sind noch nicht enthalten.

### Dokumentation

* add Mushroom dashboard examples ([#5](https://github.com/TylonHH/dhl-packstation-availability/issues/5)) ([ecc10ea](https://github.com/TylonHH/dhl-packstation-availability/commit/ecc10ea09350a8dad485ac7725243c62afc26545))

## [0.2.2](https://github.com/TylonHH/dhl-packstation-availability/compare/v0.2.1...v0.2.2) (2026-11-18)


### Fehlerbehebungen

* keep Packstation setup forms serializable ([#3](https://github.com/TylonHH/dhl-packstation-availability/issues/3)) ([32a68b4](https://github.com/TylonHH/dhl-packstation-availability/commit/32a68b431b9dc2de14c739297dcf365b8ce28874))

## [0.2.1](https://github.com/TylonHH/dhl-packstation-availability/compare/v0.2.0...v0.2.1) (2026-11-14)


### Fehlerbehebungen

* prepare Marketplace catalog validation ([#1](https://github.com/TylonHH/dhl-packstation-availability/issues/1)) ([d3eaffa](https://github.com/TylonHH/dhl-packstation-availability/commit/d3eaffafc3aae48653bf7d51a66747569f3d981a))

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
