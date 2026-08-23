# Tests pytest — couverture

Suite synthétique (pas de CR2). Lancer :

```bash
.venv/bin/python -m pytest -q
```

| Module | Ce qui est garanti | Ce qui ne l’est pas |
|--------|--------------------|---------------------|
| `tests/test_simulate_fov.py` | Axes ENU, base orthonormée, signe `right` (ouest → nord = droite image), projection au centre capteur, auto-top limbe **lunaire**, rayons umbra > Lune, YAML Tournefeuille | Exactitude des contacts P1/U1 (saisie YAML), overlay Danjon vs Jubier |
| `tests/test_generate_lem_seance.py` | Fichier séance = générateur, ASCII, Av 5,6 / RAW, N en tête de rampe, écarts ≥ 3 s, trou accu, saut MAX+2 min, 5/9/23 vues, cadence 2 min, aube 5→3 | Exécution réelle sous LEM USB |

Le miroir HTML et le PDF ne sont pas testés par pytest.
