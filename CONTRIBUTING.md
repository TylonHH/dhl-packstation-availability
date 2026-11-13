# Mitwirken

Fehlerberichte und Pull Requests sind willkommen. Bitte beschreibe bei Änderungen, was sich für Nutzer ändert und wie du es geprüft hast. Für neue Logik ergänze einen kleinen Regressionstest.

## Commit-Namen und Releases

Nutze [Conventional Commits](https://www.conventionalcommits.org/):

- `feat: ...` für eine neue Funktion
- `fix: ...` für eine Fehlerbehebung
- `docs: ...` für reine Dokumentation
- `chore: ...` oder `ci: ...` für Wartung
- `feat!: ...` oder `fix!: ...` für eine inkompatible Änderung; erkläre sie zusätzlich mit `BREAKING CHANGE:` im Commit-Text

Bei einem Squash-Merge zählt der **Pull-Request-Titel** als Commit-Name. Bitte formuliere ihn entsprechend. Nach Änderungen auf `main` erstellt Release Please einen Release-Pull-Request mit Versionsnummer, `CHANGELOG.md` und der Version in `manifest.json`. Erst nach dessen Merge wird ein GitHub-Release erstellt. Vor Version 1.0 erhöhen neue Funktionen die Nebenversion; Fehlerbehebungen erhöhen die Patch-Version.

**Nur Repository-Inhaber `@TylonHH` merged Pull Requests.** Andere können Issues und Pull Requests einreichen. Es gibt kein automatisches Mergen.
