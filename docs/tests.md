# Tests pytest — couverture

Suite synthétique (pas de CR2). Lancer :

```bash
.venv/bin/python -m pytest -q
```

| Module | Ce qui est garanti | Ce qui ne l’est pas |
|--------|--------------------|---------------------|
| `tests/test_simulate_fov.py` | Axes ENU, base orthonormée, signe `right` (ouest → nord = droite image), projection au centre capteur, auto-top limbe **lunaire** (inférieur / supérieur), `horizon_thirds` 24 mm, YAML Tournefeuille | Exactitude des contacts P1/U1 (saisie YAML), overlay Danjon vs Jubier |
| `tests/test_generate_lem_seance.py` | Fichier séance 600D = générateur, ASCII, Av 5,6 / RAW, N en tête de rampe, écarts ≥ 3 s, trou accu, saut MAX+2 min, 5/9/23 vues, cadence 2 min, aube 5→3, `say` ≤ 60 car. | Exécution réelle sous LEM USB |
| `tests/test_generate_lem_seance_100d.py` | 100D JPG-F, 3 puis 5 vues, N si pose ≥ 1 s, pas de Tv `16`, marge allumage 60 s | Idem |
| `tests/test_generate_lem_seance_interlace.py` | 600D horodatages inchangés, pas deux actions à la même seconde, écart inter-boîtiers 2 s, sauts 100D bornés | Idem |

Le miroir HTML et le PDF ne sont pas testés par pytest.
