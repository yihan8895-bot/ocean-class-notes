%% Independent validation of the Test 2 relative geostrophic calculation
% Recomputes velocity from exported dynamic height and station geometry.

rootFolder = fileparts(fileparts(mfilename("fullpath")));
profileFile = fullfile(rootFolder, "assets", "argo", "test2_argo_dynamic_height_profiles.csv");
velocityFile = fullfile(rootFolder, "assets", "argo", "test2_argo_relative_geostrophic_velocity.csv");

profiles = readtable(profileFile, TextType="string", VariableNamingRule="preserve");
velocities = readtable(velocityFile, TextType="string", VariableNamingRule="preserve");

assert(height(profiles) == 420, "Expected 6 stations x 70 pressure levels.");
assert(height(velocities) == 350, "Expected 5 station pairs x 70 pressure levels.");

referenceRows = profiles.pressure_dbar == 700;
referenceHeight = profiles.dynamic_height_m2_s2_ref_700dbar(referenceRows);
assert(all(abs(referenceHeight) < 1e-10), "Dynamic height is not zero at 700 dbar.");

omega = 7.292115e-5; % rad s^-1, TEOS-10/GSW value
calculated = nan(height(velocities), 1);
for row = 1:height(velocities)
    stationNames = split(velocities.station_pair(row), "-");
    pressure = velocities.pressure_dbar(row);
    left = profiles.station == stationNames(1) & profiles.pressure_dbar == pressure;
    right = profiles.station == stationNames(2) & profiles.pressure_dbar == pressure;
    assert(nnz(left) == 1 && nnz(right) == 1, "Station-pressure lookup must be unique.");
    dynamicHeightDifference = profiles.dynamic_height_m2_s2_ref_700dbar(right) ...
        - profiles.dynamic_height_m2_s2_ref_700dbar(left);
    coriolis = 2 * omega * sind(velocities.midpoint_latitude_north(row));
    distanceM = velocities.segment_distance_km(row) * 1000;
    calculated(row) = dynamicHeightDifference / (distanceM * coriolis);
end

maximumDifference = max(abs(calculated - velocities.relative_geostrophic_velocity_m_s));
assert(maximumDifference < 5e-12, "Exported velocity does not match the geostrophic formula.");
assert(max(abs(velocities.relative_geostrophic_velocity_m_s)) < 3, "Velocity exceeds the plausibility guardrail.");

surfaceRows = velocities.pressure_dbar == 10;
surfaceRange = [min(velocities.relative_geostrophic_velocity_m_s(surfaceRows)), ...
    max(velocities.relative_geostrophic_velocity_m_s(surfaceRows))];
fprintf("Validation passed. Max formula difference: %.3g m/s\n", maximumDifference);
fprintf("10 dbar relative-velocity range: %.3f to %.3f m/s\n", surfaceRange(1), surfaceRange(2));
