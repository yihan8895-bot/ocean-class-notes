% Independent numerical checks for the test3 wave examples and exported data.
root = fileparts(fileparts(mfilename('fullpath')));
summary = jsondecode(fileread(fullfile(root,'assets','waves','test3_wave_case_summary.json')));
g = 9.81; T = 10; cp = g*T/(2*pi); lambda = g*T^2/(2*pi);
gprime = g*2/1025; ci = sqrt(gprime*50*150/(50+150));
assert(abs(cp-summary.worked_example.surface_phase_speed_m_s)<1e-12)
assert(abs(lambda-summary.worked_example.surface_wavelength_m)<1e-12)
assert(abs(ci-summary.worked_example.internal_longwave_speed_m_s)<1e-12)
wave = readtable(fullfile(root,'assets','waves','test3_ndbc_44088_2024_wave_summary.csv'),'Delimiter',',','VariableNamingRule','preserve');
assert(height(wave)==summary.surface_case.valid_records)
assert(abs(median(wave.("WVHT"))-summary.surface_case.median_Hs_m)<1e-12)
strat = readtable(fullfile(root,'assets','waves','test3_argo_stratification_profile.csv'),'Delimiter',',','VariableNamingRule','preserve');
n2 = strat.("N2_s-2"); n2 = n2(isfinite(n2));
assert(mean(n2>0)>0.98)
assert(max(n2)>0)
fprintf('test3 verified: cp=%.6f m/s, lambda=%.6f m, ci=%.6f m/s, stable=%.2f%%, buoy records=%d\n',cp,lambda,ci,100*mean(n2>0),height(wave));
