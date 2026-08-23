#!/usr/bin/env python3
"""Generate the LEM session script for the 600D at the 150 mm f/5 focus.

Output: scripts/lem/essais-2026/seance-600d-t150.txt
Times are offsets from MAX (LEM local circumstances). Wall-clock CEST in
the header is documentary (Tournefeuille 2026-08-28).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = ROOT / "scripts" / "lem" / "essais-2026" / "seance-600d-t150.txt"

CAMERA = "600D-T150"
APERTURE = "5.6"
MLU = "0.0"
TZ = ZoneInfo("Europe/Paris")

USB_S = 1.1
BUFFER_S = 10.0
MIN_GAP_S = 3.0
LONG_GAP_S = 4.0

MAX_CEST = datetime(2026, 8, 28, 6, 12, 55, tzinfo=TZ)
U1_CEST = datetime(2026, 8, 28, 4, 33, 52, tzinfo=TZ)
MOONSET_CEST = datetime(2026, 8, 28, 7, 20, 26, tzinfo=TZ)
HOLE_START = datetime(2026, 8, 28, 5, 40, 0, tzinfo=TZ)
HOLE_END = datetime(2026, 8, 28, 5, 55, 0, tzinfo=TZ)
DAWN_5 = datetime(2026, 8, 28, 6, 44, 0, tzinfo=TZ)
DAWN_3 = datetime(2026, 8, 28, 7, 0, 0, tzinfo=TZ)
FIRST_SLOT = datetime(2026, 8, 28, 4, 20, 55, tzinfo=TZ)
CADENCE = timedelta(minutes=2)


@dataclass(frozen=True, slots=True)
class Frame:
    shutter: str
    iso: int
    duration_s: float
    note: str


@dataclass(frozen=True, slots=True)
class Line:
    action: str
    sign: str
    offset: str
    rest: str
    when: datetime


def shutter_s(shutter: str) -> float:
    if shutter.startswith("1/"):
        return 1.0 / float(shutter[2:])
    return float(shutter)


def frame(shutter: str, iso: int, note: str) -> Frame:
    return Frame(shutter, iso, shutter_s(shutter), note)


# Formes §11 — grid computed for f/5. Av 5.6 is the LEM USB column only.
HDR = (
    frame("1/1000", 100, "limbe"),
    frame("1/250", 100, "limbe"),
    frame("1/125", 200, "tons"),
    frame("1/30", 200, "tons"),
    frame("1/8", 200, "tons"),
    frame("1/8", 800, "umbra"),
    frame("1/2", 800, "umbra"),
    frame("1", 800, "sombre"),
    frame("2", 800, "sombre"),
)
PENUMBRA = HDR[:5]
CURRENT = HDR[:7]
EXTENDED = HDR
DIAG_ISO100 = (
    frame("1/1000", 100, "diag"),
    frame("1/250", 100, "diag"),
    frame("1/60", 100, "diag"),
    frame("1/15", 100, "diag"),
    frame("1/4", 100, "diag"),
    frame("1", 100, "diag"),
    frame("4", 100, "diag"),
)
DIAG_ISO1600 = (
    frame("1/4000", 1600, "fige"),
    frame("1/1000", 1600, "fige"),
    frame("1/250", 1600, "fige"),
    frame("1/60", 1600, "fige"),
    frame("1/15", 1600, "fige"),
    frame("1/4", 1600, "fige"),
    frame("1", 1600, "fige"),
)


def start_gap_s(prev_duration_s: float) -> float:
    gap = max(MIN_GAP_S, prev_duration_s + USB_S)
    if prev_duration_s >= 1.0:
        gap = max(LONG_GAP_S, gap)
    return gap


def ramp_offsets(frames: tuple[Frame, ...]) -> list[float]:
    offsets = [0.0]
    for prev in frames[:-1]:
        offsets.append(offsets[-1] + start_gap_s(prev.duration_s))
    return offsets


def ceil_second(when: datetime) -> datetime:
    if when.microsecond == 0:
        return when
    return when.replace(microsecond=0) + timedelta(seconds=1)


def ramp_free_at(start: datetime, frames: tuple[Frame, ...]) -> datetime:
    last = start + timedelta(seconds=ramp_offsets(frames)[-1])
    return last + timedelta(seconds=frames[-1].duration_s + USB_S)


def after_buffer(start: datetime, frames: tuple[Frame, ...]) -> datetime:
    return ceil_second(ramp_free_at(start, frames) + timedelta(seconds=BUFFER_S))


def format_offset(delta: timedelta) -> str:
    total = abs(delta.total_seconds())
    tenths = int(round((total - int(total)) * 10))
    if tenths == 10:
        total = int(total) + 1
        tenths = 0
    seconds = int(total)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{tenths}"


def ref_from_max(when: datetime) -> tuple[str, str]:
    delta = when - MAX_CEST
    sign = "+" if delta.total_seconds() >= 0 else "-"
    return sign, format_offset(delta)


def slot_times() -> list[datetime]:
    times: list[datetime] = []
    k = -80
    while True:
        when = MAX_CEST + k * CADENCE
        k += 1
        if when > MOONSET_CEST:
            break
        if when < FIRST_SLOT:
            continue
        times.append(when)
    return times


def slot_kind(when: datetime) -> str | None:
    if HOLE_START <= when < HOLE_END:
        return None
    if when == MAX_CEST + CADENCE:
        return None
    if when == MAX_CEST:
        return "max"
    if when in extended_slots():
        return "extended"
    if when < U1_CEST:
        return "penumbra"
    if when >= DAWN_3:
        return "dawn3"
    if when >= DAWN_5:
        return "dawn5"
    return "current"


def extended_slots() -> frozenset[datetime]:
    u1_plus_10 = MAX_CEST - timedelta(minutes=90)  # 04:42:55 ~ U1+9
    mid = MAX_CEST - timedelta(minutes=50)  # 05:22:55 ~ 50 %
    dusk = MAX_CEST + timedelta(minutes=18)  # 06:30:55 last umbra HDR
    return frozenset({u1_plus_10, mid, dusk})


def frames_for(kind: str) -> tuple[Frame, ...]:
    return {
        "penumbra": PENUMBRA,
        "current": CURRENT,
        "extended": EXTENDED,
        "dawn5": PENUMBRA,
        "dawn3": HDR[:3],
    }[kind]


def takepic(when: datetime, frame: Frame, incremental: str, comment: str) -> Line:
    sign, offset = ref_from_max(when)
    rest = (
        f"{CAMERA},{frame.shutter},{APERTURE},{frame.iso},{MLU},"
        f"RAW,None,{incremental},{comment}"
    )
    return Line("TAKEPIC", sign, offset, rest, when)


def command_say(when: datetime, spoken: str) -> Line:
    sign, offset = ref_from_max(when)
    rest = f" , , , , , , , ,{spoken} ;say \"{spoken}\""
    return Line("COMMAND", sign, offset, rest, when)


def emit_ramp(start: datetime, frames: tuple[Frame, ...], tag: str) -> list[Line]:
    lines: list[Line] = []
    for index, (offset_s, item) in enumerate(zip(ramp_offsets(frames), frames)):
        incremental = "N" if index == 0 else "Y"
        comment = f"{tag} {item.shutter} ISO{item.iso}"
        lines.append(
            takepic(
                start + timedelta(seconds=offset_s),
                item,
                incremental,
                comment,
            )
        )
    return lines


def emit_max_block() -> list[Line]:
    product_start = MAX_CEST
    iso100_start = after_buffer(product_start, EXTENDED)
    iso1600_start = after_buffer(iso100_start, DIAG_ISO100)
    lines = [
        command_say(MAX_CEST - timedelta(seconds=10), "Rampe max"),
        command_say(MAX_CEST - timedelta(seconds=9), "Etendue 9"),
        *emit_ramp(product_start, EXTENDED, "Max"),
        command_say(iso100_start - timedelta(seconds=2), "Iso 100"),
        *emit_ramp(iso100_start, DIAG_ISO100, "Iso100"),
        command_say(iso1600_start - timedelta(seconds=2), "Iso 1600"),
        *emit_ramp(iso1600_start, DIAG_ISO1600, "Iso1600"),
    ]
    return lines


def announce_lines() -> list[Line]:
    first = FIRST_SLOT
    u1_ext, mid_ext, last_ext = sorted(extended_slots())
    return [
        command_say(first - timedelta(seconds=55), "Suivi Lune"),
        command_say(first - timedelta(seconds=54), "Pas sideral"),
        command_say(u1_ext - timedelta(seconds=30), "Rampe etendue"),
        command_say(mid_ext - timedelta(seconds=30), "Rampe etendue"),
        command_say(HOLE_START - timedelta(minutes=2), "Pause accu 2 min"),
        command_say(HOLE_START, "Swap accu"),
        command_say(HOLE_END - timedelta(minutes=1), "Reprise 1 min"),
        command_say(HOLE_END + timedelta(seconds=55), "Reprise USB"),
        command_say(last_ext - timedelta(seconds=30), "Rampe etendue"),
        command_say(DAWN_5, "Aube 5 vues"),
        command_say(DAWN_3, "Aube 3 vues"),
    ]


def session_lines() -> list[Line]:
    lines = announce_lines()
    for when in slot_times():
        kind = slot_kind(when)
        if kind is None:
            continue
        if kind == "max":
            lines.extend(emit_max_block())
            continue
        tag = {
            "penumbra": "Penombre",
            "current": "Courante",
            "extended": "Etendue",
            "dawn5": "Aube5",
            "dawn3": "Aube3",
        }[kind]
        lines.extend(emit_ramp(when, frames_for(kind), tag))
    return sorted(lines, key=lambda line: line.when)


def render_line(line: Line) -> str:
    return f"{line.action},MAX,{line.sign},{line.offset},{line.rest}"


def header() -> str:
    n_pic = sum(1 for line in session_lines() if line.action == "TAKEPIC")
    return f"""#
# LEM -- seance 600D au foyer 150 mm f/5 (forme C). Usage personnel.
# Tournefeuille 28 aout 2026. Copier vers
# ~/Documents/Scripts Lunar Eclipse Maestro/ puis Fichier -> Charger script...
#
# Nom APN Configuration materielle : {CAMERA} (casse exacte)
# Carte 32 Go, RAW, mode M, MAP manuelle, AEB off, EOS Utility ferme.
#
# Optique : telescope 150 mm f/5 (750 mm), T-ring muet (KI-019).
# Colonne Av = 5.6 = ce que LEM envoie en USB (meme valeur que le bench
# 15-85). Le tube n'a pas de diaphragme : le faisceau reste f/5.
# Grille Tv/ISO calculee pour f/5 (formes para. 11). f/5 est ~0.3 EV plus
# ouvert que la colonne Jubier f/5.6 ; on garde 1/1000 (legerement riche
# vs 1/1250 equivalent), pas un recadrage d'expo.
#
# Ancrage : toutes les 2 min sur MAX (06:12:55 CEST).
#   Premiere rampe MAX-01:52:00 = 04:20:55
#   Derniere rampe MAX+01:06:00 = 07:18:55 (moonset 07:20:26)
# Penombre 5 vues (1-5). Courante 7. Etendue 9 aux stacks nommes.
# Etendue 06:30 = MAX+00:18:00 (06:30:55) : 4e HDR umbra, PAS le bloc MAX.
# Bloc MAX (DEC-015) : etendue 9 + Iso 100 (-> 4 s) + Iso 1600 (1/4000 -> 1 s).
# Saut MAX+00:02:00 (la courante de 06:14:55). Trou accu 05:40-05:55.
# Reprise 05:56:55 Incremental N. Aube 5 vues des 06:44, 3 vues des 07:00.
# Incremental N en tete de CHAQUE rampe, Y ensuite (DEC-016).
# Ecarts >= 3 s ; +4 s apres une pose >= 1 s. Tampon 5 -> 10 s entre blocs MAX.
# COMMAND ;say courts, ASCII, ~1 s (KI-021). Taux Lune, pas sideral (KI-008).
# Ne pas charger basic.txt / deluxe.txt (totalite, KI-018).
#
# ~{n_pic} TAKEPIC. Regenerer : .venv/bin/python scripts/generate_lem_seance.py
#

#Action,Date/Ref,Offset sign,Time (offset),Camera,Exposure,Aperture,ISO,MLU,Quality,Size,Incremental,Comment
"""


def render_script() -> str:
    chunks = [header()]
    previous_kind = ""
    for line in session_lines():
        marker = line.rest.split(",")[-1].split(" ", 1)[0] if line.action == "TAKEPIC" else "say"
        if marker != previous_kind and line.action == "TAKEPIC":
            chunks.append(f"\n# --- {marker} {line.when.strftime('%H:%M:%S')} ---\n")
            previous_kind = marker
        chunks.append(render_line(line) + "\n")
    return "".join(chunks)


def write_script(path: Path = OUTPUT_PATH) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_script(), encoding="ascii")
    return path


if __name__ == "__main__":
    written = write_script()
    pics = [line for line in session_lines() if line.action == "TAKEPIC"]
    print(f"{written.relative_to(ROOT)} ({len(pics)} TAKEPIC)")
