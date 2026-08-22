# Session 2026-08-22 — Volume de prises + ISO 800

Branche : `docs/formes-prise-de-vue` (depuis `7df1e48`).

## Contexte

Suite de [formes-prise-de-vue.md](2026-08-22-formes-prise-de-vue.md). Ne pas
refaire le §11 (span / DxO). Matériel annoncé en séance : cartes **16 Go**,
**2 batteries par boîtier**. Question ISO 800 (DxO Sports vs brackets).

## Accompli

- [formes-prise-de-vue.md](../formes-prise-de-vue.md) §13 (volume) + sous-section
  ISO 800 dans le §11 ; §12 ouvert → §14
- Getting Started §5, `docs/README.md`, rule `architecture-always.mdc`

Aucun test pytest, aucun PR (push de la branche d’étude).

## Décisions

| ID | Sujet |
|----|-------|
| DEC-011 | 100D JPEG Fine + AEB, défaut **90 s** (pas = intervallomètre, pas durée de film → ~10 s à 12 fps) ; 600D RAW ~70–90 CR2 ; viser ~10–20 s de clip |
| DEC-012 | ISO Sports ~800 = plafond, pas sweet spot ; 800 décale la rampe (4 s → 0,5 s), **ne coupe pas** le 7 × 2 EV ; 1/4000 trop lent à U1 · f/5 ; 100D : 800 aide le cycle AEB |

## Pièges

| ID | Sujet |
|----|-------|
| KI-016 | 16 Go : le RAW AEB 100D sur 3 h à 60–90 s déborde (~620 CR2 / carte) ; 2× LP-E12 CIPA tiennent 90 s, pas 60 s sans swap (réarmer l’AEB, KI-009) |
| KI-017 | Confondre Sports / ISO-less DSO avec « moins de brackets HDR » |

## Prochaines étapes

1. **Test Mac LEM** + USB 600D (En cours, KI-006 / KI-007).
2. Essai AEB 100D nuit + aube : caler t₀ et le plancher 60 vs 90 s (ISO 800
   raccourcit surtout la vue +2 EV).
3. Calculatrice LEM / Jubier : 7 × 2 EV, ISO mixte 100–200 (vues courtes, U1) /
   400–800 (umbra).
4. Repérage premier plan Ouest (forme D) ; horizon réel ~06:44.
