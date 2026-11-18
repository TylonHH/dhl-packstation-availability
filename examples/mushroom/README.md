# Mushroom-Beispiele für DHL Packstation

Diese optionalen Karten zeigen die fünf Sensoren der Integration. Die Werte werden aus Home Assistant gelesen; Beispielzahlen sind nicht fest eingetragen.

## Voraussetzungen

- Eine bereits eingerichtete DHL Packstation mit den Sensoren S, M, L, XL und gesamt.
- [Mushroom](https://github.com/piitaya/lovelace-mushroom), über HACS installiert und als Dashboard-Ressource geladen. Die Beispiele wurden mit Version **v5.2.3** geprüft. Beachte auch die Home-Assistant-Mindestversion von Mushroom.
- Keine Helfer, keine Layout Card und kein Card Mod erforderlich.

## Einfügen

1. Eine Ansicht wählen: [horizontal.yaml](horizontal.yaml) mit umbrechenden Chips oder [vertical.yaml](vertical.yaml) mit vier Kacheln in zwei Spalten.
2. Die YAML-Datei öffnen und über **Raw** ihren vollständigen Inhalt kopieren.
3. Die fünf unten aufgeführten Beispiel-Entitätsnamen durch die eigenen Sensor-IDs ersetzen. Die tatsächlichen IDs stehen unter **Einstellungen → Geräte & Dienste → Entitäten** bei der jeweiligen Packstation. Ein Sensor kann mehrfach in der Vorlage vorkommen; alle Vorkommen ersetzen.
4. Optional den Untertitel `Meine Packstation` anpassen.
5. **Dashboard bearbeiten → Karte hinzufügen → Manuell** öffnen, den vollständigen YAML-Inhalt einfügen und die Vorschau prüfen. Bei mehreren Stationen die Karte je Station mit den passenden fünf Sensoren hinzufügen.

| Platzhalter im Beispiel | Eigener Sensor |
| --- | --- |
| `sensor.meine_packstation_freie_facher_s` | Freie Fächer S |
| `sensor.meine_packstation_freie_facher_m` | Freie Fächer M |
| `sensor.meine_packstation_freie_facher_l` | Freie Fächer L |
| `sensor.meine_packstation_freie_facher_xl` | Freie Fächer XL |
| `sensor.meine_packstation_freie_facher_gesamt` | Freie Fächer gesamt |

Die Platzhalter sind keine zusätzlichen Sensoren und werden nicht automatisch angelegt. Die Namen können sich je nach Stationsname, Sprache und eigener Benennung unterscheiden.

## Darstellung und Layout

- **Horizontal:** Die Mushroom-Chips stehen nebeneinander und können bei wenig Platz automatisch umbrechen.
- **Vertikal:** Das eingebaute Grid zeigt zwei Spalten. Mit `columns: 1` stehen alle vier Größen untereinander; mit `columns: 4` nebeneinander. Diese Spaltenzahl wird nicht automatisch mit der Bildschirmbreite geändert.
- **Farben:** Grün bedeutet mindestens ein freies Fach, Rot bedeutet `0`, Grau bedeutet unbekannt oder nicht verfügbar. Daraus lässt sich keine prozentuale Auslastung ableiten.
- **DHL-Datenstand:** Die Karte zeigt den `source_timestamp` der DHL-Antwort, nicht den letzten Dashboard-Aufruf. Ist er älter als 30 Minuten, erscheint eine Warnung. Ein fehlender oder deutlich zukünftiger Zeitstempel wird ebenfalls angezeigt. Die Fachzahlen können deshalb trotz vorhandener Werte veraltet sein.
- **Details:** Ein Klick auf eine Fachzahl öffnet die Home-Assistant-Detailansicht dieses Sensors.

Die Beispiele lesen nur bestehende Sensoren. Sie berechnen kein historisches Maximum und erkennen keine Leerung. Diese Funktionen sind in der Integration noch nicht implementiert.

Wenn `Custom element doesn't exist: mushroom-...` erscheint, zuerst die Mushroom-Installation und die Dashboard-Ressource prüfen und den Browser neu laden. Wenn Werte als unbekannt erscheinen, die eingesetzten Entitäts-IDs und den Zustand der Integration prüfen.
