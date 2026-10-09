const metrics = {
  frequency: {
    place: "东北部与沿岸 · 西南部对照 / Northeast and coast vs. southwest",
    value: "2–3", unit: "次/年 / events/year",
    detail: "东北部与近岸格点较频繁，平均每年 2–3 次；西南部不足 2 次/年。这是不同位置的多年平均，不是全海域统一值。 / Northeastern and nearshore cells average 2–3 events per year, while southwestern cells average fewer than two. These are multi-year means at different locations, not one basin-wide value.",
    regions: ["ne", "sw"]
  },
  duration: {
    place: "西北部 / Northwest",
    value: ">14", unit: "天/次 / days/event",
    detail: "西北部局地的单次平均持续时间超过 14 天。持续时间衡量每次事件的长度，不能等同于一年的热浪总天数。 / Mean duration of individual events exceeds 14 days in parts of the northwest. This is event length, not annual total heatwave days.",
    regions: ["nw"]
  },
  intensity: {
    place: "北部陆架 / Northern shelf",
    value: ">2", unit: "°C/次 / °C/event",
    detail: "北部陆架局地平均强度超过 2°C/次，并呈现总体由北向南减弱的空间特征。它描述海温异常，不是海水的绝对温度。 / Local mean intensity on the northern shelf exceeds 2 °C per event and generally weakens southward. It is an SST anomaly, not absolute water temperature.",
    regions: ["shelf"]
  },
  days: {
    place: "北部湾 / Beibu Gulf",
    value: ">30", unit: "天/年 / days/year",
    detail: "北部湾部分格点的年热浪总天数超过 30 天。总天数累加该年所有事件，可能受发生次数和每次持续长度共同影响。 / Some Beibu Gulf cells have more than 30 total heatwave days per year. Annual days accumulate across all events and depend on both frequency and duration.",
    regions: ["beibu"]
  },
  cumulative: {
    place: "北部与西部 / North and west",
    value: ">25", unit: "°C·天/次 / °C·days/event",
    detail: "北部和西部局地的单次累积强度超过 25°C·天/次；该指标同时反映异常程度和持续时间。 / Cumulative intensity exceeds 25 °C·days per event in parts of the north and west; it combines anomaly magnitude and duration.",
    regions: ["shelf", "west"]
  }
};

function showMetric(key) {
  const metric = metrics[key];
  if (!metric) return;
  for (const button of document.querySelectorAll("[data-metric]")) {
    const active = button.dataset.metric === key;
    button.classList.toggle("active", active);
    button.setAttribute("aria-pressed", String(active));
  }
  for (const marker of document.querySelectorAll(".map-marker")) {
    marker.classList.toggle("active", metric.regions.includes(marker.dataset.region));
  }
  document.querySelector("#metric-place").textContent = metric.place;
  const value = document.querySelector("#metric-value");
  const unit = document.createElement("small");
  unit.textContent = metric.unit;
  value.replaceChildren(document.createTextNode(metric.value + " "), unit);
  document.querySelector("#metric-detail").textContent = metric.detail;
}

for (const button of document.querySelectorAll("[data-metric]")) {
  button.addEventListener("click", () => showMetric(button.dataset.metric));
}
showMetric("frequency");

document.querySelector("#copy-heatwave").addEventListener("click", async () => {
  const status = document.querySelector("#copy-heatwave-status");
  try {
    await navigator.clipboard.writeText(location.href.split("#")[0]);
    status.textContent = "专题链接已复制 / Atlas link copied";
  } catch {
    status.textContent = "请复制浏览器地址栏中的链接 / Copy the URL from your address bar";
  }
});

for (const figure of document.querySelectorAll(".hw-chart-card")) {
  const img = figure.querySelector("img");
  const caption = figure.querySelector("figcaption");
  if (!img || !caption) continue;
  const link = document.createElement("a");
  link.href = img.getAttribute("src");
  link.target = "_blank";
  link.rel = "noopener";
  link.textContent = "查看大图 / Open full-size image ↗";
  link.setAttribute("aria-label", `查看大图 / Open full-size image: ${img.alt}`);
  caption.append(" ", link);
}
