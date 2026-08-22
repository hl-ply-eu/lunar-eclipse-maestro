# Problèmes connus — lunar-eclipse-maestro

Format KI-NNN. Bugs et pièges pour éviter les fausses pistes en session agent.

---

## KI-001 : LEM est macOS uniquement

**Statut :** Contrainte applicative externe.
**Symptôme :** ce dépôt tourne sous Linux (miroir, PDF, simulateur) ; Lunar Eclipse Maestro ne s'exécute pas sur Linux.
**Action :** ne pas proposer de lancer LEM localement ; les guides supposent un Mac séparé. Voir aussi **KI-006** (plafond Mojave).

---

## KI-002 : Miroir HTML tierce — ne pas refactorer

**Statut :** Contrainte copyright et architecture (DEC-003).
**Symptôme :** pages HTML sous `mirror/xjubier.free.fr/` ; contenu © Xavier Jubier.
**Action :** ne pas réécrire, reformater ou « améliorer » le HTML miroir ; rafraîchir via `./scripts/mirror.sh` uniquement.

---

## KI-003 : Point d'entrée wget — 403 possible sur la racine

**Statut :** Leçon SEM, appliquée ici.
**Symptôme :** wget sur le répertoire racine de l'aide peut échouer (403 Forbidden).
**Action :** toujours utiliser l'URL `.../LunarEclipseMaestroHelp.html` comme entrée ; ne pas modifier `mirror.sh` pour pointer ailleurs sans tester.

---

## KI-004 : Index Cursor — miroir et output exclus

**Statut :** Configuration `.cursorignore`.
**Symptôme :** le HTML miroir et les PDF/PNG générés polluent l'index sémantique si non exclus.
**Action :** s'appuyer sur `docs/`, `scripts/` et `AGENTS.md` ; le miroir reste accessible via `@Files` ciblé.

---

## KI-005 : Site d'observation — Paris archivé, Tournefeuille actif

**Statut :** Recalé (DEC-008, 2026-08-22). L’ancien YAML `paris-600d-placeholder.yaml` reste comme archive.
**Symptôme (historique) :** Paris (48,8566° N, 2,3522° E) jusqu’au GPS réel.
**Site actuel :** Tournefeuille, 43,582389° N, 1,350944° E — [tournefeuille-2026.md](lieux/tournefeuille-2026.md). MAX ~10,5° / 06:12:55 CEST ; moonset 07:20:26 CEST ; U4 sous l’horizon.
**Reste ouvert :** élévation 155 m approx. ; horizon local ouest–SO non levé ; **optiques à repréciser** (28 mm ne tient pas U1→moonset).

---

## KI-011 : Miroir wget — pages d'aide LEM cassées (404)

**Statut :** Constaté au premier `mirror.sh` (2026-08-22).
**Symptôme :** wget code 8 ; au moins `pgs/c1sem72.html` est lié depuis l'aide mais absent du serveur. Les ~65 pages principales (dont `btoc1.html`) sont bien là.
**Action :** `mirror.sh` tolère le code wget 8 et écrit quand même `MANIFEST.txt`. Ne pas « réparer » les liens dans le HTML miroir (KI-002).

---

## KI-006 : LEM incompatible macOS Catalina et suivants

**Statut :** Documenté par Xavier Jubier (page produit LEM 1.3.x).
**Symptôme :** « Lunar Eclipse Maestro will not be compatible with macOS Catalina […] or Big Sur and newer (a complete rewrite would be necessary). » Repli annoncé : VM Mojave (Parallels / VMware / VirtualBox).
**Conséquence :** le Mac qui a fait tourner Solar Eclipse Maestro le 12 août 2026 peut être trop récent. Le duo « 600D automatisé par LEM + 100D autonome » n'est **pas** acquis.
**Action :** tester LEM sur le Mac **avant** d'écrire des scripts. Si LEM ne démarre pas : intervallomètre / déclenchement manuel sur le 600D (comme le 100D solaire). Ne pas promettre l'automatisation USB tant que le test n'est pas fait.

---

## KI-007 : Support 600D / 100D dans LEM non vérifié

**Statut :** À confirmer au premier test Mac.
**Symptôme :** la page de téléchargement LEM 1.3.3β1 cite une plage Canon (« 1D Mark III up to 6D Mark II and 200D ») qui n'est pas un inventaire exhaustif. SEM a piloté le 600D ; LEM est plus ancien.
**Action :** au test USB, vérifier que le 600D (et éventuellement le 100D) apparaissent dans Configuration matérielle. Ne pas copier un script SEM en changeant seulement le nom d'appli.

---

## KI-008 : Trépied fixe — filé sur les poses umbra

**Statut :** Conséquence géométrique (même dérive sidérale que SEM DEC-011).
**Symptôme :** à 280 mm APS-C, ~4,5 px/s (≈ 14″/s). Une pose umbra de 1–4 s produit 5–18 px de filé. SEM limitait la totalité solaire à 1 s ; l'umbra lunaire est beaucoup plus sombre.
**Action :** documenter le plafond de pose vs SNR dans le scénario 600D. Une monture suivie n'est pas dans le matériel Frías ; ne pas la supposer.

---

## KI-009 : 100D + intervallomètre — leçons SEM (AEB)

**Statut :** Transféré de SEM KI-014 ; toujours valable sur le même boîtier.
**Pièges :**
- Pas d'intervallomètre intégré (jack 2,5 mm RS-60E3).
- AEB + intervallomètre : seul le **retardateur continu « C »** enchaîne le bracket (rafale KO, retardateur 2 s KO). Minimum **C = 2 → 6 vues**.
- L'**AEB s'efface à chaque extinction** (panne silencieuse) et au passage vidéo ; le retardateur « C » survit.
- AEB disponible en mode **M** (c'est la correction d'exposition qui ne l'est pas).
**Action :** armer l'AEB en dernier, ne plus éteindre, contrôler les trois repères. Détail : [chapelet-lecons-sem.md](chapelet-lecons-sem.md).

---

## KI-010 : Ne jamais faire dépendre le MAX d'une coïncidence d'horaire

**Statut :** Transféré de SEM KI-018 (totalité solaire tombée dans un trou de 239 s).
**Symptôme :** un intervallomètre calé « pile » sur un contact échoue dès que le run part en retard.
**Action :** prévoir un **déclenchement manuel dédié au maximum** (et autour de U1 si besoin). Noter l'heure de départ réelle. L'intervalle du chapelet ne doit pas être le seul filet pour l'instant critique.
