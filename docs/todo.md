# Tâches — lunar-eclipse-maestro

## En cours

- [ ] **Volume de prises (2 boîtiers)** — combien de vues pour couvrir l’éclipse
      (100D AEB cadence × durée U1−ε→set ; 600D stacks 7 × 2 EV aux instants
      clés + vues entre les stacks). Ne pas refaire le §11 (span / DxO).
      Point d’entrée : [formes-prise-de-vue.md](formes-prise-de-vue.md) §12,
      [memory/2026-08-22-formes-prise-de-vue.md](memory/2026-08-22-formes-prise-de-vue.md)
- [ ] **Test Mac LEM** — l'appli démarre-t-elle (macOS ≤ Mojave) ? 600D / 100D vus en USB ?

## Bloqué

_(aucune tâche bloquée)_

## Backlog

- [ ] Caler en LEM la séquence télescope **7 × 2 EV** (forme C, [formes §11](formes-prise-de-vue.md)) ; ne pas porter `chapelet_exposure.py` solaire
- [ ] Essai AEB 100D de nuit + aube simulée (retardateur « C », KI-009)
- [ ] Scripts LEM `scripts/lem/` si le Mac le permet (analogues `basic`/`deluxe`)
- [ ] Analyseur de séquence hors ligne si le format de script LEM le justifie
- [ ] Variantes météo / extinction à basse altitude (~10,5° au MAX à Tournefeuille ; Soleil déjà levé au moonset)
- [ ] Repérage premier plan Ouest–SO : déclenche ou non la forme D (70–200)
- [ ] Confirmer l’horizon réel (clôture fenêtre umbra vers 06:44)

## Terminé

- [x] **Infrastructure Cursor** (2026-08-22) — `AGENTS.md`, rules `.mdc`, mémoire, skill `session-summary`, commande `resume-session`
- [x] **Miroir HTML LEM + build PDF** (2026-08-22) — `scripts/mirror.sh`, `scripts/build-pdf.sh`
- [x] **Simulateur FOV lunaire** (2026-08-22) — noyau SEM transféré, overlay ombre, placeholder Paris — DEC-006
- [x] **Recaler le site Tournefeuille** (2026-08-22) — GPS, contacts UTC, YAML + fiche + simu FOV — DEC-008
- [x] **Dépôt git local + origin** (2026-08-22) — premier commit ; `origin` = github.com/hl-ply-eu/lunar-eclipse-maestro
- [x] **Parc optique** (2026-08-22) — télescope 750 mm EQ + chapelets 15-85 / 60 / 70–200 — DEC-009 ; DEC-007 archivé
- [x] **Formes de prise de vue + HDR 7 × 2 EV** (2026-08-22) — DEC-010, KI-013/014/015 ; pourquoi 11,5 EV DxO n’éliminent pas la rampe ([formes §11](formes-prise-de-vue.md))
