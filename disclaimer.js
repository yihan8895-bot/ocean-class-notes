(() => {
  'use strict';

  function addDisclaimer() {
    if (document.getElementById('site-disclaimer')) return;
    const notice = document.createElement('aside');
    notice.id = 'site-disclaimer';
    notice.className = 'site-disclaimer';
    notice.setAttribute('aria-label', '网站免责声明 / Site disclaimer');
    notice.innerHTML = `
      <div class="site-disclaimer-inner">
        <span class="site-disclaimer-kicker">使用说明 / READING NOTE</span>
        <h2>免责声明 / Disclaimer</h2>
        <p lang="zh-CN">本站是个人物理海洋学学习与研究练习资料。公式、图表和动画应结合所列来源、数据范围及处理假设阅读；示意动画不等于实测，统计关系不直接证明成因。引用或用于研究前，请核对原始教材、文献和数据说明。</p>
        <p lang="en">This is a personal physical-oceanography learning and research-practice site. Read equations, figures and animations with their cited sources, data coverage and processing assumptions. Schematic animations are not observations, and statistical relationships do not by themselves establish causes. Check the original textbook, papers and data documentation before citing or using the material in research.</p>
        <a href="disclaimer.html">查看完整免责声明 ↗ / Read the full disclaimer ↗</a>
        <a href="ai-use.html">AI 使用与核验 ↗ / AI Use and Verification ↗</a>
      </div>`;
    const footer = document.querySelector('body > footer');
    if (footer) footer.before(notice);
    else document.body.append(notice);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', addDisclaimer, {once: true});
  } else {
    addDisclaimer();
  }
})();
