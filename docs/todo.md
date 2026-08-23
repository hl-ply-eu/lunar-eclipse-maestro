# Tâches — lunar-eclipse-maestro

## En cours

- [ ] **Scénario 150 mm f/5 + 600D** (prochain agent) — optique muette au T-ring ([KI-019](known-issues.md)) : `TAKEPIC` isolé ou rampe au foyer ; log LEM / CR2 / EXIF ouverture ; déclenchement manuel d’abord. Grille [DEC-013](decisions.md) ([formes §11](formes-prise-de-vue.md)).
- [ ] **Rampe LEM serrée** — resserrer sous 3 s (vers pose + 1,1 s) maintenant que le 7/7 à 3 s est validé ; tampon / vidage
- [ ] **Déploiement LEM** — 1.3.3β1 Intel Y + 600D USB OK ; 100D optionnel ([KI-007](known-issues.md))

## Bloqué

_(aucune tâche bloquée)_

## Backlog

- [ ] Script séance LEM (forme C, [formes §11](formes-prise-de-vue.md), [DEC-013](decisions.md)) : rampe **7** courante + **étendue sombre** (9 vues) aux instants clés ; ISO **100 / 200 / 800** ; `say` courts à ~1 s + rappel **taux Lune** ([KI-021](known-issues.md)) ; pas `chapelet_exposure.py` solaire
- [ ] Essai AEB 100D de nuit + aube simulée (retardateur « C », KI-009) — caler t₀ et le plancher 60 vs 90 s
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
- [x] **Copie scripts LEM** (2026-08-23) — `basic.txt` / `deluxe.txt` depuis Pap → [`scripts/lem/`](../scripts/lem/) ; bench 7 × 2 EV dans `essais-2026/` ; KI-018 (exemples totalité, pas séance 2026)
- [x] **Bench rampe 7 × 2 EV espacé 3 s** (2026-08-23) — `IMG_7685`–`7691` 7/7, vitesses exactes, gaps 3,00 s / 4,00 s, fenêtre 23,0 s ; `IMG_7684` = essai collé 1/15 (KI-020) ; LEM Benchmarks 1,1 s/vue
- [x] **Suivi Lune + rampe étendue sombre + ISO 100/200/800** (2026-08-23) — DEC-013, KI-008/021 ; 7 vues partout, 9 vues aux instants clés (cas L=2, tri après) ; `say` courts à 1 s ([formes §11](formes-prise-de-vue.md))
