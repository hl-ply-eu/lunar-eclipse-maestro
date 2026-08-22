# lunar-eclipse-maestro — guide agent

Documentation locale et guides pratiques pour [Lunar Eclipse Maestro](http://xjubier.free.fr/en/site_pages/lunar_eclipses/Lunar_Eclipse_Maestro_Photography_Software.html) (LEM),
application **macOS** de Xavier Jubier pour planifier et automatiser la photographie d'éclipses lunaires.

> **Copyright** : l'aide officielle est © Xavier Jubier. Ce dépôt contient une copie locale pour usage
> personnel ; la source authoritative reste le [site en ligne](http://xjubier.free.fr/site_pages/lunar_eclipses/Lunar_Eclipse_Maestro_Help/pgs2/btoc1.html).

Projet frère : [`solar-eclipse-maestro`](../solar-eclipse-maestro/) (éclipses **solaires**, SEM, recette HDR couronne).
Méthodes FOV / trajectoire validées là-bas (Skyfield DE421, projection gnomonique) sont reprises ici — pas le pipeline HDR.

## Architecture

```
lunar-eclipse-maestro/
├── docs/
│   ├── getting-started-2026-france.md  # Guide principal (éclipse 28 août 2026, France)
│   ├── methode-fov.md                  # Noyau géométrique transféré depuis SEM
│   ├── chapelet-lecons-sem.md          # Leçons 100D / intervallomètre (pas le plan d'expo solaire)
│   ├── decisions.md
│   ├── todo.md
│   ├── known-issues.md
│   └── memory/                         # Instantanés par session
├── mirror/
│   ├── index.html                      # Redirection vers le sommaire local
│   ├── MANIFEST.txt                    # Inventaire des pages miroirées
│   └── xjubier.free.fr/.../            # Copie HTML wget
├── output/                             # PDF, HTML consolidé, PNG FOV (générés)
├── scripts/
│   ├── mirror.sh
│   ├── build-pdf.sh + build-pdf.py
│   ├── simulate_fov.py                 # Trajectoire lunaire dans le champ (Skyfield DE421)
│   └── config/paris-600d-placeholder.yaml
├── AGENTS.md
└── .cursor/                            # Rules, skills, commands Cursor
```

| Composant | Rôle |
|-----------|------|
| `docs/getting-started-2026-france.md` | Workflow chronologique LEM pour l'éclipse du 28 août 2026 en France |
| `mirror/` | Aide officielle LEM hors ligne (HTML wget) |
| `scripts/build-pdf.py` | Assemble les pages prioritaires en PDF imprimable |
| `scripts/simulate_fov.py` | Trajectoire de la Lune + ombre umbrale/pénombrale sur capteur fixe |

## Commandes

```bash
# Télécharger / rafraîchir le miroir depuis xjubier.free.fr
./scripts/mirror.sh

# Regénérer le HTML/PDF consolidé (crée .venv/ si absent)
./scripts/build-pdf.sh

# Simulation FOV (placeholder Paris jusqu'au GPS réel)
.venv/bin/python scripts/simulate_fov.py \
  --config scripts/config/paris-600d-placeholder.yaml \
  --out output/fov

# Tests unitaires (géométrie FOV, pas de CR2)
.venv/bin/python -m pytest -q
```

Dépendances Python : `requirements.txt` (installées automatiquement par `build-pdf.sh`).

Le miroir doit être lancé depuis `LunarEclipseMaestroHelp.html` — le répertoire racine du site peut renvoyer 403.

## Mémoire du projet

Injecter explicitement en ouverture de session via `@Files` :

| Fichier | Rôle |
|---------|------|
| `docs/decisions.md` | Décisions techniques actives (DEC-NNN) |
| `docs/todo.md` | Registre En cours / Bloqué / Terminé |
| `docs/known-issues.md` | Bugs et pièges connus (KI-NNN) |
| `docs/memory/` | Instantanés immuables par session |
| `docs/getting-started-2026-france.md` | Guide opérationnel principal |

Clôture de session : `/session-summary`. Reprise : commande `resume-session`.

## Politique de session

| Situation | Action |
|-----------|--------|
| Interruption courte (< 2 h, même tâche) | Reprendre la conversation |
| Lendemain, changement de sous-tâche, > 50 échanges, reprise après congés | Nouvelle session + `@Files` mémoire |
| Travail agent significatif | Branche dédiée — jamais d'agent sur `main` / `master` |

Workflow recommandé pour tâches complexes : **Ask → Plan → Agent**.

## Docs à ignorer

- Contenu HTML du miroir `mirror/xjubier.free.fr/` — copie tierce ; consulter via liens dans le Getting Started ou le PDF consolidé
- Artefacts générés : `.venv/`, `output/` (régénérables)
- `README.md` du dépôt reste l'index humain ; ne remplace pas `docs/decisions.md` ni `docs/todo.md`

## Fichiers à ne pas modifier sans intention explicite

- `mirror/xjubier.free.fr/**` — contenu © Xavier Jubier ; ne modifier que via `mirror.sh`
- `output/lem-help-complet.pdf`, `output/lem-help-print.html` — régénérer plutôt qu'éditer à la main
- `docs/getting-started-2026-france.md` — coordonner les changements matériel / lieu avec l'utilisateur
