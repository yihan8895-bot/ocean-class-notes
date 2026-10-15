"""Validate the published Argo analysis assets and local page references."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    html = (ROOT / "geostrophic.html").read_text(encoding="utf-8")
    refs = set(re.findall(r'(?:src|href)="((?:assets|analysis)/[^"?#]+)', html))
    missing = sorted(ref for ref in refs if not (ROOT / ref).exists())
    if missing:
        raise FileNotFoundError(f"Missing local references: {missing}")

    summary = json.loads(
        (ROOT / "assets/argo/argo_scs_2016_2025_summary.json").read_text(encoding="utf-8")
    )
    if summary["profiles"] != 4175 or summary["gdac_index_profiles"] != 4320:
        raise ValueError("Published summary counts do not match the validated analysis")

    section = summary["density_isobar_section"]
    if section["date_range"] != "2017-03-13/2017-03-16" or len(section["stations"]) != 6:
        raise ValueError("Density-section metadata does not match the selected transect")

    with (ROOT / "assets/argo/argo_scs_density_section_samples.csv").open(
        encoding="utf-8-sig", newline=""
    ) as handle:
        sample_rows = list(csv.DictReader(handle))
    station_ids = {row["station"] for row in sample_rows}
    pressure_levels = {float(row["pressure_dbar"]) for row in sample_rows}
    if station_ids != set("ABCDEF") or not {100.0, 200.0, 500.0, 1000.0} <= pressure_levels:
        raise ValueError("Density-section CSV is missing stations or labeled pressure levels")

    with Image.open(ROOT / "assets/argo/argo_scs_100dbar_temperature_anomaly.gif") as animation:
        frames = animation.n_frames
        duration = animation.info.get("duration")
        loop = animation.info.get("loop")
    if frames != 10 or loop != 0 or duration != 1150:
        raise ValueError("Animation must contain ten 1.15-second yearly frames and loop continuously")

    print(
        json.dumps(
            {
                "local_references": len(refs),
                "missing_references": missing,
                "valid_profiles": summary["profiles"],
                "gdac_index_profiles": summary["gdac_index_profiles"],
                "gif_frames": frames,
                "gif_duration_ms": duration,
                "gif_loop": loop,
                "density_section_stations": sorted(station_ids),
                "density_section_rows": len(sample_rows),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
