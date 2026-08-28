#!/usr/bin/env python3
"""Generate the interlaced dual-USB LEM session (600D + 100D).

Output: scripts/lem/essais-2026/seance-2apn-interlace.txt

600D TAKEPIC times are those of seance-600d-t150.txt (never shifted).
100D cycles slide by at most 60 s or are skipped so that no exposure overlaps
another body, with INTER_CAM_GAP_S after (pose + USB).
"""

from __future__ import annotations

import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from generate_lem_seance import (  # noqa: E402
    CAMERA as CAM_600D,
    Line,
    command_say,
    render_line,
    session_busy_windows,
    session_lines as session_lines_600d,
)
from generate_lem_seance_100d import (  # noqa: E402
    CAMERA as CAM_100D,
    POWER_MARGIN,
    Cycle,
    announce_lines as announce_100d,
    emit_cycle,
    nominal_starts,
    place_cycles,
)

OUTPUT_PATH = ROOT / "scripts" / "lem" / "essais-2026" / "seance-2apn-interlace.txt"

# After camera A's (shutter + USB 1.1 s), wait this long before camera B.
# Same-timestamp TAKEPIC are skipped by LEM (KI-020), even across bodies.
# Dual-USB bench survived overlap; day-J script does not rely on that.
INTER_CAM_GAP_S = 2.0
MAX_SHIFT = timedelta(seconds=60)


def same_second(a: datetime, b: datetime) -> bool:
    return int(a.timestamp()) == int(b.timestamp())


def command_busy(lines: list[Line]) -> list[tuple[datetime, datetime]]:
    """1 s windows so a 100D TAKEPIC never shares a timestamp with a say."""
    windows: list[tuple[datetime, datetime]] = []
    for line in lines:
        if line.action == "COMMAND":
            windows.append((line.when, line.when + timedelta(seconds=1)))
    return windows


def uniquify_commands(lines_600: list[Line], lines_100: list[Line]) -> list[Line]:
    """Keep 600D times; slide 100D say lines onto free seconds."""
    used = {int(line.when.timestamp()) for line in lines_600}
    used.update(
        int(line.when.timestamp())
        for line in lines_100
        if line.action == "TAKEPIC"
    )
    adjusted: list[Line] = []
    for line in lines_100:
        if line.action != "COMMAND":
            adjusted.append(line)
            continue
        when = line.when
        step = timedelta(seconds=1)
        while int(when.timestamp()) in used:
            when += step
        used.add(int(when.timestamp()))
        adjusted.append(command_say(when, spoken_from(line)) if when != line.when else line)
    return adjusted


def pic_camera(line: Line) -> str:
    return line.rest.split(",", 1)[0]


def merge_lines(lines_600: list[Line], lines_100: list[Line]) -> list[Line]:
    adjusted = uniquify_commands(lines_600, lines_100)
    combined = lines_600 + adjusted
    combined.sort(key=lambda line: (line.when, line.action == "TAKEPIC"))
    pics = [line for line in combined if line.action == "TAKEPIC"]
    for previous, current in zip(pics, pics[1:], strict=False):
        if same_second(previous.when, current.when):
            raise RuntimeError(
                f"TAKEPIC collision at {current.when}: "
                f"{pic_camera(previous)} vs {pic_camera(current)}"
            )
    return combined


def spoken_from(line: Line) -> str:
    marker = ';say "'
    if marker not in line.rest:
        raise ValueError(f"not a say line: {line.rest!r}")
    return line.rest.split(marker, 1)[1].rstrip('"')


def session_bundle() -> tuple[list[Line], list[Cycle]]:
    lines_600 = session_lines_600d()
    busy = session_busy_windows() + command_busy(lines_600)
    cycles = place_cycles(busy, INTER_CAM_GAP_S, MAX_SHIFT)
    lines_100: list[Line] = announce_100d(cycles)
    for cycle in cycles:
        lines_100.extend(emit_cycle(cycle))
    return merge_lines(lines_600, lines_100), cycles


def header(n_600: int, n_100: int, n_cycles: int, n_nominal: int) -> str:
    skipped = n_nominal - n_cycles
    return f"""#
# LEM -- seance entrelacee 600D + 100D. Usage personnel.
# Tournefeuille 28 aout 2026. Copier vers
# ~/Documents/Scripts Lunar Eclipse Maestro/ puis Fichier -> Charger script...
#
# Noms Configuration materielle (casse exacte) :
#   {CAM_600D}  -- RAW, foyer 150 mm, Av USB 5.6
#   {CAM_100D}   -- JPG-F, 24 mm, Av 4.0
#
# 600D : horodatages = seance-600d-t150.txt (jamais decales). Prioritaire.
# 100D : grille 90 s DEC-018 ; glisse <= {int(MAX_SHIFT.total_seconds())} s ou saute
#   si chevauchement. Ecart inter-boitiers : pose + USB 1.1 s + {INTER_CAM_GAP_S:.0f} s
#   (DEC-019). Pas deux TAKEPIC a la meme seconde (KI-020).
# Allumage 100D : say puis {int(POWER_MARGIN.total_seconds())} s (KI-025).
# Incremental N en tete de rampe / cycle ; 100D aussi si pose >= 1 s.
# say courts ASCII, +1 s, <= 60 car. (KI-021). Pas une annonce par rampe.
#
# ~{n_600} CR2 + {n_100} JPG ({n_cycles} cycles 100D, {skipped} sautes
#   sur {n_nominal} nominaux). Regenerer :
#   .venv/bin/python scripts/generate_lem_seance_interlace.py
#

#Action,Date/Ref,Offset sign,Time (offset),Camera,Exposure,Aperture,ISO,MLU,Quality,Size,Incremental,Comment
"""


def render_script() -> str:
    lines, cycles = session_bundle()
    n_600 = sum(1 for line in lines if line.action == "TAKEPIC" and CAM_600D in line.rest)
    n_100 = sum(1 for line in lines if line.action == "TAKEPIC" and CAM_100D in line.rest)

    chunks = [header(n_600, n_100, len(cycles), len(nominal_starts()))]
    previous = ""
    for line in lines:
        marker = "say"
        if line.action == "TAKEPIC":
            marker = line.rest.split(",")[-1].split(" ", 1)[0]
        if marker != previous and line.action == "TAKEPIC":
            chunks.append(f"\n# --- {marker} {line.when.strftime('%H:%M:%S')} ---\n")
            previous = marker
        chunks.append(render_line(line) + "\n")
    return "".join(chunks)


def write_script(path: Path = OUTPUT_PATH) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_script(), encoding="ascii")
    return path


def main() -> None:
    written = write_script()
    lines, cycles = session_bundle()
    n_600 = sum(1 for line in lines if line.action == "TAKEPIC" and CAM_600D in line.rest)
    n_100 = sum(1 for line in lines if line.action == "TAKEPIC" and CAM_100D in line.rest)
    print(
        f"{written.relative_to(ROOT)} "
        f"({n_600} CR2 + {n_100} JPG, {len(cycles)} cycles 100D)"
    )


if __name__ == "__main__":
    main()
