# Décisions techniques — lunar-eclipse-maestro

Format DEC-NNN. Décisions actives uniquement ; archiver ou supprimer quand obsolètes.

---

## DEC-001 : Mémoire projet dans `docs/*` (2026-08-22)

**Contexte :** même modèle que `solar-eclipse-maestro` / `fits-browser`.
**Décision :** Mémoire versionnée dans `docs/` (`decisions.md`, `todo.md`, `known-issues.md`, `memory/`) ; index dans `AGENTS.md` ; ouverture via `@Files` ou `/resume-session` ; clôture via `/session-summary`.
**Justification :** Persistance hors historique chat ; cohérence entre dépôts Astro.
**Rejeté :** Memory Bank `.cursor/memory/` — `docs/memory/` retenu pour lisibilité Git.

---

## DEC-002 : Environnement virtuel `.venv/` à la racine (2026-08-22)

**Contexte :** `scripts/build-pdf.sh` et `simulate_fov.py` partagent un seul Python.
**Décision :** Venv standard à `${workspaceFolder}/.venv` ; exécution agent via `.venv/bin/python` ; dépendances figées dans `requirements.txt`.
**Justification :** Alignement avec SEM ; un venv pour PDF + Skyfield.
**Rejeté :** venv séparé par outil.

---

## DEC-003 : Miroir wget depuis `LunarEclipseMaestroHelp.html` (2026-08-22)

**Contexte :** l'aide LEM est hébergée sur xjubier.free.fr ; la racine d'un répertoire d'aide peut renvoyer 403 (leçon SEM KI-003).
**Décision :** `scripts/mirror.sh` télécharge via wget depuis l'URL d'entrée **francophone** `LunarEclipseMaestroHelp.html` (pas le chemin `/en/`) ; structure sous `mirror/xjubier.free.fr/...` ; `mirror/index.html` redirige vers `pgs2/btoc1.html`.
**Justification :** Reproductibilité hors ligne ; même recette que SEM.
**Rejeté :** Miroir de la version anglaise uniquement — LEM est localisé FR/EN, le projet travaille en français.

---

## DEC-004 : Rules modulaires `.cursor/rules/*.mdc` (2026-08-22)

**Contexte :** dépréciation du fichier monolithique `.cursorrules`.
**Décision :** Rules modulaires : `architecture-always.mdc` (always), `project-conventions.mdc`, `python-style.mdc` (globs `**/*.py`) ; skill `session-summary` ; commande `resume-session`.
**Justification :** Calqué sur SEM / fits-browser.
**Rejeté :** Fichier `.cursorrules` unique.

---

## DEC-005 : Guide Getting Started centré éclipse 2026 France (2026-08-22)

**Contexte :** éclipse lunaire quasi-totale du 28 août 2026 (magnitude umbrale 0,93).
**Décision :** Document unique `docs/getting-started-2026-france.md` comme guide agent et utilisateur ; liens vers le miroir HTML pour le détail officiel LEM ; pas de duplication de l'aide Jubier.
**Justification :** Workflow chronologique ; le miroir reste la référence exhaustive.
**Rejeté :** Fork complet de l'aide LEM en markdown.

---

## DEC-006 : Simulateur FOV — noyau SEM transféré, cible Lune (2026-08-22)

**Contexte :** méthodes validées dans `solar-eclipse-maestro` (DEC-008/009/010 SEM) : Skyfield + DE421, projection gnomonique, base caméra `right = forward × up`.
**Décision :** copier le noyau géométrique dans `scripts/simulate_fov.py` de *ce* dépôt (pas d'import inter-repos) ; pointer la **Lune** ; contacts `p1` / `u1` / `max` / `u4` / `p4` / `set` ; overlay disque lunaire + ombres umbrale/pénombrale (cône géométrique, élargissement Danjon 2 %) ; auto-top sur le limbe lunaire ; fenêtre longue P1→moonset. Site : [DEC-008](#dec-008--site-tournefeuille--28-août-2026-2026-08-22) (Tournefeuille). Détail : [methode-fov.md](methode-fov.md).
**Justification :** géométrie déjà corrigée (inversion gauche/droite) et testée ; l'éclipse lunaire est le même problème de cadrage trépied fixe, objet bas puis coucher.
**Rejeté :** interpoler uniquement les points Jubier ; pointer le Soleil (cible solaire SEM) ; importer le pipeline HDR couronne.

---

## DEC-007 : Optiques par défaut 600D-Tele / 100D-Wide (2026-08-22)

**Contexte :** duo confirmé par l'utilisateur, identique à Frías (SEM DEC-007) tant que le matériel n'a pas changé.
**Décision :** **600D-Tele** : Canon 70–200 mm f/4 + extender ×1,4 (**280 mm** @ f/5,6) ; **100D-Wide** : EF-S 15-85 mm, focale de chapelet à recalculer pour U1→moonset (28 mm n'est qu'un point de départ solaire). Capteur APS-C identique 22,3 × 14,9 mm / 5184 × 3456.
**Justification :** pas de re-mesure FOV en degrés ; la focale wide dépend du trajet lunaire local (moonset).
**Rejeté :** figer 28 mm avant d'avoir le site réel.

**Statut :** remplacé par [DEC-009](#dec-009--parc-optique-tournefeuille-2026-08-22) (télescope 750 mm + parc chapelet). Le couple 280 mm / 15-85 n’est plus le défaut.

---

## DEC-008 : Site Tournefeuille, 28 août 2026 (2026-08-22)

**Contexte :** KI-005 (placeholder Paris) ; commune et GPS fournis par l’observateur.
**Décision :** site unique **Tournefeuille** (43°34′56.6″ N, 1°21′03.4″ E ; 43,582389° N, 1,350944° E). YAML [`scripts/config/tournefeuille-600d.yaml`](../scripts/config/tournefeuille-600d.yaml) ; fiche [lieux/tournefeuille-2026.md](lieux/tournefeuille-2026.md). Contacts locaux = UTC observateur + 2 h (CEST), y compris moonset 05:20:26 UTC. Élévation YAML 155 m (approx.).
**Justification :** GPS réel ; moonset Skyfield DE421 = −0,05° à l’heure fournie ; U4/P4 sous l’horizon.
**Rejeté :** rester sur Paris ; interpoler un moonset générique « France ».

---

## DEC-009 : Parc optique Tournefeuille (2026-08-22)

**Contexte :** DEC-007 calquait Frías (600D @ 280 mm trépied fixe + 100D @ 15-85). Le matériel réel pour le 28 août est plus large, et une monture **équatoriale** est disponible.
**Décision :** inventorier sans figer encore les scénarios (étude des formes de prise de vue = branche suivante).

**Gros plan (600D) — suivi**

| Optique | Focale | Ouverture | Monture | Notes |
|---------|--------|-----------|---------|-------|
| Télescope 150 mm | **750 mm** | f/5 | Équatoriale | Corps de séance principal 600D |
| + Canon Extender EF 1.4× II | 1050 mm | f/7,1 | idem | Option ; qualité Canon |
| + doubleur Hoya (Zuiko / Olympus) | 1500 mm | f/10 | idem | Option ; probablement moins qualitatif, bons résultats passés |

**Chapelet — l’un des deux boîtiers (600D ou 100D), trépied fixe**

| Optique | Plage | Ouverture | Notes |
|---------|-------|-----------|-------|
| Canon EF-S 15-85 mm f/3,5–5,6 IS USM | 15–85 mm | un peu basse en bout de plage | Souplesse ; U1→moonset tient vers 18–25 mm (voir fiche lieu) |
| Canon EF-S 60 mm f/2,8 USM Macro | 60 mm | f/2,8 | Très qualitatif ; trop long pour U1→moonset en un cadrage (~40°) |
| Canon EF 70–200 mm f/4 L USM | 70–200 mm | f/4 | Très qualitatif ; chapelet serré / recentrages, pas le trajet complet |

**Justification :** le 750 mm suivi change le problème (plus de trajectoire capteur, KI-008 ne s’applique pas à ce corps) ; le 70–200 redevient une option **chapelet**, plus le télé 600D par défaut.
**Rejeté :** garder 280 mm + ×1,4 comme unique gros plan ; figer 28 mm sur le 15-85 ; étudier les formes de prise de vue dans cette branche.

---

## DEC-010 : Formes de prise de vue — hypothèses de travail (2026-08-22)

**Contexte :** idées observateur (ambiance time-lapse, chapelet LEM, départ U1, HDR « vision humaine ») + parc DEC-009 + référence Cannat 21 janv. 2019 (lunette motorisée + 20 mm ambiance). Détail : [formes-prise-de-vue.md](formes-prise-de-vue.md).
**Décision (étude, pas encore plan de séance) :**

1. **100D = forme A** : time-lapse **AEB** (leçon Frías), **peu avant U1 → moonset**. L’AEB absorbe nuit → aube et offre le choix des vues ; ce n’est pas le HDR du disque.
2. **600D = forme C** : télescope **750 mm** (cadrage confortable, dérive tolérée). **1,4× à tenter** (encore de la marge). Doubleur Hoya : très serré (~2 min à 1′/min) — seulement si la mise en station le permet.
3. **LEM en priorité sur le 600D**. 100D autonome (intervallomètre + « C »).
4. **Forme D (70–200 ± 1,4×)** : *remplace* A ou C si un premier plan Ouest le justifie — pas un troisième corps.
5. **Umbra vs aube** : au MAX le Soleil est à **−11°** (crépuscule nautique, azimut opposé). Poses umbra réalistes jusqu’au crépuscule civil (~06:44). Ensuite le fond de ciel noie les poses longues. Détail : [formes-prise-de-vue.md](formes-prise-de-vue.md) §8.

**Justification :** hypothèses observateur du 22 août au soir ; géométrie Skyfield Tournefeuille (soleil −11,2° au MAX, lever 07:15, moonset 07:20). Capteurs 600D / 100D **équivalents** en RAW DxO (65 vs 63, DR 11,5 vs 11,3 EV) : le split est ergonomique, pas un écart de silicium. Voir [formes-prise-de-vue.md](formes-prise-de-vue.md) §9. Les 11,5 EV labo **ne remplacent pas** le HDR disque : SNR DxO ≠ dynamique propre, croissant qui clippe, fenêtre glissante ; protocole **7 × 2 EV → span 12 EV** *(n−1)×pas*. Détail : [formes-prise-de-vue.md](formes-prise-de-vue.md) §11.
**Rejeté :** expo unique sans AEB sur le 100D (l’aube casse le run) ; doubleur comme plan A ; P1 dans le plan privilégié ; LEM sur le 100D comme plan A *pour un HDR disque* ; choisir le boîtier au foyer « parce qu’il est meilleur au DxO » ; une seule RAW « parce que 11,5 EV ».

**Complément 2026-08-25 :** LEM sur le 100D n’est plus rejeté pour *suivre l’aube* (centrale qui recule, 3 puis 5 vues) — [DEC-018](#dec-018--100d-sous-lem--test-2-apn-puis-aube-2026-08-25), conditionné au test USB. Ce n’est pas un second 7 × 2 EV. Tant que ce test n’est pas OK, le 100D reste autonome (AEB).

**Note OM System (2026-08-22) :** OM-3 / OM-5 II **sans test DxO publié**. Proxy labo = E-M1 II (80 / 12,8 EV / ISO 1312) ; PDR PhotonsToPhotos OM-3 9,64 / OM-5 II 9,79. Gain RAW ~+1 EV vs Rebel, poids surtout sur les zooms, **perte LEM**. Pas un changement *pour* le 28 août. Détail : [formes-prise-de-vue.md](formes-prise-de-vue.md) §10.

---

## DEC-011 : Volume de prises — JPEG 100D, RAW 600D, pas 60–90 s (2026-08-22)

**Contexte :** cartes **16 Go** (filet / 100D) et une **32 Go** (séance 600D, DEC-014), **2 batteries par boîtier** ; produit 100D = time-lapse d’ambiance (forme A), 600D = HDR disque (forme C). Détail : [formes-prise-de-vue.md](formes-prise-de-vue.md) §13. Compléments 600D (durée de rampe, fenêtre, accu) le **2026-08-23**.
**Décision (étude, pas encore calage terrain) :**

1. **Intervalle 60–90 s** = pas de l’intervallomètre 100D, **pas** la durée du film. 3 h à 90 s → ~120 images/couche → **~5 s** à 25 fps / **~10 s** à 12 fps. Un film cible de 60–90 s exigerait un pas de 5–7 s, incompatible avec AEB « C » = 2.
2. **100D en JPEG Fine + AEB** (« C » = 2 → 6 JPEG / impulsion). Défaut **90 s** (~720 fichiers, ~5 Go, 2× LP-E12 sans swap). **60 s** seulement si l’essai AEB montre une centrale assez courte *et* avec changement d’accu (réarmer l’AEB, KI-009).
3. **600D en RAW.** Une rampe 7 × 2 EV : obturation 5,3 s (ISO 100) ; LEM Benchmarks **1,1 s/vue** pose courte (2026-08-23) → rampe serrée **~13–16 s** ; script bench à 3 s entre départs **~23 s**. Manuel ~10–15 s. Une **16 Go** tient **~65 rampes** avec 20–25 % de marge (~620 CR2 plein ; ne pas remplir). **Complément 2026-08-23 (DEC-014) :** la fenêtre ~04:20 → moonset (~07:20) à ~2 min dépasse ce plafond → carte de séance **32 Go**. Les 16 Go restent le filet / le 100D. Les 4 stacks nommés (U1+10, ~50 %, MAX, 06:30) restent un choix de *produit*. **Swap LP-E8 planifié** (pause 10 min), plus « 2× sans enjeu sur un seul accu ».
4. Viser **~10–20 s de film** d’ambiance, pas une minute.

**Justification :** une 16 Go tient ~620 CR2 vs ~2 470 JPEG Fine ; 3 h d’AEB RAW à 60–90 s déborde (KI-016). Le JPEG 18 Mpx reste au-dessus d’une Full HD ; l’AEB ±2 EV est le filet aube. Deux accus CIPA (380 × 2) couvrent 720 déclenchements (90 s), pas 1 080 (60 s). Sur le 600D, LEM Benchmarks donne **1,1 s/vue** (pose courte) ; le temps de séance (126 min) n’est pas le goulot — la carte 16 Go l’est dès ~84 rampes (pas 90 s). SEM : forfait analyseur **0,6 s** hors obturation (`DEFAULT_LAG_S`), pas un chrono 0,8 s dans le dépôt.
**Rejeté :** RAW+JPEG sur le 100D ; RAW 100D à cadence time-lapse ; chasing un film de 60 s avec AEB nuit ; stacks 600D toutes les 30 s.

---

## DEC-012 : ISO 800 ne réduit pas le 7 × 2 EV (2026-08-22)

**Contexte :** lecture possible de l’ISO DxO *Sports* (~793 / 843) comme « sensibilité optimale » des deux Rebel, d’où l’idée qu’un run à 800 ISO raccourcirait les brackets (sauf si 1/4000 s est trop lent pour la partie claire). Détail : [formes-prise-de-vue.md](formes-prise-de-vue.md) §11.
**Décision (étude) :**

1. **Sports ~800** = plafond SNR 30 dB, pas l’ISO de max DR. La DR *Landscape* est au plus bas ISO ; elle est plate 100–400 puis **descend** à 800.
2. Le « best ISO » ciel profond (zone ISO-less) est **800 sur le 600D**, **400 sur le 100D** — pour une pose longue de champ faible, pas pour un HDR de disque.
3. ISO 800 **décale** la rampe de +3 EV (4 s → 0,5 s) ; le contraste croissant/umbra reste 8–12 EV → on **garde 7 × 2 EV**. LEM peut mixer ISO et vitesse ; on ne verrouille pas tout à 800 pour couper des vues.
4. **1/4000 s** : trop lent pour le limbe encore plein à ISO 800 · f/5 (~1,3 IL de trop) → ISO **100–200** sur les vues courtes à **U1**. Au **MAX** (+4–5 EV vs pleine Lune) 1/4000 suffit ; ISO 400–800 tenable sur l’umbra.
5. 100D AEB : ISO 800 aide le **plancher d’intervalle** (vue +2 EV plus courte), pas les 6 JPEG / impulsion.

**Complément 2026-08-23 (DEC-013) :** 800 n’est **pas** une cible *de toute la rampe*. Les vues 1–5 restent 100/200 (limbe U1). Les **poses longues** (6–7 et étendue) sont à **ISO 800** : pas de grosse perte RAW 400→800 sur le 600D (~0,5 EV de span DxO après le plateau 100–400 ; 800 = seuil ISO-less). On ne choisit pas 400 vs 800 le soir.

**Justification :** le span HDR est une propriété de la *scène* (Jubier / Espenak), pas du gain analogique. Les deux Rebel plafonnent à 1/4000 s.
**Rejeté :** « ISO optimal 800 ⇒ moins de brackets » ; ISO 800 dès U1 sur les vues courtes du 750 mm.

---

## DEC-013 : Suivi Lune, rampe 7 / étendue sombre, ISO 100 / 200 / 800 (2026-08-23)

**Contexte :** mise en station au **viseur polaire** (pas d’astrométrie) ; rampe 7 × 2 EV validée en 23 s (DEC-011) ; carte SD **dans le boîtier** pendant toute la séance (pas de tri sur le vif) ; leçon SEM KI-013 (`say` muet si le message est trop long). Détail : [formes-prise-de-vue.md](formes-prise-de-vue.md) §11, [KI-008](known-issues.md), [KI-021](known-issues.md).
**Décision (étude, à brancher dans le script séance) :**

1. **Taux Lune** sur la monture, pas sidéral. Rappel oral dans le script LEM (avant **04:20**, et avant la première rampe étendue).
2. **Rampe courante = 7 vues.** Aux **instants clés** (U1+10, ~50 %, MAX, éventuellement 06:30) : rampe **étendue d’éclipse sombre** — **deux vues de plus** (pas de 2 EV, ISO 800). Pas de choix L=3 / L=2 sur le vif : on programme le cas sombre, on jette après si l’umbra était claire.
3. Grille ISO : **100** (vues 1–2), **200** (vues 3–5), **800** (vues 6–7 et les deux d’étendue). Pas 400 sur les poses longues. 800 n’est pas un ISO unique pour toute la rampe (DEC-012, limbe U1).
4. Annonces vocales : **plusieurs `COMMAND ;say` courts**, **espacés d’~1 s**, ASCII, ≲ 60 caractères — **pas** un paragraphe unique (SEM : un message long invalidait `say`).

**Justification :** on ne peut pas lire les CR2 pendant l’éclipse. DxO 600D : DR plate 100–400, descente **modérée** à 800 (~0,5 EV de span) — pas une grosse perte, et les poses umbra n’ont pas besoin des hautes lumières de *cette* RAW ; 800 est le seuil ISO-less (Sensorgen ~10,2). Quatre étendues à 9 RAW = +8 CR2.
**Rejeté :** sidéral par défaut ; décider 8a/8b selon l’aspect visuel ; ISO 400 par défaut sur les poses longues ; ISO 800 dès les vues 1–2 ; une seule phrase `say` longue.

**Complément :** fenêtre pénombre / aube et pause accu = [DEC-014](#dec-014--fenêtre-600d--pénombre-aube-pause-accu-2026-08-23). Diagnostics MAX (ISO 100 / 1600) = [DEC-015](#dec-015--max--rampes-diagnostic-iso-100-et-1600-2026-08-24). Incremental N + écarts Jubier = [DEC-016](#dec-016--incremental-n-aux-rampes-clés--proportions-jubier-2026-08-24).

---

## DEC-014 : Fenêtre 600D — pénombre, aube, pause accu (2026-08-23)

**Contexte :** DEC-013 figeait la *grille* (7 / 9, ISO, taux Lune). L’observateur valide le *calendrier* de séance : référence pleine Lune, poursuite après 06:44, swap LP-E8. Détail : [formes-prise-de-vue.md](formes-prise-de-vue.md) §6, §8, §11, §13.
**Décision (étude, branchée dans [`seance-600d-t150.txt`](../scripts/lem/essais-2026/seance-600d-t150.txt)) :**

1. **Départ ~04:20** (pénombre, ~U1−14 min), pas P1 03:24. Rampe **courte 5 vues** (1–5, côté 1/1000, ISO 100/200) : référence **pleine Lune**. Les vues umbra 6–9 crameraient tout le disque — on ne les programme pas ici.
2. **U1 → ~06:40** : inchangé (DEC-013) — rampe **7** courante ; **étendue 9** à U1+10, ~50 %, MAX, **et 06:30**. L’étendue 06:30 est un **4ᵉ stack HDR umbra** (~17 min après le MAX), pas le bloc MAX (produit 9 + diagnostics ISO 100 / 1600, DEC-015).
3. **Après 06:44 jusqu’au moonset (~07:20)** : on **continue**, rampes **raccourcies** (7 → 5 → 3) à mesure que le fond monte. À chaque palier on garde **une vue trop longue** (optimiste) ; on la jette après si le ciel l’a cramée. Plus d’étendue 9 après 06:30.
4. **Pause accu 10 min** vers **05:40–05:55** (après l’étendue ~50 % à 05:23, avant le MAX 06:13). LP-E8 sous le boîtier = coupure + USB tombé. Script : trou sans `TAKEPIC` ; `say` courts ; premier `TAKEPIC` après reprise en Incremental **N** (config complète), pas **Y**. Vérifier que LEM revoit `600D-T150` avant de reprendre.
5. Carte de séance 600D = **32 Go**. Pico d’écriture annoncé **80 Mo/s** vs **95 Mo/s** sur les 16 Go déjà benchées : **pas de re-calage** des 3 s entre départs ([KI-016](known-issues.md)) — le goulot mesuré est le USB 1,1 s/vue / le bus SD du 600D (~15–25 Mo/s), pas le débit marketing de la carte.
6. Cadence courante **2 min, ancrée sur MAX** (06:12:55 CEST). Saut du cran MAX+2 min (bloc MAX ~90 s, DEC-015).
7. Colonne Av du script = **5,6** (USB LEM, même valeur que le bench 15-85). La grille Tv/ISO est celle du **f/5** réel : le T-ring n’applique pas 5,6 ([KI-019](known-issues.md)).

**Justification :** 04:20 aligne le 600D sur le départ 100D et donne un stack uneclipsé. 06:44 n’est plus une coupure : le croissant reste posable, l’umbra non. Un LP-E8 (CIPA 440) + USB allumé 3 h ne couvre pas ~04:20→07:20 à 2 min ; le swap *avant* le MAX protège le produit. Volume élargi → 32 Go (16 Go ≈ 65 rampes de 7).
**Rejeté :** partir à U1 pile sans référence pleine Lune ; couper le 600D à 06:44 ; swap « si le témoin clignote » au MAX ; Incremental **Y** juste après power cycle ; recaler la rampe à 3 s *parce que* 80 Mo/s < 95 Mo/s.

---

## DEC-015 : MAX — rampes diagnostic ISO 100 et 1600 (2026-08-24)

**Contexte :** au MAX (06:13) la rampe **étendue 9** (DEC-013) est le *produit* HDR. Elle ne juge ni le suivi (plus longue = 2 s @ 800) ni le figé (plus courte = 1/1000 @ 100). Polar au viseur, taux Lune, PE inconnue. Détail : [formes-prise-de-vue.md](formes-prise-de-vue.md) §11, [KI-008](known-issues.md), [KI-010](known-issues.md).
**Décision (étude, MAX seulement, après le produit) :**

1. Ordre **figé** : (1) étendue nominale 9 vues — **ne pas la reculer** ; (2) rampe **ISO 100** constante, 7 × 2 EV, 1/1000 → **4 s** ; (3) rampe **ISO 1600** constante, 7 × 2 EV, **1/4000 → 1 s**. Pas aux autres instants clés.
2. Chaque rampe commence en Incremental **N** ([DEC-016](#dec-016--incremental-n-aux-rampes-clés--proportions-jubier-2026-08-24)). Entre les trois : **~10 s** sans `TAKEPIC` (tampon RAW Jubier = 5 ; 9+7+7 = 23 CR2 d’affilée satureraient). `say` courts (`Rampe max` / `Iso 100` / `Iso 1600`). Écarts intra-rampe : durée de la vue précédente + USB, **≥ 3 s** entre départs tant que le serré n’est pas validé.
3. Les deux rampes extra sont du **diagnostic**, pas un second HDR. On ne les merge pas avec l’étendue 9. ISO 1600 est **au-delà** du seuil ISO-less 800 (DEC-012) : le gain est la vitesse, pas la DR.
4. Bloc MAX ≈ **90–110 s**. La rampe courante suivante à ~2 min est **sautée** (le bloc *est* le MAX dédié, KI-010). +14 CR2, négligeable en 32 Go.

**Justification :** ISO 100 × 4 s montre la PE / la station (le 0,5 s @ 800 de la vue 7 nominale a les mêmes photons, 8× moins de filé). ISO 1600 × 1/4000 fige seeing + résidu de suivi ; au MAX le croissant supporte 1/4000 (DEC-012). Tout de suite après le produit, tant que le cadrage et le taux Lune sont encore ceux du MAX.
**Rejeté :** substituer le diagnostic à l’étendue 9 ; intercaler 100/1600 *avant* le produit ; répéter 100/1600 à U1+10 / 50 % / 06:30 ; ISO 3200+ ; fusionner les 23 RAW en un seul HDR.

---

## DEC-016 : Incremental N aux rampes clés + proportions Jubier (2026-08-24)

**Contexte :** Incremental **Y** n’envoie que le *delta* depuis le dernier `TAKEPIC`. Aux instants clés la grille ISO change (100/200/800 → 100 constant → 1600) ; un Y peut laisser Tv/ISO périmés ([KI-020](known-issues.md), [KI-022](known-issues.md)). Les exemples Jubier (`deluxe.txt`) mettent **N** en tête de chaque *bloc* de phase, **Y** ensuite. Détail : [formes-prise-de-vue.md](formes-prise-de-vue.md) §11, [DEC-015](#dec-015--max--rampes-diagnostic-iso-100-et-1600-2026-08-24).
**Décision (étude, script séance) :**

1. **Config complète (Incremental N)** sur le *premier* `TAKEPIC` de :
   - chaque rampe **étendue** (U1+10, ~50 %, MAX produit, éventuellement 06:30) ;
   - **chacune** des 3 rampes du MAX (étendue 9, ISO 100, ISO 1600) ;
   - la première rampe de la séance (~04:20) et la première après le swap accu (déjà DEC-014).
   Les vues suivantes de *cette* rampe : **Y**. Pas N sur chaque fichier (lent, inutile).
2. Rampes **courantes** à ~2 min : même schéma que le bench (1ʳᵉ vue **N**, suite **Y**) — déjà la « proportion » Jubier d’un bloc homogène.
3. **Écarts (aide LEM / FAQ « skips exposures »)** — non négociables, même si on resserre plus tard :
   - un horodatage **distinct** par vue (jamais 7 lignes au même MAX+0) ;
   - écart ≥ **durée de la vue précédente + ~1,1 s** (Benchmarks) ; 600D : **≥ 3 s entre départs** tant que le serré n’est pas validé ; après une pose 1 s, +4 s avant une 4 s (bench) ;
   - tampon RAW Jubier = **5** ; au MAX, **~10 s** sans `TAKEPIC` entre les 3 rampes (DEC-015) ;
   - APN encore occupé + Incremental Y = vitesse X demandée / Y prise.

**Justification :** N force Tv+Av+ISO avant un stack dont on ne relira pas les CR2. Y à l’intérieur d’une rampe évite de retéléverser l’ouverture muette à chaque vue (KI-019). Les 3 s / tampon 5 sont la recette Jubier déjà mesurée 7/7.
**Rejeté :** Incremental Y en tête d’une étendue ou d’une des 3 rampes MAX ; N sur les 7/9 vues de chaque rampe ; coller les `TAKEPIC` au même instant ; ignorer le tampon 5 au MAX.

---

## DEC-017 : 100D 24 mm — horizon au tiers bas, MAX au ciel (2026-08-25)

**Contexte :** forme A (time-lapse d’ambiance). Le 18–21 mm de la fiche lieu maximise U1→moonset dans le cadre. L’observateur retient une composition **paysage** : horizon sur le tiers inférieur, maximum d’éclipse vers le tiers supérieur, avec un peu de marge au-dessus du disque (27 mm serait pile, 28 mm trop juste).
**Décision :**

1. Focale forme A : **24 mm** paysage sur l’EF-S 15-85, Canon **100D**, trépied fixe.
2. Pointage : `composition: horizon_thirds` — axe optique à **5,91°**, azimut du MAX (**245,3°**). Le YAML [tournefeuille-100d-24mm.yaml](../scripts/config/tournefeuille-100d-24mm.yaml) ne centre plus la Lune.
3. **Recette terrain** (même famille que SEM DEC-009, Soleil tangent au bord haut) : trépied nivelé, horizon *visuel* sur le tiers inférieur. À **04:52:44** CEST, placer la Lune **tangente au bord supérieur**, à **20 % depuis la gauche**. Verrouiller jusqu’au moonset (07:20).
4. U1 (04:34, 24,5°) est **hors cadre**. Le film d’ambiance commence visuellement à l’entrée ~04:53 ; l’intervallomètre peut partir à 04:20 (ciel vide puis entrée). MAX à 63 % de la hauteur (tiers haut = 67 %). Moonset sur la ligne d’horizon, à ~73 % depuis la gauche. Disque ~50 px.
5. Schéma : [fov-100d-24mm-tiers.png](figures/fov-100d-24mm-tiers.png) (régénérer via `simulate_fov.py --config scripts/config/tournefeuille-100d-24mm.yaml`). Variante U1→SET encore dans [tournefeuille-100d-u1-set.yaml](../scripts/config/tournefeuille-100d-u1-set.yaml) (18–21 mm).

**Justification :** 24 mm laisse ~4° de ciel au-dessus du MAX et tolère un pointage un peu haut / un horizon réel un peu au-dessus de 0°. 18 mm garde U1 mais pose le MAX trop bas pour cette composition.
**Rejeté :** 28 mm (MAX pile sur le tiers, peu d’air) ; 18 mm comme plan A de *cette* composition ; portrait 35–40 mm (HFOV trop étroit pour le trajet azimutal).

---

## DEC-018 : 100D sous LEM — test 2 APN puis aube (2026-08-25)

**Contexte :** l’AEB ±2 du 100D (DEC-010) est un écart *fixe* autour d’un M figé. L’éclairement de scène à Tournefeuille (ciel clair, modèle crépuscule + plancher suburban ~0,03 lx) reste plat jusqu’~06:00, puis ~**+2 EV** au MAX, **~+5** à 06:30, **~+7** au civil (06:44), **~+14** au moonset. Le 100D vise l’ouest : borne haute, le ciel anti-solaire peut monter 1–2 EV moins vite. LEM gagnerait à **reculer la centrale** (et passer à 5 vues), pas à copier le 7 × 2 EV du 750 mm. Le 100D n’a jamais été vu sous LEM 1.3.3β1 ([KI-007](known-issues.md)). Mac crash ignoré pour cette piste.
**Décision (séquentielle — pas de script aube tant que le test 2 APN n’est pas OK) :**

1. Nom APN Configuration matérielle : **`100D-W24`** (wide 24 mm), même esprit que `600D-T150`.
2. **Prochain essai :** scénario **simple** deux boîtiers USB (quelques `TAKEPIC`, temps simulé) — protocole [essais-2026/README.md](../scripts/lem/essais-2026/README.md). Inclure un volet **allumage tardif** ([KI-023](known-issues.md)).
3. **Si le 100D est vu et le dual USB tient :** script 100D qui **accompagne le jour** (grille ci-dessous, JPEG Fine, intervalle **90 s**, f/4) + `COMMAND ;say` **courts** (KI-021) pour le cadrage DEC-017 (**04:52:44**, bord haut, 20 % gauche, horizon au tiers).
4. **Repli :** AEB + intervallomètre ; un cran M à la main ~06:40 (sans éteindre, KI-009) si LEM ne voit pas le 100D. Le 600D USB reste prioritaire.

**Grille aube (étude ; centrale nuit 4 s · ISO 800 = placeholder, non mesurée) :**

| Fenêtre CEST | Soleil | ΔEV scène vs 04:20 | Vues | Centrale vs nuit | Exemple Tv / ISO |
|--------------|--------|---------------------|------|------------------|------------------|
| 04:20 – 06:10 | < −12° | 0 → +2 | **3** (±2 EV) | 0 | 1 s / 4 s / 16 s · 800 |
| 06:10 – 06:25 | −12 → −9° | +2 → +4 | **5 × 2 EV** | −2 EV | 1/4 … 4 s · 800 |
| 06:25 – 06:40 | −9 → −7° | +4 → +6 | 5 × 2 EV | −5 EV | 1/15 … 1 s · 800 |
| 06:40 – 06:55 | −7 → −4° | +6 → +9 | 5 × 2 EV | −8 EV | 1/60 … 1/4 · 400 |
| 06:55 – 07:10 | −4 → −1,5° | +9 → +12 | 5 × 2 EV | −11 EV | 1/250 … 1/15 · 200 |
| 07:10 – 07:20 | −1,5 → +0,7° | +12 → +14 | 5 × 2 EV | −13 EV | 1/1000 … 1/60 · 100 |

Cinq vues × 2 EV = 8 EV de filet autour d’une centrale qui suit le ciel. Recouvrement ~2 EV entre paliers (nuage, ouest plus sombre). ~450 JPEG uniques vs ~720 doublons AEB « C » = 2. Le 100D plafonne à 1/4000 : sans baisser l’ISO, le moonset est pile au plafond si le modèle est juste.

**Allumage en cours de route (ménager le LP-E12) :** oui **en principe**. FAQ LEM *« batterie vide »* : l’appli continue ; on remet un accu, on **allume**, *« les prochaines actions seront automatiquement exécutées »* — pas de rechargement mentionné. Premier `TAKEPIC` après reconnexion : Incremental **N** (analogue [KI-022](known-issues.md)). **Recharger le script (⌘R)** seulement si les lignes `100D-W24` ont été **sautées au chargement** (souvenir observateur ; option non retrouvée dans l’aide miroir — [KI-023](known-issues.md)). Ne pas recharger pendant une rampe 600D (actions déjà passées, [KI-020](known-issues.md)).

**Justification :** le levier utile est l’horloge, pas un HDR de 50 px. Dual USB = aussi un test de robustesse Mac. L’allumage tardif n’a de sens que si les lignes 100D sont *dans* le script en cours.
**Rejeté :** écrire le script aube avant le test 2 APN ; rampe 7 × 2 EV disque sur le 24 mm ; éteindre le 600D pour ménager le 100D.

**Complément 2026-08-28 :** test 2 APN OK → scripts [`seance-100d-w24.txt`](../scripts/lem/essais-2026/seance-100d-w24.txt) et [`seance-2apn-interlace.txt`](../scripts/lem/essais-2026/seance-2apn-interlace.txt). Tv `15` s (pas `16`). Marge allumage 60 s. Écart inter-boîtiers = [DEC-019](#dec-019--écart-inter-boîtiers-2-s--600d-prioritaire-2026-08-28).

---

## DEC-019 : Écart inter-boîtiers 2 s, 600D prioritaire (2026-08-28)

**Contexte :** LEM est USB série. Deux `TAKEPIC` au **même horodatage** n’en exécutent qu’un ([KI-020](known-issues.md), observé sur un seul boîtier). Le bench entrelacé du 26 août a *tenu* un chevauchement 7 CR2 + ~8 JPG dans ±25 s, mais un skip le jour J est trop cher.
**Décision :**

1. **600D jamais décalé** — horodatages = [`seance-600d-t150.txt`](../scripts/lem/essais-2026/seance-600d-t150.txt).
2. **100D glisse (≤ 60 s) ou saute** le cycle si la fenêtre est prise. Cadence nominale 90 s = grille, pas horloge figée.
3. **Écart :** ne pas démarrer le boîtier B avant la fin de (pose A + USB 1,1 s) **+ 2 s**. Pas deux `TAKEPIC` dans la même seconde.
4. Script jour J dual = [`seance-2apn-interlace.txt`](../scripts/lem/essais-2026/seance-2apn-interlace.txt). Les scripts solo restent le repli un boîtier / AEB.

**Justification :** 2 s au-delà du USB Benchmarks laisse le bus changer d’EDSDK sans coller les horodatages. Un cycle 100D sauté au bloc MAX (~90 s occupés) vaut mieux qu’un JPEG dans l’étendue 9.
**Rejeté :** chevauchement USB « parce que le bench l’a tenu » ; décaler le 600D ; intercaler le 100D dans les 10 s de tampon MAX.

---
