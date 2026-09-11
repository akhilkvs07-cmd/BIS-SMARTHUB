const toast = document.getElementById('toast');
const input = document.getElementById('copilotInput');

function show(message){
  toast.textContent = message;
  toast.classList.add('show');
  clearTimeout(window.__toast);
  window.__toast = setTimeout(()=>toast.classList.remove('show'),2600);
}

const prompts = document.querySelectorAll('[data-prompt]');
prompts.forEach(button => button.addEventListener('click', () => {
  input.value = button.dataset.prompt;
  input.focus();
}));

document.getElementById('askBtn').addEventListener('click', () => {
  const value = input.value.trim();
  if (!value) return show('Type a BIS question to start.');
  show('Copilot workflow is ready — intelligence and evidence connectors will be attached next.');
});

document.querySelectorAll('[data-action]').forEach(card => card.addEventListener('click', () => {
  const labels = {
    consumer:'Consumer product-check workflow',
    manufacturer:'MSME compliance workspace',
    scan:'Scan Anything workflow',
    standard:'Standards intelligence search',
    lab:'Smart laboratory matching',
    report:'Suspicious product reporting'
  };
  show(`${labels[card.dataset.action]} is part of the SmartHub build.`);
}));

document.getElementById('profileBtn').addEventListener('click', () => {
  show('Role selection will personalize your SmartHub dashboard.');
});

document.getElementById('languageBtn').addEventListener('click', () => {
  show('Language foundation: English, Hindi, Kannada, Telugu and Tamil.');
});
