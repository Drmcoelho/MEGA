self.addEventListener("install", (event) => {
  event.waitUntil(caches.open("mega-cache-v1").then((c) => c.add("/")));
});

self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches.match(event.request).then((r) => r || fetch(event.request)),
  );
});
