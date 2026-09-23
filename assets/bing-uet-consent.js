/* Microsoft Advertising UET 343274258; honour the existing cookie choice. */
(function () {
  window.uetq = window.uetq || [];
  window.uetq.push('consent', 'default', { ad_storage: 'denied' });
  try {
    if (localStorage.getItem('arl-cookie-consent') === 'granted') {
      window.uetq.push('consent', 'update', { ad_storage: 'granted' });
    }
  } catch (_) {}
  if (typeof window.gtag === 'function') {
    const originalGtag = window.gtag;
    window.gtag = function () {
      if (arguments[0] === 'consent' && arguments[1] === 'update') {
        const choice = arguments[2] && arguments[2].ad_storage === 'granted' ? 'granted' : 'denied';
        window.uetq.push('consent', 'update', { ad_storage: choice });
      }
      return originalGtag.apply(this, arguments);
    };
  }
  (function(w, d, t, u, o) {w[u] = w[u] || [], o.ts = (new Date).getTime();var n = d.createElement(t);n.src = "https://bat.bing.net/bat.js?ti=" + o.ti + ("uetq" != u ? "&q=" + u : ""),n.async = 1, n.onload = n.onreadystatechange = function() {var s = this.readyState;s && "loaded" !== s && "complete" !== s ||(o.q = w[u], w[u] = new UET(o), w[u].push("pageLoad"),n.onload = n.onreadystatechange = null)};var i = d.getElementsByTagName(t)[0];i.parentNode.insertBefore(n, i);})(window, document, "script", "uetq", {ti: "343274258",enableAutoSpaTracking: true});
})();
