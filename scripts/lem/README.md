# Scripts Lunar Eclipse Maestro — copie Macintosh

Copie locale pour analyse (branche courante), **usage personnel**.

| | |
|--|--|
| **Source** | `/media/fr25262/Pap/Scripts Lunar Eclipse Maestro` (export depuis le Mac, dossier livré avec LEM) |
| **Copié le** | 2026-08-23 |
| **Exclus** | fichiers AppleDouble `._*` (métadonnées macOS) |
| **Droit d’auteur** | scripts d’exemple © Xavier Jubier ; ne pas republier hors usage perso |

Même recette que [`solar-eclipse-maestro/scripts/sem/`](../../../solar-eclipse-maestro/scripts/sem/) : exemples Jubier en racine, essais 2026 dans [`essais-2026/`](essais-2026/).

> Les dates de modification sur le volume sont **anciennes** (15 décembre 2010 — éclipse totale de Lune). Ce n’est **pas** un plan de séance Tournefeuille.

---

## Inventaire

| Fichier | mtime source | Lignes | Rôle |
|---------|--------------|--------|------|
| `basic.txt` | 2010-12-15 | ~121 | Exemple Jubier **lento** ; **totalité** lunaire ; APN `D300` ; MLU 2 s |
| `deluxe.txt` | 2010-12-15 | ~139 | Exemple **agressif** ; totalité + `TAKEBST` / Live View ; carte rapide exigée |

Pas d’équivalent LEM de `Burst_Test.txt` / `Exposure_Ramping_Test.txt` / MMV sur la clé Pap : le dossier livré ne contient que `basic` et `deluxe`.

---

## Pourquoi on ne charge pas `basic` / `deluxe` tels quels

| Point | Lecture |
|-------|---------|
| Totalité | Les deux scripts s’appuient sur **U2 / U3 / MAXPRE / MAXPOST**. Le 28 août 2026 est une **partielle** (pas de U2/U3). |
| Horizon Tournefeuille | **U4 et P4 sous l’horizon** ([fiche lieu](../../docs/lieux/tournefeuille-2026.md)). Les `TAKEPIC,P4,…` et `TAKEPIC,U4,…` sont hors séance. |
| APN | Nom **`D300`** — à remplacer **exactement** par le nom de la Configuration matérielle (`600D-T150`). |
| Expo | Une vitesse par phase (1/160, 1 s, 4 s…), **pas** le protocole 7 × 2 EV (DEC-010 / formes §11). |
| Densité | Boucles `FOR` tous les 1–5 % de magnitude → des centaines de RAW ; incompatible 16 Go / tampon 600D. |
| MLU | 1–2 s par vue (plafonné à 2 s par LEM) : une rampe de 7 vues y passerait ~15 s de miroir **en plus** de l’horloge USB. |

On s’en sert comme **grammaire** (`TAKEPIC`, `FOR`, `PLAY`, `COMMAND`, contacts `P1`/`U1`/`MAX`/`SET`), pas comme scénario jour J.

Script séance : [`essais-2026/seance-600d-t150.txt`](essais-2026/seance-600d-t150.txt) (généré par [`scripts/generate_lem_seance.py`](../generate_lem_seance.py)). Recette [DEC-013](../../docs/decisions.md)–[DEC-016](../../docs/decisions.md) : rampe 7 / étendue 9, ISO **100 / 200 / 800**, **taux Lune**, `COMMAND ;say` **courts à ~1 s** ([KI-021](../../docs/known-issues.md) ; leçon SEM : un message long reste muet).

Aide : [format des scripts](http://xjubier.free.fr/site_pages/lunar_eclipses/Lunar_Eclipse_Maestro_Help/pgs2/btoc6.html) (contacts lunaires, pas `C1`/`C2` solaires). Ne pas porter un script SEM en changeant le nom d’appli.

---

## Benchmark 600D (forme C)

Le premier essai n’est **pas** un plan de séance. C’est le chrono de **une** rampe 7 × 2 EV sous LEM USB (estimation [formes §13](../../docs/formes-prise-de-vue.md) : ~20–25 s).

Fichier : [`essais-2026/bench-rampe-7x2ev.txt`](essais-2026/bench-rampe-7x2ev.txt).

`RAMPUP` existe dans l’aide 1.3.3 (pas 2,0 EV recommandé, mais autorisé). Les exemples officiels sont Nikon D500 + `LVPSTART` ; le **600D n’est pas** dans la liste Live View photo. Le bench jour J reste donc **7 × `TAKEPIC`** (ISO mixte plus tard, que `RAMPUP` ne fait pas).

Références : [Création d’un script](http://xjubier.free.fr/site_pages/lunar_eclipses/Lunar_Eclipse_Maestro_Help/pgs/c1sem47.html) · [Format](http://xjubier.free.fr/site_pages/lunar_eclipses/Lunar_Eclipse_Maestro_Help/pgs2/btoc6.html) · [Getting Started](../../docs/getting-started-2026-france.md) · [KI-018](../../docs/known-issues.md)
