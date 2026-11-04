/**
 * autocol.js — 清單型內容「自動分欄」（比縮字更保可讀性的 auto-fit 策略）
 *
 * 對任何標了 data-autocol 的容器：先用 1 欄，量是否爆出 .slide-frame；
 *   爆了就加到 2 欄、3 欄…直到塞得下為止（上限 = data-autocol 的值，預設 4）。
 *   分欄用掉橫向空白，字級維持不變、仍可讀——這是長清單爆框的首選解法。
 *   若加到上限仍爆，交給 autofit.js 縮字當最後手段（兩者可並用，autocol 先跑）。
 *
 * 容器需求：block 流式內容（每個 item 設 break-inside:avoid）。
 *   用法：<div class="...你的清單..." data-autocol="4"> … items … </div>
 *        <script src="../autocol.js"></script>
 */
(function () {
  function fits(el, frame) {
    // 框內所有 row 的底都沒超出安全框底 = 塞得下（比量容器本身可靠，避開多欄平衡誤差）
    const fb = frame.getBoundingClientRect().bottom + 1;
    const rows = el.children;
    for (let i = 0; i < rows.length; i++) {
      if (rows[i].getBoundingClientRect().bottom > fb) return false;
    }
    return true;
  }

  function balanceOne(el) {
    const frame = el.closest('.slide-frame');
    if (!frame) return;
    const maxCols = parseInt(el.dataset.autocol, 10) || 4;
    el.style.columnFill = 'balance';          // 各欄高度盡量平均
    for (let n = 1; n <= maxCols; n++) {
      el.style.columnCount = n;
      if (fits(el, frame)) { el.dataset.colsUsed = n; return; }
    }
    el.dataset.colsUsed = maxCols + '(仍超出→建議拆頁或配 autofit.js)';
  }

  function balanceAll() {
    document.querySelectorAll('[data-autocol]').forEach(balanceOne);
  }

  let t;
  function schedule() { clearTimeout(t); t = setTimeout(balanceAll, 60); }
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(balanceAll);
  window.addEventListener('load', schedule);
  window.addEventListener('resize', schedule);   // 螢幕變 → 重新決定欄數
})();
