%% South China Sea geostrophic-flow teaching analysis, 2016-2025
% Uses the local NOAA OISST v2.1 subset to diagnose SST fronts. OISST does
% not contain sea-surface height or velocity, so no absolute geostrophic
% current is inferred from these data. The figures keep that distinction
% explicit and connect SST fronts to the thermal-wind concept only.

clearvars;

dataFolder = "E:\研究生课题\data\OISST_ERA5_1996_2025\OISST";
projectFolder = fileparts(fileparts(mfilename("fullpath")));
outputFolder = fullfile(projectFolder, "assets", "geostrophic");
if ~isfolder(outputFolder)
    mkdir(outputFolder);
end

years = (2016:2025)';
seasonNames = ["冬季 DJF", "春季 MAM", "夏季 JJA", "秋季 SON"];
seasonNamesEn = ["Winter DJF", "Spring MAM", "Summer JJA", "Autumn SON"];
radiusEarth = 6371000;

sampleFile = fullfile(dataFolder, "oisst_v2.1_scs_2016.nc");
longitude = double(ncread(sampleFile, "longitude"));
latitude = double(ncread(sampleFile, "latitude"));
nLongitude = numel(longitude);
nLatitude = numel(latitude);
deltaLongitude = deg2rad(mean(diff(longitude)));
deltaLatitude = deg2rad(mean(diff(latitude)));

sumSst = zeros(nLatitude, nLongitude);
countSst = zeros(nLatitude, nLongitude);
sumFront = zeros(nLatitude, nLongitude);
countFront = zeros(nLatitude, nLongitude);
seasonSumSst = zeros(nLatitude, nLongitude, 4);
seasonCountSst = zeros(nLatitude, nLongitude, 4);
seasonSumFront = zeros(nLatitude, nLongitude, 4);
seasonCountFront = zeros(nLatitude, nLongitude, 4);

annualMeanSst = nan(numel(years), 1);
annualMeanFront = nan(numel(years), 1);
annualP95Front = nan(numel(years), 1);
annualMeanError = nan(numel(years), 1);
annualDays = zeros(numel(years), 1);
totalDays = 0;

for yearIndex = 1:numel(years)
    yearValue = years(yearIndex);
    fileName = fullfile(dataFolder, sprintf("oisst_v2.1_scs_%d.nc", yearValue));
    rawSst = double(ncread(fileName, "sst"));
    rawError = double(ncread(fileName, "err"));
    sst = permute(squeeze(rawSst), [2 1 3]);
    errorEstimate = permute(squeeze(rawError), [2 1 3]);
    sst(sst < -3 | sst > 45) = NaN;
    errorEstimate(errorEstimate < 0 | errorEstimate > 10) = NaN;
    nDays = size(sst, 3);
    annualDays(yearIndex) = nDays;
    totalDays = totalDays + nDays;
    dates = datetime(yearValue, 1, 1) + days(0:nDays-1);

    front = nan(size(sst));
    for dayIndex = 1:nDays
        field = sst(:, :, dayIndex);
        dTdx = nan(size(field));
        dTdy = nan(size(field));
        zonalDistance = radiusEarth .* cosd(latitude) .* deltaLongitude;
        dTdx(:, 2:end-1) = (field(:, 3:end) - field(:, 1:end-2)) ./ (2 .* zonalDistance);
        meridionalDistance = radiusEarth * deltaLatitude;
        dTdy(2:end-1, :) = (field(3:end, :) - field(1:end-2, :)) ./ (2 * meridionalDistance);
        front(:, :, dayIndex) = hypot(dTdx, dTdy) * 100000;
    end

    validSst = ~isnan(sst);
    validFront = ~isnan(front);
    sumSst = sumSst + sum(sst, 3, "omitnan");
    countSst = countSst + sum(validSst, 3);
    sumFront = sumFront + sum(front, 3, "omitnan");
    countFront = countFront + sum(validFront, 3);

    annualMeanSst(yearIndex) = areaWeightedMean(sst, latitude);
    annualMeanFront(yearIndex) = areaWeightedMean(front, latitude);
    annualP95Front(yearIndex) = percentile95(front(:));
    annualMeanError(yearIndex) = areaWeightedMean(errorEstimate, latitude);

    monthValues = month(dates);
    seasonIndex = 1 + (monthValues >= 3 & monthValues <= 5) + ...
        2 * (monthValues >= 6 & monthValues <= 8) + ...
        3 * (monthValues >= 9 & monthValues <= 11);
    for season = 1:4
        selected = seasonIndex == season;
        selectedSst = sst(:, :, selected);
        selectedFront = front(:, :, selected);
        seasonSumSst(:, :, season) = seasonSumSst(:, :, season) + ...
            sum(selectedSst, 3, "omitnan");
        seasonCountSst(:, :, season) = seasonCountSst(:, :, season) + ...
            sum(~isnan(selectedSst), 3);
        seasonSumFront(:, :, season) = seasonSumFront(:, :, season) + ...
            sum(selectedFront, 3, "omitnan");
        seasonCountFront(:, :, season) = seasonCountFront(:, :, season) + ...
            sum(~isnan(selectedFront), 3);
    end
end

meanSst = sumSst ./ countSst;
meanSst(countSst == 0) = NaN;
meanFront = sumFront ./ countFront;
meanFront(countFront == 0) = NaN;
seasonMeanSst = seasonSumSst ./ seasonCountSst;
seasonMeanSst(seasonCountSst == 0) = NaN;
seasonMeanFront = seasonSumFront ./ seasonCountFront;
seasonMeanFront(seasonCountFront == 0) = NaN;

[maximumFront, maximumLinearIndex] = max(meanFront, [], "all", "omitnan");
[maximumLatitudeIndex, maximumLongitudeIndex] = ind2sub(size(meanFront), maximumLinearIndex);
maximumFrontLongitude = longitude(maximumLongitudeIndex);
maximumFrontLatitude = latitude(maximumLatitudeIndex);
domainMeanSst = areaWeightedMean(meanSst, latitude);
domainMeanFront = areaWeightedMean(meanFront, latitude);

summaryTable = table(years, annualDays, annualMeanSst, annualMeanFront, ...
    annualP95Front, annualMeanError, VariableNames=["Year", "Days", ...
    "AreaWeightedMeanSST_C", "AreaWeightedMeanFront_C_per_100km", ...
    "P95Front_C_per_100km", "AreaWeightedMeanOISSTError_C"]);
writetable(summaryTable, fullfile(outputFolder, "scs_oisst_2016_2025_summary.csv"));

summary = struct;
summary.period = "2016-01-01 to 2025-12-31";
summary.totalDays = totalDays;
summary.longitudeRange = [min(longitude), max(longitude)];
summary.latitudeRange = [min(latitude), max(latitude)];
summary.gridResolutionDegrees = [mean(diff(longitude)), mean(diff(latitude))];
summary.areaWeightedMeanSST_C = domainMeanSst;
summary.areaWeightedMeanFront_C_per_100km = domainMeanFront;
summary.maximumMeanFront_C_per_100km = maximumFront;
summary.maximumMeanFrontLongitude = maximumFrontLongitude;
summary.maximumMeanFrontLatitude = maximumFrontLatitude;
summary.meanOISSTError_C = mean(annualMeanError, "omitnan");
summary.caveat = "OISST contains SST, not sea-surface height or velocity; SST gradients are not absolute geostrophic currents.";
summaryText = jsonencode(summary, PrettyPrint=true);
fileIdentifier = fopen(fullfile(outputFolder, "scs_oisst_2016_2025_summary.json"), "w");
fprintf(fileIdentifier, "%s", summaryText);
fclose(fileIdentifier);

fontName = "Microsoft YaHei UI";

figureHandle = figure(Visible="off", Color="w", Position=[80 80 1900 820]);
layout = tiledlayout(figureHandle, 1, 2, Padding="compact", TileSpacing="compact");
title(layout, "南海 NOAA OISST v2.1：十年平均海温与温度锋面 / 2016–2025 Mean SST and Thermal Fronts", ...
    FontName=fontName, FontWeight="bold", FontSize=20);
nexttile;
imageHandle = imagesc(longitude, latitude, meanSst);
imageHandle.AlphaData = ~isnan(meanSst);
axis xy tight; colorbar; colormap(gca, turbo(256));
caxis([20 30]);
xlabel("经度 / Longitude (°E)"); ylabel("纬度 / Latitude (°N)");
title("(a) 十年平均 SST / Ten-year mean SST (°C)");
applyMapStyle(gca, fontName);
nexttile;
imageHandle = imagesc(longitude, latitude, meanFront);
imageHandle.AlphaData = ~isnan(meanFront);
axis xy tight; colorbar; colormap(gca, frontColormap());
frontLimit = percentile95(meanFront(:));
caxis([0 max(frontLimit, 0.5)]);
hold on;
contour(longitude, latitude, meanSst, 20:1:30, Color=[0.12 0.2 0.25], LineWidth=0.65);
plot(maximumFrontLongitude, maximumFrontLatitude, "p", MarkerSize=15, ...
    MarkerFaceColor=[1 .75 .15], MarkerEdgeColor="k");
hold off;
xlabel("经度 / Longitude (°E)"); ylabel("纬度 / Latitude (°N)");
title("(b) 日平均锋面强度 / Mean daily |∇SST| (°C per 100 km)");
applyMapStyle(gca, fontName);
exportgraphics(figureHandle, fullfile(outputFolder, "scs_oisst_mean_fronts_2016_2025.png"), Resolution=180);
close(figureHandle);

figureHandle = figure(Visible="off", Color="w", Position=[80 80 1800 1350]);
layout = tiledlayout(figureHandle, 2, 2, Padding="compact", TileSpacing="compact");
title(layout, "南海表层温度锋面的季节变化 / Seasonal Surface Thermal Fronts, 2016–2025", ...
    FontName=fontName, FontWeight="bold", FontSize=20);
commonLimit = percentile95(seasonMeanFront(:));
for season = 1:4
    nexttile;
    imageHandle = imagesc(longitude, latitude, seasonMeanFront(:, :, season));
    imageHandle.AlphaData = ~isnan(seasonMeanFront(:, :, season));
    axis xy tight; colormap(gca, frontColormap()); caxis([0 max(commonLimit, 0.5)]);
    hold on;
    contour(longitude, latitude, seasonMeanSst(:, :, season), 20:1:31, ...
        Color=[0.12 0.2 0.25], LineWidth=0.55);
    hold off;
    colorbar;
    title(sprintf("%s / %s", seasonNames(season), seasonNamesEn(season)));
    xlabel("经度 / Longitude (°E)"); ylabel("纬度 / Latitude (°N)");
    applyMapStyle(gca, fontName);
end
exportgraphics(figureHandle, fullfile(outputFolder, "scs_oisst_seasonal_fronts_2016_2025.png"), Resolution=180);
close(figureHandle);

figureHandle = figure(Visible="off", Color="w", Position=[80 80 1800 900]);
layout = tiledlayout(figureHandle, 2, 1, Padding="compact", TileSpacing="compact");
title(layout, "南海 OISST 十年变化 / South China Sea OISST Metrics, 2016–2025", ...
    FontName=fontName, FontWeight="bold", FontSize=20);
nexttile;
plot(years, annualMeanSst, "-o", Color=[0.05 .43 .63], MarkerFaceColor=[.22 .79 .72], LineWidth=2.5);
grid on; xlim([2015.6 2025.4]); xticks(years);
ylabel("SST (°C)"); title("面积加权年平均 SST / Area-weighted annual mean SST");
applyChartStyle(gca, fontName);
nexttile;
plot(years, annualMeanFront, "-o", Color=[.08 .5 .38], MarkerFaceColor=[.45 .88 .7], LineWidth=2.5);
hold on;
plot(years, annualP95Front, "-s", Color=[.91 .39 .16], MarkerFaceColor=[1 .69 .35], LineWidth=2.5);
hold off; grid on; xlim([2015.6 2025.4]); xticks(years);
ylabel("°C per 100 km"); xlabel("年份 / Year");
title("温度锋面强度 / SST-front intensity");
legend("区域平均 / Domain mean", "第95百分位 / 95th percentile", Location="best", Box="off");
applyChartStyle(gca, fontName);
exportgraphics(figureHandle, fullfile(outputFolder, "scs_oisst_annual_metrics_2016_2025.png"), Resolution=180);
close(figureHandle);

figureHandle = figure(Visible="off", Color=[.965 .98 .985], Position=[80 80 1800 950]);
axesHandle = axes(figureHandle, Position=[0 0 1 1], Visible="off", XLim=[0 1], YLim=[0 1]);
text(axesHandle, .05, .92, "地转流如何形成？ / How Does Geostrophic Flow Form?", ...
    FontName=fontName, FontWeight="bold", FontSize=28, Color=[.02 .16 .24]);
drawBox(axesHandle, [.05 .61 .25 .22], [1 .93 .78], "1  压力梯度建立\nPressure gradient forms", ...
    "海面倾斜或密度差产生水平压强梯度。\nSea-level slope or density contrast creates a horizontal pressure gradient.", fontName);
drawBox(axesHandle, [.375 .61 .25 .22], [.79 .94 .91], "2  水团开始加速\nWater accelerates", ...
    "压强梯度力先把静止水团推向低压侧。\nPGF first accelerates still water toward lower pressure.", fontName);
drawBox(axesHandle, [.70 .61 .25 .22], [.82 .9 1], "3  科氏力使流向转弯\nCoriolis turns the flow", ...
    "速度出现后，科氏力垂直于速度并随速度增强。\nCoriolis is perpendicular to velocity and grows with speed.", fontName);
annotation(figureHandle, "arrow", [.30 .365], [.72 .72], Color=[.1 .35 .43], LineWidth=2);
annotation(figureHandle, "arrow", [.625 .69], [.72 .72], Color=[.1 .35 .43], LineWidth=2);
drawBox(axesHandle, [.22 .25 .56 .23], [.05 .25 .34], "4  近似地转平衡 / Near-geostrophic balance", ...
    "f k x u_g = -(1/rho0) grad_h p\nu_g = -(g/f) d(SSH)/dy   |   v_g = (g/f) d(SSH)/dx\n两力近似等大反向，流动主要沿等压线。 / Forces nearly oppose; flow follows pressure contours.", fontName, true);
annotation(figureHandle, "arrow", [.82 .66], [.60 .49], Color=[.1 .35 .43], LineWidth=2);
text(axesHandle, .5, .10, "热成风联系 / Thermal-wind link:  du_g/dz = -(g / f rho0) k x grad_h rho", ...
    HorizontalAlignment="center", FontName=fontName, FontSize=17, FontWeight="bold", Color=[.07 .25 .35]);
text(axesHandle, .5, .055, "SST 仅在温度主导密度且盐度影响较小时帮助识别密度锋面；绝对表层地转流仍需 SSH。 / SST can indicate density fronts only when temperature dominates; absolute surface geostrophic flow still requires SSH.", ...
    HorizontalAlignment="center", FontName=fontName, FontSize=11, Color=[.25 .32 .35]);
exportgraphics(figureHandle, fullfile(outputFolder, "geostrophic_formation_and_formulas.png"), Resolution=180);
close(figureHandle);

fprintf("Processed %d days on a %d x %d grid.\n", totalDays, nLongitude, nLatitude);
fprintf("Domain: %.3f-%.3f E, %.3f-%.3f N.\n", min(longitude), max(longitude), min(latitude), max(latitude));
fprintf("Area-weighted mean SST: %.3f C. Mean front: %.3f C/100 km.\n", domainMeanSst, domainMeanFront);
fprintf("Maximum ten-year mean front: %.3f C/100 km at %.3f E, %.3f N.\n", ...
    maximumFront, maximumFrontLongitude, maximumFrontLatitude);
fprintf("Mean OISST error estimate: %.3f C.\n", mean(annualMeanError, "omitnan"));

function value = areaWeightedMean(data, latitude)
    weights = cosd(latitude(:));
    reshapeSize = ones(1, ndims(data));
    reshapeSize(1) = numel(latitude);
    weights = reshape(weights, reshapeSize);
    weights = weights .* ones(size(data));
    valid = ~isnan(data);
    numerator = sum(data(valid) .* weights(valid), "omitnan");
    denominator = sum(weights(valid), "omitnan");
    value = numerator / denominator;
end

function value = percentile95(data)
    values = sort(data(~isnan(data)));
    if isempty(values)
        value = NaN;
        return;
    end
    index = max(1, min(numel(values), ceil(0.95 * numel(values))));
    value = values(index);
end

function applyMapStyle(axesHandle, fontName)
    axesHandle.FontName = fontName;
    axesHandle.FontSize = 11;
    axesHandle.LineWidth = 1;
    axesHandle.Box = "on";
    axesHandle.Layer = "top";
    grid(axesHandle, "on");
    axesHandle.GridAlpha = .15;
end

function applyChartStyle(axesHandle, fontName)
    axesHandle.FontName = fontName;
    axesHandle.FontSize = 11;
    axesHandle.LineWidth = 1;
    axesHandle.Box = "off";
    axesHandle.GridAlpha = .14;
end

function colors = frontColormap()
    anchors = [247 251 255; 198 230 231; 84 180 174; 5 103 132; 5 45 72] / 255;
    source = linspace(0, 1, size(anchors, 1));
    target = linspace(0, 1, 256);
    colors = interp1(source, anchors, target);
end

function drawBox(axesHandle, position, faceColor, heading, body, fontName, dark)
    if nargin < 7
        dark = false;
    end
    rectangle(axesHandle, Position=position, Curvature=.08, FaceColor=faceColor, ...
        EdgeColor=[.75 .82 .84], LineWidth=1.2);
    if dark
        headingColor = [1 1 1];
        bodyColor = [.88 .97 .98];
    else
        headingColor = [.02 .16 .24];
        bodyColor = [.2 .28 .31];
    end
    heading = replace(heading, "\n", newline);
    body = replace(body, "\n", newline);
    text(axesHandle, position(1)+.022, position(2)+position(4)-.048, heading, ...
        FontName=fontName, FontWeight="bold", FontSize=14, Color=headingColor, ...
        VerticalAlignment="top", Interpreter="none");
    text(axesHandle, position(1)+.022, position(2)+position(4)-.12, body, ...
        FontName=fontName, FontSize=10.5, Color=bodyColor, VerticalAlignment="top", ...
        Interpreter="none");
end


