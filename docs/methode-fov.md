# Méthode FOV / trajectoire — noyau transféré depuis SEM

Ce document dit **ce qui a été validé** sur l’éclipse solaire (Frías, 12 août 2026) et **ce qui change** pour la Lune. Le code vit dans `scripts/simulate_fov.py` de *ce* dépôt (copie adaptée, pas un import depuis `solar-eclipse-maestro`).

Références SEM : DEC-008, DEC-009, DEC-010 ; [manuel-simulateur-fov.md](../../solar-eclipse-maestro/docs/manuel-simulateur-fov.md) ; bug d’axe `right` corrigé le 2026-07-12.

---

## 1. Ce qui est validé (ne pas réinventer)

### Éphémérides

- **Skyfield** + JPL **DE421** (`de421.bsp` à la racine, sinon téléchargement Skyfield).
- Positions **apparentes** topocentriques : `observer.at(t).observe(body).apparent()`.
- Réfraction : température / pression du YAML (`altaz(temperature_C=..., pressure_mbar=...)`).

### Géométrie caméra

1. Alt/Az (degrés) → vecteur unitaire **ENU** (Est, Nord, Zénith) :

   - \(E = \cos a \sin A\), \(N = \cos a \cos A\), \(U = \sin a\).

2. Base caméra « droite, haut = zénith projeté », **main droite** :

   - `forward` = direction de visée ;
   - `up` = zénith projeté sur le plan tangent ;
   - **`right = forward × up`**.

   L’inverse (`up × forward`) **miroite** la trajectoire gauche/droite. Confirmé en session SEM : un coucher ouest, hémisphère nord, doit descendre **vers la droite** (nord azimutal) dans l’image.

3. Projection **gnomonique** : \(x = (t \cdot r) / (t \cdot f)\), \(y = (t \cdot u) / (t \cdot f)\) ; refusé si \(t \cdot f \le 0\) (derrière la caméra).

4. Plan tangent → pixels :

   - \(x_\mathrm{mm} = f \cdot x_\mathrm{tan}\), \(y_\mathrm{mm} = f \cdot y_\mathrm{tan}\) ;
   - \(x_\mathrm{px} = W/2 + x_\mathrm{mm} \cdot W / w_\mathrm{capteur}\) ;
   - \(y_\mathrm{px} = H/2 - y_\mathrm{mm} \cdot H / h_\mathrm{capteur}\) (**y image vers le bas**).

5. Rayon angulaire → pixels : \(r_\mathrm{mm} = f \tan\rho\), puis \(\times\) px/mm moyen.

### Capteur

Canon 600D et 100D : **22,3 × 14,9 mm**, 5184 × 3456 px. Même FOV en degrés pour une focale donnée — pas de re-mesure.

### Cadrage

- `framing.pointing_event` = n’importe quelle clé de `eclipse.contacts_local` (pas seulement un contact). SEM s’en est servi pour une visée `tl60_aim` hors C2/MAX/C3.
- Auto-top : limbe inférieur (côté horizon, \(y + r\)) au bord haut \(y = 0\) ; sinon fallback « instant le plus proche ».
- Fenêtre large + visée personnalisée pour un time-lapse C1→événement (DEC-009/010). Ici : analogie **U1→moonset**.

### Dérive

~15″/s sidéral. À 280 mm APS-C : **~4,5 px/s**. Pose umbra 1–4 s → 5–18 px de filé sans suivi (KI-008).

---

## 2. Ce qui change pour la Lune

| SEM (Soleil) | LEM (Lune) |
|--------------|------------|
| Cible = Soleil centré à MAX / visée custom | Cible = **Lune** |
| Contacts C1 C2 MAX C3 C4 SET | **P1 U1 MAX U4 P4 SET** (moonset) |
| Overlay croissant (disque solaire − Lune) | Overlay **Lune + umbra + pénombre** |
| Anneaux de couronne \(n R_\odot\) | Pas de couronne |
| Fenêtre ±15 min autour de MAX (télé) | Fenêtre **heures** (P1 → moonset) |
| Validation alt/az sur le Soleil | Validation sur la **Lune** |

### Ombres (visualisation, pas les contacts officiels)

Les instants P1/U1/MAX/U4/P4 viennent du YAML (éphémérides Jubier / canon). L’overlay est un **cône géométrique** Terre–Soleil à la distance lunaire, élargissement **Danjon 2 %** (standard des prédictions d’éclipses lunaires) :

- axe de l’ombre ≈ **anti-Soleil** topocentrique : altitude \(-a_\odot\), azimut \(A_\odot + 180^\circ\) ;
- rayons umbra / pénombre : \(\mathrm{atan}(r_\mathrm{cône} / D_\mathrm{Lune})\).

Suffisant pour un schéma de cadrage. Ne pas s’en servir pour publier des contacts.

### Convention d’image

Inchangée : \(x\) vers la droite, \(y\) vers le bas. Lune en descente vers l’ouest, hémisphère nord : trajectoire globalement **descendante vers la droite**.

---

## 3. Configuration et commande

Fichier : `scripts/config/paris-600d-placeholder.yaml` (KI-005).

```bash
.venv/bin/python scripts/simulate_fov.py \
  --config scripts/config/paris-600d-placeholder.yaml \
  --out output/fov
```

`--optic` est répétable (nom YAML exact).

Pour un autre site : copier le YAML, GPS, fuseau, `contacts_local` (surtout `set`), points `validation_altaz_deg` après un premier run.

Tests du noyau (axes ENU, base orthonormée, signe `right`, projection au centre, auto-top limbe lunaire) :

```bash
.venv/bin/python -m pytest -q tests/test_simulate_fov.py
```
