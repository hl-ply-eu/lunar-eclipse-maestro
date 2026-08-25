from __future__ import annotations

import math
import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import simulate_fov as sim  # noqa: E402


def test_altaz_to_unit_vector_axes() -> None:
    east = sim.altaz_to_unit_vector(alt_deg=0.0, az_deg=90.0)
    north = sim.altaz_to_unit_vector(alt_deg=0.0, az_deg=0.0)
    zenith = sim.altaz_to_unit_vector(alt_deg=90.0, az_deg=0.0)

    assert np.allclose(east, np.array([1.0, 0.0, 0.0]), atol=1e-7)
    assert np.allclose(north, np.array([0.0, 1.0, 0.0]), atol=1e-7)
    assert np.allclose(zenith, np.array([0.0, 0.0, 1.0]), atol=1e-7)


def test_build_camera_basis_is_orthonormal() -> None:
    forward = sim.altaz_to_unit_vector(alt_deg=8.1, az_deg=245.0)
    basis = sim.build_camera_basis(forward)

    assert np.isclose(np.linalg.norm(basis.right), 1.0, atol=1e-8)
    assert np.isclose(np.linalg.norm(basis.up), 1.0, atol=1e-8)
    assert np.isclose(np.linalg.norm(basis.forward), 1.0, atol=1e-8)
    assert np.isclose(np.dot(basis.right, basis.up), 0.0, atol=1e-8)
    assert np.isclose(np.dot(basis.right, basis.forward), 0.0, atol=1e-8)
    assert np.isclose(np.dot(basis.up, basis.forward), 0.0, atol=1e-8)


def test_build_camera_basis_right_points_north_when_facing_west() -> None:
    # Facing due west, with up aligned to zenith:
    # image right side should point to geographic north.
    forward = sim.altaz_to_unit_vector(alt_deg=0.0, az_deg=270.0)
    basis = sim.build_camera_basis(forward)
    east, north, up = basis.right

    assert np.isclose(east, 0.0, atol=1e-7)
    assert north > 0.999999
    assert np.isclose(up, 0.0, atol=1e-7)


def test_gnomonic_center_maps_to_sensor_center() -> None:
    forward = sim.altaz_to_unit_vector(alt_deg=12.0, az_deg=210.0)
    basis = sim.build_camera_basis(forward)
    target = sim.altaz_to_unit_vector(alt_deg=12.0, az_deg=210.0)
    projection = sim.gnomonic_project(target, basis)
    assert projection is not None
    x_tan, y_tan = projection

    camera = sim.CameraConfig(
        model="Test Cam",
        sensor_width_mm=22.3,
        sensor_height_mm=14.9,
        resolution_width_px=5184,
        resolution_height_px=3456,
    )
    optic = sim.OpticConfig(name="Test Lens", focal_length_mm=280.0, aperture_f=5.6)
    x_px, y_px = sim.tangent_to_pixel(x_tan, y_tan, camera, optic)

    assert np.isclose(x_px, camera.resolution_width_px / 2, atol=1e-6)
    assert np.isclose(y_px, camera.resolution_height_px / 2, atol=1e-6)


def test_anti_sun_is_opposite_hemisphere() -> None:
    alt, az = sim.anti_sun_altaz(sun_alt_deg=-20.0, sun_az_deg=70.0)
    assert np.isclose(alt, 20.0)
    assert np.isclose(az, 250.0)


def test_shadow_radii_umbra_larger_than_moon_typical() -> None:
    # Mean Earth–Moon / Earth–Sun distances: umbra ~42', moon ~15–16'.
    umbra, penumbra = sim.shadow_angular_radii_rad(
        sun_distance_km=149_600_000.0,
        moon_distance_km=384_400.0,
    )
    moon_rad = math.asin(sim.MOON_RADIUS_KM / 384_400.0)
    assert umbra > moon_rad
    assert penumbra > umbra
    assert 0.011 < umbra < 0.014  # ~38–48 arcmin


def test_interpolate_zero_crossing_returns_expected_time() -> None:
    tz = ZoneInfo("Europe/Paris")
    t0 = datetime(2026, 8, 28, 5, 0, 0, tzinfo=tz)
    times = [t0, t0 + timedelta(seconds=10), t0 + timedelta(seconds=20)]
    values = [-5.0, 5.0, 15.0]
    crossing = sim.interpolate_zero_crossing(times, values)

    assert crossing == t0 + timedelta(seconds=5)


def test_find_auto_top_time_detects_lunar_limb_crossing() -> None:
    tz = ZoneInfo("Europe/Paris")
    t0 = datetime(2026, 8, 28, 5, 0, 0, tzinfo=tz)
    samples = [
        _moon_sample(t0, moon_y=-40.0, radius=10.0),
        _moon_sample(t0 + timedelta(seconds=10), moon_y=-10.0, radius=10.0),
        _moon_sample(t0 + timedelta(seconds=20), moon_y=15.0, radius=10.0),
    ]

    auto_top = sim.find_auto_top_time(
        projected_samples=samples,
        pointing_time_local=t0 + timedelta(seconds=30),
        margin_px=0.0,
    )

    assert auto_top == t0 + timedelta(seconds=10)


def test_find_closest_top_time_when_no_crossing() -> None:
    tz = ZoneInfo("Europe/Paris")
    t0 = datetime(2026, 8, 28, 5, 0, 0, tzinfo=tz)
    samples = [
        _moon_sample(t0, moon_y=40.0, radius=10.0),
        _moon_sample(t0 + timedelta(seconds=10), moon_y=35.0, radius=10.0),
        _moon_sample(t0 + timedelta(seconds=20), moon_y=30.0, radius=10.0),
    ]

    closest = sim.find_closest_top_time(
        projected_samples=samples,
        pointing_time_local=t0 + timedelta(seconds=30),
        margin_px=0.0,
    )

    assert closest == t0 + timedelta(seconds=20)


def test_load_config_tournefeuille() -> None:
    config = sim.load_config(ROOT / "scripts/config/tournefeuille-600d.yaml")

    assert config.site.name == "Tournefeuille"
    assert config.site.latitude_deg == 43.582389
    assert config.site.longitude_deg == 1.350944
    assert config.simulation.ephemeris_path == "de421.bsp"
    assert config.framing.pointing_event == "max"
    assert config.framing.composition == sim.COMPOSITION_MOON_CENTERED
    assert "p1" in config.eclipse.contacts_local
    assert "u1" in config.eclipse.contacts_local
    assert "set" in config.eclipse.contacts_local
    assert len(config.optics) == 3
    assert config.camera.sensor_width_mm == 22.3
    assert config.simulation.window_minutes >= 180
    assert config.eclipse.contacts_local["set"].hour == 7
    assert config.eclipse.contacts_local["set"].minute == 20


def test_find_auto_top_time_upper_limb_inside_tangent() -> None:
    tz = ZoneInfo("Europe/Paris")
    t0 = datetime(2026, 8, 28, 5, 0, 0, tzinfo=tz)
    samples = [
        _moon_sample(t0, moon_y=-20.0, radius=10.0),
        _moon_sample(t0 + timedelta(seconds=10), moon_y=10.0, radius=10.0),
        _moon_sample(t0 + timedelta(seconds=20), moon_y=40.0, radius=10.0),
    ]

    auto_top = sim.find_auto_top_time(
        projected_samples=samples,
        pointing_time_local=t0 + timedelta(seconds=30),
        margin_px=0.0,
        limb="upper",
    )

    assert auto_top == t0 + timedelta(seconds=10)


def test_horizon_thirds_aim_alt_24mm() -> None:
    camera = sim.CameraConfig(
        model="Canon EOS 100D",
        sensor_width_mm=22.3,
        sensor_height_mm=14.9,
        resolution_width_px=5184,
        resolution_height_px=3456,
    )
    optic = sim.OpticConfig(name="24mm", focal_length_mm=24.0, aperture_f=4.0)
    aim = sim.horizon_thirds_aim_alt_deg(camera, optic, horizon_alt_deg=0.0)
    assert 5.85 < aim < 5.97


def test_horizon_thirds_puts_horizon_on_lower_third() -> None:
    camera = sim.CameraConfig(
        model="Canon EOS 100D",
        sensor_width_mm=22.3,
        sensor_height_mm=14.9,
        resolution_width_px=5184,
        resolution_height_px=3456,
    )
    optic = sim.OpticConfig(name="24mm", focal_length_mm=24.0, aperture_f=4.0)
    aim = sim.horizon_thirds_aim_alt_deg(camera, optic, horizon_alt_deg=0.0)
    az = 245.26
    basis = sim.build_camera_basis(sim.altaz_to_unit_vector(aim, az))
    horizon = sim.altaz_to_unit_vector(0.0, az)
    tangent = sim.gnomonic_project(horizon, basis)
    assert tangent is not None
    _x_px, y_px = sim.tangent_to_pixel(tangent[0], tangent[1], camera, optic)
    lower_third = 2.0 * camera.resolution_height_px / 3.0
    assert abs(y_px - lower_third) < 2.0


def test_horizon_thirds_max_stays_below_upper_third_at_24mm() -> None:
    camera = sim.CameraConfig(
        model="Canon EOS 100D",
        sensor_width_mm=22.3,
        sensor_height_mm=14.9,
        resolution_width_px=5184,
        resolution_height_px=3456,
    )
    optic = sim.OpticConfig(name="24mm", focal_length_mm=24.0, aperture_f=4.0)
    aim = sim.horizon_thirds_aim_alt_deg(camera, optic, horizon_alt_deg=0.0)
    az = 245.26
    basis = sim.build_camera_basis(sim.altaz_to_unit_vector(aim, az))
    moon = sim.altaz_to_unit_vector(10.51, az)
    tangent = sim.gnomonic_project(moon, basis)
    assert tangent is not None
    _x_px, y_px = sim.tangent_to_pixel(tangent[0], tangent[1], camera, optic)
    upper_third = camera.resolution_height_px / 3.0
    mid = camera.resolution_height_px / 2.0
    assert upper_third < y_px < mid


def test_load_config_100d_24mm_horizon_thirds() -> None:
    config = sim.load_config(ROOT / "scripts/config/tournefeuille-100d-24mm.yaml")

    assert config.camera.model == "Canon EOS 100D"
    assert config.framing.composition == sim.COMPOSITION_HORIZON_THIRDS
    assert config.framing.pointing_event == "max"
    assert config.optics[0].focal_length_mm == 24.0
    assert sim.auto_top_limb(config.framing.composition) == "upper"


def test_parse_composition_rejects_unknown() -> None:
    try:
        sim._parse_composition({"composition": "golden_ratio"})
    except ValueError as exc:
        assert "golden_ratio" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_load_config_archive_paris_still_parses() -> None:
    config = sim.load_config(ROOT / "scripts/config/paris-600d-placeholder.yaml")
    assert "Paris" in config.site.name
    assert "set" in config.eclipse.contacts_local


def _moon_sample(when: datetime, moon_y: float, radius: float) -> sim.ProjectedSample:
    return sim.ProjectedSample(
        when_local=when,
        moon_x_px=100.0,
        moon_y_px=moon_y,
        moon_radius_px=radius,
        umbra_x_px=100.0,
        umbra_y_px=moon_y,
        umbra_radius_px=radius * 2.5,
        penumbra_x_px=100.0,
        penumbra_y_px=moon_y,
        penumbra_radius_px=radius * 4.0,
    )
