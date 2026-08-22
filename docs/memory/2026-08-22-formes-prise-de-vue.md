# Session 2026-08-22 — Formes de prise de vue + dynamique HDR

Branche : `docs/formes-prise-de-vue` (depuis `chore/cursor-workspace-setup` @ `e7a3c95`).

## Contexte

Étude des formes pour Tournefeuille, 28 août 2026 (parc DEC-009). Pas un plan de
séance : pas de scripts LEM, pas de tables d’expo chiffrées au-delà du protocole
7 × 2 EV.

## Accompli

- Étude [formes-prise-de-vue.md](../formes-prise-de-vue.md) (DEC-010)
- Figure FOV astronomy.tools : [figures/astronomy_tools_fov.png](../figures/astronomy_tools_fov.png)
- Getting Started §5, index `docs/README.md`, `AGENTS.md`, rule `architecture-always.mdc`
- Explication documentée : pourquoi 11,5 EV DxO n’éliminent pas le HDR ; span =
  (n−1)×pas → 7 × 2 EV = **12 EV** ([formes §11](../formes-prise-de-vue.md))

Aucun test pytest, aucun PR.

## Décisions

| ID | Sujet |
|----|-------|
| DEC-010 | Formes : 100D = time-lapse AEB (A) ; 600D = HDR disque 750 mm ±1,4× (C) ; LEM sur le 600D ; forme D = remplacement, pas 3ᵉ corps ; umbra OK au MAX (soleil −11°) |
| — | Split 600D/100D **ergonomique**, pas un écart DxO (65 vs 63, 11,5 vs 11,3 EV) |
| — | Protocole HDR retenu : **7 poses × 2 EV, span 12 EV** aux instants clés |
| — | OM-3 / OM-5 II : pas de DxO officiel ; proxy E-M1 II / PDR ~9,6–9,8 ; **pas un changement pour le 28 août** (perte LEM) |

## Pièges

| ID | Sujet |
|----|-------|
| KI-013 | Ambiance fixe et chapelet rampé s’excluent sur une expo |
| KI-014 | Umbra photographiable au MAX (soleil −11,2°) ; plus après le crépuscule civil (~06:44) |
| KI-015 | Liseré turquoise (Chappuis) = tons *moyens* du HDR, pas les 2 extrêmes |

## Prochaines étapes

1. **Volume de prises (session suivante, autre agent)** — combien de vues pour
   *couvrir* l’éclipse avec les **deux** boîtiers (cadence 100D AEB × durée ;
   stacks 600D aux instants clés + vues entre les stacks). Ne pas refaire le
   raisonnement 7 × 2 EV / 11,5 EV (déjà au §11).
2. Essai AEB 100D nuit + aube simulée (retardateur « C »).
3. Test Mac LEM + USB 600D (KI-006 / KI-007).
4. Caler la séquence 7 × 2 EV dans LEM / calculatrice Jubier (backlog).
5. Repérage premier plan Ouest (forme D) ; horizon réel ~06:44.
