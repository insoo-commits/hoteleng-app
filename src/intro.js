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
 st: ["묶음", "단어", "문장", "학습자"], free: "무료",
 s1: "재생 설정", s1n: "공부하면서 언제든 바꿀 수 있어요. 이 기기에 저장됩니다.",
 pass: "내 학습 설정", rep: "재생 횟수", spd: "속도", vol: "음량", theme: "화면", th: ["자동", "☀ 낮", "☾ 밤"], fz: "글자 크기", listen: "들어 보기",
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
  <div class="stats"><div><b>${fmt(HE.n.b)}</b><span>${x.st[0]}</span></div><div><b>${fmt(HE.n.w)}</b><span>${x.st[1]}</span></div><div><b>${fmt(HE.n.s)}</b><span>${x.st[2]}</span></div><div><b data-learners>${learners()}</b><span>${x.st[3]}</span></div></div>`; }

/* RYU 2026-11-28: "메뉴" out, "학습자" last = devices counted by the anonymous stats (same number as 도움말 > 통계), from the saved copy at once, then refreshed once per visit */
let LRN = null, LRNF = false;
const lfmt = n => Number(n).toLocaleString("en-US");
function learners(){ if (LRN == null){ try { const d = JSON.parse(localStorage.getItem("hoteleng-statspage") || "null"); if (d && d.totals && d.totals.devices) LRN = +d.totals.devices; } catch (e) {} getLearners(); } return LRN ? lfmt(LRN) : "–"; }
function getLearners(){ if (LRNF) return; LRNF = true; try { if (typeof STATS_URL === "undefined" || !STATS_URL || !navigator.onLine) return;
  fetch(STATS_URL + "?stats=1", {cache: "no-store"}).then(r => r.json()).then(d => { if (!d || !d.totals) return; try { localStorage.setItem("hoteleng-statspage", JSON.stringify(d)); } catch (e) {}
    if (d.totals.devices){ LRN = +d.totals.devices; document.querySelectorAll("#intro [data-learners]").forEach(b => { b.textContent = lfmt(LRN); }); } }).catch(() => {}); } catch (e) {} }
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
   <div class="row full"><div class="rate vol"><div class="lab">${esc(x.vol)}<small>Volume</small></div><div class="rtrack"><input type="range" min="0" max="100" step="5" value="${volP()}" data-vol aria-label="${esc(x.vol)}"><div class="ticks" aria-hidden="true">${[0, 50, 100].map(v => `<span style="left:${v}%">${v}</span>`).join("")}</div></div><output>${volP()}%</output></div></div>
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
/* volume (RYU 2026-11-27): vol.js (window.AVOL) sets one level for all app sound; iPhone/iPad included */
function volP(){ try { return window.AVOL ? AVOL.pct() : 100; } catch (e) { return 100; } }
document.addEventListener("input", ev => { if (box && ev.target.matches("#intro [data-vol]")){ const v = +ev.target.value; try { if (window.AVOL) AVOL.set(v / 100); } catch (e) {} const o = ev.target.closest(".rate").querySelector("output"); if (o) o.textContent = v + "%"; } });
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
