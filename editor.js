const $ = selector => document.querySelector(selector);
let generated = "";

function download(name, content) {
  const url = URL.createObjectURL(new Blob([content], {type: "application/json;charset=utf-8"}));
  const a = document.createElement("a");
  a.href = url;
  a.download = name;
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

$("#article-form").addEventListener("submit", async event => {
  event.preventDefault();
  const status = $("#editor-status");
  status.textContent = "正在读取现有资料… / Reading current articles…";
  try {
    const response = await fetch("content/additions.json", {cache: "no-cache"});
    if (!response.ok) throw new Error("无法读取现有资料 / Could not read current articles");
    const entries = await response.json();
    if (!Array.isArray(entries)) throw new Error("现有资料格式异常 / Current file is not an array");
    const title = $("#title").value.trim();
    const category = $("#category").value.trim();
    const summary = $("#summary").value.trim();
    const body = $("#body").value.trim();
    const image = $("#image").value.trim();
    if (!title || !category || !summary || !body) throw new Error("请填写所有必填项 / Fill in all required fields");
    if (image && !/^assets\/[\w./-]+$/.test(image) && !/^https:\/\//i.test(image)) throw new Error("配图请用 assets/ 路径或 HTTPS URL / Use an assets/ path or HTTPS URL");
    const newEntry = {id: crypto.randomUUID(), title, category, summary, body, image, custom: true, updatedAt: new Date().toISOString()};
    generated = JSON.stringify([newEntry, ...entries], null, 2) + "\n";
    $("#download").disabled = false;
    try {
      await navigator.clipboard.writeText(generated);
      status.textContent = "已复制包含新文章的完整 JSON。现在打开 GitHub 编辑页，替换全部内容并提交。 / Full JSON copied. Open the GitHub editor, replace its contents and commit.";
    } catch {
      download("additions.json", generated);
      status.textContent = "浏览器未允许复制，已下载 additions.json。请在 GitHub 编辑页粘贴文件内容。 / Clipboard access was denied; additions.json was downloaded. Paste its contents into the GitHub editor.";
    }
  } catch (error) {
    status.textContent = error.message;
  }
});

$("#download").addEventListener("click", () => {
  if (generated) download("additions.json", generated);
});
