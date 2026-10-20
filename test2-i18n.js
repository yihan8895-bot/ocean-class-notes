/* Complete bilingual copy for test2; follows the site-wide language state. */
(() => {
  'use strict';

  const groups = [
    ['.identity > span:last-child', [[
      '海洋课堂笔记<small>物理海洋学</small>',
      'Ocean Classroom Notes<small>PHYSICAL OCEANOGRAPHY</small>'
    ]]],
    ['.site-header nav a', [
      ['资料库', 'Library'], ['地转流', 'Geostrophy'], ['EOF', 'EOF'], ['海洋热浪', 'MHW'],
      ['test1', 'test1'], ['test2', 'test2'], ['添加内容 ↗', 'Add Content ↗']
    ]],
    ['.t2-kicker', [['测试 2 · 物理海洋学', 'TEST 2 · PHYSICAL OCEANOGRAPHY']]],
    ['.t2-hero h1', [[
      '观测海洋<br><span>并从观测中读懂海流</span>',
      'Measuring the Ocean<br><span>and Reading Its Currents</span>'
    ]]],
    ['.t2-lead', [[
      '一套完整的分层回答，涵盖观测仪器、方法优缺点、地转平衡、反演条件、数值检验和南海数据证据。',
      'A complete, layered answer covering instruments, observing methods, geostrophic balance, inference requirements, a numerical check and evidence from South China Sea data.'
    ]]],
    ['.t2-actions a', [
      ['从简要答案开始 ↓', 'Start with the brief answer ↓'], ['查看数据证据', 'See the data evidence']
    ]],
    ['.question-card > span', [['题目', 'THE QUESTION']]],
    ['.question-card p', [[
      '简要说明常用于测量海洋温度、盐度和海流的仪器与方法，并讨论各自的优点和局限。利用地转平衡概念，解释海水密度或海表高度的水平变化如何与海流相关。讨论可以根据观测数据反演地转流所需的条件。',
      'Briefly describe the instruments and methods commonly used to measure ocean temperature, salinity, and currents, and discuss their advantages and limitations. Using the concept of geostrophic balance, explain how horizontal variations in seawater density or sea surface height are related to ocean currents. Discuss the conditions under which geostrophic currents can be inferred from observational data.'
    ]]],
    ['.t2-toc > strong', [['目录', 'CONTENTS']]],
    ['.t2-toc a', [
      ['<b>01</b> 简要回答', '<b>01</b> Brief answer'],
      ['<b>02</b> 观测仪器', '<b>02</b> Instruments'],
      ['<b>03</b> 地转理论', '<b>03</b> Geostrophic theory'],
      ['<b>04</b> 反演流程', '<b>04</b> Inference workflows'],
      ['<b>05</b> 数据证据', '<b>05</b> Data evidence'],
      ['<b>06</b> 适用条件', '<b>06</b> Conditions'],
      ['<b>07</b> 综合答案', '<b>07</b> Model answer'],
      ['<b>08</b> 自检', '<b>08</b> Self-check']
    ]],
    ['.section-label', [
      ['层次 1 · 简要回答', 'LEVEL 1 · BRIEF ANSWER'],
      ['层次 2 · 观测工具箱', 'LEVEL 2 · MEASUREMENT TOOLKIT'],
      ['层次 2 · 物理联系', 'LEVEL 2 · PHYSICAL LINK'],
      ['层次 3 · 观测反演', 'LEVEL 3 · OBSERVATIONAL INFERENCE'],
      ['层次 3 · 南海数据证据', 'LEVEL 3 · SOUTH CHINA SEA EVIDENCE'],
      ['层次 3 · 反演何时有效', 'LEVEL 3 · WHEN THE INFERENCE IS VALID'],
      ['可直接提交的参考答案', 'SUBMISSION-READY MODEL ANSWER'],
      ['质量控制', 'QUALITY CONTROL'],
      ['资料与数据来源', 'SOURCES AND DATA']
    ]],
    ['.t2-article h2', [
      ['一分钟掌握答案', 'The answer in one minute'],
      ['测量什么，又如何测量？', 'What is measured, and how?'],
      ['从压强梯度到海流', 'From pressure gradients to currents'],
      ['从观测到地转流速的两条路径', 'Two routes from observations to geostrophic velocity'],
      ['现有数据能够与不能说明什么', 'What the available data can—and cannot—show'],
      ['反演地转流所需的条件', 'Conditions for inferring geostrophic currents'],
      ['综合回答', 'Integrated response'],
      ['自检与适用范围', 'Self-check and scope'],
      ['参考资料', 'References']
    ]],
    ['#brief p', [
      [
        '海洋温度和盐度通常用 <strong>CTD</strong> 测量：热敏电阻测量温度，电导池测量电导率，并结合温度和压力换算盐度，压力传感器则给出深度。船载 CTD 采水器能获得准确、高垂向分辨率的剖面和水样，但成本高且空间采样稀疏。Argo 浮标、潜标和滑翔机扩大了覆盖范围与观测时长，但对采样位置的控制和传感器回收较有限。卫星可提供大范围、重复的海表温度和盐度图，但只能观测很薄的表层，并需要校准。海流可由流速计、<strong>ADCP</strong>、漂流浮标、剖面浮标和岸基高频雷达直接测量；其局限包括观测深度、覆盖范围、持续时间、空间采样以及波浪、潮汐和平台运动的影响。',
        'Ocean temperature and salinity are commonly measured with a <strong>CTD</strong>: a thermistor measures temperature, a conductivity cell provides salinity after conversion using temperature and pressure, and a pressure sensor gives depth. Shipboard CTD rosettes provide accurate, high-resolution profiles and water samples but are costly and sparse. Argo floats, moorings and gliders extend coverage and duration, with less control over sampling and sensor recovery. Satellites offer broad, repeated maps of sea-surface temperature and salinity but observe only a shallow surface layer and require calibration. Currents are measured directly with current meters, <strong>ADCPs</strong>, drifters, floats and coastal HF radar; their trade-offs include limited depth, range, duration, spatial coverage and sensitivity to waves, tides or platform motion.'
      ],
      [
        '对于大尺度、缓慢变化且摩擦较弱的流动，水平压强梯度力与科氏力近似平衡。因此，海表高度坡度对应沿等高度线流动的表层地转流。水平方向的密度差异会使压强差随深度变化，并通过<strong>热成风平衡</strong>决定地转流的垂向切变。卫星测高可以从海表高度梯度估算表层地转流；水文温盐剖面则可从动力高度差估算相对地转流。可靠反演要求观测具有足够空间分辨率和近同时性，定位与改正准确，观测区远离赤道，罗斯贝数较小、摩擦较弱；使用水文资料时还需要参考层或独立流速作为基准。',
        'For large-scale, slowly varying flow with weak friction, the horizontal pressure-gradient force approximately balances the Coriolis force. A sea-surface-height slope therefore implies a surface geostrophic current parallel to height contours. Horizontal density differences create pressure differences that change with depth, so they determine the <strong>vertical shear</strong> of the geostrophic current through thermal-wind balance. Altimetry can estimate surface geostrophic velocity from sea-surface-height gradients; hydrographic temperature-salinity profiles can estimate relative geostrophic velocity from dynamic-height differences. Reliable inference requires observations with adequate spatial resolution and near-synoptic timing, accurate positioning and corrections, distance from the equator, a small Rossby number, weak friction, and a reference level or independent velocity for hydrographic estimates.'
      ]
    ]],
    ['#measure .section-intro', [[
      '每种方法所覆盖的深度、区域和时间尺度都不同。高质量答案应同时说明测量原理和采样上的取舍。',
      'Every method samples a different combination of depth, area and time. A strong answer identifies both the physical principle and the sampling trade-off.'
    ]]],
    ['#measure .table-wrap table', [[
      `<thead><tr><th>变量</th><th>仪器或方法</th><th>测量内容</th><th>主要优点</th><th>主要局限</th></tr></thead>
      <tbody>
        <tr><th rowspan="4">温度</th><td><strong>船载 CTD / 热敏电阻</strong></td><td>原位温度随压力的剖面；通常随采水器下放。</td><td>垂向分辨率和精度高；温盐同步观测；水样可用于实验室核验。</td><td>船时昂贵；断面空间稀疏且并非完全同步。</td></tr>
        <tr><td><strong>XBT</strong></td><td>投弃式探头测温；利用下降速率估算深度。</td><td>航行中可快速、相对低成本地获取剖面。</td><td>不测盐度；探头一次性使用；下降速率和深度偏差需要订正。</td></tr>
        <tr><td><strong>Argo、滑翔机、潜标</strong></td><td>自动重复剖面或定点时间序列。</td><td>可长期、广域或持续观测次表层；恶劣天气下也能工作。</td><td>采样路径和深度受限；可能出现资料空缺、漂移和延迟校准。</td></tr>
        <tr><td><strong>卫星辐射计</strong></td><td>红外或微波亮温所对应的海洋皮肤层/次表层温度。</td><td>频繁、近全球的空间图像。</td><td>只观测表层；红外受云遮挡；反演需进行大气订正和现场验证。</td></tr>
        <tr><th rowspan="3">盐度</th><td><strong>CTD 电导池</strong></td><td>测量电导率、温度和压力，并换算为实用盐度。</td><td>准确且温盐共位，适合计算密度。</td><td>生物附着和传感器漂移会影响结果；盐度是由电导率间接得到的。</td></tr>
        <tr><td><strong>Niskin 采水瓶 + 盐度计</strong></td><td>在实验室分析离散水样。</td><td>可作为高质量参考和校准样本，也能分析其他性质。</td><td>深度和站位数量有限；采样和分析耗时。</td></tr>
        <tr><td><strong>Argo / 卫星 L 波段</strong></td><td>自动温盐剖面或微波海表盐度。</td><td>Argo 解析水柱结构；卫星提供盆地尺度表层图像。</td><td>Argo 时空分布不规则；卫星在近岸、降雨、海冰和低温水域噪声较大，且只代表表层。</td></tr>
        <tr><th rowspan="5">海流</th><td><strong>流速计</strong></td><td>通过旋桨、声学或电磁方法测量某一深度的流速。</td><td>提供长期、高频率的欧拉时间序列。</td><td>只代表一个或少数位置；系泊运动和生物附着可能影响资料。</td></tr>
        <tr><td><strong>ADCP</strong></td><td>测量颗粒声散射的多普勒频移，得到多个深度层的流速。</td><td>可同时获得多个深度的剖面；可安装在船舶、潜标或下放平台上。</td><td>量程与分辨率需权衡；需要足够散射体，并订正平台运动、航向和旁瓣影响。</td></tr>
        <tr><td><strong>漂流浮标和剖面浮标</strong></td><td>由轨迹随时间的位移得到拉格朗日流速。</td><td>可跟随水团运动较长距离。</td><td>采样稀疏且只代表特定深度；风曳、斯托克斯漂移和深度跟随误差会影响解释。</td></tr>
        <tr><td><strong>高频雷达</strong></td><td>利用无线电后向散射绘制近岸表层流速。</td><td>可近实时重复获取二维近岸表层流场。</td><td>仅覆盖近岸范围；几何条件、干扰和弱信号会造成资料空缺。</td></tr>
        <tr><td><strong>卫星测高</strong></td><td>测量海表高度，再由其水平坡度反演地转流。</td><td>覆盖范围广，重复采样较一致。</td><td>属于间接测量；沿轨采样和映射会平滑小尺度结构；需处理潮汐、大气、地球重力场和非地转运动。</td></tr>
      </tbody>`,
      `<thead><tr><th>Variable</th><th>Instrument or method</th><th>What it measures</th><th>Main advantages</th><th>Main limitations</th></tr></thead>
      <tbody>
        <tr><th rowspan="4">Temperature</th><td><strong>Ship CTD / thermistor</strong></td><td>In situ temperature versus pressure; often lowered on a rosette.</td><td>High vertical resolution and accuracy; paired T–S observations; bottles allow laboratory checks.</td><td>Ship time is expensive; sections are spatially sparse and not instantaneous.</td></tr>
        <tr><td><strong>XBT</strong></td><td>Temperature from a falling probe; depth is estimated from fall rate.</td><td>Fast and relatively inexpensive underway profiling.</td><td>No salinity; expendable; fall-rate and depth biases require correction.</td></tr>
        <tr><td><strong>Argo, gliders, moorings</strong></td><td>Repeated autonomous profiles or fixed time series.</td><td>Long duration, broad or sustained subsurface sampling; works in poor weather.</td><td>Sampling paths/depths are constrained; gaps, drift and delayed calibration can occur.</td></tr>
        <tr><td><strong>Satellite radiometers</strong></td><td>Infrared or microwave brightness related to skin/subskin SST.</td><td>Frequent, nearly global maps.</td><td>Surface only; infrared is blocked by cloud; retrievals need atmospheric correction and in situ validation.</td></tr>
        <tr><th rowspan="3">Salinity</th><td><strong>CTD conductivity cell</strong></td><td>Conductivity plus temperature and pressure, converted to Practical Salinity.</td><td>Accurate, co-located profiles suitable for density calculation.</td><td>Biofouling and sensor drift matter; conductivity is an indirect salinity measurement.</td></tr>
        <tr><td><strong>Niskin bottle + salinometer</strong></td><td>Discrete water sample analyzed in the laboratory.</td><td>High-quality reference and calibration samples; other properties can be measured.</td><td>Few depths and stations; sample handling takes time.</td></tr>
        <tr><td><strong>Argo / satellite L-band</strong></td><td>Autonomous profiles or microwave sea-surface salinity.</td><td>Argo resolves the water column; satellites provide basin-scale surface maps.</td><td>Argo is irregular in space/time; satellite signals are noisy near land, rain, ice and cold water and represent only the surface.</td></tr>
        <tr><th rowspan="5">Currents</th><td><strong>Current meter</strong></td><td>Velocity at one depth using rotors, acoustics or electromagnetic sensing.</td><td>Long, high-frequency Eulerian time series.</td><td>Only one or a few points; mooring motion and biofouling can affect data.</td></tr>
        <tr><td><strong>ADCP</strong></td><td>Doppler shift of sound scattered by particles, yielding velocity in depth bins.</td><td>Profiles several depths at once; can be shipboard, moored or lowered.</td><td>Range/resolution trade-off; needs scatterers and careful correction for platform motion, heading and sidelobes.</td></tr>
        <tr><td><strong>Drifters and floats</strong></td><td>Trajectory displacement over time: a Lagrangian velocity.</td><td>Follows water parcels over large distances.</td><td>Sparse and depth-specific; windage, Stokes drift and imperfect depth following can bias interpretation.</td></tr>
        <tr><td><strong>HF radar</strong></td><td>Radio backscatter used to map coastal surface velocity.</td><td>Repeated two-dimensional coastal maps in near real time.</td><td>Coastal range only; geometry, interference and low signal can create gaps.</td></tr>
        <tr><td><strong>Satellite altimetry</strong></td><td>Sea-surface height; geostrophic current is inferred from its horizontal slope.</td><td>Repeated, broad-scale coverage with consistent sampling.</td><td>Indirect; along-track sampling and mapping smooth small scales; tides, atmosphere, geoid and ageostrophic motions require treatment.</td></tr>
      </tbody>`
    ]]],
    ['.memory-grid', [[
      '<div><span>CTD</span><p><strong>C</strong>onductivity（电导率）→ 盐度<br><strong>T</strong>emperature（温度）→ 热状态<br><strong>D</strong>epth（深度）→ 由压力得到</p></div><div><span>ADCP</span><p>声学多普勒频移 → 水平流速的垂向剖面。</p></div><div><span>卫星</span><p>水平覆盖优异，但对海表以下缺少直接信息。</p></div>',
      '<div><span>CTD</span><p><strong>C</strong>onductivity → salinity<br><strong>T</strong>emperature → heat state<br><strong>D</strong>epth → from pressure</p></div><div><span>ADCP</span><p>Acoustic Doppler shift → a vertical profile of horizontal velocity.</p></div><div><span>Satellite</span><p>Excellent horizontal coverage; limited direct information below the surface.</p></div>'
    ]]],
    ['.equation-card p:last-child', [[
      '在地转平衡中，科氏加速度与水平压强梯度力大小相等、方向相反。海流沿等压线流动，而不是直接从高压流向低压。',
      'In geostrophic balance, the Coriolis acceleration and horizontal pressure-gradient force are equal and opposite. The current runs along pressure contours rather than directly from high pressure to low pressure.'
    ]]],
    ['.theory-grid', [[
      `<article><span>海表高度</span><p class="equation small"><i>u</i><sub>g</sub> = −<i>g</i>/<i>f</i> · ∂η/∂<i>y</i><br><i>v</i><sub>g</sub> = &nbsp;<i>g</i>/<i>f</i> · ∂η/∂<i>x</i></p><p>倾斜海面会在整个水柱中产生水平压强梯度。在北半球，较高海面位于地转流方向的右侧；南半球方向相反。</p></article><article><span>密度与热成风</span><p class="equation small">∂<i>u</i><sub>g</sub>/∂<i>z</i> = <i>g</i>/(<i>f</i>ρ<sub>0</sub>) · ∂ρ/∂<i>y</i><br>∂<i>v</i><sub>g</sub>/∂<i>z</i> = −<i>g</i>/(<i>f</i>ρ<sub>0</sub>) · ∂ρ/∂<i>x</i></p><p>压强来自上覆水体的重量，因此水平密度差使压强梯度随深度变化。倾斜的等密度面只决定垂向切变，本身不能给出绝对流速。</p></article>`,
      `<article><span>SEA-SURFACE HEIGHT</span><p class="equation small"><i>u</i><sub>g</sub> = −<i>g</i>/<i>f</i> · ∂η/∂<i>y</i><br><i>v</i><sub>g</sub> = &nbsp;<i>g</i>/<i>f</i> · ∂η/∂<i>x</i></p><p>A tilted sea surface creates a horizontal pressure gradient through the entire water column. In the Northern Hemisphere, higher sea level lies to the right of the geostrophic flow; the direction reverses in the Southern Hemisphere.</p></article><article><span>DENSITY AND THERMAL WIND</span><p class="equation small">∂<i>u</i><sub>g</sub>/∂<i>z</i> = <i>g</i>/(<i>f</i>ρ<sub>0</sub>) · ∂ρ/∂<i>y</i><br>∂<i>v</i><sub>g</sub>/∂<i>z</i> = −<i>g</i>/(<i>f</i>ρ<sub>0</sub>) · ∂ρ/∂<i>x</i></p><p>Because pressure is the weight of the water above, horizontal density contrasts make pressure gradients vary with depth. Sloping isopycnals therefore imply vertical shear, not an absolute velocity by themselves.</p></article>`
    ]]],
    ['.direction-note', [[
      '<strong>方向检验：</strong>若 30°N 的海面高度向东升高（∂η/∂x &gt; 0），则 <i>v</i><sub>g</sub> &gt; 0，海流向北。',
      '<strong>Direction check:</strong> if sea level rises eastward (∂η/∂x &gt; 0) at 30°N, then <i>v</i><sub>g</sub> &gt; 0: the current points north.'
    ]]],
    ['.workflow-grid', [[
      `<article class="workflow-card"><span class="workflow-no">A</span><h3>卫星测高路径：表层流速</h3><ol><li>测量卫星至海面的距离及卫星轨道。</li><li>订正潮汐、大气和仪器效应。</li><li>得到相对于大地水准面的海表高度，或将海平面异常与平均动力地形相加。</li><li>对资料进行映射，计算水平梯度，再应用表层地转公式。</li></ol><p class="result"><strong>输出：</strong>若具有绝对动力地形，可得到绝对表层地转流速的估计。</p></article><article class="workflow-card"><span class="workflow-no">B</span><h3>水文路径：相对流速</h3><ol><li>在相邻站位测量温度、盐度和压力。</li><li>进行质量控制，并依据 TEOS-10 转换为绝对盐度、保守温度和密度。</li><li>积分比容异常，得到动力高度。</li><li>利用水平动力高度差计算相对于所选压力面的地转切变或流速。</li></ol><p class="result"><strong>输出：</strong>相对地转流速；若要得到绝对流速，需要假设无运动层或使用独立参考流速。</p></article>`,
      `<article class="workflow-card"><span class="workflow-no">A</span><h3>Altimetric route: surface velocity</h3><ol><li>Measure satellite-to-surface range and orbit.</li><li>Correct for tides, atmosphere and instrumental effects.</li><li>Form sea-surface height relative to the geoid, or combine sea-level anomaly with mean dynamic topography.</li><li>Map the field, calculate horizontal gradients, and apply the surface equations above.</li></ol><p class="result"><strong>Output:</strong> an estimate of absolute surface geostrophic velocity when absolute dynamic topography is available.</p></article><article class="workflow-card"><span class="workflow-no">B</span><h3>Hydrographic route: relative velocity</h3><ol><li>Measure temperature, salinity and pressure at neighboring stations.</li><li>Apply quality control and convert to Absolute Salinity, Conservative Temperature and density using TEOS-10.</li><li>Integrate specific-volume anomaly to obtain dynamic height.</li><li>Use horizontal dynamic-height differences to calculate geostrophic shear or velocity relative to a chosen pressure.</li></ol><p class="result"><strong>Output:</strong> relative geostrophic velocity; an assumed level of no motion or an independent reference velocity is needed for an absolute current.</p></article>`
    ]]],
    ['.worked-example', [[
      '<div><span>计算示例</span><h3>30°N 处，海面高度在 100 km 内变化 20 cm</h3></div><div class="calculation"><p>∂η/∂x = 0.20 m / 100,000 m = 2.0 × 10<sup>−6</sup></p><p><i>f</i> = 2Ω sin 30° = 7.292 × 10<sup>−5</sup> s<sup>−1</sup></p><p><i>v</i><sub>g</sub> = (<i>g</i>/<i>f</i>)∂η/∂x = <strong>0.269 m s<sup>−1</sup>，方向向北</strong></p></div>',
      '<div><span>WORKED EXAMPLE</span><h3>A 20 cm height change across 100 km at 30°N</h3></div><div class="calculation"><p>∂η/∂x = 0.20 m / 100,000 m = 2.0 × 10<sup>−6</sup></p><p><i>f</i> = 2Ω sin 30° = 7.292 × 10<sup>−5</sup> s<sup>−1</sup></p><p><i>v</i><sub>g</sub> = (<i>g</i>/<i>f</i>)∂η/∂x = <strong>0.269 m s<sup>−1</sup> northward</strong></p></div>'
    ]]],
    ['.data-figure figcaption', [
      [
        '<strong>图 1。</strong>E 盘中已有的 NOAA OISST 数据，时间为 2016—2025 年（3,653 个逐日场，0.25° 网格）。区域面积加权平均海温为 28.412 °C，平均锋面强度为每 100 km 0.585 °C。海温锋可以指出表层密度可能快速变化的位置，但海温资料不包含盐度、次表层密度或海表高度，因此不能据此确定绝对地转流。',
        '<strong>Figure 1.</strong> NOAA OISST data already stored on the E: drive, 2016–2025 (3,653 daily fields, 0.25° grid). The area-weighted mean SST is 28.412 °C and the mean front strength is 0.585 °C per 100 km. SST fronts identify locations where surface density may change sharply, but SST alone omits salinity, subsurface density and sea-surface height. It therefore cannot determine an absolute geostrophic current.'
      ],
      [
        '<strong>图 2。</strong>经过质量控制的南海准同步 Argo 断面，包含六个站位，观测时间为 2017 年 3 月 13—16 日。100 dbar 处的站间密度范围为 1.804 kg m<sup>−3</sup>，说明存在水平密度差异。完整的垂向密度场可以约束地转切变，但不规则路径和多日采样需要谨慎处理，而且仍需独立参考才能得到绝对流速。',
        '<strong>Figure 2.</strong> A quality-controlled, quasi-synoptic Argo section across six South China Sea stations, 13–16 March 2017. At 100 dbar, the station density range is 1.804 kg m<sup>−3</sup>, confirming a horizontal density contrast. The full vertical density field can constrain geostrophic shear, but the irregular path and multi-day sampling require care, and an independent reference is still needed for absolute velocity.'
      ]
    ]],
    ['.evidence-cards', [[
      '<article><strong>有用的证据</strong><p>OISST 可定位持续存在的温度锋；Argo 提供次表层温度、盐度、压力和密度。两者结合可改善物理解释。</p></article><article><strong>唯一确定海流所缺少的资料</strong><p>已检查的 E 盘文件没有共位的海表高度或直接流速场。温度资料不能单独排除盐度补偿或非地转流动。</p></article><article><strong>下一步最佳观测</strong><p>加入绝对动力地形以获得表层流，或将水文断面与 ADCP/参考流速配合，以得到绝对流速断面。</p></article>',
      '<article><strong>Useful evidence</strong><p>OISST locates persistent thermal fronts. Argo supplies subsurface temperature, salinity, pressure and density. Together they improve physical interpretation.</p></article><article><strong>Missing for a unique current</strong><p>The E: drive files inspected contain no collocated SSH or direct velocity field. Temperature alone cannot separate salinity compensation or ageostrophic flow.</p></article><article><strong>Best next observation</strong><p>Add mapped absolute dynamic topography for surface flow, or pair the hydrographic section with an ADCP/reference velocity for an absolute section.</p></article>'
    ]]],
    ['.check-grid', [[
      `<div><b>01</b><p><strong>旋转效应占主导。</strong>罗斯贝数 <i>Ro</i> = <i>U</i>/(|<i>f</i>|<i>L</i>) 应远小于 1。</p></div><div><b>02</b><p><strong>远离赤道。</strong>由于 <i>f</i> 趋近于零，普通地转公式会出现奇异，需要使用赤道动力学。</p></div><div><b>03</b><p><strong>摩擦较弱。</strong>该估计最适用于海洋内部，不适用于表层埃克曼层、底边界层和强摩擦近岸区。</p></div><div><b>04</b><p><strong>变化缓慢。</strong>水平加速度应远小于压强梯度项与科氏项；潮汐、惯性振荡、锋面和风生事件可能破坏这一条件。</p></div><div><b>05</b><p><strong>满足静力结构。</strong>压强应能用上覆水体重量良好表示，这通常适用于大尺度海流。</p></div><div><b>06</b><p><strong>采样充分。</strong>站位或卫星图必须能解析水平梯度，并且足够同步，以免把时间变化误判为空间结构。</p></div><div><b>07</b><p><strong>观测经过订正。</strong>卫星测高需要轨道、地球重力场、潮汐和大气订正；水文资料需要温盐压传感器校准、质量控制和 TEOS-10 计算。</p></div><div><b>08</b><p><strong>具有流速参考。</strong>密度断面给出切变或相对海流。若要得到绝对流速，应采用可信参考层、ADCP、浮标位移或其他独立约束。</p></div>`,
      `<div><b>01</b><p><strong>Rotation dominates.</strong> The Rossby number <i>Ro</i> = <i>U</i>/(|<i>f</i>|<i>L</i>) should be much smaller than one.</p></div><div><b>02</b><p><strong>Away from the equator.</strong> Because <i>f</i> approaches zero, ordinary geostrophic formulas become singular and equatorial dynamics must be used.</p></div><div><b>03</b><p><strong>Weak friction.</strong> The estimate is most appropriate in the ocean interior, outside the surface Ekman layer, bottom boundary layer and strongly frictional coastal zones.</p></div><div><b>04</b><p><strong>Slow evolution.</strong> Horizontal acceleration should be small relative to pressure-gradient and Coriolis terms; tides, inertial oscillations, fronts and wind-driven events may violate this.</p></div><div><b>05</b><p><strong>Hydrostatic structure.</strong> Pressure should be well represented by the weight of the overlying water, as is typical for large-scale ocean flow.</p></div><div><b>06</b><p><strong>Adequate sampling.</strong> Stations or satellite maps must resolve the horizontal gradient and be sufficiently simultaneous that temporal change is not mistaken for spatial structure.</p></div><div><b>07</b><p><strong>Corrected observations.</strong> Altimetry needs orbit, geoid, tide and atmospheric corrections; hydrography needs calibrated T–S–p sensors, quality control and TEOS-10 calculations.</p></div><div><b>08</b><p><strong>A velocity reference.</strong> Density sections yield shear or relative current. Use a credible reference level, ADCP, float displacement or another independent constraint for absolute velocity.</p></div>`
    ]]],
    ['#model-answer p', [
      [
        '海洋温度可由 CTD、XBT、Argo 浮标、滑翔机和潜标上的热敏电阻进行现场测量，也可通过红外或微波卫星辐射计进行遥感。现场传感器能准确解析垂向结构，但时空覆盖有限；卫星能重复绘制大范围图像，却只能观测海洋皮肤层或近表层，而且需要大气订正和校准。盐度通常由 CTD 测得的电导率、温度和压力换算得到。用盐度计分析的采水瓶样本可提供高质量核验，Argo 则能将温盐剖面扩展到开阔海域。卫星 L 波段辐射计可以绘制全球表层盐度，但在近岸、降雨、海冰和低温水域的分辨率与精度会下降。海流可由流速计、ADCP、表层漂流浮标、次表层浮标和岸基高频雷达直接测量。这些方法分别提供时间序列、垂向剖面、轨迹或表层图像，但没有一种方法能同时覆盖全部深度和尺度；平台运动、声学量程、风曳和地理覆盖是常见限制。',
        'Ocean temperature is measured in situ by thermistors on CTDs, XBTs, Argo floats, gliders and moorings, and remotely by infrared or microwave satellite radiometers. In situ sensors resolve the vertical structure accurately but provide limited spatial or temporal coverage, whereas satellites repeatedly map large areas but observe only the skin or near-surface ocean and require atmospheric correction and calibration. Salinity is usually derived from conductivity, temperature and pressure measured by a CTD. Bottle samples analyzed with a salinometer provide high-quality checks, and Argo extends T–S profiling over the open ocean. Satellite L-band radiometry maps surface salinity globally, but its resolution and accuracy decline near coasts, rain, ice and cold water. Currents are measured directly by current meters, ADCPs, surface drifters, subsurface floats and coastal HF radar. These methods provide either time series, vertical profiles, trajectories or surface maps, but none samples all depths and scales; platform motion, acoustic range, windage and geographic coverage are common limitations.'
      ],
      [
        '对于远离强摩擦区的大尺度缓慢运动，水平压强梯度力与科氏力近似平衡：<i>f</i><b>k</b> × <b>u</b><sub>g</sub> = −ρ<sub>0</sub><sup>−1</sup>∇<sub>h</sub><i>p</i>。海表高度坡度对应 <i>u</i><sub>g</sub> = −(<i>g</i>/<i>f</i>)∂η/∂<i>y</i> 和 <i>v</i><sub>g</sub> = (<i>g</i>/<i>f</i>)∂η/∂<i>x</i>。因此，海流沿海表等高度线流动；在北半球，较高海面位于流向右侧。水平方向的温度和盐度差异会改变密度；在静力平衡下，这些密度差异使水平压强梯度随深度变化。因此，热成风平衡把水平密度梯度与地转流的垂向切变联系起来。',
        'For large-scale, slowly varying motion away from strong friction, the horizontal pressure-gradient force approximately balances the Coriolis force: <i>f</i><b>k</b> × <b>u</b><sub>g</sub> = −ρ<sub>0</sub><sup>−1</sup>∇<sub>h</sub><i>p</i>. At the sea surface, a height slope gives <i>u</i><sub>g</sub> = −(<i>g</i>/<i>f</i>)∂η/∂<i>y</i> and <i>v</i><sub>g</sub> = (<i>g</i>/<i>f</i>)∂η/∂<i>x</i>. Thus the current is parallel to sea-surface-height contours, with higher sea level on its right in the Northern Hemisphere. Horizontal temperature and salinity differences change density; under hydrostatic balance, these density contrasts make the horizontal pressure gradient vary with depth. Thermal-wind balance therefore relates horizontal density gradients to vertical geostrophic shear.'
      ],
      [
        '卫星测高可从绝对动力地形的梯度反演表层地转流速。CTD 或 Argo 断面能够计算动力高度差，以及相对于参考压力面的地转流速。只有给出无运动层或独立流速观测后，后者才能转化为绝对流速。两种方法都要求准确订正、足够空间分辨率和近同步采样。它们最适用于罗斯贝数较小、远离赤道和强边界摩擦、满足静力平衡的流动，同时需要滤除或单独处理潮汐、惯性运动、埃克曼流和其他非地转分量。',
        'Satellite altimetry can infer surface geostrophic velocity from gradients of absolute dynamic topography. CTD or Argo sections can infer dynamic-height differences and geostrophic velocity relative to a reference pressure. The latter becomes absolute only when a level of no motion or an independent velocity measurement is supplied. Both approaches require accurate corrections, sufficient spatial resolution and near-synoptic sampling. They work best when the Rossby number is small, the flow is away from the equator and strong boundary friction, hydrostatic balance is appropriate, and tides, inertial motion, Ekman flow and other ageostrophic components have been filtered or treated separately.'
      ]
    ]],
    ['#check ul', [[
      '<li><strong>物理关系：</strong>矢量方程和分量方程在北半球采用正科氏参数，所述方向与公式符号一致。</li><li><strong>数值检验：</strong>30°N 处 100 km 范围内 0.20 m 的海面高度差对应 0.269 m s<sup>−1</sup>；该结果已在 MATLAB 中独立计算。</li><li><strong>密度证据：</strong>六个实际 Argo 站位在 100 dbar 处的密度为 1023.522–1025.325 kg m<sup>−3</sup>，范围为 1.804 kg m<sup>−3</sup>。</li><li><strong>解释边界：</strong>SST 被用作示踪量和密度的部分控制因素，没有把它当作完整温盐密度、海表高度或流速的替代物。</li><li><strong>反演范围：</strong>在没有参考流速时，密度资料只用于估算切变或相对流速；卫星测高若要得到绝对表层流，需要绝对动力地形。</li>',
      '<li><strong>Physics:</strong> the vector and component equations use a positive Coriolis parameter in the Northern Hemisphere; the stated direction follows their signs.</li><li><strong>Numerics:</strong> 0.20 m over 100 km at 30°N gives 0.269 m s<sup>−1</sup>; the calculation was independently evaluated in MATLAB.</li><li><strong>Density evidence:</strong> six actual Argo station samples at 100 dbar give 1023.522–1025.325 kg m<sup>−3</sup>, a range of 1.804 kg m<sup>−3</sup>.</li><li><strong>Interpretation:</strong> SST is treated as a tracer and partial density control, never as a complete substitute for T–S density, SSH or velocity.</li><li><strong>Inference:</strong> density data are described as providing shear/relative velocity unless a reference is supplied; altimetry requires absolute dynamic topography for absolute surface current.</li>'
    ]]],
    ['.source-list small', [
      ['CTD 原理：电导率、温度、深度与盐度换算。', 'What is a CTD? Conductivity, temperature, depth and salinity conversion.'],
      ['利用声学多普勒流速剖面仪测量海流。', 'Measuring ocean currents with an Acoustic Doppler Current Profiler.'],
      ['全球资料汇集中心与剖面资料获取。', 'Global Data Assembly Centres and profile data access.'],
      ['用于海水热力学计算的 GSW 软件。', 'GSW software for seawater thermodynamic calculations.'],
      ['海表高度和表层地转流变量。', 'Sea-surface height and surface geostrophic current variables.'],
      ['高频雷达表层流观测网。', 'High-frequency radar surface-current observing network.'],
      ['图 1 使用的逐日 0.25° 海表温度分析。', 'Daily 0.25° sea-surface-temperature analysis used for Figure 1.'],
      ['图 2 使用的 Argo 剖面数据集。', 'Argo profile dataset used for Figure 2.']
    ]],
    ['.data-note', [[
      '本地数据来源：OISST 文件读取自 <code>E:\\研究生课题\\data\\OISST_ERA5_1996_2025\\OISST</code>。相关 Argo 图件和摘要保存在本站可复现的资料集合中。数值仅在展示时进行了四舍五入。',
      'Local data provenance: OISST files were read from <code>E:\\研究生课题\\data\\OISST_ERA5_1996_2025\\OISST</code>. The accompanying Argo figures and summaries are retained in this site’s reproducible asset collection. Values are rounded only for presentation.'
    ]]],
    ['footer span', [
      ['≈ &nbsp; 海洋课堂笔记', '≈ &nbsp; Ocean Classroom Notes'],
      ['test2 · 海洋观测与地转流', 'test2 · Measurements and Geostrophic Currents']
    ]],
    ['footer a', [['返回资料库', 'Back to Library']]]
  ];

  const bindings = [];
  for (const [selector, copies] of groups) {
    const nodes = [...document.querySelectorAll(selector)];
    copies.forEach((copy, index) => {
      if (nodes[index]) bindings.push({node: nodes[index], zh: copy[0], en: copy[1]});
    });
  }

  const attributes = [
    [document.querySelector('.identity'), 'aria-label', '海洋课堂笔记首页', 'Ocean Classroom Notes home'],
    [document.querySelector('.site-header nav'), 'aria-label', '主导航', 'Primary navigation'],
    [document.querySelector('.question-card'), 'aria-label', '课程作业题目', 'Assignment question'],
    [document.querySelector('.t2-toc'), 'aria-label', '页面目录', 'Page contents'],
    [document.querySelector('meta[name="description"]'), 'content', '海洋温盐流观测方法、优缺点、地转平衡及观测反演条件的分层课程答案。', 'A layered answer on instruments for measuring ocean temperature, salinity and currents, and on inferring geostrophic currents from density or sea-surface-height observations.'],
    [document.querySelector('meta[property="og:title"]'), 'content', 'test2｜海洋观测与地转流反演', 'test2 | Ocean Measurements and Geostrophic Currents'],
    [document.querySelector('meta[property="og:description"]'), 'content', '观测方法、优缺点、地转方程、反演条件、数值示例和南海数据证据。', 'Measurement methods, advantages and limitations, geostrophic equations, observational conditions, a worked example and South China Sea data evidence.']
  ];

  function apply(language = window.siteI18n?.language || 'zh') {
    for (const binding of bindings) {
      const value = language === 'zh' ? binding.zh : binding.en;
      if (binding.node.innerHTML !== value) binding.node.innerHTML = value;
    }
    for (const [node, name, zh, en] of attributes) {
      if (node) node.setAttribute(name, language === 'zh' ? zh : en);
    }
  }

  apply();
  window.addEventListener('site-language-change', event => apply(event.detail.language));
})();
