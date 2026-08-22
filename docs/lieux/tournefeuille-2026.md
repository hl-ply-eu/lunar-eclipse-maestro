# Tournefeuille — 28 août 2026

Site retenu pour l’éclipse lunaire quasi-totale (DEC-008).
Optiques encore **provisoires** (DEC-007) — à repréciser.

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

## Cadrage (indicatif, optiques à repréciser)

Trajet angulaire **U1 → moonset ≈ 39,7°** (beaucoup plus long que C1→SET solaire à Frías).

**600D-Tele** (70–200 + ×1,4 @ 280 mm, pointage MAX) :

- Lune entière dans le cadre ~**16 min** (06:05–06:21 CEST).
- Auto-top limbe ~**06:01:28** CEST.
- Un cadrage unique ne couvre pas U1 ni le coucher : recentrages ou second corps de séance.

**100D-Wide** (EF-S 15-85, marges ≥ 10 % sur le disque, APS-C paysage) :

| Pointage | Focale max ≥ 10 % | 24 mm | 28 mm |
|----------|-------------------|-------|-------|
| MAX (06:12:55) | **21 mm** | limbe haut ~5 % | sort du cadre |
| Milieu U1–SET (05:57:09) | **25 mm** | OK (~12 % vertical) | marge verticale ~6 % |

28 mm (réglage solaire Frías) **ne tient pas** U1→moonset ici. Ne pas figer 18 / 21 / 24 mm
tant que le jeu d’optiques n’est pas confirmé.

## Commandes

```bash
.venv/bin/python scripts/simulate_fov.py \
  --config scripts/config/tournefeuille-600d.yaml \
  --out output/fov

.venv/bin/python scripts/simulate_fov.py \
  --config scripts/config/tournefeuille-100d-u1-set.yaml \
  --out output/fov
```
