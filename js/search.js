document.addEventListener('DOMContentLoaded', function() {
  var input = document.getElementById('search-input');
  var results = document.getElementById('results');
  if (!input || !results) return;

  var indexUrl = '/index.json';
  var entries = [];

  fetch(indexUrl)
    .then(function(r) { return r.json(); })
    .then(function(data) {
      (data.pages || data).forEach(function(p) {
        entries.push({
          title: p.title,
          summary: p.summary || '',
          url: p.permalink || p.url
        });
      });
    })
    .catch(function(err) { console.error('Search index load failed', err); });

  function fuzzyMatch(text, query) {
    if (!query) return true;
    text = (text || '').toLowerCase();
    query = query.toLowerCase();
    return text.indexOf(query) !== -1;
  }

  function displayResults(matches) {
    if (matches.length === 0) {
      results.innerHTML = '<p style="color:#888;text-align:center;margin-top:1em;">没有找到匹配的文章</p>';
      return;
    }
    var html = '<ul class="post-archive">';
    matches.forEach(function(m) {
      html += '<li class="post-item">' +
        '<a class="post-title" href="' + m.url + '">' + m.title + '</a>' +
        '</li>';
    });
    html += '</ul>';
    results.innerHTML = html;
  }

  input.addEventListener('input', function() {
    var q = input.value.trim();
    if (q.length === 0) { results.innerHTML = ''; return; }
    var matches = entries.filter(function(e) {
      return fuzzyMatch(e.title, q) || fuzzyMatch(e.summary, q);
    }).slice(0, 30);
    displayResults(matches);
  });
});
