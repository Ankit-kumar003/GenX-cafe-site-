// ── Loader ──────────────────────────────────────────
window.addEventListener('load', () => {
  setTimeout(() => {
    const loader = document.getElementById('page-loader');
    if (loader) { loader.classList.add('hidden'); setTimeout(() => loader.remove(), 400); }
  }, 600);
});

// ── Theme Toggle ────────────────────────────────────
const themeBtn = document.getElementById('themeToggle');
const html = document.documentElement;
const saved = localStorage.getItem('theme') || 'light';
html.setAttribute('data-theme', saved);
updateThemeIcon();

if (themeBtn) {
  themeBtn.addEventListener('click', () => {
    const next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
    updateThemeIcon();
  });
}
function updateThemeIcon() {
  if (!themeBtn) return;
  const icon = themeBtn.querySelector('i');
  if (icon) icon.className = html.getAttribute('data-theme') === 'dark' ? 'bi bi-sun' : 'bi bi-moon-stars';
}

// ── Navbar Scroll ────────────────────────────────────
const nav = document.getElementById('mainNav');
if (nav) {
  window.addEventListener('scroll', () => {
    nav.classList.toggle('scrolled', window.scrollY > 50);
  });
}

// ── Chatbot ──────────────────────────────────────────
const fab = document.getElementById('chatbotFab');
const win = document.getElementById('chatbotWindow');
const closeBtn = document.getElementById('chatClose');
const sendBtn = document.getElementById('chatSend');
const inputEl = document.getElementById('chatInput');
const msgBox = document.getElementById('chatMessages');

if (fab) {
  fab.addEventListener('click', () => { win.classList.toggle('open'); if (win.classList.contains('open')) inputEl.focus(); });
}
if (closeBtn) { closeBtn.addEventListener('click', () => win.classList.remove('open')); }
if (sendBtn) { sendBtn.addEventListener('click', sendChat); }
if (inputEl) { inputEl.addEventListener('keydown', e => { if (e.key === 'Enter') sendChat(); }); }

async function sendChat() {
  const msg = inputEl.value.trim();
  if (!msg) return;
  appendMsg(msg, 'user');
  inputEl.value = '';
  const typing = appendMsg('...', 'bot typing');
  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: msg })
    });
    const data = await res.json();
    typing.remove();
    appendMsg(data.reply || 'Sorry, something went wrong!', 'bot');
  } catch {
    typing.remove();
    appendMsg('Connection error. Please try again.', 'bot');
  }
}

function appendMsg(text, type) {
  const div = document.createElement('div');
  div.className = `chat-msg ${type}`;
  div.textContent = text;
  msgBox.appendChild(div);
  msgBox.scrollTop = msgBox.scrollHeight;
  return div;
}

// ── Scroll Reveal ─────────────────────────────────────
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); } });
}, { threshold: 0.1 });
document.querySelectorAll('.menu-card, .review-card, .team-card, .mv-card, .stat-card').forEach(el => {
  el.classList.add('reveal');
  observer.observe(el);
});

// Add CSS for reveal
const style = document.createElement('style');
style.textContent = `.reveal { opacity: 0; transform: translateY(20px); transition: opacity 0.5s, transform 0.5s; } .reveal.visible { opacity: 1; transform: none; } #mainNav.scrolled { box-shadow: 0 2px 20px rgba(0,0,0,0.15); }`;
document.head.appendChild(style);
