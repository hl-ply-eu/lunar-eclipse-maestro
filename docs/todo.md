# Tâches — lunar-eclipse-maestro

## En cours

- [ ] **Déploiement LEM sur le Mac** — install + prise en main (macOS ≤ Mojave, [KI-006](known-issues.md)) ; 600D / 100D vus en USB ([KI-007](known-issues.md))
- [ ] **Scénario de benchmark LEM** — rampe 7 × 2 EV sur 600D ; chronométrer la durée réelle (estimation [formes §13](formes-prise-de-vue.md) : ~20–25 s) ; tampon RAW / vidage (analogue SEM B1–B5)

## Bloqué

_(aucune tâche bloquée)_

## Backlog

- [ ] Caler en LEM la séquence télescope **7 × 2 EV** (forme C, [formes §11](formes-prise-de-vue.md)) ; ISO mixte 100–200 (U1, vues courtes) / 400–800 (umbra) ; ne pas porter `chapelet_exposure.py` solaire
- [ ] Essai AEB 100D de nuit + aube simulée (retardateur « C », KI-009) — caler t₀ et le plancher 60 vs 90 s
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
- [x] **Volume de prises (2 boîtiers)** (2026-08-22) — DEC-011, KI-016 ; 100D JPEG Fine 90 s (~720 fich., ~10 s de film à 12 fps) ; 600D RAW ~70–90 CR2 ; cartes 16 Go / 2 accus ([formes §13](formes-prise-de-vue.md))
- [x] **Durée rampe 600D + capacité 16 / 32 Go** (2026-08-23) — une rampe 7 × 2 EV ~20–25 s sous LEM ; 16 Go ≈ 65 rampes avec marge ; 32 Go si densification ; 4 stacks = produit, pas limite carte ([formes §13](formes-prise-de-vue.md), DEC-011)
- [x] **ISO 800 vs brackets** (2026-08-22) — DEC-012, KI-017 ; Sports/ISO-less ≠ moins de vues ; 1/4000 trop lent à U1 · f/5 ; 800 décale les temps (4 s → 0,5 s) et aide le cycle AEB 100D ([formes §11](formes-prise-de-vue.md))
