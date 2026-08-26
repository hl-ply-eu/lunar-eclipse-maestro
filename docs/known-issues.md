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
**Reste ouvert :** élévation 155 m approx. ; horizon local ouest–SO non levé. Parc DEC-009 ; formes DEC-010 (étude, pas plan de séance).

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

**Statut :** **600D OK** (2026-08-23). **100D OK** sous LEM 1.3.3β1 (2026-08-26) : benches simple, séquentiel et entrelacé ; JPG-F ; dual USB tenu. Suite : script aube + marge allumage ([KI-025](known-issues.md)).
**Symptôme :** la page de téléchargement LEM 1.3.3β1 cite une plage Canon (« 1D Mark III up to 6D Mark II and 200D ») qui n'est pas un inventaire exhaustif. SEM a piloté le 600D ; LEM est plus ancien. Le 100D est listé dans l’aide Configuration APN (EOS 100D / Rebel SL1 / Kiss X7, USB, tampon RAW 6).
**Action :** ne pas écrire le script aube 100D tant que LEM n’a pas vu le boîtier et tenu deux USB. Repli = AEB autonome (DEC-010). Ne pas copier un script SEM en changeant seulement le nom d'appli. Si LEM ne voit qu’un corps, garder le 600D.

---

## KI-008 : Trépied fixe — filé sur les poses umbra

**Statut :** Valable pour les **chapelets** sur trépied fixe (DEC-009). Le gros plan 600D est désormais sur **monture équatoriale** (750 mm) : le filé sidéral ne s’applique plus à ce corps, sous réserve de mise en station.
**Symptôme (trépied fixe) :** à 280 mm APS-C, ~4,5 px/s (≈ 14″/s). Une pose umbra de 1–4 s produit 5–18 px de filé. À 60 mm : ~1 px/s ; à 15–25 mm : négligeable pour 1–4 s.
**Action :** plafond de pose vs SNR uniquement sur le boîtier chapelet (trépied). Sur l’équatoriale : juger l’erreur périodique / mise en station, pas la dérive diurne. Le simulateur `simulate_fov.py` (caméra fixe) ne décrit **pas** le 750 mm suivi.

**Viseur polaire (pas d’astrométrie) :** une erreur de station de ~0,5° ne fait qu’une fraction de pixel en 4 s à 750 mm. Le filé dominant **sans taux Lune** est le décalage lunaire vs sidéral (~0,55″/s → **~2″ / ~2 px en 4 s**, **~7 px en 15 s** à 750 mm APS-C). **DEC-013 : activer le suivi lunaire** (rappel oral dans le script). Avec ce taux, il reste l’erreur périodique / la station. Alignement dans la nuit, **avant 04:20**, pas à 06:13. Rampe courante : plus longue **1/2 s @ ISO 800**. Rampes **étendues** (1 s + 2 s @ 800, cas sombre) **uniquement** aux instants clés, taux Lune **on**. Pas de tri sur le vif (carte dans le boîtier).

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
**Action :** prévoir un **déclenchement manuel dédié au maximum** (et autour de U1 si besoin). Noter l'heure de départ réelle. L'intervalle du chapelet ne doit pas être le seul filet pour l'instant critique. Sous LEM, le MAX 600D est le **bloc** étendue 9 + diagnostics ISO 100 / 1600 ([DEC-015](decisions.md)) : ne pas y superposer une rampe courante à +2 min.

---

## KI-012 : Multiplicateurs sur le 750 mm — pas équivalents

**Statut :** À valider sur le train optique réel (bague EF du télescope).
**Symptôme :** Canon Extender EF 1.4× II (1050 mm, f/7,1) vs doubleur Hoya prévu pour **Olympus Zuiko** (1500 mm, f/10). Montage, tirage et piqué ne sont pas interchangeables ; le Hoya a déjà donné de bons résultats mais est jugé moins qualitatif.
**Action :** ne pas traiter 1,4× / 2× comme de simples coefficients dans un YAML FOV fixe. Tester le jeu de bagues avant J−7. Au f/10, budget de pose et seeing limitent plus que le cadre.

---

## KI-013 : Ambiance fixe et chapelet rampé s’excluent sur une expo

**Statut :** Contrainte de l’étude des formes (DEC-010).
**Symptôme :** un time-lapse d’ambiance exige une expo **constante** (l’assombrissement est le sujet). Un chapelet / une rampe LEM expose le disque et **efface** cette histoire. L’AEB 100D (±2 EV) ne couvre pas l’écart croissant/umbra (8–12 EV).
**Action :** 100D = AEB pour le time-lapse (choix de vues / aube), 600D = rampe HDR du disque. Ne pas vendre « LEM sur le wide = les deux produits ». Détail : [formes-prise-de-vue.md](formes-prise-de-vue.md).

---

## KI-014 : Umbra photographiable au MAX, plus après le crépuscule civil

**Statut :** Géométrie Tournefeuille 28 août 2026 (Skyfield DE421).
**Symptôme :** le MAX est à 06:13 CEST, proche de l’aube calendaire, ce qui suggère un ciel trop clair pour des poses umbra. En réalité le Soleil est encore à **−11,2°** (crépuscule nautique), à 179° d’azimut de la Lune.
**Action :** poser l’umbra **U1 → ~06:40**. Dès le crépuscule civil (06:44, Lune à 5,6°) les poses longues ramassent l’aube. Après le lever (07:15) l’umbra est perdue. Le **600D continue** jusqu’au moonset avec des rampes **raccourcies** (croissant / silhouette, [DEC-014](decisions.md)) ; le 100D AEB aussi, pour l’ambiance. Ne pas conclure « MAX = jour ».

---

## KI-015 : Liseré turquoise — tons *moyens* du HDR, pas les extrêmes

**Statut :** Connu (ozone / Chappuis) ; plus difficile en partielle 2026 qu’en totalité.
**Symptôme :** bande cyan étroite (~2′) au bord de l’umbra, souvent manquée (œil ébloui par le croissant, ou stack à 2 vues seulement). Pas un liseré « vert » saturé.
**Action :** 7 poses × 2 EV au 750 mm ; ne pas jeter les vues intermédiaires ; WB plutôt daylight. Détail : [formes-prise-de-vue.md](formes-prise-de-vue.md) §11.

---

## KI-016 : 16 Go — le RAW AEB 100D ne tient pas 3 h

**Statut :** Contrainte matériel observateur (cartes **16 Go**, une **32 Go** carte de séance 600D, 2 accus / boîtier).
**Symptôme :** 100D, « C » = 2 → 6 fichiers / impulsion. Sur 16 Go : ~620 CR2 vs ~2 470 JPEG Fine. À 90 s pendant 3 h : 720 fichiers (~17 Go en RAW, ~5 Go en JPEG). À 60 s : 1 080 fichiers, encore pire en RAW. Deux accus CIPA (380 × 2 = 760) couvrent 720 déclenchements (90 s), pas 1 080 (60 s). 600D : ~88 rampes de 7 RAW rempliraient une 16 Go ; une carte **pleine** ralentit l’énumération USB (leçon SEM). Fenêtre DEC-014 (~04:20 → 07:20 à ~2 min) ≈ 500+ CR2 → **au-delà du plafond 16 Go avec marge**.
**Débit annoncé 32 Go vs 16 Go :** 32 Go **80 Mo/s**, 16 Go benchées **95 Mo/s** (pics marketing, souvent UHS-I « jusqu’à »). Un CR2 ~24,5 Mo à 80 Mo/s ≈ 0,3 s/fichier vs 0,26 s à 95 Mo/s (~50 ms). Le 600D (2011) n’alimente le bus SD qu’à **~15–25 Mo/s** ; LEM Benchmarks = **1,1 s/vue** USB. Les deux cartes sont au-dessus du plafond boîtier. Tampon RAW Jubier = 5 ; espacement 3 s entre départs déjà largement > vidage d’un CR2. **Pas de re-calage** des timings de rampe. Inconnu : Speed Class réelle (U1/V10 vs U3/V30) — si la 32 Go n’était que U1, le plancher *garanti* (10 Mo/s) resterait sous le bus 600D. Optionnel : une rampe 7/7 sur la 32 Go pour confirmer le tampon, pas pour changer les 3 s a priori.
**Action :** 100D en **JPEG Fine + AEB** ; défaut **90 s** ; 60 s seulement avec swap d’accu **et** AEB réarmé (KI-009). 600D : RAW sur **32 Go** (séance élargie, DEC-014) ; 16 Go = filet / plafond **~65 rampes** si on restait U1→06:40 ; ne pas remplir. Ne pas régler l’intervallomètre sur la *durée de film* voulue. Détail : [formes-prise-de-vue.md](formes-prise-de-vue.md) §13, [DEC-011](decisions.md), [DEC-014](decisions.md).

---

## KI-017 : ISO « sports » ~800 ≠ moins de brackets HDR

**Statut :** Confusion de métriques (DxO *Low-Light* / ISO-less DSO vs span de scène).
**Symptôme :** prendre 793 / 843 (DxO Sports) ou le « best ISO 800 » ciel profond comme ISO de travail unique, et en déduire qu’on peut raccourcir le 7 × 2 EV — sauf si 1/4000 s clippe le croissant.
**Action :** le contraste croissant/umbra ne dépend pas de l’ISO ; 800 **raccourcit les temps**, pas le nombre de vues. **800 n’est pas l’ISO des vues courtes** (DEC-013) : 100/200 sur 1–5 (limbe U1), **800 sur les poses longues**. 400→800 n’est pas une grosse perte RAW umbra. 1/4000 est trop lent à ISO 800 · f/5 **à U1**, pas au MAX. ISO **1600** = diagnostic MAX seulement ([DEC-015](decisions.md)), au-delà de l’ISO-less : figé, pas DR. 100D : 800 aide le cycle AEB. Détail : [formes-prise-de-vue.md](formes-prise-de-vue.md) §11, [DEC-012](decisions.md).

---

## KI-018 : `basic.txt` / `deluxe.txt` LEM = totalité, pas la séance 2026

**Statut :** Copie Pap 2026-08-23 (`scripts/lem/`).
**Symptôme :** les exemples livrés avec LEM (15 déc. 2010, APN `D300`) programment **U2 / U3 / MAXPRE / MAXPOST**, de la pénombre jusqu’à P4, et une vitesse par phase. Le 28 août 2026 n’a **pas de totalité** ; à Tournefeuille U4 et P4 sont **sous l’horizon** ; le protocole retenu est **7 × 2 EV** (DEC-010), pas une vue toutes les 1–5 % de magnitude.
**Action :** s’en servir comme grammaire (`TAKEPIC`, `FOR`, contacts `P1`/`U1`/`MAX`/`SET`). Ne pas les charger tels quels. Ne pas porter un script SEM (`C1`/`C2`) en changeant le nom d’appli. Bench : [`scripts/lem/essais-2026/`](../scripts/lem/essais-2026/).

---

## KI-019 : Télescope / optique muette — LEM et le champ ouverture

**Statut :** À tester au foyer (après le bench 15-85). L’aide Jubier **ne documente pas** le cas.
**Ce que dit LEM :** Configuration initiale / préparatifs : régler le boîtier **et l’objectif** en MAP manuelle — *« does not apply to a non-AF lens or telescope »*. Dépannage : si l’AF est encore armé et que la MAP échoue, **la vue n’est pas prise**. Rien sur un T-ring / bague EF sans contacts (pas de diaphragme, pas de puce).
**Conséquence attendue (non vérifiée) :** `TAKEPIC` envoie quand même une ouverture (colonne obligatoire). Le 600D peut ignorer, renvoyer une erreur EDSDK, ou bloquer la vue. Incremental **N** (1ʳᵉ vue du bench) force vitesse + ouverture + ISO ; **Y** ne retéléverse l’ouverture que si elle change — notre rampe est à f/5,6 constant donc les 6 suivantes ne retouchent pas le diaph.
**Action :** bench actuel = **15-85 @ f/5,6**, nom APN **`600D-T150`**. Ensuite une rampe (ou un `TAKEPIC` isolé) au 150 mm f/5 : noter le log LEM, si les 7 CR2 sortent, et l’EXIF ouverture (`00` / absent / f/5,6 fantôme). Sur le boîtier : confirmer qu’un déclenchement **manuel** au T-ring fonctionne avant d’incriminer LEM.

---

## KI-020 : `TAKEPIC` au même horodatage — LEM n’en exécute qu’un

**Statut :** Constaté 2026-08-23, bench 600D-T150 (`IMG_7684` : 1 CR2 à **1/15 s**). Contre-essai espacé **7/7** (`IMG_7685`–`7691`, gaps 3,00 s / 4,00 s, fenêtre 23,0 s).
**Symptôme :** sept `TAKEPIC,MAX,+,00:00.0,…` collés. LEM les traite comme dus *en même temps* ; le 600D n’en prend qu’une (ici la 4ᵉ vitesse de la rampe). Aide format : l’écart entre deux poses doit **inclure la durée de la précédente**. FAQ dépannage : *« My camera skips exposures »* → espacer ; APN lents **≥ 3 s**.
**Action :** un horodatage **distinct** par vue. Bench : départs MAX+0 / +3 / +6 / +9 / +12 / +15 / +19 s. Temps simulé **avant** MAX (−30 s) et **laisser courir** jusqu’à MAX+30 s (ne pas sauter pile sur MAX : les actions à +0 sont alors déjà « passées »). Recopier le `.txt` sur le Mac après chaque edit. Script séance : Incremental **N** en tête des étendues et de **chaque** rampe MAX ([DEC-016](decisions.md)) ; écarts = durée précédente + ~1,1 s, plancher 3 s ; tampon 5 → ~10 s entre les 3 blocs MAX.

**Trop serré mais horodatages distincts** (pas le cas MAX+0) : LEM n’empile pas. Chaque `TAKEPIC` part à *son* instant. Si le 600D est encore en pose / USB / vidage, FAQ : vue **sautée**, ou vitesse **X demandée / Y prise** (surtout Incremental **Y** : le changement de réglage n’est pas passé). Tampon RAW Jubier = **5** : au-delà le boîtier décroche. Analyseur : Temps libre &lt; 1–2 s = suspect. Règle d’écart : **durée de la vue précédente + ~1,1 s** (Benchmarks) + marge.

---

## KI-021 : `COMMAND ;say` — messages longs muets (leçon SEM)

**Statut :** Mesuré sur **SEM** le 2026-08-12 (même famille d’appli, même Mac). Pas encore benché sous LEM ; on applique la même recette au script séance ([DEC-013](decisions.md)).
**Symptôme :** `COMMAND ;say` s’exécute, mais un message trop long reste **muet**. SEM : « Controle. Mise au point. Niveau du trepied. Filtre en place. Cadrage dans quatre minutes. » = silence ; la même phrase sans la dernière clause = OK. Seuil pratique ≈ **60 caractères**. Accents UTF-8 : scripts en **ASCII pur** (SEM KI-013).
**Action (script LEM final) :** plusieurs annonces **courtes**, **espacées d’~1 s**, plutôt qu’un paragraphe. Ex. rappel suivi : `say "Suivi Lune"` puis +1 s `say "Pas sideral"` — pas « Verifier le taux lunaire de la monture, pas le sideral. ». Repli SEM (`PLAY FR_*.wav` dans `AdditionalSounds/`) seulement si `say` est muet aussi sous LEM. Détail : [scripts/lem/essais-2026/README.md](../scripts/lem/essais-2026/README.md).

**Idée (2026-08-26) — progression de rampe :** accompagner chaque début de séquence par des `say` du type *boîtier / rang / taille*, en **2–3 fragments ASCII** (≲ 60 car. chacun, +1 s), pas une seule phrase longue. Ex. générateur :

```
say "600D"
say "Rampe 12 sur 35"
say "7 vues"
```

Même schéma pour le 100D (`100D` / `Cycle 40 sur 500` / `3 vues`). À brancher dans `generate_lem_seance.py` / benches quand on écrit le script aube. Backlog todo.

---

## KI-022 : Swap LP-E8 600D — USB tombé, Incremental Y périmé

**Statut :** Décision de séance ([DEC-014](decisions.md)) ; pas encore répété sous LEM (le bench 23 août n’a pas coupé l’accu).
**Symptôme :** le LP-E8 s’extrait par le **fond** du 600D. Couper l’accu = extinction + **renumérotation USB**. LEM peut garder en cache les derniers Tv/Av/ISO. Un `TAKEPIC` Incremental **Y** n’envoie que le *delta* : vitesses fausses ou vues sautées (voisin de [KI-020](known-issues.md)). Ce n’est pas l’AEB qui s’efface ([KI-009](known-issues.md), 100D).
**Action :** trou script **10 min** (~05:40–05:55, après étendue ~50 %, avant MAX). `say` courts (T−2 min, T−1 min, début de trou, reprise). Premier `TAKEPIC` après reprise : Incremental **N**. Même **N** en tête de chaque étendue et de chaque rampe MAX ([DEC-016](decisions.md)). Vérifier l’icône `600D-T150` avant de laisser courir. Ne pas swapper au MAX ni pendant une étendue. Détail : [formes-prise-de-vue.md](formes-prise-de-vue.md) §13.

---

## KI-023 : APN éteint au chargement / allumé en cours de script

**Statut :** Aide officielle claire pour un *accu vide en cours de run* ; le cas « jamais vu au chargement » n’est **pas** documenté dans le miroir. À trancher au test 2 APN ([DEC-018](decisions.md)).
**Ce que dit LEM :**

- FAQ *« Que dois-je faire quand la batterie de l’APN est vide ? »* ([Dépannage](../mirror/xjubier.free.fr/site_pages/lunar_eclipses/Lunar_Eclipse_Maestro_Help/pgs2/btoc8.html)) : LEM **continue**. On met un autre accu, on **allume** ; *« les prochaines actions seront automatiquement exécutées normalement. »* Aucun *Recharger script* dans cette réponse.
- Configuration matérielle ([c1sem7](../mirror/xjubier.free.fr/site_pages/lunar_eclipses/Lunar_Eclipse_Maestro_Help/pgs/c1sem7.html)) : un APN apparaît dès qu’il est allumé sur USB (comme un GPS ouvert après le dialogue).
- Nouveautés : *Simulation des APNs* — APN **absent pendant l’exécution** → bruit d’obturateur (les lignes sont donc *dans* le script, pas forcément exécutées sur le boîtier).
- **Recharger script (⌘R)** : relit le fichier après **édition**. Un offset vide s’exécute au **chargement**, pas au rechargement. Une mise à jour GPS **recharge** le script en cours. Relire en cours de séance saute les actions déjà « passées » ([KI-020](known-issues.md)).

**Souvenir observateur (SEM/LEM) :** par défaut, au *chargement*, les lignes d’un APN **non connecté** seraient ignorées ; une **option** permettrait de charger quand même. **Non retrouvée** dans l’aide miroir (préférences `c1sem9` très lacunaires, menus `btoc3`, dépannage). Possible dialogue à ⌘L, case non listée, ou confusion avec la simulation. À noter tel quel au test : Visualiseur de script, lignes `100D-W24` présentes ou non.

**Conséquence pour ménager le LP-E12 :**

1. **Oui on peut l’allumer plus tard** si les lignes 100D sont *déjà* dans le script en cours (FAQ batterie). Premier `TAKEPIC` : Incremental **N** (cache Tv/Av/ISO, [KI-022](known-issues.md)).
2. Si le 100D n’était **pas** dans la Configuration matérielle au ⌘L et que ses lignes ont disparu : l’allumer ne suffit pas — **recharger** une fois l’icône `100D-W24` visible, **hors rampe 600D** (trou, ou avant 04:20). Ne pas recharger au milieu d’une étendue 9.
3. Ne pas éteindre / rallumer le **600D** pour ça (swap déjà prévu ~05:40).
4. USB 3 h + LEM draine plus qu’un intervallomètre : l’allumage tardif (~04:15) n’a d’intérêt que si le volet 2 du bench 2 APN le confirme.

**Action :** au test simple, trois passes — (a) les deux allumés au chargement ; (b) 100D éteint au ⌘L, allumé pendant le temps simulé, **sans** ⌘R ; (c) si (b) est muet, ⌘R une fois reconnu. Noter l’option / le dialogue s’il apparaît. Repli AEB si (a) échoue.

---

## KI-024 : Qualité / vitesses script 100D sous LEM

**Statut :** confirmé 2026-08-26 (bench 2 APN).
**Symptôme :**

1. Jeton qualité hors liste → LEM annonce un basculement **RAW**. Chaîne valide sur EOS 100D : **`JPG-F`** (aide Scripts `btoc6`). **`JPG-L`** était une mauvaise lecture des Propriétés disponibles (taille L ≠ jeton qualité).
2. Vitesses hors crans Canon (`1/16`, `16` s) : le boîtier prend le voisin (`1/15`) ou **ne change pas** (demande `16` s après une `4` s en Incremental **Y** → EXIF resté à **4** s, alors que LEM a cadencé comme pour 16 s).

**Action :** colonne Quality = **`JPG-F`** ; Size = `None`. N’écrire que des Tv de l’enum LEM ([lem-apn-scripting.md](lem-apn-scripting.md), dumps [lem/camera-properties/](lem/camera-properties/)). Incremental **N** en tête de chaque rampe **et** sur toute vue dont la pose est ≥ 1 s (ou après un gros saut Tv).

---

## KI-025 : Démarrage LEM dual USB + délai reconnexion 100D

**Statut :** confirmé 2026-08-26 (bench entrelacé).
**Symptôme / procédure :**

1. **Ordre boot :** LEM doit démarrer **sans scénario**. Allumer les deux APN **consécutivement** (espacement **15–20 s**), attendre la reconnaissance des deux icônes, **ensuite** charger le script. Un scénario déjà chargé au lancement gêne la reconnaissance.
2. **Allumage en cours de run** (après extinction) : FAQ batterie ([KI-023](known-issues.md)) reste vraie *en principe*, mais l’USB n’est pas instantané. Bench interlace : `say` « Cent D » à MAX+150 s ; power-on ~1–2 s après ; **premier JPG à MAX+180,3 s** (cycle TL02). **TL01** (3 vues, +160…+166 s) entièrement manqué. Latence power-on → 1ʳᵉ vue ≈ **29 s** ; say → 1ʳᵉ vue ≈ **30 s**. Ensuite 23 cycles stables, cadence 20 s, Tv exacts, dual USB OK pendant les rampes 600D.

**Action :**

- Documenter l’ordre boot dans [lem-apn-scripting.md](lem-apn-scripting.md) et le README essais.
- Pour un allumage tardif le jour J : prévoir **≥ 45 s** de marge (retenu **60 s**) entre allumage et premier `TAKEPIC` 100D ; `say` en avance ; Incremental **N** sur la 1ʳᵉ vue. Ne pas compter sur les créneaux dans les ~30 s suivant le power-on.
- Générateurs aube / interlace : décaler le 1ʳᵉ bracket 100D d’autant (prochaine itération).
