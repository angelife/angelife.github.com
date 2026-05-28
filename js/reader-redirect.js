(function () {
  try {
    var path = window.location.pathname;
    var search = window.location.search || "";
    var ua = navigator.userAgent || "";

    // 已在 /kindle/ 下，不跳转
    if (path.indexOf("/kindle/") === 0) return;

    // ?normal=1 强制图文版，写入 localStorage
    if (/[?&](normal|desktop)=1/.test(search)) {
      try { localStorage.setItem("angelife_view_mode", "normal"); } catch (e) {}
      return;
    }

    // ?reader=1 或 ?kindle=1 强制阅读版
    if (/[?&](reader|kindle)=1/.test(search)) {
      try { localStorage.setItem("angelife_view_mode", "reader"); } catch (e) {}
    }

    // 检查 localStorage 用户偏好
    var saved = null;
    try { saved = localStorage.getItem("angelife_view_mode"); } catch (e) {}

    // 判断 Kindle 设备
    var isKindle =
      /Kindle|Silk|KFTT|KFOT|KFTB|KFAP|KF[A-Z]+|AmazonWebAppPlatform/i.test(ua);

    // 判断移动端
    var isMobile =
      /Mobi|Android|iPhone|iPod|Mobile/i.test(ua) ||
      (window.matchMedia && window.matchMedia("(max-width: 760px)").matches);

    // 非 Kindle 且已保存 normal 模式 → 不跳转
    if (!isKindle && saved === "normal") return;

    // 不是 Kindle 不是手机 也不是 reader 模式 → 不跳转
    if (!(isKindle || isMobile || saved === "reader")) return;

    // 计算跳转目标
    var target = null;

    if (path === "/" || path === "/index.html") {
      target = "/kindle/";
    } else {
      var match = path.match(/^\/posts\/([^\/]+)\/?$/);
      if (match && match[1]) {
        target = "/kindle/posts/" + match[1] + "/";
      }
    }

    // 执行跳转
    if (target && target !== path) {
      window.location.replace(target);
    }
  } catch (e) {
    // 静默失败，不阻塞页面
  }
})();
