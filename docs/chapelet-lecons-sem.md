# Leçons chapelet 100D — ce qui se transfère depuis SEM

Ce n’est **pas** un plan d’exposition lunaire. C’est l’inventaire des leçons Frías (éclipse solaire 12 août 2026, Canon 100D) qui restent vraies sur le **même boîtier** pour un chapelet d’éclipse de Lune.

Source SEM : DEC-013, KI-014, KI-018 ; fiche `docs/lieux/frias-100d-terrain-2026.md` dans `solar-eclipse-maestro`.

---

## Réutiliser tel quel

| Leçon | Détail |
|-------|--------|
| Pas d’intervallomètre interne | Jack 2,5 mm RS-60E3 ; intervallomètre filaire = point de défaillance unique. |
| AEB + intervallomètre | Seul le **retardateur continu « C »** enchaîne le bracket. Rafale : une vue. Retardateur 2 s : une vue (le manuel se trompe). |
| Arithmétique « C » | Nombre de vues = **3 × le réglage** (plage 2–10). Minimum utile **C = 2 → 6 vues**. Un seul cycle AEB est impossible. |
| AEB en mode M | Disponible ; c’est la *correction d’exposition* qui ne l’est pas. En M + ISO fixe, l’AEB fait varier la **vitesse**. |
| AEB effacé à l’extinction | Panne **silencieuse** : 6 vues partent, toutes à la même expo. Effacé aussi par le mode vidéo. Le retardateur « C » survit. Armer l’AEB **en dernier**, ne plus éteindre. |
| Géométrie | Intervalle en diamètres de Lune (SEM : 4 min ≈ 1,83 Ø solaire). Viser ~1,5–2 Ø pour un chapelet lisible. |
| KI-018 / KI-010 ici | **Ne jamais** faire dépendre l’instant critique (totalité solaire alors, **MAX** lunaire maintenant) d’une coïncidence d’horaire. Déclenchement manuel dédié. |

---

## Ne pas copier

- `scripts/chapelet_exposure.py` (SEM) : rescale d’un **filtre ND solaire** + extinction Kasten-Young du **disque solaire** descendant. La Lune n’a pas de ND ; sa dynamique est une rampe umbra de plusieurs EV, pas +2 EV d’airmass.
- Fixation AstroSolar à l’élastique, ND 3,8 vs 5,0.
- Option « retirer le filtre à C2 » (pas de filtre ici).
- Focale 28 mm figée : c’était le max C1→coucher **solaire** à Frías (DEC-010). À Tournefeuille, U1→moonset (~40°) ne tient que vers 18–25 mm sur le 15-85. Le 60 mm f/2,8 et le 70–200 f/4 (DEC-009) servent un chapelet plus court, pas le trajet complet.

---

## Conséquence pour le 28 août

1. Même chaîne 100D : intervallomètre + « C » + AEB, ISO par paliers si besoin.
2. Une pression manuelle au MAX (et autour de U1 si le trou d’intervalle est trop large).
3. Plan d’expo lunaire = session suivante (calculatrice Jubier / tables Espenak), pas un portage du script ND.
