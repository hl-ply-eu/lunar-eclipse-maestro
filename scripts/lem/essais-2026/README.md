# Essais scripts LEM — août 2026

Scripts écrits dans ce dépôt (pas un export Mac). À copier vers
`~/Documents/Scripts Lunar Eclipse Maestro/` sur le MacBook Pro 2012, puis
**Fichier → Charger script…**

| | |
|--|--|
| **Noms APN** | `600D-T150` (télescope 150 mm) ; candidat 100D **`100D-W24`** (wide 24 mm) — matcher **exactement** la Configuration matérielle (casse, tiret) |
| **Éclipse** | 28 août 2026, lieu Tournefeuille (fuseau **UTC+2**, CEST) |
| **Optique du bench** | EF-S **15-85 mm @ f/5,6** (diaphragme électronique). Le télescope 150 mm f/5 est le corps de séance ; optique **muette** = [KI-019](../../../docs/known-issues.md). |

## Mapping

| Fichier local | Rôle | APN |
|---------------|------|-----|
| `bench-rampe-7x2ev.txt` | Chrono d’**une** rampe 7 × 2 EV (forme C) | `600D-T150` |
| `bench-2apn.txt` | Test **simple** deux USB (DEC-018) ; pas l’aube | `600D-T150` + `100D-W24` |
| `seance-600d-t150.txt` | Séance 04:20 → moonset (généré) | `600D-T150` |

Script séance : [DEC-013](../../../docs/decisions.md)–[DEC-016](../../../docs/decisions.md). Régénérer :

```bash
.venv/bin/python scripts/generate_lem_seance.py
```

- ~04:20 : rampe **5 vues** (pleine Lune) ; rappel oral **taux Lune** ;
- cadence **2 min ancrée sur MAX** ;
- U1 → ~06:40 : rampe **7** ; **étendue 9** à U1+10, ~50 %, MAX, **06:30** (4ᵉ HDR umbra, pas le bloc MAX) ;
- au **MAX**, après l’étendue 9 : rampes diagnostic **ISO 100** (→ 4 s) puis **ISO 1600** (1/4000 → 1 s), ~10 s de vidage entre les trois ([DEC-015](../../../docs/decisions.md)) ; saut MAX+2 min ;
- Incremental **N** en tête de **chaque** rampe ; Y ensuite ; écarts ≥ 3 s, tampon 5 ([DEC-016](../../../docs/decisions.md)) ;
- ~05:40–05:55 : trou **10 min**, `say`, reprise 05:56:55 Incremental **N** ([KI-022](../../../docs/known-issues.md)) ;
- 06:44 → moonset : **5 puis 3** (une vue trop longue gardée par palier) ;
- ISO **100 / 200 / 800** (vues 1–2 / 3–5 / 6–9) ; colonne Av **5,6** (USB) ; expo **f/5** ;
- annonces : plusieurs `COMMAND ;say` **courts**, **+1 s** entre eux, ASCII, ≲ 60 car. ([KI-021](../../../docs/known-issues.md)).

Grammaire (ASCII, ~1 s d’écart) :

```
COMMAND,U1,-,10:00.0, , , , , , , , ,Suivi Lune ;say "Suivi Lune"
COMMAND,U1,-,09:59.0, , , , , , , , ,Pas sideral ;say "Pas sideral"
```

## Test 2 APN — `bench-2apn.txt` (DEC-018)

Pas le script aube. Vérifier que LEM **voit** le 100D et tient deux USB. Nom **`100D-W24`**.

**Passe (a) — les deux allumés.** Configuration matérielle : 600D déjà `600D-T150` ; 100D → nom `100D-W24`, modèle EOS 100D, **Déclencher** une vue. ⌘L `bench-2apn.txt`. Temps simulé **MAX − 40 s**, laisser courir. Compter **3 RAW** 600D + **3 JPEG** 100D. Visualiseur : les six `TAKEPIC` sont là.

**Passe (b) — allumage tardif, sans ⌘R.** Décharger. 100D **éteint**. Recharger le même fichier. Noter si les lignes `100D-W24` restent dans le Visualiseur (souvenir : ignorées au chargement — option non retrouvée dans l’aide, [KI-023](../../../docs/known-issues.md)). Temps simulé MAX − 40 s. Allumer le 100D vers MAX − 15 s. **Ne pas** recharger. Les `TAKEPIC` 100D à −5 / +5 / +20 doivent partir tout seuls (FAQ batterie). Premier cliché : Incremental **N** déjà dans ce bench.

**Passe (c) — ⌘R seulement si (b) est muet.** Une fois l’icône `100D-W24` visible, **Recharger script** hors des `TAKEPIC` 600D (après MAX+10 s, ou nouveau run). Les actions déjà « passées » sont sautées ([KI-020](../../../docs/known-issues.md)).

**Si (a) échoue :** 100D = AEB, ne pas écrire le script aube. Si (a) OK et (b) OK : allumage ~04:15 le jour J tenable. Si (a) OK et (b) KO : allumer le 100D **avant** ⌘L, ou recharger dans un trou.

### `say` cadrage (script aube, **après** ce test)

ASCII, ≲ 60 car., **+1 s** (KI-021). Recette DEC-017, **04:52:44** = U1+18:52 :

```
COMMAND,U1,+,18:50.0, , , , , , , , ,Cadrage Lune ;say "Cadrage Lune"
COMMAND,U1,+,18:51.0, , , , , , , , ,Bord haut ;say "Bord haut"
COMMAND,U1,+,18:52.0, , , , , , , , ,Vingt pct gauche ;say "Vingt pct gauche"
COMMAND,U1,+,18:53.0, , , , , , , , ,Horizon tiers ;say "Horizon tiers"
```

## Résultat 2026-08-23 — `bench-rampe-7x2ev.txt` (espacé 3 s)

Carte SD `EOS_DIGITAL` / `100CANON`, EXIF lus **sur place** (SubSecTimeOriginal). 15-85 @ 15 mm, f/5,6, ISO 100, RAW. Horloge boîtier = **UTC** (Synchroniser LEM).

| Fichier | UTC | t−t₀ (s) | Script | Vitesse | Écart précédent (s) |
|---------|-----|----------|--------|---------|---------------------|
| `IMG_7684.CR2` | 16:56:04.90 | — | 1er essai (MAX+0 collés) | **1/15** | une seule vue (KI-020) |
| `IMG_7685.CR2` | 17:10:18.59 | 0.00 | +0 | 1/1000 | — |
| `IMG_7686.CR2` | 17:10:21.61 | 3.02 | +3 | 1/250 | 3.02 |
| `IMG_7687.CR2` | 17:10:24.60 | 6.01 | +6 | 1/60 | 2.99 |
| `IMG_7688.CR2` | 17:10:27.60 | 9.01 | +9 | 1/15 | 3.00 |
| `IMG_7689.CR2` | 17:10:30.59 | 12.00 | +12 | 1/4 | 2.99 |
| `IMG_7690.CR2` | 17:10:33.59 | 15.00 | +15 | 1 s | 3.00 |
| `IMG_7691.CR2` | 17:10:37.59 | 19.00 | +19 | 4 s | 4.00 |

**7/7 CR2**, vitesses = script. Départs : moyenne des cinq gaps « 3 s » = **3,000 s** (±0,02). Ouverture première→fermeture dernière = **23,000 s** (19 s d’horaire + 4 s). Somme des obturations = 5,34 s. LEM a **respecté l’horloge**, pas le cycle USB 1,1 s (les 3 s laissent ~2,9 s d’inactivité sur les vues courtes). Le minimum USB reste le chiffre Benchmarks, pas ce run.

## Protocole du bench (Mac + 600D USB + 15-85)

Conditions : LEM 1.3.3β1, USB stable, carte **vide** formatée, **RAW**, mode **M**, MAP manuelle sur l’objectif, AEB **off**, flash off, batterie pleine, Image Capture / EOS Utility **fermés** (aide Configuration initiale).

1. Configuration → Configuration matérielle : modèle 600D, nom **`600D-T150`**, case Synchroniser si voulue (hors mesure de durée).
2. Vérifier que le 600D apparaît (KI-007). Bouton **Déclencher** (1/2000 f/8 ISO 200, test intégré LEM) : une vue OK.
3. Fichier → Charger `bench-rampe-7x2ev.txt` (**recharger** après copie ; le nom APN doit être `600D-T150`).
4. Observateur → **Temps simulé…** : **~30 s avant** le MAX (UTC 04:12:55). Ne pas sauter *sur* le MAX ([KI-020](../../../docs/known-issues.md)).
5. **Laisser courir** jusqu’au `PLAY` MAX+30 s (la 7ᵉ vue part à MAX+19 s et dure 4 s).
6. Chronométrer : **premier déclenchement → LED carte éteinte après la 7ᵉ vue**.
   LEM Benchmarks (pose courte) : **1,1 s/vue**. Rampe serrée attendue **~13–16 s** ;
   ce script à 3 s entre départs : **~23 s** jusqu’à la fin de la 4 s.
7. Compter **7 CR2**. EXIF vitesses : 1/1000, 1/250, 1/60, 1/15, 1/4, 1 s, 4 s ; f/5,6. Noter l’analyseur (Temps libre).
8. Observateur → Heure courante (ou Décharger le script) pour arrêter.

Optionnel ensuite (analogue SEM B1–B5) : vidage tampon, Incremental N vs Y, écriture carte, autonomie USB 1 h.

**MLU = 0** exprès : le plafond LEM (2 s) fausserait la mesure. Le jour J on pourra le réactiver à part.

**Après ce chrono :** même script (ou une vue `TAKEPIC` isolée) avec le 600D au foyer du 150 mm — voir KI-019.
