from __future__ import annotations

import sys
from datetime import timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import generate_lem_seance as gen600  # noqa: E402
import generate_lem_seance_100d as gen100  # noqa: E402
import generate_lem_seance_interlace as gen  # noqa: E402


def _pics(lines: list[gen.Line], camera: str) -> list[gen.Line]:
    return [
        line
        for line in lines
        if line.action == "TAKEPIC" and line.rest.startswith(camera)
    ]


def test_committed_script_matches_generator() -> None:
    generated = gen.render_script()
    on_disk = gen.OUTPUT_PATH.read_text(encoding="ascii")
    assert on_disk == generated


def test_script_is_ascii() -> None:
    gen.render_script().encode("ascii")


def test_600d_timestamps_unchanged() -> None:
    solo = [line.when for line in gen600.session_lines() if line.action == "TAKEPIC"]
    merged, _cycles = gen.session_bundle()
    dual = [line.when for line in _pics(merged, "600D-T150")]
    assert dual == solo


def test_no_two_actions_same_second() -> None:
    lines, _cycles = gen.session_bundle()
    stamps = [int(line.when.timestamp()) for line in lines]
    assert len(stamps) == len(set(stamps))


def test_inter_camera_gap() -> None:
    lines, _cycles = gen.session_bundle()
    occupied: list[tuple[str, object, object]] = []
    for line in lines:
        if line.action != "TAKEPIC":
            continue
        camera, shutter, *_rest = line.rest.split(",")
        start = line.when
        end = start + timedelta(seconds=gen600.shutter_s(shutter) + gen600.USB_S)
        occupied.append((camera, start, end))
    occupied.sort(key=lambda item: item[1])
    gap = timedelta(seconds=gen.INTER_CAM_GAP_S)
    for previous, current in zip(occupied, occupied[1:], strict=False):
        if previous[0] == current[0]:
            continue
        assert previous[2] + gap <= current[1] or current[2] + gap <= previous[1], (
            previous,
            current,
        )


def test_100d_quality_and_skips_bounded() -> None:
    lines, cycles = gen.session_bundle()
    pics = _pics(lines, "100D-W24")
    assert pics
    for line in pics:
        assert ",JPG-F," in line.rest
    nominal = len(gen100.nominal_starts())
    skipped = nominal - len(cycles)
    assert skipped < 15, skipped
    assert len(cycles) > 90


def test_say_is_short_ascii() -> None:
    lines, _cycles = gen.session_bundle()
    for line in lines:
        if line.action != "COMMAND":
            continue
        spoken = line.rest.split(';say "', 1)[1].rstrip('"')
        spoken.encode("ascii")
        assert len(spoken) <= 60, spoken
