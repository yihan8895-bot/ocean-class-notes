"""Reproduce the Test 2 Argo dynamic-height and relative-geostrophic case study.

Inputs are six official single-cycle Argo GDAC NetCDF files downloaded from
https://data-argo.ifremer.fr/dac/.  The script applies Argo QC flags, prefers
adjusted variables, converts SP/t/p to TEOS-10 SA/CT, calculates dynamic height
relative to 700 dbar, and estimates section-normal geostrophic velocity.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".mplcache"))

import gsw
import matplotlib

matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr
from matplotlib.colors import TwoSlopeNorm


DATA_DIR = ROOT / "data" / "test2_argo_case"
ASSET_DIR = ROOT / "assets" / "argo"
ASSET_DIR.mkdir(parents=True, exist_ok=True)

FILES = [
    ("A", "aoml/5904747/profiles/R5904747_081.nc"),
    ("B", "csio/2902698/profiles/D2902698_028.nc"),
    ("C", "csio/2902697/profiles/D2902697_025.nc"),
    ("D", "csio/2902695/profiles/D2902695_039.nc"),
    ("E", "csio/2902694/profiles/D2902694_038.nc"),
    ("F", "aoml/2901481/profiles/R2901481_081.nc"),
]
P_GRID = np.arange(10.0, 700.1, 10.0)
P_REF = 700.0


def setup_style() -> None:
    for candidate in (
        Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/msyhbd.ttc"),
        Path("C:/Windows/Fonts/simhei.ttf"),
    ):
        if candidate.exists():
            fm.fontManager.addfont(str(candidate))
            plt.rcParams["font.family"] = fm.FontProperties(fname=str(candidate)).get_name()
            break
    plt.rcParams.update({
        "figure.facecolor": "#f7fbfa",
        "axes.facecolor": "#f7fbfa",
        "axes.edgecolor": "#9db9b5",
        "axes.labelcolor": "#294f59",
        "xtick.color": "#54757d",
        "ytick.color": "#54757d",
        "axes.unicode_minus": False,
        "figure.dpi": 140,
        "savefig.dpi": 200,
    })


def chars(values: np.ndarray) -> np.ndarray:
    return np.char.strip(values.astype("U"))


def select_parameter(ds: xr.Dataset, name: str) -> tuple[np.ndarray, np.ndarray, str]:
    """Prefer adjusted values with QC 1/2, then fill from raw values with QC 1/2."""
    raw = np.asarray(ds[name].values[0], dtype=float)
    raw_qc = chars(np.asarray(ds[f"{name}_QC"].values[0]))
    raw_valid = np.isfinite(raw) & np.isin(raw_qc, ["1", "2"])
    values = np.where(raw_valid, raw, np.nan)
    source = "raw"
    adj_name = f"{name}_ADJUSTED"
    adj_qc_name = f"{name}_ADJUSTED_QC"
    if adj_name in ds and adj_qc_name in ds:
        adjusted = np.asarray(ds[adj_name].values[0], dtype=float)
        adjusted_qc = chars(np.asarray(ds[adj_qc_name].values[0]))
        adj_valid = np.isfinite(adjusted) & np.isin(adjusted_qc, ["1", "2"])
        values = np.where(adj_valid, adjusted, values)
        if np.any(adj_valid):
            source = "adjusted; raw fallback"
    return values, np.isfinite(values), source


def read_profile(station: str, relative_path: str) -> dict:
    path = DATA_DIR / Path(relative_path).name
    with xr.open_dataset(path, decode_cf=True) as ds:
        p, p_ok, p_source = select_parameter(ds, "PRES")
        t, t_ok, t_source = select_parameter(ds, "TEMP")
        sp, s_ok, s_source = select_parameter(ds, "PSAL")
        valid = p_ok & t_ok & s_ok & (p >= 0) & (p <= 2000) & (sp > 0) & (sp < 42)
        p, t, sp = p[valid], t[valid], sp[valid]
        order = np.argsort(p)
        p, t, sp = p[order], t[order], sp[order]
        p, unique_index = np.unique(p, return_index=True)
        t, sp = t[unique_index], sp[unique_index]
        if p.min() > P_GRID.min() or p.max() < P_REF:
            raise ValueError(f"{station}: pressure range {p.min():.1f}-{p.max():.1f} dbar cannot support 10-{P_REF:.0f} dbar")

        lon = float(ds["LONGITUDE"].values[0])
        lat = float(ds["LATITUDE"].values[0])
        time = pd.Timestamp(ds["JULD"].values[0]).isoformat()
        mode = chars(np.asarray(ds["DATA_MODE"].values))[0]
        wmo = "".join(chars(np.asarray(ds["PLATFORM_NUMBER"].values)).ravel()).strip()

    t_i = np.interp(P_GRID, p, t)
    sp_i = np.interp(P_GRID, p, sp)
    sa = gsw.SA_from_SP(sp_i, P_GRID, lon, lat)
    ct = gsw.CT_from_t(sa, t_i, P_GRID)
    sigma0 = gsw.sigma0(sa, ct)
    dynamic_height = np.asarray(
        gsw.geo_strf_dyn_height(sa, ct, P_GRID, p_ref=P_REF, axis=0, max_dp=1.0),
        dtype=float,
    )
    return {
        "station": station,
        "file": path.name,
        "relative_path": relative_path,
        "wmo": wmo,
        "time": time,
        "longitude": lon,
        "latitude": lat,
        "data_mode": mode,
        "parameter_source": f"P:{p_source}; T:{t_source}; S:{s_source}",
        "observed_p_min": float(p.min()),
        "observed_p_max": float(p.max()),
        "temperature": t_i,
        "practical_salinity": sp_i,
        "absolute_salinity": sa,
        "conservative_temperature": ct,
        "sigma0": sigma0,
        "dynamic_height": dynamic_height,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def cumulative_distance(lon: np.ndarray, lat: np.ndarray) -> np.ndarray:
    distances = np.zeros(lon.size)
    for index in range(1, lon.size):
        segment = float(gsw.distance(lon[index - 1:index + 1], lat[index - 1:index + 1])[0])
        distances[index] = distances[index - 1] + segment / 1000.0
    return distances


def save_figure(
    profiles: list[dict], distance: np.ndarray, velocity: np.ndarray,
    mid_lon: np.ndarray, mid_lat: np.ndarray, language: str,
) -> Path:
    labels = {
        "en": {
            "title": "Observed Density Structure to Relative Geostrophic Current",
            "subtitle": "Six Argo profiles, South China Sea, 13-16 March 2017 | TEOS-10 | reference = 700 dbar",
            "map": "(a) Quasi-synoptic station path",
            "dh": "(b) Dynamic height relative to 700 dbar",
            "vel": "(c) Section-normal geostrophic velocity relative to 700 dbar",
            "x": "Distance along A-F section (km)",
            "p": "Pressure (dbar)",
            "dhx": "Dynamic height anomaly (m$^2$ s$^{-2}$)",
            "cb": "Relative geostrophic velocity (m s$^{-1}$)",
            "note": "Positive velocity points to the left of the local A-F path. Values are relative to 700 dbar, not absolute current.",
            "station": "Station",
        },
        "zh": {
            "title": "从观测密度结构到相对地转流",
            "subtitle": "南海六个 Argo 剖面，2017年3月13-16日 | TEOS-10 | 参考层 = 700 dbar",
            "map": "(a) 准同步测站路径",
            "dh": "(b) 相对于700 dbar的动力高度",
            "vel": "(c) 相对于700 dbar的断面法向地转流速",
            "x": "沿 A-F 断面距离 (km)",
            "p": "压力 (dbar)",
            "dhx": "动力高度异常 (m$^2$ s$^{-2}$)",
            "cb": "相对地转流速 (m s$^{-1}$)",
            "note": "正值指向局部 A-F 路径左侧；流速以700 dbar为参考，并非绝对流速。",
            "station": "测站",
        },
    }[language]

    lon = np.array([p["longitude"] for p in profiles])
    lat = np.array([p["latitude"] for p in profiles])
    dynamic_height = np.column_stack([p["dynamic_height"] for p in profiles])
    stations = [p["station"] for p in profiles]

    fig = plt.figure(figsize=(15.7, 10.2), constrained_layout=True)
    grid = fig.add_gridspec(2, 2, height_ratios=[0.86, 1.25], width_ratios=[0.82, 1.35])
    ax_map = fig.add_subplot(grid[0, 0])
    ax_dh = fig.add_subplot(grid[0, 1])
    ax_vel = fig.add_subplot(grid[1, :])

    ax_map.plot(lon, lat, color="#d66536", linewidth=2.2, zorder=2)
    ax_map.scatter(lon, lat, s=70, color="#087f7a", edgecolor="white", linewidth=1.2, zorder=3)
    for station, x_value, y_value in zip(stations, lon, lat):
        ax_map.text(x_value, y_value + 0.10, station, ha="center", fontsize=10, fontweight="bold")
    ax_map.set(xlabel="Longitude (deg E)", ylabel="Latitude (deg N)", title=labels["map"])
    ax_map.grid(alpha=0.3)

    colors = plt.cm.viridis(np.linspace(0.05, 0.9, len(profiles)))
    for profile, color in zip(profiles, colors):
        ax_dh.plot(profile["dynamic_height"], P_GRID, color=color, linewidth=2.0, label=profile["station"])
    ax_dh.invert_yaxis()
    ax_dh.set(xlabel=labels["dhx"], ylabel=labels["p"], title=labels["dh"])
    ax_dh.grid(alpha=0.25)
    ax_dh.legend(ncol=3, frameon=False, title=labels["station"])

    vmax = max(0.05, float(np.nanmax(np.abs(velocity[:-1]))))
    norm = TwoSlopeNorm(vmin=-vmax, vcenter=0, vmax=vmax)
    p_edges = np.r_[P_GRID[0] - 5, 0.5 * (P_GRID[:-1] + P_GRID[1:]), P_GRID[-1] + 5]
    mesh = ax_vel.pcolormesh(distance, p_edges, velocity, cmap="RdBu_r", norm=norm, shading="flat")
    ax_vel.invert_yaxis()
    ax_vel.set(xlabel=labels["x"], ylabel=labels["p"], title=labels["vel"])
    ax_vel.set_xticks(distance, stations)
    for station_x in distance:
        ax_vel.axvline(station_x, color="white", linewidth=0.7, alpha=0.7)
    colorbar = fig.colorbar(mesh, ax=ax_vel, pad=0.012)
    colorbar.set_label(labels["cb"])
    ax_vel.text(
        0.01, 0.985, labels["note"], transform=ax_vel.transAxes, va="top", fontsize=9,
        color="#163f4a", bbox=dict(boxstyle="round,pad=.35", facecolor="white", alpha=.90, edgecolor="#9ebfc0"),
    )

    fig.suptitle(labels["title"] + "\n" + labels["subtitle"], fontsize=17, fontweight="bold", color="#082f3d")
    suffix = "-en" if language == "en" else ""
    target = ASSET_DIR / f"test2_scs_relative_geostrophic_velocity{suffix}.png"
    fig.savefig(target, bbox_inches="tight")
    plt.close(fig)
    return target


def main() -> None:
    setup_style()
    profiles = [read_profile(station, path) for station, path in FILES]
    lon = np.array([p["longitude"] for p in profiles])
    lat = np.array([p["latitude"] for p in profiles])
    distance = cumulative_distance(lon, lat)
    dynamic_height = np.column_stack([p["dynamic_height"] for p in profiles])
    # The optional pressure term only makes a tiny correction to station spacing;
    # omit it so one horizontal distance is used consistently at every level.
    velocity, mid_lon, mid_lat = gsw.geostrophic_velocity(dynamic_height, lon, lat, axis=0)
    velocity = np.asarray(velocity, dtype=float)

    if dynamic_height.shape != (P_GRID.size, len(profiles)):
        raise AssertionError("unexpected dynamic-height matrix shape")
    if velocity.shape != (P_GRID.size, len(profiles) - 1):
        raise AssertionError("unexpected velocity matrix shape")
    if not np.allclose(dynamic_height[-1], 0.0, atol=1e-10):
        raise AssertionError("dynamic height must be zero at the reference pressure")
    if not np.allclose(velocity[-1], 0.0, atol=1e-10):
        raise AssertionError("relative velocity must be zero at the reference pressure")
    if not (np.diff(distance) > 0).all():
        raise AssertionError("station distance must increase")
    if np.any(np.abs(velocity) > 3.0):
        raise AssertionError("implausibly large geostrophic velocity")

    profile_rows = []
    for profile, station_distance in zip(profiles, distance):
        for level_index, pressure in enumerate(P_GRID):
            profile_rows.append({
                "station": profile["station"],
                "wmo": profile["wmo"],
                "date_utc": profile["time"],
                "longitude_east": profile["longitude"],
                "latitude_north": profile["latitude"],
                "distance_km": station_distance,
                "pressure_dbar": pressure,
                "temperature_degC": profile["temperature"][level_index],
                "practical_salinity": profile["practical_salinity"][level_index],
                "absolute_salinity_g_kg": profile["absolute_salinity"][level_index],
                "conservative_temperature_degC": profile["conservative_temperature"][level_index],
                "sigma0_kg_m3": profile["sigma0"][level_index],
                "dynamic_height_m2_s2_ref_700dbar": profile["dynamic_height"][level_index],
            })
    pd.DataFrame(profile_rows).to_csv(
        ASSET_DIR / "test2_argo_dynamic_height_profiles.csv", index=False, encoding="utf-8-sig"
    )

    pair_rows = []
    pair_names = []
    for pair_index in range(len(profiles) - 1):
        pair_name = f"{profiles[pair_index]['station']}-{profiles[pair_index + 1]['station']}"
        pair_names.append(pair_name)
        for level_index, pressure in enumerate(P_GRID):
            pair_rows.append({
                "station_pair": pair_name,
                "midpoint_longitude_east": mid_lon[pair_index],
                "midpoint_latitude_north": mid_lat[pair_index],
                "segment_distance_km": distance[pair_index + 1] - distance[pair_index],
                "pressure_dbar": pressure,
                "relative_geostrophic_velocity_m_s": velocity[level_index, pair_index],
                "sign_convention": "positive points left of local A-to-F path",
                "reference_pressure_dbar": P_REF,
            })
    pd.DataFrame(pair_rows).to_csv(
        ASSET_DIR / "test2_argo_relative_geostrophic_velocity.csv", index=False, encoding="utf-8-sig"
    )

    valid_depth = P_GRID <= 500
    max_index = np.unravel_index(np.nanargmax(np.abs(velocity[valid_depth])), velocity[valid_depth].shape)
    surface_velocity = velocity[0]
    manifest = {
        "title": "Test 2 South China Sea Argo geostrophic case study",
        "source": "Argo GDAC (Coriolis mirror)",
        "source_root": "https://data-argo.ifremer.fr/dac/",
        "argo_doi": "10.17882/42182",
        "retrieved_utc_date": "2026-10-20",
        "method": {
            "qc": "Adjusted PRES/TEMP/PSAL with QC 1 or 2 where available; raw QC 1 or 2 as fallback",
            "interpolation": "Linear interpolation to 10 dbar levels from 10 to 700 dbar; no extrapolation",
            "thermodynamics": "TEOS-10 GSW: SA_from_SP, CT_from_t, sigma0",
            "dynamic_height": "gsw.geo_strf_dyn_height with p_ref=700 dbar and max_dp=1 dbar",
            "velocity": "gsw.geostrophic_velocity between successive stations",
            "sign": "Positive velocity points left of the local A-to-F station path",
        },
        "stations": [
            {
                key: profile[key] for key in (
                    "station", "file", "relative_path", "wmo", "time", "longitude", "latitude",
                    "data_mode", "parameter_source", "observed_p_min", "observed_p_max", "sha256",
                )
            }
            for profile in profiles
        ],
        "section": {
            "cumulative_distance_km": distance.tolist(),
            "segment_distance_km": np.diff(distance).tolist(),
            "station_pairs": pair_names,
            "reference_pressure_dbar": P_REF,
            "near_surface_10dbar_velocity_m_s": surface_velocity.tolist(),
            "near_surface_range_m_s": [float(np.min(surface_velocity)), float(np.max(surface_velocity))],
            "max_abs_velocity_10_500dbar_m_s": float(np.abs(velocity[valid_depth])[max_index]),
            "max_abs_velocity_pair": pair_names[max_index[1]],
            "max_abs_velocity_pressure_dbar": float(P_GRID[valid_depth][max_index[0]]),
        },
        "limitations": [
            "Profiles span approximately four days and the path is irregular, so temporal evolution can alias spatial gradients.",
            "Velocity is normal to each local station segment and referenced to 700 dbar.",
            "An independent velocity or validated level of no motion is required for absolute current.",
            "Argo spacing cannot resolve narrow fronts, tides, inertial currents, Ekman flow, or other ageostrophic motions.",
        ],
    }
    (ASSET_DIR / "test2_argo_geostrophic_summary.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    save_figure(profiles, distance, velocity, mid_lon, mid_lat, "zh")
    save_figure(profiles, distance, velocity, mid_lon, mid_lat, "en")
    print(json.dumps(manifest["section"], indent=2))


if __name__ == "__main__":
    main()
