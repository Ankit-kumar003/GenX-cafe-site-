// ── Sidebar Toggle ────────────────────────────────────
const sidebar = document.getElementById('adminSidebar');
const toggleBtn = document.getElementById('sidebarToggle');
if (toggleBtn) {
  toggleBtn.addEventListener('click', () => sidebar.classList.toggle('open'));
}

// ── Admin Theme Toggle ────────────────────────────────
const adminThemeBtn = document.getElementById('adminTheme');
const html = document.documentElement;
const saved = localStorage.getItem('admin-theme') || 'light';
html.setAttribute('data-theme', saved);
updateAdminIcon();

if (adminThemeBtn) {
  adminThemeBtn.addEventListener('click', () => {
    const next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', next);
    localStorage.setItem('admin-theme', next);
    updateAdminIcon();
  });
}
function updateAdminIcon() {
  if (!adminThemeBtn) return;
  const icon = adminThemeBtn.querySelector('i');
  if (icon) icon.className = html.getAttribute('data-theme') === 'dark' ? 'bi bi-sun' : 'bi bi-moon-stars';
}

// ── Auto-dismiss alerts ───────────────────────────────
document.querySelectorAll('.alert').forEach(el => {
  setTimeout(() => { const b = bootstrap.Alert.getOrCreateInstance(el); if (b) b.close(); }, 4000);
});
