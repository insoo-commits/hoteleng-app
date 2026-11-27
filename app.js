const HE_VER = "v1.74";
/* Audio packs in the browser (see tools/audiopack.js): one file per lesson holds all of its clips.
   Opening a lesson loads its pack (from IndexedDB when saved before, else from the network), then every clip of it plays at once
   from memory, as before. A clip from another lesson (search, related lessons) loads that clip's home pack first.
   Packs are kept in IndexedDB (store "c", key "p:" + code, value {h: hash, b: bytes}), next to the single clips that older versions saved
   there (key = clip name); those still play. Same file can be copied to the other apps: makeAudioPack({db: "<their IndexedDB name>"}). */
function makeAudioPack(opt){
  const IDX = window.AUDIO_INDEX || {}, PACKS = window.AUDIO_PACKS || [], base = opt.base || "audio/";
  const byCode = new Map(PACKS.map((p, i) => [p[0], i]));
  const MEM = new Map(), PEND = new Map(), LIMIT = 4000;   // clip name -> blob URL (about 25 MB at most)
  let _db;
  const db = () => _db || (_db = new Promise((res, rej) => { const r = indexedDB.open(opt.db, 1); r.onupgradeneeded = () => r.result.createObjectStore("c");
    r.onsuccess = () => res(r.result); r.onerror = () => { _db = null; rej(r.error); }; }));
  const get = k => db().then(d => new Promise(res => { const q = d.transaction("c").objectStore("c").get(k); q.onsuccess = () => res(q.result || null); q.onerror = () => res(null); })).catch(() => null);
  const put = (k, v) => db().then(d => new Promise(res => { const tx = d.transaction("c", "readwrite"); tx.objectStore("c").put(v, k); tx.oncomplete = () => res(true); tx.onerror = tx.onabort = () => res(false); })).catch(() => false);
  const remember = (k, bytes) => {
    if (MEM.has(k)) return;
    if (MEM.size >= LIMIT){ let n = 0; for (const [x, u] of MEM){ URL.revokeObjectURL(u); MEM.delete(x); if (++n >= 500) break; } }
    MEM.set(k, URL.createObjectURL(new Blob([bytes], {type: "audio/mpeg"})));
  };
  function unpack(buf){
    const n = new DataView(buf).getUint32(0, true), table = JSON.parse(new TextDecoder().decode(new Uint8Array(buf, 4, n))), at = 4 + n;
    for (const [k, o, l] of table) remember(k, new Uint8Array(buf, at + o, l));
  }
  const fetchPack = i => fetch(base + "p/" + PACKS[i][0] + ".bin?h=" + PACKS[i][1]).then(r => { if (!r.ok) throw new Error(r.status); return r.arrayBuffer(); });
  /* load pack i into memory: IndexedDB first, then the network (and keep it in IndexedDB for next time and offline) */
  function load(i){
    if (i == null || !PACKS[i]) return Promise.resolve(false);
    if (PEND.has(i)) return PEND.get(i);
    const [code, h] = PACKS[i];
    const p = get("p:" + code).then(s => s && s.h === h ? s.b : fetchPack(i).then(b => { put("p:" + code, {h, b}); return b; }))
      .then(b => { unpack(b); return true; })
      .catch(() => { PEND.delete(i); return false; });   // failed: try again next time
    PEND.set(i, p); return p;
  }
  return {
    has: k => k in IDX,
    now: k => MEM.get(k) || null,          // ready to play this moment, or null
    /* blob URL of a clip, or null when it cannot be had (then the device voice speaks) */
    url(k){
      if (MEM.has(k)) return Promise.resolve(MEM.get(k));
      if (!(k in IDX)) return Promise.resolve(null);
      return get(k).then(b => { if (b){ remember(k, b); return MEM.get(k); }
        return load(IDX[k]).then(() => MEM.get(k) || null); });
    },
    warm: code => load(byCode.get(code)),   // a lesson is opened: get its clips ready
    count: () => PACKS.length,
    sig: () => PACKS.map(p => p[1]).join("").length ? String(PACKS.length) + ":" + PACKS.reduce((s, p) => (s * 31 + parseInt(p[1], 16)) % 2147483647, 7) : "",
    /* save every pack in IndexedDB for offline use; tick(done, total) */
    async saveAll(tick){
      let i = 0, done = 0, bad = 0; const N = PACKS.length;
      await Promise.all(Array.from({length: 4}, async () => { while (i < N){ const j = i++, [code, h] = PACKS[j];
        try { const s = await get("p:" + code); if (!(s && s.h === h)){ const b = await fetchPack(j); if (!(await put("p:" + code, {h, b}))) bad++; } } catch (e) { bad++; }
        tick(++done, N); } }));
      return bad;
    }
  };
}

/* ---------- HotelEng anonymous usage statistics + public stats page + short survey (RYU 2026-11-27, v1.68) ----------
   Copied from PhasaKAO src/stats.js (itself from JeyCampus). No names, no e-mail: each device gets a random id. Events wait in
   this device's storage and are sent in small batches to RYU's Google Sheet (Apps Script: /mnt/project-files/hotel-english-app/stats/Code.gs).
   Not sent from localhost / file previews. STATS_URL empty = nothing is recorded. */
const STATS_URL = /^https:/.test(location.protocol) && !/^(localhost|127\.)/.test(location.hostname) && !/claude|anthropic/.test(location.hostname) ? "https://script.google.com/macros/s/AKfycbwZNJ6JYJ7GaqgU56WZoAqklaPSX_KnE2viSEPhSdtvfZC3tazNRqRvitklWNiHx5KGdw/exec" : "";   // RYU 2026-11-27: HotelEng sheet
const ST = (() => {
  const QK = "hoteleng-stats", IK = "hoteleng-id", MAX = 400;
  const get = k => { try { return localStorage.getItem(k); } catch (e) { return null; } };
  const put = (k, v) => { try { localStorage.setItem(k, v); } catch (e) {} };
  let id = get(IK);
  if (!id){ id = (crypto.randomUUID ? crypto.randomUUID() : Date.now().toString(36) + Math.random().toString(36).slice(2)).replace(/-/g, "").slice(0, 16); put(IK, id); }
  const ua = navigator.userAgent;
  const os = /iPhone|iPad|iPod/.test(ua) || (/Macintosh/.test(ua) && navigator.maxTouchPoints > 1) ? "iOS" : /Android/.test(ua) ? "Android" : /Windows/.test(ua) ? "Windows" : /Mac OS/.test(ua) ? "Mac" : /CrOS/.test(ua) ? "ChromeOS" : /Linux/.test(ua) ? "Linux" : "other";
  const dev = /iPad/.test(ua) || (os === "iOS" && !/iPhone|iPod/.test(ua)) || (os === "Android" && !/Mobile/.test(ua)) ? "tablet" : /iPhone|iPod|Mobile/.test(ua) ? "phone" : "computer";
  const pwa = matchMedia("(display-mode: standalone)").matches || navigator.standalone === true;
  const load = () => { try { const q = JSON.parse(get(QK) || "[]"); return Array.isArray(q) ? q : []; } catch (e) { return []; } };
  const stamp = () => { const d = new Date(), z = -d.getTimezoneOffset(), p = n => String(Math.abs(n)).padStart(2, "0");
    return d.getFullYear() + "-" + p(d.getMonth() + 1) + "-" + p(d.getDate()) + " " + p(d.getHours()) + ":" + p(d.getMinutes()) + ":" + p(d.getSeconds()) + (z < 0 ? "-" : "+") + p(z / 60 | 0) + ":" + p(z % 60); };
  let busy = false;
  function log(ev, code, a, b){
    if (!STATS_URL) return;
    const q = load(); q.push([stamp(), ev, code || "", a == null ? "" : a, b == null ? "" : b]);
    put(QK, JSON.stringify(q.slice(-MAX)));
  }
  function send(beacon){
    if (!STATS_URL || busy || !navigator.onLine) return;
    const q = load(); if (!q.length) return;
    const n = Math.min(q.length, 100), body = JSON.stringify({id, v: HE_VER, dev, os, pwa, lang: navigator.language || "", ev: q.slice(0, n)});
    const done = () => { const r = load(); put(QK, JSON.stringify(r.slice(n))); };
    if (beacon && navigator.sendBeacon){ if (navigator.sendBeacon(STATS_URL, new Blob([body], {type: "text/plain"}))) done(); return; }
    busy = true;   // text/plain + no-cors: no preflight; the answer cannot be read, a network error rejects
    fetch(STATS_URL, {method: "POST", mode: "no-cors", body, keepalive: body.length < 60000}).then(() => { done(); busy = false; if (load().length) setTimeout(send, 2000); }, () => { busy = false; });
  }
  if (STATS_URL){
    log("open", "", dev, pwa ? "installed" : "browser");
    setTimeout(send, 4000); setInterval(send, 60000);
    addEventListener("online", () => send());
    document.addEventListener("visibilitychange", () => { if (document.visibilityState === "hidden") send(true); });
  }
  let last = "";
  return {log, send, meta: () => ({id, v: HE_VER, dev, os, pwa, lang: navigator.language || ""}), lesson(code){ if (code && code !== last){ last = code; log("lesson", code); } }};
})();

/* ---------- public statistics page (도움말 > 사용 통계, RYU 2026-11-25, v1.3) ----------
   Only totals that the sheet's Apps Script adds up (doGet ?stats=1): no device ids, no single person's scores.
   STATS_PUBLIC false = build.js leaves the page out of the menu. Charts are drawn here as SVG (works offline,
   follows the light / dark colors). The last numbers are kept on the device so the page also opens offline. */
const STATS_PUBLIC = true;   // RYU 2026-11-25: show the stats page (도움말 > 사용 통계)
const STP = (() => {
  const CK = "hoteleng-statspage", NS = "http://www.w3.org/2000/svg";
  const AC = {"1": "var(--k1)", "2": "var(--k2)", "3": "var(--k3)", "4": "var(--k4)", "5": "var(--k5)", "6": "var(--k6)", "7": "var(--k7)", "8": "var(--k8)", "9": "var(--muted)"};
  const PAL = ["var(--k1)", "var(--k2)", "var(--k3)", "var(--k4)", "var(--k6)", "var(--k7)", "var(--k5)", "var(--k8)"];
  const fmt = n => n == null || n === "" ? "–" : Number(n).toLocaleString("en-US");
  function el(tag, at, ...k){ const e = document.createElement(tag);   // own small builder: app.js keeps its h() inside its own scope
    for (const n in at || {}) e.setAttribute(n, at[n]);
    for (const c of k.flat(9)) if (c != null && c !== false) e.append(c.nodeType ? c : String(c));
    return e; }
  function svg(w, hgt, kids){ const s = document.createElementNS(NS, "svg"); s.setAttribute("viewBox", "0 0 " + w + " " + hgt); s.setAttribute("class", "stsvg"); s.setAttribute("role", "img");
    for (const k of kids.flat()) if (k) s.appendChild(k); return s; }
  function sv(tag, at, text){ const e = document.createElementNS(NS, tag); for (const k in at) e.setAttribute(k, at[k]); if (text != null) e.textContent = text; return e; }
  const card = (title, ko, body, wide) => el("section", {class: "stcard" + (wide ? " wide" : "")}, el("h3", null, title, " ", el("span", {class: "ko"}, ko)), body);
  /* bars over time + a line (two series), labels every few columns */
  function timeChart(rows, aName, bName){
    const W = CW, H = Math.round(Math.min(260, Math.max(200, CW * .3))), L = 34, B = 26, T = 12, n = rows.length || 1, bw = (W - L - 8) / n;
    const maxA = Math.max(1, ...rows.map(r => r[1])), maxB = Math.max(1, ...rows.map(r => r[2]));
    const y = (v, m) => T + (H - T - B) * (1 - v / m), k = [];
    for (let g = 0; g <= 4; g++){ const v = Math.round(maxA * g / 4), yy = y(v, maxA); k.push(sv("line", {x1: L, x2: W - 4, y1: yy, y2: yy, class: "stgrid"}), sv("text", {x: L - 6, y: yy + 4, class: "stax", "text-anchor": "end"}, fmt(v))); }
    rows.forEach((r, i) => { const x = L + i * bw, hh = H - B - y(r[1], maxA);
      k.push(sv("rect", {x: x + bw * .15, y: y(r[1], maxA), width: Math.max(1, bw * .7), height: Math.max(0, hh), rx: 2, style: "fill:var(--k1)"}, null));
      k[k.length - 1].appendChild(sv("title", {}, r[0] + " · " + aName + " " + r[1] + " · " + bName + " " + r[2]));
      const step = Math.ceil(n / Math.max(3, Math.floor(CW / 70))); if (i % step === 0 || i === n - 1) k.push(sv("text", {x: x + bw / 2, y: H - 8, class: "stax", "text-anchor": "middle"}, r[0].length > 7 ? r[0].slice(5) : r[0])); });
    const pts = rows.map((r, i) => (L + i * bw + bw / 2) + "," + y(r[2], maxB)).join(" ");
    if (rows.length > 1) k.push(sv("polyline", {points: pts, class: "stline"}));
    rows.forEach((r, i) => k.push(sv("circle", {cx: L + i * bw + bw / 2, cy: y(r[2], maxB), r: rows.length > 40 ? 1.5 : 3, class: "stdot"})));
    return el("div", null, svg(W, H, k), el("div", {class: "stleg"}, el("span", {class: "sw", style: "background:var(--k1)"}), aName, el("span", {class: "sw ln"}), bName + " (오른쪽 눈금, 최대 " + fmt(maxB) + ")"));
  }
  /* horizontal bars: [label, value, color?, sub-label?] */
  function hbars(rows, unit){
    const max = Math.max(1, ...rows.map(r => r[1]));
    return el("div", {class: "sthb"}, rows.map((r, i) => el("div", {class: "sthr"},
      el("div", {class: "sthl"}, el("span", {class: "ko"}, r[0]), r[3] ? el("small", null, r[3]) : null),
      el("div", {class: "stht"}, el("i", {style: "width:" + (100 * r[1] / max).toFixed(1) + "%;background:" + (r[2] || PAL[i % PAL.length])})),
      el("b", null, fmt(r[1]) + (unit || "")))));
  }
  function donut(rows){
    const tot = rows.reduce((s, r) => s + r[1], 0) || 1, R = 70, C = 2 * Math.PI * R, k = []; let off = 0;
    rows.forEach((r, i) => { const len = C * r[1] / tot; k.push(sv("circle", {cx: 100, cy: 100, r: R, class: "stdn", style: "stroke:" + PAL[i % PAL.length], "stroke-dasharray": len + " " + (C - len), "stroke-dashoffset": -off, transform: "rotate(-90 100 100)"})); off += len; });
    k.push(sv("text", {x: 100, y: 98, class: "stdc", "text-anchor": "middle"}, fmt(tot)), sv("text", {x: 100, y: 118, class: "stax", "text-anchor": "middle"}, "학습자"));
    return el("div", {class: "stdnw"}, svg(200, 200, k), el("ul", {class: "stdl"}, rows.map((r, i) => el("li", null, el("span", {class: "sw", style: "background:" + PAL[i % PAL.length]}), r[0] + " ", el("b", null, Math.round(100 * r[1] / tot) + "%"), " (" + fmt(r[1]) + ")"))));
  }
  function vbars(rows, color){
    const W = CW, H = 170, B = 24, T = 16, n = rows.length, bw = (W - 8) / n, max = Math.max(1, ...rows.map(r => r[1])), k = [];
    rows.forEach((r, i) => { const hh = (H - B - T) * r[1] / max, x = 4 + i * bw;
      k.push(sv("rect", {x: x + bw * .12, y: H - B - hh, width: bw * .76, height: hh, rx: 3, style: "fill:" + (color || "var(--k2)")}));
      if (r[1] && n <= 12) k.push(sv("text", {x: x + bw / 2, y: H - B - hh - 4, class: "stax", "text-anchor": "middle"}, fmt(r[1])));
      if (n <= 12 || i % 3 === 0) k.push(sv("text", {x: x + bw / 2, y: H - 7, class: "stax", "text-anchor": "middle"}, r[0])); });
    return svg(W, H, k);
  }
  let CW = 640;   // chart width in px = the card width, so text keeps its size on a computer
  function draw(box, d){
    CW = Math.max(300, Math.min(1100, (box.clientWidth || 640) - 30));
    const t = d.totals || {}, titles = new Map(Object.keys(B).map(c => [c, [B[c].t, B[c].en]])), areaName = new Map(G.map((g, i) => [String(i + 1), g[0]]));
    const tile = (v, ko, sub) => el("div", {class: "sttile"}, el("b", null, v), el("span", null, ko), sub ? el("small", null, sub) : null);
    const kids = [
      el("div", {class: "sttiles"},
        tile(fmt(t.devices), "학습자", "기기 수"), tile(fmt(t.returning), "다시 온 학습자", "2일 이상"),
        tile(fmt(t.lessons), "묶음 열람"), tile(t.perLearner == null ? "–" : t.perLearner, "1인당 묶음"),
        tile(fmt(t.quizzes), "퀴즈 완료"), tile(t.quizAvg == null ? "–" : t.quizAvg + "%", "퀴즈 평균"),
        tile(fmt(t.toeic), "TOEIC 문제 세트", t.toeicAvg == null ? null : "평균 " + t.toeicAvg + "%"), tile(fmt(t.mocks), "모의 면접 질문"),
        tile(fmt(t.plays), "음성 재생")),
      d.daily && d.daily.length ? card("날마다", "학습자 · 묶음 열람", timeChart(d.daily, "학습자", "묶음 열람"), true) : null,
      d.monthly && d.monthly.length > 1 ? card("달마다", "학습자 · 묶음 열람", timeChart(d.monthly, "학습자", "묶음 열람"), true) : null,
      d.top && d.top.length ? card("많이 본 묶음", "Top 10", hbars(d.top.slice(0, 10).map(r => { const ti = titles.get(r[0]); return [ti ? ti[0] : r[0], r[1], AC[r[0].split("-")[0]], (ti && ti[1] ? ti[1] + " · " : "") + r[0]]; })), true) : null,
      d.areas && d.areas.length ? card("메뉴별 열람", "", hbars(d.areas.map(r => [areaName.get(String(r[0])) || r[0], r[1], AC[r[0]]]))) : null,
      d.devices && d.devices.length ? card("기기", "", donut(d.devices.map(r => [{phone: "휴대폰", tablet: "태블릿", computer: "컴퓨터"}[r[0]] || r[0], r[1]]))) : null,
      d.os && d.os.length ? card("운영체제", "", hbars(d.os)) : null,
      d.survey && d.survey.n ? card("만족도 설문", "", el("div", null, el("div", {class: "sttiles"}, tile(fmt(d.survey.n), "응답"), tile(d.survey.avg == null ? "–" : d.survey.avg + " ★", "평균 별점"), tile(d.survey.recPct == null ? "–" : d.survey.recPct + "%", "추천 의향")), vbars(["★1", "★2", "★3", "★4", "★5"].map((l, i) => [l, d.survey.dist[i] || 0]), "var(--k5)")), true) : null,
      d.quizHist && d.quizHist.some(Boolean) ? card("퀴즈 점수 분포", "", vbars(["0–19%", "20–39%", "40–59%", "60–79%", "80–100%"].map((l, i) => [l, d.quizHist[i] || 0]), "var(--good)"), true) : null,
      d.hours && d.hours.some(Boolean) ? card("공부하는 시간", "한국 시간", vbars(d.hours.map((v, i) => [String(i), v]), "var(--k6)"), true) : null,
      el("p", {class: "stnote"}, "업데이트 " + (d.updated || "–") + (d.first ? " · " + d.first + "부터" : "") + ". 이름 없이 모은 전체 합계입니다. 한 사람의 점수는 보이지 않아요.")];
    box.replaceChildren(el("div", {class: "stwrap"}, kids));
  }
  function page(box){ requestAnimationFrame(() => page2(box)); }   // after the page is on screen, so the cards have their width
  function page2(box){
    let old = null; try { old = JSON.parse(localStorage.getItem(CK) || "null"); } catch (e) {}
    if (window.__STATS_DEMO){ draw(box, window.__STATS_DEMO); return; }   // screenshots and tests only
    if (old) draw(box, old); else box.replaceChildren(el("p", {class: "empty"}, STATS_URL ? "통계를 불러오는 중…" : "통계는 앱 주소(hoteleng.pages.dev)에서 볼 수 있어요."));
    if (!STATS_URL) return;
    fetch(STATS_URL + "?stats=1", {cache: "no-store"}).then(r => r.json()).then(d => { if (!d || !d.totals) throw 0; try { localStorage.setItem(CK, JSON.stringify(d)); } catch (e) {} if (box.isConnected) draw(box, d); })
      .catch(() => { if (!old && box.isConnected) box.replaceChildren(el("p", {class: "empty"}, "통계를 불러오지 못했어요. 인터넷에 연결된 뒤 다시 열어 주세요.")); });
  }
  return {page};
})();

/* ---------- short satisfaction survey (RYU 2026-11-25, v1.11) ----------
   Four questions: stars, most helpful menu, recommend to a friend, a free comment. Sent once per device to the same
   Apps Script (sheet "survey"); the public stats page shows only the totals (number of answers, average stars).
   Offered under the 내 학습 card after 5 lessons on 2 different days; "Later" asks again in 3 days; always open in 도움말. */
const SV = (() => {
  const DK = "hoteleng-survey", PK = "hoteleng-svq";
  const get = k => { try { return localStorage.getItem(k); } catch (e) { return null; } };
  const put = (k, v) => { try { localStorage.setItem(k, v); } catch (e) {} };
  function el(tag, at, ...k){ const e = document.createElement(tag);
    for (const a in at || {}) if (at[a] != null){ if (a.startsWith("on")) e.addEventListener(a.slice(2), at[a]); else e.setAttribute(a, at[a]); }
    for (const x of k.flat(9)) if (x != null && x !== false) e.append(x.nodeType ? x : String(x)); return e; }
  const state = () => { try { return JSON.parse(get(DK) || "{}"); } catch (e) { return {}; } };
  const today = () => new Date().toISOString().slice(0, 10);
  function flush(){
    const p = get(PK); if (!p || !STATS_URL || !navigator.onLine) return;
    fetch(STATS_URL, {method: "POST", mode: "no-cors", body: p, keepalive: true}).then(() => put(PK, ""), () => {});
  }
  function form(box, inPage){
    const st = state();
    if (st.done){ box.replaceChildren(el("div", {class: "svcard svdone"},
      el("p", null, el("b", null, "의견 고마워요! "), "앱을 고치는 데 잘 쓸게요."))); return; }
    const a = {stars: 0, menu: "", rec: "", text: ""};
    const menus = G.slice(0, -1).map((g, i) => [String(i + 1), g[0]]);
    const stars = el("div", {class: "svstars", role: "radiogroup", "aria-label": "별점"});
    const more = el("div", {class: "svmore", hidden: ""});
    const chip = (grp, key, val, label) => el("button", {type: "button", class: "svchip", "data-v": val, onclick: ev => { a[key] = val;
      for (const b of grp.querySelectorAll(".svchip")) b.classList.toggle("on", b.dataset.v === val); }}, label);
    for (let i = 1; i <= 5; i++) stars.append(el("button", {type: "button", class: "svstar", "aria-label": i + "점", onclick: () => { a.stars = i;
      stars.querySelectorAll(".svstar").forEach((b, k) => b.classList.toggle("on", k < i)); more.hidden = false; }}, "★"));
    const mg = el("div", {class: "svchips"}); menus.forEach(m => mg.append(chip(mg, "menu", m[0], m[1])));
    const rg = el("div", {class: "svchips"}); [["yes", "네"], ["maybe", "글쎄요"], ["no", "아니요"]].forEach(r => rg.append(chip(rg, "rec", r[0], r[1])));
    const ta = el("textarea", {class: "svtext", maxlength: "300", rows: "3", placeholder: "바라는 점이나 고칠 점 (선택)"});
    const send = () => {
      if (!a.stars) return;
      a.text = ta.value.trim().slice(0, 300);
      const m = ST.meta(); put(PK, JSON.stringify(Object.assign(m, {survey: a})));
      put(DK, JSON.stringify({done: today()})); flush(); form(box, inPage); if (!inPage) setTimeout(() => box.replaceChildren(), 4000);
    };
    more.append(
      el("p", {class: "svq"}, "가장 도움이 된 메뉴는?"), mg,
      el("p", {class: "svq"}, "친구에게 추천할래요?"), rg,
      ta, el("div", {class: "svbtns"}, el("button", {type: "button", class: "btn primary", onclick: send}, "보내기")));
    box.replaceChildren(el("div", {class: "svcard"},
      inPage ? null : el("button", {type: "button", class: "svx", "aria-label": "나중에", title: "나중에", onclick: () => {
        const d = new Date(); d.setDate(d.getDate() + 3); put(DK, JSON.stringify({later: d.toISOString().slice(0, 10)})); box.replaceChildren(); }}, "×"),
      el("div", {class: "svhead"},
        el("p", {class: "svq"}, el("b", null, "HotelEng 어때요? "), "별을 눌러 주세요.")), stars, more));
  }
  /* offer it under the 내 학습 card: seen = lessons opened, days = study days */
  function offer(box, seen, days){
    if (!box || !STATS_URL) return; const st = state();
    if (st.done || (st.later && st.later > today()) || seen < 5 || days < 2){ if (!box.querySelector(".svmore:not([hidden])")) box.replaceChildren(); return; }
    if (!box.firstChild) form(box, false);
  }
  if (STATS_URL){ setTimeout(flush, 5000); addEventListener("online", flush); }
  return {form, offer};
})();

/* 호텔서비스 영어 — app logic. DATA (bundles) and AUD (mp3 clips) are injected by build.py. */
const $ = id => document.getElementById(id), $$ = s => [...document.querySelectorAll(s)];
const ICO = {
  spk: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 5 6 9H3v6h3l5 4z" fill="currentColor"/><path d="M15.5 8.5a5 5 0 0 1 0 7"/><path d="M18.5 5.5a9 9 0 0 1 0 13"/></svg>',
  rep: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="m17 2 4 4-4 4"/><path d="M3 11v-1a4 4 0 0 1 4-4h14"/><path d="m7 22-4-4 4-4"/><path d="M21 13v1a4 4 0 0 1-4 4H3"/></svg>'};
const PSPK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 5 6 9H3v6h3l5 4V5z" fill="currentColor"/><path d="M15.5 8.5a5 5 0 0 1 0 7M18.5 5.5a9 9 0 0 1 0 13"/></svg>';
const PICO = {pause: '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="6" y="5" width="4" height="14" rx="1" fill="currentColor"/><rect x="14" y="5" width="4" height="14" rx="1" fill="currentColor"/></svg>', play: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 5v14l12-7z" fill="currentColor"/></svg>'};
function ico(n){ const s = document.createElement("span"); s.className = "ico"; s.setAttribute("aria-hidden", "true"); s.innerHTML = ICO[n]; return s; }
function h(tag, attrs, ...kids){
  const el = document.createElement(tag);
  if (attrs) for (const [k, v] of Object.entries(attrs)){
    if (v == null || v === false) continue;
    if (k.startsWith("on")) el.addEventListener(k.slice(2), v);
    else if (k === "hidden" || k === "disabled") el[k] = !!v;
    else el.setAttribute(k, v === true ? "" : v);
  }
  for (const c of kids.flat(9)) if (c != null && c !== false && c !== "") el.append(c.nodeType ? c : String(c));
  return el;
}
const spk = () => h("button", {class: "spk", type: "button", "aria-label": "듣기"}, ico("spk"));
const LV = {"하": "초급", "중": "중급", "상": "실무"};
const WHO = {G: "손님", S: "직원", A: "A", B: "B", I: "면접관", C: "지원자"};
const MALE = new Set(["G", "A", "I"]);

/* ---------- data index ---------- */
const G = DATA.g, B = DATA.b;
const ORDER = [];             // every bundle code in app order
G.forEach(g => g[1].forEach(s => s[1].forEach(c => ORDER.push(c))));
const at = new Map(ORDER.map((c, i) => [c, i]));
const gOf = c => +c.split("-")[0], sOf = c => c.split("-").slice(0, 2).join("-");
const HELP = G.length;    // 도움말 is the last menu, with sub-tabs and bundles like the others (kor-app / lao-app)
const HELP0 = G[HELP - 1][1][0][1][0];
const isInfo = c => !!(B[c] && B[c].info);
const isMock = c => !!(B[c] && B[c].mk);

/* ---------- state ---------- */
const LS = "hoteleng-v2";
let S = {code: ORDER[0], mode: "learn", rep: 2, rate: 1, lastA: {}, lastS: {}};
try { Object.assign(S, JSON.parse(localStorage.getItem(LS) || "{}")); } catch (e) {}
if (S.code === "help") S.code = HELP0;
if (!at.has(S.code)) S.code = ORDER[0];
function save(){ try { localStorage.setItem(LS, JSON.stringify(S)); } catch (e) {} }

/* ---------- sound: own mp3 when the build made one, otherwise the device's English voice ----------
   voice codes: m = man (guest, A, interviewer), f = woman (staff, B, candidate, words), f2 / m2 = a second woman / man.
   A bundle's vo map sets a speaker's voice, e.g. {"G": "f2"} when the guest is a woman (RYU 2026-11-23). */
const synth = window.speechSynthesis;
let voices = [];
const loadVoices = () => { if (synth) voices = synth.getVoices().filter(v => /^en[-_](US|GB|AU|CA)/i.test(v.lang)); };
if (synth){ loadVoices(); synth.onvoiceschanged = loadVoices; }
/* device voices: a man's voice for m, a woman's for f (US first, then any English); a second voice for m2 / f2.
   When the device has no man's voice (e.g. only "Google US English"), the pitch is lowered so A and B still sound different. */
const FEM_RE = /female|samantha|jenny|aria|zira|ava|allison|susan|karen|emma|michelle|victoria|moira|tessa|fiona|serena|nicky|joelle|kathy|shelley|sandy|flo|google us english|libby|sonia|natasha|hazel|catherine/i,
      MAL_RE = /\bmale\b|guy|david|alex|daniel|tom\b|aaron|mark|andrew|brian|christopher|eric|ryan|rishi|arthur|oliver|gordon|reed|rocko|eddy|evan|nathan|ralph|albert|junior|grandpa|lee\b|thomas|james|william|george|google uk english male/i;
function voiceList(code){
  const us = voices.filter(v => /en[-_]US/i.test(v.lang));
  const isF = x => FEM_RE.test(x.name) && !/\bmale\b/i.test(x.name.replace(/female/i, "")), isM = x => MAL_RE.test(x.name) && !/female/i.test(x.name);
  const want = code[0] === "m" ? isM : isF;
  const L = us.filter(want).concat(voices.filter(x => !/en[-_]US/i.test(x.lang)).filter(want));
  return L;
}
/* a lower pitch makes many phone engines speak slower too (RYU: the man was much slower), so the pitch only goes down a little
   and the rate goes up a little to match; some men's voices are slow on their own */
const SLOW_RE = /google uk english male|\bfred\b|\bdaniel\b|\brishi\b/i;
function pickVoice(code){
  if (!voices.length) return {v: null, pitch: code[0] === "m" ? 0.85 : code[1] === "2" ? 1.15 : 1, rate: code[0] === "m" ? 1.12 : 1};
  const L = voiceList(code), i = code[1] === "2" ? 1 : 0;
  if (L.length){ const v = L[i] || L[0]; return {v, pitch: L[i] ? 1 : code[0] === "m" ? 0.88 : 1.12, rate: (L[i] ? 1 : code[0] === "m" ? 1.08 : 1) * (SLOW_RE.test(v.name) ? 1.12 : 1)}; }
  // no voice of that sex on this device: use what there is, with a lower (man) or higher (second woman) pitch
  const any = voiceList(code[0] === "m" ? "f" : "m")[0] || voices.find(v => /en[-_]US/i.test(v.lang)) || voices[0];
  return {v: any, pitch: code[0] === "m" ? 0.85 : 1.15, rate: code[0] === "m" ? 1.12 : 1};
}
const vOf = (b, who) => (b && b.vo && b.vo[who]) || (MALE.has(who) ? "m" : "f");
const clipKey = (t, v) => v + "|" + t.trim();
const AEL = new Audio();
/* audio packs (RYU 2026-11-25: "묶음마다 묶어서 개수를 줄여서", like kor-app v2.65): on the site AUD[key] = "<clip id>.<home pack number>" and the
   clips of one bundle come in one file audio/p/<code>.bin (audiopack.js, kept in IndexedDB "hoteleng-audio"). The preview has data: URIs instead. */
window.AUDIO_PACKS = typeof APK !== "undefined" ? APK : [];
window.AUDIO_INDEX = {}; for (const k in AUD){ const u = AUD[k]; if (u.slice(0, 5) !== "data:"){ const i = u.indexOf("."); window.AUDIO_INDEX[u.slice(0, i)] = +u.slice(i + 1); } }
const AP = makeAudioPack({db: "hoteleng-audio"});
/* phones (iPhone above all) only let a page play sound that starts from a tap: the first tap plays a short silent mp3 on the
   same audio element, so later clips that start after a pause can play too (RYU 2026-11-23: no sound on the phone) */
const SILENT = "data:audio/mpeg;base64,SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjYwLjE2LjEwMAAAAAAAAAAAAAAA//NYwAAAAAAAAAAAAEluZm8AAAAPAAAABwAAAqwAXl5eXl5eXl5eXl5eXl55eXl5eXl5eXl5eXl5eZSUlJSUlJSUlJSUlJSUr6+vr6+vr6+vr6+vr6+vysrKysrKysrKysrKysrl5eXl5eXl5eXl5eXl5f//////////////////AAAAAExhdmM2MC4zMQAAAAAAAAAAAAAAACQEIAAAAAAAAAKsXdbMjQAAAAAAAAAAAAAA//MoxAAAAANIAAAAAExBTUUzLjEwMFVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVMQU1FMy4xMDBVVVVVVVVVVVVV//MoxDsAAANIAAAAAFVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVMQU1FMy4xMDBVVVVVVVVVVVVV//MoxHYAAANIAAAAAFVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVMQU1FMy4xMDBVVVVVVVVVVVVV//MoxLEAAANIAAAAAFVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV//MoxMQAAANIAAAAAFVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV//MoxMQAAANIAAAAAFVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV//MoxMQAAANIAAAAAFVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV";
let unlocked = false;
function unlockAudio(){
  if (unlocked) return; unlocked = true;
  try { if (!AEL.src || AEL.paused){ AEL.src = SILENT; const pr = AEL.play(); if (pr && pr.catch) pr.catch(e => { if (e && e.name === "NotAllowedError") unlocked = false; }); } } catch (e) { unlocked = false; }
  try { if (synth){ const u = new SpeechSynthesisUtterance(" "); u.volume = 0; synth.speak(u); } } catch (e) {}
}
["touchend", "click", "keydown"].forEach(t => document.addEventListener(t, unlockAudio, {capture: true, passive: true}));
let P = {tok: 0, mode: null, paused: false, hold: false, skip: 0}, CUR_END = null;
const sleep = ms => new Promise(r => setTimeout(r, ms));
/* background play (RYU 2026-11-24: keep playing with the app in the background or the screen off): phones stop a page's
   timers once its sound stops, so the pauses between sentences play the silent mp3 in a loop on the same audio element
   and end on its timeupdate as well as on a timer; the sound never stops while a bundle plays */
function gap(ms){
  if (!P.mode) return sleep(ms);
  return new Promise(r => {
    const t0 = Date.now(); let fin = false, to = 0;
    const end = () => { if (fin) return; fin = true; clearTimeout(to); AEL.ontimeupdate = null; if (AEL.src === SILENT){ AEL.loop = false; if (!P.mode) AEL.pause(); } r(); };
    to = setTimeout(end, ms);
    try { AEL.onended = AEL.onerror = null; AEL.ontimeupdate = () => { if (Date.now() - t0 >= ms) end(); }; if (AEL.src !== SILENT) AEL.src = SILENT; AEL.loop = true; AEL.playbackRate = 1; const pr = AEL.play(); if (pr && pr.catch) pr.catch(() => {}); } catch (e) {}
  });
}
function quiet(){ if (synth) try { synth.cancel(); if (synth.paused) synth.resume(); } catch (e) {} try { AEL.onended = AEL.onerror = null; AEL.loop = false; AEL.pause(); } catch (e) {} const f = CUR_END; CUR_END = null; if (f) f(); }
function speakOne(text, v){
  return new Promise(res => {
    const done = () => { if (CUR_END === done) CUR_END = null; res(); };
    CUR_END = done;
    const src = AUD[clipKey(text, v)];
    if (src){
      const play = url => { if (CUR_END !== done) return; if (!url) return tts();
        AEL.ontimeupdate = null; AEL.loop = false; AEL.src = url; AEL.playbackRate = +S.rate || 1; AEL.onended = AEL.onerror = done; AEL.play().catch(done); };
      if (src.slice(0, 5) === "data:") return play(src);
      const id = src.slice(0, src.indexOf(".")), now = AP.now(id);
      if (now) return play(now);
      /* the pack is not in memory yet: keep the player going with the silent mp3 (a phone lets sound start only from the tap,
         and stops a page whose sound stops), then play the clip when the pack arrives; the device voice if it cannot be had */
      try { AEL.onended = AEL.onerror = null; AEL.ontimeupdate = null; if (AEL.src !== SILENT) AEL.src = SILENT; AEL.loop = true; AEL.playbackRate = 1; const pr = AEL.play(); if (pr && pr.catch) pr.catch(() => {}); } catch (e) {}
      AP.url(id).then(play, () => play(null)); return;
    }
    tts();
   function tts(){
    if (!synth){ setTimeout(done, 400); return; }
    const u = new SpeechSynthesisUtterance(text); u.lang = "en-US"; u.rate = +S.rate || 1;
    /* Chrome can drop an utterance it has garbage-collected and never send onend, which stopped repeats:
       keep a reference, and go on anyway once the line must have finished */
    window.__utt = u;
    const est = 2500 + text.length * 110 / (+S.rate || 1);
    let wd = setTimeout(function tick(){ if (CUR_END !== done) return; if (P.paused || synth.speaking && !synth.paused && Date.now() - t0 < est * 2) { wd = setTimeout(tick, 500); return; } done(); }, est); const t0 = Date.now();
    const pk = pickVoice(v); if (pk.v) u.voice = pk.v; u.pitch = pk.pitch; u.rate = Math.min(2, (+S.rate || 1) * (pk.rate || 1));
    u.onend = u.onerror = done; synth.speak(u);
   }
  });
}
async function waitPause(tok){ while (P.paused && tok === P.tok) await sleep(150); return tok === P.tok; }
async function say(tok, text, v){ if (tok !== P.tok) return false; await speakOne(text, v || "f"); return waitPause(tok); }
/* bottom bar: [menu-sub-bundle/bundles in the sub] sentence/sentences · text, like lao-app (RYU 2026-11-23) */
function showPlayer(t, i, n){
  $("player").hidden = false; document.body.classList.add("has-player");
  const c = S.code, nb = (G[gOf(c) - 1][1].find((x, j) => gOf(c) + "-" + String(j + 1).padStart(2, "0") === sOf(c)) || [0, []])[1].length;
  const sp = h("span", {class: "pspk", "aria-hidden": "true"}); sp.innerHTML = PSPK;
  $("pt").replaceChildren(sp, h("span", {class: "pw"}, "[" + c + "/" + String(nb).padStart(2, "0") + "]" + (n ? " " + i + "/" + n : "")), " · " + t);
  mediaInfo(t, c);
}
/* lock screen / notification: what is playing, with play·pause, previous·next sentence (RYU 2026-11-24) */
let MS_ON = false;
function mediaInfo(t, c){
  const ms = navigator.mediaSession; if (!ms) return;
  try {
    const b = B[c] || {};
    ms.metadata = new MediaMetadata({title: t, artist: (b.t || "") + " · " + c, album: "호텔서비스 영어", artwork: [{src: "icon-192.png", sizes: "192x192", type: "image/png"}, {src: "icon-512.png", sizes: "512x512", type: "image/png"}]});
    ms.playbackState = P.paused ? "paused" : "playing";
    if (MS_ON) return; MS_ON = true;
    const H = [["play", () => { if (P.paused || P.hold) togglePause(); }], ["pause", () => { if (!P.paused) togglePause(); }],
      ["previoustrack", () => skipBy(-1)], ["nexttrack", () => skipBy(1)], ["stop", () => stopPlay()]];
    for (const [a, f] of H) try { ms.setActionHandler(a, f); } catch (e) {}
  } catch (e) {}
}
function pauseLabel(){ const b = $("ppause"); if (!b) return; const go = P.paused || (P.hold && P.els && P.els.length > 1 && !LINE);
  b.querySelector(".bt").textContent = P.paused ? "재개" : go ? "계속" : "일시정지"; b.querySelector(".pico").innerHTML = go ? PICO.play : PICO.pause; }
function stopPlay(){ LINE = null; if (GRP){ GRP.classList.toggle("on", false); GRP = null; } const cr = document.getElementById("ctlrep"); if (cr) delete cr.dataset.on; P.tok++; P.mode = null; P.paused = false; P.hold = false; P.skip = 0; quiet(); $$(".now").forEach(x => x.classList.remove("now")); $("player").hidden = true; document.body.classList.remove("has-player"); pauseLabel(); try { if (navigator.mediaSession) navigator.mediaSession.playbackState = "none"; } catch (e) {} }
function togglePause(){
  if (!P.mode) return;
  if (P.hold && P.els && P.els.length > 1 && !LINE){ P.hold = false; P.skip = 1; if (P.paused){ P.paused = false; } quiet(); pauseLabel(); return; }   // release the held sentence, go on
  P.paused = !P.paused;
  try {
    if (P.paused){ if (AEL.src && !AEL.paused) AEL.pause(); else if (synth) synth.pause(); }
    else { if (AEL.src && AEL.paused && CUR_END && !AEL.ended) AEL.play().catch(() => {}); if (synth) synth.resume(); }
  } catch (e) {}
  pauseLabel(); try { if (navigator.mediaSession) navigator.mediaSession.playbackState = P.paused ? "paused" : "playing"; } catch (e) {}
}
/* ← →: previous / next line while a bundle plays */
function skipBy(d){ if (P.mode !== "seq") return; P.hold = false; P.skip = d; if (P.paused){ P.paused = false; pauseLabel(); } quiet(); }
/* what one element says, in order: [[voice, text], …] */
function segs(el){
  if (el.dataset.seq) return JSON.parse(el.dataset.seq);
  const out = [[el.dataset.v || "f", el.dataset.say]];
  if (el.dataset.say2) out.push([el.dataset.v2 || "f", el.dataset.say2]);
  return out;
}
const nextCode = () => { const c = ORDER[at.get(S.code) + 1]; return c && !isInfo(c) && !isMock(c) ? c : undefined; };
function chainOn(){ const nx = nextCode(); if (!nx){ stopPlay(); return; } go(nx); gap(500).then(() => playBundle(true)); }
/* plays elements in order, each S.rep times (Enter: the current one without end); chain = go on to the next bundles (C) */
/* keep the sentence being read in view: when it reaches the bottom 10% of the screen (or is above it),
   scroll so it sits about 10% from the top (RYU 2026-11-23) */
function follow(el){
  const r = el.getBoundingClientRect(), vh = innerHeight;
  if (r.bottom > vh * 0.9 || r.top < 0) window.scrollTo({top: Math.max(0, scrollY + r.top - vh * 0.1), behavior: "smooth"});
}
async function playEls(els, chain, loop){
  const was = !!P.mode; stopPlay(); const tok = ++P.tok; P.mode = els.length > 1 || chain || loop ? "seq" : "single";
  if (was){ await sleep(150); if (tok !== P.tok) return; }   // speak() right after cancel() is sometimes dropped (Chrome, Safari)
  let i = 0; P.els = els;
  while (i < els.length){
    if (tok !== P.tok) return;
    const el = els[i]; P.i = i;
    $$(".now").forEach(x => x.classList.remove("now")); el.classList.add("now");
    follow(el);
    const sg = segs(el);
    for (let k = 0; P.hold || k < (+S.rep || 1); k++){
      for (let j = 0; j < sg.length; j++){
        showPlayer((P.hold ? "∞ · " : "") + sg[j][1], i + 1, els.length);
        if (!(await say(tok, sg[j][1], sg[j][0]))) return;
        if (P.skip) break;
        if (j < sg.length - 1){ await gap(300); if (!(await waitPause(tok))) return; }
      }
      if (P.skip) break;
      await gap(450); if (!(await waitPause(tok))) return;
      if (P.skip) break;
    }
    if (P.skip){ i = Math.max(0, Math.min(els.length - 1, i + P.skip)); P.skip = 0; continue; }
    i++;
    if (loop && i >= els.length){ i = 0; await gap(600); if (!(await waitPause(tok))) return; }   // group repeat: after the last line, back to the first (RYU 2026-11-23)
  }
  if (tok !== P.tok) return;
  if (chain) return chainOn();
  stopPlay();
}
/* G: this bundle · C: this bundle and the next ones */
/* a speaker or a tap on a sentence box: that sentence over and over until a second tap or 정지 (RYU 2026-11-23) */
let LINE = null;
function lineRep(el){
  if (LINE === el && P.mode){ stopPlay(); return; }
  /* like lao-app: while a group or bundle plays, tapping one of its sentences holds that sentence (∞);
     tapping it again stops, Space lets the group go on from the next sentence */
  if (P.mode === "seq" && !LINE && P.els && P.els.includes(el) && P.els.length > 1){
    const idx = P.els.indexOf(el);
    if (P.hold && P.i === idx){ stopPlay(); return; }
    P.hold = true; if (P.paused){ P.paused = false; pauseLabel(); }
    if (idx !== P.i){ P.skip = idx - P.i; P.i = idx; quiet(); }
    pauseLabel(); return;
  }
  playEls([el], false, !el.classList.contains("tq")); LINE = el;   // TOEIC question audio: one play only; the explanation lines below still repeat (RYU 2026-11-23)
}
/* 대화 반복 · 단어 반복 · 문장 반복: the group plays round and round until 정지 (Esc) or a second tap */
let GRP = null;
function groupRep(ev, els){
  const b = ev.currentTarget;
  if (GRP === b && P.mode){ stopPlay(); return; }
  playEls(els, false, true); P.mode = "seq"; GRP = b; b.classList.add("on");
}
const bundleEls = () => $$("#view [data-say]").filter(x => !x.closest(".tq"));
function playBundle(chain){
  const cr = $("ctlrep");
  if (query || isInfo(S.code) || isMock(S.code)) return;
  ST.log("play", S.code, chain ? "all" : "lesson");   // usage statistics (v1.68)
  if (S.mode === "cards"){ playCardsAll(chain); if (cr) cr.dataset.on = chain ? "chain" : "bundle"; return; }
  if (S.mode !== "learn") return;
  const els = bundleEls();
  if (!els.length){ if (chain) chainOn(); return; }
  playEls(els, chain, !chain); if (cr) cr.dataset.on = chain ? "chain" : "bundle";
}
$("pstop").addEventListener("click", stopPlay);
$("ppause").addEventListener("click", togglePause);
/* for make_audio: every [voice, text] this bundle can say */
window.clipsOf = code => {
  const b = B[code]; b.code = code; const out = [];
  const box = h("div", null, renderLearn(b).flat(9).filter(Boolean));
  box.querySelectorAll("[data-say]").forEach(el => out.push(...segs(el)));
  (b.tq || []).forEach((q, i) => { const t = tqBox(q, i); [t, ...t.querySelectorAll("[data-say]")].forEach(el => { if (el.dataset.say) out.push(...segs(el)); }); });   // every bank question, not only today's draw
  const wa = b.ww || ["G", "S"];
  for (const w of b.w || []){ out.push(["f", w[0]]); w[4].forEach((p, j) => { out.push(["f", p[0]], ["f", p[2]]); if (!j) out.push([(b.pv && b.pv[(b.w || []).indexOf(w) + ".0"] || [vOf(b, wa[0])])[0], p[0]]); }); }
  return out;
};

/* ---------- header, menus ---------- */
function drawStats(){
  let w = 0, s = 0;
  const L = ORDER.filter(c => !isInfo(c));
  for (const c of L){ const b = B[c]; w += (b.w || []).length; s += (b.w || []).reduce((t, x) => t + x[4].length * 2, 0) + (b.d || []).length + (b.dr || []).reduce((t, x) => t + x[2].length, 0); }
  const n = x => Number(x).toLocaleString("en-US");
  $("stats").replaceChildren(h("span", null, h("b", null, L.length), "묶음"), h("span", null, h("b", null, n(w)), "단어"), h("span", null, h("b", null, n(s)), "문장"));
}
const SEP = new Set([1, 7, HELP]);    // | before 기초회화, TOEIC, 도움말 (RYU)
function drawGroups(){
  const cur = gOf(S.code);
  const btns = G.map((g, i) => h("button", {class: "group" + (SEP.has(i + 1) ? " sep" : ""), type: "button", "aria-pressed": cur === i + 1 ? "true" : "false",
    onclick: () => go(S.lastA[i + 1] && at.has(S.lastA[i + 1]) ? S.lastA[i + 1] : g[1][0][1][0])}, h("span", {class: "gn"}, g[0])));
  $("groups").replaceChildren(h("span", {class: "gsep", "aria-hidden": "true"}), ...btns);
  if (cur) $("app").dataset.g = "K" + cur;    // v1.30 RYU: colour follows the main menu, like the Lao app
}
function drawSubs(){
  const gi = gOf(S.code), g = G[gi - 1], cur = sOf(S.code);
  $("subs").replaceChildren(...g[1].map((s, j) => { const sc = gi + "-" + String(j + 1).padStart(2, "0");
    return h("button", {class: "sub", type: "button", role: "tab", "aria-selected": sc === cur ? "true" : "false",
      onclick: () => go(S.lastS[sc] && at.has(S.lastS[sc]) ? S.lastS[sc] : s[1][0])}, h("span", {class: "code"}, String(j + 1).padStart(2, "0")), h("span", {class: "name"}, s[0])); }));
  const s = g[1].find((x, j) => gi + "-" + String(j + 1).padStart(2, "0") === cur);
  const nw = s[1].reduce((t, c) => t + (B[c].w || []).length, 0);
  $("sinfo").replaceChildren(h("b", null, "[" + cur + "]"), " " + s[0] + " · " + s[1].length + "묶음" + (nw ? " " + nw + "단어" : ""));
  const on = $("subs").querySelector('[aria-selected="true"]'); if (on && on.scrollIntoView) on.scrollIntoView({block: "nearest", inline: "nearest"});
}
function sibs(code){ return ORDER.filter(c => sOf(c) === sOf(code)); }
function drawPicker(){
  const b = B[S.code];
  const lab = (c, x) => [h("span", {class: "ddn"}, "[" + c + "]"), h("span", {class: "ddk"}, x.t), x.en ? h("span", {class: "ddo"}, x.en) : null];
  $("bselBtn").replaceChildren(...lab(S.code, b));
  fitBsel();
  $("bselList").replaceChildren(...sibs(S.code).map(c => h("button", {type: "button", class: "ddi", role: "option", "aria-selected": c === S.code ? "true" : "false",
    onclick: () => { ddClose(); go(c); }}, ...lab(c, B[c]))));
}
function ddClose(){ $("bselList").hidden = true; $("bselBtn").setAttribute("aria-expanded", "false"); }
$("bselBtn").addEventListener("click", e => {
  if (Date.now() - (window.SWIPED_AT || 0) < 600) return;   // the end of a swipe never opens the list
  const l = $("bselList"); if (!l.hidden) return ddClose();
  l.hidden = false; $("bselBtn").setAttribute("aria-expanded", "true");
  const on = l.querySelector('[aria-selected="true"]'); if (on) l.scrollTop = on.offsetTop - l.clientHeight / 2 + on.offsetHeight / 2;
});
document.addEventListener("click", ev => { if (!ev.target.closest("#bsel")) ddClose(); });
function drawBand(b){
  const txt = [b.i ? h("p", {class: "intro"}, b.i) : null,
    b.tp && b.tp.length ? h("div", {class: "tipbox"}, b.tp.map(t => h("p", null, h("span", {class: "tb", "aria-hidden": "true"}, "•"), h("span", null, t)))) : null].filter(Boolean);
  /* a small drawing of the bundle's scene, left of the text (RYU 2026-11-24) */
  let pic = null; if (b.sc && DATA.sc && DATA.sc[b.sc] && txt.length){ pic = h("div", {class: "bandpic", "aria-hidden": "true"}); pic.innerHTML = DATA.sc[b.sc]; }
  $("bandin").replaceChildren($("bsel"), ...(pic ? [h("div", {class: "bandrow"}, pic, h("div", {class: "bandtxt"}, txt))] : txt));
}

/* ---------- sentence view (문장보기) ---------- */
const esc = s => s;
function hw(sent, word){   // headword inside an example, underlined
  const base = word.replace(/\(.*?\)/g, "").replace(/[~]/g, "").trim();
  const tries = [base, base.replace(/e$/, ""), base.split(" ")[0]].filter(t => t && t.length > 2 || t === base);
  for (const t of tries){ const m = sent.match(new RegExp("\\b" + t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "i"));
    if (m){ const i = m.index, j = i + (sent.slice(i).match(/^[\w'’-]+(?:\s[\w'’-]+){0,}/) && t === base ? base.length : m[0].length);
      let e = j; while (e < sent.length && /[a-z]/i.test(sent[e])) e++;
      return [sent.slice(0, i), h("span", {class: "hw"}, sent.slice(i, e)), sent.slice(e)]; } }
  return [sent];
}
/* key words under a sentence, right-aligned under a dotted line: ※ word(뜻), word(뜻) (RYU 2026-11-23, like lao-app) */
const gloss = g => g && g.length ? h("div", {class: "gl"}, "※ ", g.flatMap((x, j) => [j ? ", " : null, h("span", {class: "en"}, x[0]), "(", h("span", {class: "gm"}, x[1]), ")"])) : null;
const sec = (title, extra, ...kids) => kids.flat(9).filter(Boolean).length ? h("section", {class: "sec"}, h("h3", null, title, extra), kids) : null;
const lbl = (b, k) => (b.wl || ["손님", "직원"])[k];
function wordBox(b, w){
  const head = h("div", {class: "line head", "data-say": w[0], "data-v": "f"}, spk(),
    h("div", null, h("div", {class: "k"}, w[0]), w[1] ? h("div", {class: "p"}, w[1]) : null, h("div", {class: "m"}, w[2]), w[3] ? h("span", {class: "lvl"}, LV[w[3]] || w[3]) : null),
    h("button", {class: "wrep", type: "button", onclick: ev => groupRep(ev, [...ev.currentTarget.closest(".word").querySelectorAll("[data-say]")])}, ico("rep"), "단어 반복"));
  const wa = (b.ww || ["G", "S"]);
  const wi = (b.w || []).indexOf(w);
  const rows = w[4].map((p, n) => { const pv = (b.pv && b.pv[wi + "." + n]) || [vOf(b, wa[0]), vOf(b, wa[1])]; return h("div", {class: "line ex pairx", "data-say": p[0], "data-v": pv[0], "data-say2": p[2], "data-v2": pv[1]},
    h("div", {class: "exn"}, String(n + 1)), spk(),
    h("div", null,
      h("div", {class: "turn g"}, h("span", {class: "who"}, lbl(b, 0)), h("div", {class: "k"}, b.nohw ? p[0] : hw(p[0], w[0])), h("div", {class: "m"}, p[1])),
      h("div", {class: "turn s"}, h("span", {class: "who"}, lbl(b, 1)), h("div", {class: "k"}, b.nohw ? p[2] : hw(p[2], w[0])), h("div", {class: "m"}, p[3])),
      gloss(p[4]))); });
  return h("div", {class: "word"}, head, h("div", {class: "exs"}, rows));
}
function dlgBox(b){
  return h("div", {class: "rows dlg"}, b.d.map((d, n) => h("div", {class: "line " + (MALE.has(d[0]) ? "gu" : "st"), "data-say": d[1], "data-v": vOf(b, d[0])},
    h("div", {class: "exn"}, String(n + 1)), spk(),
    /* speaker label in its own column so the English and Korean lines start at the same place (RYU, like 단어와 예문) */
    h("div", null, h("div", {class: "turn"}, h("span", {class: "who"}, (b.dn && b.dn[d[0]]) || WHO[d[0]] || d[0]), h("div", {class: "k"}, d[1]), h("div", {class: "m"}, d[2])), gloss(d[3])))));
}
function drillBox(d){
  return h("div", {class: "drill"}, h("div", {class: "dpat"}, h("b", null, d[0]), h("span", null, d[1]),
      h("button", {class: "wrep drep", type: "button", onclick: ev => groupRep(ev, [...ev.currentTarget.closest(".drill").querySelectorAll("[data-say]")])}, ico("rep"), "문장 반복")),
    h("div", {class: "rows nrows"}, d[2].map((s, n) => h("div", {class: "line", "data-say": s[0], "data-v": "f"}, h("div", {class: "exn"}, String(n + 1)), spk(), h("div", null, h("div", {class: "k"}, s[0]), h("div", {class: "m"}, s[1]), gloss(s[2]))))));
}
function qaBox(q, n){
  const a = h("div", {class: "a", hidden: true}, q[1]);
  return h("div", {class: "qa"}, h("div", {class: "qq"}, h("div", {class: "exn"}, String(n + 1)), h("div", null, q[0])),
    h("div", {class: "qr"}, a, h("button", {class: "btn", type: "button", onclick: ev => { a.hidden = !a.hidden; ev.currentTarget.textContent = a.hidden ? "답 보기" : "답 숨기기"; }}, "답 보기")));
}
/* TOEIC: [part, question, [choices], answer index, explanation, script?]  Part 1–4 are listening: text hidden until 듣기 문제 영어 보기 */
const isLis = p => /^Part [1-4]/.test(p);
const TQN = 10;   // TOEIC questions shown at a time (TOEIC menu bundles hold a bank of ~90 and draw 10)
/* voices like the test: Part 1 one voice; Part 2 question and answers in different voices;
   Part 3 M: man, W: woman; Part 4 one speaker; the question of Part 3·4 read by a narrator (m2). Voices take turns by question number. */
function tqSeq(q, n){
  const L = "ABCD", a = n % 2 ? "f" : "m", o = a === "m" ? "f" : "m", p = q[0].match(/^Part (\d)/)[1];
  if (p === "1") return [[a, q[5] || q[2].map((c, j) => "(" + L[j] + ") " + c).join(" ")]];
  if (p === "2") return q[5] ? [[a, q[5]]] : [[a, q[1]], [o, q[2].map((c, j) => L[j] + ". " + c).join(" ")]];
  const out = [];
  if (p === "3") for (const ln of (q[5] || "").split("\n").map(x => x.trim()).filter(Boolean)){
    const m = ln.match(/^([MW])\d?:\s*(.*)$/); out.push(m ? [m[1] === "M" ? "m" : "f", m[2]] : [a, ln]); }
  else if (q[5]) out.push([a, q[5]]);
  out.push(["m2", q[1]]);
  return out;
}
function picBox(k){ const f = h("div", {class: "tpic"}); f.innerHTML = DATA.pics[k]; return f; }   // TOEIC Part 1 drawing (RYU 2026-11-23)
function tqBox(q, n){
  /* real test: Part 1 shows the photo only (here a Korean description), Part 2 shows nothing, Part 3·4 print the question and choices but not the script */
  const lis = isLis(q[0]), L = "ABCD", p34 = /^Part [34]/.test(q[0]), p1 = /^Part 1/.test(q[0]);
  const vn = [...(q[1] + q[2][0])].reduce((a, ch) => a + ch.charCodeAt(0), 0);   // voices follow the question, not its place (random draws)
  const seq = lis ? tqSeq(q, vn) : null, sayTxt = seq ? seq.map(x => x[1]).join(" ") : null;
  const why = h("p", {class: "twhy", hidden: true});
  const box = h("div", {class: "tq" + (lis ? " lis" : "") + (p34 ? " p34" : ""), "data-say": sayTxt, "data-seq": seq ? JSON.stringify(seq) : null},
    h("div", {class: "tqh"}, h("span", {class: "exn"}, String(n + 1)), h("span", {class: "tpart"}, q[0]), lis ? spk() : null),
    p1 && q[1] && DATA.pics && DATA.pics[q[1]] ? [picBox(q[1]), h("details", {class: "tdescd"}, h("summary", null, "사진 설명 보기"), q[1].replace(/^사진:\s*/, ""))]
      : p1 && q[1] ? h("p", {class: "tdesc"}, "📷 " + q[1]) : null,
    q[5] ? h("p", {class: "tqq tscr"}, q[5]) : null,
    q[1] && !p1 ? h("p", {class: "tqq" + (p34 ? " tqs" : "")}, q[1]) : null,
    lis && n === 0 ? h("p", {class: "tnote"}, "듣기 문제는 시험처럼 영어가 가려져 있어요. 🔊로 듣고 풀어 보세요.") : null,
    h("div", {class: "topts"}, q[2].map((c, j) => h("button", {type: "button", class: "topt", "data-ok": j === q[3] ? "1" : "0",
      onclick: ev => { box.querySelectorAll(".topt").forEach(o => { o.disabled = true; if (o.dataset.ok === "1") o.classList.add("right"); });
        const ok = j === q[3]; if (!ok) ev.currentTarget.classList.add("wrong");
        why.replaceChildren(h("b", null, ok ? "정답입니다. " : "정답: (" + L[q[3]] + ") "), q[4]); why.hidden = false; box.dataset.ok = ok ? "1" : "0";
        /* usage statistics (v1.68): a TOEIC set counts once every question on the page has an answer */
        const all = $$("#view .tq"); if (all.length && all.every(x => x.dataset.ok)) ST.log("toeic", S.code, all.filter(x => x.dataset.ok === "1").length, all.length); }},
      h("span", {class: "ol"}, "(" + L[j] + ")"), " ", h("span", {class: "ot"}, c)))), why);
  return box;
}
function relBox(b){
  const rel = (b.rel || []).filter(c => at.has(c)); if (!rel.length) return null;
  return h("div", {class: "relbox"}, h("div", {class: "relhd"}, "관련 묶음"),
    rel.map(c => h("button", {class: "relrow", type: "button", onclick: () => go(c)}, h("span", {class: "rc"}, "[" + c + "]"), h("span", null, B[c].t), B[c].en ? h("span", {class: "ddo"}, B[c].en) : null)));
}
function pnRow(code){
  const i = at.get(code), pv = ORDER[i - 1], nx = ORDER[i + 1];
  return h("div", {class: "pnrow"},
    pv ? h("button", {class: "pn pv", type: "button", onclick: () => go(pv)}, h("b", null, h("kbd", {class: "kc"}, "<"), "← 이전 묶음"), h("small", null, "[" + pv + "] " + B[pv].t)) : h("span"),
    nx ? h("button", {class: "pn nx", type: "button", onclick: () => go(nx)}, h("b", null, "다음 묶음 →", h("kbd", {class: "kc"}, ">")), h("small", null, "[" + nx + "] " + B[nx].t)) : h("span"));
}
function renderLearn(b){
  const tShow = h("label", {class: "tshow"}, h("input", {type: "checkbox", id: "tShow", checked: document.body.classList.contains("show-lis") ? true : null,
    onchange: ev => document.body.classList.toggle("show-lis", ev.target.checked)}), "듣기 문제 영어 보기");
  const dlgRep = h("button", {class: "wrep hrep", type: "button", onclick: ev => groupRep(ev, $$("#view .dlg .line"))}, ico("rep"), "대화 반복");
  const hasLis = (b.tq || []).some(q => isLis(q[0]));
  const parts = {
    d: () => sec(b.dt || "대화", (b.d || []).length ? dlgRep : null, (b.d || []).length ? dlgBox(b) : null),
    w: () => sec(b.wt || "단어와 예문", null, (b.w || []).map(w => wordBox(b, w))),
    dr: () => sec(b.drt || "바꿔 말하기", null, (b.dr || []).map(drillBox)),
    sm: () => sec("정리", null, b.sm ? h("div", {class: "tip"}, [].concat(b.sm).map(t => h("p", {class: "note-ko"}, t))) : null),
    qa: () => sec("확인 문제", null, (b.qa || []).map(qaBox)),
    tq: () => { const all = b.tq || []; if (!all.length) return null;
      /* question bank (RYU 2026-11-23): TQN questions drawn at random each time; 🔀 draws again */
      const wrap = h("div", {class: "tqwrap"});
      const shuf = a => { for (let i = a.length - 1; i > 0; i--){ const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
      const partOf = q => q[0].split(" ·")[0];
      /* 미니 모의고사 (b.tqk): the same number per Part as a real mini test, each drawn from that Part's bank, in Part order */
      const n = b.tqn || TQN, show = b.tqk ? Object.values(b.tqk).reduce((x, y) => x + y, 0) : Math.min(n, all.length);
      const draw = () => { let pick = all.map((q, i) => i);
        if (b.tqk) pick = Object.keys(b.tqk).sort().flatMap(p => shuf(pick.filter(i => partOf(all[i]) === p)).slice(0, b.tqk[p]).sort((x, y) => x - y));
        else if (all.length > n) pick = shuf(pick).slice(0, n).sort((x, y) => x - y);
        wrap.replaceChildren(...pick.map((i, n) => tqBox(all[i], n))); };
      draw();
      const more = all.length > show ? h("button", {class: "wrep hrep", type: "button", onclick: () => { stopPlay(); draw(); }}, "🔀 다른 문제 (" + all.length + "문제 중 " + show + ")") : null;
      return sec(b.tqt || "TOEIC 연계", [more, hasLis ? tShow : null], wrap); }};
  return [(b.ord || ["d", "w", "dr", "sm", "qa", "tq"]).map(k => parts[k]()), relBox(b), pnRow(b.code)];
}

/* ---------- word cards (주요단어) ---------- */
async function playCard(c){
  if (c.classList.contains("now")) return stopPlay();
  stopPlay(); const tok = ++P.tok; c.classList.add("now");
  for (let k = 0; k < S.rep && tok === P.tok; k++){
    c.classList.remove("back"); showPlayer(c.dataset.say, 1, 1);
    if (!(await say(tok, c.dataset.say, "f"))) return; await gap(300);
    c.classList.add("back"); if (c.dataset.ex){ if (!(await say(tok, c.dataset.ex, c.dataset.exv))) return; } else await gap(1200);
    await gap(500);
  }
  if (tok === P.tok){ stopPlay(); }
}
function renderCards(b){
  const ws = b.w || [];
  if (!ws.length) return [h("p", {class: "empty"}, "이 묶음에는 단어 카드가 없어요."), pnRow(b.code)];
  const wa = b.ww || ["G", "S"];
  return [h("p", {class: "quizp"}, "카드를 누르면 영어 → 뜻과 예문 순서로 들려줘요. 다시 누르면 멈춰요."),
    h("div", {class: "wcards"}, ws.map(w => { const ex = w[4][0];
      return h("div", {class: "wcard", role: "button", tabindex: "0", "data-say": w[0], "data-ex": ex ? ex[0] : null, "data-exv": (b.pv && b.pv[ws.indexOf(w) + ".0"] || [vOf(b, wa[0])])[0], onclick: ev => playCard(ev.currentTarget)},
        h("span", {class: "spk", "aria-hidden": "true"}, ico("spk")),
        h("div", {class: "fr"}, h("div", {class: "k" + (w[0].length > 16 ? " xl" : w[0].length > 11 ? " long" : "")}, w[0]), w[1] ? h("div", {class: "p"}, w[1]) : null),
        h("div", {class: "bk"}, h("div", {class: "m"}, w[2]), ex ? h("div", {class: "ex"}, h("div", null, ex[0]), h("div", {class: "exm"}, ex[1])) : null)); })),
    pnRow(b.code)];
}
async function playCardsAll(chain){
  stopPlay(); const tok = ++P.tok; P.mode = "seq"; const cs = $$("#view .wcard"); let i = 0;
  while (i < cs.length){
    if (tok !== P.tok) return; const c = cs[i];
    $$(".now").forEach(x => x.classList.remove("now")); c.classList.add("now"); follow(c);
    for (let k = 0; P.hold || k < (+S.rep || 1); k++){
      c.classList.remove("back"); showPlayer((P.hold ? "∞ · " : "") + c.dataset.say, i + 1, cs.length);
      if (!(await say(tok, c.dataset.say, "f"))) return; if (P.skip) break;
      await gap(400); c.classList.add("back");   // word, then the example on the back, as one set (RYU 2026-11-23)
      if (c.dataset.ex){ if (!(await say(tok, c.dataset.ex, c.dataset.exv))) return; } else await gap(1100);
      await gap(600); if (!(await waitPause(tok))) return; if (P.skip) break;
    }
    c.classList.remove("back");
    if (P.skip){ i = Math.max(0, Math.min(cs.length - 1, i + P.skip)); P.skip = 0; continue; }
    i++;
    if (!chain && i >= cs.length){ i = 0; await gap(600); if (!(await waitPause(tok))) return; }   // 묶음 재생 starts again from the first card (RYU 2026-11-23)
  }
  if (tok !== P.tok) return;
  if (chain) return chainOn();
  stopPlay();
}

/* ---------- review quiz (복습퀴즈): 10 questions from the bundle's words ---------- */
let quiz = null;
const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--){ const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
function makeQuiz(b){
  const own = (b.w || []).map(w => ({en: w[0], ko: w[2], ex: w[4]}));
  const pool = sibs(b.code).filter(c => c !== b.code).flatMap(c => (B[c].w || []).map(w => ({en: w[0], ko: w[2]})))
    .concat(ORDER.filter(c => gOf(c) === gOf(b.code)).flatMap(c => (B[c].w || []).map(w => ({en: w[0], ko: w[2]}))));
  if (own.length < 2 || own.length + pool.length < 4) return {code: b.code, qs: [], at: 0, right: 0};
  const qs = shuffle(own).slice(0, 10).map((it, n) => {
    let kind = ["mean", "en", "listen", "blank"][n % 4], blank = null;
    if (kind === "blank"){
      const cand = [];
      for (const p of it.ex) for (const s of [p[0], p[2]]){ const m = s.match(new RegExp("\\b" + it.en.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "\\b", "i")); if (m) cand.push({s, k: s === p[0] ? p[1] : p[3], i: m.index}); }
      const c = shuffle(cand)[0];
      if (c) blank = {pre: c.s.slice(0, c.i), post: c.s.slice(c.i + it.en.length), ko: c.k, full: c.s}; else kind = "en";
    }
    const key = kind === "mean" || kind === "listen" ? "ko" : "en", seen = new Set([it[key]]), wrong = [];
    for (const o of shuffle(own).concat(shuffle(pool))){ if (wrong.length === 3) break; if (o[key] && !seen.has(o[key])){ seen.add(o[key]); wrong.push(o[key]); } }
    return {kind, it, key, blank, a: it[key], opts: shuffle([it[key]].concat(wrong)), picked: null};
  });
  return {code: b.code, qs, at: 0, right: 0};
}
function renderQuiz(b){
  if (!quiz || quiz.code !== b.code) quiz = makeQuiz(b);
  if (!quiz.qs.length) return [h("p", {class: "empty"}, "이 묶음에는 퀴즈로 낼 단어가 부족해요."), pnRow(b.code)];
  if (quiz.at >= quiz.qs.length){ const r = quiz.right / quiz.qs.length;   // department character on the result screen (RYU 2026-11-27)
    return [h("div", {class: "qmascot"}, h("img", {src: "img/intro/mascot.png", alt: "", width: 420, height: 337}), h("div", {class: "bub"}, r >= 0.9 ? "Excellent! 호텔리어 준비 완료예요." : r >= 0.6 ? "Good job! 틀린 단어만 한 번 더 봐요." : "Nice try! 문장보기로 한 번 더 듣고 다시 풀어 봐요.")),
    h("p", {class: "quizp"}, "점수"), h("div", {class: "score"}, quiz.right + " / " + quiz.qs.length),
    h("div", {class: "rowbtns", style: "justify-content:center"}, h("button", {class: "btn primary", type: "button", onclick: () => { stopPlay(); quiz = null; render(); }}, "다시 풀기")), pnRow(b.code)]; }
  const q = quiz.qs[quiz.at];
  const head = q.kind === "listen" ? h("div", {class: "quizq listen", "data-say": q.it.en, "data-v": "f"}, h("button", {class: "btn primary", type: "button", onclick: ev => playEls([ev.currentTarget.parentNode])}, ico("spk"), " 듣기"))
    : q.kind === "blank" ? h("div", {class: "quizq qblank"}, h("div", {class: "qen"}, q.blank.pre, h("span", {class: "blank"}, "?"), q.blank.post), h("div", {class: "qlo"}, q.blank.ko))
    : q.kind === "mean" ? h("div", {class: "quizq qen"}, q.it.en) : h("div", {class: "quizq"}, q.it.ko);
  const lab = {mean: "뜻을 고르세요", en: "영어를 고르세요", listen: "듣고 뜻을 고르세요", blank: "빈칸에 알맞은 말을 고르세요"}[q.kind];
  return [h("div", null, head, h("p", {class: "quizp"}, lab + " · " + (quiz.at + 1) + " / " + quiz.qs.length)),
    h("div", {class: "choices"}, q.opts.map(o => h("button", {class: "choice" + (q.key === "en" ? " qen" : "") + (q.picked != null ? (o === q.a ? " right" : o === q.picked ? " wrong" : "") : ""), type: "button", disabled: q.picked != null,
      onclick: () => { q.picked = o; if (o === q.a) quiz.right++; render(); stopPlay(); const tok = ++P.tok; say(tok, q.kind === "blank" ? q.blank.full : q.it.en, "f"); }}, o))),
    q.picked != null ? h("div", {class: "rowbtns", style: "justify-content:flex-end"}, h("button", {class: "btn primary", type: "button", onclick: () => {
      stopPlay(); quiz.at++; if (quiz.at === quiz.qs.length) ST.log("quiz", quiz.code, quiz.right, quiz.qs.length); render(); const nq = quiz.qs[quiz.at], el = document.querySelector(".quizq.listen"); if (nq && nq.kind === "listen" && el) playEls([el]); }}, "다음 →")) : null];
}

/* ---------- search ---------- */
let query = "";
function renderSearch(){
  const q = query.toLowerCase(), hits = [];
  const add = (code, en, ko) => hits.push({code, en, ko});
  for (const c of ORDER){ const b = B[c]; if (b.info) continue;
    if (b.t.toLowerCase().includes(q) || (b.en || "").toLowerCase().includes(q)) add(c, b.t, b.en || "");
    for (const w of b.w || []){ if (w[0].toLowerCase().includes(q) || w[2].includes(q)) add(c, w[0], w[2]);
      for (const p of w[4]) for (const k of [0, 2]) if (p[k].toLowerCase().includes(q) || p[k + 1].includes(q)) add(c, p[k], p[k + 1]); }
    for (const d of b.d || []) if (d[1].toLowerCase().includes(q) || d[2].includes(q)) add(c, d[1], d[2]);
    if (hits.length > 120) break;
  }
  if (!hits.length) return [h("p", {class: "empty"}, "찾는 말이 없어요.")];
  return [h("p", {class: "quizp"}, hits.length > 120 ? "앞의 120개만 보여요." : hits.length + "개 찾음"),
    h("div", null, hits.slice(0, 120).map(x => h("button", {class: "hit", type: "button", onclick: () => { $("q").value = ""; query = ""; go(x.code); }},
      h("span", {class: "k"}, x.en), h("span", {class: "where"}, "[" + x.code + "] " + B[x.code].t), h("span", null, x.ko))))];
}

/* ---------- help ---------- */
/* ---------- 모의 면접 (RYU 2026-11-24): one question at a time, drawn at random; question, answer and its intent hidden until ticked ---------- */
/* 면접 장면 그림 (RYU 2026-11-24): 면접관 두 명과 지원자 한 명, 문제 아래 왼쪽 */
const MKSVG = '<svg viewBox="0 0 280 124" role="img" aria-label="면접관 두 명과 지원자 한 명의 면접 장면"><line x1="4" y1="116" x2="276" y2="116" stroke="var(--line)" stroke-width="2" stroke-linecap="round"/><g><rect x="30" y="54" width="34" height="34" rx="12" fill="var(--accent)"/><path d="M47 54l-5 8 5 4 5-4z" fill="#fff" opacity=".9"/><circle cx="47" cy="38" r="12" fill="#F2C9A5"/><path d="M35 37a12 12 0 0 1 24 0c-3-5-8-7-12-7s-9 2-12 7z" fill="#3A2E2A"/><rect x="92" y="54" width="34" height="34" rx="12" fill="#5E6866"/><path d="M109 54l-5 8 5 4 5-4z" fill="#fff" opacity=".9"/><circle cx="109" cy="38" r="12" fill="#E8B48C"/><path d="M96 40c-2-14 8-17 13-17s15 3 13 17c-2-6-6-9-13-9s-11 3-13 9z" fill="#5A4034"/><rect x="103.5" y="36" width="5" height="4" rx="1.5" fill="none" stroke="#3A2E2A" stroke-width="1.2"/><rect x="110.5" y="36" width="5" height="4" rx="1.5" fill="none" stroke="#3A2E2A" stroke-width="1.2"/></g><rect x="12" y="78" width="134" height="7" rx="3.5" fill="var(--accent)" opacity=".85"/><rect x="18" y="85" width="122" height="31" rx="3" fill="var(--accent-soft)" stroke="var(--line)"/><rect x="36" y="71" width="20" height="7" rx="1.5" fill="#fff" stroke="var(--line)"/><rect x="98" y="66" width="22" height="12" rx="2" fill="var(--ink)" opacity=".75"/><g><rect x="196" y="82" width="6" height="34" rx="2" fill="var(--muted)"/><rect x="238" y="56" width="6" height="60" rx="2" fill="var(--muted)"/><rect x="194" y="82" width="50" height="7" rx="3.5" fill="var(--muted)"/><rect x="204" y="52" width="32" height="34" rx="12" fill="#E9A15B"/><path d="M220 52l-5 8 5 4 5-4z" fill="#fff" opacity=".9"/><rect x="180" y="80" width="40" height="11" rx="5.5" fill="#3F4A5A"/><rect x="180" y="84" width="11" height="32" rx="5" fill="#3F4A5A"/><rect x="172" y="110" width="20" height="6" rx="3" fill="#2B2B2B"/><circle cx="220" cy="36" r="12" fill="#F2C9A5"/><path d="M208 36a12 12 0 0 1 24 0v9c-1-7-3-11-6-13-5 2-12 2-18 4z" fill="#3A2E2A"/></g><path d="M150 30h22a6 6 0 0 1 6 6v8a6 6 0 0 1-6 6h-12l-7 6 1-6h-4a6 6 0 0 1-6-6v-8a6 6 0 0 1 6-6z" fill="var(--sheet)" stroke="var(--accent)" stroke-width="1.5"/><text x="162" y="45" text-anchor="middle" font-size="12" font-weight="700" fill="var(--accent)">Q</text></svg>';
function mkPic(){ const d = h("div", {class: "mkpic"}); d.innerHTML = MKSVG; return d; }
const MOCKQ = {area: 0, order: [], i: -1, on: false};
function renderMock(b){
  /* b.mk: [[분야, [question, 뜻, [[answer, 뜻]…], 의도, 답변 방향]…]…]; 분야 0 = 전체 */
  const areas = [["전체", b.mk.flatMap(g => g[1])], ...b.mk], st = MOCKQ;
  const pool = () => areas[st.area][1];
  const next = () => { const all = pool(); st.i++; if (st.i >= st.order.length){ const last = st.order[st.order.length - 1]; st.order = shuffle(all.map((x, i) => i)); if (st.order.length > 1 && st.order[0] === last) st.order.push(st.order.shift()); st.i = 0; } };
  const vq = t => AUD[clipKey(t, "m")] ? "m" : "f", va = t => AUD[clipKey(t, "f")] ? "f" : "m";
  const sayList = (ev, list) => { const btn = ev.currentTarget; if (btn.classList.contains("on")){ stopPlay(); return; } stopPlay(); const tok = ++P.tok; btn.classList.add("on");
    (async () => { for (const [t, v] of list){ if (!(await say(tok, t, v))) break; await sleep(250); } btn.classList.remove("on"); if (tok === P.tok) stopPlay(); })(); };
  const box = h("div", {class: "mock"});
  const draw = () => {
    if (!st.on){ box.hidden = true; return; } box.hidden = false;
    const all = pool(), q = all[st.order[st.i]];
    const part = (id, label, body) => { const in_ = h("input", {type: "checkbox"}), bd = h("div", {class: "mkbody", hidden: true}, body);
      in_.addEventListener("change", () => { bd.hidden = !in_.checked; });
      return h("div", {class: "mkpart mk-" + id}, h("label", {class: "mkchk"}, in_, label), bd); };
    box.replaceChildren(
      h("div", {class: "mkhead"}, h("span", {class: "mkn"}, areas[st.area][0] + " · 문제 " + (st.i + 1) + " / " + all.length),
        h("button", {class: "btn mkplay", type: "button", onclick: ev => sayList(ev, [[q[0], vq(q[0])]])}, ico("spk"), "질문 듣기")),
      part("q", "질문 보기", [h("div", {class: "k"}, q[0]), h("div", {class: "m"}, q[1])]),
      part("a", "모범 답변 보기", [h("div", {class: "mkans"}, q[2].map(a => h("div", {class: "mkline"}, h("div", {class: "k"}, a[0]), h("div", {class: "m"}, a[1])))),
        h("button", {class: "btn mkplay", type: "button", onclick: ev => sayList(ev, q[2].map(a => [a[0], va(a[0])]))}, ico("spk"), "답변 듣기")]),
      q[3] ? part("t", "질문 의도·답변 방향 보기", h("div", {class: "tip"}, h("p", {class: "note-ko"}, h("b", null, "질문 의도 "), q[3]), h("p", {class: "note-ko"}, h("b", null, "답변 방향 "), q[4]))) : null,
      h("div", {class: "mkfoot"}, mkPic(), h("button", {class: "btn mknext", type: "button", onclick: () => { stopPlay(); next(); draw(); ST.log("mock", "8-07-01"); }}, "다음 문제 →")));
  };
  const start = () => { stopPlay(); st.order = []; st.i = -1; st.on = true; next(); draw(); ST.log("mock", "8-07-01"); box.scrollIntoView({block: "nearest"}); };
  const radios = h("div", {class: "mkareas", role: "radiogroup"}, areas.map((a, i) => {
    const r = h("input", {type: "radio", name: "mkarea", value: String(i), checked: i === st.area ? true : null});
    r.addEventListener("change", () => { if (r.checked){ st.area = i; st.on = false; stopPlay(); draw(); } });
    return h("label", {class: "mkarea"}, r, h("span", null, a[0]), h("small", null, a[1].length + "문제")); }));
  const pick = h("div", {class: "mkpick"}, h("div", {class: "mkpt"}, "분야 선택"), radios,
    h("div", {class: "mkgo"},
      /* 재생 속도 (RYU 2026-11-24): the same setting as the other bundles, also changed by the - = keys */
      h("label", {class: "mkrate"}, h("span", null, "재생 속도"), h("select", {id: "mkRate", class: "bsel", "aria-label": "재생 속도", onchange: ev => { setRate(ev.target.value); save(); }},
        [0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5].map(v => h("option", {value: String(v), selected: v === (+S.rate || 1) ? true : null}, "×" + v.toFixed(1))))),
      h("button", {class: "btn mkstart", type: "button", onclick: start}, "문제 내기")));
  draw();
  return [pick, box];   // no 이전·다음 묶음 buttons here (RYU 2026-11-24)
}
function renderInfo(b){
  const art = h("article", {class: "info"}); art.innerHTML = b.info; helpDeco(art, b);
  { const sp = art.querySelector("#statsPage"); if (sp) STP.page(sp); const sv = art.querySelector("#surveyPage"); if (sv) SV.form(sv, true); }   // 통계·의견 pages (src/stats.js, v1.68)
  return [art, pnRow(b.code)];   // 이전·다음 묶음 in 도움말 too (RYU 2026-11-24)
}

/* ---------- render and routing ---------- */
function render(){
  const view = $("view");
  if (query){ $("band").hidden = true; $("controls").hidden = true; view.replaceChildren(...renderSearch()); return; }
  const b = B[S.code]; b.code = S.code;
  $("band").hidden = false; $("controls").hidden = !!b.info;
  drawBand(b);
  if (b.info){ view.replaceChildren(...renderInfo(b)); return; }
  if (b.mk){ $("controls").hidden = true; view.replaceChildren(...renderMock(b).flat(9).filter(Boolean)); return; }
  $$(".seg button").forEach(x => x.setAttribute("aria-pressed", x.dataset.mode === S.mode ? "true" : "false"));
  $("ctlrep").hidden = S.mode === "quiz"; $("classRow").hidden = S.mode !== "learn"; $("kbinfo").hidden = S.mode === "quiz";
  const parts = S.mode === "cards" ? renderCards(b) : S.mode === "quiz" ? renderQuiz(b) : renderLearn(b);
  view.replaceChildren(...parts.flat(9).filter(Boolean));
  if (S.mode === "cards") fitWords();
}
function fitWords(){ $$(".wcard .k").forEach(k => { let fs = parseFloat(getComputedStyle(k).fontSize); while (k.scrollWidth > k.clientWidth + 1 && fs > 12){ fs -= 1; k.style.fontSize = fs + "px"; } }); }
function go(code){ if (location.hash === "#" + code) route(); else location.hash = code; }
function route(){
  const c = decodeURIComponent(location.hash.replace(/^#/, ""));
  if (at.has(c)) S.code = c; else if (c === "help") S.code = HELP0;
  AP.warm(S.code);   // get this bundle's clips ready
  S.lastA[gOf(S.code)] = S.code; S.lastS[sOf(S.code)] = S.code;
  stopPlay(); quiz = null; track(S.code); save(); ST.lesson(S.code);   // usage statistics (src/stats.js, v1.68)
  if (query || $("q").value){ query = ""; $("q").value = ""; }   // moving to a bundle ends the search
  drawGroups(); drawSubs(); drawPicker(); render();
  window.scrollTo({top: 0});
}
addEventListener("hashchange", route);
$$(".seg button").forEach(b => b.addEventListener("click", () => { S.mode = b.dataset.mode; stopPlay(); save(); render(); }));
$("repSel").value = S.rep;
/* speed: 0.7–1.5 by 0.1, select box + keys - = (or - +, numpad − +) (RYU 2026-11-24) */
function setRate(r){ r = Math.round(Math.min(1.5, Math.max(0.7, +r || 1)) * 10) / 10; S.rate = r; $("rateSel").value = String(r); const mr = $("mkRate"); if (mr) mr.value = String(r); try { AEL.playbackRate = r; } catch (er) {} }
setRate(S.rate);
$("rateSel").onchange = e => { setRate(e.target.value); save(); };
$("repSel").onchange = e => { S.rep = +e.target.value; save(); };
/* a second click on the same button stops it (RYU 2026-11-23) */
const ctlToggle = chain => { const cr = $("ctlrep"); if (P.mode && cr && cr.dataset.on === (chain ? "chain" : "bundle")){ stopPlay(); return; } playBundle(chain); };
$("playAll").addEventListener("click", () => ctlToggle(false));
$("playCont").addEventListener("click", () => ctlToggle(true));
for (const [id, c] of [["tKo", "hide-ko"], ["tEn", "hide-en"], ["tSt", "hide-st"]])
  $(id).onchange = e => { document.body.classList.toggle(c, e.target.checked); $$("#view .show").forEach(x => x.classList.remove("show")); };
/* tapping a hidden (blurred) text shows it; tapping a line plays it */
document.addEventListener("click", ev => {
  const b = ev.target.closest("button");
  const bl = ev.target.closest("#view .m, #view .k, #view .gm, #view .a, #view .tqq, #view .ot");
  if (bl && !(b && !b.classList.contains("topt")) && getComputedStyle(bl).filter !== "none"){ bl.classList.toggle("show"); ev.stopPropagation(); ev.preventDefault(); return; }
  if (b && b.classList.contains("spk") && !b.closest(".wcard")){ const el = b.closest("[data-say]"); if (el) lineRep(el); return; }
  if (b || ev.target.closest("a, input, select, label, .topts, .qa, .tq")) return;
  const ln = ev.target.closest("#view .line[data-say]");
  if (ln){ try { if (String(getSelection())) return; } catch (e) {}
    const wr = ln.classList.contains("head") && ln.querySelector(".wrep");   // the word's own line = 단어 반복, like lao-app
    if (wr){ wr.click(); return; }
    lineRep(ln); }
}, true);
let qt = 0;
/* the box is read when the timer fires (phones with the Korean keyboard can end a composition without one more input event),
   and clearing it by any means brings the bundle back (RYU 2026-11-23) */
const qSync = () => { clearTimeout(qt); qt = setTimeout(() => { const v = $("q").value.trim(); if (v === query) return; query = v; stopPlay(); render(); }, 150); };
for (const ev of ["input", "search", "change", "compositionend", "keyup"]) $("q").addEventListener(ev, qSync);
/* ---------- keyboard (same keys as lao-app / kor-app, RYU 2026-11-23) ----------
   Space pause / resume (idle: 묶음 재생) · C 연속 재생 · G 묶음 재생 · Esc stop · ← → previous / next line
   , . previous / next bundle · Enter this line without end (∞) · 1-5 횟수 · - = 속도 · S W E views (all apps, RYU 2026-11-27) · ? list of keys.
   Keys go by e.code too, so they work with the Korean keyboard on. */
const KEYS = [["Space", "일시정지 · 재개 (멈춰 있으면 묶음 듣기)"], ["C", "연속 듣기 (이 묶음부터 다음 묶음으로)"], ["G", "묶음 전체 듣기"], ["Esc", "정지"],
  ["← →", "이전 · 다음 문장"], ["< >  (, .)", "이전 · 다음 묶음"], ["Enter", "지금 문장 무한 반복 · 끄기"], ["1 ~ 5", "반복 횟수"], ["-  =  (또는 - +)", "느리게 · 빠르게 (×0.7 ~ ×1.5)"],
  ["S W E", "문장보기 · 주요단어 · 복습퀴즈"], ["?", "단축키 목록 열기 · 닫기"]];
function keyHelp(){
  const box = h("div", {id: "kbhelp", onclick: () => box.remove()},
    h("div", {class: "kbcard"}, h("b", null, "키보드 단축키"),
      h("table", null, KEYS.map(r => h("tr", null, h("td", null, h("kbd", null, r[0])), h("td", null, r[1]))))));
  document.body.appendChild(box);
}
const setSel = (id, i) => { const r = $(id); if (!r || i < 0 || i >= r.options.length || i === r.selectedIndex) return; r.selectedIndex = i; r.dispatchEvent(new Event("change", {bubbles: true})); };
document.addEventListener("keydown", e => {
  if (e.ctrlKey || e.metaKey || e.altKey) return;
  const t = e.target, tn = t && t.tagName;
  if (tn === "INPUT" || tn === "TEXTAREA" || tn === "SELECT" || (t && t.isContentEditable)){ if (e.key === "Escape" && t.id === "q"){ t.blur(); } return; }
  const hp = $("kbhelp"); if (hp){ hp.remove(); e.preventDefault(); return; }
  if (e.key === "Escape") ddClose();
  const c = e.code, k = (e.key || "").toLowerCase();
  const is = (code, ...ks) => c === code || ks.includes(k);
  if (e.key === "?" || (c === "Slash" && e.shiftKey)){ e.preventDefault(); keyHelp(); return; }
  if (e.key === "Escape"){ if (P.mode){ e.preventDefault(); stopPlay(); } return; }
  if (query) return;
  if (isInfo(S.code) && !/^(Arrow|[<>,.?]|Escape)/.test(e.key)) return;
  if (is("Comma", ",", "<") || is("Period", ".", ">")){
    e.preventDefault(); const i = at.get(S.code), d = is("Period", ".", ">") ? 1 : -1;
    go(ORDER[(i + d + ORDER.length) % ORDER.length]); return; }
  if (is("KeyS", "s", "ㄴ") || is("KeyW", "w", "ㅈ") || is("KeyE", "e", "ㄷ")){
    e.preventDefault(); $(is("KeyS", "s", "ㄴ") ? "m-learn" : is("KeyW", "w", "ㅈ") ? "m-cards" : "m-quiz").click(); return; }
  if (is("KeyC", "c", "ㅊ")){ e.preventDefault(); ctlToggle(true); return; }
  if (is("KeyG", "g", "ㅎ")){ e.preventDefault(); ctlToggle(false); return; }
  if (/^Digit[1-5]$/.test(c) || /^[1-5]$/.test(e.key)){ e.preventDefault(); setSel("repSel", +(e.key.match(/[1-5]/) || c.slice(-1))[0] - 1); return; }
  const up = is("Equal", "=", "+") || c === "NumpadAdd", dn = is("Minus", "-", "_") || c === "NumpadSubtract";
  if (up || dn){ e.preventDefault(); setRate(S.rate + (up ? 0.1 : -0.1)); save(); return; }
  if (c === "Space" || e.key === " "){
    if (P.mode){ e.preventDefault(); togglePause(); return; }
    if (tn !== "BUTTON" && tn !== "A"){ e.preventDefault(); playBundle(false); } return; }
  if (!P.mode) return;
  if (e.key === "Enter"){ e.preventDefault(); if (P.mode === "single") return; P.hold = !P.hold; if (P.paused) togglePause(); return; }
  if (e.key === "ArrowRight" || e.key === "ArrowLeft"){ e.preventDefault(); skipBy(e.key === "ArrowRight" ? 1 : -1); }
});
/* phone swipe left / right = next / previous bundle, like lao-app v3.26: decided during the move (60px within 1s, sideways 1.5x more than up/down; >40px up/down = scrolling).
   Left out: screen edges (browser back), menus, the bundle list, the player, form fields, areas that really scroll sideways, and text selection. */
(function(){ let sx = 0, sy = 0, st = 0, ok = false;
  const hscroll = el => { for (; el && el !== document.body; el = el.parentElement){ if (el.scrollWidth > el.clientWidth + 4){ const o = getComputedStyle(el).overflowX; if (o === "auto" || o === "scroll") return true; } } return false; };
  document.addEventListener("touchstart", e => { ok = false; if (e.touches.length !== 1 || query) return; const t = e.touches[0], w = innerWidth; if (t.clientX < 20 || t.clientX > w - 20) return;
    const el = e.target; if (el.closest && el.closest("input,select,textarea,#player,#bsel,#groups,#subs,#kbhelp")) return; if (hscroll(el)) return; sx = t.clientX; sy = t.clientY; st = Date.now(); ok = true; }, {passive: true});
  document.addEventListener("touchmove", e => { if (!ok) return; const t = e.touches[0], dx = t.clientX - sx, dy = t.clientY - sy;
    if (Math.abs(dy) > 40 || Date.now() - st > 1000){ ok = false; return; }
    if (Math.abs(dx) < 60 || Math.abs(dx) < Math.abs(dy) * 1.5) return; ok = false;
    try { const s = getSelection(); if (s && String(s).length) return; } catch (_) {}
    const i = at.get(S.code), c = ORDER[i + (dx < 0 ? 1 : -1)]; if (!c) return;
    window.SWIPED_AT = Date.now(); go(c);
    const s2 = $("sheet"); if (s2){ s2.style.transition = "none"; s2.style.transform = "translateX(" + (dx < 0 ? 36 : -36) + "px)"; s2.style.opacity = ".4";
      requestAnimationFrame(() => requestAnimationFrame(() => { s2.style.transition = "transform .2s ease-out,opacity .2s"; s2.style.transform = ""; s2.style.opacity = ""; })); } }, {passive: true});
  document.addEventListener("touchend", () => { ok = false; }, {passive: true});
})();
drawStats();
if (location.hash && (at.has(decodeURIComponent(location.hash.slice(1))) || location.hash === "#help")) route(); else go(S.code);

/* ---------- offline: service worker + "음성 mp3 내려받기" (like lao-app; only on the web site, not in the preview) ---------- */
if (/^https?:/.test(location.protocol) && "serviceWorker" in navigator) navigator.serviceWorker.register("sw.js").catch(() => {});
(function(){
  const n = $("voiceNote"), N = AP.count();
  if (!n || !N || !/^https?:/.test(location.protocol) || !window.indexedDB) return;
  const p = h("p", {class: "dlp"}), a = h("a", {href: "#", class: "dla"}, "↓ 음성 mp3 내려받기 (오프라인용)"), st = h("span", {class: "dls"});
  p.append(a, " ", st); n.after(p);
  /* one file per bundle now (v1.67): the mark keeps which set of packs was saved, so new clips ask for another tap */
  const mark = () => { let m = ""; try { m = localStorage.getItem("hoteleng-audio-saved") || ""; } catch (er) {} st.textContent = !m ? "" : m === AP.sig() ? "(완료)" : "(새 음성이 있어요. 다시 눌러 주세요)"; };
  let busy = false;
  a.addEventListener("click", async e => {
    e.preventDefault(); if (busy) return; busy = true;
    try { navigator.storage && navigator.storage.persist && navigator.storage.persist(); } catch (er) {}
    let bad = 1;
    try { bad = await AP.saveAll((d, t) => { st.textContent = Math.floor(d / t * 100) + "% (" + d + " / " + t + ")"; }); } catch (er) {}
    if (bad) st.textContent = "(" + bad + "개 남음, 다시 누르기)";
    else { try { localStorage.setItem("hoteleng-audio-saved", AP.sig()); } catch (er) {} mark(); }
    busy = false;
  });
  mark();
})();

// menu bar that stays at the top while reading down (design A, RYU 2026-11-24)
(function(){
  const st = $("stick"), mb = document.querySelector(".menubox"), sg = $("stickG"), g = $("groups");
  if (!st || !mb || !("IntersectionObserver" in window)) return;
  const sync = () => { sg.innerHTML = g.innerHTML; sg.querySelectorAll(".glide").forEach(x => x.remove()); $("stickT").textContent = [...$("bselBtn").querySelectorAll(".ddn,.ddk")].map(x => x.textContent).join(" "); const on = sg.querySelector('[aria-pressed="true"]'); if (on && !st.hidden) on.scrollIntoView({block: "nearest", inline: "center"}); };
  /* v1.72 (RYU 2026-11-27): the sticky row takes over exactly when the page's own menu row reaches the place where the sticky row sits,
     and gives it back at the same point when scrolling up (it used to wait until the whole menu box had left the screen) */
  const upd = () => { const T = innerWidth > 600 ? 11 : 6, show = g.getBoundingClientRect().top < T; if (show === !st.hidden) return; st.hidden = !show; if (show) sync(); };
  addEventListener("scroll", upd, {passive: true}); addEventListener("resize", upd); upd();
  new MutationObserver(() => { if (!st.hidden) sync(); }).observe(g, {childList: true, subtree: true, attributes: true});
  new MutationObserver(() => { if (!st.hidden) sync(); }).observe($("bselBtn"), {childList: true, subtree: true, characterData: true});
  sg.addEventListener("click", e => { const t = e.target.closest(".group"); if (!t) return; const i = [...sg.querySelectorAll(".group")].indexOf(t); const o = g.querySelectorAll(".group")[i]; if (o) o.click(); document.querySelector(".search").scrollIntoView({block: "start"}); });
  $("stickQ").addEventListener("click", () => { window.scrollTo(0, 0); $("q").focus(); });
})();

// bundle title button: when the English name does not fit on one line, it goes to a second line (no "…") (RYU 2026-11-24)
function fitBsel(){ const b = $("bselBtn"); if (!b) return; b.classList.remove("two"); const o = b.querySelector(".ddo"), k = b.querySelector(".ddk");
  if ((o && o.scrollWidth > o.clientWidth + 1) || b.scrollWidth > b.clientWidth + 1 || (k && k.scrollWidth > k.clientWidth + 1)) b.classList.add("two"); }
addEventListener("resize", () => fitBsel());
if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => fitBsel());

// PC: a soft pill with a line under it slides along the menu after the mouse (RYU 2026-11-24)
(function(){
  if (!matchMedia("(hover:hover) and (pointer:fine)").matches) return;
  for (const id of ["groups", "stickG"]) { const nav = $(id); if (!nav) continue;
    const gl = () => { let e = nav.querySelector(".glide"); if (!e) { e = h("span", {class: "glide", "aria-hidden": "true"}); nav.appendChild(e); } return e; };
    nav.addEventListener("mouseover", ev => { const t = ev.target.closest(".group"); if (!t || !nav.contains(t)) return; const e = gl(), first = e.style.opacity !== "1";
      if (first) { e.style.transition = "none"; e.style.left = t.offsetLeft + "px"; e.style.width = t.offsetWidth + "px"; e.style.top = t.offsetTop + "px"; e.style.height = t.offsetHeight + "px"; e.offsetWidth; e.style.transition = ""; }
      e.style.left = t.offsetLeft + "px"; e.style.width = t.offsetWidth + "px"; e.style.top = t.offsetTop + "px"; e.style.height = t.offsetHeight + "px"; e.style.opacity = "1"; });
    nav.addEventListener("mouseleave", () => { const e = nav.querySelector(".glide"); if (e) e.style.opacity = "0"; });
  }
})();

// PC: menu rows that do not fit get a round arrow button at the end that has more; the mouse wheel moves the row too (RYU 2026-11-24)
(function(){
  if (!matchMedia("(hover:hover) and (pointer:fine)").matches) return;
  const chev = d => { const b = h("button", {class: "hsb " + (d < 0 ? "l" : "r"), type: "button", "aria-label": d < 0 ? "왼쪽 메뉴 보기" : "오른쪽 메뉴 보기"}); b.hidden = true;
    b.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="' + (d < 0 ? "m15 5-7 7 7 7" : "m9 5 7 7-7 7") + '"/></svg>'; return b; };
  for (const id of ["groups", "subs", "stickG"]) { const nav = $(id); if (!nav) continue;
    const w = h("div", {class: "hs"}); nav.parentNode.insertBefore(w, nav); w.appendChild(nav);
    const l = chev(-1), r = chev(1); w.append(l, r);
    const upd = () => { const m = nav.scrollWidth - nav.clientWidth, x = nav.scrollLeft; l.hidden = !(m > 2 && x > 2); r.hidden = !(m > 2 && x < m - 2); w.classList.toggle("ml", !l.hidden); w.classList.toggle("mr", !r.hidden); };
    const mv = d => nav.scrollBy({left: d * Math.max(120, nav.clientWidth * .6), behavior: "smooth"});
    l.addEventListener("click", () => mv(-1)); r.addEventListener("click", () => mv(1));
    nav.addEventListener("scroll", upd, {passive: true});
    nav.addEventListener("wheel", e => { if (nav.scrollWidth - nav.clientWidth < 3 || Math.abs(e.deltaY) <= Math.abs(e.deltaX)) return; e.preventDefault(); nav.scrollLeft += e.deltaY; }, {passive: false});
    addEventListener("resize", upd);
    const show = () => { const t = nav.querySelector('[aria-pressed="true"],[aria-selected="true"]'); if (t) { const a = t.offsetLeft - 40, z = t.offsetLeft + t.offsetWidth + 40 - nav.clientWidth; if (nav.scrollLeft > a) nav.scrollLeft = Math.max(0, a); else if (nav.scrollLeft < z) nav.scrollLeft = z; } upd(); };
    new MutationObserver(() => requestAnimationFrame(show)).observe(nav, {childList: true, subtree: true, attributes: true, attributeFilter: ["aria-pressed", "aria-selected"]});
    requestAnimationFrame(show);
    if ("ResizeObserver" in window) new ResizeObserver(upd).observe(nav);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(upd);
    upd();
  }
})();

/* ======================= v1.68 HotelEng (RYU 2026-11-27) =======================
   App renamed HotelEng; like PhasaKAO / PhasaLAO: intro page (src/intro.js), theme + text size + HOME row at the bottom,
   title tap = intro, help pages in numbered colour boxes, anonymous stats + survey (src/stats.js). */
/* lessons seen and study days on this device (for the survey offer and the intro) */
function track(c){ if (!c || isInfo(c)) return; S.seen = S.seen || {}; S.seen[c] = 1;
  const d = new Date(), t = d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0");
  S.days = S.days || []; if (S.days[S.days.length - 1] !== t){ S.days.push(t); S.days = S.days.slice(-60); }
  const sb = $("svbox"); if (sb) SV.offer(sb, Object.keys(S.seen).length, S.days.length); }

/* help pages like PhasaKAO: page title, a lead box, each <h3> part in a numbered colour box, pictures in their own "화면 보기" box */
function helpDeco(art, b){
  if (gOf(b.code) !== HELP) return;
  art.classList.add("hpinfo");
  const head = h("div", {class: "hphead"}, h("h2", null, b.t), b.en ? h("div", {class: "sub2"}, b.en) : null);
  const kids = [...art.childNodes].filter(n => n.nodeType === 1 || (n.nodeType === 3 && n.textContent.trim()));
  const lead = [], boxes = [], shots = []; let cur = null;
  for (const n of kids){
    if (n.nodeType === 1 && (n.matches("figure.hshot,.hshots"))){ shots.push(n); continue; }
    if (n.nodeType === 1 && n.tagName === "H3"){ cur = {h: n, items: []}; boxes.push(cur); continue; }
    if (n.nodeType === 1 && n.matches("#statsPage,#surveyPage")){ cur = null; boxes.push({raw: n}); continue; }
    if (cur) cur.items.push(n); else lead.push(n);
  }
  let k = 0; const mk = (title, items, extra) => { const ib = h("div", {class: "ib hc" + (k++ % 4) + (extra || "")}, h("h3", null, title), h("div", {class: "ibb"}, items)); return ib; };
  const out = [head];
  if (lead.length) out.push(h("div", {class: "ib ib-lead"}, h("div", {class: "ibb"}, lead)));
  for (const x of boxes) out.push(x.raw ? x.raw : mk([...x.h.childNodes], x.items));
  if (shots.length) out.push(mk(["화면 보기"], shots, " ib-shots"));
  art.replaceChildren(...out);
}

/* dark screen: most dark rules only answer the device setting (@media); copy them once for the 밤 button ([data-theme="dark"]), as PhasaLAO does */
(function(){ const out = [];
  for (const sh of document.styleSheets){ let rs; try { rs = sh.cssRules; } catch (e) { continue; }
    for (const r of rs) if (r.media && /prefers-color-scheme:\s*dark/.test(r.media.mediaText)) for (const x of r.cssRules){ if (!x.selectorText) continue;
      const sel = x.selectorText.split(",").map(t => t.trim()).filter(t => t.includes(':root:not([data-theme="light"])')).map(t => t.replace(/:root:not\(\[data-theme="light"\]\)/g, ':root[data-theme="dark"]'));
      if (sel.length) out.push(sel.join(",") + "{" + x.style.cssText + "}"); } }
  if (out.length) document.head.appendChild(h("style", {id: "darkcopy"}, out.join("\n"))); })();

/* bottom row: 글자 크기 · 낮/밤 · HOME (RYU 2026-11-27) */
function applyPrefs(){
  const r = document.documentElement;
  if (S.theme === "light" || S.theme === "dark") r.setAttribute("data-theme", S.theme); else r.removeAttribute("data-theme");
  r.style.setProperty("--fz", String(S.fz || 1));
  const box = $("prefs"); if (!box) return;
  const seg = (label, opts, cur, set) => h("div", {class: "pseg", role: "group", "aria-label": label, title: label},
    h("div", {class: "pbtns"}, opts.map(([v, t]) => h("button", {type: "button", class: "pb" + (String(cur) === String(v) ? " on" : ""), "aria-pressed": String(cur) === String(v) ? "true" : "false",
      onclick: () => { set(v); save(); applyPrefs(); if (S.mode === "cards") fitWords(); fitBsel(); }}, t))));
  box.replaceChildren(
    seg("글자 크기", [[0.9, "A−"], [1, "A"], [1.15, "A+"], [1.3, "A++"]], S.fz || 1, v => S.fz = v),
    seg("화면", [["auto", "자동"], ["light", "☀ 낮"], ["dark", "☾ 밤"]], S.theme || "auto", v => S.theme = v),
    h("button", {type: "button", class: "pb phome", title: "HotelEng 첫 화면", onclick: () => goHome()}, h("span", {class: "hico", "aria-hidden": "true"}), "HOME"));
  box.querySelector(".hico").innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 11 12 4l9 7"/><path d="M5 10v10h5v-6h4v6h5V10"/></svg>';
}
function goHome(){ stopPlay(); if (window.HE && window.HE.intro){ window.HE.intro(); return; } go(ORDER[0]); setTimeout(() => scrollTo(0, 0), 60); }
applyPrefs();
{ const sb = $("svbox"); if (sb && S.seen) SV.offer(sb, Object.keys(S.seen).length, (S.days || []).length); }

/* title (top left, and HotelEng in the sticky bar) opens the intro */
for (const e of [document.querySelector(".top .brand"), document.querySelector("#stick .strow > b")]) if (e){
  e.style.cursor = "pointer"; e.setAttribute("role", "link"); e.setAttribute("tabindex", "0"); e.title = "HotelEng 첫 화면";
  e.addEventListener("click", goHome); e.addEventListener("keydown", ev => { if (ev.key === "Enter") goHome(); }); }

/* hooks for src/intro.js */
window.HE = {logo: (document.querySelector(".hmlogo-a") || {}).outerHTML, S, save, applyPrefs, speak: (t, v) => speakOne(t, v || "f"), quiet, setRep: v => { S.rep = +v; $("repSel").value = String(S.rep); save(); }, setRate: v => { setRate(v); save(); },
  go: code => go(code), groups: G.map((g, i) => [i + 1, g[0], g[1][0][1][0]]), ver: HE_VER,
  n: (() => { let w = 0, s = 0; const L = ORDER.filter(c => !isInfo(c)); for (const c of L){ const b = B[c]; w += (b.w || []).length; s += (b.w || []).reduce((t, x) => t + x[4].length * 2, 0) + (b.d || []).length + (b.dr || []).reduce((t, x) => t + x[2].length, 0); } return {b: L.length, w, s, m: G.length - 1}; })()};

/* HotelEng intro page (v1.68, RYU 2026-11-27): PhasaKAO's intro (kor-app src/intro.js, approved design) with Korean text,
   no character and no meaning-voice switch. Shown when the app opens without a lesson link, once per visit; a refresh keeps
   whichever screen was showing. The settings card writes straight into the app's saved state (window.HE, from src/app.js).
   Pictures: RYU sends them later. Until then each slot shows a drawn placeholder with its number (PICS below = file per slot). */
(function(){
"use strict";
const HE = window.HE; if (!HE) return;
const S = HE.S, URL_APP = "hoteleng.pages.dev";
/* picture slots: file in img/intro/ once RYU has sent it (null = placeholder) */
/* RYU's photos 2026-11-27 (picked by Claude from 25): Temasek welcome programme (hero), Together programme group (install band),
   PC rows under the menus: wine service, Conrad Singapore talk, HR mock interview, PMS practice, banquet set-up, job shadowing */
const PICS = {hero: "welcome-s.jpg", heroPad: "welcome.jpg", heroPc: "welcome.jpg", inst: "together.jpg", s1: null, s2: null, s3: null,
  g1: "wine.jpg", g2: "conrad.jpg", g3: "interview.jpg", g4: "pms.jpg", g5: "banquet-s.jpg", g6: "shadowing.jpg"};
const SLOT = {hero: "① 휴대폰 첫 화면 배경", heroPad: "② 태블릿 첫 화면 배경", heroPc: "③ PC 첫 화면 배경", inst: "④ 설치 안내 배경",
  s1: "⑤ PC 작은 사진 1", s2: "⑥ PC 작은 사진 2", s3: "⑦ PC 작은 사진 3", g1: "⑧ PC 메뉴 아래 사진 1", g2: "⑨ PC 메뉴 아래 사진 2", g3: "⑩ PC 메뉴 아래 사진 3"};
function pic(k){
  if (PICS[k]) return "img/intro/" + PICS[k];
  const big = /^(hero|heroPad|heroPc|inst)$/.test(k), W = big ? 1200 : 480, H = big ? 800 : 300;
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1E5B88"/><stop offset="1" stop-color="#0C2440"/></linearGradient></defs>`
    + `<rect width="${W}" height="${H}" fill="url(#g)"/><g fill="none" stroke="#fff" stroke-opacity=".28" stroke-width="${big ? 3 : 2}" transform="translate(${W * .58} ${H * .2}) scale(${H / 160})"><path d="M0 120h150M30 120V20h60v100M30 20l30-12 30 12M60 8V0M10 120V50h20M90 50h20v70"/>`
    + `<g fill="#fff" fill-opacity=".18">${[0, 1, 2, 3, 4].map(r => [0, 1, 2].map(c => `<rect x="${38 + c * 16}" y="${30 + r * 17}" width="8" height="10"/>`).join("")).join("")}</g></g>`
    + `<text x="${W * .05}" y="${H * (big ? .07 : .9)}" font-family="sans-serif" font-size="${big ? 34 : 22}" fill="#fff" fill-opacity=".75">사진 자리 ${SLOT[k]}</text></svg>`;
  return "data:image/svg+xml;charset=utf-8," + encodeURIComponent(svg);
}
/* the app's menus: [group no, tile text, name, short note] */
const TILE = {"기초회화": ["Hi", "인사·숫자·기본 문장"], "호텔기본": ["Hotel", "부서·직무·호텔 용어"], "프런트": ["Desk", "예약·체크인·체크아웃"], "객실·시설": ["Room", "하우스키핑·시설 안내"],
  "식음료": ["F&B", "레스토랑·바·룸서비스"], "고객응대·실무": ["Care", "불만·응급·실무"], "TOEIC": ["TOEIC", "LC·RC 1,000문제"], "영어면접": ["Job", "자기소개·모의 면접"], "도움말": ["?", "사용법·통계·의견"]};
const MENUS = HE.groups.map(g => [g[0], (TILE[g[1]] || [g[1].slice(0, 2)])[0], g[1], (TILE[g[1]] || ["", ""])[1], g[2]]);
const LEARN = 6;
const x = {
 hello: "Welcome! 어서 오세요!", sub: "호텔 현장에서 바로 쓰는 영어, 주제별로 쉽게",
 lead: "기초 회화부터 프런트·객실·식음료·고객 응대 실무 영어, TOEIC, 영어면접까지. 원어민 음성과 한국어 뜻, 주요 단어 메모로 공부해요.",
 st: ["묶음", "단어", "문장", "메뉴"], free: "무료",
 s1: "재생 설정", s1n: "공부하면서 언제든 바꿀 수 있어요. 이 기기에 저장됩니다.",
 pass: "내 학습 설정", rep: "재생 횟수", spd: "속도", theme: "화면", th: ["자동", "☀ 낮", "☾ 밤"], fz: "글자 크기", listen: "들어 보기",
 start: "시작하기", how: "사용법",
 s2: "공부 방법", s2n: "모든 묶음은 세 가지 보기로 공부해요.", h3: [["문장보기", "대화·예문 듣고 따라 하기", "listen"], ["주요단어", "단어 카드로 뜻 익히기", "cards"], ["복습퀴즈", "10문제로 확인", "quiz"]], h3k: ["S", "W", "E"],
 inside: "메뉴", learn: "호텔 영어", live: "시험·취업",
 it: "HotelEng를 홈 화면에 추가", itn: "앱처럼 전체 화면으로 열리고, 음성을 저장하면 인터넷 없이도 들을 수 있어요. 앱 스토어는 필요 없어요.", det: "지금 쓰는 기기",
 dlt: "내려받기", dla: "앱 설치", dlad: "다른 앱처럼 전체 화면으로 열려요.", inst: "설치", seehow: "방법 보기",
 dlv: "음성 모두 저장", dlvd: "오프라인에서 듣기용 영어 음성. Wi‑Fi에서 받으세요.", save: "저장",
 qr: "휴대폰으로 열기", qrd: "휴대폰 카메라로 찍으면 열려요.", copy: "복사", copied: "주소를 복사했어요",
 foot: "호텔경영학과 학생을 위한 무료 영어 앱",
 steps: {ios: ["Safari에서 이 페이지를 여세요.", "아래쪽 공유 버튼 {share}을 누르세요.", "아래로 내려 “홈 화면에 추가”를 고르세요.", "“추가”를 누르면 홈 화면에 HotelEng가 생겨요."],
  android: ["아래 “설치”를 누르세요.", "안 보이면 Chrome 메뉴 {dots}에서 “앱 설치”를 고르세요.", "“설치”를 누른 뒤 홈 화면에서 HotelEng를 여세요."],
  ipad: ["Safari에서 이 페이지를 여세요.", "오른쪽 위 공유 버튼 {share}을 누르세요.", "“홈 화면에 추가” → “추가”를 누르세요."],
  chrome: ["Chrome이나 Edge 주소창 끝의 설치 아이콘 {inst}을 누르세요.", "“설치”를 누르면 HotelEng가 따로 창으로 열리고 바탕화면에 바로가기가 생겨요."],
  safari: ["Mac Safari에서 파일 메뉴를 여세요.", "“Dock에 추가” → “추가”를 누르세요."]}
};
const ICON = {
 play: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M7 4.5v15l13-7.5z"/></svg>',
 stop: '<svg viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="6" width="12" height="12" rx="2"/></svg>',
 arrow: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
 share: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v12M8 7l4-4 4 4"/><path d="M6 11H5v10h14V11h-1"/></svg>',
 inst: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="14" rx="2"/><path d="M12 8v6M9 11l3 3 3-3"/></svg>',
 dots: '<svg viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="5" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="12" cy="19" r="2"/></svg>',
 audio: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 14v-2a9 9 0 0 1 18 0v2"/><rect x="3" y="14" width="4" height="7" rx="1.5"/><rect x="17" y="14" width="4" height="7" rx="1.5"/></svg>',
 phone: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><rect x="7" y="3" width="10" height="18" rx="2.5"/></svg>',
 pc: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8"/></svg>',
 poster: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8 8h8M8 12h8M8 16h5"/></svg>',
 bell: '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M10 46h44M14 46a18 18 0 0 1 36 0"/><path d="M32 22v-4M28 18h8"/><path d="M8 52h48"/></svg>',
 listen: '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 36v-4a20 20 0 0 1 40 0v4"/><rect x="10" y="36" width="10" height="16" rx="4"/><rect x="44" y="36" width="10" height="16" rx="4"/></svg>',
 cards: '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"><rect x="14" y="12" width="30" height="40" rx="5" transform="rotate(-8 29 32)"/><rect x="22" y="14" width="30" height="40" rx="5"/><path d="M30 28h14M30 36h10"/></svg>',
 quiz: '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="32" cy="32" r="20"/><path d="m23 32 6 6 12-13"/></svg>'
};

/* the device: install steps for it are shown first */
const ua = navigator.userAgent || "";
const isIPad = /iPad/.test(ua) || (/Macintosh/.test(ua) && navigator.maxTouchPoints > 1);
const REAL = isIPad ? "ipad" : /iPhone|iPod/.test(ua) ? "ios" : /Android/.test(ua) ? (/Mobile/.test(ua) ? "android" : "atab") : /Mac/.test(ua) ? "mac" : "pc";
const os = {phone: REAL === "android" ? "android" : "ios", pad: REAL === "atab" ? "atab" : "ipad", pc: REAL === "mac" ? "safari" : "chrome"};
const standalone = (window.matchMedia && matchMedia("(display-mode: standalone)").matches) || navigator.standalone === true;
let bip = null;
window.addEventListener("beforeinstallprompt", e => { e.preventDefault(); bip = e; });

const esc = s => String(s).replace(/[&<>"]/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}[c]));
const kb = s => esc(s).replace(/\{(share|inst|dots)\}/g, (m, k) => '<span class="kbd">' + ICON[k] + '</span>');
const fmt = n => Number(n).toLocaleString("en-US");
const rep = () => String(S.rep || 2), rate = () => String(S.rate || 1), theme = () => S.theme || "auto", fz = () => S.fz || 1;
function isDark(){ const th = theme(); if (th === "dark") return true; if (th === "light") return false; return !!(window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches); }
/* no separate landscape layout (RYU 2026-11-27): a phone on its side keeps the phone layout */
function devOf(){ const w = window.innerWidth, touch = navigator.maxTouchPoints > 0, sm = Math.min(screen.width, screen.height);
  if (touch && sm < 600) return "phone"; return w < 700 ? "phone" : w < 1100 ? "pad" : "pc"; }

function heroCopy(){ return `
  <span class="badge"><img src="icon-192.png" alt="">HotelEng</span>
  <h1 class="ko">호텔서비스 영어</h1>
  <p class="losub">${esc(x.sub)}</p>
  <p class="lead">${esc(x.lead)}</p>
  <div class="stats"><div><b>${fmt(HE.n.b)}</b><span>${x.st[0]}</span></div><div><b>${fmt(HE.n.w)}</b><span>${x.st[1]}</span></div><div><b>${fmt(HE.n.s)}</b><span>${x.st[2]}</span></div><div><b>${HE.n.m}</b><span>${x.st[3]}</span></div></div>`; }
function brand(){ return `<div class="brand"><img src="icon-192.png" alt=""><div><b>HotelEng</b><span>Hotel Service English · 호텔서비스 영어</span></div></div>`; }
function free(long){ return `<span class="freepill"><i></i>${x.free}${long ? " · " + esc(x.hello) : ""}</span>`; }
function step(n, k, note){ return `<div class="sh">${n ? `<span class="n">${n}</span>` : ""}<div><h2>${esc(x[k])}</h2>${note ? `<p>${esc(x[note])}</p>` : ""}</div></div>`; }
function seg(name, opts, cur, cls){ return `<div class="seg${cls ? " " + cls : ""}" role="group">${opts.map(([v, l]) => `<button type="button" data-${name}="${v}" class="${String(v) === String(cur) ? "on" : ""}" aria-pressed="${String(v) === String(cur)}">${esc(l)}</button>`).join("")}</div>`; }
function pass(withCta){
  return `<div class="pass">
  <div class="passhead"><span class="ph pico">${ICON.bell}</span><div><div class="pt">HOTELENG PASS</div><div class="pn">${esc(x.pass)}<small>Study settings</small></div></div><div class="pid">ENGLISH · 영어<br>${new Date().getFullYear()}</div></div>
  <div class="scarf"></div>
  <div class="passbody">
   <div class="row"><div class="lab">${esc(x.rep)}<small>Repeat</small></div>${seg("rep", [1, 2, 3, 4, 5].map(n => [n, n + "회"]), rep())}</div>
   <div class="row full"><div class="rate"><div class="lab">${esc(x.spd)}<small>Speed</small></div><div class="rtrack"><input type="range" min="0.7" max="1.5" step="0.1" value="${rate()}" data-rate aria-label="${esc(x.spd)}"><div class="ticks" aria-hidden="true">${[0.7, 1, 1.5].map(v => `<span style="left:${((v - 0.7) / 0.8 * 100).toFixed(2)}%">${v.toFixed(1)}</span>`).join("")}</div></div><output>×${(+rate()).toFixed(1)}</output></div></div>
   <div class="row"><div class="lab">${esc(x.theme)}<small>Theme</small></div>${seg("theme", [["auto", x.th[0]], ["light", x.th[1]], ["dark", x.th[2]]], theme(), "txt")}</div>
   <div class="row"><div class="lab">${esc(x.fz)}<small>Text size</small></div>${seg("fz", [[0.9, "A−"], [1, "A"], [1.15, "A+"], [1.3, "A++"]], fz())}</div>
   <div class="sample"><button type="button" class="play" data-act="sample" aria-label="${esc(x.listen)}">${playing ? ICON.stop : ICON.play}</button><div><div class="s1 en">${esc(SAMPLE_EN)}</div><div class="s2">${esc(SAMPLE_KO)}</div></div><div class="s3">${rep()}회 · ×${(+rate()).toFixed(1)}<br>${esc(x.listen)}</div></div>
  </div>
  ${withCta ? `<div class="passcta">${cta()}</div>` : ""}
  <div class="passfoot">${esc(x.s1n)}</div>
 </div>`; }
/* department character (RYU 2026-11-27) with a short greeting */
function mascot(){ return `<div class="mascot"><img src="img/intro/mascot.png" alt="호텔경영학과 캐릭터" width="420" height="337"><div class="bub"><b>Welcome to HotelEng!</b><span>호텔 현장 영어, 오늘 한 묶음부터 같이 시작해요.</span></div></div>`; }
function how3(){ return `<div class="how3">${x.h3.map((h, i) => `<div class="hstep"><span class="k">${x.h3k[i]}</span><span class="hico">${ICON[h[2]]}</span><b>${esc(h[0])}</b><small>${esc(h[1])}</small></div>`).join("")}</div>`; }
function menus(){ const tile = (m, i) => `<button type="button" class="mt${i >= LEARN ? " live" : ""}" data-area="${m[0]}"><span class="g"${m[1].length > 3 ? ' style="font-size:.6em"' : ""}>${esc(m[1])}</span><span class="t"><b>${esc(m[2])}</b><small>${esc(m[3])}</small></span></button>`;
  return `<div class="menus"><div class="mgl">${esc(x.learn)}</div>${MENUS.slice(0, LEARN).map(tile).join("")}<div class="mgl">${esc(x.live)}</div>${MENUS.slice(LEARN).map((m, i) => tile(m, i + LEARN)).join("")}</div>`; }
function osTabs(dev){ const o = dev === "phone" ? [["ios", "iPhone"], ["android", "Android"]] : dev === "pad" ? [["ipad", "iPad"], ["atab", "Android"]] : [["chrome", "Chrome · Edge"], ["safari", "Mac Safari"]];
  return `<div class="otabs" role="group">${o.map(([k, l]) => `<button type="button" data-os="${dev}:${k}" class="${os[dev] === k ? "on" : ""}">${l}</button>`).join("")}</div>`; }
function steps(dev){ const k = os[dev] === "atab" ? "android" : os[dev]; return `<ol class="steps">${x.steps[k].map(s => `<li><span>${kb(s)}</span></li>`).join("")}</ol>`; }
function detectChip(dev){ const name = {phone: {ios: "iPhone · Safari", android: "Android · Chrome"}, pad: {ipad: "iPad · Safari", atab: "Android 태블릿"}, pc: {chrome: "PC · Chrome/Edge", safari: "Mac · Safari"}}[dev][os[dev]];
  return `<span class="detect"><i>${dev === "pc" ? ICON.pc : ICON.phone}</i>${esc(x.det)}: <b>${name}</b></span>`; }
function downloads(dev){ const ios = (dev === "phone" && os.phone === "ios") || (dev === "pad" && os.pad === "ipad") || (dev === "pc" && os.pc === "safari");
  const hasAudio = !!document.querySelector(".dla");
  return `<div class="dls">
   <div class="dl"><span class="ic"><img src="icon-192.png" alt=""></span><span class="tx"><b>${esc(x.dla)}</b><small>${esc(x.dlad)}</small></span>${standalone ? '<span class="go y">✓</span>' : `<button type="button" class="go y" data-act="${ios ? "how" : "install"}">${esc(ios ? x.seehow : x.inst)}</button>`}</div>
   ${hasAudio ? `<div class="dl"><span class="ic">${ICON.audio}</span><span class="tx"><b>${esc(x.dlv)}</b><small>${esc(x.dlvd)}</small><small class="dlmsg" data-dlmsg></small></span><button type="button" class="go" data-act="audio">${esc(x.save)}</button></div>` : ""}
  </div>`; }
function addr(){ return `<div class="addr">${URL_APP}<button type="button" data-act="copy">${esc(x.copy)}</button></div>`; }
function foot(){ return `<div class="foot"><div><b>HotelEng</b> · 호텔서비스 영어<div>${esc(x.foot)}</div><div>${URL_APP} · ${esc(HE.ver)} · Copyleft</div></div>${HE.logo || ""}</div>`; }
function cta(){ return `<button type="button" class="btn pri" data-act="start">${esc(x.start)} ${ICON.arrow}</button>`; }
function howBtn(cls){ return `<button type="button" class="btn ${cls}" data-act="how">${esc(x.how)}</button>`; }
const img = (k, alt, cls, st) => `<img${cls ? ` class="${cls}"` : ""} src="${pic(k)}" alt="${esc(alt || "")}"${st ? ` style="${st}"` : ""}>`;

/* ---- the three layouts ---- */
function phone(){ return `
 <div class="hero">${img("hero", "", "bg")}
  <div class="top">${brand()}${free(false)}</div>
  <div class="copy">${heroCopy()}</div></div>
 <div class="sec">${step(1, "s1")}${pass(false)}</div>
 <div class="sec">${step(2, "s2", "s2n")}${how3()}${mascot()}</div>
 <div class="sec"><div class="sh"><div><h2>${esc(x.inside)}</h2></div></div>${menus()}</div>
 <div class="inst">${img("inst", "", "bg")}
  ${detectChip("phone")}<h2>${esc(x.it)}</h2><p style="margin:0;opacity:.85;font-size:.88em">${esc(x.itn)}</p>
  ${osTabs("phone")}${steps("phone")}${downloads("phone")}${addr()}</div>
 ${foot()}
 <div class="sticky">${cta()}</div>`; }
function pad(){ return `
 <div class="hero">${img("heroPad", "", "bg")}
  <div class="top">${brand()}${free(true)}</div>
  <div class="copy">${heroCopy()}</div></div>
 <div class="wrap">
  <div class="duo">
   <div class="lcard">${step(0, "s2", "s2n")}${how3()}${mascot()}</div>
   ${pass(false)}
  </div>
  <div class="ctarow" style="margin-top:-8px">${howBtn("sec")}${cta()}</div>
  <div style="display:grid;gap:12px"><h2 style="font-size:1.25em">${esc(x.inside)}</h2>${menus()}</div>
 </div>
 <div class="inst">${img("inst", "", "bg")}
  <div style="display:grid;gap:14px;align-content:start">${detectChip("pad")}<h2 style="font-size:1.4em">${esc(x.it)}</h2><p style="margin:0;opacity:.85;font-size:.9em">${esc(x.itn)}</p>${osTabs("pad")}${steps("pad")}</div>
  <div style="display:grid;gap:12px;align-content:start"><h3 style="font-size:1em;opacity:.9">${esc(x.dlt)}</h3>${downloads("pad")}${addr()}</div>
 </div>
 <div class="frow">${foot()}</div>`; }
function pc(){ return `
 <div class="hero">${img("heroPc", "", "bg")}<span class="glow2"></span>
  <div class="nav">${brand()}${[0, 2, 6, 7].map(i => `<a href="#" data-area="${MENUS[i][0]}">${esc(MENUS[i][2])}</a>`).join("")}<span class="sp"></span>${free(true)}${cta()}</div>
  <div class="hgrid">
   <div class="copy">${heroCopy()}<div class="cta">${cta()}${howBtn("ghost")}</div></div>
   <div class="passwrap">${pass(true)}</div>
  </div></div>
 <div class="band">
  <div style="display:grid;gap:14px;align-content:start"><h2>${esc(x.s2)}</h2><p style="margin:0;color:var(--mm);font-size:.92em">${esc(x.s2n)} ${esc(x.s1n)}</p>${how3()}${mascot()}</div>
  <div><h2 style="margin-bottom:12px">${esc(x.inside)}</h2>${menus()}<div class="gal">${img("g1", "와인 서비스 실습")}${img("g2", "콘래드 싱가포르 특강")}${img("g3", "호텔 인사담당자 모의 면접")}${img("g4", "프런트 PMS 실습")}${img("g5", "연회 테이블 세팅")}${img("g6", "코트야드 메리어트 잡섀도잉")}</div></div>
 </div>
 <div class="inst">${img("inst", "", "bg")}
  <div style="display:grid;gap:14px;align-content:start">${detectChip("pc")}<h2 style="font-size:1.5em">${esc(x.it)}</h2><p style="margin:0;opacity:.85;font-size:.92em">${esc(x.itn)}</p>${osTabs("pc")}${steps("pc")}</div>
  <div style="display:grid;gap:12px;align-content:start;justify-items:start"><h3 style="font-size:1em">${esc(x.qr)}</h3><div class="qrbox"><img src="img/qr.svg" alt="QR ${URL_APP}"></div><p style="margin:0;opacity:.85;font-size:.85em">${esc(x.qrd)}</p>${addr()}</div>
  <div style="display:grid;gap:12px;align-content:start"><h3 style="font-size:1em;opacity:.9">${esc(x.dlt)}</h3>${downloads("pc")}</div>
 </div>
 <div class="frow">${foot()}</div>`; }

/* ---- show, redraw, close ---- */
let box = null, curDev = null;
function render(){
  if (!box) return;
  const d = devOf(), y = box.scrollTop;
  box.className = "m " + (d === "phone" ? "P" : d === "pad" ? "T" : "D") + (isDark() ? " dk" : "");
  box.style.setProperty("--fz", fz());
  box.innerHTML = '<div class="wrapin">' + (d === "phone" ? phone() : d === "pad" ? pad() : pc()) + "</div>";
  box.scrollTop = d === curDev ? y : 0; curDev = d;
  mirrorDl();
}
function open(){
  if (box) return;
  box = document.createElement("div"); box.id = "intro"; box.lang = "ko"; box.className = "notr"; box.setAttribute("role", "dialog"); box.setAttribute("aria-label", "HotelEng");
  document.body.appendChild(box); document.documentElement.classList.add("introon");
  render();
  try { sessionStorage.setItem("he-intro", "open"); } catch (e) {}
}
function close(){
  stopSample();
  try { sessionStorage.setItem("he-intro", "closed"); } catch (e) {}
  if (box){ box.remove(); box = null; } document.documentElement.classList.remove("introon");
}
let rT = 0;
window.addEventListener("resize", () => { clearTimeout(rT); rT = setTimeout(() => { if (box && devOf() !== curDev) render(); }, 150); });
if (window.matchMedia){ const mq = matchMedia("(prefers-color-scheme: dark)"); if (mq.addEventListener) mq.addEventListener("change", () => { if (box && theme() === "auto") render(); }); }

/* sample: one of the app's own recorded sentences, repeated × at the chosen speed */
const SAMPLE_EN = "Good evening. Welcome to our hotel.", SAMPLE_KO = "안녕하세요(저녁 인사). 저희 호텔에 오신 것을 환영합니다.";
let RUN = 0, playing = false;
function stopSample(){ RUN++; if (playing){ playing = false; try { HE.quiet(); } catch (e) {} } }
async function sample(){
  if (playing){ stopSample(); render(); return; }
  const me = ++RUN, on = () => playing && RUN === me;
  playing = true; render(); const n = +rep() || 1;
  for (let i = 0; i < n && on(); i++){
    await HE.speak(SAMPLE_EN, "f");
    if (on()) await new Promise(r => setTimeout(r, 350));
  }
  if (RUN === me){ playing = false; render(); }
}
function toast(msg){ if (!box) return; const el = document.createElement("div"); el.className = "toast"; el.textContent = msg; box.appendChild(el); setTimeout(() => el.remove(), 2200); }
/* the app's own "음성 mp3 내려받기" link does the work; its progress text is copied here */
function mirrorDl(){ const src = document.querySelector("p.dlp .dls"), dst = box && box.querySelector("[data-dlmsg]"); if (src && dst) dst.textContent = src.textContent; }
{ const src = document.querySelector("p.dlp .dls"); if (src && window.MutationObserver) new MutationObserver(mirrorDl).observe(src, {childList: true, characterData: true, subtree: true}); }
function goArea(a){ const m = MENUS.find(m => String(m[0]) === String(a)); close(); if (m) HE.go(S.lastA && S.lastA[m[0]] ? S.lastA[m[0]] : m[4]); setTimeout(() => scrollTo(0, 0), 80); }

document.addEventListener("click", ev => {
  if (!box || !box.contains(ev.target)) return;
  const b = ev.target.closest("button,a"); if (!b || b.disabled) return;
  if (b.dataset.rep){ HE.setRep(b.dataset.rep); render(); return; }
  if (b.dataset.theme){ S.theme = b.dataset.theme; HE.save(); HE.applyPrefs(); render(); return; }
  if (b.dataset.fz){ S.fz = +b.dataset.fz; HE.save(); HE.applyPrefs(); render(); return; }
  if (b.dataset.os){ const [d, k] = b.dataset.os.split(":"); os[d] = k; render(); return; }
  if (b.dataset.area){ ev.preventDefault(); goArea(b.dataset.area); return; }
  const a = b.dataset.act; if (!a) return;
  ev.preventDefault();
  if (a === "start") close();
  else if (a === "sample") sample();
  else if (a === "copy"){ const done = () => toast(x.copied); try { navigator.clipboard.writeText("https://" + URL_APP + "/").then(done, done); } catch (e) { done(); } }
  else if (a === "install"){ if (bip){ bip.prompt(); bip.userChoice.then(() => { bip = null; }, () => {}); } else { const el = box.querySelector(".steps"); if (el) el.scrollIntoView({behavior: "smooth", block: "center"}); } }
  else if (a === "audio"){ const d = document.querySelector(".dla"); if (d) d.click(); }
  else if (a === "how"){ const el = box.querySelector(".steps"); if (el) el.scrollIntoView({behavior: "smooth", block: "center"}); }
});
document.addEventListener("input", ev => { if (box && ev.target.matches("#intro [data-rate]")){ const v = (+ev.target.value).toFixed(1); HE.setRate(v); const o = ev.target.closest(".rate").querySelector("output"); if (o) o.textContent = "×" + (+v).toFixed(1); } });
document.addEventListener("change", ev => { if (box && ev.target.matches("#intro [data-rate]")) render(); });
/* while the intro is open, the app's keys stay off; Esc closes it */
document.addEventListener("keydown", ev => { if (!box) return; if (ev.key === "Escape") close(); else if (!/^(Tab|Enter| )$/.test(ev.key) && !ev.target.closest("#intro input")) ev.stopImmediatePropagation(); }, true);

/* open: no lesson link in the address and not yet closed in this visit; a refresh keeps whichever screen was showing */
let st = null; try { st = sessionStorage.getItem("he-intro"); } catch (e) {}
const h0 = window.HE_HASH0 != null ? window.HE_HASH0 : location.hash;   // the address as it was before app.js added the bundle
if (st === "open" || (h0.length <= 1 && st !== "closed")) open();
HE.intro = open;
})();
