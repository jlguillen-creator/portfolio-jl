const CACHE_NAME = 'portfolio-jl-v1';
const ASSETS_TO_CACHE = [
  './',
  './index.html',
  './manifest.json',
  'https://cdn.jsdelivr.net/npm/chart.js@4.4.0'
];

// Instalar service worker y cachear assets
self.addEventListener('install', (event) => {
  console.log('[Service Worker] Instalando...');
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[Service Worker] Cacheando assets');
      return cache.addAll(ASSETS_TO_CACHE).catch((err) => {
        console.log('[Service Worker] Error cacheando:', err);
        // No fallar si algunos assets no están disponibles
      });
    })
  );
  self.skipWaiting(); // Activar inmediatamente
});

// Activar service worker y limpiar caches viejos
self.addEventListener('activate', (event) => {
  console.log('[Service Worker] Activando...');
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            console.log('[Service Worker] Borrando cache viejo:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  self.clients.claim(); // Controlar clientes inmediatamente
});

// Estrategia de cache: Network first, fallback a cache
self.addEventListener('fetch', (event) => {
  // No cachear requests POST
  if (event.request.method !== 'GET') {
    return;
  }

  event.respondWith(
    // Intentar red primero
    fetch(event.request)
      .then((response) => {
        // Si éxito, cachear y devolver
        if (response && response.status === 200) {
          const responseToCache = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseToCache);
          });
        }
        return response;
      })
      .catch(() => {
        // Si falla red, devolver desde cache
        return caches.match(event.request).then((response) => {
          return response || new Response('Offline - No hay datos en cache', {
            status: 503,
            statusText: 'Service Unavailable'
          });
        });
      })
  );
});

// Escuchar mensajes de la app (para forzar actualización)
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});
