# Lunar Eclipse Maestro — documentation locale

Copie locale et guides pratiques pour [Lunar Eclipse Maestro](http://xjubier.free.fr/en/site_pages/lunar_eclipses/Lunar_Eclipse_Maestro_Photography_Software.html) (LEM), l’application macOS de Xavier Jubier pour planifier et automatiser la photographie d’éclipses lunaires.

> **Copyright** : la documentation officielle est © Xavier Jubier. Ce dépôt contient une **copie locale pour usage personnel** ; la source authoritative reste le [site en ligne](http://xjubier.free.fr/site_pages/lunar_eclipses/Lunar_Eclipse_Maestro_Help/pgs2/btoc1.html).

## Contenu

| Ressource | Description |
|-----------|-------------|
| [Getting Started — 28 août 2026, France](docs/getting-started-2026-france.md) | Guide de découverte LEM, duo Canon 600D + 100D |
| [Méthode FOV](docs/methode-fov.md) | Noyau géométrique transféré depuis SEM (DE421, gnomonique) |
| [Leçons chapelet 100D](docs/chapelet-lecons-sem.md) | AEB, intervallomètre, pas de coïncidence horaire |
| [Miroir HTML](mirror/index.html) | Aide complète LEM, navigable hors ligne |
| [PDF consolidé](output/lem-help-complet.pdf) | Manuel imprimable (généré) |
| [Inventaire](mirror/MANIFEST.txt) | Liste des pages miroirées |

## Démarrage rapide

1. Lisez le [Getting Started](docs/getting-started-2026-france.md).
2. Consultez l’aide via le [miroir HTML](mirror/index.html) (après `./scripts/mirror.sh`).

## Mettre à jour la documentation

```bash
./scripts/mirror.sh
./scripts/build-pdf.sh
```

Le miroir doit être lancé depuis `LunarEclipseMaestroHelp.html`.

## Structure

```
lunar-eclipse-maestro/
├── docs/           # Guides pratiques et mémoire projet
├── mirror/         # Copie HTML de l'aide officielle
├── output/         # PDF, HTML consolidé, PNG FOV
└── scripts/        # mirror, PDF, simulate_fov
```

## Matériel visé par le Getting Started

- Éclipse **lunaire quasi-totale du 28 août 2026** (magnitude umbrale 0,93), **France**
- **Canon EOS 600D** + 70–200 mm f/4 + extender ×1,4 (280 mm)
- **Canon EOS 100D** + EF-S 15-85 mm (chapelet paysage) — focale à repréciser (28 mm trop long pour U1→moonset)
- Site : **Tournefeuille** (43,582389° N, 1,350944° E) — [fiche](docs/lieux/tournefeuille-2026.md)

## Projet frère

[`solar-eclipse-maestro`](../solar-eclipse-maestro/) — Solar Eclipse Maestro, éclipse solaire 12 août 2026, recette HDR couronne. Périmètres distincts.
