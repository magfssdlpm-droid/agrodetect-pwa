// Service Worker para AgroDetect PWA
// Permite funcionar offline y mejorar rendimiento

const CACHE_NAME = 'agrodetect-v1.0.0';
const MODEL_CACHE = 'agrodetect-model-v1';

// Archivos que se cachearán al instalar
const urlsToCache = [
  '/',
  '/manifest.json',
  '/logo.png'
];

// INSTALACIÓN - Cachear recursos básicos
self.addEventListener('install', (event) => {
  console.log('[SW] Instalando Service Worker...');
  
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('[SW] Cacheando recursos iniciales');
        return cache.addAll(urlsToCache);
      })
      .then(() => {
        console.log('[SW] ✅ Service Worker instalado correctamente');
        return self.skipWaiting();
      })
      .catch((error) => {
        console.error('[SW] ❌ Error en instalación:', error);
      })
  );
});

// ACTIVACIÓN - Limpiar cachés viejos
self.addEventListener('activate', (event) => {
  console.log('[SW] Activando Service Worker...');
  
  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => {
            if (cacheName !== CACHE_NAME && cacheName !== MODEL_CACHE) {
              console.log('[SW] Eliminando caché viejo:', cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      })
      .then(() => {
        console.log('[SW] ✅ Service Worker activado');
        return self.clients.claim();
      })
  );
});

// FETCH - Estrategia de red primero, luego caché
self.addEventListener('fetch', (event) => {
  // Ignorar requests que no sean HTTP/HTTPS
  if (!event.request.url.startsWith('http')) {
    return;
  }

  event.respondWith(
    fetch(event.request)
      .then((response) => {
        // Si la respuesta es válida, cachearla
        if (response && response.status === 200) {
          const responseClone = response.clone();
          
          caches.open(CACHE_NAME)
            .then((cache) => {
              cache.put(event.request, responseClone);
            })
            .catch((error) => {
              console.error('[SW] Error guardando en caché:', error);
            });
        }
        
        return response;
      })
      .catch(() => {
        // Si falla la red, intentar obtener de caché
        return caches.match(event.request)
          .then((cachedResponse) => {
            if (cachedResponse) {
              console.log('[SW] Sirviendo desde caché:', event.request.url);
              return cachedResponse;
            }
            
            // Si no está en caché y no hay red, mostrar página offline
            return caches.match('/')
              .then((fallbackResponse) => {
                return fallbackResponse || new Response(
                  '<!DOCTYPE html><html><body><h1>🌿 AgroDetect</h1><p>Sin conexión. Por favor verifica tu internet.</p></body></html>',
                  { headers: { 'Content-Type': 'text/html' } }
                );
              });
          });
      })
  );
});

// Mensajes del cliente
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  
  if (event.data && event.data.type === 'CACHE_MODEL') {
    // Cachear modelo si es necesario
    caches.open(MODEL_CACHE)
      .then((cache) => {
        console.log('[SW] Cacheando modelo...');
        // Aquí podrías cachear el modelo .keras si fuera servido por HTTP
      });
  }
});

console.log('[SW] Service Worker de AgroDetect cargado');
