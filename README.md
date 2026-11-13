# DHL Packstation Availability für Home Assistant

Diese inoffizielle HACS-Integration zeigt freie Fächer einer DHL-Packstation nach Größe: S, M, L, XL und gesamt. Sie liest den DHL-Postfinder-Endpunkt ohne Anmeldung oder API-Schlüssel. Jede Station wird alle 15 Minuten abgefragt.

## Voraussetzungen

- Home Assistant 2024.6 oder neuer
- Zugriff von Home Assistant auf `www.dhl.de`
- Eine Packstation, für die DHL im Postfinder `liveStatus` mit Fachzahlen liefert
- Für Installation über HACS: [HACS](https://www.hacs.xyz/docs/use/)

## Postfinder-ID finden

Öffne den [DHL Standortfinder](https://www.dhl.de/de/privatkunden/dhl-standorte-finden.html), wähle eine Packstation und suche in ihrer Detail- oder Netzwerkadresse nach `locationByPrimaryKeyPF/`. Der Teil dahinter ist die ID. Beispiel: Bei `.../locationByPrimaryKeyPF/1-23611202` ist die ID `1-23611202`. Du kannst die URL im Browser öffnen und prüfen, ob `liveStatus` die Werte `freeCompartmentsS`, `freeCompartmentsM`, `freeCompartmentsL` oder `freeCompartmentsXl` enthält.

## Installation

### HACS

1. In HACS **Drei Punkte → Benutzerdefinierte Repositories** öffnen.
2. Repository-URL `https://github.com/TylonHH/dhl-packstation-availability` eintragen und Typ **Integration** wählen.
3. **DHL Packstation Availability** installieren.
4. Home Assistant neu starten.

### Manuell

Ordner `custom_components/dhl_packstation_availability` nach `<config>/custom_components/` kopieren. Home Assistant neu starten.

## Einrichten

In **Einstellungen → Geräte & Dienste → Integration hinzufügen** nach **DHL Packstation Availability** suchen. Postfinder-ID eingeben. Für weitere Stationen die Integration erneut hinzufügen. Gleiche ID kann nur einmal eingerichtet werden.

## Auslesen

Pro Station entstehen fünf Sensoren: **Freie Fächer S**, **M**, **L**, **XL** und **gesamt**. Entitäts-IDs legt Home Assistant anhand des Stationsnamens fest. Die genaue ID steht unter **Einstellungen → Geräte & Dienste → Entitäten**. Sensorattribute `source_timestamp` und `address` zeigen Zeitpunkt der DHL-Quelldaten und Standortadresse. `0` bedeutet kein freies Fach. Fehlt eine Größe in der DHL-Antwort, ist ihr Sensor `unavailable`; Gesamt ist dann ebenfalls `unavailable`.

Beispiel einer Template-Bedingung für mindestens ein XL-Fach (Entitäts-ID anpassen):

```yaml
condition: template
value_template: "{{ states('sensor.parkdeck_freie_facher_xl') | int(0) > 0 }}"
```

Für Benachrichtigungen kannst du in der Home-Assistant-Oberfläche einen **Numerischer Zustand**-Trigger auf den gewünschten Sensor setzen, Schwelle **über 0**.

## Grenzen

Der verwendete Postfinder-Endpunkt ist keine dokumentierte öffentliche API. DHL kann Felder oder Zugriff jederzeit ändern. Nicht jede Packstation liefert Live-Fachzahlen. Werte können gegenüber der tatsächlichen Belegung verzögert sein. Bei HTTP-Fehlern oder fehlenden Daten werden Sensoren nicht als `0` ausgegeben. Diese Integration stammt nicht von DHL und ermöglicht weder Paketverfolgung noch Fachreservierung oder Öffnen einer Packstation.

Code: [MIT-Lizenz](LICENSE). DHL-Daten und Marken bleiben Eigentum ihrer jeweiligen Inhaber.
