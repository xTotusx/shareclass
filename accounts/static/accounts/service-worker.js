const CACHE_NAME = 'shareclass-v1';
const urlsToCache = [
  '/',  // landing
  '/auth/', // login / registro
  '/static/accounts/styles.css',
  '/static/accounts/logo.png',
];

// ===== INSTALACIÓN =====
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      console.log('[SW] Cacheando app shell');
      return cache.addAll(urlsToCache);
    })
  );
});

// ===== FETCH =====
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      // Si está en caché → devolverlo (Happy Path)
      if (response) return response;

      // Si no → obtener de red (Unhappy Path)
      return fetch(event.request).catch(() => caches.match('/'));
    })
  );
});

// ===== ACTIVACIÓN =====
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => {
      return Promise.all(
        keys.filter(key => key !== CACHE_NAME)
            .map(key => caches.delete(key))
      );
    })
  );
  console.log('[SW] Activado y cache actualizado');
});

