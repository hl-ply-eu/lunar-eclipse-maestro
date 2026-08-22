# Tournefeuille — 28 août 2026

Site retenu pour l’éclipse lunaire quasi-totale (DEC-008).
Parc optique : [DEC-009](../decisions.md). Formes de prise de vue encore à étudier.

## Lieu

| | |
|---|---|
| Commune | Tournefeuille (31170, Haute-Garonne) |
| Point | 43°34′56.6″ N, 1°21′03.4″ E (43,582389° N, 1,350944° E) |
| Quartier (Nominatim) | Rue de Verdun / Belbèze |
| Élévation YAML | **155 m** (approx. plateau ; IGN à affiner si besoin) |
| Fuseau | Europe/Paris (CEST = UTC+2) |
| Horizon critique | Ouest–sud-ouest (azimut moonset ~257°) |

YAML : [`scripts/config/tournefeuille-600d.yaml`](../../scripts/config/tournefeuille-600d.yaml)
(chapelet wide : [`tournefeuille-100d-u1-set.yaml`](../../scripts/config/tournefeuille-100d-u1-set.yaml)).

## Circonstances locales (UTC fournis → CEST)

Contacts **topocentriques** saisis par l’observateur. Skyfield DE421 au même instant
donne l’altitude / azimut ci-dessous (run 2026-08-22).

| Contact | UTC | CEST | Alt Lune | Az | Notes |
|---------|-----|------|----------|----|-------|
| P1 | 01:23:59 | 03:23:59 | 31,6° | 208° | Pénombre |
| O1 / U1 | 02:33:52 | 04:33:52 | 24,5° | 225° | Entrée umbra |
| MAX | 04:12:55 | **06:12:55** | **10,5°** | 245° | ~96 % du disque dans l’umbra |
| Coucher | 05:20:26 | **07:20:26** | −0,05° | 257° | Fin de séance ; U4 n’est pas visible |
| O2 / U4 | 05:52:03 | 07:52:03 | −6,0° | 263° | Sous l’horizon |
| P2 / P4 | 07:01:47 | 09:01:47 | −18,0° | 274° | Sous l’horizon |

Le moonset fourni est cohérent avec DE421 (limbe à ~0°). U4 et P4 sont **après le coucher**.
Le Soleil se lève pendant le moonset (sun alt +0,8° à 07:20) : ciel déjà clair, extinction
et contraste umbra dégradés en fin de run.

## Cadrage (indicatif, DEC-009)

Trajet angulaire **U1 → moonset ≈ 39,7°** (beaucoup plus long que C1→SET solaire à Frías).

**600D + télescope 150 mm f/5 (750 mm), monture équatoriale** — suivi : la Lune reste au centre, l’ombre traverse le disque. `simulate_fov.py` (caméra fixe) **ne s’applique pas** à ce corps. FOV APS-C approx. : 1,70° × 1,14° (750 mm) ; 1,22° × 0,81° (1050 mm) ; 0,85° × 0,57° (1500 mm). Disque lunaire ~0,51°.

**Chapelet trépied fixe** — U1→moonset, marges ≥ 10 %, APS-C paysage, EF-S 15-85 :

| Pointage | Focale max ≥ 10 % | 24 mm | 28 mm | 60 mm | 70–200 |
|----------|-------------------|-------|-------|-------|--------|
| MAX (06:12:55) | **21 mm** | limbe haut ~5 % | sort | sort | sort |
| Milieu U1–SET (05:57:09) | **25 mm** | OK (~12 % vertical) | marge ~6 % | sort | sort |

60 mm et 70–200 restent utiles pour un chapelet **plus court** (autour du MAX) ou avec recentrages — à chiffrer sur la branche « formes de prise de vue ».

Les PNG `output/fov/fov-70-200mm-*.png` datent encore de l’hypothèse Frías 280 mm fixe ; ne pas s’en servir pour le 750 mm suivi.

## Commandes

```bash
.venv/bin/python scripts/simulate_fov.py \
  --config scripts/config/tournefeuille-600d.yaml \
  --out output/fov

.venv/bin/python scripts/simulate_fov.py \
  --config scripts/config/tournefeuille-100d-u1-set.yaml \
  --out output/fov
```
