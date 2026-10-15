(() => {
  'use strict';
  const $ = selector => document.querySelector(selector);
  const $$ = selector => [...document.querySelectorAll(selector)];
  const clamp = (value, min, max) => Math.max(min, Math.min(max, value));
  const stages = [
    {title:'建立水平压强梯度 / A Horizontal Pressure Gradient Forms',text:'海面高度差产生水平压强差；静止水团尚无科氏力。 / A sea-level difference creates a horizontal pressure contrast; a stationary parcel has no Coriolis force yet.'},
    {title:'水团向低压侧加速 / Water Accelerates Toward Lower Pressure',text:'压强梯度力先使水团向东运动。速度出现后，科氏力才开始产生。 / The pressure-gradient force first accelerates the parcel eastward. Coriolis force appears only after velocity develops.'},
    {title:'科氏力使流向转弯 / Coriolis Force Turns the Current',text:'在北半球，运动水团向其右侧偏转；南半球则向左。随着速度增大，科氏力也增强。 / Moving water turns to its right in the Northern Hemisphere and to its left in the Southern Hemisphere. Coriolis force strengthens as speed increases.'},
    {title:'两力近似平衡 / The Two Forces Nearly Balance',text:'科氏力与压强梯度力近似等大反向，水流主要沿等海面高度线前进。 / Coriolis and pressure-gradient forces become nearly equal and opposite, so the current runs mainly along sea-surface-height contours.'}
  ];
  const latitude = $('#latitude');
  const slope = $('#slope');
  const progress = $('#formation-progress');
  const parcel = $('#water-parcel');
  const parcelLabel = $('#parcel-label');
  const trail = $('#parcel-trail');
  const pressure = $('#pressure-vector');
  const coriolis = $('#coriolis-vector');
  const velocity = $('#velocity-vector');
  const playButton = $('#play-formation');
  let playing = false;
  let timer = 0;
  let lastTime = 0;

  function latitudeText(value) {
    if (value === 0) return '0° / Equator';
    return `${Math.abs(value)}°${value > 0 ? 'N' : 'S'}`;
  }

  function updateParameters() {
    const lat = Number(latitude.value);
    const riseCm = Number(slope.value);
    const f = 2 * 7.292115e-5 * Math.sin(lat * Math.PI / 180);
    const gradient = riseCm * .01 / 100000;
    const nearEquator = Math.abs(lat) < 5;
    $('#latitude-output').textContent = latitudeText(lat);
    $('#slope-output').textContent = `${riseCm} cm / 100 km`;
    const superscript = value => String(value).replace(/-/g,'⁻').replace(/0/g,'⁰').replace(/1/g,'¹').replace(/2/g,'²').replace(/3/g,'³').replace(/4/g,'⁴').replace(/5/g,'⁵').replace(/6/g,'⁶').replace(/7/g,'⁷').replace(/8/g,'⁸').replace(/9/g,'⁹');
    const exponent = nearEquator ? 0 : Math.floor(Math.log10(Math.abs(f)));
    const mantissa = nearEquator ? 0 : Math.abs(f) / (10 ** exponent);
    $('#f-readout').textContent = nearEquator ? '0 — 公式不适用 / formula not valid' : `${mantissa.toFixed(2)} × 10${superscript(exponent)} s⁻¹`;
    $('#speed-readout').textContent = nearEquator ? '—' : `${(9.81 * gradient / Math.abs(f)).toFixed(3)} m s⁻¹`;
    $('#direction-readout').textContent = nearEquator ? '无法由本公式确定 / Not determined here' : lat > 0 ? '向南 / Southward' : '向北 / Northward';
    $('#equator-warning').hidden = !nearEquator;
    render(Number(progress.value));
  }

  function pointAt(p) {
    const lat = Number(latitude.value);
    if (Math.abs(lat) < 5) return {x:300+clamp((p-25)/75,0,1)*250,y:220};
    const turn = lat >= 0 ? 1 : -1;
    if (p < 25) return {x:300,y:220};
    if (p < 48) {
      const q=(p-25)/23;
      return {x:300+105*q,y:220};
    }
    if (p < 76) {
      const q=(p-48)/28;
      const one=1-q;
      return {x:one*one*405+2*one*q*455+q*q*370,y:one*one*220+2*one*q*(220+turn*58)+q*q*(220+turn*112)};
    }
    const q=(p-76)/24;
    return {x:370,y:220+turn*(112+72*q)};
  }

  function transformVector(element, x, y, rotation, scale=1) {
    element.setAttribute('transform',`translate(${x} ${y}) rotate(${rotation}) scale(${scale})`);
  }

  function render(value) {
    const p = clamp(value,0,100);
    const pos = pointAt(p);
    const lat = Number(latitude.value);
    const nearEquator = Math.abs(lat) < 5;
    const turn = lat >= 0 ? 1 : -1;
    parcel.setAttribute('cx',pos.x); parcel.setAttribute('cy',pos.y);
    parcelLabel.setAttribute('x',pos.x+18); parcelLabel.setAttribute('y',pos.y-12);
    const samples=[];
    for(let n=0;n<=p;n+=3){const q=pointAt(n);samples.push(`${q.x.toFixed(1)},${q.y.toFixed(1)}`)}
    samples.push(`${pos.x.toFixed(1)},${pos.y.toFixed(1)}`);
    trail.setAttribute('points',samples.join(' '));
    const forceGrowth=clamp((p-28)/50,0,1);
    const speedGrowth=clamp((p-25)/48,0,1);
    transformVector(pressure,pos.x,pos.y,0,1);
    transformVector(coriolis,pos.x,pos.y,0,nearEquator?0:forceGrowth);
    transformVector(velocity,pos.x,pos.y,nearEquator?-90:turn>0?0:180,speedGrowth);
    pressure.style.opacity=p<8?'.7':'1';
    coriolis.style.opacity=nearEquator?'0':String(forceGrowth);
    velocity.style.opacity=String(speedGrowth);
    const stage = p<25?0:p<48?1:p<76?2:3;
    $('#stage-number').textContent=`阶段 ${stage+1} / Stage ${stage+1}`;
    $('#stage-title').textContent=stages[stage].title;
    $('#stage-explanation').textContent=stages[stage].text;
    $$('[data-stage]').forEach((button,index)=>button.classList.toggle('active',index===stage));
  }

  function stop() {
    playing=false;
    clearInterval(timer);
    timer=0;
    playButton.textContent='▶ 播放 / Play';
    playButton.setAttribute('aria-label','播放地转流形成动画 / Play geostrophic-flow formation animation');
  }

  function tick() {
    if(!playing) return;
    const time=performance.now();
    if(!lastTime) lastTime=time;
    const next=Number(progress.value)+(time-lastTime)/115;
    lastTime=time;
    progress.value=String(next>100?0:next);
    render(Number(progress.value));
  }

  playButton.addEventListener('click',()=>{
    if(playing){stop();return}
    if(Number(progress.value)>=100)progress.value='0';
    playing=true;lastTime=0;
    playButton.textContent='Ⅱ 暂停 / Pause';
    playButton.setAttribute('aria-label','暂停地转流形成动画 / Pause geostrophic-flow formation animation');
    tick();
    timer=setInterval(tick,40);
  });
  progress.addEventListener('input',()=>{stop();render(Number(progress.value))});
  $$('[data-stage]').forEach(button=>button.addEventListener('click',()=>{stop();progress.value=String([0,30,56,84][Number(button.dataset.stage)]);render(Number(progress.value))}));
  latitude.addEventListener('input',updateParameters);
  slope.addEventListener('input',updateParameters);
  $('#reset-lab').addEventListener('click',()=>{stop();latitude.value='30';slope.value='5';progress.value='0';updateParameters()});
  $$('.quiz-options button').forEach(button=>button.addEventListener('click',()=>{
    $$('.quiz-options button').forEach(option=>option.classList.remove('correct','wrong'));
    const correct=button.dataset.answer==='correct';
    button.classList.add(correct?'correct':'wrong');
    $('#quiz-feedback').textContent=correct?'正确。压强梯度力向东；北半球中，要产生向西的科氏力，水流必须向南。 / Correct. The pressure-gradient force is eastward; in the Northern Hemisphere, a southward current produces the opposing westward Coriolis force.':'再想一步：北半球科氏力位于流向右侧。要让它指向西方，水流应向南。 / One more step: Northern Hemisphere Coriolis force lies to the right of the flow. For it to point west, the current must flow south.';
  }));
  document.addEventListener('visibilitychange',()=>{if(document.hidden)stop()});
  updateParameters();
})();
