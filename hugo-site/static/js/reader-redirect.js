(function () {
  'use strict';
  try {
    var path = window.location.pathname;
    var search = window.location.search || "";
    var ua = navigator.userAgent || "";

    // Already on Kindle version, or no Kindle UA
    if (path.indexOf("/kindle/") === 0) return;
    if (!/Kindle|Silk|KFTT|KFOT|KFTB|KFAP|KF[A-Z]+|AmazonWebAppPlatform/i.test(ua)) return;

    // ?normal=1 or ?desktop=1 force desktop view
    if (/[?&](normal|desktop)=1/.test(search)) return;

    // Normalize path
    if (path === "/" || path === "/index.html") {
      window.location.replace("/kindle/");
      return;
    }

    // Hugo post pages → Kindle version
    var m = path.match(/^\/posts\/([^\/]+)\/?$/);
    if (m && m[1]) {
      window.location.replace("/kindle/posts/" + m[1] + "/");
      return;
    }

    // Old-site pages → stay on old-site (Kindle can render simple HTML),
    // but add ?kindle=1 for CSS hint
    if (path.indexOf("/old-site/") === 0) {
      if (search.indexOf("kindle=1") === -1) {
        window.location.replace(path + (search ? search + "&kindle=1" : "?kindle=1"));
      }
      return;
    }
  } catch (e) {
    // silent fail
  }
})();
