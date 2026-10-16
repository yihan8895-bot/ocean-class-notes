/* Complete bilingual copy for test1; follows the site-wide language state. */
(() => {
  'use strict';

  const groups = [
    ['.test1-back', [['← 返回海洋课堂笔记', '← Back to Ocean Classroom Notes']]],
    ['.test1-label', [['课程作答 · 三个层次', 'COURSE ANSWER · THREE LEVELS']]],
    ['.test1-hero h1', [['<em>test1</em>物理海洋学、上层海洋层结与对流混合', '<em>test1</em>Physical Oceanography, Upper-Ocean Stratification, and Convective Mixing']]],
    ['.test1-hero-copy > p', [['用简要答案、结构化课程解释和本地 NOAA OISST 定量案例，分三个层次回答问题。', 'A concise answer, a structured course explanation, and a quantitative extension with a local NOAA OISST example.']]],
    ['.test1-meta span', [
      ['<strong>3</strong> 个作答层次', '<strong>3</strong> answer levels'],
      ['<strong>2</strong> 幅已核验图', '<strong>2</strong> checked figures'],
      ['<strong>1982–2020</strong> 本地海温背景', '<strong>1982–2020</strong> local SST context']
    ]],
    ['#question-title', [['题目', 'THE QUESTION']]],
    ['.test1-question p', [['简述物理海洋学研究的主要内容。说明上层海洋典型的垂向层结，以及海水温度、盐度与密度之间的关系。为什么表层冷却或表层盐度升高会触发垂向对流？请从密度变化和层结稳定性的角度解释。', 'Briefly describe the main topics studied in physical oceanography. Explain the typical vertical stratification of the upper ocean in terms of the relationship among seawater temperature, salinity, and density. Why can surface cooling or an increase in surface salinity trigger vertical convection? Explain in terms of density changes and stratification stability.']]],
    ['.test1-toc > span', [['本页目录', 'ON THIS PAGE']]],
    ['.test1-toc a', [
      ['答案导图', 'Answer map'], ['层次 1 · 简答', 'Level 1 · concise'], ['层次 2 · 结构化解释', 'Level 2 · structured'],
      ['层次 3 · 定量拓展', 'Level 3 · quantitative'], ['综合答案', 'Integrated answer'], ['自检', 'Self-check'], ['参考文献', 'References']
    ]],
    ['#overview .test1-heading small', [['答案导图', 'ANSWER MAP']]],
    ['#overview .test1-heading h2', [['选择适合作业要求的回答深度', 'Choose the depth that fits the assignment']]],
    ['.level-grid b', [['层次 1', 'Level 1'], ['层次 2', 'Level 2'], ['层次 3', 'Level 3']]],
    ['.level-grid strong', [['简短回答', 'Short response'], ['课程作业', 'Course assignment'], ['进阶拓展', 'Advanced extension']]],
    ['.level-grid span', [
      ['约 180 个英文单词，或一分钟口头回答。', 'About 180 words or a one-minute oral answer.'],
      ['按“主题—层结—对流”的清晰顺序展开。', 'Topics, stratification, and convection in a clear sequence.'],
      ['加入密度方程、稳定性判据、数值和数据背景。', 'Density equation, stability criterion, numbers, and data context.']
    ]],
    ['#level-1 .test1-heading small', [['层次 1', 'LEVEL 1']]],
    ['#level-1 .test1-heading h2', [['简要答案', 'Concise answer']]],
    ['#level-1 .answer-box p', [
      ['物理海洋学研究海洋的物理状态与运动。主要内容包括海水物理性质、海气热量与淡水交换、波浪与潮汐、风生环流和热盐环流、湍流与混合，以及海洋在气候系统中的作用。', 'Physical oceanography studies the physical state and motion of the ocean. Its main topics include seawater properties, air-sea exchanges of heat and freshwater, waves and tides, wind-driven and thermohaline circulation, turbulence and mixing, and the role of the ocean in climate.'],
      ['上层海洋通常由近似均匀的表层混合层和下方的温跃层组成，温度在温跃层中随深度迅速降低。盐度也可能在盐跃层中变化。温度和盐度共同控制海水密度：升温通常降低密度，冷却和盐度升高则增大密度。二者共同作用，通常形成密度随深度增大的密跃层。轻水位于重水之上，因此层结稳定。', 'The upper ocean commonly consists of a well-mixed surface layer overlying a thermocline, where temperature decreases rapidly with depth. Salinity may also change through a halocline. Temperature and salinity jointly control seawater density: warming usually lowers density, whereas cooling and increasing salinity raise it. Their combined effect usually produces a pycnocline in which density increases downward. This arrangement is stable because light water lies above dense water.'],
      ['表层冷却会增大表层海水密度。蒸发或海冰形成时的盐析也会提高表层盐度和密度。如果表层水比下层水更密，密度梯度会反转，层结变得重力不稳定。密水下沉、轻水上升，从而产生垂向对流并混合热量与盐分，直到密度反转消失，重新形成稳定或近似均匀的混合层。', 'Surface cooling increases the density of surface water. Evaporation or brine rejection during sea-ice formation can also raise surface salinity and density. If surface water becomes denser than the water below, the density gradient is reversed and the stratification becomes gravitationally unstable. Dense water then sinks while lighter water rises. This overturning causes vertical convection and mixes heat and salt until the density inversion is removed and a stable or nearly uniform mixed layer is restored.']
    ]],
    ['#level-2 .test1-heading small', [['层次 2', 'LEVEL 2']]],
    ['#level-2 .test1-heading h2', [['结构化解释', 'Structured explanation']]],
    ['#level-2 > h3', [
      ['物理海洋学的主要内容', 'Main topics in physical oceanography'],
      ['典型上层海洋结构', 'Typical upper-ocean structure'],
      ['为什么冷却和盐化会引起对流', 'Why cooling and salinification cause convection']
    ]],
    ['#level-2 > p', [
      ['物理海洋学解释海洋如何储存和输送热量、淡水、盐分、动量与机械能。该学科通常包括：', 'Physical oceanography explains how the ocean stores and transports heat, freshwater, salt, momentum, and mechanical energy. The field commonly includes:'],
      ['上层海洋常分为表层混合层、过渡层和深层水。风搅拌、波浪和浮力湍流使混合层内的温度和盐度较均匀。混合层下方的温度常在季节性或永久性<strong>温跃层</strong>中迅速下降。盐度则可能在<strong>盐跃层</strong>中升高或降低，取决于蒸发、降水、河流、海冰过程和水团。', 'The upper ocean is often divided into a surface mixed layer, a transition zone, and deeper water. Wind stirring, waves, and buoyancy-driven turbulence keep the mixed layer relatively uniform in temperature and salinity. Below it, temperature often falls rapidly through a seasonal or permanent <strong>thermocline</strong>. Salinity may increase or decrease through a <strong>halocline</strong>, depending on evaporation, precipitation, rivers, ice processes, and water masses.'],
      ['温度和盐度共同决定密度。在通常的海洋条件下，温度降低和盐度升高都会使海水变密。在许多低纬和中纬海区，温度随深度降低的作用占主导，形成密度向下增大的<strong>密跃层</strong>。轻水位于密水之上时层结稳定，因为受到垂向扰动的水团会受到恢复浮力。', 'Temperature and salinity act together to set density. Under ordinary ocean conditions, lower temperature and higher salinity both make seawater denser. In many low- and mid-latitude regions, the temperature decrease with depth dominates, producing a <strong>pycnocline</strong> in which density increases downward. Light water above dense water is stable because a vertically displaced parcel experiences a restoring buoyancy force.']
    ]],
    ['.topic-grid h4', [
      ['海水物理性质', 'Seawater properties'], ['海气相互作用', 'Air-sea interaction'], ['海洋环流', 'Ocean circulation'],
      ['波浪与潮汐', 'Waves and tides'], ['湍流与混合', 'Turbulence and mixing'], ['海洋与气候', 'Ocean and climate']
    ]],
    ['.topic-grid p', [
      ['温度、盐度、压力、密度及其三维分布。', 'Temperature, salinity, pressure, density, and their three-dimensional distributions.'],
      ['大气与海洋之间的热量、淡水、气体和动量交换。', 'Exchanges of heat, freshwater, gases, and momentum between atmosphere and ocean.'],
      ['风生环流、边界流、上升流、涡旋和翻转环流。', 'Wind-driven gyres, boundary currents, upwelling, eddies, and overturning circulation.'],
      ['表面波与内波、潮汐运动、能量传播和耗散。', 'Surface and internal waves, tidal motion, energy propagation, and dissipation.'],
      ['重新分配热量、盐分、动量、营养盐和溶解气体的过程。', 'Processes that redistribute heat, salt, momentum, nutrients, and dissolved gases.'],
      ['水团形成、极地与近岸过程、气候模态和长期变化。', 'Water-mass formation, polar and coastal processes, climate modes, and long-term change.']
    ]],
    ['#level-2 figcaption', [['<b>图 1。</b>上层海洋层结和对流概念图。稳定状态下，混合层覆盖在温跃层或密跃层之上。冷却或盐化会增大表层密度；当表层比下层更密时，密水下沉并形成对流环流，使上层海洋发生混合。图中层厚与箭头均为示意。', '<b>Figure 1.</b> Conceptual upper-ocean stratification and convection. A mixed layer overlies a thermocline or pycnocline in the stable case. Cooling or salinification raises surface density; if the surface becomes denser than the water below, dense water sinks and a convective circulation mixes the upper ocean. Layer thicknesses and arrows are schematic.']]],
    ['.relationship-strip span', [['冷却', 'COOLING'], ['盐化', 'SALINIFICATION'], ['稳定海洋', 'STABLE OCEAN']]],
    ['.relationship-strip strong', [['T ↓ → ρ ↑', 'T ↓ → ρ ↑'], ['S ↑ → ρ ↑', 'S ↑ → ρ ↑'], ['ρ 随深度增大', 'ρ increases downward']]],
    ['.process-list b', [
      ['初始层结稳定', 'Stable starting state'], ['表层密度增大', 'Surface density rises'], ['可能形成密度反转', 'A density inversion may form'],
      ['对流翻转开始', 'Convective overturning begins'], ['恢复稳定', 'Stability is restored']
    ]],
    ['.process-list p', [
      ['较轻的表层水位于密度更大的下层水之上。', 'Relatively light surface water lies above denser water.'],
      ['冷却使海水收缩；蒸发移除淡水，海冰形成排出盐分，这些过程都可能增大表层密度。', 'Cooling contracts the water. Evaporation removes freshwater, and sea-ice formation rejects brine. Each process can raise surface density.'],
      ['如果表层水比紧邻下方的海水更密，原先稳定的密度排列便会反转。', 'If the surface becomes denser than the water immediately below, the original stable ordering is reversed.'],
      ['密的表层水下沉、较轻的水上升，从而垂向输送热量和盐分。', 'Dense surface water sinks and lighter water rises, vertically transporting heat and salt.'],
      ['混合持续到密度反转消失，留下更深、近似均匀的混合层，或恢复密度向下增大的状态。', 'Mixing continues until the inversion disappears, leaving a deeper, nearly uniform mixed layer or density increasing downward again.']
    ]],
    ['.caveat', [['<b>综合控制：</b>降雨、河流输入或融冰会淡化并减轻表层水，即使发生冷却，也可能维持稳定层结。对流取决于温度和盐度对密度的共同作用。', '<b>Combined control:</b> rainfall, river discharge, or melting ice can freshen and lighten the surface, preserving stable stratification even during cooling. Convection depends on the combined temperature and salinity effects on density.']]],
    ['#level-3 .test1-heading small', [['层次 3', 'LEVEL 3']]],
    ['#level-3 .test1-heading h2', [['定量解释与数据背景', 'Quantitative explanation and data context']]],
    ['#level-3 > h3', [
      ['密度响应', 'Density response'], ['静力稳定性', 'Static stability'], ['示例数值检验', 'Illustrative numerical check'], ['本地 NOAA OISST 数据背景', 'Local NOAA OISST context']
    ]],
    ['#level-3 > p', [
      ['在压力不变且变化幅度较小时，海水状态方程可线性化为：', 'For modest changes at fixed pressure, the seawater equation of state can be linearized as:'],
      ['其中 α 为热膨胀系数，β 为盐收缩系数。在通常海洋条件下二者均为正。因此，冷却时 ΔT &lt; 0，会得到 Δρ &gt; 0；盐度升高时 ΔS &gt; 0，同样得到 Δρ &gt; 0。', 'Here α is the thermal expansion coefficient and β is the saline contraction coefficient. Both are positive under normal ocean conditions. Therefore cooling, ΔT &lt; 0, gives Δρ &gt; 0; increasing salinity, ΔS &gt; 0, also gives Δρ &gt; 0.'],
      ['当垂向坐标 <i>z</i> 向上为正时，浮力频率为：', 'For a vertical coordinate <i>z</i> that increases upward, the buoyancy frequency is:'],
      ['精确分析中，海洋学家使用位密度或相关的压力校正变量，因为原位密度还会因压力压缩而增大。', 'In precise analysis, oceanographers use potential density or a related pressure-corrected variable because in-situ density also increases through compression with pressure.'],
      ['现有本地数据是 NOAA OISST 在南海北部的 1982—2020 年子集，包含 5 × 7 网格上的逐日海表温度。下图的月气候态采用纬度余弦面积权重，并使用有效观测，没有填补占网格—时间组合 2.86% 的缺测值。', 'The available local dataset is a northern South China Sea subset of NOAA OISST for 1982–2020. It contains daily sea-surface temperature on a 5 × 7 grid. The monthly climatology below uses cosine-of-latitude area weights and valid observations without filling the missing 2.86% of grid-time entries.']
    ]],
    ['.stability-grid span', [['稳定', 'STABLE'], ['不稳定', 'UNSTABLE']]],
    ['.stability-grid strong', [['dρ/dz &lt; 0', 'dρ/dz &lt; 0'], ['密度反转', 'density inversion']]],
    ['.stability-grid p', [
      ['密度向上减小；受到扰动的水团会受到恢复力。', 'Density decreases upward; displaced parcels feel a restoring force.'],
      ['密水位于轻水之上；随后会发生对流翻转。', 'Dense water overlies lighter water; convective overturning follows.']
    ]],
    ['.small-note', [['精确分析中，海洋学家使用位密度或相关的压力校正变量，因为原位密度还会因压力压缩而增大。', 'In precise analysis, oceanographers use potential density or a related pressure-corrected variable because in-situ density also increases through compression with pressure.']]],
    ['.table-wrap th', [['水样', 'Water sample'], ['温度', 'Temperature'], ['实用盐度', 'Practical salinity'], ['密度', 'Density'], ['解释', 'Interpretation']]],
    ['.table-wrap tbody td:first-child', [
      ['初始表层水', 'Initial surface'], ['示例 50 m 海水', 'Illustrative 50 m water'], ['冷却后的表层水', 'Cooled surface'], ['盐化后的表层水', 'Salinified surface']
    ]],
    ['.table-wrap tbody td:last-child', [
      ['比 50 m 海水轻', 'Lighter than 50 m water'], ['初始位于较轻表层水下方', 'Initially below lighter water'],
      ['比 50 m 海水密', 'Denser than 50 m water'], ['比 50 m 海水密', 'Denser than 50 m water']
    ]],
    ['#level-3 figcaption', [['<b>图 2。</b>18.125–22.125°N、112.125–118.125°E 的月平均海表温度气候态。面积加权平均值从 2 月的 22.48 °C 上升至 7 月的 28.92 °C，随后降至 12 月的 23.95 °C。阴影表示各月逐日数值的 ±1 个标准差，代表变率，而不是均值的不确定性。', '<b>Figure 2.</b> Monthly sea-surface temperature climatology for 18.125–22.125°N, 112.125–118.125°E. The area-weighted mean rises from 22.48 °C in February to 28.92 °C in July, then falls to 23.95 °C in December. The shaded band is ±1 standard deviation of daily values within each month; it represents variability rather than uncertainty in the mean.']]],
    ['.data-boundary', [['<b>数据能够说明：</b>从夏末到冬季存在明显的表层降温阶段，这一过程倾向于增大表层密度并削弱层结。<br><b>数据不能说明：</b>OISST 不包含盐度剖面或次表层温度，不能单独证明发生了对流。确认对流需要垂向温盐剖面，以计算位密度、混合层深度和 N²。', '<b>What the dataset can show:</b> a strong seasonal surface-cooling phase from late summer into winter, which tends to increase surface density and weaken stratification.<br><b>What it cannot show:</b> OISST has no salinity profile or subsurface temperature. It cannot by itself demonstrate that convection occurred. That requires vertical temperature and salinity profiles to calculate potential density, mixed-layer depth, and N².']]],
    ['#integrated .test1-heading small', [['提交版本', 'SUBMISSION VERSION']]],
    ['#integrated .test1-heading h2', [['综合课程答案', 'Integrated course answer']]],
    ['#integrated .answer-box p', [
      ['物理海洋学研究海洋的物理性质与运动，以及控制这些性质和运动的过程。主要内容包括温度、盐度与密度；海气之间的热量、淡水和动量交换；波浪与潮汐；风生环流与密度驱动环流；涡旋、湍流与混合；以及海洋在气候系统中的作用。', 'Physical oceanography examines the physical properties and motion of the ocean and the processes that control them. Its main subjects include temperature, salinity and density; air-sea exchanges of heat, freshwater and momentum; waves and tides; wind-driven and density-driven circulation; eddies, turbulence and mixing; and the ocean\'s role in climate.'],
      ['上层海洋通常包含一个表层混合层，风和波浪使其中的温度与盐度近似均匀。其下是过渡层，通常包含温度随深度迅速下降的温跃层，有时还包含盐度快速变化的盐跃层。温度和盐度共同决定密度。冷却通常会增大海水密度，盐度升高也会增大密度。二者共同作用，通常形成密度向下增大的密跃层。轻水位于密水之上时，层结在重力作用下稳定，因为受到扰动的水团会受到恢复浮力。', 'The upper ocean commonly contains a surface mixed layer in which wind and waves keep temperature and salinity nearly uniform. Beneath it lies a transition zone that often includes a thermocline, where temperature decreases rapidly with depth, and sometimes a halocline, where salinity changes rapidly. Temperature and salinity together determine density. Cooling generally increases seawater density, and increasing salinity also increases density. Their combined effect usually creates a pycnocline with density increasing downward. Light water over dense water is gravitationally stable because a displaced parcel experiences a restoring buoyancy force.'],
      ['表层冷却会侵蚀这种稳定性。海面失热后，表层密度上升。蒸发或海冰形成时的盐析也能提高表层盐度和密度。如果表层水仍比下层水轻，水柱保持稳定，但混合层可能加深。如果表层水变得比下层水更密，就会形成密度反转。密的表层水下沉、较轻的水上升，产生垂向对流。翻转过程垂向输送热量和盐分，并持续到不稳定的密度梯度消失。最终通常形成更深、更均匀的混合层，密度保持近似均匀或重新随深度增大。', 'Surface cooling can erode this stability. As the surface loses heat, its density rises. Surface salinity can increase through evaporation or brine rejection when sea ice forms, which also increases density. If the surface remains lighter than the water below, the water column stays stable, although the mixed layer may deepen. If the surface becomes denser than the underlying water, a density inversion forms. Dense surface water sinks and lighter water rises, causing vertical convection. This overturning transports heat and salt vertically and continues until the unstable density gradient is removed. The final state is usually a deeper, more uniform mixed layer with density that is constant or increases with depth.'],
      ['关键在于，对流响应的是密度，而不是分别响应温度或盐度。冷却与盐化都会使表层海水变密，因此有利于对流；降雨、河流输入或融冰则会降低表层盐度并增强稳定性。完整判断需要同时获得温度和盐度剖面，并使用位密度去除压力压缩的直接影响。', 'The key point is that convection responds to density rather than to temperature or salinity separately. Cooling and salinification favor convection because both make surface water denser, whereas rainfall, river discharge, or ice melt can lower surface salinity and stabilize the water column. A complete assessment therefore requires both temperature and salinity profiles and should use potential density to remove the direct compression effect of pressure.']
    ]],
    ['#self-check .test1-heading small', [['质量控制', 'QUALITY CONTROL']]],
    ['#self-check .test1-heading h2', [['自检', 'Self-check']]],
    ['.check-list b', [
      ['问题覆盖', 'Question coverage'], ['作用方向', 'Direction of effects'], ['稳定性符号', 'Stability sign'], ['压力注意事项', 'Pressure caveat'],
      ['区域适用范围', 'Regional caveat'], ['数据限制', 'Data limitation'], ['数值检验', 'Numerical check']
    ]],
    ['.check-list span', [
      ['已覆盖主要主题、上层海洋分层、温盐密关系与对流。', 'Main topics, upper-ocean layers, T–S–density relations, and convection are all addressed.'],
      ['冷却增密；盐化增密；稳定层结中密度通常向下增大。', 'Cooling increases density; salinification increases density; stable density usually increases downward.'],
      ['当 z 向上为正，稳定层结满足 dρ/dz &lt; 0、N² &gt; 0；密度反转满足 N² &lt; 0。', 'With z positive upward, stable stratification has dρ/dz &lt; 0 and N² &gt; 0; an inversion has N² &lt; 0.'],
      ['已区分位密度与未经压力校正的原位密度。', 'Potential density is distinguished from raw in-situ density.'],
      ['温跃层占主导的剖面被说明为许多低纬和中纬海区的典型情况，而非全球普遍状态。', 'The thermocline-dominated profile is presented as typical of many low- and mid-latitude regions, not universal.'],
      ['OISST 仅用于说明表层温度背景，没有作为观测到对流的证据。', 'OISST is used for surface-temperature context, not as evidence of observed convection.'],
      ['两种示例表层扰动都使海水密度超过所选下层水。', 'Both illustrative surface perturbations produce water denser than the selected underlying layer.']
    ]],
    ['#references .test1-heading small', [['资料来源', 'SOURCES']]],
    ['#references .test1-heading h2', [['参考文献', 'References']]],
    ['footer span', [['test1 · 物理海洋学课程作答', 'test1 · Physical Oceanography Course Answer']]],
    ['footer a', [['海洋课堂笔记 ↗', 'Ocean Classroom Notes ↗']]]
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
    [document.querySelector('.test1-meta'), 'aria-label', '文档摘要', 'Document summary'],
    [document.querySelector('.test1-toc'), 'aria-label', '页面目录', 'Page contents'],
    [document.querySelector('.relationship-strip'), 'aria-label', '温度、盐度与密度关系', 'Temperature salinity density relationships']
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
