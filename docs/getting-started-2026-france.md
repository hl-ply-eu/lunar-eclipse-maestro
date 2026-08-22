# Getting Started — éclipse lunaire du 28 août 2026 (France)

Guide opérationnel pour [Lunar Eclipse Maestro](http://xjubier.free.fr/en/site_pages/lunar_eclipses/Lunar_Eclipse_Maestro_Photography_Software.html) (LEM) et le duo **Canon 600D-Tele + 100D-Wide**.

L’aide officielle (© Xavier Jubier) reste la référence : [miroir local](../mirror/index.html) après `./scripts/mirror.sh`, ou [en ligne](http://xjubier.free.fr/site_pages/lunar_eclipses/Lunar_Eclipse_Maestro_Help/pgs2/btoc1.html).

**Statut :** stub d’initialisation (2026-08-22). Le site GPS n’est pas encore connu ([KI-005](known-issues.md)) — les horaires ci-dessous sont en **CEST** et les altitudes **à Paris**. Recaler dès la commune.

---

## 1. L’événement

Éclipse **lunaire partielle profonde** (quasi-totale) : magnitude umbrale **0,93**. Pas de totalité. Contacts **identiques en UTC** partout ; visibilité locale = altitude + moonset.

| Contact | UTC | CEST (France) | Notes |
|---------|-----|---------------|--------|
| P1 (pénombre) | 01:23:32 | 03:23 | Ombre souvent peu visible au début |
| U1 (ombre) | 02:33:25 | 04:33 | Début de la partielle umbrale |
| MAX | 04:12:55 | **06:12** | ~96 % du disque dans l’umbra |
| U4 | 05:52:13 | 07:52 | Souvent **sous l’horizon** en France |
| P4 | 07:02:03 | 09:02 | Sous l’horizon |

À Paris : Lune ~8° au MAX, moonset ~07:09 CEST. C’est le même régime « objet bas puis coucher » que Frías le 12 août (soleil ~8°).

---

## 2. Matériel visé (DEC-007)

| Boîtier | Optique | Rôle prévu |
|---------|---------|------------|
| **600D-Tele** | 70–200 mm f/4 + ×1,4 → **280 mm** f/5,6 | Gros plan du disque / morsure umbrale |
| **100D-Wide** | EF-S 15-85 mm | Chapelet paysage U1→moonset — **focale à calculer** une fois le site connu (28 mm n’est qu’un souvenir solaire) |

Capteur identique : APS-C 22,3 × 14,9 mm, 5184 × 3456 px. Pas de filtre solaire. Trépieds **fixes** (pas de suivi dans le matériel Frías) → filé ~4,5 px/s à 280 mm ([KI-008](known-issues.md)).

---

## 3. LEM vs réalité Mac (lire avant d’écrire un script)

LEM est **macOS uniquement** ([KI-001](known-issues.md)) et **s’arrête à Mojave** ([KI-006](known-issues.md)). Catalina et suivants : l’auteur indique qu’une réécriture serait nécessaire ; repli = VM Mojave.

Le Mac qui a piloté Solar Eclipse Maestro le 12 août 2026 peut donc **ne pas** lancer LEM. Jusqu’au test :

1. Lancer LEM (Help → lire la config matérielle).
2. Brancher le 600D, vérifier qu’il apparaît ([KI-007](known-issues.md)).
3. **Si LEM ne part pas** : le 600D passe en intervallomètre / manuel, comme le 100D.

Ne pas copier un script SEM en changeant le nom de l’application : contacts (`P1`/`U1`/`MAX`…), calculatrice d’exposition et liste APN sont ceux de LEM.

---

## 4. Cadrage (simulateur)

Noyau géométrique validé sur l’éclipse solaire : [methode-fov.md](methode-fov.md).

```bash
.venv/bin/python scripts/simulate_fov.py \
  --config scripts/config/paris-600d-placeholder.yaml \
  --out output/fov
```

- Pointage = **Lune** à l’événement YAML (`max` par défaut).
- Overlay = disque lunaire + umbra/pénombre (pas croissant solaire).
- Auto-top = limbe lunaire inférieur au bord haut du capteur.
- Fenêtre longue autour du MAX (P1 → moonset), pas ±15 min.

Dès le GPS : copier le YAML, mettre à jour `site.*` et `eclipse.contacts_local.set`, relancer.

---

## 5. Scénarios (à écrire — voir todo.md)

**600D-Tele.** Cadrage unique verrouillé (dérive comme SEM) vs recentrages. Plafond de pose vs filé. Automatisation LEM seulement après test Mac.

**100D-Wide.** Chapelet à l’intervallomètre. Reprendre les leçons AEB ([chapelet-lecons-sem.md](chapelet-lecons-sem.md)) : retardateur « C », AEB armé en dernier. **Déclenchement manuel dédié au MAX** — ne pas miser sur une coïncidence d’intervalle ([KI-010](known-issues.md)).

Le plan d’exposition lunaire (rampe umbra, calculatrice Jubier / Espenak) n’est **pas** le `chapelet_exposure.py` solaire (ND + extinction du disque).

---

## 6. Checklist minimale avant le 28 août

- [ ] Commune / GPS renseignés, YAML recalé, FOV relancé
- [ ] Horizon ouest–sud-ouest dégagé (moonset)
- [ ] Test LEM sur le Mac (démarrage + USB 600D)
- [ ] Intervallomètre 100D + piles ; AEB vérifié en mode M
- [ ] Plan B 600D sans LEM (intervallomètre ou manuel)
- [ ] Cartes formatées, horloges, batterie
