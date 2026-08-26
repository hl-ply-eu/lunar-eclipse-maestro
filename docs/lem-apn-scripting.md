# Scripts LEM — propriétés APN (600D / 100D)

Référence agent pour écrire des `TAKEPIC` / générateurs. Sources : dumps LEM
*Camera Properties Analysis* du **2026-08-26** (USB réel).

| Dump brut | Fichier |
|-----------|---------|
| `600D-T150` | [camera-properties/600D-T150-lem-properties.txt](lem/camera-properties/600D-T150-lem-properties.txt) |
| `100D-W24` | [camera-properties/100D-W24-lem-properties.txt](lem/camera-properties/100D-W24-lem-properties.txt) |

Rafraîchir : LEM → Configuration matérielle → propriétés / analyse → recopier ici
sous le même nom. L’enum **ouverture** dépend de l’objectif monté au moment du
dump (600D : 15-85 ; 100D : 18-135 dans ces fichiers).

Voir aussi [KI-024](known-issues.md) (qualité / Incremental Y / Tv hors liste).

---

## Noms Configuration matérielle

| Rôle | Nom script (casse exacte) | Modèle LEM |
|------|---------------------------|------------|
| Gros plan / HDR | `600D-T150` | Canon EOS 600D |
| Wide / time-lapse | `100D-W24` | Canon EOS 100D |

Firmware dump : 600D **1.0.3** ; 100D **1.0.0**.

---

## Colonnes script utiles

| Colonne | 600D séance | 100D ambiance |
|---------|-------------|---------------|
| Quality | **`RAW`** | **`JPG-F`** (pas `Fine`, pas `JPG-L`) |
| Size | `None` | `None` |
| Aperture (USB) | `5.6` (foyer 150 mm f/5 → Av script 5,6) | `4.0` (24 mm, DEC-018) |
| Incremental | **N** en tête de rampe ; **Y** ensuite | idem ; **N** aussi si pose ≥ 1 s ou gros saut Tv |
| MLU | `0.0` en bench ; plafond LEM 2 s | `0.0` |

Jetons qualité aide Scripts (`btoc6`) : `RAW`, `JPG-F`, `JPG-N`, `JPG-B`.

ISO communs (enum identique) : `100`, `200`, `400`, `800`, `1600`, `3200`, `6400`,
`12800` (+ `0` = Auto, à éviter en M scripté).

---

## Vitesses d’obturation (enum LEM, 53 crans)

**Identiques** sur 600D et 100D dans les dumps. N’écrire dans un script que des
chaînes de cette liste (sinon voisin Canon ou Tv inchangé — [KI-024](known-issues.md)).

```
100  (souvent Bulb côté PTP — ne pas utiliser comme pose minutée)
30  25  20  15  13  10  8  6  5  4  3.2  2.5  2  1.6  1.3  1
1/1.3  1/1.6  1/2  1/2.5  1/3  1/4  1/5  1/6  1/8  1/10  1/13  1/15
1/20  1/25  1/30  1/40  1/50  1/60  1/80  1/100  1/125  1/160  1/200
1/250  1/320  1/400  1/500  1/640  1/800  1/1000  1/1250  1/1600
1/2000  1/2500  1/3200  1/4000
```

Règles de rédaction :

- Poses longues minutées : max pratique **`30`** ; pas de `16` → utiliser **`15`**
  (ou `13` / `20`).
- Pas de `1/16` → **`1/15`**.
- Préférer `1/2` à `0.5` ; pour 0,8 s / 0,6 s le dump affiche `1/1.3` / `1/1.6`
  (à tester avant une séance si besoin).
- Grille HDR 600D actuelle (`1/1000`…`2`) ⊆ liste.

---

## Ouvertures (enum au dump)

Valeurs Canon ×100 : `3.5` … `22` (`350`…`2200` dans le dump). Scripts : `5.6`,
`4.0`, etc. **Re-dumper** si l’optique change (télescope muet → [KI-019](known-issues.md) ;
l’enum peut différer ou le diaph USB être ignoré).

---

## Check-list avant un nouveau script

1. Nom APN = Configuration matérielle.
2. Quality ∈ {`RAW`, `JPG-F`, …} ; 100D ambiance = `JPG-F`.
3. Chaque Tv ∈ liste ci-dessus.
4. ISO ∈ enum ; Av compatible objectif.
5. Écarts : durée précédente + ~1,1 s USB, ≥ 3 s (≥ 4 s si pose ≥ 1 s).
6. Incremental **N** en tête de rampe et sur poses ≥ 1 s.
7. Régénérer via les scripts `generate_lem_*.py` plutôt qu’éditer le `.txt` à la main
   quand un générateur existe.

## Démarrage LEM dual USB ([KI-025](known-issues.md))

1. Allumer les APN **l’un après l’autre** (15–20 s entre les deux).
2. Lancer LEM **sans scénario**.
3. Attendre les deux icônes reconnues.
4. **Puis** charger le script.

Allumage **en cours de run** : compter **~30 s** avant la 1ʳᵉ vue utile (mesuré 2026-08-26) ; marge script **60 s** recommandée entre power-on et premier `TAKEPIC`.

## Annonces vocales (idée)

Avant chaque rampe / cycle : progression en fragments courts ([KI-021](known-issues.md)), ex. `600D` → `Rampe 12 sur 35` → `7 vues` (pas une seule phrase longue).

Benches : [scripts/lem/essais-2026/README.md](../scripts/lem/essais-2026/README.md).
