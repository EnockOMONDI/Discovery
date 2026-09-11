const script = document.currentScript;
const sections = Array.from(document.querySelectorAll(".section"));
const stepButtons = Array.from(document.querySelectorAll(".step-dot"));
const progressBar = document.getElementById("progressBar");
const stepLabel = document.getElementById("stepLabel");
const stepPercent = document.getElementById("stepPercent");
const backButton = document.getElementById("backButton");
const nextButton = document.getElementById("nextButton");
const submitButton = document.getElementById("submitButton");
const form = document.querySelector("form[data-autosave-key]");
const introToggle = document.querySelector(".intro-toggle");
const sidebar = document.querySelector("aside");
const autosaveKey = form?.dataset.autosaveKey;
let currentStep = Number(script?.dataset.initialStep || 0);

function showStep(index) {
    currentStep = Math.max(0, Math.min(index, sections.length - 1));
    sections.forEach((section, i) => section.classList.toggle("is-active", i === currentStep));
    stepButtons.forEach((button, i) => button.classList.toggle("is-active", i === currentStep));
    const percent = Math.round(((currentStep + 1) / sections.length) * 100);
    progressBar.style.width = `${percent}%`;
    stepLabel.textContent = `Step ${currentStep + 1} of ${sections.length}`;
    stepPercent.textContent = `${percent}%`;
    backButton.disabled = currentStep === 0;
    nextButton.classList.toggle("is-hidden", currentStep === sections.length - 1);
    submitButton.classList.toggle("is-visible", currentStep === sections.length - 1);
    window.scrollTo({ top: 0, behavior: "smooth" });
}

backButton.addEventListener("click", () => showStep(currentStep - 1));
nextButton.addEventListener("click", () => showStep(currentStep + 1));
stepButtons.forEach((button) => {
    button.addEventListener("click", () => showStep(Number(button.dataset.stepJump)));
});

introToggle?.addEventListener("click", () => {
    const isOpen = sidebar?.classList.toggle("is-intro-open");
    introToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    introToggle.textContent = isOpen ? "Hide note" : "About this form";
});

function readSavedForm() {
    if (!autosaveKey) return {};
    try {
        return JSON.parse(localStorage.getItem(autosaveKey) || "{}");
    } catch {
        return {};
    }
}

function saveForm() {
    if (!form || !autosaveKey) return;
    const saved = {};
    new FormData(form).forEach((value, key) => {
        if (key === "csrfmiddlewaretoken" || key === "company_site") return;
        if (Object.prototype.hasOwnProperty.call(saved, key)) {
            saved[key] = Array.isArray(saved[key]) ? [...saved[key], value] : [saved[key], value];
        } else {
            saved[key] = value;
        }
    });
    localStorage.setItem(autosaveKey, JSON.stringify(saved));
}

function restoreForm() {
    if (!form || !autosaveKey) return;
    const saved = readSavedForm();
    for (const [key, value] of Object.entries(saved)) {
        const fields = Array.from(form.querySelectorAll(`[name="${CSS.escape(key)}"]`));
        fields.forEach((field) => {
            if (field.type === "checkbox" || field.type === "radio") {
                const values = Array.isArray(value) ? value : [value];
                field.checked = values.includes(field.value);
            } else if (!field.value) {
                field.value = value;
            }
        });
    }
}

restoreForm();
form?.addEventListener("input", saveForm);
form?.addEventListener("change", saveForm);
form?.addEventListener("submit", saveForm);
showStep(currentStep);
