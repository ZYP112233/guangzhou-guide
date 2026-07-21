// Service Worker for 木子菲儿创业手册
const CACHE_NAME = 'mzfe-handbook-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/daily-data.json',
  '/hero-h1.webp',
  '/hero-h2.webp',
  '/hero-h3.webp',
  '/hero-h4.webp',
  '/hero-v1.webp',
  '/hero-v2.webp',
  '/hero-v3.webp',
  '/hero-v4.webp'
];

// 安装Service Worker
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

// 拦截请求
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // 如果缓存中有，直接返回
        if (response) {
          return response;
        }

        // 否则从网络获取
        return fetch(event.request).then(
          response => {
            // 检查是否是有效的响应
            if(!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }

            // 克隆响应
            const responseToCache = response.clone();

            caches.open(CACHE_NAME)
              .then(cache => {
                cache.put(event.request, responseToCache);
              });

            return response;
          }
        );
      })
  );
});

// 更新Service Worker
self.addEventListener('activate', event => {
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});
