from __future__ import annotations

import sys
from datetime import timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import generate_lem_seance as gen  # noqa: E402


def _pics() -> list[gen.Line]:
    return [line for line in gen.session_lines() if line.action == "TAKEPIC"]


def _incremental(line: gen.Line) -> str:
    return line.rest.split(",")[7]


def test_committed_script_matches_generator() -> None:
    generated = gen.render_script()
    on_disk = gen.OUTPUT_PATH.read_text(encoding="ascii")
    assert on_disk == generated


def test_script_is_ascii() -> None:
    gen.render_script().encode("ascii")


def test_camera_aperture_raw() -> None:
    for line in _pics():
        camera, _shutter, aperture, _iso, mlu, quality, size, incremental, _c = (
            line.rest.split(",", 8)
        )
        assert camera == "600D-T150"
        assert aperture == "5.6"
        assert mlu == "0.0"
        assert quality == "RAW"
        assert size == "None"
        assert incremental in {"N", "Y"}


def test_ramp_starts_with_incremental_n() -> None:
    pics = _pics()
    assert _incremental(pics[0]) == "N"
    for previous, current in zip(pics, pics[1:]):
        gap = (current.when - previous.when).total_seconds()
        if gap > 10:
            assert _incremental(current) == "N", current.when
        else:
            assert _incremental(current) == "Y", current.when


def test_min_gap_three_seconds() -> None:
    pics = _pics()
    for previous, current in zip(pics, pics[1:]):
        gap = (current.when - previous.when).total_seconds()
        assert gap >= 3.0, (previous.when, current.when, gap)


def test_bench_gap_after_one_second_is_four() -> None:
    assert gen.start_gap_s(1.0) == 4.0
    assert gen.start_gap_s(0.5) == 3.0
    assert gen.start_gap_s(2.0) == 4.0


def test_no_takepic_in_battery_hole() -> None:
    for line in _pics():
        assert not (gen.HOLE_START <= line.when < gen.HOLE_END)


def test_max_plus_two_minutes_slot_skipped() -> None:
    skipped = gen.MAX_CEST + gen.CADENCE
    starts = {line.when for line in _pics()}
    assert skipped not in starts


def test_penumbra_is_five_frames() -> None:
    first = gen.FIRST_SLOT
    frames = [line for line in _pics() if first <= line.when < first + timedelta(seconds=20)]
    assert len(frames) == 5


def test_named_extended_stacks_have_nine_frames() -> None:
    for start in sorted(gen.extended_slots()):
        frames = [
            line
            for line in _pics()
            if start <= line.when < start + timedelta(seconds=40)
        ]
        assert len(frames) == 9, start


def test_max_block_is_product_then_diagnostics() -> None:
    block = [
        line
        for line in _pics()
        if gen.MAX_CEST <= line.when < gen.MAX_CEST + timedelta(seconds=120)
    ]
    shutters = [line.rest.split(",")[1] for line in block]
    isos = [int(line.rest.split(",")[3]) for line in block]
    assert len(block) == 9 + 7 + 7
    assert shutters[0] == "1/1000" and isos[0] == 100
    assert shutters[8] == "2" and isos[8] == 800
    assert isos[9] == 100 and shutters[15] == "4"
    assert isos[16] == 1600 and shutters[16] == "1/4000"
    assert shutters[-1] == "1" and isos[-1] == 1600
    last = block[-1].when
    assert last < gen.MAX_CEST + timedelta(minutes=2)


def test_cadence_anchored_on_max() -> None:
    first_of_ramps: list[gen.Line] = []
    pics = _pics()
    first_of_ramps.append(pics[0])
    for previous, current in zip(pics, pics[1:]):
        if (current.when - previous.when).total_seconds() > 10:
            first_of_ramps.append(current)
    max_block_end = gen.MAX_CEST + timedelta(seconds=120)
    for line in first_of_ramps:
        if gen.MAX_CEST <= line.when < max_block_end:
            continue
        delta_min = abs((line.when - gen.MAX_CEST).total_seconds() / 60.0)
        assert abs(delta_min - round(delta_min / 2) * 2) < 1e-6, line.when


def test_dawn_shortens() -> None:
    dawn5 = [
        line
        for line in _pics()
        if gen.DAWN_5 <= line.when < gen.DAWN_3
    ]
    dawn3 = [line for line in _pics() if line.when >= gen.DAWN_3]
    assert dawn5
    assert dawn3
    first_5 = dawn5[0]
    group_5 = [line for line in dawn5 if line.when < first_5.when + timedelta(seconds=20)]
    assert len(group_5) == 5
    first_3 = dawn3[0]
    group_3 = [line for line in dawn3 if line.when < first_3.when + timedelta(seconds=20)]
    assert len(group_3) == 3
