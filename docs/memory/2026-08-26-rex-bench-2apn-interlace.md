# Session 2026-08-26 — REX bench 2 APN entrelacé + allumage tardif

Branche : `docs/formes-prise-de-vue`. Suite benches DEC-018.

## Protocole de démarrage LEM (validé ce soir)

LEM doit démarrer **sans scénario chargé**. Reconnaissance dual USB OK si :

1. Allumer les APN **l’un après l’autre**, espacés de **15–20 s**
2. Lancer LEM **sans** script
3. Attendre que les deux icônes soient reconnues
4. **Puis** charger le scénario (⌘L)

## Bench `bench-2apn-interlace.txt`

Cartes formatées ; run ~20:50–23:01 CEST (horloges boîtiers).

| | Attendu | Obtenu |
|--|---------|--------|
| 600D | 33 CR2 (5+7×4) | **33 CR2** `7723`–`7755` |
| 100D | 72 JPG (24×3) | **69 JPG** `7537`–`7605` (**−1 cycle**) |

**600D :** rampes à +0 / +2:00 / +4:00 / +6:00 / +8:00 (±0,3 s). Tv/ISO OK. Chevauchement USB avec 100D aux +4/+6/+8 : 7 CR2 + ~8 JPG dans ±25 s — **tenu**.

**100D :** JPG-F ; Tv exacts `1/60` · `1/15` · `1/4` · ISO 800 ; cadence t₀ cycles **20,00 s** (19,56–20,31).

### Allumage tardif (volontaire)

- `say` « Cent D » : MAX+**150** s
- Power-on : **1–2 s après** le say (~MAX+151–152 s)
- Premier JPG : MAX+**180,33** s = script **TL02** (pas TL01)

| Grandeur | Valeur |
|----------|--------|
| Latence say → 1ʳᵉ vue | **~30,3 s** |
| Latence power-on → 1ʳᵉ vue | **~29 s** |
| Manqué | **TL01** entier (3 JPG, créneau +2:40…+2:46) |
| Reprise stable | TL02→TL24 (23 cycles) |

Marge séance proposée : **≥ 45 s** (cible **60 s**) entre allumage 100D et premier `TAKEPIC` ; `say` assez tôt. Incremental **N** au premier cliché après USB ([KI-023](../known-issues.md), [KI-025](../known-issues.md)).

## Décisions / docs

- [KI-025](../known-issues.md) : ordre démarrage LEM + délai reconnexion ~30 s
- [lem-apn-scripting.md](../lem-apn-scripting.md) : check-list boot
- Pas de nouveau DEC (calage marge script aube = prochaine itération générateur)

## Prochaines étapes

1. Reporter **60 s** de marge dans le générateur aube / interlace (`say` puis trou avant 1ʳᵉ vue 100D)
2. Script aube 3→5 (DEC-018) maintenant que dual + JPG-F + entrelacement OK
3. Scénario 150 mm f/5 (KI-019) ; passe (b) formelle bench-2apn si besoin
4. Optionnel : re-mesurer délai reconnexion à froid vs chaud
