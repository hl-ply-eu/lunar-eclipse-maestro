# Tâches — lunar-eclipse-maestro

## En cours

_(préparation logicielle terminée — v1.0 — en attente séance terrain 28 août 2026)_

- [ ] **Séance terrain Tournefeuille** — checklist [`checklist-tournefeuille-2026.html`](checklist-tournefeuille-2026.html) ; script [`seance-2apn-interlace.txt`](../scripts/lem/essais-2026/seance-2apn-interlace.txt) ; boot LEM §2c (KI-025) ; ~04:20→07:20 CEST
- [ ] **Scénario 150 mm f/5 + 600D** — optique muette au T-ring ([KI-019](known-issues.md)) : `TAKEPIC` isolé ou rampe au foyer ; log LEM / CR2 / EXIF ouverture ; déclenchement manuel d’abord. Grille [DEC-013](decisions.md) ([formes §11](formes-prise-de-vue.md)).
- [ ] **Rampe LEM serrée** — resserrer sous 3 s (vers pose + 1,1 s) maintenant que le 7/7 à 3 s est validé ; tampon / vidage — **après** séance ou bench post-terrain

## Bloqué

_(aucune tâche bloquée)_

## Backlog

- [ ] Optionnel : rampe 7/7 sur la **32 Go** (80 Mo/s) pour confirmer le tampon — pas un re-calage des 3 s a priori ([KI-016](known-issues.md))
- [ ] Essai AEB 100D de nuit + aube simulée (retardateur « C », KI-009) — caler t₀, la centrale **4 s · ISO 800** (placeholder DEC-018) et le plancher 60 vs 90 s ; **repli** si LEM ne voit pas le 100D
- [ ] Analyseur de séquence hors ligne si le format de script LEM le justifie
- [ ] Variantes météo / extinction à basse altitude (~10,5° au MAX à Tournefeuille ; Soleil déjà levé au moonset)
- [ ] Repérage premier plan Ouest–SO : déclenche ou non la forme D (70–200)
- [ ] Confirmer l’horizon réel (clôture fenêtre umbra vers 06:44)
- [ ] Re-mesure délai reconnexion 100D (à froid vs chaud)

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
- [x] **Fenêtre 600D pénombre / aube + pause accu** (2026-08-23) — DEC-014, KI-022 ; 04:20 rampe courte, étendues 9, aube 7→5→3, swap 10 min ~05:40 Incremental N ; 32 Go 80 Mo/s vs 16 Go 95 Mo/s sans re-calage ([formes §11–13](formes-prise-de-vue.md))
- [x] **Diagnostics MAX ISO 100 / 1600** (2026-08-24) — DEC-015 ; après l’étendue 9 seulement : rampe 100 (→ 4 s, suivi) puis 1600 (1/4000 → 1 s, figé) ; +14 CR2 ; pas un second HDR
- [x] **Incremental N + écarts Jubier** (2026-08-24) — DEC-016 ; N en tête des étendues et des 3 rampes MAX ; Y ensuite ; ≥ 3 s / tampon 5
- [x] **Script séance LEM** (2026-08-24) — [`seance-600d-t150.txt`](../scripts/lem/essais-2026/seance-600d-t150.txt) ; générateur `scripts/generate_lem_seance.py` ; 5 vues pénombre ; 9 étendue à U1+10 / 50 % / MAX / 06:30 ; diagnostics MAX ; cadence 2 min ; Av 5,6 / f/5
- [x] **Cadrage 100D 24 mm / composition tiers** (2026-08-25) — DEC-017 ; horizon au tiers bas, MAX au ciel ; lock **04:52:44** bord haut 20 % gauche ; schéma `docs/figures/fov-100d-24mm-tiers.png`
- [x] **100D sous LEM — plan** (2026-08-25) — DEC-018, KI-023 ; nom `100D-W24` ; test 2 APN simple d’abord ; grille aube 3→5 (4 s · ISO 800 non mesurée) ; allumage tardif FAQ + Incremental N ; script aube **après** le test
- [x] **Test 2 APN + entrelacé** (2026-08-26) — JPG-F ; seq OK ; interlace 33/33 CR2 + 69/72 JPG ; boot sans scénario ; reconnexion ~30 s (KI-025) ; [REX](memory/2026-08-26-rex-bench-2apn-interlace.md)
- [x] **Scripts séance 100D + dual** (2026-08-28) — [`seance-100d-w24.txt`](../scripts/lem/essais-2026/seance-100d-w24.txt) 3→5 JPG-F ; [`seance-2apn-interlace.txt`](../scripts/lem/essais-2026/seance-2apn-interlace.txt) (600D prioritaire, gap 2 s, DEC-019) ; marge allumage 60 s ; `say` sparses (KI-021)
- [x] **Checklist terrain HTML** (2026-08-28) — [`checklist-tournefeuille-2026.html`](checklist-tournefeuille-2026.html) (modèle Frías) : boot LEM (vider → quitter → APN 15–20 s → relancer → 10 s → reset 20 s), horloge CEST, compte à rebours, mode nuit
- [x] **Revue scripts Opus 4.8** (2026-08-28) — validation 600D / 100D / entrelacé (DEC-019, KI-020/021/025) ; 45 pytest ; tag v1.0
