# Test 2 Argo case data

This folder contains the six single-cycle core Argo profiles used in the Test 2 South China Sea calculation. The files were downloaded on 20 October 2026 from the official Coriolis Argo GDAC mirror:

`https://data-argo.ifremer.fr/dac/`

| Station | WMO | Cycle file | UTC date | Position | Data mode |
|---|---:|---|---|---|---|
| A | 5904747 | `aoml/5904747/profiles/R5904747_081.nc` | 2017-03-15 | 110.201 E, 14.081 N | Adjusted |
| B | 2902698 | `csio/2902698/profiles/D2902698_028.nc` | 2017-03-13 | 112.800 E, 14.310 N | Delayed |
| C | 2902697 | `csio/2902697/profiles/D2902697_025.nc` | 2017-03-14 | 113.465 E, 14.002 N | Delayed |
| D | 2902695 | `csio/2902695/profiles/D2902695_039.nc` | 2017-03-16 | 114.506 E, 15.542 N | Delayed |
| E | 2902694 | `csio/2902694/profiles/D2902694_038.nc` | 2017-03-14 | 115.246 E, 15.803 N | Delayed |
| F | 2901481 | `aoml/2901481/profiles/R2901481_081.nc` | 2017-03-14 | 115.601 E, 15.836 N | Adjusted |

The workflow uses adjusted pressure, temperature and salinity with Argo QC flags 1 or 2 where available, with raw QC-approved values as fallback. It interpolates only within each observed profile, converts to TEOS-10 Absolute Salinity and Conservative Temperature, calculates dynamic height relative to 700 dbar, and calculates section-normal relative geostrophic velocity between adjacent stations.

Reproduce the analysis with `analysis/test2_argo_geostrophic.py`. See `assets/argo/test2_argo_geostrophic_summary.json` for hashes, method details, and limitations. Cite the Argo dataset DOI: https://doi.org/10.17882/42182.
