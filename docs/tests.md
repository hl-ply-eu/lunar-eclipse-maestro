# Tests pytest — couverture

Suite synthétique (pas de CR2). Lancer :

```bash
.venv/bin/python -m pytest -q
```

| Module | Ce qui est garanti | Ce qui ne l’est pas |
|--------|--------------------|---------------------|
| `tests/test_simulate_fov.py` | Axes ENU, base orthonormée, signe `right` (ouest → nord = droite image), projection au centre capteur, auto-top limbe **lunaire**, rayons umbra > Lune, YAML placeholder | Exactitude des contacts P1/U1 (YAML), overlay Danjon vs Jubier, moonset réel hors Paris |

Le miroir HTML et le PDF ne sont pas testés par pytest.
