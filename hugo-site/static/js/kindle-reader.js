(function () {
  'use strict';

  // ===== 自动生成目录 =====
  function buildTOC() {
    var tocEl = document.getElementById('toc');
    if (!tocEl) return;

    var content = document.querySelector('.kindle-article-content');
    if (!content) return;

    var headings = content.querySelectorAll('h2, h3, h4');
    if (headings.length < 2) return;

    var title = document.createElement('div');
    title.className = 'kindle-article-toc-title';
    title.textContent = '目录';
    tocEl.appendChild(title);

    var ul = document.createElement('ul');

    headings.forEach(function (heading, i) {
      if (!heading.id) {
        heading.id = 'toc-' + i;
      }
      var li = document.createElement('li');
      li.className = 'toc-' + heading.tagName.toLowerCase();
      var a = document.createElement('a');
      a.href = '#' + heading.id;
      a.textContent = heading.textContent;
      li.appendChild(a);
      ul.appendChild(li);
    });

    tocEl.appendChild(ul);
  }

  // ===== 书签功能 =====
  var BOOKMARK_KEY = 'angelife_bookmarks';

  function getBookmarks() {
    try {
      return JSON.parse(localStorage.getItem(BOOKMARK_KEY)) || [];
    } catch (e) {
      return [];
    }
  }

  function saveBookmarks(bookmarks) {
    try {
      localStorage.setItem(BOOKMARK_KEY, JSON.stringify(bookmarks));
    } catch (e) {}
  }

  function addBookmark() {
    var url = window.location.href;
    var title = document.title;
    var bookmarks = getBookmarks();

    // 去重
    for (var i = 0; i < bookmarks.length; i++) {
      if (bookmarks[i].url === url) return;
    }

    bookmarks.unshift({ url: url, title: title, time: Date.now() });
    if (bookmarks.length > 20) bookmarks = bookmarks.slice(0, 20);
    saveBookmarks(bookmarks);
    renderBookmarks();
  }

  function removeBookmark(url) {
    var bookmarks = getBookmarks().filter(function (b) { return b.url !== url; });
    saveBookmarks(bookmarks);
    renderBookmarks();
  }

  function renderBookmarks() {
    var bar = document.getElementById('bookmark-bar');
    if (!bar) return;

    var bookmarks = getBookmarks();
    bar.innerHTML = '';

    if (bookmarks.length === 0) return;

    var label = document.createElement('span');
    label.className = 'kindle-bookmark-label';
    label.textContent = '书签：';
    bar.appendChild(label);

    bookmarks.forEach(function (b) {
      var a = document.createElement('a');
      a.className = 'kindle-bookmark-item';
      a.href = b.url;
      a.textContent = b.title.replace(/ \|.*$/, '').replace(/ -.*$/, '');
      bar.appendChild(a);
    });
  }

  function initBookmarks() {
    // 在文章页添加书签按钮
    var article = document.querySelector('.kindle-article');
    if (!article) return;

    var nav = article.querySelector('.kindle-article-nav');
    if (!nav) return;

    var btn = document.createElement('button');
    btn.className = 'kindle-bookmark-add';
    btn.textContent = '+ 收藏本文';
    btn.onclick = addBookmark;
    nav.insertBefore(btn, nav.firstChild);
  }

  // ===== 初始化 =====
  document.addEventListener('DOMContentLoaded', function () {
    buildTOC();
    initBookmarks();
    renderBookmarks();
  });
})();
