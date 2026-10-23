"""Generate the bilingual ocean–atmosphere wave atlas data and PNG tables."""
from __future__ import annotations

import csv
import json
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "waves"
OUT.mkdir(parents=True, exist_ok=True)


def t(zh: str, en: str) -> dict[str, str]:
    return {"zh": zh, "en": en}


ROWS = [
    dict(group=t("海面与海岸", "Surface & coastal"), name=t("毛细波\nCapillary wave", "Capillary wave"), medium=t("空气—海水界面", "Air–sea interface"), restoring=t("表面张力 σ", "Surface tension σ"), assumptions=t("短波；深水极限常用", "Short waves; often deep-water"), dispersion=t("ω²=(gk+σk³/ρ)tanh(kH)；毛细极限 ω²≈σk³/ρ", "ω²=(gk+σk³/ρ)tanh(kH); capillary limit ω²≈σk³/ρ"), dispersive=t("强色散；深水 cᵍ=3cₚ/2", "Strong; deep water cᵍ=3cₚ/2"), period=t("<0.1 s", "<0.1 s"), scale=t("λ≲1.7 cm（水）", "λ≲1.7 cm in water"), propagation=t("短波传播更快；能量随群速", "Shorter waves faster; energy at group speed"), source=t("微风、雨滴、界面扰动", "Light wind, raindrops, interface disturbance"), observation=t("高频海面纹理、实验波槽", "High-frequency ripples, wave tanks")),
    dict(group=t("海面与海岸", "Surface & coastal"), name=t("表面重力波\nSurface gravity wave", "Surface gravity wave"), medium=t("自由海面；运动随深度衰减", "Free surface; motion decays with depth"), restoring=t("重力 g", "Gravity g"), assumptions=t("线性、小振幅；任意水深", "Linear, small amplitude; any depth"), dispersion=t("ω²=gk tanh(kH)；深水 ω²=gk", "ω²=gk tanh(kH); deep water ω²=gk"), dispersive=t("深水色散；深水 cᵍ=cₚ/2", "Deep water dispersive; cᵍ=cₚ/2"), period=t("约 1–30 s", "about 1–30 s"), scale=t("约 1 m–1 km", "about 1 m–1 km"), propagation=t("深水长波更快；近岸折射、浅化、破碎", "Longer deep-water waves faster; refract, shoal and break near shore"), source=t("局地风、远处风暴、船舶", "Local wind, distant storms, vessels"), observation=t("浮标波高/周期、雷达、卫星高度计", "Buoy height/period, radar, altimetry")),
    dict(group=t("海面与海岸", "Surface & coastal"), name=t("浅水长波／海啸\nShallow-water wave / tsunami", "Shallow-water wave / tsunami"), medium=t("全水深近同相运动", "Nearly depth-uniform motion"), restoring=t("重力；海面坡度", "Gravity; surface slope"), assumptions=t("kH≪1；静水压力", "kH≪1; hydrostatic"), dispersion=t("无旋转 ω²=gHK²；含旋转 ω²=f²+gHK²", "No rotation ω²=gHK²; rotating ω²=f²+gHK²"), dispersive=t("均匀水深近无色散；c=√(gH)", "Nearly non-dispersive at uniform depth; c=√(gH)"), period=t("约 5–120 min（海啸）", "about 5–120 min for tsunamis"), scale=t("约 10–500+ km", "about 10–500+ km"), propagation=t("深海快、近岸减速增高；可跨洋", "Fast in deep water, slows and grows near shore; basin crossing"), source=t("海底地震、滑坡、火山、撞击", "Seafloor earthquake, landslide, volcano, impact"), observation=t("DART 底压、验潮站、GNSS 浮标", "DART bottom pressure, tide gauges, GNSS buoys")),
    dict(group=t("海面与海岸", "Surface & coastal"), name=t("潮汐长波\nTidal wave", "Tidal long wave"), medium=t("全球海洋与陆架", "Global ocean and shelves"), restoring=t("重力；天体潮汐势周期强迫", "Gravity; periodic astronomical forcing"), assumptions=t("旋转浅水方程；盆地几何", "Rotating shallow-water equations; basin geometry"), dispersion=t("受迫频率固定；自由模局地近似 ω²=f²+gHK²", "Forced frequency fixed; free modes locally ω²=f²+gHK²"), dispersive=t("传播近无色散；共振与摩擦改变响应", "Nearly non-dispersive; resonance and friction shape response"), period=t("12.42 h、12 h、23.93 h、25.82 h 等", "12.42 h, 12 h, 23.93 h, 25.82 h, etc."), scale=t("陆架至全球尺度", "Shelf to global scale"), propagation=t("旋转盆地中的 Kelvin/Poincaré 型响应", "Kelvin/Poincaré-like response in rotating basins"), source=t("月、日引潮力", "Lunar and solar tidal potential"), observation=t("验潮站、卫星高度计、潮流仪", "Tide gauges, altimetry, current meters")),
    dict(group=t("海面与海岸", "Surface & coastal"), name=t("海湾静振\nSeiche", "Seiche"), medium=t("封闭或半封闭湖湾、港池", "Enclosed or semi-enclosed basins and harbours"), restoring=t("重力；边界反射形成驻波", "Gravity; standing wave from reflections"), assumptions=t("一维均匀浅水盆地近似", "1-D uniform shallow basin approximation"), dispersion=t("ωₙ≈nπ√(gH)/L；基模 T₁≈2L/√(gH)", "ωₙ≈nπ√(gH)/L; fundamental T₁≈2L/√(gH)"), dispersive=t("离散本征模；频率由几何决定", "Discrete eigenmodes set by geometry"), period=t("数分钟–数小时/天", "minutes to hours/days"), scale=t("港池至湖盆尺度", "Harbour to lake-basin scale"), propagation=t("节点与腹点固定；弱阻尼时持续", "Fixed nodes/antinodes; persists under weak damping"), source=t("风压突变、气压、海啸、船波", "Wind setup, pressure jumps, tsunamis, ship waves"), observation=t("验潮站、压力计；港湾共振风险", "Tide gauges, pressure sensors; harbour resonance risk")),
    dict(group=t("海面与海岸", "Surface & coastal"), name=t("风暴潮\nStorm surge", "Storm surge"), medium=t("陆架、近岸与河口", "Shelf, coast and estuaries"), restoring=t("风应力与低气压强迫；重力调整", "Wind stress and low pressure forcing; gravity adjustment"), assumptions=t("受迫、耗散的旋转浅水响应", "Forced, dissipative rotating shallow-water response"), dispersion=t("无唯一自由频散式；自由部分近似 ω²=f²+gHK²", "No unique free dispersion; free part ≈f²+gHK²"), dispersive=t("受地形、摩擦、共振和移动风暴控制", "Controlled by topography, friction, resonance and storm motion"), period=t("数小时–数天", "hours to days"), scale=t("约 10–1000 km", "about 10–1000 km"), propagation=t("常与潮汐叠加；浅海和漏斗形海湾放大", "Adds to tides; amplified on shallow shelves and funnel bays"), source=t("热带/温带气旋、强持续风", "Tropical/extratropical cyclones, persistent wind"), observation=t("验潮站、浮标、气压、风场与数值预报", "Gauges, buoys, pressure/wind fields and forecasts")),
    dict(group=t("海洋内部", "Ocean interior"), name=t("内重力波\nInternal gravity wave", "Internal gravity wave"), medium=t("稳定层结海洋内部", "Stably stratified ocean interior"), restoring=t("浮力；旋转提供低频界限", "Buoyancy; rotation sets lower-frequency bound"), assumptions=t("Boussinesq、线性、均匀 N 与 f", "Boussinesq, linear, uniform N and f"), dispersion=t("ω²=(N²K²+f²m²)/(K²+m²)", "ω²=(N²K²+f²m²)/(K²+m²)"), dispersive=t("强色散；自由传播通常 |f|<|ω|<N", "Strongly dispersive; usually |f|<|ω|<N"), period=t("数分钟–数十小时", "minutes to tens of hours"), scale=t("水平 0.1–100 km；垂向模态/波束", "0.1–100 km horizontal; modes/beams"), propagation=t("相位与能量方向可不同；能量沿波束", "Phase and energy directions differ; energy follows beams"), source=t("潮流越过地形、风、对流、流剪切", "Tides over topography, wind, convection, shear"), observation=t("温盐链、ADCP、Argo/滑翔机、SAR", "T/S chains, ADCP, Argo/gliders, SAR")),
    dict(group=t("海洋内部", "Ocean interior"), name=t("内潮\nInternal tide", "Internal tide"), medium=t("层结内部；海岭与陆坡附近生成", "Stratified interior; generated near ridges/slopes"), restoring=t("浮力；潮汐周期强迫", "Buoyancy; tidal-frequency forcing"), assumptions=t("内波垂向模态；ω 固定为潮频", "Internal-wave modes; ω fixed at tidal frequency"), dispersion=t("ω=ω潮；水平波数由内波频散式与模态决定", "ω=ωtide; horizontal wavenumber set by internal-wave dispersion and mode"), dispersive=t("多模态、可相干跨盆地；非线性时转为孤立波", "Multimodal, coherently basin-spanning; may steepen into solitary waves"), period=t("主要 12.42 h 或 24 h 附近", "mainly near 12.42 h or 24 h"), scale=t("约 10–1000 km", "about 10–1000 km"), propagation=t("从生成地辐射；模态群速不同", "Radiates from generation sites; modal group speeds differ"), source=t("正压潮流跨越海脊、海峡、陆坡", "Barotropic tide over ridges, straits and slopes"), observation=t("卫星高度计/SAR、潜标、剖面与微结构", "Altimetry/SAR, moorings, profiles and microstructure")),
    dict(group=t("海洋内部", "Ocean interior"), name=t("惯性振荡／惯性波\nInertial oscillation", "Inertial oscillation / wave"), medium=t("海洋混合层与旋转流体内部", "Ocean mixed layer and rotating-fluid interior"), restoring=t("科氏力", "Coriolis force"), assumptions=t("水平无压强梯度的自由惯性运动", "Free horizontal motion without pressure gradient"), dispersion=t("局地惯性振荡 ω=±f；三维惯性波 |ω|≤2Ω", "Local oscillation ω=±f; 3-D inertial waves |ω|≤2Ω"), dispersive=t("局地频率由纬度决定；赤道 f→0", "Local frequency set by latitude; f→0 at equator"), period=t("T=2π/|f|；约 12 h–数天", "T=2π/|f|; about 12 h to days"), scale=t("局地至数百 km", "local to hundreds of km"), propagation=t("北半球水平速度顺时针旋转", "Horizontal velocity rotates clockwise in NH"), source=t("风暴突然停止/改变、混合层调整", "Abrupt wind change, mixed-layer adjustment"), observation=t("漂流浮标、ADCP、流速时间序列", "Drifters, ADCP and current time series")),
    dict(group=t("旋转波动", "Rotating waves"), name=t("Poincaré／惯性—重力波\nPoincaré / inertia–gravity", "Poincaré / inertia–gravity wave"), medium=t("旋转浅水层；海洋或大气等效层", "Rotating shallow-water layer in ocean or atmosphere"), restoring=t("重力/浮力 + 科氏力", "Gravity/buoyancy plus Coriolis"), assumptions=t("f 平面、线性浅水、波速 c", "f-plane, linear shallow water, speed c"), dispersion=t("ω²=f²+c²K²", "ω²=f²+c²K²"), dispersive=t("有截止频率 |f|；高波数趋近重力波", "Cutoff at |f|; approaches gravity wave at high wavenumber"), period=t("数十分钟–数天", "tens of minutes to days"), scale=t("约 10–1000+ km", "about 10–1000+ km"), propagation=t("可向各方向传播；相速与群速不同", "Propagates in any direction; phase and group speeds differ"), source=t("快速质量/动量扰动、地转调整", "Rapid mass/momentum disturbance, geostrophic adjustment"), observation=t("海平面/位势高度、风流场频谱", "Sea level/geopotential and velocity spectra")),
    dict(group=t("旋转波动", "Rotating waves"), name=t("沿岸 Kelvin 波\nCoastal Kelvin wave", "Coastal Kelvin wave"), medium=t("海岸、陆坡或垂直边界附近", "Near a coast, slope or vertical boundary"), restoring=t("沿岸重力传播 + 横岸地转平衡", "Along-boundary gravity propagation + cross-shore geostrophy"), assumptions=t("线性浅水；边界法向流为零", "Linear shallow water; zero normal flow at boundary"), dispersion=t("ω=±ck；横岸振幅 ∝exp(−x/Rd)，Rd=c/|f|", "ω=±ck; cross-shore amplitude ∝exp(−x/Rd), Rd=c/|f|"), dispersive=t("理想情况下无色散；边界选择单向支", "Ideally non-dispersive; boundary selects one branch"), period=t("数小时–数月", "hours to months"), scale=t("沿岸 10–10000 km；横岸约 Rd", "10–10000 km alongshore; cross-shore ≈Rd"), propagation=t("北半球传播时海岸在右侧", "In NH the coast lies to the right of propagation"), source=t("风、潮汐、海啸、边界调整", "Wind, tides, tsunamis, boundary adjustment"), observation=t("沿岸验潮站相位、卫星高度计", "Coastal gauge phase and satellite altimetry")),
    dict(group=t("旋转波动", "Rotating waves"), name=t("Rossby／行星波\nRossby / planetary wave", "Rossby / planetary wave"), medium=t("海洋与大气大尺度内部", "Large-scale ocean and atmosphere"), restoring=t("背景位涡梯度 β 与位涡守恒", "Background PV gradient β and PV conservation"), assumptions=t("β 平面、准地转、线性", "β-plane, quasigeostrophic, linear"), dispersion=t("ω=Uk−βk/(K²+Rd⁻²)", "ω=Uk−βk/(K²+Rd⁻²)"), dispersive=t("强色散；静止背景中波相通常向西", "Strongly dispersive; phase usually westward in resting medium"), period=t("数天–数十年", "days to decades"), scale=t("约 100–10000+ km", "about 100–10000+ km"), propagation=t("相速向西；群速可与相速不同甚至向东", "Westward phase; group velocity can differ or be eastward"), source=t("风应力、加热、地形、流不稳定", "Wind stress, heating, topography, flow instability"), observation=t("SSH/位势高度、OLR、再分析与 Hovmöller 图", "SSH/geopotential, OLR, reanalysis and Hovmöller diagrams")),
    dict(group=t("旋转波动", "Rotating waves"), name=t("地形 Rossby／陆架波\nTopographic Rossby / shelf wave", "Topographic Rossby / shelf wave"), medium=t("陆架坡折、海山和等深线附近", "Shelf breaks, seamounts and isobaths"), restoring=t("水深变化产生的地形位涡梯度", "Topographic PV gradient from depth changes"), assumptions=t("准地转、弱坡度；沿等深线传播", "Quasigeostrophic, gentle slope; along isobaths"), dispersion=t("ω≈Uk−βtopo k/(K²+Rd⁻²)，βtopo≈f₀∂lnH/∂y", "ω≈Uk−βtopo k/(K²+Rd⁻²), βtopo≈f₀∂lnH/∂y"), dispersive=t("低频色散；公式符号依坐标/坡向", "Low-frequency dispersive; sign depends on coordinates/slope"), period=t("数小时–数月", "hours to months"), scale=t("约 10–1000 km", "about 10–1000 km"), propagation=t("沿等深线；北半球常使浅水位于右侧", "Along isobaths; often shallow water on right in NH"), source=t("沿坡流扰动、风、涡旋和潮汐", "Slope-current disturbances, wind, eddies and tides"), observation=t("陆架流速阵列、底压、海平面", "Shelf current arrays, bottom pressure and sea level")),
    dict(group=t("赤道波导", "Equatorial waveguide"), name=t("赤道 Kelvin 波\nEquatorial Kelvin wave", "Equatorial Kelvin wave"), medium=t("赤道海洋/大气，赤道附近俘获", "Equatorial ocean/atmosphere, equatorially trapped"), restoring=t("重力 + β 效应；经向风/流 v=0", "Gravity plus β effect; meridional velocity v=0"), assumptions=t("赤道 β 平面、浅水等效深度 hₑ", "Equatorial β-plane, equivalent depth hₑ"), dispersion=t("ω=ck（仅东传）；c=√(ghₑ)，Le=√(c/β)", "ω=ck (eastward only); c=√(ghₑ), Le=√(c/β)"), dispersive=t("理想情况下无色散；高斯型经向俘获", "Ideally non-dispersive; Gaussian meridional trapping"), period=t("数天–数月", "days to months"), scale=t("东西 1000–40000 km；南北约 Le", "1000–40000 km zonal; meridional ≈Le"), propagation=t("东传；海洋第一斜压模常约 2–3 m s⁻¹", "Eastward; first oceanic baroclinic mode often 2–3 m s⁻¹"), source=t("风异常、MJO/对流、ENSO 调整", "Wind anomalies, MJO/convection, ENSO adjustment"), observation=t("赤道海平面、跃层深度、OLR 与风", "Equatorial SSH, thermocline depth, OLR and wind")),
    dict(group=t("赤道波导", "Equatorial waveguide"), name=t("赤道 Rossby 波\nEquatorial Rossby wave", "Equatorial Rossby wave"), medium=t("赤道两侧对称/反对称模态", "Symmetric/antisymmetric modes about equator"), restoring=t("赤道 β 与位涡守恒", "Equatorial β and PV conservation"), assumptions=t("长波低频近似；模态序号 n≥1", "Long-wave, low-frequency approximation; n≥1"), dispersion=t("ω≈−βk/[k²+(2n+1)/Le²]", "ω≈−βk/[k²+(2n+1)/Le²]"), dispersive=t("色散；静止背景中西传", "Dispersive; westward in resting medium"), period=t("数天–数月/年", "days to months/years"), scale=t("约 1000–20000 km", "about 1000–20000 km"), propagation=t("西传；在赤道两侧出现涡旋对", "Westward; gyre pairs straddle equator"), source=t("热带加热、风应力和 Kelvin 波反射", "Tropical heating, wind stress and reflected Kelvin waves"), observation=t("OLR、风、SSH 与跃层异常", "OLR, winds, SSH and thermocline anomalies")),
    dict(group=t("赤道波导", "Equatorial waveguide"), name=t("混合 Rossby—重力波／Yanai 波\nMixed Rossby–gravity wave", "Mixed Rossby–gravity / Yanai wave"), medium=t("赤道海洋与大气；n=0 模态", "Equatorial ocean/atmosphere; n=0 mode"), restoring=t("重力与位涡梯度共同作用", "Combined gravity and PV-gradient effects"), assumptions=t("赤道 β 平面浅水方程", "Equatorial β-plane shallow-water equations"), dispersion=t("ω²−c²k²−βc²k/ω=(2n+1)βc，取 n=0", "ω²−c²k²−βc²k/ω=(2n+1)βc, with n=0"), dispersive=t("西传长波似 Rossby；东传短波似重力波", "Westward long waves are Rossby-like; eastward short waves gravity-like"), period=t("约 3–30 d（大气常见）", "about 3–30 d, common in atmosphere"), scale=t("约 1000–10000 km", "about 1000–10000 km"), propagation=t("可东/西传；经向风跨赤道为反对称", "Eastward or westward; meridional wind antisymmetric"), source=t("热带对流、风和初始扰动", "Tropical convection, wind and initial disturbances"), observation=t("OLR—风谱、赤道流速/海平面", "OLR–wind spectra, equatorial currents/SSH")),
    dict(group=t("赤道波导", "Equatorial waveguide"), name=t("赤道惯性—重力波\nEquatorial inertia–gravity wave", "Equatorial inertia–gravity wave"), medium=t("赤道波导；高频分支", "Equatorial waveguide; high-frequency branches"), restoring=t("重力/浮力 + β 效应", "Gravity/buoyancy plus β effect"), assumptions=t("赤道浅水方程；n≥0", "Equatorial shallow-water equations; n≥0"), dispersion=t("ω²−c²k²−βc²k/ω=(2n+1)βc", "ω²−c²k²−βc²k/ω=(2n+1)βc"), dispersive=t("东传和西传高频支；有赤道俘获", "Eastward and westward high-frequency branches; trapped"), period=t("约 1–10 d（大气）", "about 1–10 d in atmosphere"), scale=t("约 1000–10000 km", "about 1000–10000 km"), propagation=t("相速快于赤道 Rossby；能量可上下传播", "Faster phase than equatorial Rossby; energy may propagate vertically"), source=t("深对流、加热脉冲、地转调整", "Deep convection, heating pulses, geostrophic adjustment"), observation=t("OLR、风场、温度和位势高度谱", "OLR, winds, temperature and geopotential spectra")),
    dict(group=t("大气波动", "Atmospheric waves"), name=t("大气重力波／山岳波\nAtmospheric gravity / mountain wave", "Atmospheric gravity / mountain wave"), medium=t("稳定层结对流层至中高层大气", "Stably stratified troposphere to upper atmosphere"), restoring=t("浮力；旋转修正低频", "Buoyancy; rotation modifies low frequencies"), assumptions=t("线性、Boussinesq/非弹性；本征频率 ω̂=ω−U·k", "Linear Boussinesq/anelastic; intrinsic frequency ω̂=ω−U·k"), dispersion=t("ω̂²=(N²K²+f²m²)/(K²+m²)", "ω̂²=(N²K²+f²m²)/(K²+m²)"), dispersive=t("强色散；山岳波在地面系常 ω≈0", "Strongly dispersive; mountain waves often ω≈0 in ground frame"), period=t("约 5 min–数小时", "about 5 min to hours"), scale=t("约 1–1000 km", "about 1–1000 km"), propagation=t("能量常向上传播；破碎后产生重力波拖曳", "Energy often upward; breaking produces gravity-wave drag"), source=t("地形、对流、急流/锋面、风切变", "Topography, convection, jets/fronts and shear"), observation=t("卫星亮温/气辉、雷达、探空、激光雷达", "Satellite brightness/airglow, radar, soundings, lidar")),
    dict(group=t("大气波动", "Atmospheric waves"), name=t("声波\nAcoustic wave", "Acoustic wave"), medium=t("可压缩海水或大气；大气中最典型", "Compressible ocean or atmosphere; most familiar in air"), restoring=t("可压缩性产生的压力梯度", "Pressure gradient from compressibility"), assumptions=t("均匀无耗散介质；忽略重力/旋转", "Uniform, inviscid medium; neglect gravity/rotation"), dispersion=t("ω²=cₛ²(K²+m²)", "ω²=cₛ²(K²+m²)"), dispersive=t("理想均匀介质无色散；cₛ 为空气/海水声速", "Non-dispersive in ideal uniform medium; speed cₛ"), period=t("毫秒–数分钟", "milliseconds to minutes"), scale=t("厘米–数百 km", "centimetres to hundreds of km"), propagation=t("纵向压缩波；空气约 340 m s⁻¹，海水约 1500 m s⁻¹", "Longitudinal compression wave; ~340 m s⁻¹ in air, ~1500 m s⁻¹ in seawater"), source=t("爆炸、雷暴、火山、机械振动", "Explosions, thunderstorms, volcanoes, mechanical vibration"), observation=t("微气压计、水听器、声学遥感", "Microbarometers, hydrophones, acoustic remote sensing")),
    dict(group=t("大气波动", "Atmospheric waves"), name=t("Lamb 波\nLamb wave", "Lamb wave"), medium=t("大气边界附近的水平压缩模态", "Horizontally propagating atmospheric compression mode"), restoring=t("可压缩性 + 重力维持的垂向结构", "Compressibility plus gravity-supported vertical structure"), assumptions=t("等温/静力大气；垂直速度近零、垂向衰减", "Isothermal/hydrostatic atmosphere; near-zero vertical velocity, evanescent"), dispersion=t("ω²≈cL²K²，cL≈√(γRT)", "ω²≈cL²K², cL≈√(γRT)"), dispersive=t("理想情况下近无色散；可绕地球传播多圈", "Nearly non-dispersive ideally; can circle the globe repeatedly"), period=t("数分钟–数小时", "minutes to hours"), scale=t("区域至全球尺度", "regional to global scale"), propagation=t("接近声速水平传播；地面气压信号突出", "Near-acoustic horizontal speed; strong surface-pressure signal"), source=t("大型火山喷发、爆炸、强对流", "Major eruptions, explosions and intense convection"), observation=t("全球微气压计与地面气压网", "Global infrasound and surface-pressure networks")),
    dict(group=t("大气波动", "Atmospheric waves"), name=t("大气潮汐\nAtmospheric tide", "Atmospheric tide"), medium=t("全球大气；随高度振幅常增大", "Global atmosphere; amplitude often increases with height"), restoring=t("太阳加热/引潮势周期强迫；重力与旋转", "Periodic solar heating/tidal potential; gravity and rotation"), assumptions=t("Laplace 潮汐方程；Hough 水平模态", "Laplace tidal equations; Hough horizontal modes"), dispersion=t("受迫于 24 h、12 h 等频率；垂向波数由等效深度决定", "Forced at 24 h, 12 h, etc.; vertical wavenumber set by equivalent depth"), dispersive=t("多 Hough 模态；辐射、摩擦与背景风影响", "Multiple Hough modes; affected by radiation, friction and mean wind"), period=t("24 h、12 h、8 h 等", "24 h, 12 h, 8 h, etc."), scale=t("行星尺度", "planetary scale"), propagation=t("迁移潮随太阳向西；非迁移潮可东西传播", "Migrating tide follows the Sun westward; nonmigrating tides vary"), source=t("臭氧/水汽吸收太阳辐射、潜热与地形", "Solar absorption by ozone/water vapour, latent heating and topography"), observation=t("雷达、卫星温度/风、气压", "Radar, satellite temperature/winds and pressure")),
    dict(group=t("大气波动", "Atmospheric waves"), name=t("天气尺度斜压 Rossby 波\nSynoptic baroclinic Rossby wave", "Synoptic baroclinic Rossby wave"), medium=t("中纬度对流层急流与锋区", "Midlatitude tropospheric jets and frontal zones"), restoring=t("位涡梯度；斜压不稳定可放大扰动", "PV gradients; baroclinic instability can amplify disturbances"), assumptions=t("准地转、分层、垂向风切变", "Quasigeostrophic, stratified, vertical shear"), dispersion=t("实部近 Rossby：ω≈Uk−βk/(K²+Rd⁻²)；不稳定时 Im(ω)>0", "Real part Rossby-like: ω≈Uk−βk/(K²+Rd⁻²); Im(ω)>0 when unstable"), dispersive=t("传播且可增长；不是单纯中性自由波", "Propagating and growing; not a purely neutral free wave"), period=t("约 2–10 d", "about 2–10 d"), scale=t("约 1000–5000 km", "about 1000–5000 km"), propagation=t("通常随西风向东；群速造成下游发展", "Usually eastward with westerlies; group velocity drives downstream development"), source=t("南北温度梯度和垂直风切变的可用位能", "Available potential energy from meridional temperature gradient and vertical shear"), observation=t("500 hPa 高度、卫星云图、再分析涡度/位涡", "500-hPa height, satellite clouds and reanalysis vorticity/PV")),
]


FIELDS = ["group", "name", "medium", "restoring", "assumptions", "dispersion", "dispersive", "period", "scale", "propagation", "source", "observation"]
HEADERS = {
    "zh": ["类别", "波动名称", "介质/位置", "恢复力或主导平衡", "主要近似/垂向结构", "频散关系（K²=k²+l²）", "色散性/频率界限", "典型周期", "波长/水平尺度", "传播方向与速度特征", "典型激发源", "主要观测与意义"],
    "en": ["Family", "Wave", "Medium / location", "Restoring mechanism / balance", "Main approximation / vertical structure", "Dispersion relation (K²=k²+l²)", "Dispersion / frequency bounds", "Typical period", "Wavelength / horizontal scale", "Propagation and speed", "Typical source", "Main observations / relevance"],
}

GROUP_COLORS = {
    "海面与海岸": "#dff4f1",
    "海洋内部": "#e3eef9",
    "旋转波动": "#eee6f7",
    "赤道波导": "#fff0d8",
    "大气波动": "#f7e4e2",
    "Surface & coastal": "#dff4f1",
    "Ocean interior": "#e3eef9",
    "Rotating waves": "#eee6f7",
    "Equatorial waveguide": "#fff0d8",
    "Atmospheric waves": "#f7e4e2",
}


def write_data() -> None:
    payload = {"version": 1, "symbols": {"zh": "ω 角频率；k,l 水平波数；K 水平总波数；m 垂向波数；H 水深；f 科氏参数；β=df/dy；N 浮力频率；Rd 变形半径；c 相速或模态长波速度。", "en": "ω angular frequency; k,l horizontal wavenumbers; K total horizontal wavenumber; m vertical wavenumber; H depth; f Coriolis parameter; β=df/dy; N buoyancy frequency; Rd deformation radius; c phase or modal long-wave speed."}, "fields": FIELDS, "headers": HEADERS, "rows": ROWS}
    (OUT / "ocean_atmosphere_wave_atlas.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    for lang in ("zh", "en"):
        suffix = "" if lang == "zh" else "-en"
        with (OUT / f"ocean_atmosphere_wave_atlas{suffix}.csv").open("w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(HEADERS[lang])
            for row in ROWS:
                writer.writerow([row[field][lang].replace("\n", " / ") for field in FIELDS])


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "msyhbd.ttc" if bold else "msyh.ttc"
    return ImageFont.truetype(str(Path("C:/Windows/Fonts") / name), size=size)


def wrap(draw: ImageDraw.ImageDraw, text: str, ft: ImageFont.FreeTypeFont, width: int) -> list[str]:
    lines: list[str] = []
    for block in text.split("\n"):
        if not block:
            lines.append("")
            continue
        current = ""
        for ch in block:
            candidate = current + ch
            if draw.textlength(candidate, font=ft) <= width or not current:
                current = candidate
            else:
                lines.append(current)
                current = ch
        if current:
            lines.append(current)
    return lines


def render(lang: str) -> None:
    widths = [330, 560, 570, 620, 650, 900, 580, 410, 470, 650, 560, 620]
    pad_x, pad_y = 22, 18
    margin = 70
    title_h = 230
    footer_h = 180
    header_h = 150
    body_font = font(31)
    body_bold = font(31, True)
    head_font = font(31, True)
    title_font = font(70, True)
    sub_font = font(30)
    line_h = 48
    probe = Image.new("RGB", (sum(widths) + 2 * margin, 1000), "white")
    pd = ImageDraw.Draw(probe)
    row_heights: list[int] = []
    wrapped_rows: list[list[list[str]]] = []
    for row in ROWS:
        wrapped = [wrap(pd, row[field][lang], body_bold if field in ("group", "name") else body_font, widths[i] - 2 * pad_x) for i, field in enumerate(FIELDS)]
        wrapped_rows.append(wrapped)
        row_heights.append(max(132, max(len(lines) for lines in wrapped) * line_h + 2 * pad_y))
    total_w = sum(widths) + 2 * margin
    total_h = title_h + header_h + sum(row_heights) + footer_h + margin
    image = Image.new("RGB", (total_w, total_h), "#f8fbfb")
    d = ImageDraw.Draw(image)
    title = "海洋与大气中的主要波动汇总表" if lang == "zh" else "Major Waves in the Ocean and Atmosphere"
    subtitle = "22 类波动 · 12 项特征 · 频散关系、尺度、传播、激发与观测" if lang == "zh" else "22 wave types · 12 attributes · dispersion, scales, propagation, forcing and observation"
    d.text((margin, 45), title, fill="#082943", font=title_font)
    d.text((margin, 140), subtitle, fill="#456879", font=sub_font)
    x0, y = margin, title_h
    x = x0
    for i, head in enumerate(HEADERS[lang]):
        d.rectangle((x, y, x + widths[i], y + header_h), fill="#073f68", outline="#c4d9df", width=2)
        lines = wrap(d, head, head_font, widths[i] - 2 * pad_x)
        ty = y + (header_h - len(lines) * line_h) / 2
        for line in lines:
            d.text((x + pad_x, ty), line, fill="white", font=head_font)
            ty += line_h
        x += widths[i]
    y += header_h
    last_group = None
    stripe = False
    for row, wrapped, rh in zip(ROWS, wrapped_rows, row_heights):
        group = row["group"][lang]
        if group != last_group:
            stripe = False
            last_group = group
        base = GROUP_COLORS[group]
        x = x0
        for i, (field, lines) in enumerate(zip(FIELDS, wrapped)):
            fill = base if field == "group" else ("#f4f8f8" if stripe else "#ffffff")
            d.rectangle((x, y, x + widths[i], y + rh), fill=fill, outline="#c5d6da", width=2)
            ft = body_bold if field in ("group", "name") else body_font
            ty = y + max(pad_y, (rh - len(lines) * line_h) / 2)
            for line in lines:
                d.text((x + pad_x, ty), line, fill="#102f42", font=ft)
                ty += line_h
            x += widths[i]
        y += rh
        stripe = not stripe
    legend = ("符号：" if lang == "zh" else "Symbols: ") + ({"zh": "ω 角频率；k,l 水平波数；K²=k²+l²；m 垂向波数；H 水深；f 科氏参数；β=df/dy；N 浮力频率；Rd 变形半径；c 波速。", "en": "ω angular frequency; k,l horizontal wavenumbers; K²=k²+l²; m vertical wavenumber; H depth; f Coriolis parameter; β=df/dy; N buoyancy frequency; Rd deformation radius; c wave speed."}[lang])
    note = "范围为典型量级，会随纬度、水深、层结、背景流与等效深度变化。受迫响应已明确标注，不应把所有行都理解为中性自由波。" if lang == "zh" else "Ranges are typical orders of magnitude and vary with latitude, depth, stratification, background flow and equivalent depth. Forced responses are labelled and should not all be read as neutral free waves."
    d.text((margin, y + 35), legend, fill="#173f54", font=sub_font)
    d.text((margin, y + 92), note, fill="#5b7079", font=sub_font)
    suffix = "" if lang == "zh" else "-en"
    image.save(OUT / f"ocean_atmosphere_wave_atlas{suffix}.png", optimize=True)


if __name__ == "__main__":
    write_data()
    render("zh")
    render("en")
    print(f"Generated {len(ROWS)} rows in {OUT}")
