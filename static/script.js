const $ = (id) => document.getElementById(id);

const dropzone = $("dropzone");
const fileInput = $("fileInput");
const preview = $("preview");
const dropText = $("dropText");
const analyzeBtn = $("analyzeBtn");
const resetBtn = $("resetBtn");

const emptyState = $("emptyState");
const loader = $("loader");
const errorBox = $("error");
const resultBox = $("result");

const MAX_SIZE = 5 * 1024 * 1024;
const HISTORY_KEY = "cropcare_history";

let selectedFile = null;
let previewDataUrl = "";

// ---------- File selection ----------
dropzone.addEventListener("click", () => fileInput.click());
dropzone.addEventListener("keydown", (e) => {
  if (e.key === "Enter" || e.key === " ") fileInput.click();
});
fileInput.addEventListener("change", () => handleFile(fileInput.files[0]));

["dragenter", "dragover"].forEach((evt) =>
  dropzone.addEventListener(evt, (e) => { e.preventDefault(); dropzone.classList.add("drag"); })
);
["dragleave", "drop"].forEach((evt) =>
  dropzone.addEventListener(evt, (e) => { e.preventDefault(); dropzone.classList.remove("drag"); })
);
dropzone.addEventListener("drop", (e) => handleFile(e.dataTransfer.files[0]));

function handleFile(file) {
  hideError();
  if (!file) return;
  if (!["image/jpeg", "image/png", "image/webp"].includes(file.type)) {
    return showError("Please choose a JPG, PNG or WEBP image.");
  }
  if (file.size > MAX_SIZE) {
    return showError("Image is too large. Maximum size is 5 MB.");
  }
  selectedFile = file;
  const reader = new FileReader();
  reader.onload = (e) => {
    previewDataUrl = e.target.result;
    preview.src = previewDataUrl;
    preview.hidden = false;
    dropText.hidden = true;
    analyzeBtn.disabled = false;
  };
  reader.readAsDataURL(file);
}

resetBtn.addEventListener("click", () => {
  selectedFile = null;
  fileInput.value = "";
  preview.hidden = true;
  dropText.hidden = false;
  analyzeBtn.disabled = true;
  resultBox.hidden = true;
  emptyState.hidden = false;
  hideError();
});

// ---------- Analyze ----------
analyzeBtn.addEventListener("click", async () => {
  if (!selectedFile) return;
  hideError();
  emptyState.hidden = true;
  resultBox.hidden = true;
  loader.hidden = false;
  analyzeBtn.disabled = true;

  const formData = new FormData();
  formData.append("image", selectedFile);

  try {
    const res = await fetch("/predict", { method: "POST", body: formData });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Something went wrong.");
    showResult(data);
    saveHistory(data);
  } catch (err) {
    emptyState.hidden = false;
    showError(err.message);
  } finally {
    loader.hidden = true;
    analyzeBtn.disabled = false;
  }
});

function showResult(d) {
  $("cropName").textContent = d.crop;
  $("diseaseName").textContent = d.disease;
  $("confText").textContent = d.confidence + "%";
  $("description").textContent = d.description;
  $("lowConf").hidden = !d.low_confidence;

  const badge = $("statusBadge");
  badge.textContent = d.is_healthy ? "Healthy" : "Disease detected";
  badge.className = "badge " + (d.is_healthy ? "ok" : "bad");

  fillList($("treatment"), d.treatment);
  fillList($("prevention"), d.prevention);

  const top3 = $("top3");
  top3.innerHTML = "";
  d.top3.forEach((t) => {
    const li = document.createElement("li");
    li.innerHTML = `<span></span><strong>${t.confidence}%</strong>`;
    li.querySelector("span").textContent = t.label;
    top3.appendChild(li);
  });

  resultBox.hidden = false;
  const bar = $("confBar");
  bar.style.width = "0";
  requestAnimationFrame(() => requestAnimationFrame(() => (bar.style.width = d.confidence + "%")));
}

function fillList(ul, items) {
  ul.innerHTML = "";
  items.forEach((text) => {
    const li = document.createElement("li");
    li.textContent = text;
    ul.appendChild(li);
  });
}

function showError(msg) { errorBox.textContent = msg; errorBox.hidden = false; }
function hideError() { errorBox.hidden = true; }

// ---------- History (saved in the browser) ----------
function getHistory() {
  try { return JSON.parse(localStorage.getItem(HISTORY_KEY)) || []; }
  catch { return []; }
}

function saveHistory(d) {
  const thumb = makeThumbnail(previewDataUrl, 160).then((img) => {
    const items = getHistory();
    items.unshift({
      img, crop: d.crop, disease: d.disease,
      confidence: d.confidence, time: new Date().toLocaleString(),
    });
    try { localStorage.setItem(HISTORY_KEY, JSON.stringify(items.slice(0, 8))); } catch {}
    renderHistory();
  });
  return thumb;
}

function makeThumbnail(dataUrl, size) {
  return new Promise((resolve) => {
    const img = new Image();
    img.onload = () => {
      const canvas = document.createElement("canvas");
      const scale = size / Math.max(img.width, img.height);
      canvas.width = img.width * scale;
      canvas.height = img.height * scale;
      canvas.getContext("2d").drawImage(img, 0, 0, canvas.width, canvas.height);
      resolve(canvas.toDataURL("image/jpeg", 0.7));
    };
    img.src = dataUrl;
  });
}

function renderHistory() {
  const list = $("historyList");
  const items = getHistory();
  list.innerHTML = "";
  if (!items.length) {
    list.innerHTML = '<p class="history-empty">No scans yet. Your recent results will show up here.</p>';
    return;
  }
  items.forEach((it) => {
    const card = document.createElement("div");
    card.className = "history-item";
    card.innerHTML = `<img alt="" /><div><strong></strong><span></span></div>`;
    card.querySelector("img").src = it.img;
    card.querySelector("strong").textContent = `${it.crop} - ${it.disease}`;
    card.querySelector("span").textContent = `${it.confidence}% · ${it.time}`;
    list.appendChild(card);
  });
}

$("clearHistory").addEventListener("click", () => {
  localStorage.removeItem(HISTORY_KEY);
  renderHistory();
});

renderHistory();
