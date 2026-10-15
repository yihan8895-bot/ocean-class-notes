"""Download, quality-control and visualize 2016-2025 South China Sea Argo profiles.

Data access: Argovis API through argopy. Argovis is listed by the Argo Program
as an access and visualization service. The returned physical profiles are
curated by Argovis/argopy. This script additionally filters position/time QC,
removes implausible values, rejects profiles without adequate vertical support,
and never extrapolates beyond the observed pressure range.

Thermodynamics: TEOS-10 GSW (SA, CT, sigma0 and in-situ density).
"""

from __future__ import annotations

import json
import math
import os
import sys
import time
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PYDEPS = ROOT / ".pydeps"
if PYDEPS.exists():
    sys.path.insert(0, str(PYDEPS))
os.environ.setdefault("ARGOPY_CACHEDIR", str(ROOT / ".cache" / "argopy"))
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".cache" / "matplotlib"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr
from matplotlib.colors import TwoSlopeNorm
from PIL import Image
from scipy.interpolate import griddata
from scipy.stats import linregress

import gsw
from argopy import DataFetcher

warnings.filterwarnings("ignore", message="'argovis' as a 'src' option")


@dataclass(frozen=True)
class Config:
    lon_min: float = 99.0
    lon_max: float = 122.0
    lat_min: float = 0.0
    lat_max: float = 25.0
    p_min: float = 0.0
    p_max: float = 2000.0
    start_year: int = 2016
    end_year: int = 2025
    pressure_levels: tuple[float, ...] = (
        0, 10, 20, 30, 50, 75, 100, 150, 200, 300, 500, 750, 1000, 1500, 2000
    )


CFG = Config()
DATA_DIR = ROOT / "data" / "argo_scs_2016_2025"
ASSET_DIR = ROOT.parent / "assets" / "argo"
FRAME_DIR = DATA_DIR / "frames"
CHUNK_DIR = DATA_DIR / "chunks"
for folder in (DATA_DIR, ASSET_DIR, FRAME_DIR, CHUNK_DIR, ROOT / ".cache" / "argopy", ROOT / ".cache" / "matplotlib"):
    folder.mkdir(parents=True, exist_ok=True)


class NoDataMonth(RuntimeError):
    """Argovis returned a JSON null response for the requested month."""


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
        "axes.unicode_minus": False,
        "figure.dpi": 140,
        "savefig.dpi": 180,
        "axes.facecolor": "#f7fbfa",
        "figure.facecolor": "#f7fbfa",
        "axes.edgecolor": "#9db9b5",
        "axes.labelcolor": "#294f59",
        "xtick.color": "#54757d",
        "ytick.color": "#54757d",
        "grid.color": "#cbdedb",
        "grid.alpha": 0.55,
    })


def clean_qc(values: pd.Series) -> pd.Series:
    return values.astype(str).str.strip().str.replace(".0", "", regex=False)


def fetch_chunk(start: pd.Timestamp, end: pd.Timestamp, attempts: int = 3) -> xr.Dataset:
    box = [
        CFG.lon_min, CFG.lon_max, CFG.lat_min, CFG.lat_max,
        CFG.p_min, CFG.p_max, start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")
    ]
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            return DataFetcher(src="argovis", ds="phy").region(box).to_xarray()
        except TypeError as exc:
            if "NoneType" in str(exc) and "len" in str(exc):
                raise NoDataMonth(f"No Argovis profiles for {start.date()}..{end.date()}") from exc
            last_error = exc
        except Exception as exc:  # network/API errors are retried deterministically
            last_error = exc
            print(f"retry {attempt}/{attempts}: {start.date()}..{end.date()} -> {exc}", flush=True)
            time.sleep(3 * attempt)
    raise RuntimeError(f"Argo fetch failed for {start.date()}..{end.date()}") from last_error


def interpolate_profile(group: pd.DataFrame, levels: np.ndarray) -> dict[str, np.ndarray] | None:
    group = group.sort_values("PRES").copy()
    p = pd.to_numeric(group["PRES"], errors="coerce").to_numpy(float)
    t = pd.to_numeric(group["TEMP"], errors="coerce").to_numpy(float)
    sp = pd.to_numeric(group["PSAL"], errors="coerce").to_numpy(float)
    valid = (
        np.isfinite(p) & np.isfinite(t) & np.isfinite(sp)
        & (p >= CFG.p_min) & (p <= CFG.p_max)
        & (t >= -2.5) & (t <= 40.0)
        & (sp >= 0.0) & (sp <= 42.0)
    )
    p, t, sp = p[valid], t[valid], sp[valid]
    if p.size < 5:
        return None
    order = np.argsort(p)
    p, t, sp = p[order], t[order], sp[order]
    unique_p, unique_index = np.unique(p, return_index=True)
    p, t, sp = unique_p, t[unique_index], sp[unique_index]
    if p.size < 5 or np.ptp(p) < 20:
        return None

    lon = float(group["LONGITUDE"].iloc[0])
    lat = float(group["LATITUDE"].iloc[0])
    sa = gsw.SA_from_SP(sp, p, lon, lat)
    ct = gsw.CT_from_t(sa, t, p)

    inside = (levels >= p.min()) & (levels <= p.max())
    def interp(values: np.ndarray) -> np.ndarray:
        out = np.full(levels.shape, np.nan, dtype=float)
        out[inside] = np.interp(levels[inside], p, values)
        return out

    temp_i = interp(t)
    psal_i = interp(sp)
    sa_i = interp(sa)
    ct_i = interp(ct)
    sigma0 = gsw.sigma0(sa_i, ct_i)
    density = gsw.rho(sa_i, ct_i, levels)
    return {
        "temperature": temp_i,
        "practical_salinity": psal_i,
        "absolute_salinity": sa_i,
        "conservative_temperature": ct_i,
        "sigma0": sigma0,
        "density": density,
    }


def dataset_to_standard_profiles(ds: xr.Dataset) -> xr.Dataset:
    fields = [
        "PRES", "TEMP", "PSAL", "LATITUDE", "LONGITUDE", "TIME",
        "PLATFORM_NUMBER", "CYCLE_NUMBER", "DIRECTION", "DATA_MODE",
        "POSITION_QC", "TIME_QC",
    ]
    data = {name: ds[name].values for name in fields if name in ds}
    frame = pd.DataFrame(data)
    if "POSITION_QC" in frame:
        frame = frame[clean_qc(frame["POSITION_QC"]).isin({"1", "2"})]
    if "TIME_QC" in frame:
        frame = frame[clean_qc(frame["TIME_QC"]).isin({"1", "2"})]
    frame = frame.dropna(subset=["PRES", "TEMP", "PSAL", "LATITUDE", "LONGITUDE", "TIME"])
    frame["TIME"] = pd.to_datetime(frame["TIME"], utc=True).dt.tz_localize(None)
    keys = ["PLATFORM_NUMBER", "CYCLE_NUMBER", "DIRECTION", "TIME"]
    levels = np.asarray(CFG.pressure_levels, dtype=float)
    meta: list[dict] = []
    values: dict[str, list[np.ndarray]] = {
        name: [] for name in (
            "temperature", "practical_salinity", "absolute_salinity",
            "conservative_temperature", "sigma0", "density"
        )
    }
    for key, group in frame.groupby(keys, sort=False, dropna=False):
        profile = interpolate_profile(group, levels)
        if profile is None:
            continue
        modes = group["DATA_MODE"].astype(str).str.strip()
        mode = modes.mode().iloc[0] if not modes.mode().empty else "?"
        meta.append({
            "platform": str(key[0]).strip(),
            "cycle": int(key[1]),
            "direction": str(key[2]).strip(),
            "time": np.datetime64(key[3]),
            "latitude": float(group["LATITUDE"].iloc[0]),
            "longitude": float(group["LONGITUDE"].iloc[0]),
            "data_mode": mode,
            "observed_pmin": float(group["PRES"].min()),
            "observed_pmax": float(group["PRES"].max()),
        })
        for name, array in profile.items():
            values[name].append(array)
    if not meta:
        return xr.Dataset(coords={"profile": np.arange(0), "pressure": levels})
    coords = {
        "profile": np.arange(len(meta)),
        "pressure": levels,
        "time": ("profile", np.array([m["time"] for m in meta], dtype="datetime64[ns]")),
        "latitude": ("profile", [m["latitude"] for m in meta]),
        "longitude": ("profile", [m["longitude"] for m in meta]),
        "platform": ("profile", np.array([m["platform"] for m in meta], dtype=str)),
        "cycle": ("profile", [m["cycle"] for m in meta]),
        "direction": ("profile", np.array([m["direction"] for m in meta], dtype=str)),
        "data_mode": ("profile", np.array([m["data_mode"] for m in meta], dtype=str)),
    }
    out = xr.Dataset(coords=coords)
    for name, arrays in values.items():
        out[name] = (("profile", "pressure"), np.vstack(arrays).astype("float32"))
    out["observed_pmin"] = ("profile", [m["observed_pmin"] for m in meta])
    out["observed_pmax"] = ("profile", [m["observed_pmax"] for m in meta])
    out.attrs.update({
        "title": "South China Sea Argo profiles interpolated to standard pressure levels",
        "source": "Argovis API via argopy; Argo DOI 10.17882/42182",
        "processing": "Curated physical data; position/time QC 1-2; physical range filter; no extrapolation; TEOS-10 GSW",
        "region": "99-122E, 0-25N",
    })
    return out


def process_year(year: int) -> Path:
    target = DATA_DIR / f"argo_scs_{year}_standard.nc"
    if target.exists():
        print(f"reuse {target.name}", flush=True)
        return target
    chunks: list[xr.Dataset] = []
    # One-month requests stay well below common API response limits and avoid
    # silently truncated quarter-sized responses.
    starts = pd.date_range(
        f"{year}-01-01", f"{year + 1}-01-01", freq="MS", inclusive="left"
    )
    for start in starts:
        end = min(start + pd.DateOffset(months=1), pd.Timestamp(f"{year + 1}-01-01"))
        chunk_path = CHUNK_DIR / f"argo_scs_{start:%Y%m%d}_{end:%Y%m%d}.nc"
        no_data_path = chunk_path.with_suffix(".nodata")
        if chunk_path.exists():
            print(f"reuse chunk {chunk_path.name}", flush=True)
            standard = xr.load_dataset(chunk_path)
            raw_count = "cached"
        elif no_data_path.exists():
            print(f"reuse no-data marker {no_data_path.name}", flush=True)
            continue
        else:
            print(f"fetch {start.date()}..{end.date()}", flush=True)
            try:
                raw = fetch_chunk(start, end)
            except NoDataMonth as exc:
                no_data_path.write_text(str(exc), encoding="utf-8")
                print(f"  no profiles: {exc}", flush=True)
                continue
            except RuntimeError as exc:
                # Argovis currently returns JSON null for a valid query with no
                # matching profiles. It is retried above before being recorded
                # as a no-data month here.
                print(f"  no retrievable profiles: {exc}", flush=True)
                continue
            raw_count = f"{raw.sizes.get('N_POINTS', 0):,}"
            standard = dataset_to_standard_profiles(raw)
            if standard.sizes.get("profile", 0):
                standard.to_netcdf(chunk_path)
        if standard.sizes.get("profile", 0):
            chunks.append(standard)
            print(f"  {raw_count} levels -> {standard.sizes['profile']:,} profiles", flush=True)
    if not chunks:
        raise RuntimeError(f"No valid profiles for {year}")
    combined = xr.concat(chunks, dim="profile")
    keys = np.array([
        f"{p}|{c}|{d}|{np.datetime_as_string(t, unit='s')}"
        for p, c, d, t in zip(
            combined.platform.values, combined.cycle.values,
            combined.direction.values, combined.time.values
        )
    ])
    _, keep = np.unique(keys, return_index=True)
    combined = combined.isel(profile=np.sort(keep)).assign_coords(profile=np.arange(len(keep)))
    combined.attrs["year"] = year
    combined.to_netcdf(target)
    print(f"saved {target.name}: {combined.sizes['profile']:,} profiles", flush=True)
    return target


def load_all_years(paths: list[Path]) -> xr.Dataset:
    datasets = [xr.load_dataset(path) for path in paths]
    combined = xr.concat(datasets, dim="profile")
    return combined.assign_coords(profile=np.arange(combined.sizes["profile"]))


def coastlines() -> tuple[np.ndarray, np.ndarray]:
    path = ROOT / "coastlines.csv"
    if not path.exists():
        return np.array([]), np.array([])
    coast = np.loadtxt(path, delimiter=",")
    return coast[:, 0], coast[:, 1]


def map_base(ax: plt.Axes, title: str) -> None:
    lon, lat = coastlines()
    if lon.size:
        ax.plot(lon, lat, color="#4f6f73", linewidth=0.65, zorder=4)
    ax.set_xlim(CFG.lon_min, CFG.lon_max)
    ax.set_ylim(CFG.lat_min, CFG.lat_max)
    ax.set_xlabel("经度 / Longitude (°E)")
    ax.set_ylabel("纬度 / Latitude (°N)")
    ax.set_title(title, loc="left", fontsize=12, fontweight="bold", color="#123d4a")
    ax.grid(True, linewidth=0.6)


def grid_profile_values(ds: xr.Dataset, variable: str, pressure: float, year: int | None = None, step: float = 2.0):
    p_index = int(np.argmin(np.abs(ds.pressure.values - pressure)))
    values = ds[variable].isel(pressure=p_index).values
    lon = ds.longitude.values
    lat = ds.latitude.values
    time_values = pd.DatetimeIndex(ds.time.values)
    mask = np.isfinite(values)
    if year is not None:
        mask &= time_values.year == year
    lon, lat, values = lon[mask], lat[mask], values[mask]
    lon_edges = np.arange(CFG.lon_min, CFG.lon_max + step, step)
    lat_edges = np.arange(CFG.lat_min, CFG.lat_max + step, step)
    lon_centers = (lon_edges[:-1] + lon_edges[1:]) / 2
    lat_centers = (lat_edges[:-1] + lat_edges[1:]) / 2
    grid = np.full((len(lat_centers), len(lon_centers)), np.nan)
    count = np.zeros_like(grid)
    ix = np.digitize(lon, lon_edges) - 1
    iy = np.digitize(lat, lat_edges) - 1
    for row in range(len(lat_centers)):
        for col in range(len(lon_centers)):
            subset = values[(iy == row) & (ix == col)]
            subset = subset[np.isfinite(subset)]
            count[row, col] = subset.size
            if subset.size >= 3:
                grid[row, col] = np.nanmean(subset)
    return lon_centers, lat_centers, grid, count


def plot_coverage(ds: xr.Dataset) -> None:
    years = pd.DatetimeIndex(ds.time.values).year
    counts = pd.Series(years).value_counts().sort_index().reindex(range(CFG.start_year, CFG.end_year + 1), fill_value=0)
    modes = pd.Series(ds.data_mode.values.astype(str)).value_counts()
    fig, axes = plt.subplots(1, 2, figsize=(13.5, 5.6), constrained_layout=True)
    ax = axes[0]
    map_base(ax, "(a) Argo 剖面位置 / Profile locations")
    scatter = ax.scatter(ds.longitude, ds.latitude, c=years, s=8, alpha=0.58, cmap="viridis", edgecolors="none", zorder=3)
    cbar = fig.colorbar(scatter, ax=ax, pad=0.02)
    cbar.set_label("观测年份 / Observation year")
    ax = axes[1]
    bars = ax.bar(counts.index.astype(str), counts.values, color="#0e8b83")
    ax.bar_label(bars, fontsize=8, padding=3)
    ax.set_title("(b) 各年有效标准化剖面 / Valid standardized profiles", loc="left", fontsize=12, fontweight="bold", color="#123d4a")
    ax.set_ylabel("剖面数 / Number of profiles")
    ax.tick_params(axis="x", rotation=45)
    ax.grid(axis="y")
    mode_text = " · ".join(f"{key}: {value:,}" for key, value in modes.items())
    ax.text(0.98, 0.97, f"数据模式 / DATA_MODE\n{mode_text}", transform=ax.transAxes, va="top", ha="right", fontsize=9,
            bbox=dict(boxstyle="round,pad=.5", facecolor="#e7f4f1", edgecolor="#9ac9c1"))
    fig.suptitle("2016–2025 南海 Argo 观测覆盖 / South China Sea Argo Coverage", fontsize=17, fontweight="bold", color="#082f3d")
    fig.savefig(ASSET_DIR / "argo_scs_coverage_2016_2025.png", bbox_inches="tight")
    plt.close(fig)


def plot_vertical_climatology(ds: xr.Dataset) -> None:
    variables = [
        ("temperature", "温度 / Temperature", "°C", "#df6b34"),
        ("practical_salinity", "实用盐度 / Practical salinity", "", "#1672a5"),
        ("sigma0", r"位势密度异常 $\sigma_0$ / Potential density anomaly", r"kg m$^{-3}$", "#158878"),
    ]
    seasons = {
        "冬 / DJF": ([12, 1, 2], "#276d9f"),
        "春 / MAM": ([3, 4, 5], "#44a56d"),
        "夏 / JJA": ([6, 7, 8], "#e36f35"),
        "秋 / SON": ([9, 10, 11], "#8b62a7"),
    }
    months = pd.DatetimeIndex(ds.time.values).month
    pressure = ds.pressure.values
    fig, axes = plt.subplots(1, 3, figsize=(14, 7.2), sharey=True)
    for ax, (var, title, unit, base_color) in zip(axes, variables):
        all_values = ds[var].values
        level_mask = (pressure <= 1000) & (np.sum(np.isfinite(all_values), axis=0) >= 20)
        selected_pressure = pressure[level_mask]
        all_values = all_values[:, level_mask]
        mean = np.nanmean(all_values, axis=0)
        q25 = np.nanpercentile(all_values, 25, axis=0)
        q75 = np.nanpercentile(all_values, 75, axis=0)
        ax.fill_betweenx(selected_pressure, q25, q75, color=base_color, alpha=0.13, label="四分位范围 / IQR")
        ax.plot(mean, selected_pressure, color=base_color, linewidth=3, label="十年平均 / 10-year mean")
        for label, (month_list, color) in seasons.items():
            season_mean = np.nanmean(all_values[np.isin(months, month_list)], axis=0)
            ax.plot(season_mean, selected_pressure, color=color, linewidth=1.25, alpha=0.85, label=label)
        ax.set_ylim(1000, 0)
        ax.set_xlabel(f"{title}\n{unit}")
        ax.set_title(title, fontsize=12, fontweight="bold", color="#123d4a")
        ax.grid(True)
    axes[0].set_ylabel("海水压力 / Sea pressure (dbar)")
    handles, labels = axes[-1].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(0.5, 0.012))
    fig.suptitle("南海十年温盐密垂向气候态 / 2016–2025 Vertical T–S–Density Climatology", fontsize=17, fontweight="bold", color="#082f3d")
    fig.tight_layout(rect=[0, .12, 1, .94])
    fig.savefig(ASSET_DIR / "argo_scs_vertical_climatology.png", bbox_inches="tight")
    plt.close(fig)


def plot_ts_diagram(ds: xr.Dataset) -> None:
    sp = ds.practical_salinity.values.ravel()
    temp = ds.temperature.values.ravel()
    pres = np.broadcast_to(ds.pressure.values, ds.temperature.shape).ravel()
    valid = np.isfinite(sp) & np.isfinite(temp) & np.isfinite(pres) & (pres <= 1000)
    sp, temp, pres = sp[valid], temp[valid], pres[valid]
    if sp.size > 70000:
        rng = np.random.default_rng(42)
        take = rng.choice(sp.size, 70000, replace=False)
        sp, temp, pres = sp[take], temp[take], pres[take]
    s_grid = np.linspace(max(20, np.nanpercentile(sp, .5)), min(38, np.nanpercentile(sp, 99.5)), 120)
    t_grid = np.linspace(max(-2, np.nanpercentile(temp, .5)), min(35, np.nanpercentile(temp, 99.5)), 120)
    ss, tt = np.meshgrid(s_grid, t_grid)
    # Educational isopycnals at representative South China Sea coordinates and sea pressure.
    sa_grid = gsw.SA_from_SP(ss, 0, 112, 15)
    ct_grid = gsw.CT_from_t(sa_grid, tt, 0)
    sigma_grid = gsw.sigma0(sa_grid, ct_grid)
    fig, ax = plt.subplots(figsize=(9.8, 7.2), constrained_layout=True)
    points = ax.scatter(sp, temp, c=pres, s=4, alpha=.22, cmap="viridis_r", rasterized=True)
    contours = ax.contour(ss, tt, sigma_grid, colors="#365e66", linewidths=.8, levels=np.arange(18, 30, 1))
    ax.clabel(contours, fontsize=8, fmt="sigma0 %.0f")
    cbar = fig.colorbar(points, ax=ax)
    cbar.set_label("压力 / Pressure (dbar)")
    ax.set_xlabel("实用盐度 / Practical salinity")
    ax.set_ylabel("原位温度 / In-situ temperature (°C)")
    ax.set_xlim(s_grid.min() - .15, s_grid.max() + .15)
    ax.set_ylim(t_grid.min() - .5, t_grid.max() + .5)
    ax.set_title("温盐关系与等密度线 / T–S Diagram With Isopycnals", loc="left", fontsize=15, fontweight="bold", color="#082f3d")
    ax.grid(True)
    ax.text(.02, .02, "等密度线由 TEOS-10 在 112°E、15°N、0 dbar 计算\nIsopycnals use TEOS-10 at 112°E, 15°N and 0 dbar",
            transform=ax.transAxes, fontsize=8, color="#527078")
    fig.savefig(ASSET_DIR / "argo_scs_ts_diagram.png", bbox_inches="tight")
    plt.close(fig)


def plot_climatology_maps(ds: xr.Dataset) -> None:
    specs = [
        ("temperature", 10, "10 dbar 温度 / Temperature", "turbo"),
        ("practical_salinity", 100, "100 dbar 盐度 / Salinity", "viridis"),
        ("sigma0", 500, r"500 dbar $\sigma_0$ / Density anomaly", "cividis"),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(15, 5.4), constrained_layout=True)
    for ax, (var, pressure, title, cmap) in zip(axes, specs):
        lon, lat, grid, count = grid_profile_values(ds, var, pressure, step=2)
        mesh = ax.pcolormesh(lon, lat, grid, shading="nearest", cmap=cmap)
        map_base(ax, title)
        cb = fig.colorbar(mesh, ax=ax, shrink=.8, pad=.02)
        cb.ax.tick_params(labelsize=8)
        valid_cells = int(np.isfinite(grid).sum())
        ax.text(.02, .03, f"有效网格 / valid cells: {valid_cells}", transform=ax.transAxes, fontsize=8,
                bbox=dict(facecolor="white", alpha=.78, edgecolor="none"))
    fig.suptitle("标准压力层气候态 / Standard-Pressure Climatology (minimum 3 profiles per 2° cell)", fontsize=16, fontweight="bold", color="#082f3d")
    fig.savefig(ASSET_DIR / "argo_scs_climatology_maps.png", bbox_inches="tight")
    plt.close(fig)


def area_balanced_annual_mean(ds: xr.Dataset, variable: str, pressure: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    years = np.arange(CFG.start_year, CFG.end_year + 1)
    results = np.full(years.shape, np.nan, dtype=float)
    cells = np.zeros(years.shape, dtype=int)
    for i, year in enumerate(years):
        _, lat, grid, count = grid_profile_values(ds, variable, pressure, year=year, step=2)
        weights = np.cos(np.deg2rad(lat))[:, None] * np.ones_like(grid)
        valid = np.isfinite(grid)
        cells[i] = int(valid.sum())
        if valid.sum() >= 8:
            results[i] = np.average(grid[valid], weights=weights[valid])
    return years, results, cells


def plot_annual_anomalies(ds: xr.Dataset) -> dict:
    specs = [
        ("temperature", 10, "10 dbar 温度异常 / Temperature anomaly", "°C", "#db6c36"),
        ("practical_salinity", 100, "100 dbar 盐度异常 / Salinity anomaly", "", "#297aa1"),
        ("sigma0", 500, r"500 dbar $\sigma_0$ 异常 / Density anomaly", r"kg m$^{-3}$", "#148878"),
    ]
    fig, axes = plt.subplots(3, 1, figsize=(11.5, 9), sharex=True, constrained_layout=True)
    metrics: dict[str, dict] = {}
    for ax, (var, pressure, title, unit, color) in zip(axes, specs):
        years, mean_values, cells = area_balanced_annual_mean(ds, var, pressure)
        anomaly = mean_values - np.nanmean(mean_values)
        valid = np.isfinite(anomaly)
        slope = np.nan
        pvalue = np.nan
        if valid.sum() >= 5:
            fit = linregress(years[valid], anomaly[valid])
            slope, pvalue = fit.slope * 10, fit.pvalue
            trend = fit.intercept + fit.slope * years[valid]
            ax.plot(years[valid], trend, color="#263f47", linestyle="--", linewidth=1.4, label="线性趋势 / Linear trend")
        ax.axhline(0, color="#78969c", linewidth=.9)
        ax.plot(years, anomaly, marker="o", color=color, linewidth=2.2)
        ax.fill_between(years, 0, anomaly, color=color, alpha=.15)
        ax.set_ylabel(unit or "psu")
        ax.set_title(title, loc="left", fontsize=11, fontweight="bold", color="#123d4a")
        ax.grid(axis="y")
        ax.text(.99, .88, f"趋势 / trend: {slope:+.3g} {unit or 'psu'} per decade · p={pvalue:.3f}",
                transform=ax.transAxes, ha="right", fontsize=8, color="#496970")
        metrics[f"{var}_{pressure}dbar"] = {
            "years": years.tolist(),
            "area_balanced_mean": np.round(mean_values, 5).tolist(),
            "anomaly": np.round(anomaly, 5).tolist(),
            "valid_grid_cells": cells.tolist(),
            "trend_per_decade": None if not np.isfinite(slope) else float(slope),
            "trend_p_value": None if not np.isfinite(pvalue) else float(pvalue),
        }
    axes[-1].set_xticks(np.arange(CFG.start_year, CFG.end_year + 1))
    fig.suptitle("面积平衡年平均异常 / Area-balanced Annual Anomalies", fontsize=16, fontweight="bold", color="#082f3d")
    fig.text(.5, -.01, "每年先计算 2° 网格平均，再按 cos(latitude) 加权；结果仍受 Argo 采样覆盖影响。\nEach year is averaged on a 2° grid then weighted by cos(latitude); sampling coverage still affects the result.", ha="center", fontsize=8, color="#56747a")
    fig.savefig(ASSET_DIR / "argo_scs_annual_anomalies.png", bbox_inches="tight")
    plt.close(fig)
    return metrics


def plot_workflow() -> None:
    steps = [
        ("01", "检索 / Retrieve", "Argovis API\n2016–2025 · 99–122°E · 0–25°N"),
        ("02", "质量控制 / QC", "时间和位置 QC=1–2\n剔除缺测与非物理值"),
        ("03", "TEOS-10", "SP,t,p → SA,CT\n→ sigma0 与 rho"),
        ("04", "标准层 / Standardize", "15 个压力层\n只在观测范围内插值"),
        ("05", "统计 / Aggregate", "2°网格、季节与年平均\n样本阈值和面积权重"),
        ("06", "验证与呈现 / Report", "覆盖图、剖面、T–S 图\n异常、PNG 与 GIF"),
    ]
    fig, ax = plt.subplots(figsize=(15, 4.2))
    ax.set_axis_off()
    colors = ["#0b5267", "#0f746f", "#178f7f", "#2b9f8b", "#d28b45", "#d66b3d"]
    for i, (num, title, desc) in enumerate(steps):
        x = .03 + i * .16
        ax.add_patch(plt.Rectangle((x, .23), .135, .57, transform=ax.transAxes, facecolor="white", edgecolor=colors[i], linewidth=2))
        ax.text(x + .012, .72, num, transform=ax.transAxes, fontsize=11, fontweight="bold", color=colors[i])
        ax.text(x + .012, .58, title, transform=ax.transAxes, fontsize=11, fontweight="bold", color="#123d4a")
        ax.text(x + .012, .43, desc, transform=ax.transAxes, fontsize=8.5, color="#56737a", va="top", linespacing=1.5)
        if i < len(steps) - 1:
            ax.annotate("", xy=(x + .157, .51), xytext=(x + .138, .51), xycoords=ax.transAxes,
                        arrowprops=dict(arrowstyle="->", color="#7f9b9e", lw=1.5))
    ax.text(.03, .92, "关键处理链 / Reproducible Processing Chain", transform=ax.transAxes, fontsize=18, fontweight="bold", color="#082f3d")
    ax.text(.03, .1, "压力是观测坐标；密度为 TEOS-10 推导量。禁止越过剖面最大/最小压力外推。 / Pressure is observed; density is TEOS-10-derived. No extrapolation beyond observed limits.", transform=ax.transAxes, fontsize=9, color="#47676e")
    fig.savefig(ASSET_DIR / "argo_processing_workflow.png", bbox_inches="tight")
    plt.close(fig)


def make_animation(ds: xr.Dataset) -> None:
    lon, lat, clim, _ = grid_profile_values(ds, "temperature", 100, step=2)
    frames: list[Path] = []
    anomalies = []
    for year in range(CFG.start_year, CFG.end_year + 1):
        _, _, grid, _ = grid_profile_values(ds, "temperature", 100, year=year, step=2)
        anomalies.append(grid - clim)
    finite = np.concatenate([a[np.isfinite(a)] for a in anomalies if np.isfinite(a).any()])
    limit = max(.3, float(np.nanpercentile(np.abs(finite), 95))) if finite.size else 1.0
    norm = TwoSlopeNorm(vmin=-limit, vcenter=0, vmax=limit)
    for year, anomaly in zip(range(CFG.start_year, CFG.end_year + 1), anomalies):
        fig, ax = plt.subplots(figsize=(8.4, 7), constrained_layout=True)
        mesh = ax.pcolormesh(lon, lat, anomaly, shading="nearest", cmap="RdBu_r", norm=norm)
        map_base(ax, f"{year} · 100 dbar 温度异常 / Temperature anomaly")
        cb = fig.colorbar(mesh, ax=ax, shrink=.78)
        cb.set_label("相对 2016–2025 气候态 / Relative to climatology (°C)")
        ax.text(.02, .03, "2°网格 · 每格至少3个剖面\n2° grid · ≥3 profiles per cell", transform=ax.transAxes,
                fontsize=8, bbox=dict(facecolor="white", alpha=.82, edgecolor="none"))
        frame = FRAME_DIR / f"temp100_{year}.png"
        fig.savefig(frame, bbox_inches="tight")
        plt.close(fig)
        frames.append(frame)
    images = [Image.open(path).convert("RGB") for path in frames]
    images[0].save(
        ASSET_DIR / "argo_scs_100dbar_temperature_anomaly.gif",
        save_all=True,
        append_images=images[1:],
        duration=1150,
        loop=0,
        disposal=2,
    )


def build_summary(ds: xr.Dataset, metrics: dict) -> dict:
    years = pd.DatetimeIndex(ds.time.values).year
    mode_counts = pd.Series(ds.data_mode.values.astype(str)).value_counts().to_dict()
    gdac_index_path = DATA_DIR / "gdac_index_scs_2016_2025.csv"
    gdac_counts = {str(y): 0 for y in range(CFG.start_year, CFG.end_year + 1)}
    if gdac_index_path.exists():
        gdac_index = pd.read_csv(gdac_index_path)
        index_years = pd.to_datetime(gdac_index["date"].astype(str).str[:8], format="%Y%m%d", errors="coerce").dt.year
        counted = index_years.value_counts()
        gdac_counts = {str(y): int(counted.get(y, 0)) for y in range(CFG.start_year, CFG.end_year + 1)}
    summary = {
        "dataset": "Argo physical profiles accessed from Argovis via argopy",
        "argo_doi": "10.17882/42182",
        "period": "2016-01-01/2025-12-31",
        "region": {"lon": [CFG.lon_min, CFG.lon_max], "lat": [CFG.lat_min, CFG.lat_max], "pressure_dbar": [CFG.p_min, CFG.p_max]},
        "profiles": int(ds.sizes["profile"]),
        "platforms": int(np.unique(ds.platform.values.astype(str)).size),
        "gdac_index_profiles": int(sum(gdac_counts.values())),
        "gdac_index_profiles_by_year": gdac_counts,
        "profiles_by_year": {str(y): int(np.sum(years == y)) for y in range(CFG.start_year, CFG.end_year + 1)},
        "data_mode_counts": {str(k): int(v) for k, v in mode_counts.items()},
        "standard_pressure_levels_dbar": list(CFG.pressure_levels),
        "qc": [
            "Argovis-curated physical profiles",
            "POSITION_QC and TIME_QC retained for flags 1-2",
            "PRES 0-2000 dbar, TEMP -2.5 to 40 C, PSAL 0-42",
            "At least five valid levels and at least 20 dbar observed range",
            "No extrapolation outside the observed pressure range",
        ],
        "thermodynamics": {
            "absolute_salinity": "gsw.SA_from_SP(SP,p,lon,lat)",
            "conservative_temperature": "gsw.CT_from_t(SA,t,p)",
            "sigma0": "gsw.sigma0(SA,CT)",
            "in_situ_density": "gsw.rho(SA,CT,p)",
        },
        "annual_metrics": metrics,
        "limitations": [
            "Argo sampling is uneven in space, season and depth, especially over shallow shelves.",
            "Only adjusted and delayed modes passed this workflow; no raw real-time-mode profile entered the final sample.",
            "The GDAC index contains no regional profiles in 2023-2024 and only five in 2025, so recent-year anomalies are not estimated.",
            "Trend estimates cover only ten years and are sampling-sensitive; they are descriptive, not long-term climate attribution.",
        ],
    }
    def json_safe(value):
        if isinstance(value, dict):
            return {key: json_safe(item) for key, item in value.items()}
        if isinstance(value, list):
            return [json_safe(item) for item in value]
        if isinstance(value, (float, np.floating)):
            return float(value) if np.isfinite(value) else None
        if isinstance(value, (int, np.integer)):
            return int(value)
        return value

    summary = json_safe(summary)
    (ASSET_DIR / "argo_scs_2016_2025_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8"
    )
    pd.DataFrame({
        "year": list(range(CFG.start_year, CFG.end_year + 1)),
        "profiles": [summary["profiles_by_year"][str(y)] for y in range(CFG.start_year, CFG.end_year + 1)],
    }).to_csv(ASSET_DIR / "argo_scs_profiles_by_year.csv", index=False, encoding="utf-8-sig")
    return summary


def main() -> None:
    setup_style()
    print("download and standardize annual Argo profiles", flush=True)
    years = list(range(CFG.start_year, CFG.end_year + 1))
    completed: dict[int, Path | None] = {}
    # Three concurrent years keep individual API requests small while avoiding
    # an unnecessarily long serial download. Each month writes a separate cache.
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {pool.submit(process_year, year): year for year in years}
        for future in as_completed(futures):
            year = futures[future]
            try:
                completed[year] = future.result()
                print(f"completed year {year}", flush=True)
            except RuntimeError as exc:
                if str(exc) == f"No valid profiles for {year}":
                    completed[year] = None
                    print(f"completed year {year}: no valid profiles", flush=True)
                else:
                    raise
    paths = [completed[year] for year in years if completed.get(year) is not None]
    ds = load_all_years(paths)
    print(f"combined profiles: {ds.sizes['profile']:,}", flush=True)
    plot_workflow()
    plot_coverage(ds)
    plot_vertical_climatology(ds)
    plot_ts_diagram(ds)
    plot_climatology_maps(ds)
    metrics = plot_annual_anomalies(ds)
    make_animation(ds)
    summary = build_summary(ds, metrics)
    print(json.dumps({k: summary[k] for k in ("period", "profiles", "platforms", "profiles_by_year", "data_mode_counts")}, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
