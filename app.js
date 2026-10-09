const $ = (selector) => document.querySelector(selector);
let entries = [];
let activeCategory = "全部";
const categoryEnglish = {
  "全部": "All", "专题分析": "Research Atlas", "课堂问答": "Classroom Q&A",
  "热量收支": "Heat Budget", "计算例题": "Worked Example", "图片解读": "Figure Guide",
  "EOF 方法": "EOF Method", "动态图解": "Animation", "研究方法": "Research Methods"
};
const bilingualCategory = (name) => `${name} / ${categoryEnglish[name] || name}`;

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function textOf(entry) {
  return [entry.title, entry.summary, entry.category, ...(entry.tags || []), ...(entry.blocks || []).map((block) => block.text || ""), entry.body || ""].join(" ").toLocaleLowerCase();
}

function renderFilters() {
  const choices = ["全部", ...new Set(entries.map((entry) => entry.category))];
  if (!choices.includes(activeCategory)) activeCategory = "全部";
  const root = $("#filters");
  root.replaceChildren();
  for (const category of choices) {
    const button = el("button", `filter${category === activeCategory ? " selected" : ""}`, bilingualCategory(category));
    button.type = "button";
    button.setAttribute("aria-pressed", String(category === activeCategory));
    button.addEventListener("click", () => { activeCategory = category; renderFilters(); renderCards(); });
    root.append(button);
  }
}

function renderCards() {
  const query = $("#search").value.trim().toLocaleLowerCase();
  const filtered = entries.filter((entry) => (activeCategory === "全部" || entry.category === activeCategory) && textOf(entry).includes(query));
  const root = $("#cards");
  root.replaceChildren();
  for (const [index, entry] of filtered.entries()) {
    const card = el("a", "card");
    card.href = entry.href || `#note/${encodeURIComponent(entry.id)}`;
    if (entry.href) card.classList.add("card-feature");
    const top = el("div", "card-top");
    top.append(el("span", "pill", bilingualCategory(entry.category)), el("span", "card-index", String(index + 1).padStart(2, "0")));
    card.append(top, el("h3", "", entry.title), el("p", "", entry.summary));
    const bottom = el("div", "card-bottom");
    bottom.append(el("span", "", entry.href ? "查看专题 / Open Atlas" : "阅读全文 / Read Article"), el("span", "card-arrow", "↗"));
    card.append(bottom);
    root.append(card);
  }
  $("#result-count").textContent = `${filtered.length} 篇内容 / articles`;
  $("#empty").hidden = filtered.length > 0;
}

function appendImage(root, imageUrl, title) {
  if (!imageUrl) return;
  const figure = el("figure", "article-figure");
  const image = el("img");
  image.src = imageUrl;
  image.alt = title;
  image.loading = "lazy";
  figure.append(image);
  root.append(figure);
}

function renderArticle(entry) {
  $("#home").hidden = true;
  $("#article-page").hidden = false;
  $("#article-labels").replaceChildren(el("span", "pill", bilingualCategory(entry.category)), el("span", "article-label", entry.custom ? "新增内容 / Added Article" : "课堂整理 / Classroom Notes"));
  $("#article-title").textContent = entry.title;
  $("#article-summary").textContent = entry.summary;
  const content = $("#article-content");
  content.replaceChildren();
  appendImage(content, entry.image, entry.title);
  if (entry.blocks) {
    for (const block of entry.blocks) {
      const tag = block.type === "formula" || block.type === "note" ? "div" : "p";
      const node = el(tag, `block-${block.type}`);
      const parts = block.text.split("\n");
      if (parts.length === 2) {
        node.append(el("span", "zh-copy", parts[0]), el("span", "en-copy", parts[1]));
      } else {
        node.textContent = block.text;
      }
      content.append(node);
    }
  } else {
    for (const paragraph of (entry.body || "").split(/\n\s*\n/).filter(Boolean)) {
      const node = el("p", "block-p");
      const parts = paragraph.split("\n");
      if (parts.length === 2) node.append(el("span", "zh-copy", parts[0]), el("span", "en-copy", parts[1]));
      else node.textContent = paragraph;
      content.append(node);
    }
  }
  const sources = $("#article-sources");
  sources.replaceChildren();
  if (entry.sources?.length) {
    sources.append(el("h2", "", "参考资料 / References"));
    for (const source of entry.sources) {
      const link = el("a", "", source.label);
      link.href = source.url;
      link.target = "_blank";
      link.rel = "noopener noreferrer";
      sources.append(link);
    }
  }
  document.title = `${entry.title} · 海洋课堂笔记 / Ocean Classroom Notes`;
  window.scrollTo(0, 0);
}

function route() {
  let hash;
  try { hash = decodeURIComponent(location.hash.slice(1)); } catch { hash = ""; }
  if (hash.startsWith("note/")) {
    const entry = entries.find((candidate) => candidate.id === hash.slice(5));
    if (entry) { renderArticle(entry); return; }
  }
  $("#home").hidden = false;
  $("#article-page").hidden = true;
  document.title = "海洋课堂笔记 / Ocean Classroom Notes · 物理海洋学 / Physical Oceanography";
  if (hash === "library") requestAnimationFrame(() => $("#library").scrollIntoView());
}

async function load() {
  const [coreResponse, additionsResponse] = await Promise.all([
    fetch("content.json", {cache: "no-cache"}),
    fetch("content/additions.json", {cache: "no-cache"})
  ]);
  if (!coreResponse.ok || !additionsResponse.ok) throw new Error("无法读取资料 / Could not load articles");
  entries = [...await coreResponse.json(), ...await additionsResponse.json()];
  $("#hero-count").textContent = String(entries.length);
  renderFilters(); renderCards(); route();
}

$("#search").addEventListener("input", renderCards);
$("#copy-link").addEventListener("click", async () => {
  try { await navigator.clipboard.writeText(location.href); $("#copy-status").textContent = "链接已复制 / Link copied"; }
  catch { $("#copy-status").textContent = "请复制浏览器地址栏中的链接 / Copy the URL from your address bar"; }
});
document.addEventListener("keydown", (event) => {
  if (event.key === "/" && $("#article-page").hidden && !["INPUT", "TEXTAREA"].includes(document.activeElement.tagName)) { event.preventDefault(); $("#search").focus(); }
});
window.addEventListener("hashchange", route);
load().catch((error) => { $("#load-note").textContent = error.message; });
