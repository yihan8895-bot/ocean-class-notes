/* One language at a time for the existing paired Chinese/English copy. */
(() => {
  'use strict';
  const storageKey = 'ocean-class-notes-language';
  const originalText = new WeakMap();
  const originalAttributes = new WeakMap();
  const forcedLanguage = new WeakMap();
  let language;

  try { language = localStorage.getItem(storageKey) === 'en' ? 'en' : 'zh'; }
  catch { language = 'zh'; }
  document.documentElement.lang = language === 'zh' ? 'zh-CN' : 'en';
  document.documentElement.dataset.language = language;

  function pair(value) {
    const newline = value.match(/^([^\n]+)\n([^\n]+)$/);
    if (newline && /\p{Script=Han}/u.test(newline[1]) && /[A-Za-z]/.test(newline[2])) {
      return {zh: newline[1], en: newline[2]};
    }
    const separators = [...value.matchAll(/\s*\/\s+/g)];
    for (const match of separators) {
      const left = value.slice(0, match.index);
      const right = value.slice(match.index + match[0].length);
      if (!/\p{Script=Han}/u.test(left) || !/[A-Za-z\p{Script=Greek}]/u.test(right)) continue;
      const prefix = left.match(/^(\s*\d{1,2}\s*\/\s*)/);
      return {
        zh: left,
        en: (prefix ? prefix[1] : (left.match(/^\s*/) || [''])[0]) + right,
      };
    }
    return null;
  }

  function text(value) {
    const found = pair(value);
    return found ? found[language] : value;
  }

  function labelBlocks(root) {
    const elements = root.nodeType === Node.ELEMENT_NODE ? [root, ...root.querySelectorAll('*')] : [];
    for (const element of elements) {
      if (element.matches('h1 > small, h2 > small, h3 > small') && !/\p{Script=Han}/u.test(element.textContent)) {
        forcedLanguage.set(element, 'en');
        const parent = element.parentElement;
        for (const sibling of parent.childNodes) {
          if (sibling !== element) forcedLanguage.set(sibling, 'zh');
        }
      }
      if (element !== document.documentElement && element.matches('[lang="en"], .en-copy')) forcedLanguage.set(element, 'en');
      if (element.matches('.zh-copy')) forcedLanguage.set(element, 'zh');
      if (element.tagName === 'BR' && element.parentElement) {
        const siblings = [...element.parentElement.childNodes];
        const index = siblings.indexOf(element);
        const before = siblings.slice(0, index).map(node => node.textContent || '').join('');
        const after = siblings.slice(index + 1).map(node => node.textContent || '').join('');
        if (/\p{Script=Han}/u.test(before) && /^[\s\S]*[A-Za-z]/.test(after)) {
          for (const sibling of siblings.slice(0, index)) {
            if (!pair(sibling.textContent || '')) forcedLanguage.set(sibling, 'zh');
          }
          for (const sibling of siblings.slice(index + 1)) {
            if (!pair(sibling.textContent || '')) forcedLanguage.set(sibling, 'en');
          }
          forcedLanguage.set(element, 'none');
        }
      }
      if (element.matches('p, figcaption, li')) {
        const siblings = [...element.childNodes];
        const divider = siblings.findIndex(node => node.nodeType === 3 && pair(node.nodeValue));
        if (divider > 0) {
          for (const sibling of siblings.slice(0, divider)) {
            const value = sibling.textContent || '';
            if (value.trim() && !pair(value)) forcedLanguage.set(sibling, 'zh');
          }
        }
        if (divider >= 0) {
          for (const sibling of siblings.slice(divider + 1)) {
            const value = sibling.textContent || '';
            if (value.trim() && !pair(value)) forcedLanguage.set(sibling, 'en');
          }
        }
      }
    }
  }

  function inheritedLanguage(node) {
    let current = node;
    while (current && current !== document) {
      if (forcedLanguage.has(current)) return forcedLanguage.get(current);
      current = current.parentNode;
    }
    return null;
  }

  function updateTextNode(node) {
    if (!node.parentElement || node.parentElement.closest('script, style, noscript')) return;
    const previous = originalText.get(node);
    if (!previous || node.nodeValue !== previous.rendered) {
      originalText.set(node, {source: node.nodeValue, rendered: node.nodeValue});
    }
    const record = originalText.get(node);
    const mode = inheritedLanguage(node);
    const rendered = mode === 'none' || (mode && mode !== language) ? '' : mode ? record.source : text(record.source);
    if (node.nodeValue !== rendered) node.nodeValue = rendered;
    record.rendered = rendered;
  }

  function updateElement(element) {
    const mode = inheritedLanguage(element);
    if (mode && mode !== language) element.hidden = true;
    else if (mode && element.hidden) element.hidden = false;
    const names = ['alt', 'aria-label', 'placeholder', 'title', 'content'];
    let records = originalAttributes.get(element);
    if (!records) { records = new Map(); originalAttributes.set(element, records); }
    for (const name of names) {
      if (!element.hasAttribute(name)) continue;
      if (name === 'content' && element.tagName !== 'META') continue;
      const current = element.getAttribute(name);
      const previous = records.get(name);
      if (!previous || current !== previous.rendered) records.set(name, {source: current, rendered: current});
      const record = records.get(name);
      const rendered = text(record.source);
      if (current !== rendered) element.setAttribute(name, rendered);
      record.rendered = rendered;
    }
  }

  function refresh(root = document.documentElement) {
    if (!root) return;
    forcedLanguage.delete(document.documentElement);
    labelBlocks(root);
    const elements = root.nodeType === Node.ELEMENT_NODE ? [root, ...root.querySelectorAll('*')] : [];
    for (const element of elements) updateElement(element);
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    while (walker.nextNode()) updateTextNode(walker.currentNode);
    if (root.nodeType === Node.TEXT_NODE) updateTextNode(root);
    for (const img of document.querySelectorAll('img[data-i18n-src]')) {
      const base = img.dataset.i18nSrc;
      const extension = img.dataset.i18nExt || 'svg';
      const suffix = language === 'zh' ? (img.dataset.i18nZhSuffix ?? '-zh') : '-en';
      const version = base.startsWith('assets/argo/') ? '20261016-quarter-degree' : '20261015-i18n';
      const src = `${base}${suffix}.${extension}?v=${version}`;
      if (img.getAttribute('src') !== src) img.setAttribute('src', src);
      const imageLink = img.closest('a');
      if (imageLink && imageLink.getAttribute('href') !== src) imageLink.setAttribute('href', src);
      const fullSize = img.closest('figure')?.querySelector('figcaption a[target="_blank"]');
      if (fullSize && fullSize.getAttribute('href') !== src) fullSize.setAttribute('href', src);
      const download = img.closest('figure')?.querySelector('a.png-download');
      if (download && download.getAttribute('href') !== src) download.setAttribute('href', src);
    }
  }

  function setLanguage(next) {
    if (next !== 'zh' && next !== 'en') return;
    language = next;
    try { localStorage.setItem(storageKey, next); } catch { /* private browsing */ }
    document.documentElement.lang = next === 'zh' ? 'zh-CN' : 'en';
    document.documentElement.dataset.language = next;
    refresh();
    updatePageTitle();
    updateSwitch();
    window.dispatchEvent(new CustomEvent('site-language-change', {detail: {language: next}}));
  }

  function updateSwitch() {
    const button = document.querySelector('#language-switch');
    if (!button) return;
    button.textContent = language === 'zh' ? 'English' : '中文';
    button.setAttribute('aria-label', language === 'zh' ? 'Switch to English' : '切换为中文');
    button.setAttribute('aria-pressed', String(language === 'en'));
  }

  function updatePageTitle() {
    const name = location.pathname.split('/').pop();
    const titles = {
      'geostrophic.html': ['地转流｜形成机制、动画与观测', 'Geostrophic Flow | Formation, Animation and Observation'],
      'heatwaves.html': ['南海海洋热浪｜识别与时空特征', 'South China Sea Marine Heatwaves | Detection and Patterns'],
      'eof.html': ['南海海洋热浪 × EOF｜观测、分析与动画', 'South China Sea Heatwaves × EOF | Observations and Animation'],
      'test1.html': ['test1｜物理海洋学、上层海洋层结与对流混合', 'test1 | Physical Oceanography, Upper-Ocean Stratification and Convective Mixing'],
      'editor.html': ['添加内容 · 海洋课堂笔记', 'Add Content · Ocean Classroom Notes'],
    };
    if (titles[name]) document.title = titles[name][language === 'zh' ? 0 : 1];
  }

  function installSwitch() {
    const nav = document.querySelector('.site-header nav');
    if (!nav || document.querySelector('#language-switch')) return;
    const button = document.createElement('button');
    button.id = 'language-switch';
    button.className = 'language-switch';
    button.type = 'button';
    button.addEventListener('click', () => setLanguage(language === 'zh' ? 'en' : 'zh'));
    nav.append(button);
    updateSwitch();
  }

  let queued = false;
  const pending = new Set();
  const observer = new MutationObserver(mutations => {
    for (const item of mutations) pending.add(item.target);
    if (queued || !pending.size) return;
    queued = true;
    queueMicrotask(() => {
      queued = false;
      const changed = [...pending];
      pending.clear();
      for (const node of changed) {
        if (node.nodeType === Node.TEXT_NODE) updateTextNode(node);
        else if (node.isConnected) refresh(node);
      }
    });
  });

  window.siteI18n = {get language() { return language; }, text, refresh, setLanguage};
  installSwitch();
  refresh();
  updatePageTitle();
  observer.observe(document.body, {subtree: true, childList: true, characterData: true});
})();
