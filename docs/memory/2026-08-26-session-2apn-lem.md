# Session 2026-08-26 — dual USB LEM : benches + REX

Branche : `docs/formes-prise-de-vue`. Suite
[2026-08-25-100d-24mm-lem-2apn.md](2026-08-25-100d-24mm-lem-2apn.md).
REX détaillé entrelacé :
[2026-08-26-rex-bench-2apn-interlace.md](2026-08-26-rex-bench-2apn-interlace.md).

## Accompli

- Benches 2 APN : simple (`JPG-F`), séquentiel ~12 min (générateur),
  entrelacé (600D×2 puis 100D @ 20 s, film 20 s @ 25 fps).
- Dumps LEM Propriétés → [`docs/lem/camera-properties/`](../lem/camera-properties/) ;
  référence agent [`lem-apn-scripting.md`](../lem-apn-scripting.md).
- Terrain : passe (a) OK ; seq OK ; interlace **33/33 CR2**, **69/72 JPG**
  (TL01 manqué = allumage tardif).
- Boot LEM validé : sans scénario ; APN à 15–20 s ; charger après
  reconnaissance. Reconnexion 100D ≈ **30 s** → marge **60 s**.
- Idée notée : `say` progression rampe (KI-021, backlog).

Fichiers clés : `generate_lem_bench_2apn_{seq,interlace}.py`,
`bench-2apn*.txt`, KI-024/025, AGENTS / README essais.

Aucun PR (push branche).

## Décisions

Pas de nouveau DEC. DEC-018 : test 2 APN **OK** → script aube débloqué
(sous réserve marge 60 s).

## Pièges

| ID | Sujet |
|----|-------|
| KI-024 | `JPG-F` (pas Fine / JPG-L) ; Tv = enum LEM ; N si pose ≥ 1 s |
| KI-025 | Boot sans scénario ; reconnexion ~30 s |
| KI-021 | Idée `say` « rampe N sur M » en fragments courts |

## Prochaines étapes

1. Marge 60 s dans générateurs aube / interlace
2. Script aube 100D 3→5 (JPG-F, crans LEM)
3. `say` progression de rampe (backlog)
4. Scénario 150 mm f/5 (KI-019) ; rampe serrée &lt; 3 s
