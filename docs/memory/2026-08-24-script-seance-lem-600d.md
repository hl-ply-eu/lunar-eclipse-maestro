# Session 2026-08-24 (nuit) — script séance LEM 600D

Branche : `docs/formes-prise-de-vue` (depuis `26d7ad0`). Suite de
[fenetre-600d-dec014-016.md](2026-08-24-fenetre-600d-dec014-016.md).

## Contexte

Reprise : écrire le script LEM 600D au foyer 150 mm conformément à
DEC-013–016. Observateur : pénombre **5 vues** ; étendue **06:30** = 4ᵉ HDR
umbra (pas le bloc MAX) ; colonne Av **5,6** (USB) / grille **f/5** ; cadence
**2 min ancrée sur MAX**.

## Accompli

- Générateur [`scripts/generate_lem_seance.py`](../../scripts/generate_lem_seance.py)
  et script [`seance-600d-t150.txt`](../../scripts/lem/essais-2026/seance-600d-t150.txt)
  (~519 `TAKEPIC`, 04:20:55 → 07:18:55).
- Pénombre 5 ; courante 7 / 2 min sur MAX ; étendue 9 à U1+10, ~50 %, MAX,
  06:30 ; bloc MAX + ISO 100 / 1600 ; saut MAX+2 min ; trou accu 05:40–05:55 ;
  reprise 05:56:55 Incremental N ; aube 5 dès 06:44, 3 dès 07:00.
- Tests [`tests/test_generate_lem_seance.py`](../../tests/test_generate_lem_seance.py)
  : 12 cas + FOV = 24 pytest OK.
- DEC-014 précisé (points 1–2, 6–7). README LEM / essais-2026 / tests.md /
  todo.md.

Push demandé en clôture.

## Décisions

| ID | Sujet |
|----|-------|
| **DEC-014** (complément) | Pénombre **5** vues ; étendue **06:30** = 4ᵉ HDR umbra, distincte du bloc MAX ; cadence **2 min** sur MAX ; Av script **5,6** / expo **f/5** |

Pas de nouveau DEC. DEC-015 / DEC-016 inchangés, maintenant dans le `.txt`.

## Pièges

Aucun KI nouveau. KI-019 (optique muette au foyer) reste le prochain essai
terrain. KI-021 (`say` long muet) appliqué (COMMAND courts ASCII).

## Prochaines étapes

1. **Scénario 150 mm f/5 + 600D** — `TAKEPIC` isolé / rampe au T-ring (KI-019).
2. Copier `seance-600d-t150.txt` sur le Mac (`600D-T150`) et valider un
   fragment en temps simulé.
3. Optionnel : rampe serrée &lt; 3 s ; 7/7 sur 32 Go ; AEB 100D ; horizon ~06:44.
