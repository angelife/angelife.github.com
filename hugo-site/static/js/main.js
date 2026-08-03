document.addEventListener('DOMContentLoaded', () => {
  const KEY = 'theme';
  const root = document.documentElement;
  const btn = document.getElementById('theme-toggle');

  // Sync button to current dataset state
  const syncBtn = () => {
    if (!btn) return;
    const dark = root.dataset.theme === 'dark';
    btn.textContent = dark ? '☀️' : '🌙';
    btn.setAttribute('aria-pressed', dark);
    btn.setAttribute('aria-label', dark ? '深色模式 — 点击切换' : '浅色模式 — 点击切换');
  };

  // Toggle click: flip theme & persist
  if (btn) {
    btn.addEventListener('click', () => {
      const next = root.dataset.theme === 'dark' ? 'light' : 'dark';
      root.dataset.theme = next;
      root.dataset.themePref = next;
      try { localStorage.setItem(KEY, next); } catch {}
      syncBtn();
    });
  }

  // System colour-scheme change — only when user hasn't saved a preference
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    const saved = (() => { try { return localStorage.getItem(KEY); } catch {} })();
    if (saved) return;
    root.dataset.theme = e.matches ? 'dark' : 'light';
    root.dataset.themePref = 'system';
    syncBtn();
  });

  // Initial sync (inline boot script already set dataset; sync button to match)
  syncBtn();

  // Progressive enhancements (non-theme, keep as-is)
  document.querySelectorAll('img').forEach(img => {
    if (!img.hasAttribute('loading')) img.setAttribute('loading', 'lazy');
    img.setAttribute('decoding', 'async');
  });
  document.querySelectorAll('a[target="_blank"]:not([rel])').forEach(link => {
    link.setAttribute('rel', 'noopener noreferrer');
  });
});
