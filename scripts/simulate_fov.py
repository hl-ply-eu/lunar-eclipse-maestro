#!/usr/bin/env python3
"""Simulate the lunar trajectory inside a camera field of view.

Fixed-tripod lunar-eclipse framing:
- the camera is pointed once, then remains fixed (no tracking),
- the Moon is centered at the configured pointing event (typically MAX),
- Earth's umbra/penumbra are overlaid on the lunar disk for a bite preview.
"""

from __future__ import annotations

import argparse
import math
import re
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import matplotlib

matplotlib.use("Agg")

import numpy as np
import yaml
from matplotlib import pyplot as plt
from matplotlib.patches import Circle, Rectangle
from skyfield.api import Loader, load_file, wgs84

SUN_RADIUS_KM = 695_700.0
MOON_RADIUS_KM = 1_737.4
EARTH_RADIUS_KM = 6_378.137
DANJON_ENLARGEMENT = 1.02
ROOT = Path(__file__).resolve().parent.parent

CONTACT_EVENTS = ("p1", "u1", "max", "u4", "p4", "set")
CONTACT_COLORS = {
    "p1": "#6c757d",
    "u1": "#2a9d8f",
    "max": "#e63946",
    "u4": "#9b5de5",
    "p4": "#264653",
    "set": "#d62828",
}


@dataclass(frozen=True)
class SiteConfig:
    name: str
    latitude_deg: float
    longitude_deg: float
    elevation_m: float
    timezone_name: str


@dataclass(frozen=True)
class CameraConfig:
    model: str
    sensor_width_mm: float
    sensor_height_mm: float
    resolution_width_px: int
    resolution_height_px: int

    @property
    def px_per_mm(self) -> float:
        scale_x = self.resolution_width_px / self.sensor_width_mm
        scale_y = self.resolution_height_px / self.sensor_height_mm
        return (scale_x + scale_y) / 2.0


@dataclass(frozen=True)
class OpticConfig:
    name: str
    focal_length_mm: float
    aperture_f: float


@dataclass(frozen=True)
class SimulationConfig:
    window_minutes: int
    step_seconds: int
    tick_minutes: int
    overlay_stride_ticks: int
    ephemeris_path: str
    temperature_c: float
    pressure_mbar: float


@dataclass(frozen=True)
class FramingConfig:
    pointing_event: str
    auto_top_margin_px: float


@dataclass(frozen=True)
class ValidationPoint:
    altitude_deg: float
    azimuth_deg: float


@dataclass(frozen=True)
class EclipseConfig:
    contacts_local: dict[str, datetime]
    validation_altaz_deg: dict[str, ValidationPoint]


@dataclass(frozen=True)
class AppConfig:
    site: SiteConfig
    camera: CameraConfig
    optics: tuple[OpticConfig, ...]
    simulation: SimulationConfig
    framing: FramingConfig
    eclipse: EclipseConfig

    @property
    def timezone(self) -> ZoneInfo:
        return ZoneInfo(self.site.timezone_name)

    @property
    def pointing_time_local(self) -> datetime:
        event = self.framing.pointing_event.lower()
        try:
            return self.eclipse.contacts_local[event]
        except KeyError as exc:
            options = ", ".join(sorted(self.eclipse.contacts_local))
            raise ValueError(
                f"Unknown pointing event '{self.framing.pointing_event}'. "
                f"Available events: {options}"
            ) from exc


@dataclass(frozen=True)
class CameraBasis:
    right: np.ndarray
    up: np.ndarray
    forward: np.ndarray


@dataclass(frozen=True)
class EphemerisSample:
    when_local: datetime
    sun_alt_deg: float
    sun_az_deg: float
    moon_alt_deg: float
    moon_az_deg: float
    moon_radius_rad: float
    umbra_alt_deg: float
    umbra_az_deg: float
    umbra_radius_rad: float
    penumbra_radius_rad: float


@dataclass(frozen=True)
class ProjectedSample:
    when_local: datetime
    moon_x_px: float
    moon_y_px: float
    moon_radius_px: float
    umbra_x_px: float
    umbra_y_px: float
    umbra_radius_px: float
    penumbra_x_px: float
    penumbra_y_px: float
    penumbra_radius_px: float


def parse_local_datetime(value: str | datetime, tz: ZoneInfo) -> datetime:
    """Parse a local datetime string and attach the provided timezone."""
    if isinstance(value, datetime):
        parsed = value
    else:
        parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=tz)
    return parsed.astimezone(tz)


def load_config(path: Path) -> AppConfig:
    """Load and validate the simulation configuration from YAML."""
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    tz = ZoneInfo(data["site"]["timezone"])

    contacts = {
        key.lower(): parse_local_datetime(value, tz)
        for key, value in data["eclipse"]["contacts_local"].items()
    }
    validation_raw = data["eclipse"].get("validation_altaz_deg") or {}
    validation = {
        key.lower(): ValidationPoint(
            altitude_deg=float(value["alt"]),
            azimuth_deg=float(value["az"]),
        )
        for key, value in validation_raw.items()
    }

    overlay_stride = data["simulation"].get(
        "overlay_stride_ticks",
        data["simulation"].get("crescent_stride_ticks", 1),
    )

    return AppConfig(
        site=SiteConfig(
            name=str(data["site"]["name"]),
            latitude_deg=float(data["site"]["latitude_deg"]),
            longitude_deg=float(data["site"]["longitude_deg"]),
            elevation_m=float(data["site"]["elevation_m"]),
            timezone_name=str(data["site"]["timezone"]),
        ),
        camera=CameraConfig(
            model=str(data["camera"]["model"]),
            sensor_width_mm=float(data["camera"]["sensor_width_mm"]),
            sensor_height_mm=float(data["camera"]["sensor_height_mm"]),
            resolution_width_px=int(data["camera"]["resolution_width_px"]),
            resolution_height_px=int(data["camera"]["resolution_height_px"]),
        ),
        optics=tuple(
            OpticConfig(
                name=str(optic["name"]),
                focal_length_mm=float(optic["focal_length_mm"]),
                aperture_f=float(optic["aperture_f"]),
            )
            for optic in data["optics"]
        ),
        simulation=SimulationConfig(
            window_minutes=int(data["simulation"]["window_minutes"]),
            step_seconds=int(data["simulation"]["step_seconds"]),
            tick_minutes=int(data["simulation"]["tick_minutes"]),
            overlay_stride_ticks=int(overlay_stride),
            ephemeris_path=str(data["simulation"]["ephemeris_path"]),
            temperature_c=float(data["simulation"]["temperature_c"]),
            pressure_mbar=float(data["simulation"]["pressure_mbar"]),
        ),
        framing=FramingConfig(
            pointing_event=str(data["framing"]["pointing_event"]).lower(),
            auto_top_margin_px=float(data["framing"].get("auto_top_margin_px", 0.0)),
        ),
        eclipse=EclipseConfig(
            contacts_local=contacts,
            validation_altaz_deg=validation,
        ),
    )


def normalize(vec: np.ndarray) -> np.ndarray:
    """Return a unit vector."""
    norm = np.linalg.norm(vec)
    if norm == 0:
        raise ValueError("Cannot normalize a zero vector")
    return vec / norm


def altaz_to_unit_vector(alt_deg: float, az_deg: float) -> np.ndarray:
    """Convert local Alt/Az degrees to ENU unit vector (East, North, Up)."""
    alt = math.radians(alt_deg)
    az = math.radians(az_deg)
    east = math.cos(alt) * math.sin(az)
    north = math.cos(alt) * math.cos(az)
    up = math.sin(alt)
    return normalize(np.array([east, north, up], dtype=float))


def anti_sun_altaz(sun_alt_deg: float, sun_az_deg: float) -> tuple[float, float]:
    """Topocentric anti-sun: Earth's shadow axis on the sky."""
    return -sun_alt_deg, (sun_az_deg + 180.0) % 360.0


def shadow_angular_radii_rad(
    sun_distance_km: float,
    moon_distance_km: float,
) -> tuple[float, float]:
    """Umbra and penumbra angular radii at the Moon, Danjon 2 % enlargement.

    Framing overlay only — official contacts stay in the YAML.
    """
    l_umbra = EARTH_RADIUS_KM * sun_distance_km / (SUN_RADIUS_KM - EARTH_RADIUS_KM)
    r_umbra_km = EARTH_RADIUS_KM * (l_umbra - moon_distance_km) / l_umbra
    l_penumbra = EARTH_RADIUS_KM * sun_distance_km / (SUN_RADIUS_KM + EARTH_RADIUS_KM)
    r_penumbra_km = EARTH_RADIUS_KM * (moon_distance_km + l_penumbra) / l_penumbra
    r_umbra_km *= DANJON_ENLARGEMENT
    r_penumbra_km *= DANJON_ENLARGEMENT
    umbra_rad = math.atan(r_umbra_km / moon_distance_km)
    penumbra_rad = math.atan(r_penumbra_km / moon_distance_km)
    return umbra_rad, penumbra_rad


def build_camera_basis(forward: np.ndarray) -> CameraBasis:
    """Build an upright camera basis on the tangent plane."""
    fwd = normalize(forward)
    zenith = np.array([0.0, 0.0, 1.0], dtype=float)
    up = zenith - np.dot(zenith, fwd) * fwd
    if np.linalg.norm(up) < 1e-9:
        north = np.array([0.0, 1.0, 0.0], dtype=float)
        up = north - np.dot(north, fwd) * fwd
    up = normalize(up)
    # Right-handed camera basis: right = forward x up.
    # Using up x forward would mirror the image left/right.
    right = normalize(np.cross(fwd, up))
    return CameraBasis(right=right, up=up, forward=fwd)


def gnomonic_project(target: np.ndarray, basis: CameraBasis) -> tuple[float, float] | None:
    """Project a target direction onto the camera tangent plane."""
    denominator = float(np.dot(target, basis.forward))
    if denominator <= 0:
        return None
    x_tan = float(np.dot(target, basis.right) / denominator)
    y_tan = float(np.dot(target, basis.up) / denominator)
    return x_tan, y_tan


def tangent_to_pixel(
    x_tan: float,
    y_tan: float,
    camera: CameraConfig,
    optic: OpticConfig,
) -> tuple[float, float]:
    """Convert tangent-plane coordinates to sensor pixel coordinates."""
    x_mm = optic.focal_length_mm * x_tan
    y_mm = optic.focal_length_mm * y_tan

    x_px = camera.resolution_width_px / 2 + x_mm * (
        camera.resolution_width_px / camera.sensor_width_mm
    )
    y_px = camera.resolution_height_px / 2 - y_mm * (
        camera.resolution_height_px / camera.sensor_height_mm
    )
    return x_px, y_px


def angular_radius_to_px(
    angular_radius_rad: float,
    camera: CameraConfig,
    optic: OpticConfig,
) -> float:
    """Convert an angular radius to pixel radius for an optic."""
    radius_mm = optic.focal_length_mm * math.tan(angular_radius_rad)
    return radius_mm * camera.px_per_mm


def build_time_grid(
    center_time_local: datetime,
    window_minutes: int,
    step_seconds: int,
) -> list[datetime]:
    """Create regularly sampled times around the center."""
    start = center_time_local - timedelta(minutes=window_minutes)
    stop = center_time_local + timedelta(minutes=window_minutes)
    times: list[datetime] = []
    current = start
    step = timedelta(seconds=step_seconds)
    while current < stop:
        times.append(current)
        current += step
    times.append(stop)
    return times


def build_tick_times(
    center_time_local: datetime,
    window_minutes: int,
    tick_minutes: int,
) -> list[datetime]:
    """Build labeled tick times around the center time."""
    ticks: list[datetime] = []
    start = center_time_local - timedelta(minutes=window_minutes)
    stop = center_time_local + timedelta(minutes=window_minutes)
    current = start
    step = timedelta(minutes=tick_minutes)
    while current <= stop:
        ticks.append(current)
        current += step
    return ticks


def interpolate_zero_crossing(
    times: list[datetime],
    values: list[float],
    target: float = 0.0,
) -> datetime | None:
    """Find the first crossing of a target value using linear interpolation."""
    if len(times) != len(values):
        raise ValueError("times and values must have the same length")
    if len(times) < 2:
        return None

    shifted = [value - target for value in values]
    for index in range(1, len(shifted)):
        prev = shifted[index - 1]
        cur = shifted[index]
        if prev == 0:
            return times[index - 1]
        if prev * cur <= 0:
            dt_seconds = (times[index] - times[index - 1]).total_seconds()
            if dt_seconds == 0:
                return times[index]
            fraction = abs(prev) / (abs(prev) + abs(cur))
            return times[index - 1] + timedelta(seconds=dt_seconds * fraction)
    return None


def sanitize_slug(value: str) -> str:
    """Create a filesystem-friendly slug from a label."""
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


class EphemerisEngine:
    """Skyfield wrapper producing local Moon / anti-sun apparent positions."""

    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.loader = Loader(str(ROOT))
        self.timescale = self.loader.timescale()

        ephemeris_path = Path(config.simulation.ephemeris_path)
        if not ephemeris_path.is_absolute():
            ephemeris_path = ROOT / ephemeris_path

        if ephemeris_path.exists():
            self.ephemeris = load_file(ephemeris_path)
        else:
            self.ephemeris = self.loader(config.simulation.ephemeris_path)

        self.observer = self.ephemeris["earth"] + wgs84.latlon(
            latitude_degrees=config.site.latitude_deg,
            longitude_degrees=config.site.longitude_deg,
            elevation_m=config.site.elevation_m,
        )
        self.sun = self.ephemeris["sun"]
        self.moon = self.ephemeris["moon"]

    def sample(self, when_local: datetime) -> EphemerisSample:
        """Compute one local sample for Moon and Earth's shadow axis."""
        when_utc = when_local.astimezone(timezone.utc)
        t = self.timescale.from_datetime(when_utc)

        sun_apparent = self.observer.at(t).observe(self.sun).apparent()
        moon_apparent = self.observer.at(t).observe(self.moon).apparent()

        sun_alt, sun_az, _ = sun_apparent.altaz(
            temperature_C=self.config.simulation.temperature_c,
            pressure_mbar=self.config.simulation.pressure_mbar,
        )
        moon_alt, moon_az, _ = moon_apparent.altaz(
            temperature_C=self.config.simulation.temperature_c,
            pressure_mbar=self.config.simulation.pressure_mbar,
        )

        sun_distance_km = float(sun_apparent.distance().km)
        moon_distance_km = float(moon_apparent.distance().km)
        moon_radius_rad = math.asin(MOON_RADIUS_KM / moon_distance_km)
        umbra_radius_rad, penumbra_radius_rad = shadow_angular_radii_rad(
            sun_distance_km=sun_distance_km,
            moon_distance_km=moon_distance_km,
        )
        umbra_alt_deg, umbra_az_deg = anti_sun_altaz(
            float(sun_alt.degrees),
            float(sun_az.degrees),
        )

        return EphemerisSample(
            when_local=when_local,
            sun_alt_deg=float(sun_alt.degrees),
            sun_az_deg=float(sun_az.degrees),
            moon_alt_deg=float(moon_alt.degrees),
            moon_az_deg=float(moon_az.degrees),
            moon_radius_rad=moon_radius_rad,
            umbra_alt_deg=umbra_alt_deg,
            umbra_az_deg=umbra_az_deg,
            umbra_radius_rad=umbra_radius_rad,
            penumbra_radius_rad=penumbra_radius_rad,
        )


def project_sample(
    sample: EphemerisSample,
    basis: CameraBasis,
    camera: CameraConfig,
    optic: OpticConfig,
) -> ProjectedSample | None:
    """Project one ephemeris sample into sensor pixel space."""
    moon_vector = altaz_to_unit_vector(sample.moon_alt_deg, sample.moon_az_deg)
    umbra_vector = altaz_to_unit_vector(sample.umbra_alt_deg, sample.umbra_az_deg)

    moon_tangent = gnomonic_project(moon_vector, basis)
    umbra_tangent = gnomonic_project(umbra_vector, basis)
    if moon_tangent is None or umbra_tangent is None:
        return None

    moon_x_px, moon_y_px = tangent_to_pixel(moon_tangent[0], moon_tangent[1], camera, optic)
    umbra_x_px, umbra_y_px = tangent_to_pixel(
        umbra_tangent[0], umbra_tangent[1], camera, optic
    )
    moon_radius_px = angular_radius_to_px(sample.moon_radius_rad, camera, optic)
    umbra_radius_px = angular_radius_to_px(sample.umbra_radius_rad, camera, optic)
    penumbra_radius_px = angular_radius_to_px(sample.penumbra_radius_rad, camera, optic)

    return ProjectedSample(
        when_local=sample.when_local,
        moon_x_px=moon_x_px,
        moon_y_px=moon_y_px,
        moon_radius_px=moon_radius_px,
        umbra_x_px=umbra_x_px,
        umbra_y_px=umbra_y_px,
        umbra_radius_px=umbra_radius_px,
        penumbra_x_px=umbra_x_px,
        penumbra_y_px=umbra_y_px,
        penumbra_radius_px=penumbra_radius_px,
    )


def find_auto_top_time(
    projected_samples: list[ProjectedSample],
    pointing_time_local: datetime,
    margin_px: float,
) -> datetime | None:
    """Find when the lower lunar limb crosses the top sensor edge (y=0)."""
    pre_pointing = [
        sample for sample in projected_samples if sample.when_local <= pointing_time_local
    ]
    if len(pre_pointing) < 2:
        return None

    times = [sample.when_local for sample in pre_pointing]
    values = [sample.moon_y_px + sample.moon_radius_px - margin_px for sample in pre_pointing]
    return interpolate_zero_crossing(times, values, target=0.0)


def find_closest_top_time(
    projected_samples: list[ProjectedSample],
    pointing_time_local: datetime,
    margin_px: float,
) -> datetime | None:
    """Pick the pre-pointing sample closest to top-limb contact."""
    pre_pointing = [
        sample for sample in projected_samples if sample.when_local <= pointing_time_local
    ]
    if not pre_pointing:
        return None
    scored = [
        (abs(sample.moon_y_px + sample.moon_radius_px - margin_px), sample.when_local)
        for sample in pre_pointing
    ]
    scored.sort(key=lambda item: item[0])
    return scored[0][1]


def draw_eclipsed_moon(ax: plt.Axes, sample: ProjectedSample, zorder: int = 6) -> None:
    """Draw the Moon disk with umbra/penumbra clipped to the limb."""
    moon = Circle(
        (sample.moon_x_px, sample.moon_y_px),
        sample.moon_radius_px,
        facecolor=(0.92, 0.90, 0.82, 0.95),
        edgecolor="#3d3d3d",
        linewidth=1.1,
        zorder=zorder,
    )
    ax.add_patch(moon)
    penumbra = Circle(
        (sample.penumbra_x_px, sample.penumbra_y_px),
        sample.penumbra_radius_px,
        facecolor=(0.35, 0.22, 0.18, 0.28),
        edgecolor="none",
        zorder=zorder + 1,
    )
    umbra = Circle(
        (sample.umbra_x_px, sample.umbra_y_px),
        sample.umbra_radius_px,
        facecolor=(0.32, 0.05, 0.05, 0.58),
        edgecolor="#5c1a1a",
        linewidth=0.5,
        zorder=zorder + 2,
    )
    penumbra.set_clip_path(moon)
    umbra.set_clip_path(moon)
    ax.add_patch(penumbra)
    ax.add_patch(umbra)


def compute_ephemeris_samples(
    engine: EphemerisEngine,
    times_local: list[datetime],
) -> list[EphemerisSample]:
    """Evaluate skyfield samples for all provided times."""
    return [engine.sample(when_local) for when_local in times_local]


def project_samples(
    samples: list[EphemerisSample],
    basis: CameraBasis,
    camera: CameraConfig,
    optic: OpticConfig,
) -> list[ProjectedSample]:
    """Project a list of samples and drop points behind camera."""
    projected: list[ProjectedSample] = []
    for sample in samples:
        maybe = project_sample(sample, basis, camera, optic)
        if maybe is not None:
            projected.append(maybe)
    return projected


def validate_reference_points(engine: EphemerisEngine, config: AppConfig) -> list[str]:
    """Validate computed lunar Alt/Az against configured reference points."""
    lines: list[str] = []
    for event, expected in config.eclipse.validation_altaz_deg.items():
        when_local = config.eclipse.contacts_local.get(event)
        if when_local is None:
            continue
        computed = engine.sample(when_local)
        delta_alt_arcmin = (computed.moon_alt_deg - expected.altitude_deg) * 60.0
        delta_az_arcmin = (computed.moon_az_deg - expected.azimuth_deg) * 60.0
        lines.append(
            f"{event.upper():>3} "
            f"dAlt={delta_alt_arcmin:+.2f}' "
            f"dAz={delta_az_arcmin:+.2f}'"
        )
    return lines


def render_optic(
    config: AppConfig,
    optic: OpticConfig,
    projected_samples: list[ProjectedSample],
    tick_samples: list[ProjectedSample],
    contact_samples: dict[str, ProjectedSample],
    auto_top_sample: ProjectedSample,
    output_path: Path,
) -> None:
    """Render one PNG for one optic."""
    camera = config.camera
    fig = plt.figure(figsize=(14, 7))
    grid = fig.add_gridspec(1, 2, width_ratios=[3.2, 1.7])
    ax = fig.add_subplot(grid[0, 0])
    zoom_ax = fig.add_subplot(grid[0, 1])

    ax.set_title(
        f"Trajectoire lunaire | {optic.name} | "
        f"{optic.focal_length_mm:.0f} mm f/{optic.aperture_f:g}"
    )
    ax.set_xlim(0, camera.resolution_width_px)
    ax.set_ylim(camera.resolution_height_px, 0)
    ax.set_aspect("equal")
    ax.add_patch(
        Rectangle(
            (0, 0),
            camera.resolution_width_px,
            camera.resolution_height_px,
            fill=False,
            edgecolor="#666",
            linewidth=1.2,
            zorder=1,
        )
    )
    ax.set_xlabel("x [px]")
    ax.set_ylabel("y [px]")

    trajectory_x = [sample.moon_x_px for sample in projected_samples]
    trajectory_y = [sample.moon_y_px for sample in projected_samples]
    ax.plot(trajectory_x, trajectory_y, color="#0077b6", linewidth=1.7, zorder=2)

    for sample in tick_samples:
        ax.scatter(sample.moon_x_px, sample.moon_y_px, color="#005f73", s=13, zorder=4)
        ax.annotate(
            sample.when_local.strftime("%H:%M"),
            (sample.moon_x_px, sample.moon_y_px),
            xytext=(6, -6),
            textcoords="offset points",
            fontsize=7,
            color="#16324f",
            zorder=4,
        )

    for event in CONTACT_EVENTS:
        sample = contact_samples.get(event)
        if sample is None:
            continue
        ax.scatter(
            sample.moon_x_px,
            sample.moon_y_px,
            color=CONTACT_COLORS[event],
            s=40,
            marker="x",
            linewidths=1.8,
            zorder=7,
        )
        ax.annotate(
            event.upper(),
            (sample.moon_x_px, sample.moon_y_px),
            xytext=(8, 8),
            textcoords="offset points",
            fontsize=8,
            weight="bold",
            color=CONTACT_COLORS[event],
            zorder=7,
        )

    stride = max(1, config.simulation.overlay_stride_ticks)
    overlay_candidates = [
        sample for idx, sample in enumerate(tick_samples) if idx % stride == 0
    ]
    for sample in overlay_candidates:
        draw_eclipsed_moon(ax, sample, zorder=6)

    zoom_ax.set_title("Panneau cadrage (entrée haut de champ)")
    draw_eclipsed_moon(zoom_ax, auto_top_sample, zorder=6)
    zoom_ax.scatter(
        auto_top_sample.moon_x_px,
        auto_top_sample.moon_y_px,
        marker="+",
        color="#00b4d8",
        s=120,
        linewidths=1.6,
        zorder=8,
    )
    zoom_ax.axhline(y=0.0, color="#ef476f", linestyle="--", linewidth=1.2, zorder=2)
    zoom_ax.annotate(
        auto_top_sample.when_local.strftime("Pointage auto-top: %H:%M:%S"),
        (auto_top_sample.moon_x_px, auto_top_sample.moon_y_px),
        xytext=(0, -18),
        textcoords="offset points",
        ha="center",
        fontsize=9,
        color="#264653",
        zorder=9,
    )
    zoom_ax.annotate(
        "Ligne y=0 (bord supérieur capteur)",
        (0, 0),
        xytext=(10, 8),
        textcoords="offset points",
        fontsize=8,
        color="#ef476f",
        zorder=9,
    )

    radius = auto_top_sample.moon_radius_px
    padding = max(2.6 * radius, 80.0)
    zoom_ax.set_xlim(auto_top_sample.moon_x_px - padding, auto_top_sample.moon_x_px + padding)
    zoom_ax.set_ylim(auto_top_sample.moon_y_px + padding, auto_top_sample.moon_y_px - padding)
    zoom_ax.set_aspect("equal")
    zoom_ax.set_xlabel("x [px]")
    zoom_ax.set_ylabel("y [px]")
    zoom_ax.grid(color="#bbb", linestyle=":", linewidth=0.7, alpha=0.6)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=160, bbox_inches="tight")
    plt.close(fig)


def pick_optics(config: AppConfig, selected_names: list[str]) -> tuple[OpticConfig, ...]:
    """Filter optics using one or more --optic names."""
    if not selected_names:
        return config.optics

    lowered = {name.lower() for name in selected_names}
    selected = tuple(optic for optic in config.optics if optic.name.lower() in lowered)
    if not selected:
        names = ", ".join(optic.name for optic in config.optics)
        raise ValueError(f"No matching optic in config. Available optics: {names}")
    return selected


def run(config: AppConfig, output_dir: Path, selected_optics: list[str]) -> int:
    """Main execution for simulation and rendering."""
    engine = EphemerisEngine(config)
    print(
        f"Using site {config.site.name} "
        f"({config.site.latitude_deg:.5f}, {config.site.longitude_deg:.5f}, "
        f"{config.site.elevation_m:.0f} m)"
    )
    print(f"Using ephemeris: {config.simulation.ephemeris_path} (DE421 expected)")

    for line in validate_reference_points(engine, config):
        print(f"Validation {line}")

    pointing_time_local = config.pointing_time_local
    time_grid = build_time_grid(
        center_time_local=pointing_time_local,
        window_minutes=config.simulation.window_minutes,
        step_seconds=config.simulation.step_seconds,
    )
    tick_times = build_tick_times(
        center_time_local=pointing_time_local,
        window_minutes=config.simulation.window_minutes,
        tick_minutes=config.simulation.tick_minutes,
    )

    sampled = compute_ephemeris_samples(engine, time_grid)
    tick_ephemeris = compute_ephemeris_samples(engine, tick_times)
    pointing_sample = engine.sample(pointing_time_local)
    forward = altaz_to_unit_vector(pointing_sample.moon_alt_deg, pointing_sample.moon_az_deg)
    basis = build_camera_basis(forward)

    for optic in pick_optics(config, selected_optics):
        projected = project_samples(sampled, basis, config.camera, optic)
        projected_ticks = project_samples(tick_ephemeris, basis, config.camera, optic)
        if len(projected) < 2:
            raise RuntimeError(f"Not enough projected samples for optic '{optic.name}'")

        projected_contacts: dict[str, ProjectedSample] = {}
        for event in CONTACT_EVENTS:
            contact_time = config.eclipse.contacts_local.get(event)
            if contact_time is None:
                continue
            contact_projection = project_sample(
                engine.sample(contact_time),
                basis,
                config.camera,
                optic,
            )
            if contact_projection is not None:
                projected_contacts[event] = contact_projection

        auto_top_time = find_auto_top_time(
            projected_samples=projected,
            pointing_time_local=pointing_time_local,
            margin_px=config.framing.auto_top_margin_px,
        )
        if auto_top_time is None:
            auto_top_time = find_closest_top_time(
                projected_samples=projected,
                pointing_time_local=pointing_time_local,
                margin_px=config.framing.auto_top_margin_px,
            )
            if auto_top_time is None:
                raise RuntimeError(f"Could not infer framing time for optic '{optic.name}'")
            print(
                f"Info: no strict top-limb crossing for '{optic.name}' within "
                f"the window, using closest approach at {auto_top_time.strftime('%H:%M:%S')}"
            )
        auto_top_projection = project_sample(
            engine.sample(auto_top_time), basis, config.camera, optic
        )
        if auto_top_projection is None:
            raise RuntimeError(
                f"Auto-top sample projects behind camera for optic '{optic.name}'"
            )

        output_file = output_dir / f"fov-{sanitize_slug(optic.name)}.png"
        render_optic(
            config=config,
            optic=optic,
            projected_samples=projected,
            tick_samples=projected_ticks,
            contact_samples=projected_contacts,
            auto_top_sample=auto_top_projection,
            output_path=output_file,
        )
        print(
            f"Wrote {output_file} | auto-top={auto_top_time.strftime('%Y-%m-%d %H:%M:%S %Z')}"
        )

    return 0


def build_arg_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(
        description="Simulate Moon trajectory in camera FOV for lunar-eclipse framing.",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("scripts/config/paris-600d-placeholder.yaml"),
        help="YAML configuration path.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("output/fov"),
        help="Output directory for generated PNG figures.",
    )
    parser.add_argument(
        "--optic",
        action="append",
        default=[],
        help="Optic name from YAML config (repeatable).",
    )
    return parser


def main() -> int:
    """CLI entrypoint."""
    parser = build_arg_parser()
    args = parser.parse_args()
    config = load_config(args.config)
    output_dir = args.out if args.out.is_absolute() else ROOT / args.out
    return run(config=config, output_dir=output_dir, selected_optics=args.optic)


if __name__ == "__main__":
    raise SystemExit(main())
