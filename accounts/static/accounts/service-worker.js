const CACHE_NAME = 'shareclass-v1';
const OFFLINE_URL = '/'; // A donde ir si todo falla

// Archivos vitales que queremos guardar sí o sí al instalar
const ASSETS_TO_CACHE = [
  '/', 
  '/home/',
  '/static/accounts/home.css',
  '/static/accounts/perfil.css',
  '/static/accounts/base.css',
  '/static/accounts/sh_logo.png',
  '/static/accounts/shareclass_logo.jpeg',
  '/static/accounts/avatar_pp1.jpeg',
  // CSS de las Apps (Asegúrate de que estas rutas existan en tu static final)
  '/static/libros/libros_home.css',
  '/static/libros/libro_detalle.css',
  '/static/dispositivos/dispositivos_home.css',
  '/static/dispositivos/dispositivo_detalle.css'
];

// 1. INSTALACIÓN: Guardamos los recursos estáticos
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[Service Worker] Pre-cacheando archivos base');
      return cache.addAll(ASSETS_TO_CACHE);
    })
  );
  self.skipWaiting(); // Fuerza al SW a activarse inmediatamente
});

// 2. ACTIVACIÓN: Limpiamos cachés viejas si cambiamos la versión
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cache) => {
          if (cache !== CACHE_NAME) {
            console.log('[Service Worker] Borrando caché vieja:', cache);
            return caches.delete(cache);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// 3. FETCH: La estrategia inteligente
self.addEventListener('fetch', (event) => {
  const requestUrl = new URL(event.request.url);

  // A) ESTRATEGIA PARA IMÁGENES Y ESTÁTICOS (Cache First)
  // Si es un archivo static o una imagen subida (media), busca en caché primero.
  if (requestUrl.pathname.startsWith('/static/') || requestUrl.pathname.startsWith('/media/')) {
    event.respondWith(
      caches.match(event.request).then((cachedResponse) => {
        return cachedResponse || fetch(event.request).then((networkResponse) => {
            return caches.open(CACHE_NAME).then((cache) => {
                // Guardamos en caché lo nuevo que vayamos viendo
                cache.put(event.request, networkResponse.clone());
                return networkResponse;
            });
        });
      })
    );
    return;
  }

  // B) ESTRATEGIA PARA PÁGINAS HTML (Network First)
  // Para ver libros, dispositivos o perfil, intentamos internet primero para tener datos frescos.
  if (event.request.mode === 'navigate') {
    event.respondWith(
      fetch(event.request)
        .then((networkResponse) => {
          return caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, networkResponse.clone());
            return networkResponse;
          });
        })
        .catch(() => {
          // Si no hay internet, devolvemos la versión en caché
          console.log('[Service Worker] Sin conexión. Sirviendo caché para:', event.request.url);
          return caches.match(event.request).then((cachedResponse) => {
             // Si no está en caché (ej: nunca visitaste esa página), podrías redirigir al home
             if (cachedResponse) return cachedResponse;
             return caches.match('/'); 
          });
        })
    );
    return;
  }

  // C) POR DEFECTO: Intenta red, si falla, nada.
  event.respondWith(fetch(event.request));
});