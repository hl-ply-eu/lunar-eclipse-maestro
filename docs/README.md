# Documentation Lunar Eclipse Maestro

Ressources locales dérivées de l’[aide officielle](http://xjubier.free.fr/site_pages/lunar_eclipses/Lunar_Eclipse_Maestro_Help/pgs2/btoc1.html) de Xavier Jubier.

## Guides

- **[Getting Started — éclipse 28 août 2026, France](getting-started-2026-france.md)**  
  Premier parcours LEM : contraintes macOS, duo 600D/100D, cadrage, chapelet.
- **[Méthode FOV / trajectoire](methode-fov.md)**  
  Noyau Skyfield DE421 + projection gnomonique transféré depuis SEM ; overlay ombre.
- **[Leçons chapelet 100D (SEM)](chapelet-lecons-sem.md)**  
  Ce qui se réutilise (AEB, intervallomètre, KI-018) ; ce qui ne se copie pas (ND solaire).
- **[Tournefeuille 2026](lieux/tournefeuille-2026.md)**  
  GPS, contacts UTC/CEST, altitudes Skyfield, cadrage indicatif (DEC-008).
- **[Formes de prise de vue](formes-prise-de-vue.md)**  
  Étude : ambiance, HDR disque, aube, 600D vs 100D (DxO), OM-3 / OM-5 II,
  pourquoi 11,5 EV labo n’éliminent pas la rampe 7 × 2 EV ; ISO 800 décale
  les temps, pas le nombre de vues ; volume (§13) : JPEG 100D vs RAW 600D,
  intervalle ≠ durée de film.

## Mémoire projet

- [Décisions](decisions.md) · [Tâches](todo.md) · [Problèmes connus](known-issues.md) · [memory/](memory/)

## Aide officielle (miroir)

| Format | Fichier |
|--------|---------|
| HTML (navigable) | [../mirror/index.html](../mirror/index.html) |
| PDF consolidé | [../output/lem-help-complet.pdf](../output/lem-help-complet.pdf) |
| HTML imprimable | [../output/lem-help-print.html](../output/lem-help-print.html) |
| Inventaire | [../mirror/MANIFEST.txt](../mirror/MANIFEST.txt) |

```bash
./scripts/mirror.sh
./scripts/build-pdf.sh
```
