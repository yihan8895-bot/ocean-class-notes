(() => {
  'use strict';
  const NS = 'http://www.w3.org/2000/svg';
  const byId = id => document.getElementById(id);
  const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));
  const mix = (a, b, t) => a.map((v, i) => Math.round(v + (b[i] - v) * t));
  function color(value, limit) {
    const x = clamp(value / limit, -1, 1);
    const neutral = [247, 250, 248];
    const rgb = x < 0 ? mix(neutral, [28, 105, 161], -x) : mix(neutral, [186, 55, 50], x);
    return `rgb(${rgb.join(',')})`;
  }
  function plotMap(canvas, data, values, limit) {
    const W = 660, H = 530, x0 = 110, y0 = 48, pw = 440, ph = 440;
    canvas.width = W; canvas.height = H;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, W, H);
    ctx.fillStyle = '#e8efec'; ctx.fillRect(x0, y0, pw, ph);
    const cw = pw / data.nx, ch = ph / data.ny;
    for (let j = 0; j < data.ny; j++) {
      for (let i = 0; i < data.nx; i++) {
        const n = i + data.nx * j;
        if (!data.ocean[n] || values[n] === null) continue;
        ctx.fillStyle = color(values[n], limit);
        ctx.fillRect(x0 + i * cw, y0 + (data.ny - 1 - j) * ch, cw + .35, ch + .35);
      }
    }
    ctx.strokeStyle = '#b8cecd'; ctx.lineWidth = 1;
    ctx.strokeRect(x0 + .5, y0 + .5, pw, ph);
    ctx.fillStyle = '#64818b'; ctx.font = '13px sans-serif';
    ctx.textAlign = 'center';
    for (const tick of [100, 105, 110, 115, 120]) {
      const px = x0 + (tick - 100) / 22 * pw;
      ctx.fillText(`${tick}°E`, px, y0 + ph + 23);
    }
    ctx.textAlign = 'right';
    for (const tick of [0, 5, 10, 15, 20, 25]) {
      const py = y0 + ph - tick / 25 * ph;
      ctx.fillText(`${tick}°N`, x0 - 12, py + 4);
    }
    ctx.textAlign = 'left';ctx.font = 'bold 13px sans-serif';ctx.fillStyle = '#345967';
    ctx.fillText(`色标 / Scale: −${limit} to +${limit} 天 / days`, x0, 27);
  }
  function svgElement(name, attrs = {}) {
    const el = document.createElementNS(NS, name);
    for (const [key, value] of Object.entries(attrs)) el.setAttribute(key, String(value));
    return el;
  }
  function plotPC(container, data, index) {
    const w = 540, h = 165, x0 = 35, x1 = 525, y0 = 15, y1 = 133;
    const values = data.pc.map(row => row[index]);
    const cap = Math.max(1, Math.ceil(Math.max(...values.map(Math.abs)) * 2) / 2);
    const x = i => x0 + i / (values.length - 1) * (x1 - x0);
    const y = v => y0 + (cap - v) / (2 * cap) * (y1 - y0);
    const svg = svgElement('svg', {viewBox:`0 0 ${w} ${h}`,role:'img','aria-label':`EOF ${index + 1} 的 1996 至 2025 年标准化时间系数 / standardized principal component, 1996–2025`});
    svg.append(svgElement('line',{x1:x0,y1:y(0),x2:x1,y2:y(0),class:'pc-zero'}));
    svg.append(svgElement('line',{x1:x0,y1:y0,x2:x0,y2:y1,class:'pc-axis'}));
    const path = values.map((v,i) => `${i ? 'L' : 'M'} ${x(i).toFixed(1)} ${y(v).toFixed(1)}`).join(' ');
    svg.append(svgElement('path',{d:path,class:'pc-line'}));
    values.forEach((v,i) => {
      const c = svgElement('circle',{cx:x(i),cy:y(v),r:2.9,class:'pc-dot'});
      const title = svgElement('title'); title.textContent = `${data.years[i]}：${v > 0 ? '+' : ''}${v.toFixed(2)} SD`;
      c.append(title);
      svg.append(c);
    });
    for (const year of [1996, 2005, 2015, 2025]) {
      const t = svgElement('text',{x:x(year - 1996),y:154,'text-anchor':year===1996?'start':year===2025?'end':'middle',class:'pc-label'});
      t.textContent = year; svg.append(t);
    }
    const lab = svgElement('text',{x:x0+3,y:12,class:'pc-label'});lab.textContent='PC（标准差 / SD）';svg.append(lab);
    container.replaceChildren(svg);
  }
  function main(data) {
    if (data.nx !== 88 || data.ny !== 100 || data.years.length !== 30 || data.patterns.length < 2) throw new Error('EOF 数据结构不符合预期');
    for (let k=0;k<2;k++) {
      const vals = data.patterns[k].filter(Number.isFinite);
      const limit = Math.ceil(Math.max(...vals.map(Math.abs)) / 5) * 5;
      plotMap(byId(`mode-map-${k+1}`), data, data.patterns[k], limit);
      plotPC(byId(`pc-plot-${k+1}`), data, k);
    }
    const slider = byId('year-slider'), yearLabel = byId('animation-year'), pcLabel = byId('animation-pc');
    const caption = byId('animation-caption'), button = byId('play-eof');
    byId('scale-minus').textContent = `−${data.reconstructionColorLimit}`;
    byId('scale-plus').textContent = `+${data.reconstructionColorLimit}`;
    let timer = null;
    function stop() { if (timer !== null) clearInterval(timer); timer = null; button.textContent='▶ 播放 / Play'; button.setAttribute('aria-label','播放逐年 EOF 重建动画 / Play annual EOF reconstruction'); }
    function renderYear(i) {
      slider.value = String(i);
      const pc1 = data.pc[i][0], pc2 = data.pc[i][1];
      const field = data.patterns[0].map((v,n) => v === null ? null : pc1*v + pc2*data.patterns[1][n]);
      plotMap(byId('reconstruction-map'),data,field,data.reconstructionColorLimit);
      yearLabel.textContent = String(data.years[i]);
      const fmt = v => `${v >= 0 ? '+' : ''}${v.toFixed(2)}`;
      pcLabel.textContent = `PC1 ${fmt(pc1)} · PC2 ${fmt(pc2)}`;
      caption.textContent = `${data.years[i]} 年 / year: 前两 EOF 模态的重建年热浪天数距平（天）。红色为高于该格点 30 年均值，蓝色为低于均值；该图不是逐日观测。 / Annual heatwave-day anomaly reconstructed from the first two EOF modes. Red is above and blue below each cell's 30-year mean. This is not daily observation.`;
    }
    slider.addEventListener('input',() => {stop();renderYear(Number(slider.value));});
    button.addEventListener('click',() => {
      if (timer !== null) {stop();return;}
      button.textContent='Ⅱ 暂停 / Pause';button.setAttribute('aria-label','暂停逐年 EOF 重建动画 / Pause annual EOF reconstruction');
      timer=setInterval(() => renderYear((Number(slider.value)+1)%data.years.length),800);
    });
    document.addEventListener('visibilitychange',() => {if(document.hidden)stop();});
    renderYear(0);
  }
  fetch('assets/eof-analysis.json').then(response => {if(!response.ok)throw new Error(`HTTP ${response.status}`);return response.json();}).then(main).catch(error => {
    byId('animation-caption').textContent=`数据未能加载。请刷新页面或查看下方研究原图。 / Data could not load. Refresh the page or view the original research figures below. (${error.message})`;
    console.error('EOF atlas failed:',error);
  });
})();
