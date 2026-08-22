---
name: session-summary
description: Résumé de fin de session, mise à jour todo.md, decisions.md et known-issues.md
---

Quand l'utilisateur invoque ce skill (ou `/session-summary`) :

1. Crée `docs/memory/<YYYY-MM-DD>-<sujet-kebab>.md` avec :
   - Ce qui a été accompli (fichiers modifiés, tests, PRs)
   - Décisions prises (référencer DEC-NNN ; ajouter dans `docs/decisions.md` si structurantes)
   - Pièges identifiés
   - Prochaines étapes ordonnées

2. Mets à jour `docs/todo.md` :
   - Coche les tâches terminées (section Terminé avec date)
   - Ajoute les nouvelles tâches En cours
   - Déplace vers Bloqué si dépendance externe

3. Si bug ou limitation identifiée : ajoute une entrée KI-NNN dans `docs/known-issues.md`

4. Ne réinvente rien — demande à l'utilisateur si une information manque avant d'écrire.

5. Base-toi uniquement sur ce qui a été fait dans la session courante.
