/**
 * autofit.js — 內容自動縮放塞進安全框（選配，與「偵測爆框」相對的另一種策略）
 *
 * 原理：每個 .slide-frame 內容包進一層 .autofit；量內容自然尺寸 vs 安全框，
 *   若超出就對 .autofit 套 transform:scale(<1) 等比縮小，直到剛好塞進框內。
 *   螢幕尺寸改變（cqw 變）時自動重算，所以「螢幕自適應」與「內容自適應」並存。
 *
 * ⚠ 取捨：這會讓塞太多的頁字級被縮小，可能低於「≥2vw」可讀底線。
 *   它解決「不爆框」，但不保證「好讀」。內容該砍還是要砍——auto-fit 是安全網，不是藉口。
 *
 * 用法：HTML 末尾加 <script src="../autofit.js"></script>（放在 presenter.js 之後）。
 */
(function () {
  function fitOne(frame) {
    // 第一次：把 frame 既有子節點搬進 .autofit 包裝層
    let fit = frame.querySelector(':scope > .autofit');
    if (!fit) {
      fit = document.createElement('div');
      fit.className = 'autofit';
      fit.style.cssText = 'transform-origin:top left;display:flex;flex-direction:column;width:100%;';
      while (frame.firstChild) fit.appendChild(frame.firstChild);
      frame.appendChild(fit);
    }
    // 量自然尺寸前先還原
    fit.style.transform = 'none';
    fit.style.width = '100%';
    fit.style.height = 'auto';
    const fw = frame.clientWidth, fh = frame.clientHeight;
    if (!fw || !fh) return;
    const cw = fit.scrollWidth, ch = fit.scrollHeight;
    const scale = Math.min(1, fw / cw, fh / ch);
    if (scale < 1) {
      // 縮小：寬度先放大成 1/scale，縮放後剛好等於框寬（避免縮完右側留大白邊、行又重排）
      fit.style.width = (100 / scale) + '%';
      fit.style.transform = 'scale(' + scale + ')';
    }
    fit.dataset.fitScale = scale.toFixed(3);
  }

  function fitAll() {
    document.querySelectorAll('.slide-frame').forEach(fitOne);
  }

  let t;
  function schedule() { clearTimeout(t); t = setTimeout(fitAll, 60); }

  // 字型載入會改變文字度量，等 fonts ready 再算；不支援就退回 load
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(fitAll);
  }
  window.addEventListener('load', schedule);
  window.addEventListener('resize', schedule);   // 螢幕尺寸變 → cqw 變 → 重新塞
})();
