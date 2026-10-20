# test3 observational wave case

This package combines two official observational records for two distinct purposes.

- `44088h2024.txt.gz`: NOAA NDBC station 44088 standard meteorological archive for 2024. `WVHT` is significant wave height and `DPD` is dominant wave period. The buoy directly measures surface-wave statistics.
- `D2902695_039.nc`: official Argo GDAC profile 2902695 cycle 39, South China Sea, 16 March 2017. Quality flags 1 and 2 are retained; adjusted pressure, temperature and salinity are preferred. TEOS-10 GSW produces potential-density anomaly and buoyancy frequency.

The single Argo profile diagnoses stable density stratification capable of supporting internal waves. It does not, by itself, demonstrate a propagating internal wave. Time-resolved density and velocity, repeated profiles, or image sequences are required to estimate internal-wave frequency, wavelength and phase speed.

Run `analysis/test3_wave_case.py` to rebuild the processed CSV files, summary and figures. Run `analysis/validate_test3_waves.m` in MATLAB to verify the numerical examples and exported statistics.

Sources:

- https://www.ndbc.noaa.gov/data/historical/stdmet/44088h2024.txt.gz
- https://data-argo.ifremer.fr/dac/csio/2902695/profiles/D2902695_039.nc
- https://www.teos-10.org/pubs/gsw/html/gsw_Nsquared.html
