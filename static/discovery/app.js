const script = document.currentScript;
const sections = Array.from(document.querySelectorAll(".section"));
const stepButtons = Array.from(document.querySelectorAll(".step-dot"));
const progressBar = document.getElementById("progressBar");
const stepLabel = document.getElementById("stepLabel");
const stepPercent = document.getElementById("stepPercent");
const backButton = document.getElementById("backButton");
const nextButton = document.getElementById("nextButton");
const submitButton = document.getElementById("submitButton");
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
showStep(currentStep);
