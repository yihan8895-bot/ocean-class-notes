"""Validate the published Argo analysis assets and local page references."""

from __future__ import annotations

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
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
