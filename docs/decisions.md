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
**Rejeté :** expo unique sans AEB sur le 100D (l’aube casse le run) ; doubleur comme plan A ; P1 dans le plan privilégié ; LEM sur le 100D comme plan A ; choisir le boîtier au foyer « parce qu’il est meilleur au DxO » ; une seule RAW « parce que 11,5 EV ».

**Note OM System (2026-08-22) :** OM-3 / OM-5 II **sans test DxO publié**. Proxy labo = E-M1 II (80 / 12,8 EV / ISO 1312) ; PDR PhotonsToPhotos OM-3 9,64 / OM-5 II 9,79. Gain RAW ~+1 EV vs Rebel, poids surtout sur les zooms, **perte LEM**. Pas un changement *pour* le 28 août. Détail : [formes-prise-de-vue.md](formes-prise-de-vue.md) §10.

---

## DEC-011 : Volume de prises — JPEG 100D, RAW 600D, pas 60–90 s (2026-08-22)

**Contexte :** cartes **16 Go** (et une **32 Go** pour densifier le 600D), **2 batteries par boîtier** ; produit 100D = time-lapse d’ambiance (forme A), 600D = HDR disque (forme C). Détail : [formes-prise-de-vue.md](formes-prise-de-vue.md) §13. Complément 600D (durée de rampe / capacité) le **2026-08-23**.
**Décision (étude, pas encore calage terrain) :**

1. **Intervalle 60–90 s** = pas de l’intervallomètre 100D, **pas** la durée du film. 3 h à 90 s → ~120 images/couche → **~5 s** à 25 fps / **~10 s** à 12 fps. Un film cible de 60–90 s exigerait un pas de 5–7 s, incompatible avec AEB « C » = 2.
2. **100D en JPEG Fine + AEB** (« C » = 2 → 6 JPEG / impulsion). Défaut **90 s** (~720 fichiers, ~5 Go, 2× LP-E12 sans swap). **60 s** seulement si l’essai AEB montre une centrale assez courte *et* avec changement d’accu (réarmer l’AEB, KI-009).
3. **600D en RAW.** Une rampe 7 × 2 EV dure **~20–25 s** sous LEM (~10–15 s en manuel) : l’obturation (5,3 s à ISO 100) n’est pas le poste. Une **16 Go** tient **~65 rampes** avec 20–25 % de marge (~620 CR2 plein ; ne pas remplir). Une **32 Go** est disponible si le pas descend sous ~2 min. Les 4 stacks nommés (U1+10, ~50 %, MAX, 06:30) + milieu 3–4 min (~60–90 CR2) restent un choix de *produit*, pas une limite carte. 2× LP-E8 sans enjeu.
4. Viser **~10–20 s de film** d’ambiance, pas une minute.

**Justification :** une 16 Go tient ~620 CR2 vs ~2 470 JPEG Fine ; 3 h d’AEB RAW à 60–90 s déborde (KI-016). Le JPEG 18 Mpx reste au-dessus d’une Full HD ; l’AEB ±2 EV est le filet aube. Deux accus CIPA (380 × 2) couvrent ~720 déclenchements (90 s), pas 1 080 (60 s). Sur le 600D, l’horloge LEM (~2,5 s entre départs `TAKEPIC`, tampon 6 RAW) fixe la durée de rampe ; le temps de séance (126 min) n’est pas le goulot — la carte 16 Go l’est dès ~84 rampes (pas 90 s).
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

**Justification :** le span HDR est une propriété de la *scène* (Jubier / Espenak), pas du gain analogique. Les deux Rebel plafonnent à 1/4000 s.
**Rejeté :** « ISO optimal 800 ⇒ moins de brackets » ; ISO 800 dès U1 sur les vues courtes du 750 mm.
