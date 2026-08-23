# Session 2026-08-23 (soir) — LEM 1.3.3β1, bench rampe, DEC-013

Branche : `docs/formes-prise-de-vue` (depuis `d1abbc7`). Suite de
[duree-rampe-600d.md](2026-08-23-duree-rampe-600d.md).

## Contexte

Reprise : choisir la version LEM pour le MacBook Pro 2012 (Mojave 10.14.6),
copier les scripts Pap, chronométrer une rampe 7 × 2 EV, puis figer la grille
d’expo (suivi Lune, étendue sombre, ISO mixte).

## Accompli

- **LEM 1.3.3β1 Intel Y** (16 janv. 2019) installée et lancée sur Mojave.
  Lieu Tournefeuille **UTC+2** (CEST). Nom APN **`600D-T150`**. 600D vu en USB.
  Pas de DEC-NNN pour le numéro de version (retenu en séance, pas numéroté).
- Copie Pap → [`scripts/lem/`](../../scripts/lem/) (`basic.txt`, `deluxe.txt`,
  sans AppleDouble) + bench
  [`essais-2026/bench-rampe-7x2ev.txt`](../../scripts/lem/essais-2026/bench-rampe-7x2ev.txt).
- Bench 15-85 @ f/5,6, ISO 100, RAW, espacement 3 s : **7/7**
  (`IMG_7685`–`7691`), vitesses exactes, fenêtre **23,0 s**. Premier essai
  collé MAX+0 = 1 CR2 à 1/15 (`IMG_7684`). LEM Benchmarks **1,1 s/vue**.
- Grille séance (étude, pas encore script jour J) dans
  [formes §11](../formes-prise-de-vue.md) : rampe 7 courante / 9 vues étendue
  sombre ; ISO 100 / 200 / 800 ; `say` courts à ~1 s.

Aucun pytest. Push demandé en clôture.

## Décisions

| ID | Sujet |
|----|-------|
| *(sans n°)* | LEM **1.3.3β1 Intel Y** sur Mojave ; pas 1.3.2, pas Universal Binary ; fuseau LEM **+2** |
| DEC-011 (complément) | Bench 3 s → **23 s** ; cycle USB 1,1 s → rampe serrée ~13–16 s |
| **DEC-013** | Taux **Lune** ; rampe 7 partout ; étendue **sombre** (9 vues) aux instants clés, tri **après** (carte dans le boîtier) ; ISO **100 / 200 / 800** ; `COMMAND ;say` courts à ~1 s |

## Pièges

| ID | Sujet |
|----|-------|
| KI-018 | `basic` / `deluxe` = totalité 2010, pas la séance 2026 |
| KI-019 | Télescope / T-ring muet : LEM envoie quand même une ouverture |
| KI-020 | Plusieurs `TAKEPIC` au même horodatage → LEM n’en exécute qu’un |
| KI-021 | `say` long = muet (leçon SEM) ; plusieurs phrases courtes à ~1 s |
| KI-008 (étendu) | Viseur polaire OK en 0,5–2 s avec taux Lune ; filé dominant = sidéral vs Lune |

## Prochaines étapes

1. **Scénario télescope 150 mm f/5 + 600D** (agent suivant) — optique muette
   (KI-019) : `TAKEPIC` isolé ou rampe au foyer ; log LEM, 7 CR2, EXIF
   ouverture ; confirmer le déclenchement manuel au T-ring. Brancher la grille
   DEC-013 (pas encore le script séance complet).
2. Optionnel : resserrer l’espacement sous 3 s (pose + 1,1 s) ; tampon / vidage.
3. Script séance LEM (backlog) : 7 / 9 vues, `say` taux Lune, instants clés.
4. 100D USB optionnel ; essai AEB nuit+aube ; horizon ~06:44 ; forme D.
