const fileInput = document.getElementById("fileInput");
const pickBtn = document.getElementById("pickBtn");
const analyzeBtn = document.getElementById("analyzeBtn");
const preview = document.getElementById("preview");
const rawTextEl = document.getElementById("rawText");
const cleanTextEl = document.getElementById("cleanText");
const reviewTextEl = document.getElementById("reviewText");

let selectedFile = null;

pickBtn.addEventListener("click", () => fileInput.click());

fileInput.addEventListener("change", (ev) => {
  const f = ev.target.files && ev.target.files[0];
  if (!f) return;

  selectedFile = f;

  const url = URL.createObjectURL(f);
  preview.innerHTML = "";
  const img = document.createElement("img");
  img.src = url;
  img.alt = "Selected ingredient image";
  preview.appendChild(img);

  analyzeBtn.disabled = false;
  rawTextEl.value = "";
  cleanTextEl.value = "";
  reviewTextEl.textContent = "";
});

analyzeBtn.addEventListener("click", async () => {
  if (!selectedFile) return;

  analyzeBtn.disabled = true;
  analyzeBtn.textContent = "Analyzing...";
  rawTextEl.value = "";
  cleanTextEl.value = "";
  reviewTextEl.textContent = "";

  try {
    const form = new FormData();
    form.append("image", selectedFile);

    const resp = await fetch("/api/analyze", { method: "POST", body: form });
    if (!resp.ok) {
      const errText = await resp.text();
      throw new Error(`Server error (${resp.status}): ${errText}`);
    }

    const json = await resp.json();
    rawTextEl.value = json.raw_text || "";
    cleanTextEl.value = json.clean_text || "";
    reviewTextEl.textContent = json.review || "";
  } catch (err) {
    console.error(err);
    rawTextEl.value = "";
    cleanTextEl.value = "";
    reviewTextEl.textContent = `Analysis failed: ${err.message || err}`;
  } finally {
    analyzeBtn.disabled = false;
    analyzeBtn.textContent = "Analyze";
  }
});

