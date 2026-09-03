const CACHE_NAME = "calculadora-ademicon-pwa-v7";
const APP_SHELL = [
  "./",
  "./index.html",
  "./manifest.webmanifest",
  "./pwa-register.js",
  "./icon-192.png",
  "./icon-512.png"
];

self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(APP_SHELL))
  );
  self.skipWaiting();
});

self.addEventListener("activate", event => {
  event.waitUntil(
    Promise.all([
      caches.keys().then(keys => Promise.all(
        keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
      )),
      self.clients.claim()
    ])
  );
});

self.addEventListener("fetch", event => {
  const request = event.request;
  if (request.method !== "GET") return;

  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;

  // Navegação: internet primeiro. Isso evita que o app fique preso em um HTML antigo.
  // Se estiver offline, usa a última versão salva no aparelho.
  if (request.mode === "navigate") {
    event.respondWith(
      fetch(request)
        .then(response => {
          if (response && response.ok) {
            const copy = response.clone();
            caches.open(CACHE_NAME).then(cache => {
              cache.put("./index.html", copy.clone());
              cache.put("./", copy);
            });
          }
          return response;
        })
        .catch(async () => {
          return (await caches.match("./index.html")) ||
                 (await caches.match("./")) ||
                 Response.error();
        })
    );
    return;
  }

  // Arquivos estáticos: usa cache imediatamente e atualiza em segundo plano.
  event.respondWith(
    caches.match(request).then(cached => {
      const networkUpdate = fetch(request)
        .then(response => {
          if (response && response.ok) {
            caches.open(CACHE_NAME).then(cache => cache.put(request, response.clone()));
          }
          return response;
        })
        .catch(() => null);

      return cached || networkUpdate || caches.match("./index.html");
    })
  );
});
