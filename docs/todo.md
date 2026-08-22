# Tâches — lunar-eclipse-maestro

## En cours

- [ ] **Recaler le site** — commune / GPS France (remplacer le placeholder Paris) → YAML + simu FOV 280 mm et 15-85 mm (U1→moonset, marges ≥ 10 %)
- [ ] **Scénario 600D-Tele** — cadrage fixe vs recentrage ; plafond de pose vs filé (~4,5 px/s à 280 mm) ; LEM si Mac compatible, sinon intervallomètre
- [ ] **Scénario 100D chapelet** — focale à calculer pour U1→moonset ; intervalle ~1,5–2 Ø ; AEB ; **déclenchement manuel dédié au MAX** (pas de coïncidence horaire)
- [ ] **Test Mac LEM** — l'appli démarre-t-elle (macOS ≤ Mojave) ? 600D / 100D vus en USB ?

## Bloqué

_(aucune tâche bloquée)_

## Backlog

- [ ] Plan d'exposition lunaire (tables Espenak / calculatrice Jubier) — rampe umbra de plusieurs EV ; **ne pas** porter `chapelet_exposure.py` solaire tel quel (ND + Soleil)
- [ ] Scripts LEM `scripts/lem/` si le Mac le permet (analogues `basic`/`deluxe`)
- [ ] Analyseur de séquence hors ligne si le format de script LEM le justifie
- [ ] Fiche lieu dédiée `docs/lieux/<commune>-2026.md` une fois le GPS connu
- [ ] Variantes météo / extinction à basse altitude (~8° au MAX à Paris)

## Terminé

- [x] **Infrastructure Cursor** (2026-08-22) — `AGENTS.md`, rules `.mdc`, mémoire, skill `session-summary`, commande `resume-session`
- [x] **Miroir HTML LEM + build PDF** (2026-08-22) — `scripts/mirror.sh`, `scripts/build-pdf.sh`
- [x] **Simulateur FOV lunaire** (2026-08-22) — noyau SEM transféré, overlay ombre, placeholder Paris — DEC-006
