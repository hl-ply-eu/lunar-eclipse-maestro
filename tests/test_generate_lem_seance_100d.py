from __future__ import annotations

import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import generate_lem_seance_100d as gen  # noqa: E402


def _pics() -> list[gen.Line]:
    return [line for line in gen.session_lines() if line.action == "TAKEPIC"]


def _fields(line: gen.Line) -> list[str]:
    return line.rest.split(",")


def test_committed_script_matches_generator() -> None:
    generated = gen.render_script()
    on_disk = gen.OUTPUT_PATH.read_text(encoding="ascii")
    assert on_disk == generated


def test_script_is_ascii() -> None:
    gen.render_script().encode("ascii")


def test_camera_jpeg_fine() -> None:
    for line in _pics():
        camera, shutter, aperture, _iso, mlu, quality, size, incremental, _c = (
            line.rest.split(",", 8)
        )
        assert camera == "100D-W24"
        assert aperture == "4.0"
        assert mlu == "0.0"
        assert quality == "JPG-F"
        assert size == "None"
        assert incremental in {"N", "Y"}
        assert shutter != "16"
        assert shutter != "1/16"


def test_night_is_three_then_dawn_five() -> None:
    cycles = gen.cycles_on_grid()
    night = [c for c in cycles if c.tag == "Nuit3"]
    dawn = [c for c in cycles if c.tag != "Nuit3"]
    assert night
    assert all(len(c.frames) == 3 for c in night)
    assert dawn
    assert all(len(c.frames) == 5 for c in dawn)
    assert night[-1].nominal < datetime(2026, 8, 28, 6, 10, tzinfo=gen.TZ)


def test_incremental_n_on_long_and_first() -> None:
    for cycle in gen.cycles_on_grid():
        pics = gen.emit_cycle(cycle)
        assert _fields(pics[0])[7] == "N"
        for index, (line, item) in enumerate(zip(pics, cycle.frames, strict=True)):
            incremental = _fields(line)[7]
            if index == 0 or item.duration_s >= 1.0:
                assert incremental == "N", (cycle.start, item)
            else:
                assert incremental == "Y"


def test_power_margin_sixty_seconds() -> None:
    lines = gen.session_lines()
    first_pic = next(line for line in lines if line.action == "TAKEPIC")
    first_say = next(line for line in lines if line.action == "COMMAND")
    assert first_pic.when - first_say.when >= timedelta(seconds=60)


def test_say_is_short_ascii() -> None:
    for line in gen.session_lines():
        if line.action != "COMMAND":
            continue
        spoken = line.rest.split(';say "', 1)[1].rstrip('"')
        spoken.encode("ascii")
        assert len(spoken) <= 60, spoken
