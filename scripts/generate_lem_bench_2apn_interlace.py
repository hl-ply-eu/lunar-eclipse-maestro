#!/usr/bin/env python3
"""Generate an interlaced dual-USB LEM bench.

Output: scripts/lem/essais-2026/bench-2apn-interlace.txt

Timeline:
  1. 600D alone — two ramps (pénombre 5, then courante 7) at 2 min cadence.
  2. 100D joins — 3-view JPG-F brackets every INTERVAL_100D_S seconds
     (film target: 20 s @ 25 fps over U1→moonset ≈ 20 s between keyframes).
  3. 600D continues every 2 min while 100D keeps firing (true USB interlace).

100D Tv are short Canon crans so each 3-bracket fits inside the 20 s slot.
"""

from __future__ import annotations

import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from generate_lem_seance import (  # noqa: E402
    CURRENT,
    PENUMBRA,
    Frame,
    format_offset,
    frame,
    ramp_offsets,
)

OUTPUT_PATH = ROOT / "scripts" / "lem" / "essais-2026" / "bench-2apn-interlace.txt"

CAM_600D = "600D-T150"
CAM_100D = "100D-W24"
AV_600D = "5.6"
AV_100D = "4.0"
MLU = "0.0"
QUALITY_100D = "JPG-F"
CADENCE_600D = timedelta(minutes=2)
SAY_LEAD = timedelta(seconds=10)

# U1 04:33:52 → moonset 07:20:26 CEST ≈ 9974 s (Tournefeuille 2026-08-28).
# 20 s film @ 25 fps → 500 keyframes → 9974/500 ≈ 20.0 s between cycles.
INTERVAL_100D_S = 20.0
# First 100D cycle after the second 600D ramp has finished (~+2:18) + short buffer.
START_100D = timedelta(minutes=2, seconds=40)
# Last 100D cycle start (bench ~12 min wall from MAX).
END_100D = timedelta(minutes=10, seconds=20)

MAX_ANCHOR = datetime(2026, 8, 28, 6, 12, 55)

# Short ±2 EV around 1/15 · ISO 800 — wall time ≪ 20 s.
# Tv ∈ enum LEM 600D/100D (docs/lem-apn-scripting.md) : 1/60, 1/15, 1/4.
BRACKET_3 = (
    frame("1/60", 800, "tl"),
    frame("1/15", 800, "tl"),
    frame("1/4", 800, "tl"),
)


def ref_from_max(when: datetime) -> tuple[str, str]:
    delta = when - MAX_ANCHOR
    sign = "+" if delta.total_seconds() >= 0 else "-"
    return sign, format_offset(delta)


def command_say(when: datetime, spoken: str) -> str:
    sign, offset = ref_from_max(when)
    return (
        f"COMMAND,MAX,{sign},{offset}, , , , , , , , ,"
        f'{spoken} ;say "{spoken}"'
    )


def takepic(
    when: datetime,
    camera: str,
    item: Frame,
    aperture: str,
    quality: str,
    incremental: str,
    comment: str,
) -> str:
    sign, offset = ref_from_max(when)
    return (
        f"TAKEPIC,MAX,{sign},{offset},{camera},{item.shutter},{aperture},"
        f"{item.iso},{MLU},{quality},None,{incremental},{comment}"
    )


def incremental_for(index: int, item: Frame) -> str:
    if index == 0 or item.duration_s >= 1.0:
        return "N"
    return "Y"


def emit_ramp(
    start: datetime,
    camera: str,
    aperture: str,
    quality: str,
    frames: tuple[Frame, ...],
    tag: str,
    say: str | None,
) -> list[str]:
    lines: list[str] = []
    if say is not None:
        lines.append(command_say(start - SAY_LEAD, say))
    for index, (offset_s, item) in enumerate(
        zip(ramp_offsets(frames), frames, strict=True)
    ):
        comment = f"{tag} {item.shutter} ISO{item.iso}"
        lines.append(
            takepic(
                start + timedelta(seconds=offset_s),
                camera,
                item,
                aperture,
                quality,
                incremental_for(index, item),
                comment,
            )
        )
    return lines


def build() -> str:
    base = MAX_ANCHOR
    lines: list[str] = []

    # --- 600D alone (2 ramps), then continues while 100D runs ---
    ramps_600: list[tuple[timedelta, tuple[Frame, ...], str, str]] = [
        (timedelta(0), PENUMBRA, "Pen5", "Rampe 5"),
        (CADENCE_600D, CURRENT, "Cour7a", "Rampe 7"),
        (2 * CADENCE_600D, CURRENT, "Cour7b", "Rampe 7"),
        (3 * CADENCE_600D, CURRENT, "Cour7c", "Rampe 7"),
        (4 * CADENCE_600D, CURRENT, "Cour7d", "Rampe 7"),
    ]
    for offset, frames, tag, say in ramps_600:
        lines.extend(
            emit_ramp(
                base + offset,
                CAM_600D,
                AV_600D,
                "RAW",
                frames,
                tag,
                say,
            )
        )
        lines.append("")

    # --- 100D joins after 2 ramps ---
    lines.append(command_say(base + START_100D - SAY_LEAD, "Cent D"))
    lines.append(command_say(base + START_100D - SAY_LEAD + timedelta(seconds=1), "Time lapse"))
    lines.append("")

    n_100_cycles = 0
    t = START_100D
    while t <= END_100D:
        n_100_cycles += 1
        tag = f"TL{n_100_cycles:02d}"
        say = "Trois vues" if n_100_cycles == 1 else None
        lines.extend(
            emit_ramp(
                base + t,
                CAM_100D,
                AV_100D,
                QUALITY_100D,
                BRACKET_3,
                tag,
                say,
            )
        )
        t += timedelta(seconds=INTERVAL_100D_S)

    lines.append("")
    play_at = base + END_100D + timedelta(seconds=15)
    lines.append(
        f"PLAY,MAX,+,{format_offset(play_at - MAX_ANCHOR)},"
        f"Max_Eclipse.wav, , , , , , , ,Fin bench 2apn interlace"
    )

    n_600 = sum(len(frames) for _, frames, _, _ in ramps_600)
    n_100 = n_100_cycles * len(BRACKET_3)

    header = f"""#
# LEM -- bench entrelace 2 APN (~12 min). Usage personnel. Pas le script aube.
# Genere par scripts/generate_lem_bench_2apn_interlace.py -- ne pas editer a la main.
#
# Noms : 600D-T150 (RAW) ; 100D-W24 (JPG-F). Ref : docs/lem-apn-scripting.md
#
# Phase 1 : 600D seul — rampe 5 puis 7 (cadence 2 min).
# Phase 2 : 100D demarre a MAX+{START_100D} ; bracket 3 vues toutes les
#   {INTERVAL_100D_S:.0f} s (cible film 20 s @ 25 fps sur U1->moonset ~9974 s
#   -> 500 keyframes -> pas ~20 s). Tv 1/60 1/15 1/4 (enum LEM) pour le creneau.
# Phase 3 : 600D continue a 4/6/8 min pendant les brackets 100D (USB dual).
#
# Incremental N en tete de rampe / si pose >= 1 s. Pas d'allumage tardif.
# Mac : Temps simule = MAX - 30 s ; laisser courir jusqu'au PLAY (~MAX+10:35).
# Cartes vides. Attendu : {n_600} CR2 + {n_100} JPG ({n_100_cycles} x 3).
# Protocole : essais-2026/README.md
#

#Action,Date/Ref,Offset sign,Time (offset),Camera,Exposure,Aperture,ISO,MLU,Quality,Size,Incremental,Comment

COMMAND,MAX,-,00:00:20.0, , , , , , , , ,Deux APN ;say "Deux APN"
COMMAND,MAX,-,00:00:19.0, , , , , , , , ,Entrelace ;say "Entrelace"

"""
    return header + "\n".join(lines) + "\n"


def main() -> None:
    text = build()
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH.relative_to(ROOT)} ({text.count(chr(10))} lines)")


if __name__ == "__main__":
    main()
