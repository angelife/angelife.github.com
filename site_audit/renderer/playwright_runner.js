const { chromium } = require('playwright');

const args = JSON.parse(process.argv[2]);
const action = args.action;

(async () => {
  const browser = await chromium.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-gpu']
  });

  try {
    if (action === 'screenshot') {
      const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
      await page.goto(args.url, { waitUntil: 'domcontentloaded', timeout: 15000 });
      await page.screenshot({ path: args.output, fullPage: args.fullPage || false });
      console.log(JSON.stringify({ ok: true, path: args.output }));
    }
    else if (action === 'overflow') {
      const page = await browser.newPage({ viewport: { width: 375, height: 812 } });
      await page.goto(args.url, { waitUntil: 'networkidle', timeout: 15000 });
      const overflows = await page.evaluate(() => {
        const docW = document.documentElement.offsetWidth;
        const items = [];
        document.querySelectorAll('*').forEach(el => {
          const ow = el.offsetWidth;
          if (ow > docW && !['script','style','svg','pre','code'].includes(el.tagName.toLowerCase())) {
            items.push({
              tag: el.tagName, id: el.id || '', className: (el.className && typeof el.className === 'string') ? el.className : '',
              width: ow, text: (el.textContent || '').trim().substring(0, 60)
            });
          }
        });
        return items.slice(0, 20);
      });
      const result = { ok: true, overflows };
      if (args.screenshot && overflows.length > 0) {
        await page.screenshot({ path: args.screenshot, fullPage: true });
        result.screenshot = args.screenshot;
      }
      console.log(JSON.stringify(result));
    }
    else if (action === 'contrast') {
      const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
      await page.goto(args.url, { waitUntil: 'networkidle', timeout: 15000 });
      const issues = await page.evaluate(() => {
        const content = document.querySelector('article, .post-content, .entry-content, main, .content, #content, body');
        if (!content) return [];
        const tags = 'p, h1, h2, h3, h4, h5, h6, li, span, a, td, th, label, blockquote, figcaption';
        const results = [];
        content.querySelectorAll(tags).forEach(el => {
          if (['script','style','svg','pre','code'].includes(el.tagName.toLowerCase())) return;
          const text = (el.textContent || '').trim();
          if (text.length < 3) return;
          const cs = window.getComputedStyle(el);
          const fg = cs.color;
          const bg = cs.backgroundColor;
          const fontSize = cs.fontSize;
          results.push({ tag: el.tagName, text: text.substring(0, 80), color: fg, bg: bg, fontSize: fontSize });
        });
        return results.slice(0, 100);
      });
      console.log(JSON.stringify({ ok: true, issues }));
    }
    else if (action === 'pages') {
      const page = await browser.newPage();
      let urls = [];

      // Try sitemap
      try {
        await page.goto(args.baseUrl + '/sitemap.xml', { waitUntil: 'domcontentloaded', timeout: 10000 });
        const locs = await page.evaluate(() =>
          [...document.querySelectorAll('loc')].map(l => l.textContent.trim())
        );
        urls = locs.filter(u => u.startsWith(args.baseUrl));
      } catch(e) {
        // sitemap may not exist
      }

      // Also try public directory scan (for local Hugo)
      if (urls.length === 0) {
        try {
          await page.goto(args.baseUrl, { waitUntil: 'domcontentloaded', timeout: 10000 });
          await new Promise(r => setTimeout(r, 2000));
          urls = await page.evaluate((baseUrl) => {
            const links = [...document.querySelectorAll('a[href]')];
            const seen = new Set();
            return links
              .map(a => a.href.split('#')[0].replace(/\/$/, ''))
              .filter(h => h.startsWith(baseUrl) && !seen.has(h) && seen.add(h));
          }, args.baseUrl);
        } catch(e) {}
      }

      const unique = [...new Set(urls.map(u => u.replace(/\/$/, '')))];
      console.log(JSON.stringify({ ok: true, urls: unique.slice(0, args.maxPages || 100) }));
    }
    else if (action === 'html') {
      const page = await browser.newPage();
      await page.goto(args.url, { waitUntil: 'domcontentloaded', timeout: 10000 });
      await new Promise(r => setTimeout(r, 1000));
      const html = await page.content();
      console.log(JSON.stringify({ ok: true, html: html.substring(0, 5000) }));
    }
    else {
      console.log(JSON.stringify({ ok: false, error: 'unknown action: ' + action }));
    }
  } catch(e) {
    console.log(JSON.stringify({ ok: false, error: e.message }));
  } finally {
    await browser.close();
  }
})();
