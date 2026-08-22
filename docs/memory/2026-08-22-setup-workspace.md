# Session 2026-08-22 — Setup workspace Cursor lunar-eclipse-maestro

Branche : `chore/cursor-workspace-setup`.

## Contexte

Initialisation d'un dépôt jumeau de `solar-eclipse-maestro` pour Lunar Eclipse Maestro
et l'éclipse lunaire quasi-totale du 28 août 2026 (France, duo 600D-Tele + 100D-Wide).
Site GPS encore inconnu → placeholder Paris.

## Accompli

- Infrastructure Cursor : `AGENTS.md`, rules `.mdc`, skill `session-summary`, commande `resume-session`
- Mémoire : DEC-001 à DEC-007, KI-001 à KI-010, `docs/todo.md`
- Miroir wget LEM (FR) + `build-pdf.sh` / `build-pdf.py`
- Simulateur FOV lunaire (noyau SEM : DE421, gnomonique, `right = forward × up`) + tests
- Premier run placeholder Paris : validation MAX dAlt −0,33′ vs timeanddate ; trajectoire descendante vers la droite ; auto-top 280 mm à 06:00:10 CEST
- Guides : Getting Started stub, `methode-fov.md`, `chapelet-lecons-sem.md`

## Décisions (dans `docs/decisions.md`)

| ID | Sujet |
|----|-------|
| DEC-001 | Mémoire projet dans `docs/*` |
| DEC-002 | Venv `.venv/` à la racine |
| DEC-003 | Miroir wget depuis `LunarEclipseMaestroHelp.html` |
| DEC-004 | Rules modulaires `.mdc` |
| DEC-005 | Getting Started éclipse 2026 France |
| DEC-006 | Simulateur FOV, cible Lune |
| DEC-007 | Optiques 600D-Tele / 100D-Wide (focale wide à recalculer) |

## Pièges identifiés

- KI-006 : LEM ne tourne pas après Mojave — l'automatisation 600D n'est pas acquise.
- KI-005 : ne pas figer cadrage / focale avant le GPS réel.

## Prochaines étapes

1. Commune / GPS → recaler le YAML et relancer la simu.
2. Test Mac : LEM démarre-t-il ? USB 600D ?
3. Scénarios 600D-Tele et chapelet 100D (MAX en déclenchement manuel dédié).
