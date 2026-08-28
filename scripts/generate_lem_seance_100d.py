#!/usr/bin/env python3
"""Generate the LEM session script for the 100D at 24 mm (forme A, DEC-018).

Output: scripts/lem/essais-2026/seance-100d-w24.txt

JPEG Fine, 90 s cadence, 3-view night then 5-view dawn brackets. Tv = Canon
crans only (15 s not 16 s). Power-on say 60 s before the first TAKEPIC.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from generate_lem_seance import (  # noqa: E402
    MOONSET_CEST,
    TZ,
    Frame,
    Line,
    command_say,
    frame,
    ramp_free_at,
    ramp_offsets,
    ref_from_max,
    render_line,
)

OUTPUT_PATH = ROOT / "scripts" / "lem" / "essais-2026" / "seance-100d-w24.txt"

CAMERA = "100D-W24"
APERTURE = "4.0"
MLU = "0.0"
QUALITY = "JPG-F"
INTERVAL = timedelta(seconds=90)
POWER_MARGIN = timedelta(seconds=60)
FIRST_SLOT = datetime(2026, 8, 28, 4, 20, 0, tzinfo=TZ)
FRAME_LOCK = datetime(2026, 8, 28, 4, 52, 40, tzinfo=TZ)
PROGRESS_EVERY = 15

# DEC-018 placeholders — 15 s not 16 s (KI-024). Central night = 4 s · ISO 800.
NIGHT_3 = (
    frame("1", 800, "nuit"),
    frame("4", 800, "nuit"),
    frame("15", 800, "nuit"),
)
# −2 EV vs night: 1/15 … 15 s · 800 (5 × 2 EV).
DAWN_A = (
    frame("1/15", 800, "aube"),
    frame("1/4", 800, "aube"),
    frame("1", 800, "aube"),
    frame("4", 800, "aube"),
    frame("15", 800, "aube"),
)
# −5 EV: 1/60 … 4 s · 800.
DAWN_B = (
    frame("1/60", 800, "aube"),
    frame("1/15", 800, "aube"),
    frame("1/4", 800, "aube"),
    frame("1", 800, "aube"),
    frame("4", 800, "aube"),
)
# −8 EV: 1/250 … 1 s · 400.
DAWN_C = (
    frame("1/250", 400, "aube"),
    frame("1/60", 400, "aube"),
    frame("1/15", 400, "aube"),
    frame("1/4", 400, "aube"),
    frame("1", 400, "aube"),
)
# −11 EV: 1/1000 … 1/4 · 200.
DAWN_D = (
    frame("1/1000", 200, "aube"),
    frame("1/250", 200, "aube"),
    frame("1/60", 200, "aube"),
    frame("1/15", 200, "aube"),
    frame("1/4", 200, "aube"),
)
# −13 EV: 1/4000 … 1/15 · 100.
DAWN_E = (
    frame("1/4000", 100, "aube"),
    frame("1/1000", 100, "aube"),
    frame("1/250", 100, "aube"),
    frame("1/60", 100, "aube"),
    frame("1/15", 100, "aube"),
)

WINDOWS: tuple[tuple[datetime, datetime, tuple[Frame, ...], str, str], ...] = (
    (
        datetime(2026, 8, 28, 4, 20, 0, tzinfo=TZ),
        datetime(2026, 8, 28, 6, 10, 0, tzinfo=TZ),
        NIGHT_3,
        "Nuit3",
        "Trois vues",
    ),
    (
        datetime(2026, 8, 28, 6, 10, 0, tzinfo=TZ),
        datetime(2026, 8, 28, 6, 25, 0, tzinfo=TZ),
        DAWN_A,
        "AubeA",
        "Cinq vues",
    ),
    (
        datetime(2026, 8, 28, 6, 25, 0, tzinfo=TZ),
        datetime(2026, 8, 28, 6, 40, 0, tzinfo=TZ),
        DAWN_B,
        "AubeB",
        "Cinq vues",
    ),
    (
        datetime(2026, 8, 28, 6, 40, 0, tzinfo=TZ),
        datetime(2026, 8, 28, 6, 55, 0, tzinfo=TZ),
        DAWN_C,
        "AubeC",
        "Moins expo",
    ),
    (
        datetime(2026, 8, 28, 6, 55, 0, tzinfo=TZ),
        datetime(2026, 8, 28, 7, 10, 0, tzinfo=TZ),
        DAWN_D,
        "AubeD",
        "Moins expo",
    ),
    (
        datetime(2026, 8, 28, 7, 10, 0, tzinfo=TZ),
        datetime(2026, 8, 28, 7, 21, 0, tzinfo=TZ),
        DAWN_E,
        "AubeE",
        "Moins expo",
    ),
)

PHASE_CLOCK = {
    "AubeA": "Six heures dix",
    "AubeB": "Six heures 25",
    "AubeC": "Six heures 40",
    "AubeD": "Six heures 55",
    "AubeE": "Sept heures dix",
}


@dataclass(frozen=True, slots=True)
class Cycle:
    index: int
    nominal: datetime
    start: datetime
    frames: tuple[Frame, ...]
    tag: str
    phase_say: str


def window_for(when: datetime) -> tuple[tuple[Frame, ...], str, str]:
    for start, end, frames, tag, phase_say in WINDOWS:
        if start <= when < end:
            return frames, tag, phase_say
    raise ValueError(f"no 100D window for {when.isoformat()}")


def incremental_for(index: int, item: Frame) -> str:
    if index == 0 or item.duration_s >= 1.0:
        return "N"
    return "Y"


def takepic(when: datetime, item: Frame, incremental: str, comment: str) -> Line:
    sign, offset = ref_from_max(when)
    rest = (
        f"{CAMERA},{item.shutter},{APERTURE},{item.iso},{MLU},"
        f"{QUALITY},None,{incremental},{comment}"
    )
    return Line("TAKEPIC", sign, offset, rest, when)


def emit_cycle(cycle: Cycle) -> list[Line]:
    lines: list[Line] = []
    for index, (offset_s, item) in enumerate(
        zip(ramp_offsets(cycle.frames), cycle.frames, strict=True)
    ):
        comment = f"{cycle.tag}{cycle.index:03d} {item.shutter} ISO{item.iso}"
        lines.append(
            takepic(
                cycle.start + timedelta(seconds=offset_s),
                item,
                incremental_for(index, item),
                comment,
            )
        )
    return lines


def nominal_starts() -> list[datetime]:
    times: list[datetime] = []
    when = FIRST_SLOT
    while when < MOONSET_CEST:
        times.append(when)
        when += INTERVAL
    return times


def cycles_on_grid(starts: list[datetime] | None = None) -> list[Cycle]:
    """Place one cycle per nominal slot (no 600D avoidance)."""
    out: list[Cycle] = []
    for index, nominal in enumerate(starts or nominal_starts(), start=1):
        frames, tag, phase_say = window_for(nominal)
        if ramp_free_at(nominal, frames) > MOONSET_CEST + timedelta(seconds=30):
            continue
        out.append(
            Cycle(
                index=index,
                nominal=nominal,
                start=nominal,
                frames=frames,
                tag=tag,
                phase_say=phase_say,
            )
        )
    return out


def overlaps(
    start: datetime,
    end: datetime,
    other_start: datetime,
    other_end: datetime,
    gap_s: float,
) -> bool:
    gap = timedelta(seconds=gap_s)
    return not (end + gap <= other_start or other_end + gap <= start)


def find_start(
    nominal: datetime,
    frames: tuple[Frame, ...],
    busy: list[tuple[datetime, datetime]],
    gap_s: float,
    max_shift: timedelta,
) -> datetime | None:
    duration = ramp_free_at(nominal, frames) - nominal
    t = nominal
    limit = nominal + max_shift
    step = timedelta(seconds=1)
    while t <= limit:
        end = t + duration
        if end > MOONSET_CEST + timedelta(seconds=30):
            return None
        if not any(overlaps(t, end, b0, b1, gap_s) for b0, b1 in busy):
            return t
        t += step
    return None


def place_cycles(
    busy: list[tuple[datetime, datetime]],
    gap_s: float,
    max_shift: timedelta | None = None,
) -> list[Cycle]:
    """Shift or skip 100D cycles so they do not overlap `busy` windows."""
    shift = max_shift if max_shift is not None else timedelta(seconds=60)
    placed: list[Cycle] = []
    occupied = list(busy)
    skipped = 0
    for index, nominal in enumerate(nominal_starts(), start=1):
        frames, tag, phase_say = window_for(nominal)
        start = find_start(nominal, frames, occupied, gap_s, shift)
        if start is None:
            skipped += 1
            continue
        cycle = Cycle(
            index=index - skipped,
            nominal=nominal,
            start=start,
            frames=frames,
            tag=tag,
            phase_say=phase_say,
        )
        placed.append(cycle)
        occupied.append((start, ramp_free_at(start, frames)))
    return placed


def announce_lines(cycles: list[Cycle]) -> list[Line]:
    first = cycles[0]
    last = cycles[-1]
    n = len(cycles)
    power_on = first.start - POWER_MARGIN
    lines = [
        command_say(power_on, "Allume"),
        command_say(power_on + timedelta(seconds=1), "Cent D"),
        command_say(first.start - timedelta(seconds=12), "Time lapse"),
        command_say(first.start - timedelta(seconds=11), first.phase_say),
        command_say(FRAME_LOCK, "Cadrage Lune"),
        command_say(FRAME_LOCK + timedelta(seconds=1), "Bord haut"),
        command_say(FRAME_LOCK + timedelta(seconds=2), "Vingt pct gauche"),
        command_say(FRAME_LOCK + timedelta(seconds=3), "Horizon tiers"),
        command_say(last.start - timedelta(seconds=12), "Moonset"),
        command_say(last.start - timedelta(seconds=11), "Dernier cycle"),
    ]
    seen_phase = {first.tag}
    for cycle in cycles[1:]:
        if cycle is last:
            continue
        if cycle.tag not in seen_phase:
            seen_phase.add(cycle.tag)
            clock = PHASE_CLOCK.get(cycle.tag)
            lead = cycle.start - timedelta(seconds=14)
            lines.append(command_say(lead, "Cent D"))
            offset = 1
            if clock is not None:
                lines.append(command_say(lead + timedelta(seconds=offset), clock))
                offset += 1
            lines.append(
                command_say(lead + timedelta(seconds=offset), cycle.phase_say)
            )
            continue
        if cycle.index % PROGRESS_EVERY != 0:
            continue
        lead = cycle.start - timedelta(seconds=12)
        lines.append(command_say(lead, "Cent D"))
        lines.append(
            command_say(lead + timedelta(seconds=1), f"Cycle {cycle.index} sur {n}")
        )
    return lines


def session_lines(cycles: list[Cycle] | None = None) -> list[Line]:
    schedule = cycles if cycles is not None else cycles_on_grid()
    lines = announce_lines(schedule)
    for cycle in schedule:
        lines.extend(emit_cycle(cycle))
    return sorted(lines, key=lambda line: line.when)


def header(n_pic: int, n_cycles: int) -> str:
    return f"""#
# LEM -- seance 100D 24 mm paysage (forme A). Usage personnel.
# Tournefeuille 28 aout 2026. Copier vers
# ~/Documents/Scripts Lunar Eclipse Maestro/ puis Fichier -> Charger script...
#
# Nom APN Configuration materielle : {CAMERA} (casse exacte)
# JPEG Fine = JPG-F (pas Fine, pas JPG-L). Av 4.0. Intervalle 90 s.
# Grille DEC-018 (centrale nuit 4 s ISO 800 = placeholder). 15 s pas 16 s.
# Incremental N en tete de cycle et si pose >= 1 s (KI-024).
# Allumage : say puis {int(POWER_MARGIN.total_seconds())} s avant 1ere vue (KI-025).
# Cadrage DEC-017 : 04:52:40 Bord haut / 20 pct gauche / horizon tiers.
# ~{n_pic} TAKEPIC, {n_cycles} cycles. Regenerer :
#   .venv/bin/python scripts/generate_lem_seance_100d.py
#

#Action,Date/Ref,Offset sign,Time (offset),Camera,Exposure,Aperture,ISO,MLU,Quality,Size,Incremental,Comment
"""


def render_script(cycles: list[Cycle] | None = None) -> str:
    schedule = cycles if cycles is not None else cycles_on_grid()
    lines = session_lines(schedule)
    n_pic = sum(1 for line in lines if line.action == "TAKEPIC")
    chunks = [header(n_pic, len(schedule))]
    previous = ""
    for line in lines:
        marker = (
            line.rest.split(",")[-1].split(" ", 1)[0]
            if line.action == "TAKEPIC"
            else "say"
        )
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
    pics = [line for line in session_lines() if line.action == "TAKEPIC"]
    n_cycles = len(cycles_on_grid())
    print(f"{written.relative_to(ROOT)} ({len(pics)} TAKEPIC, {n_cycles} cycles)")


if __name__ == "__main__":
    main()
