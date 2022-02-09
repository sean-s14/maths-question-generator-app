// Base Service Worker implementation.  To use your own Service Worker, set the PWA_SERVICE_WORKER_PATH variable in settings.py
console.log('Templates (old) - serviceworker.js');

var staticCacheName = "django-pwa-v" + new Date().getTime();
var filesToCache = [
    '/offline/',
    '/static/css/django-pwa-app.css',
    '/static/images/icons/icon-72x72.png',
    '/static/images/icons/icon-96x96.png',
    '/static/images/icons/icon-128x128.png',
    '/static/images/icons/icon-144x144.png',
    '/static/images/icons/icon-152x152.png',
    '/static/images/icons/icon-192x192.png',
    '/static/images/icons/icon-384x384.png',
    '/static/images/icons/icon-512x512.png',
    '/static/images/icons/splash-640x1136.png',
    '/static/images/icons/splash-750x1334.png',
    '/static/images/icons/splash-1242x2208.png',
    '/static/images/icons/splash-1125x2436.png',
    '/static/images/icons/splash-828x1792.png',
    '/static/images/icons/splash-1242x2688.png',
    '/static/images/icons/splash-1536x2048.png',
    '/static/images/icons/splash-1668x2224.png',
    '/static/images/icons/splash-1668x2388.png',
    '/static/images/icons/splash-2048x2732.png'
];

// Cache on install
self.addEventListener("install", event => {
    this.skipWaiting();
    event.waitUntil(
        caches.open(staticCacheName)
            .then(cache => {
                return cache.addAll(filesToCache);
            })
            .catch(err => {console.log(err)})
    )
});

// Clear cache on activate
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames
                    .filter(cacheName => (cacheName.startsWith("django-pwa-")))
                    .filter(cacheName => (cacheName !== staticCacheName))
                    .map(cacheName => caches.delete(cacheName))
            );
        })
    );
});

// Serve from Cache
self.addEventListener("fetch", event => {
    console.log('Serving from Cache #1...');
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                console.log('Serving from Cache #2...');
                console.log(caches);
                console.log(response);
                console.log(event.request);
                return response || fetch(event.request);
            })
            .catch( err => {
                console.log('Serving from Cache #3 (offline)...');
                console.log(err);
                return caches.match('/offline/');
            })
    )
});


// NEW
// self.addEventListener('fetch', event => {
//     let requestUrl = new URL(event.request.url);
//       if (requestUrl.origin === location.origin) {
//         if ((requestUrl.pathname === '/')) {
//           event.respondWith(caches.match(''));
//           console.log(caches);
//           console.log(event);
//           console.log('Returning');
//           return;
//         }
//       }
//       event.respondWith(
//         caches.match(event.request)
//           .then(function(response) {
//             console.log(response);
//             console.log(event.request);
//             return response || fetch(event.request);
//           })
//       );
//   });