# Tâches — lunar-eclipse-maestro

## En cours

- [ ] **Préciser les optiques** — DEC-007 encore provisoire ; 28 mm ne tient pas U1→moonset à Tournefeuille (max ~21 mm si pointage MAX, ~25 mm si milieu U1–SET)
- [ ] **Scénario 600D-Tele** — cadrage fixe vs recentrage ; 280 mm ≈ 16 min autour du MAX ; plafond de pose vs filé (~4,5 px/s) ; LEM si Mac compatible, sinon intervallomètre
- [ ] **Scénario 100D chapelet** — focale après choix d’optique ; intervalle ~1,5–2 Ø ; AEB ; **déclenchement manuel dédié au MAX** (pas de coïncidence horaire)
- [ ] **Test Mac LEM** — l'appli démarre-t-elle (macOS ≤ Mojave) ? 600D / 100D vus en USB ?

## Bloqué

_(aucune tâche bloquée)_

## Backlog

- [ ] Plan d'exposition lunaire (tables Espenak / calculatrice Jubier) — rampe umbra de plusieurs EV ; **ne pas** porter `chapelet_exposure.py` solaire tel quel (ND + Soleil)
- [ ] Scripts LEM `scripts/lem/` si le Mac le permet (analogues `basic`/`deluxe`)
- [ ] Analyseur de séquence hors ligne si le format de script LEM le justifie
- [ ] Variantes météo / extinction à basse altitude (~10,5° au MAX à Tournefeuille ; Soleil déjà levé au moonset)

## Terminé

- [x] **Infrastructure Cursor** (2026-08-22) — `AGENTS.md`, rules `.mdc`, mémoire, skill `session-summary`, commande `resume-session`
- [x] **Miroir HTML LEM + build PDF** (2026-08-22) — `scripts/mirror.sh`, `scripts/build-pdf.sh`
- [x] **Simulateur FOV lunaire** (2026-08-22) — noyau SEM transféré, overlay ombre, placeholder Paris — DEC-006
- [x] **Recaler le site Tournefeuille** (2026-08-22) — GPS, contacts UTC, YAML + fiche + simu FOV — DEC-008
- [x] **Dépôt git local + origin** (2026-08-22) — premier commit ; `origin` = github.com/hl-ply-eu/lunar-eclipse-maestro (pas de push)
