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
const HELP = G.length + 1;    // menu number of 도움말

/* ---------- state ---------- */
const LS = "hoteleng-v1";
let S = {code: ORDER[0], mode: "learn", rep: 1, rate: 1, lastA: {}, lastS: {}};
try { Object.assign(S, JSON.parse(localStorage.getItem(LS) || "{}")); } catch (e) {}
if (!at.has(S.code) && S.code !== "help") S.code = ORDER[0];
function save(){ try { localStorage.setItem(LS, JSON.stringify(S)); } catch (e) {} }

/* ---------- sound: own mp3 when the build made one, otherwise the device's English voice ---------- */
const synth = window.speechSynthesis;
let voices = [];
const loadVoices = () => { if (synth) voices = synth.getVoices().filter(v => /^en[-_](US|GB|AU|CA)/i.test(v.lang)); };
if (synth){ loadVoices(); synth.onvoiceschanged = loadVoices; }
function pickVoice(male){
  const us = voices.filter(v => /en[-_]US/i.test(v.lang)), v = us.length ? us : voices;
  if (!v.length) return null;
  const f = v.find(x => /female|samantha|jenny|aria|zira|ava|allison|susan|karen/i.test(x.name)),
        m = v.find(x => /\bmale|guy|david|alex|daniel|fred|tom|aaron|mark/i.test(x.name) && !/female/i.test(x.name));
  return male ? (m || v[0]) : (f || v[0]);
}
const clipKey = (t, male) => (male ? "m|" : "f|") + t.trim();
const AEL = new Audio();
let P = {tok: 0}, CUR_END = null;
const gap = ms => new Promise(r => setTimeout(r, ms));
function quiet(){ if (synth) try { synth.cancel(); } catch (e) {} try { AEL.onended = AEL.onerror = null; AEL.pause(); } catch (e) {} const f = CUR_END; CUR_END = null; if (f) f(); }
function speakOne(text, male){
  return new Promise(res => {
    const done = () => { if (CUR_END === done){ CUR_END = null; } res(); };
    CUR_END = done;
    const src = AUD[clipKey(text, male)];
    if (src){ AEL.src = src; AEL.playbackRate = S.rate; AEL.onended = AEL.onerror = done; AEL.play().catch(done); return; }
    if (!synth){ setTimeout(done, 400); return; }
    const u = new SpeechSynthesisUtterance(text); u.lang = "en-US"; u.rate = S.rate;
    const v = pickVoice(male); if (v) u.voice = v;
    u.onend = u.onerror = done; synth.speak(u);
  });
}
async function say(tok, text, male){ if (tok !== P.tok) return false; await speakOne(text, male); return tok === P.tok; }
function showPlayer(t){ $("player").hidden = false; document.body.classList.add("has-player"); $("pt").textContent = t; }
function stopPlay(){ P.tok++; quiet(); $$(".now").forEach(x => x.classList.remove("now")); $("player").hidden = true; document.body.classList.remove("has-player"); }
/* an element plays its data-say (who in data-who), then data-say2 (the second speaker) */
async function playEls(els){
  stopPlay(); const tok = ++P.tok;
  for (const el of els){
    if (tok !== P.tok) return;
    $$(".now").forEach(x => x.classList.remove("now")); el.classList.add("now");
    el.scrollIntoView({block: "nearest", behavior: "smooth"});
    for (let i = 0; i < S.rep; i++){
      showPlayer((S.rep > 1 ? (i + 1) + "/" + S.rep + " · " : "") + el.dataset.say);
      if (!(await say(tok, el.dataset.say, MALE.has(el.dataset.who || "S")))) return;
      if (el.dataset.say2){ await gap(250); showPlayer(el.dataset.say2); if (!(await say(tok, el.dataset.say2, MALE.has(el.dataset.who2 || "S")))) return; }
      await gap(450);
    }
  }
  if (tok === P.tok) stopPlay();
}
$("pstop").addEventListener("click", stopPlay);

/* ---------- header, menus ---------- */
function drawStats(){
  let w = 0, s = 0;
  for (const c of ORDER){ const b = B[c]; w += (b.w || []).length; s += (b.w || []).reduce((t, x) => t + x[4].length * 2, 0) + (b.d || []).length + (b.dr || []).reduce((t, x) => t + x[2].length, 0); }
  const n = x => Number(x).toLocaleString("en-US");
  $("stats").replaceChildren(h("span", null, h("b", null, ORDER.length), "묶음"), h("span", null, h("b", null, n(w)), "단어"), h("span", null, h("b", null, n(s)), "문장"));
}
const SEP = new Set([1, 7, HELP]);    // | before 기초회화, TOEIC, 도움말 and after 도움말 (RYU)
function drawGroups(){
  const cur = S.code === "help" ? HELP : gOf(S.code);
  const btns = G.map((g, i) => h("button", {class: "group" + (SEP.has(i + 1) ? " sep" : ""), type: "button", "aria-pressed": cur === i + 1 ? "true" : "false",
    onclick: () => go(S.lastA[i + 1] && at.has(S.lastA[i + 1]) ? S.lastA[i + 1] : g[1][0][1][0])}, h("span", {class: "gn"}, g[0])));
  btns.push(h("button", {class: "group sep", type: "button", "aria-pressed": cur === HELP ? "true" : "false", onclick: () => go("help")}, h("span", {class: "gn"}, "도움말")));
  $("groups").replaceChildren(h("span", {class: "gsep", "aria-hidden": "true"}), ...btns);
}
function drawSubs(){
  if (S.code === "help"){ $("subs").replaceChildren(); $("sinfo").replaceChildren(h("b", null, "도움말"), " · 앱 쓰는 법"); return; }
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
$("bselBtn").addEventListener("click", () => {
  const l = $("bselList"); if (!l.hidden) return ddClose();
  l.hidden = false; $("bselBtn").setAttribute("aria-expanded", "true");
  const on = l.querySelector('[aria-selected="true"]'); if (on) l.scrollTop = on.offsetTop - l.clientHeight / 2 + on.offsetHeight / 2;
});
document.addEventListener("click", ev => { if (!ev.target.closest("#bsel")) ddClose(); });
function drawBand(b){
  $("bandin").replaceChildren($("bsel"),
    b.i ? h("p", {class: "intro"}, b.i) : null,
    b.tp && b.tp.length ? h("div", {class: "tipbox"}, b.tp.map(t => h("p", null, "• " + t))) : null);
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
const gloss = g => g && g.length ? h("div", {class: "gl"}, "※ ", g.flatMap((x, j) => [j ? " · " : null, h("span", {class: "en"}, x[0]), " (", h("span", {class: "gm"}, x[1]), ")"])) : null;
const sec = (title, extra, ...kids) => kids.flat(9).filter(Boolean).length ? h("section", {class: "sec"}, h("h3", null, title, extra), kids) : null;
const lbl = (b, k) => (b.wl || ["손님", "직원"])[k];
function wordBox(b, w){
  const head = h("div", {class: "line head", "data-say": w[0], "data-who": "S"}, spk(),
    h("div", null, h("div", {class: "k"}, w[0]), w[1] ? h("div", {class: "p"}, w[1]) : null, h("div", {class: "m"}, w[2]), w[3] ? h("span", {class: "lvl"}, LV[w[3]] || w[3]) : null),
    h("button", {class: "wrep", type: "button", onclick: ev => playEls([...ev.currentTarget.closest(".word").querySelectorAll("[data-say]")])}, ico("rep"), "단어 반복"));
  const wa = (b.ww || ["G", "S"]);
  const rows = w[4].map((p, n) => h("div", {class: "line ex pairx", "data-say": p[0], "data-who": wa[0], "data-say2": p[2], "data-who2": wa[1]},
    h("div", {class: "exn"}, String(n + 1)), spk(),
    h("div", null,
      h("div", {class: "turn g"}, h("span", {class: "who"}, lbl(b, 0)), h("div", {class: "k"}, b.nohw ? p[0] : hw(p[0], w[0])), h("div", {class: "m"}, p[1])),
      h("div", {class: "turn s"}, h("span", {class: "who"}, lbl(b, 1)), h("div", {class: "k"}, b.nohw ? p[2] : hw(p[2], w[0])), h("div", {class: "m"}, p[3])),
      gloss(p[4]))));
  return h("div", {class: "word"}, head, h("div", {class: "exs"}, rows));
}
function dlgBox(b){
  return h("div", {class: "rows dlg"}, b.d.map((d, n) => h("div", {class: "line " + (MALE.has(d[0]) ? "gu" : "st"), "data-say": d[1], "data-who": d[0]},
    h("div", {class: "exn"}, String(n + 1)), spk(),
    h("div", null, h("div", {class: "k"}, h("span", {class: "who"}, (b.dn && b.dn[d[0]]) || WHO[d[0]] || d[0]), d[1]), h("div", {class: "m"}, d[2]), gloss(d[3])))));
}
function drillBox(d){
  return h("div", {class: "drill"}, h("div", {class: "dpat"}, h("b", null, d[0]), h("span", null, d[1])),
    h("div", {class: "rows"}, d[2].map(s => h("div", {class: "line", "data-say": s[0], "data-who": "S"}, spk(), h("div", null, h("div", {class: "k"}, s[0]), h("div", {class: "m"}, s[1]))))));
}
function qaBox(q, n){
  const a = h("div", {class: "a", hidden: true}, q[1]);
  return h("div", {class: "qa"}, h("div", {class: "qq"}, h("div", {class: "exn"}, String(n + 1)), h("div", null, q[0])),
    h("div", {class: "qr"}, a, h("button", {class: "btn", type: "button", onclick: ev => { a.hidden = !a.hidden; ev.currentTarget.textContent = a.hidden ? "답 보기" : "답 숨기기"; }}, "답 보기")));
}
/* TOEIC: [part, question, [choices], answer index, explanation, script?]  Part 1–4 are listening: text hidden until 듣기 문제 영어 보기 */
const isLis = p => /^Part [1-4]/.test(p);
function tqBox(q, n){
  /* real test: Part 1 shows the photo only (here a Korean description), Part 2 shows nothing, Part 3·4 print the question and choices but not the script */
  const lis = isLis(q[0]), L = "ABCD", p34 = /^Part [34]/.test(q[0]), p1 = /^Part 1/.test(q[0]);
  const sayTxt = p34 ? q[5] + " " + q[1] : q[5] ? q[5] : q[1] + " " + q[2].map((c, j) => L[j] + ". " + c).join(" ");
  const why = h("p", {class: "twhy", hidden: true});
  const box = h("div", {class: "tq" + (lis ? " lis" : "") + (p34 ? " p34" : ""), "data-say": lis ? sayTxt : null, "data-who": "A"},
    h("div", {class: "tqh"}, h("span", {class: "exn"}, String(n + 1)), h("span", {class: "tpart"}, q[0]), lis ? spk() : null),
    p1 && q[1] ? h("p", {class: "tdesc"}, "📷 " + q[1]) : null,
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
    pv ? h("button", {class: "pn pv", type: "button", onclick: () => go(pv)}, h("b", null, "← 이전 묶음"), h("small", null, "[" + pv + "] " + B[pv].t)) : h("span"),
    nx ? h("button", {class: "pn nx", type: "button", onclick: () => go(nx)}, h("b", null, "다음 묶음 →"), h("small", null, "[" + nx + "] " + B[nx].t)) : h("span"));
}
function renderLearn(b){
  const tShow = h("label", {class: "tshow"}, h("input", {type: "checkbox", id: "tShow", checked: document.body.classList.contains("show-lis") ? true : null,
    onchange: ev => document.body.classList.toggle("show-lis", ev.target.checked)}), "듣기 문제 영어 보기");
  const dlgRep = h("button", {class: "wrep hrep", type: "button", onclick: () => playEls($$("#view .dlg .line"))}, ico("rep"), "대화 반복");
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
    if (!(await say(tok, c.dataset.say, false))) return; await gap(300);
    c.classList.add("back"); if (c.dataset.ex){ if (!(await say(tok, c.dataset.ex, c.dataset.exm === "1"))) return; } else await gap(1200);
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
      return h("div", {class: "wcard", role: "button", tabindex: "0", "data-say": w[0], "data-ex": ex ? ex[0] : null, "data-exm": ex && MALE.has(wa[0]) ? "1" : "0", onclick: ev => playCard(ev.currentTarget)},
        h("span", {class: "spk", "aria-hidden": "true"}, ico("spk")),
        h("div", {class: "fr"}, h("div", {class: "k" + (w[0].length > 16 ? " xl" : w[0].length > 11 ? " long" : "")}, w[0]), w[1] ? h("div", {class: "p"}, w[1]) : null),
        h("div", {class: "bk"}, h("div", {class: "m"}, w[2]), ex ? h("div", {class: "ex"}, h("div", null, ex[0]), h("div", {class: "exm"}, ex[1])) : null)); })),
    h("div", {class: "rowbtns", style: "justify-content:center;margin-top:12px"}, h("button", {class: "wrep tbtn", type: "button", onclick: () => playCardsAll()}, ico("rep"), "단어 전체 듣기")),
    pnRow(b.code)];
}
async function playCardsAll(){
  stopPlay(); const tok = ++P.tok;
  for (const c of $$("#view .wcard")){
    if (tok !== P.tok) return; $$(".now").forEach(x => x.classList.remove("now")); c.classList.add("now"); c.scrollIntoView({block: "nearest", behavior: "smooth"});
    for (let k = 0; k < S.rep; k++){ c.classList.remove("back"); showPlayer(c.dataset.say); if (!(await say(tok, c.dataset.say, false))) return; await gap(700); c.classList.add("back"); await gap(1100); }
    c.classList.remove("back");
  }
  if (tok === P.tok) stopPlay();
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
  const head = q.kind === "listen" ? h("div", {class: "quizq listen", "data-say": q.it.en, "data-who": "S"}, h("button", {class: "btn primary", type: "button", onclick: ev => playEls([ev.currentTarget.parentNode])}, ico("spk"), " 듣기"))
    : q.kind === "blank" ? h("div", {class: "quizq qblank"}, h("div", {class: "qen"}, q.blank.pre, h("span", {class: "blank"}, "?"), q.blank.post), h("div", {class: "qlo"}, q.blank.ko))
    : q.kind === "mean" ? h("div", {class: "quizq qen"}, q.it.en) : h("div", {class: "quizq"}, q.it.ko);
  const lab = {mean: "뜻을 고르세요", en: "영어를 고르세요", listen: "듣고 뜻을 고르세요", blank: "빈칸에 알맞은 말을 고르세요"}[q.kind];
  return [h("div", null, head, h("p", {class: "quizp"}, lab + " · " + (quiz.at + 1) + " / " + quiz.qs.length)),
    h("div", {class: "choices"}, q.opts.map(o => h("button", {class: "choice" + (q.key === "en" ? " qen" : "") + (q.picked != null ? (o === q.a ? " right" : o === q.picked ? " wrong" : "") : ""), type: "button", disabled: q.picked != null,
      onclick: () => { q.picked = o; if (o === q.a) quiz.right++; render(); stopPlay(); const tok = ++P.tok; say(tok, q.kind === "blank" ? q.blank.full : q.it.en, false); }}, o))),
    q.picked != null ? h("div", {class: "rowbtns", style: "justify-content:flex-end"}, h("button", {class: "btn primary", type: "button", onclick: () => {
      stopPlay(); quiz.at++; render(); const nq = quiz.qs[quiz.at], el = document.querySelector(".quizq.listen"); if (nq && nq.kind === "listen" && el) playEls([el]); }}, "다음 →")) : null];
}

/* ---------- search ---------- */
let query = "";
function renderSearch(){
  const q = query.toLowerCase(), hits = [];
  const add = (code, en, ko) => hits.push({code, en, ko});
  for (const c of ORDER){ const b = B[c];
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
function renderHelp(){
  const art = h("article", {class: "info"}); art.innerHTML = DATA.help; return [art];
}

/* ---------- render and routing ---------- */
function render(){
  const view = $("view");
  if (query){ $("band").hidden = true; $("controls").hidden = true; view.replaceChildren(...renderSearch()); return; }
  if (S.code === "help"){ $("band").hidden = true; $("controls").hidden = true; view.replaceChildren(...renderHelp()); return; }
  $("band").hidden = false; $("controls").hidden = false;
  const b = B[S.code]; b.code = S.code;
  drawBand(b);
  $$(".seg button").forEach(x => x.setAttribute("aria-pressed", x.dataset.mode === S.mode ? "true" : "false"));
  $("playAll").hidden = S.mode !== "learn"; $("classRow").hidden = S.mode !== "learn";
  const parts = S.mode === "cards" ? renderCards(b) : S.mode === "quiz" ? renderQuiz(b) : renderLearn(b);
  view.replaceChildren(...parts.flat(9).filter(Boolean));
  if (S.mode === "cards") fitWords();
}
function fitWords(){ $$(".wcard .k").forEach(k => { let fs = parseFloat(getComputedStyle(k).fontSize); while (k.scrollWidth > k.clientWidth + 1 && fs > 12){ fs -= 1; k.style.fontSize = fs + "px"; } }); }
function go(code){ if (location.hash === "#" + code) route(); else location.hash = code; }
function route(){
  const c = decodeURIComponent(location.hash.replace(/^#/, ""));
  if (at.has(c) || c === "help") S.code = c;
  if (S.code !== "help"){ S.lastA[gOf(S.code)] = S.code; S.lastS[sOf(S.code)] = S.code; }
  stopPlay(); quiz = null; save();
  drawGroups(); drawSubs(); if (S.code !== "help") drawPicker(); render();
  window.scrollTo({top: 0});
}
addEventListener("hashchange", route);
$$(".seg button").forEach(b => b.addEventListener("click", () => { S.mode = b.dataset.mode; stopPlay(); save(); render(); }));
$("repSel").value = S.rep; $("rateSel").value = S.rate;
$("repSel").onchange = e => { S.rep = +e.target.value; save(); };
$("rateSel").onchange = e => { S.rate = +e.target.value; save(); };
$("playAll").addEventListener("click", () => playEls($$("#view [data-say]").filter(x => !x.closest(".tq"))));
for (const [id, c] of [["tKo", "hide-ko"], ["tEn", "hide-en"], ["tSt", "hide-st"]])
  $(id).onchange = e => { document.body.classList.toggle(c, e.target.checked); $$("#view .show").forEach(x => x.classList.remove("show")); };
/* tapping a hidden (blurred) text shows it; tapping a line plays it */
document.addEventListener("click", ev => {
  const b = ev.target.closest("button");
  const bl = ev.target.closest("#view .m, #view .k, #view .gm, #view .a, #view .tqq, #view .ot");
  if (bl && !(b && !b.classList.contains("topt")) && getComputedStyle(bl).filter !== "none"){ bl.classList.toggle("show"); ev.stopPropagation(); ev.preventDefault(); return; }
  if (b && b.classList.contains("spk") && !b.closest(".wcard")){ const el = b.closest("[data-say]"); if (el) playEls([el]); }
}, true);
let qt = 0;
$("q").addEventListener("input", e => { clearTimeout(qt); qt = setTimeout(() => { query = e.target.value.trim(); stopPlay(); render(); }, 150); });
document.addEventListener("keydown", e => { if (e.key === "Escape"){ stopPlay(); ddClose(); } });
drawStats();
if (location.hash && (at.has(decodeURIComponent(location.hash.slice(1))) || location.hash === "#help")) route(); else go(S.code);
