// Cache hors ligne : réseau d'abord, cache en secours.
var C = 'noamdash-test-v13';
var FILES = ['./', './index.html', './apple-touch-icon.png'];
self.addEventListener('install', function (e) {
  e.waitUntil(caches.open(C).then(function (c) { return c.addAll(FILES); }));
  self.skipWaiting();
});
self.addEventListener('activate', function (e) { e.waitUntil(self.clients.claim()); });
self.addEventListener('fetch', function (e) {
  if (e.request.method !== 'GET') return;
  e.respondWith(
    /* la page elle-même : toujours la dernière version (on contourne le cache de 10 min de GitHub Pages) */
    (e.request.mode === 'navigate' ? fetch(e.request.url.split('#')[0].split('?')[0] + '?t=' + Date.now(), {credentials: 'same-origin'}) : fetch(e.request)).then(function (r) {
      var cp = r.clone();
      caches.open(C).then(function (c) { c.put(e.request, cp); });
      return r;
    }).catch(function () {
      return caches.match(e.request).then(function (r) { return r || caches.match('./index.html'); });
    })
  );
});
