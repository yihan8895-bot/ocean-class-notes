const journalStorage = {
  read(key, fallback = "") {
    try { return localStorage.getItem(key) ?? fallback; } catch { return fallback; }
  },
  write(key, value) {
    try { localStorage.setItem(key, value); } catch { /* Private browsing may block storage. */ }
  },
  remove(key) {
    try { localStorage.removeItem(key); } catch { /* Ignore unavailable storage. */ }
  }
};

const tickets = [...document.querySelectorAll(".ticket")];
const progressBar = document.querySelector("#ticket-progress-bar");
const progressText = document.querySelector("#ticket-progress-text");

function updateTicketProgress() {
  const answered = tickets.filter((ticket) => ticket.querySelector("textarea").value.trim()).length;
  if (progressBar) progressBar.style.width = `${(answered / Math.max(tickets.length, 1)) * 100}%`;
  if (progressText) progressText.textContent = `${answered} / ${tickets.length} 已作答 / answered`;
  tickets.forEach((ticket) => ticket.classList.toggle("completed", Boolean(ticket.querySelector("textarea").value.trim())));
}

tickets.forEach((ticket) => {
  const id = ticket.dataset.ticket;
  const textarea = ticket.querySelector("textarea");
  const guide = ticket.querySelector(".ticket-guide");
  const reveal = ticket.querySelector(".reveal-answer");
  textarea.value = journalStorage.read(`ocean-ticket-${id}`);
  textarea.addEventListener("input", () => {
    journalStorage.write(`ocean-ticket-${id}`, textarea.value);
    updateTicketProgress();
  });
  reveal.addEventListener("click", () => {
    guide.hidden = !guide.hidden;
    reveal.textContent = guide.hidden ? "查看参考思路 / Reveal guide" : "收起参考思路 / Hide guide";
  });
});

document.querySelector("#ticket-reset")?.addEventListener("click", () => {
  tickets.forEach((ticket) => {
    const id = ticket.dataset.ticket;
    ticket.querySelector("textarea").value = "";
    journalStorage.remove(`ocean-ticket-${id}`);
  });
  updateTicketProgress();
});

const tellbackForm = document.querySelector("#tellback-form");
const reviewerName = document.querySelector("#reviewer-name");
const reviewerSummary = document.querySelector("#reviewer-summary");
const tellbackStatus = document.querySelector("#tellback-status");

function restoreTellback() {
  if (!tellbackForm) return;
  reviewerName.value = journalStorage.read("ocean-reviewer-name");
  reviewerSummary.value = journalStorage.read("ocean-reviewer-summary");
  const savedAt = journalStorage.read("ocean-reviewer-date");
  if (reviewerName.value && reviewerSummary.value && savedAt) {
    tellbackStatus.textContent = `✓ 已记录复述确认 / Tell-back recorded · ${savedAt}`;
  }
}

tellbackForm?.addEventListener("submit", (event) => {
  event.preventDefault();
  if (!reviewerName.value.trim() || !reviewerSummary.value.trim()) {
    tellbackStatus.textContent = "请填写复述者和复述内容 / Add both reviewer and tell-back";
    return;
  }
  const savedAt = new Date().toLocaleDateString("zh-CN");
  journalStorage.write("ocean-reviewer-name", reviewerName.value.trim());
  journalStorage.write("ocean-reviewer-summary", reviewerSummary.value.trim());
  journalStorage.write("ocean-reviewer-date", savedAt);
  tellbackStatus.textContent = `✓ 已记录复述确认 / Tell-back recorded · ${savedAt}`;
});

restoreTellback();
updateTicketProgress();
