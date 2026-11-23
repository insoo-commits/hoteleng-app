/* 호텔서비스 영어 — app logic. DATA (bundles) and AUD (mp3 clips) are injected by build.py. */
const $ = id => document.getElementById(id), $$ = s => [...document.querySelectorAll(s)];
const ICO = {
  spk: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 5 6 9H3v6h3l5 4z" fill="currentColor"/><path d="M15.5 8.5a5 5 0 0 1 0 7"/><path d="M18.5 5.5a9 9 0 0 1 0 13"/></svg>',
  rep: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="m17 2 4 4-4 4"/><path d="M3 11v-1a4 4 0 0 1 4-4h14"/><path d="m7 22-4-4 4-4"/><path d="M21 13v1a4 4 0 0 1-4 4H3"/></svg>'};
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
let P = {tok: 0, mode: null, paused: false, hold: false, skip: 0}, CUR_END = null;
const gap = ms => new Promise(r => setTimeout(r, ms));
function quiet(){ if (synth) try { synth.cancel(); if (synth.paused) synth.resume(); } catch (e) {} try { AEL.onended = AEL.onerror = null; AEL.pause(); } catch (e) {} const f = CUR_END; CUR_END = null; if (f) f(); }
function speakOne(text, v){
  return new Promise(res => {
    const done = () => { if (CUR_END === done) CUR_END = null; res(); };
    CUR_END = done;
    const src = AUD[clipKey(text, v)];
    if (src){ AEL.src = src; AEL.playbackRate = +S.rate || 1; AEL.onended = AEL.onerror = done; AEL.play().catch(done); return; }
    if (!synth){ setTimeout(done, 400); return; }
    const u = new SpeechSynthesisUtterance(text); u.lang = "en-US"; u.rate = +S.rate || 1;
    /* Chrome can drop an utterance it has garbage-collected and never send onend, which stopped repeats:
       keep a reference, and go on anyway once the line must have finished */
    window.__utt = u;
    const est = 2500 + text.length * 110 / (+S.rate || 1);
    let wd = setTimeout(function tick(){ if (CUR_END !== done) return; if (P.paused || synth.speaking && !synth.paused && Date.now() - t0 < est * 2) { wd = setTimeout(tick, 500); return; } done(); }, est); const t0 = Date.now();
    const pk = pickVoice(v); if (pk.v) u.voice = pk.v; u.pitch = pk.pitch; u.rate = Math.min(2, (+S.rate || 1) * (pk.rate || 1));
    u.onend = u.onerror = done; synth.speak(u);
  });
}
async function waitPause(tok){ while (P.paused && tok === P.tok) await gap(150); return tok === P.tok; }
async function say(tok, text, v){ if (tok !== P.tok) return false; await speakOne(text, v || "f"); return waitPause(tok); }
function showPlayer(t){ $("player").hidden = false; document.body.classList.add("has-player"); $("pt").textContent = t; }
function pauseLabel(){ const b = $("ppause"); if (b) b.querySelector(".bt").textContent = P.paused ? "재개" : P.hold && P.els && P.els.length > 1 && !LINE ? "계속" : "일시정지"; }
function stopPlay(){ LINE = null; if (GRP){ GRP.classList.toggle("on", false); GRP = null; } const cr = document.getElementById("ctlrep"); if (cr) delete cr.dataset.on; P.tok++; P.mode = null; P.paused = false; P.hold = false; P.skip = 0; quiet(); $$(".now").forEach(x => x.classList.remove("now")); $("player").hidden = true; document.body.classList.remove("has-player"); pauseLabel(); }
function togglePause(){
  if (!P.mode) return;
  if (P.hold && P.els && P.els.length > 1 && !LINE){ P.hold = false; P.skip = 1; if (P.paused){ P.paused = false; } quiet(); pauseLabel(); return; }   // release the held sentence, go on
  P.paused = !P.paused;
  try {
    if (P.paused){ if (AEL.src && !AEL.paused) AEL.pause(); else if (synth) synth.pause(); }
    else { if (AEL.src && AEL.paused && CUR_END && !AEL.ended) AEL.play().catch(() => {}); if (synth) synth.resume(); }
  } catch (e) {}
  pauseLabel();
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
const nextCode = () => { const c = ORDER[at.get(S.code) + 1]; return c && !isInfo(c) ? c : undefined; };
function chainOn(){ const nx = nextCode(); if (!nx){ stopPlay(); return; } go(nx); setTimeout(() => playBundle(true), 500); }
/* plays elements in order, each S.rep times (Enter: the current one without end); chain = go on to the next bundles (C) */
async function playEls(els, chain, loop){
  const was = !!P.mode; stopPlay(); const tok = ++P.tok; P.mode = els.length > 1 || chain || loop ? "seq" : "single";
  if (was){ await gap(150); if (tok !== P.tok) return; }   // speak() right after cancel() is sometimes dropped (Chrome, Safari)
  let i = 0; P.els = els;
  while (i < els.length){
    if (tok !== P.tok) return;
    const el = els[i]; P.i = i;
    $$(".now").forEach(x => x.classList.remove("now")); el.classList.add("now");
    el.scrollIntoView({block: "nearest", behavior: "smooth"});
    const sg = segs(el);
    for (let k = 0; P.hold || k < (+S.rep || 1); k++){
      for (let j = 0; j < sg.length; j++){
        showPlayer((P.hold ? "∞ · " : +S.rep > 1 ? (k % +S.rep + 1) + "/" + S.rep + " · " : "") + sg[j][1]);
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
  playEls([el], false, true); LINE = el;
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
  if (query || isInfo(S.code)) return;
  if (S.mode === "cards"){ playCardsAll(chain); if (cr) cr.dataset.on = chain ? "chain" : "bundle"; return; }
  if (S.mode !== "learn") return;
  const els = bundleEls();
  if (!els.length){ if (chain) chainOn(); return; }
  playEls(els, chain); if (cr) cr.dataset.on = chain ? "chain" : "bundle";
}
$("pstop").addEventListener("click", stopPlay);
$("ppause").addEventListener("click", togglePause);
/* for make_audio: every [voice, text] this bundle can say */
window.clipsOf = code => {
  const b = B[code]; b.code = code; const out = [];
  const box = h("div", null, renderLearn(b).flat(9).filter(Boolean));
  box.querySelectorAll("[data-say]").forEach(el => out.push(...segs(el)));
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
  $("bandin").replaceChildren(...[$("bsel"),
    b.i ? h("p", {class: "intro"}, b.i) : null,
    b.tp && b.tp.length ? h("div", {class: "tipbox"}, b.tp.map(t => h("p", null, "• " + t))) : null].filter(Boolean));
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
    h("div", null, h("div", {class: "k"}, h("span", {class: "who"}, (b.dn && b.dn[d[0]]) || WHO[d[0]] || d[0]), d[1]), h("div", {class: "m"}, d[2]), gloss(d[3])))));
}
function drillBox(d){
  return h("div", {class: "drill"}, h("div", {class: "dpat"}, h("b", null, d[0]), h("span", null, d[1]),
      h("button", {class: "wrep drep", type: "button", onclick: ev => groupRep(ev, [...ev.currentTarget.closest(".drill").querySelectorAll("[data-say]")])}, ico("rep"), "문장 반복")),
    h("div", {class: "rows"}, d[2].map(s => h("div", {class: "line", "data-say": s[0], "data-v": "f"}, spk(), h("div", null, h("div", {class: "k"}, s[0]), h("div", {class: "m"}, s[1]), gloss(s[2]))))));
}
function qaBox(q, n){
  const a = h("div", {class: "a", hidden: true}, q[1]);
  return h("div", {class: "qa"}, h("div", {class: "qq"}, h("div", {class: "exn"}, String(n + 1)), h("div", null, q[0])),
    h("div", {class: "qr"}, a, h("button", {class: "btn", type: "button", onclick: ev => { a.hidden = !a.hidden; ev.currentTarget.textContent = a.hidden ? "답 보기" : "답 숨기기"; }}, "답 보기")));
}
/* TOEIC: [part, question, [choices], answer index, explanation, script?]  Part 1–4 are listening: text hidden until 듣기 문제 영어 보기 */
const isLis = p => /^Part [1-4]/.test(p);
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
  const seq = lis ? tqSeq(q, n) : null, sayTxt = seq ? seq.map(x => x[1]).join(" ") : null;
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
        why.replaceChildren(h("b", null, ok ? "정답입니다. " : "정답: (" + L[q[3]] + ") "), q[4]); why.hidden = false; }},
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
    tq: () => sec(b.tqt || "TOEIC 연계", hasLis ? tShow : null, (b.tq || []).map(tqBox))};
  return [(b.ord || ["d", "w", "dr", "sm", "qa", "tq"]).map(k => parts[k]()), relBox(b), pnRow(b.code)];
}

/* ---------- word cards (주요단어) ---------- */
async function playCard(c){
  if (c.classList.contains("now")) return stopPlay();
  stopPlay(); const tok = ++P.tok; c.classList.add("now");
  for (let k = 0; k < S.rep && tok === P.tok; k++){
    c.classList.remove("back"); showPlayer(c.dataset.say);
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
    h("div", {class: "rowbtns", style: "justify-content:center;margin-top:12px"}, h("button", {class: "wrep tbtn", type: "button", onclick: () => playCardsAll()}, ico("rep"), "단어 전체 듣기")),
    pnRow(b.code)];
}
async function playCardsAll(chain){
  stopPlay(); const tok = ++P.tok; P.mode = "seq"; const cs = $$("#view .wcard"); let i = 0;
  while (i < cs.length){
    if (tok !== P.tok) return; const c = cs[i];
    $$(".now").forEach(x => x.classList.remove("now")); c.classList.add("now"); c.scrollIntoView({block: "nearest", behavior: "smooth"});
    for (let k = 0; P.hold || k < (+S.rep || 1); k++){
      c.classList.remove("back"); showPlayer((P.hold ? "∞ · " : "") + c.dataset.say);
      if (!(await say(tok, c.dataset.say, "f"))) return; if (P.skip) break;
      await gap(700); c.classList.add("back"); await gap(1100); if (!(await waitPause(tok))) return; if (P.skip) break;
    }
    c.classList.remove("back");
    if (P.skip){ i = Math.max(0, Math.min(cs.length - 1, i + P.skip)); P.skip = 0; continue; }
    i++;
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
  if (quiz.at >= quiz.qs.length) return [h("p", {class: "quizp"}, "점수"), h("div", {class: "score"}, quiz.right + " / " + quiz.qs.length),
    h("div", {class: "rowbtns", style: "justify-content:center"}, h("button", {class: "btn primary", type: "button", onclick: () => { stopPlay(); quiz = null; render(); }}, "다시 풀기")), pnRow(b.code)];
  const q = quiz.qs[quiz.at];
  const head = q.kind === "listen" ? h("div", {class: "quizq listen", "data-say": q.it.en, "data-v": "f"}, h("button", {class: "btn primary", type: "button", onclick: ev => playEls([ev.currentTarget.parentNode])}, ico("spk"), " 듣기"))
    : q.kind === "blank" ? h("div", {class: "quizq qblank"}, h("div", {class: "qen"}, q.blank.pre, h("span", {class: "blank"}, "?"), q.blank.post), h("div", {class: "qlo"}, q.blank.ko))
    : q.kind === "mean" ? h("div", {class: "quizq qen"}, q.it.en) : h("div", {class: "quizq"}, q.it.ko);
  const lab = {mean: "뜻을 고르세요", en: "영어를 고르세요", listen: "듣고 뜻을 고르세요", blank: "빈칸에 알맞은 말을 고르세요"}[q.kind];
  return [h("div", null, head, h("p", {class: "quizp"}, lab + " · " + (quiz.at + 1) + " / " + quiz.qs.length)),
    h("div", {class: "choices"}, q.opts.map(o => h("button", {class: "choice" + (q.key === "en" ? " qen" : "") + (q.picked != null ? (o === q.a ? " right" : o === q.picked ? " wrong" : "") : ""), type: "button", disabled: q.picked != null,
      onclick: () => { q.picked = o; if (o === q.a) quiz.right++; render(); stopPlay(); const tok = ++P.tok; say(tok, q.kind === "blank" ? q.blank.full : q.it.en, "f"); }}, o))),
    q.picked != null ? h("div", {class: "rowbtns", style: "justify-content:flex-end"}, h("button", {class: "btn primary", type: "button", onclick: () => {
      stopPlay(); quiz.at++; render(); const nq = quiz.qs[quiz.at], el = document.querySelector(".quizq.listen"); if (nq && nq.kind === "listen" && el) playEls([el]); }}, "다음 →")) : null];
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
function renderInfo(b){
  const art = h("article", {class: "info"}); art.innerHTML = b.info; return [art];
}

/* ---------- render and routing ---------- */
function render(){
  const view = $("view");
  if (query){ $("band").hidden = true; $("controls").hidden = true; view.replaceChildren(...renderSearch()); return; }
  const b = B[S.code]; b.code = S.code;
  $("band").hidden = false; $("controls").hidden = !!b.info;
  drawBand(b);
  if (b.info){ view.replaceChildren(...renderInfo(b)); return; }
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
  S.lastA[gOf(S.code)] = S.code; S.lastS[sOf(S.code)] = S.code;
  stopPlay(); quiz = null; save();
  drawGroups(); drawSubs(); drawPicker(); render();
  window.scrollTo({top: 0});
}
addEventListener("hashchange", route);
$$(".seg button").forEach(b => b.addEventListener("click", () => { S.mode = b.dataset.mode; stopPlay(); save(); render(); }));
$("repSel").value = S.rep; $("rateSel").value = S.rate;
$("repSel").onchange = e => { S.rep = +e.target.value; save(); };
$("rateSel").onchange = e => { S.rate = +e.target.value; save(); try { AEL.playbackRate = +S.rate || 1; } catch (er) {} };
$("playAll").addEventListener("click", () => playBundle(false));
$("playCont").addEventListener("click", () => playBundle(true));
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
$("q").addEventListener("input", e => { clearTimeout(qt); qt = setTimeout(() => { query = e.target.value.trim(); stopPlay(); render(); }, 150); });
/* ---------- keyboard (same keys as lao-app / kor-app, RYU 2026-11-23) ----------
   Space pause / resume (idle: 묶음 재생) · C 연속 재생 · G 묶음 재생 · Esc stop · ← → previous / next line
   , . previous / next bundle · Enter this line without end (∞) · 1-5 횟수 · - = 속도 · Q W E views · ? list of keys.
   Keys go by e.code too, so they work with the Korean keyboard on. */
const KEYS = [["Space", "일시정지 · 재개 (멈춰 있으면 묶음 듣기)"], ["C", "연속 듣기 (이 묶음부터 다음 묶음으로)"], ["G", "묶음 전체 듣기"], ["Esc", "정지"],
  ["← →", "이전 · 다음 문장"], ["< >  (, .)", "이전 · 다음 묶음"], ["Enter", "지금 문장 무한 반복 · 끄기"], ["1 ~ 5", "반복 횟수"], ["-  =", "느리게 · 빠르게"],
  ["Q W E", "문장보기 · 주요단어 · 복습퀴즈"], ["?", "단축키 목록 열기 · 닫기"]];
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
  if (is("KeyQ", "q", "ㅂ") || is("KeyW", "w", "ㅈ") || is("KeyE", "e", "ㄷ")){
    e.preventDefault(); $(is("KeyQ", "q", "ㅂ") ? "m-learn" : is("KeyW", "w", "ㅈ") ? "m-cards" : "m-quiz").click(); return; }
  if (is("KeyC", "c", "ㅊ")){ e.preventDefault(); playBundle(true); return; }
  if (is("KeyG", "g", "ㅎ")){ e.preventDefault(); if (P.mode === "seq") stopPlay(); else playBundle(false); return; }
  if (/^Digit[1-5]$/.test(c) || /^[1-5]$/.test(e.key)){ e.preventDefault(); setSel("repSel", +(e.key.match(/[1-5]/) || c.slice(-1))[0] - 1); return; }
  if (is("Minus", "-", "_") || is("Equal", "=", "+")){ e.preventDefault(); const r = $("rateSel"); setSel("rateSel", r.selectedIndex + (is("Equal", "=", "+") ? 1 : -1)); return; }
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
