/* 호텔서비스 영어 service worker (same plan as lao-app):
   app files in CacheStorage (network first, saved copy after 4 s or offline);
   mp3 clips in IndexedDB ("hoteleng-audio" / store "c", key = file name), filled as they play or by "음성 mp3 내려받기". */
const SHELL = "hoteleng-shell-1.16";
const FILES = ["./", "index.html", "data.js?v=1.16", "app.js?v=1.16", "manifest.webmanifest", "icon-180.png", "icon-192.png", "icon-512.png"];
let _db; const ADB = () => _db || (_db = new Promise((res, rej) => { const r = indexedDB.open("hoteleng-audio", 1); r.onupgradeneeded = () => r.result.createObjectStore("c"); r.onsuccess = () => res(r.result); r.onerror = () => { _db = null; rej(r.error); }; }));
const aget = k => ADB().then(db => new Promise(res => { const q = db.transaction("c").objectStore("c").get(k); q.onsuccess = () => res(q.result || null); q.onerror = () => res(null); })).catch(() => null);
const aput = (k, v) => ADB().then(db => new Promise(res => { const tx = db.transaction("c", "readwrite"); tx.objectStore("c").put(v, k); tx.oncomplete = () => res(true); tx.onerror = tx.onabort = () => res(false); })).catch(() => false);
const mp3 = b => new Response(b, {headers: {"Content-Type": "audio/mpeg", "Content-Length": String(b.byteLength)}});

self.addEventListener("install", e => { e.waitUntil(caches.open(SHELL).then(c => Promise.all(FILES.map(f => fetch(new Request(f, {cache: "reload"})).then(r => { if (r.ok) return c.put(f, r); }).catch(() => {})))).then(() => self.skipWaiting())); });
self.addEventListener("activate", e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k.startsWith("hoteleng-shell-") && k !== SHELL).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener("fetch", e => {
  const u = new URL(e.request.url); if (e.request.method !== "GET" || u.origin !== location.origin) return;
  if (u.pathname.includes("/audio/") && u.pathname.endsWith(".mp3")){
    const k = u.pathname.split("/").pop().slice(0, -4);
    e.respondWith(aget(k).then(b => b ? mp3(b) : fetch(e.request).then(r => { if (r.ok){ const cl = r.clone(); e.waitUntil(cl.arrayBuffer().then(b => aput(k, b)).catch(() => {})); } return r; })));
    return;
  }
  const key = e.request.mode === "navigate" ? "index.html" : e.request;
  const cached = () => caches.open(SHELL).then(c => c.match(key).then(m => m || c.match(key, {ignoreSearch: true})).then(m => m || (e.request.mode === "navigate" ? c.match("index.html") : null)));
  const net = fetch(e.request, {cache: "no-cache"}).then(r => { if (r.ok){ const cl = r.clone(); e.waitUntil(caches.open(SHELL).then(c => c.put(key, cl))); } return r; });
  e.respondWith(new Promise(res => { let done = false; const go = r => { if (!done && r){ done = true; res(r); } };
    const t = setTimeout(() => cached().then(go), 4000);
    net.then(r => { clearTimeout(t); go(r); }).catch(() => { clearTimeout(t); cached().then(m => go(m || Response.error())); }); }));
});
