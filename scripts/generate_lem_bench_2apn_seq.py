#!/usr/bin/env python3
"""Generate the sequential dual-USB LEM bench (~12 min, DEC-018 follow-up).

Output: scripts/lem/essais-2026/bench-2apn-seq.txt

Cadence: one ramp every 2 min (same as the 600D session). Bodies alternate;
no late power-on. 100D quality: JPG-F. Shutter speeds = Canon 1/3-stop crans.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from generate_lem_seance import (  # noqa: E402
    CURRENT,
    EXTENDED,
    PENUMBRA,
    Frame,
    format_offset,
    frame,
    ramp_offsets,
)

OUTPUT_PATH = ROOT / "scripts" / "lem" / "essais-2026" / "bench-2apn-seq.txt"

CAM_600D = "600D-T150"
CAM_100D = "100D-W24"
AV_600D = "5.6"
AV_100D = "4.0"
MLU = "0.0"
QUALITY_100D = "JPG-F"
CADENCE = timedelta(minutes=2)
SAY_LEAD = timedelta(seconds=10)

MAX_ANCHOR = datetime(2026, 8, 28, 6, 12, 55)

# DEC-018 placeholders — crans Canon only (1/15 not 1/16 ; 15 s not 16 s).
# Incremental N on every frame with duration >= 1 s (Y failed to apply 16→4, 2026-08-26).
NIGHT_3 = (
    frame("1", 800, "nuit"),
    frame("4", 800, "nuit"),
    frame("15", 800, "nuit"),
)
DAWN_5 = (
    frame("1/15", 800, "aube"),
    frame("1/4", 800, "aube"),
    frame("1", 800, "aube"),
    frame("4", 800, "aube"),
    frame("15", 800, "aube"),
)


@dataclass(frozen=True, slots=True)
class Slot:
    start: datetime
    camera: str
    aperture: str
    quality: str
    frames: tuple[Frame, ...]
    say: str
    tag: str


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


def emit_ramp(slot: Slot) -> list[str]:
    lines = [command_say(slot.start - SAY_LEAD, slot.say)]
    for index, (offset_s, item) in enumerate(
        zip(ramp_offsets(slot.frames), slot.frames, strict=True)
    ):
        comment = f"{slot.tag} {item.shutter} ISO{item.iso}"
        lines.append(
            takepic(
                slot.start + timedelta(seconds=offset_s),
                slot.camera,
                item,
                slot.aperture,
                slot.quality,
                incremental_for(index, item),
                comment,
            )
        )
    return lines


def slots() -> list[Slot]:
    base = MAX_ANCHOR
    return [
        Slot(base + 0 * CADENCE, CAM_600D, AV_600D, "RAW", PENUMBRA, "Rampe 5", "Pen5"),
        Slot(
            base + 1 * CADENCE,
            CAM_100D,
            AV_100D,
            QUALITY_100D,
            NIGHT_3,
            "Trois vues",
            "Nuit3",
        ),
        Slot(base + 2 * CADENCE, CAM_600D, AV_600D, "RAW", CURRENT, "Rampe 7", "Cour7"),
        Slot(
            base + 3 * CADENCE,
            CAM_100D,
            AV_100D,
            QUALITY_100D,
            DAWN_5,
            "Cinq vues",
            "Aube5",
        ),
        Slot(base + 4 * CADENCE, CAM_600D, AV_600D, "RAW", EXTENDED, "Rampe 9", "Etd9"),
        Slot(
            base + 5 * CADENCE,
            CAM_100D,
            AV_100D,
            QUALITY_100D,
            NIGHT_3,
            "Trois vues",
            "Nuit3b",
        ),
    ]


def build() -> str:
    schedule = slots()
    body: list[str] = []
    for slot in schedule:
        body.extend(emit_ramp(slot))
        body.append("")

    last_start = schedule[-1].start
    last_frames = schedule[-1].frames
    last_end = last_start + timedelta(
        seconds=ramp_offsets(last_frames)[-1] + last_frames[-1].duration_s + 5.0
    )
    play = (
        f"PLAY,MAX,+,{format_offset(last_end - MAX_ANCHOR)},"
        f"Max_Eclipse.wav, , , , , , , ,Fin bench 2apn seq"
    )

    n_600 = sum(len(s.frames) for s in schedule if s.camera == CAM_600D)
    n_100 = sum(len(s.frames) for s in schedule if s.camera == CAM_100D)

    header = f"""#
# LEM -- bench sequentiel 2 APN (~12 min). Usage personnel. Pas le script aube.
# Genere par scripts/generate_lem_bench_2apn_seq.py -- ne pas editer a la main.
#
# Noms Configuration materielle (casse exacte) :
#   600D-T150  -- RAW
#   100D-W24   -- JPG-F (pas Fine ; JPG-L = mauvaise lecture)
#
# Cadence 2 min entre departs (comme seance 600D). Une rampe a la fois.
# Vitesses = crans Canon. Incremental N en tete de rampe et si pose >= 1 s.
# Pas d'allumage tardif.
#
# Optique bench : 15-85 diaph electronique (KI-019 si 150 mm muet).
# Mac : Temps simule = MAX moins ~30 s, LAISSER COURIR jusqu'au PLAY (~MAX+10:30).
# Cartes formatees vides. Attendu : {n_600} CR2 (600D) + {n_100} JPG (100D).
# Recopier dans ~/Documents/Scripts Lunar Eclipse Maestro/
# Protocole : essais-2026/README.md
#

#Action,Date/Ref,Offset sign,Time (offset),Camera,Exposure,Aperture,ISO,MLU,Quality,Size,Incremental,Comment

COMMAND,MAX,-,00:00:20.0, , , , , , , , ,Deux APN ;say "Deux APN"
COMMAND,MAX,-,00:00:19.0, , , , , , , , ,Sequentiel ;say "Sequentiel"

"""
    return header + "\n".join(body) + play + "\n"


def main() -> None:
    text = build()
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH.relative_to(ROOT)} ({text.count(chr(10))} lines)")


if __name__ == "__main__":
    main()
