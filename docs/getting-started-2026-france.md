# Getting Started — éclipse lunaire du 28 août 2026 (France)

Guide opérationnel pour [Lunar Eclipse Maestro](http://xjubier.free.fr/en/site_pages/lunar_eclipses/Lunar_Eclipse_Maestro_Photography_Software.html) (LEM) et le duo **Canon 600D-Tele + 100D-Wide**.

L’aide officielle (© Xavier Jubier) reste la référence : [miroir local](../mirror/index.html) après `./scripts/mirror.sh`, ou [en ligne](http://xjubier.free.fr/site_pages/lunar_eclipses/Lunar_Eclipse_Maestro_Help/pgs2/btoc1.html).

**Statut :** site recalé **Tournefeuille** ([DEC-008](decisions.md), [fiche lieu](lieux/tournefeuille-2026.md)). Horaires en **CEST** (UTC+2). Parc : [DEC-009](decisions.md). Formes (étude) : [DEC-010](decisions.md), [formes-prise-de-vue.md](formes-prise-de-vue.md).

---

## 1. L’événement

Éclipse **lunaire partielle profonde** (quasi-totale) : magnitude umbrale **0,93**. Pas de totalité. Contacts en **UTC** fournis pour le point 43°34′56.6″ N, 1°21′03.4″ E ; visibilité locale = altitude + moonset.

| Contact | UTC | CEST | Alt Lune | Notes |
|---------|-----|------|----------|--------|
| P1 (pénombre) | 01:23:59 | 03:24 | 31,6° | Ombre souvent peu visible au début |
| O1 / U1 (ombre) | 02:33:52 | 04:34 | 24,5° | Début de la partielle umbrale |
| MAX | 04:12:55 | **06:13** | **10,5°** | ~96 % du disque dans l’umbra |
| Coucher | 05:20:26 | **07:20** | 0° | Fin de séance |
| O2 / U4 | 05:52:03 | 07:52 | −6° | **Sous l’horizon** |
| P2 / P4 | 07:01:47 | 09:02 | −18° | Sous l’horizon |

Régime « objet bas puis coucher », proche de Frías le 12 août (soleil ~8°) mais Lune un peu plus haute au MAX qu’à Paris (~8°). Le Soleil se lève pendant le moonset.

---

## 2. Matériel visé (DEC-009)

Capteur **équivalent** sur les deux boîtiers (APS-C 22,3 × 14,9 mm, 5184 × 3456 px) : DxOMark RAW 65 vs 63, dynamique 11,5 vs 11,3 EV — écart négligeable ([formes-prise-de-vue.md](formes-prise-de-vue.md) §9). Pas de filtre solaire. Le 600D n’est pas « le meilleur capteur ».

| Rôle | Boîtier | Optique | Monture |
|------|---------|---------|---------|
| **Gros plan** | 600D | Télescope 150 mm f/5 → **750 mm** ; option 1,4× Canon (1050 mm) ou doubleur Hoya Zuiko (1500 mm, [KI-012](known-issues.md)) | **Équatoriale** (suivi) |
| **Chapelet** | 600D *ou* 100D | EF-S 15-85 mm f/3,5–5,6 (souple, un peu fermé) ; EF-S **60 mm f/2,8** Macro ; EF **70–200 mm f/4 L** | Trépied **fixe** |

Le 70–200 n’est plus le télé 600D par défaut. U1→moonset (~40°) ne tient que sur le **15-85 vers 18–25 mm** ; 60 mm et 70–200 = chapelet plus court ou recentré. Filé sidéral : [KI-008](known-issues.md) (trépied seulement).

Hypothèse actuelle (DEC-010) : 600D @ 750 mm = HDR disque ; 100D @ 15-85 = time-lapse d’ambiance. LEM plutôt sur le 600D. **Candidat** ([DEC-018](decisions.md)) : 100D aussi sous LEM (`100D-W24`) pour suivre l’aube — seulement après un test 2 APN simple. Détail : [formes-prise-de-vue.md](formes-prise-de-vue.md).

---

## 3. LEM vs réalité Mac (lire avant d’écrire un script)

LEM est **macOS uniquement** ([KI-001](known-issues.md)) et **s’arrête à Mojave** ([KI-006](known-issues.md)). Catalina et suivants : l’auteur indique qu’une réécriture serait nécessaire ; repli = VM Mojave.

Le Mac qui a piloté Solar Eclipse Maestro le 12 août 2026 peut donc **ne pas** lancer LEM. Jusqu’au test :

1. Lancer LEM (Help → lire la config matérielle).
2. Brancher le 600D, vérifier qu’il apparaît ([KI-007](known-issues.md)).
3. **Si LEM ne part pas** : le 600D passe en intervallomètre / manuel, comme le 100D.

Ne pas copier un script SEM en changeant le nom de l’application : contacts (`P1`/`U1`/`MAX`/`SET`), calculatrice d’exposition et liste APN sont ceux de LEM. Les exemples livrés `basic.txt` / `deluxe.txt` visent une **totalité** ([KI-018](known-issues.md)) — copie locale : [`scripts/lem/`](../scripts/lem/). Le bench 600D est [`bench-rampe-7x2ev.txt`](../scripts/lem/essais-2026/bench-rampe-7x2ev.txt) (nom APN **`600D-T150`**, 15-85 @ f/5,6 ; à copier dans `~/Documents/Scripts Lunar Eclipse Maestro/` sur le Mac). Optique muette au télescope : [KI-019](known-issues.md).

---

## 4. Cadrage (simulateur)

Noyau géométrique validé sur l’éclipse solaire : [methode-fov.md](methode-fov.md).

```bash
.venv/bin/python scripts/simulate_fov.py \
  --config scripts/config/tournefeuille-600d.yaml \
  --out output/fov

.venv/bin/python scripts/simulate_fov.py \
  --config scripts/config/tournefeuille-100d-24mm.yaml \
  --out output/fov
```

- Pointage 600D = **Lune** au MAX (suivi EQ, pas le simulateur fixe).
- 100D forme A = **24 mm**, composition `horizon_thirds` ([DEC-017](decisions.md)) :
  à **04:52:44**, Lune tangente au bord haut, 20 % depuis la gauche.
- Overlay = disque lunaire + umbra/pénombre (pas croissant solaire).
- Fenêtre longue autour du MAX (P1 → moonset).

Détail numérique : [tournefeuille-2026.md](lieux/tournefeuille-2026.md).

---

## 5. Formes (étude — DEC-010)

Voir [formes-prise-de-vue.md](formes-prise-de-vue.md). En résumé : **forme C** (600D, 750 mm ± 1,4×, HDR) + **forme A** (100D @ **24 mm**, time-lapse AEB, horizon au tiers — [DEC-017](decisions.md)). LEM plutôt sur le 600D. Si le test 2 APN (`100D-W24`) est OK, le 100D peut passer sous LEM pour **suivre l’aube** (3 vues puis 5, pas un 7 × 2 EV — [DEC-018](decisions.md)) ; sinon AEB + cran M ~06:40. Au MAX le Soleil est encore à −11° : l’umbra n’est pas noyée dans l’aube ([KI-014](known-issues.md)). Les 11,5 EV DxO du 600D **ne remplacent pas** le HDR disque ([formes §11](formes-prise-de-vue.md) : SNR labo ≠ dynamique propre ; croissant qui clippe ; fenêtre glissante ; span = (n−1)×pas).

Volume ([formes §13](formes-prise-de-vue.md), [DEC-011](decisions.md), [DEC-014](decisions.md)) : **100D en JPEG Fine**, intervalle **90 s** ; **600D en RAW** sur **32 Go** (fenêtre ~04:20 → 07:20). Rampe 7 × 2 EV **~20–25 s** sous LEM ; 16 Go = filet **~65 rampes**. Le RAW AEB 100D sur 3 h **ne tient pas** en 16 Go ([KI-016](known-issues.md)). Pico 32 Go **80 Mo/s** vs 16 Go **95 Mo/s** : pas de re-calage des 3 s (bus 600D ≪ 80). **Swap LP-E8 10 min** vers 05:40 ([KI-022](known-issues.md)).

ISO **800 sur les poses longues seulement** ([DEC-013](decisions.md)) : vues 1–5 à 100/200 (à U1, 1/4000 @ 800 **clippe** le limbe, [KI-017](known-issues.md)). Rampe **7 vues** le plus souvent ; **étendue sombre** (9 vues) aux instants clés ; **3–5 vues** en pénombre (~04:20) ; **7 → 5 → 3** après 06:44. Au MAX, après l’étendue 9 : rampes diagnostic **ISO 100** puis **ISO 1600** ([DEC-015](decisions.md)) — pas un second HDR. Incremental **N** (Tv+Av+ISO) en tête des étendues et de chaque rampe MAX ([DEC-016](decisions.md)). Carte dans le boîtier, on jette après.

Monture 600D : **taux Lune**, pas sidéral ([KI-008](known-issues.md)). Mise en station au viseur polaire **avant 04:20**. Le script séance rappellera ça à voix haute (`say` courts à ~1 s, [KI-021](known-issues.md)).

**Déclenchement manuel dédié au MAX** sur le 600D ([KI-010](known-issues.md)), même si LEM tourne.

Le plan d’exposition lunaire (rampe umbra, calculatrice Jubier / Espenak) n’est **pas** le `chapelet_exposure.py` solaire (ND + extinction du disque).

---

## 6. Checklist minimale avant le 28 août

**Jour J (téléphone) :** [checklist-tournefeuille-2026.html](checklist-tournefeuille-2026.html) —
hors ligne, cases mémorisées, compte à rebours. Copier sur le téléphone et l’ouvrir **avant**
la nuit (comme Frías le 12 août).

- [x] Commune / GPS renseignés, YAML recalé, FOV relancé (Tournefeuille)
- [ ] Horizon ouest–sud-ouest dégagé (moonset, azimut ~257°)
- [ ] Optiques confirmées (focale wide U1→moonset)
- [ ] Test LEM sur le Mac (démarrage + USB 600D) ; charger le bench rampe [`scripts/lem/essais-2026/`](../scripts/lem/essais-2026/)
- [ ] **Test 2 APN** `600D-T150` + **`100D-W24`** (scénario simple, [DEC-018](decisions.md) ; allumage tardif [KI-023](known-issues.md)) — avant tout script aube 100D
- [ ] Monture 750 mm en **taux Lune** (pas sidéral) ; station polaire **avant 04:20**
- [ ] Intervallomètre 100D + piles ; AEB vérifié en mode M (**repli** si LEM ne voit pas le 100D)
- [ ] Plan B 600D sans LEM (intervallomètre ou manuel)
- [ ] Cartes formatées (100D **JPEG Fine** 16 Go, 600D **RAW 32 Go** ; 16 Go 600D = filet) ; 2 accus / boîtier ; **swap 600D prévu ~05:40** ; horloges
