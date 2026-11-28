import shutil, re
# Builds the 호텔서비스 영어 app.
#   python3 build.py            -> ../preview/hoteleng_app.html (single file, check-in mp3 inlined)  +  ../site/ (GitHub Pages: index.html, app.js, data.js, audio/)
# Content: content/m1.py … m8.py (class bundles), source words from ../data/phe_areas.json (Practical Hotel English, copied, not changed).
import hashlib, json, os, re, sys, base64, hashlib, importlib, html
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H); sys.path.insert(0, os.path.join(H, "content"))
from ipa import ipa
import shell_parts as SP
CSS = open(os.path.join(H, "korapp_v252.css"), encoding="utf8").read()
# numbered drill lines (RYU 2026-11-24): .nrows gets every .dlg .line rule (number badge column, speaker column)
def _nrows(css):
    def fix(m):
        sels = [x for x in m.group(1).split(",")]
        add = [x.replace(".dlg .line", ".nrows .line") for x in sels if ".dlg .line" in x]
        return ",".join(sels + add) + "{"
    return re.sub(r"([^{}]+)\{", fix, css)
CSS = _nrows(CSS)
SRC = {a["id"]: a for a in json.load(open(os.path.join(H, "..", "data", "phe_areas.json"), encoding="utf8"))}
WORD = {(a, w[0]): w for a in SRC for w in SRC[a]["words"]}
LVL = {"하": "초급", "중": "중급", "상": "실무"}

MENUS = [("기초회화", "m1"), ("호텔기본", "m2"), ("프런트", "m3"), ("객실·시설", "m4"), ("식음료", "m5"), ("고객응대·실무", "m6"), ("TOEIC", "m7"), ("영어면접", "m8")]
IPA_FIX = {}
used = set()

def word_entry(x, notes=None):
    """x = (area, word) | (area, word, [pair idx]) | (area, word, [idx], ipa/ko overrides dict) | full: [word, ipa|None, ko, lv, [[ge,gk,se,sk,(notes)]]]"""
    if isinstance(x, dict): x = x["w"]
    if isinstance(x[0], str) and x[0] in SRC and len(x) <= 4 and (len(x) < 3 or isinstance(x[2], (list, tuple))):
        area, w = x[0], x[1]
        src = WORD[(area, w)]; used.add((area, w))
        idx = x[2] if len(x) > 2 else [0, 1]
        ov = x[3] if len(x) > 3 else {}
        pairs = [list(src[3][i][:4]) + ([ov["n"][k]] if "n" in ov and k < len(ov["n"]) and ov["n"][k] else []) for k, i in enumerate(idx)]
        return [w, ov.get("ipa") or IPA_FIX.get(w) or ipa(w) or "", ov.get("ko", src[1]), LVL[src[2]], pairs]
    w, p, ko, lv, pairs = x
    return [w, p if p is not None else (ipa(w) or ""), ko, LVL.get(lv, lv), [list(q) for q in pairs]]

# ---------- voices by what the sentences say (RYU 2026-11-23) ----------
# Staff calling the guest ma'am / Ms. Kim -> a woman guest; sir / Mr. Kim -> a man. "my wife" -> the speaker is a man, "my husband" -> a woman.
# Two women (or two men) talking: the first speaker gets the second voice (f2 / m2) so they sound different.
VOC = r"(?:^|[,.!?]\s*|\b(?:Thank you|Hello|Hi|Good (?:morning|afternoon|evening)|Welcome(?: back)?|Excuse me|Sorry|Of course|Certainly|Yes|No problem),?\s+)"
def _voc(t, fem):
    w = (r"(?:ma'am|madam|(?:Ms|Mrs)\.\s+[A-Z]\w+|" + NAMES_F + ")") if fem else (r"(?:sir|Mr\.\s+[A-Z]\w+|" + NAMES_M + ")")
    return bool(re.search(r"\b(?:Thank you|Thanks|Hello|Hi|Hey|Bye|Good (?:morning|afternoon|evening)|Welcome(?: back)?|Excuse me|Sorry|Of course|Certainly|Yes|No problem|Nice to meet you(?:, too)?|See you),?\s+" + w + r"\s*[.,!?]", t)) or bool(re.search(r",\s+" + w + r"\s*[.!?]", t))
NAMES_F = "Jisu|Sarah|Sora|Mina|Minji|Siobhan|Seoyeon|Jiwoo|Anna|Emma|Yuna|Hana|Jenny|Amy|Lisa|Emily"
NAMES_M = "Minho|Tom|Daniel|Jun|Junho|Mark|John|David|James|Mike|Kevin|Brian|Hyunwoo|Sam"
def _self(t, fem):
    nm = NAMES_F if fem else NAMES_M
    if re.search(r"\b(?:I'm|I am|This is|[Nn]ame is|[Cc]all me)\s+(?:" + nm + r")\b", t): return True
    return bool(re.search(r"\bmy (?:husband|boyfriend)\b|\bI'm (?:Ms|Mrs)\.", t) if fem else re.search(r"\bmy (?:wife|girlfriend)\b|\bI'm Mr\.", t))
def _sex(v): return "m" if v.startswith("m") else "f"
def pair_voices(t1, t2, v1, v2):
    """clues in the words decide; a speaker with no clue gets the other sex from the one with a clue (unknown pairs keep the default man / woman)"""
    g1 = g2 = None
    if _voc(t2, True) or _self(t1, True): g1 = "f"
    elif _voc(t2, False) or _self(t1, False): g1 = "m"
    if _voc(t1, True) or _self(t2, True): g2 = "f"
    elif _voc(t1, False) or _self(t2, False) or (re.search(r"speak (?:to|with) Mr\.", t1) and re.match(r"Speaking", t2)): g2 = "m"
    if re.search(r"speak (?:to|with) (?:Ms|Mrs)\.", t1) and re.match(r"Speaking", t2): g2 = "f"
    opp = {"m": "f", "f": "m"}
    if g1 is None and g2 is None: g1, g2 = _sex(v1), _sex(v2)
    elif g1 is None: g1 = opp[g2] if _sex(v1) == g2 and (v1, v2) != (v1, v1) else _sex(v1)
    elif g2 is None: g2 = opp[g1] if _sex(v2) == g1 else _sex(v2)
    a, b = g1, g2
    if a == b: a += "2"
    return a, b
MALE_W = {"G", "A", "I"}
def dv(w): return "m" if w in MALE_W else "f"
def voice_pass(b):
    ww = b.get("ww", ["G", "S"]); vo = dict(b.get("vo", {}))
    d1, d2 = vo.get(ww[0], dv(ww[0])), vo.get(ww[1], dv(ww[1]))
    pv = {}
    for i, w in enumerate(b.get("w", [])):
        for j, p in enumerate(w[4]):
            a, c = pair_voices(p[0], p[2], d1, d2)
            if (a, c) != (d1, d2): pv[f"{i}.{j}"] = [a, c]
    if pv: b["pv"] = pv
    # dialogue: who speaks to whom is read from the whole dialogue
    d = b.get("d", [])
    whos = sorted({x[0] for x in d})
    if len(whos) == 2 and "vo" not in b:
        sex = {w: _sex(dv(w)) for w in whos}
        for w in whos:
            other = [x[1] for x in d if x[0] != w]; mine = [x[1] for x in d if x[0] == w]
            fem = sum(_voc(t, True) for t in other) + sum(_self(t, True) for t in mine)
            mal = sum(_voc(t, False) for t in other) + sum(_self(t, False) for t in mine)
            if fem > mal: sex[w] = "f"
            elif mal > fem: sex[w] = "m"
        x, y = whos
        v = {x: sex[x], y: sex[y]}
        if sex[x] == sex[y]:
            first = d[0][0]; second = y if first == x else x
            # the guest / first speaker takes the second voice, the staff keeps the main one
            tgt = "G" if "G" in whos else ("A" if "A" in whos else first)
            v[tgt] += "2"
        auto = {k: val for k, val in v.items() if val != dv(k)}
        if auto: b["vo"] = auto

def norm_bundle(b):
    o = {"t": b["t"], "en": b.get("en", "")}
    for k in ("nohw", "i", "tp", "dt", "wt", "drt", "tqt", "sm", "rel", "wl", "ww", "dn", "ord", "vo", "tqpart", "tqk", "mk"):
        if k in b: o[k] = b[k]
    if "d" in b: o["d"] = [list(d) + ([] if len(d) > 3 else [[]]) for d in b["d"]]
    if "w" in b: o["w"] = [word_entry(x) for x in b["w"]]
    if "dr" in b: o["dr"] = [[d[0], d[1], [list(s) for s in d[2]]] for d in b["dr"]]
    if "qa" in b: o["qa"] = [list(q) for q in b["qa"]]
    if "tq" in b: o["tq"] = [list(q) for q in b["tq"]]
    return o

def self_bundles(sub_name, areas):
    """leftover source words of these areas -> self-study bundles of ~10 words (all source pairs)"""
    out = []
    for a in areas:
        left = [w for w in SRC[a]["words"] if (a, w[0]) not in used]
        for w in left: used.add((a, w[0]))
        left.sort(key=lambda w: "하중상".index(w[2]))
        n = max(1, round(len(left) / 10)) if left else 0
        if not n: continue
        size = -(-len(left) // n)
        for k in range(n):
            chunk = left[k * size:(k + 1) * size]
            if not chunk: continue
            lv = sorted({LVL[w[2]] for w in chunk}, key=["초급", "중급", "실무"].index)
            nm = SRC[a]["ko"]
            # words are sorted by level, so two parts = basic words, then harder ones (RYU 2026-11-23: own titles)
            KO = {2: ["기본", "심화"], 3: ["기본", "중급", "심화"], 4: ["기본 1", "기본 2", "심화 1", "심화 2"]}; EN = {2: ["Basics", "Advanced"], 3: ["Basics", "Intermediate", "Advanced"], 4: ["Basics 1", "Basics 2", "Advanced 1", "Advanced 2"]}
            named = n in KO
            sfx = KO[n][k] if named else str(k + 1) if n > 1 else ""
            esfx = EN[n][k] if named else str(k + 1) if n > 1 else ""
            out.append({"t": f"{nm} {sfx} 표현" if named else f"{nm} 표현 더 익히기 {sfx}" if n > 1 else f"{nm} 표현 더 익히기", "en": SRC[a]["en"] + (f": {esfx}" if named else f" {esfx}" if n > 1 else ""),
                        "i": f"{nm} 장면에서 자주 쓰는 단어 {len(chunk)}개를 손님·직원 예문으로 더 익힙니다. 수준: {'·'.join(lv)}.",
                        "w": [[w[0], IPA_FIX.get(w[0]) or ipa(w[0]) or "", w[1], LVL[w[2]], [list(p[:4]) for p in w[3]]] for w in chunk], "self": 1})
    return out

# ---------- one class bundle -> two bundles with 5-8 dialogue lines (content/splits.py, RYU 2026-11-23) ----------
from splits import SPLIT
def _stem(w): return re.sub(r"[^a-z ]", "", w.lower()).split()
def _uses(word, text):
    t = " " + re.sub(r"[^a-z0-9 ]", " ", text.lower()) + " "
    ws = _stem(word)
    if not ws: return False
    return all(re.search(r"\b" + re.escape(x[:max(3, len(x) - 2)]), t) for x in ws if len(x) > 2) if any(len(x) > 2 for x in ws) else (" " + " ".join(ws) + " ") in t
def split_bundle(b):
    sp = SPLIT.get(b["t"])
    if not sp or not b.get("d"): return [b]
    d = [list(x) for x in b["d"]]
    for i, x in (sp.get("edit") or {}).items(): d[i] = list(x) + ([] if len(x) > 3 else [[]])
    fix = lambda L: [list(x) + ([] if len(x) > 3 else [[]]) for x in L]
    d1 = d[:sp["cut"]] + fix(sp.get("end1", []))
    d2 = fix(sp["d2"]) if sp.get("d2") else fix(sp.get("start2", [])) + d[sp["cut"]:]
    t1 = " ".join(x[1] for x in d1); t2 = " ".join(x[1] for x in d2)
    w1, w2, rest = [], [], []
    for w in b.get("w", []):
        u1, u2 = _uses(w[0], t1), _uses(w[0], t2)
        (w1 if u1 and not u2 else w2 if u2 and not u1 else rest).append(w)
    for w in rest: (w1 if len(w1) <= len(w2) else w2).append(w)
    order = {id(w): i for i, w in enumerate(b.get("w", []))}
    w1.sort(key=lambda w: order[id(w)]); w2.sort(key=lambda w: order[id(w)])
    half = lambda L: (L[:(len(L) + 1) // 2], L[(len(L) + 1) // 2:])
    a, c = dict(b), dict(b)
    # each half is named after its own dialogue (RYU 2026-11-23); EN_T holds the English names
    from splits import EN_T
    a["t"], c["t"] = sp["dt"]
    a["en"], c["en"] = (EN_T.get(sp["dt"][0], b.get("en", "") + " 1"), EN_T.get(sp["dt"][1], b.get("en", "") + " 2"))
    a["dt"], c["dt"] = sp["dt"]
    a["d"], c["d"] = d1, d2
    a["w"], c["w"] = w1, w2
    for k in ("dr", "qa", "tq"):
        if b.get(k): a[k], c[k] = half(b[k])
    for x in (a, c):
        for k in ("w", "dr", "qa", "tq"):
            if k in x and not x[k]: del x[k]
    a["_sib"], c["_sib"] = 1, -1
    return [a, c]

REMAP = {}
# ---------- TOEIC question bank (RYU 2026-11-23: TOEIC 메뉴만 10배, Part별 묶음에서 무작위 출제) ----------
def _mix(q):
    """bank questions are written with the answer first; choices are put in a fixed shuffled order"""
    opts = list(q[2]); n = len(opts)
    k = int(hashlib.md5((q[1] + opts[0]).encode()).hexdigest(), 16)
    order = list(range(n))
    for i in range(n - 1, 0, -1):
        j = k % (i + 1); k //= (i + 1); order[i], order[j] = order[j], order[i]
    return (q[0], q[1], [opts[i] for i in order], order.index(q[3])) + tuple(q[4:])
def add_bank(bundles):
    from tqbank import BANK
    allq = [_mix(q) for p in sorted(BANK) for q in BANK[p]]
    for b in bundles.values():
        tp = b.get("tqpart")
        if not tp: continue
        if tp == "all":   # 미니 모의고사: same number per Part as the original test, drawn from every Part bank
            k = {}
            for q in b["tq"]: p = q[0].split(" ·")[0]; k[p] = k.get(p, 0) + 1
            b["tqk"] = b.get("tqk") or k; b["tq"] = list(b["tq"]) + allq
        else:
            b["tqn"] = len(b["tq"])   # RYU: show the original number (e.g. Part 1: 3 of 16), drawn from the bank
            b["tq"] = list(b["tq"]) + [_mix(q) for q in BANK.get(tp, [])]
        b.pop("tqpart", None)

def build():
    groups, bundles = [], {}
    for gi, (gname, mod) in enumerate(MENUS, 1):
        try: M = importlib.import_module(mod)
        except ModuleNotFoundError: M = None
        subs = []
        if M:
            for si, sub in enumerate(M.SUBS, 1):
                codes = []
                items = []
                for oi, b in enumerate(sub["b"], 1):
                    for k, x in enumerate(split_bundle(norm_bundle(b))): x["_oi"] = oi; x["_first"] = k == 0; items.append(x)
                subs.append((sub, items))
        # self-study after every class bundle of the app is known (so `used` is complete) -> second pass
        if not subs: subs = [({"n": "준비 중"}, [{"t": "준비 중", "en": "", "i": "이 메뉴는 준비 중입니다."}])]
        groups.append([gname, subs])
    out_groups = []
    for gi, (gname, subs) in enumerate(groups, 1):
        og = []
        for si, (sub, items) in enumerate(subs, 1):
            n_old = max([x.get("_oi", 0) for x in items] + [0])
            selfs = [norm_bundle(x) | {"self": 1} if "self" not in x else x for x in self_bundles(sub["n"], sub.get("self", []))]
            for k, x in enumerate(selfs, 1): x["_oi"] = n_old + k; x["_first"] = True
            items = items + selfs
            codes = []
            for bi, b in enumerate(items, 1):
                c = f"{gi}-{si:02d}-{bi:02d}"; bundles[c] = b; codes.append(c)
                if b.get("_first"): REMAP[f"{gi}-{si:02d}-{b['_oi']:02d}"] = c
            og.append([sub["n"], codes])
        out_groups.append([gname, og])
    # related bundles were written with the codes before the split: point them at the new codes, and join the two halves
    allc = list(bundles)
    TCODE = {}
    for c in allc: TCODE.setdefault(bundles[c]["t"], c)   # "@title": the bundle with this title (survives moving bundles between subs)
    def _rc(r):
        if r.startswith("@"):
            if r[1:] not in TCODE: raise SystemExit("rel: no bundle titled " + r[1:])
            return TCODE[r[1:]]
        return r[1:] if r.startswith("=") else REMAP.get(r, r)
    for i, c in enumerate(allc):
        b = bundles[c]
        rel = [_rc(r) for r in b.get("rel", [])]   # "=code": already a final code; "@title": by title
        sib = b.pop("_sib", 0)
        if sib: rel = [allc[i + sib]] + [r for r in rel if r != allc[i + sib]]
        if rel: b["rel"] = rel
        for k in ("_oi", "_first"): b.pop(k, None)
    unused = [k for k in WORD if k not in used]
    # 도움말: the last menu, sub-tabs and bundles like the other menus (RYU 2026-11-23, like kor-app / lao-app)
    hm = importlib.import_module("m9"); hg = len(out_groups) + 1; og = []
    for si, sub in enumerate(hm.SUBS, 1):
        codes = []
        for bi, x in enumerate(sub["b"], 1):
            c = f"{hg}-{si:02d}-{bi:02d}"; bundles[c] = {"t": x["t"], "en": x["en"], "info": _shots(x["info"].strip())}; codes.append(c)
        og.append([sub["n"], codes])
    out_groups.append(["도움말", og])
    add_bank(bundles)
    from pics import PICS   # TOEIC Part 1 drawings (RYU 2026-11-23)
    used_q = {q[1] for b in bundles.values() for q in b.get("tq", []) if len(q) > 1}
    # bundle pictures (RYU 2026-11-24): b["sc"] = scene key, drawings in DATA.sc
    from scenes import S as SCENES, scene_of
    used_sc = set()
    for gname, og in out_groups:
        for sname, codes in og:
            for c in codes:
                b = bundles[c]
                if b.get("info") or b.get("mk"): continue
                k = scene_of(gname, sname, b["t"])
                if k: b["sc"] = k; used_sc.add(k)
    return {"g": out_groups, "b": bundles, "pics": {k: v for k, v in PICS.items() if k in used_q}, "sc": {k: SCENES[k] for k in sorted(used_sc)}}, unused

def mp3_dir():
    """the mp3 clips live in ../audio/mp3.tar (RYU 2026-11-26: one file instead of 14,000 in the project folder);
    unpacked once to local disk (/tmp/mp3cache) and reused. HOTELENG_MP3 = use that folder instead.
    Without the tar, the clips are taken out of the audio packs ../audio/p/*.bin (byte for byte the same mp3)."""
    if os.environ.get("HOTELENG_MP3"): return os.environ["HOTELENG_MP3"]
    tar = os.path.join(H, "..", "audio", "mp3.tar")
    # no mp3.tar (it is not in the repository): mp3tar.path takes the clips back out of audio/p/*.bin (2026-11-28)
    sys.path.insert(0, "/mnt/project-files/tools"); sys.path.insert(0, os.path.join(H, "..", "tools")); import mp3tar
    return mp3tar.path(tar)

def audio_map(data, inline):
    """mp3 clips that exist in ../audio (made by make_audio.py) -> {key: url or data-uri}"""
    adir = os.path.join(H, "..", "audio"); m = {}
    if not os.path.isdir(adir): return m
    idx = json.load(open(os.path.join(adir, "index.json"), encoding="utf8")) if os.path.exists(os.path.join(adir, "index.json")) else {}
    mdir = mp3_dir()
    for key, fn in idx.items():
        p = os.path.join(mdir, fn)
        if not os.path.exists(p): continue
        m[key] = ("data:audio/mpeg;base64," + base64.b64encode(open(p, "rb").read()).decode()) if inline else "audio/" + fn
    return m

# Audio packs (RYU 2026-11-25: "파일의 개수가 만개가 넘어가니 묶음마다 묶어서 개수를 줄여서", same plan as kor-app v2.65 tools/audiopack.js):
# ../audio/p/<code>.bin = 4-byte little-endian header length N, N bytes of JSON [[clip id, offset, length], ...], then the mp3 bytes
# (each slice is the mp3 file byte for byte). A clip used by several bundles is in each of their packs, so opening a bundle needs
# one file; the two 모의고사 bundles (they draw from every Part) only hold clips that have no other home.
# Returns (packs [[code, hash], ...], home {clip id: pack number}). The site and the repository carry only the packs, not the mp3 files.
def audio_packs(data, aud):
    import hashlib, struct, subprocess
    adir = os.path.join(H, "..", "audio"); pdir = os.path.join(adir, "p"); os.makedirs(pdir, exist_ok=True)
    codes = [c for c, x in data["b"].items() if not x.get("info")]
    codes.sort(key=lambda c: 1 if data["b"][c].get("tqk") else 0)
    by = json.loads(subprocess.run(["node", os.path.join(H, "clips.js"), "--by", *codes], capture_output=True, text=True, check=True, cwd="/tmp").stdout)
    packs, home, keep = [], {}, set()
    # reading 14,000 mp3 files from the project folder takes very long: a pack whose clip list did not change is reused without
    # reading anything (audio/packs.json: code -> [hash of the clip list, hash of the pack]); HOTELENG_MP3 = a faster copy of the mp3 folder
    src = mp3_dir()
    cpath = os.path.join(adir, "packs.json"); cache = json.load(open(cpath)) if os.path.exists(cpath) else {}
    for code in codes:
        ids = []
        for v, t in by[code]:
            u = aud.get(v + "|" + t.strip())
            if not u: continue
            i = u.split("/")[-1][:-4]
            if i not in ids and not (data["b"][code].get("tqk") and i in home): ids.append(i)
        if not ids: continue
        fn = os.path.join(pdir, code + ".bin"); keep.add(code + ".bin")
        kh = hashlib.sha1(",".join(ids).encode()).hexdigest()[:12]
        if not (code in cache and cache[code][0] == kh and os.path.exists(fn)):
            table, parts, off = [], [], 0
            for i in ids:
                d = open(os.path.join(src, i + ".mp3"), "rb").read(); table.append([i, off, len(d)]); parts.append(d); off += len(d)
            head = json.dumps(table, separators=(",", ":")).encode()
            buf = struct.pack("<I", len(head)) + head + b"".join(parts)
            open(fn, "wb").write(buf)
            cache[code] = [kh, hashlib.sha1(buf).hexdigest()[:8]]; json.dump(cache, open(cpath, "w"))
            print("pack", code, len(ids), len(buf), flush=True)
        for i in ids: home.setdefault(i, len(packs))
        packs.append([code, cache[code][1]])
    for f in os.listdir(pdir):
        if f.endswith(".bin") and f not in keep: os.remove(os.path.join(pdir, f))
    return packs, home

TAB_JS = '<script>(function(){var n=navigator,t=n.maxTouchPoints>0||"ontouchstart" in window;if((/iPad/.test(n.userAgent)||(/Macintosh/.test(n.userAgent)&&t))||(t&&Math.min(screen.width,screen.height)>=700))document.documentElement.classList.add("tab")})()</script>'
# app screenshots inside the help pages (RYU 2026-11-25): [[shot:name|caption]] in content/m9.py, pictures in src/helpshots/*.webp
# (made by helpshots.js from the built site; "name+" = a wide PC picture). Inlined so the help works offline and in the preview.
def _shots(html):
    def one(m):
        n, cap = m.group(1), m.group(2); wide = n.endswith("+"); n = n.rstrip("+")
        d = base64.b64encode(open(os.path.join(H, "helpshots", n + ".webp"), "rb").read()).decode()
        return '<figure class="hshot%s"><img alt="%s" loading="lazy" src="data:image/webp;base64,%s"><figcaption>%s</figcaption></figure>' % (" wide" if wide else "", cap, d, cap)
    return re.sub(r"\[\[shot:([a-z+]+)\|([^\]]*)\]\]", one, html)
# link preview in KakaoTalk etc. (RYU 2026-11-28): og.jpg made from the intro photo + mascot, copied next to index.html
OG_TAGS = ('<meta property="og:type" content="website"><meta property="og:site_name" content="HotelEng"><meta property="og:url" content="https://hoteleng.pages.dev/">'
  '<meta property="og:title" content="HotelEng · 호텔서비스 영어"><meta property="og:description" content="Hotel Service English · 호텔 현장에서 바로 쓰는 영어, 주제별로 쉽게">'
  '<meta property="og:image" content="https://hoteleng.pages.dev/og.jpg?v=1"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
  '<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="https://hoteleng.pages.dev/og.jpg?v=1">')
def shell(head_extra, body_scripts, n_b):
    return f'''<title>HotelEng · 호텔서비스 영어</title>
<meta name="claude:viewport-fit-sides" content="cover">
{head_extra}
{TAB_JS}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=IBM+Plex+Sans+KR:wght@400;500;600&display=swap">
<style>{CSS}{SP.EXTRA_CSS}{APP_CSS}{SKIN_CSS}{HE_CSS}</style>
<script>window.HE_HASH0=location.hash</script>
<div class="wrap" id="app" data-g="K1">
  <header class="top"><svg class="hart" viewBox="120 0 250 124" preserveAspectRatio="xMaxYMax meet" fill="none" stroke="#fff" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M120 122h250"/><path d="M188 122V24h82v98M188 24l41-14 41 14M229 10V2M222 4h14"/><path d="M132 122V52h56M270 52h56v70M132 52h-6M326 52h6"/><path d="M218 122v-16a11 11 0 0 1 22 0v16M206 100h46"/><g stroke-width=".9" fill="#fff" fill-opacity=".28"><rect x="196" y="34" width="7" height="9"/><rect x="209" y="34" width="7" height="9"/><rect x="222" y="34" width="7" height="9"/><rect x="235" y="34" width="7" height="9"/><rect x="248" y="34" width="7" height="9"/><rect x="261" y="34" width="7" height="9"/><rect x="196" y="50" width="7" height="9"/><rect x="209" y="50" width="7" height="9"/><rect x="222" y="50" width="7" height="9"/><rect x="235" y="50" width="7" height="9"/><rect x="248" y="50" width="7" height="9"/><rect x="261" y="50" width="7" height="9"/><rect x="196" y="66" width="7" height="9"/><rect x="209" y="66" width="7" height="9"/><rect x="222" y="66" width="7" height="9"/><rect x="235" y="66" width="7" height="9"/><rect x="248" y="66" width="7" height="9"/><rect x="261" y="66" width="7" height="9"/><rect x="196" y="82" width="7" height="9"/><rect x="209" y="82" width="7" height="9"/><rect x="222" y="82" width="7" height="9"/><rect x="235" y="82" width="7" height="9"/><rect x="248" y="82" width="7" height="9"/><rect x="261" y="82" width="7" height="9"/><rect x="196" y="98" width="7" height="9"/><rect x="209" y="98" width="7" height="9"/><rect x="222" y="98" width="7" height="9"/><rect x="235" y="98" width="7" height="9"/><rect x="248" y="98" width="7" height="9"/><rect x="261" y="98" width="7" height="9"/><rect x="140" y="62" width="6" height="8"/><rect x="153" y="62" width="6" height="8"/><rect x="166" y="62" width="6" height="8"/><rect x="284" y="62" width="6" height="8"/><rect x="297" y="62" width="6" height="8"/><rect x="310" y="62" width="6" height="8"/><rect x="140" y="77" width="6" height="8"/><rect x="153" y="77" width="6" height="8"/><rect x="166" y="77" width="6" height="8"/><rect x="284" y="77" width="6" height="8"/><rect x="297" y="77" width="6" height="8"/><rect x="310" y="77" width="6" height="8"/><rect x="140" y="92" width="6" height="8"/><rect x="153" y="92" width="6" height="8"/><rect x="166" y="92" width="6" height="8"/><rect x="284" y="92" width="6" height="8"/><rect x="297" y="92" width="6" height="8"/><rect x="310" y="92" width="6" height="8"/><rect x="140" y="107" width="6" height="8"/><rect x="153" y="107" width="6" height="8"/><rect x="166" y="107" width="6" height="8"/><rect x="284" y="107" width="6" height="8"/><rect x="297" y="107" width="6" height="8"/><rect x="310" y="107" width="6" height="8"/></g><path d="M352 122c0-14 1-26 3-36M355 86c-7-6-15-6-22-2M355 86c-2-8-9-13-17-13M355 86c5-7 12-10 20-8"/></svg>
    <div class="brand"><span class="eyebrow"><span class="logo">HotelEng</span>기초 회화부터 실무 영어·TOEIC·영어면접까지</span><h1>호텔서비스 영어</h1></div>
    <div class="stats" id="stats"></div>
  </header>
  <label class="search" for="q"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
    <input id="q" type="search" placeholder="영어나 뜻으로 검색 (예: deposit, 보증금)" autocomplete="off"></label>
  <div class="menubox"><nav class="groups" id="groups" aria-label="대분류"></nav><nav class="subs" id="subs" role="tablist" aria-label="소분류"></nav><div class="sinfo" id="sinfo"></div></div>
  <section class="sheet" id="sheet">
    <div class="band" id="band"><div class="bandin" id="bandin">
      <div class="dd" id="bsel"><button class="bsel ddb" id="bselBtn" type="button" aria-haspopup="listbox" aria-expanded="false" aria-label="묶음 고르기"></button><div id="bselList" class="ddl" role="listbox" hidden></div></div>
    </div></div>
    <div class="controls" id="controls">
      <div class="seg" role="group" aria-label="학습 방식">
        <button data-mode="learn" id="m-learn" type="button" aria-pressed="true"><span class="lg">문장보기</span><span class="sh">문장</span><kbd class="kc">S</kbd></button>
        <button data-mode="cards" id="m-cards" type="button" aria-pressed="false"><span class="lg">주요단어</span><span class="sh">단어</span><kbd class="kc">W</kbd></button>
        <button data-mode="quiz" id="m-quiz" type="button" aria-pressed="false"><span class="lg">복습퀴즈</span><span class="sh">퀴즈</span><kbd class="kc">E</kbd></button>
      </div>
      <div class="opts"><label class="ctl"><span class="replab">문장 재생 횟수<kbd class="kc">1~5</kbd></span><span class="repw"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m17 2 4 4-4 4"/><path d="M3 11v-1a4 4 0 0 1 4-4h14"/><path d="m7 22-4-4 4-4"/><path d="M21 13v1a4 4 0 0 1-4 4H3"/></svg><select id="repSel" class="bsel" aria-label="문장 재생 횟수"><option value="1">1회</option><option value="2">2회</option><option value="3">3회</option><option value="4">4회</option><option value="5">5회</option></select></span></label>
      <label class="ctl"><span>속도<kbd class="kc">±</kbd></span><select id="rateSel" class="bsel" aria-label="속도"><option value="0.7">×0.7</option><option value="0.8">×0.8</option><option value="0.9">×0.9</option><option value="1">×1.0</option><option value="1.1">×1.1</option><option value="1.2">×1.2</option><option value="1.3">×1.3</option><option value="1.4">×1.4</option><option value="1.5">×1.5</option></select></label></div>
      <div class="rowbtns ctlrep" id="ctlrep"><button class="wrep tbtn" type="button" id="playCont"><span class="ico" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="m17 2 4 4-4 4"/><path d="M3 11v-1a4 4 0 0 1 4-4h14"/><path d="m7 22-4-4 4-4"/><path d="M21 13v1a4 4 0 0 1-4 4H3"/></svg></span>연속 재생<kbd class="kc">C</kbd></button><button class="wrep tbtn" type="button" id="playAll"><span class="ico" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="m17 2 4 4-4 4"/><path d="M3 11v-1a4 4 0 0 1 4-4h14"/><path d="m7 22-4-4 4-4"/><path d="M21 13v1a4 4 0 0 1-4 4H3"/></svg></span>묶음 재생<kbd class="kc">G</kbd></button></div>
      <div class="kbinfo" id="kbinfo"><span><kbd class="kc">Space</kbd>일시정지·재개</span><span><kbd class="kc">Esc</kbd>정지</span><span><kbd class="kc">Enter</kbd>무한 반복</span><span><kbd class="kc">←</kbd>이전 문장</span><span><kbd class="kc">→</kbd>다음 문장</span><span><kbd class="kc">?</kbd>단축키 목록</span></div>
      <div class="class-row" id="classRow" aria-label="가리기">
        <label><input type="checkbox" id="tKo">한국어 뜻 가리기</label>
        <label><input type="checkbox" id="tEn">영어 가리기<span class="lnote"> (통역 연습)</span></label>
        <label><input type="checkbox" id="tSt">직원 대사 가리기<span class="lnote"> (역할극)</span></label></div>
    </div>
    <div class="body" id="view"></div>
  </section>
  <div class="player" id="player" hidden><span class="t" id="pt"></span><button id="ppause" type="button"><span class="pico" aria-hidden="true"><svg viewBox="0 0 24 24"><rect x="6" y="5" width="4" height="14" rx="1" fill="currentColor"/><rect x="14" y="5" width="4" height="14" rx="1" fill="currentColor"/></svg></span><span class="bt">일시정지</span></button><button id="pstop" type="button"><span class="pico" aria-hidden="true"><svg viewBox="0 0 24 24"><rect x="6" y="6" width="12" height="12" rx="1.5" fill="currentColor"/></svg></span><span class="bt">정지</span></button></div>
  <p class="foot" id="voiceNote">🔊 남자와 여자는 서로 다른 음성으로 들려줍니다. 녹음 파일이 없는 문장은 기기의 영어 음성으로 읽습니다.</p>
  <div class="svbox" id="svbox"></div>
  <div class="prefs" id="prefs"></div>
  <a class="hmlogo-a" href="http://hotel.jj.ac.kr" target="_blank" rel="noopener">{HMLOGO}</a>
  <p class="ver">HotelEng v{VERSION} · {VDATE} · Copyleft</p>
  <div class="stick" id="stick" hidden><div class="stin"><div class="strow"><b>HotelEng</b><span id="stickT"></span><button type="button" id="stickQ" aria-label="검색"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg></button></div><nav class="groups" id="stickG" aria-label="대분류"></nav></div></div>
</div>
{body_scripts}'''

VERSION = "1.77"
SKIN_CSS = open(os.path.join(H, "skin_a.css"), encoding="utf8").read()   # design A (RYU 2026-11-24)
# v1.68 HotelEng (RYU 2026-11-27): bottom prefs row, help boxes, stats/survey, intro page
HMLOGO = open(os.path.join(H, "hmlogo.svg"), encoding="utf8").read().strip()   # 호텔경영학과 logo (RYU 2026-11-27)
HE_CSS = open(os.path.join(H, "he.css"), encoding="utf8").read() + open(os.path.join(H, "stats.css"), encoding="utf8").read() + open(os.path.join(H, "intro.css"), encoding="utf8").read()
# release date in Korea, shown at the bottom as 호텔서비스영어(v1.17) 2026.11.23. (RYU 2026-11-23)
import datetime as _dt
VDATE = (_dt.datetime.utcnow() + _dt.timedelta(hours=9)).strftime("%Y.%m.%d.")
APP_CSS = '''
/* repeat icon inside the 횟수 box, like lao-app */
.repw{position:relative;display:inline-flex;flex:0 0 auto}
.repw svg{position:absolute;left:10px;top:50%;width:14px;height:14px;transform:translateY(-50%);pointer-events:none;color:var(--ink)}
.controls .repw .bsel{padding-left:30px}
/* phones: roomier controls like lao-app (RYU 2026-11-23) */
@media (max-width:560px){
  html:not(.tab) .controls{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;padding:14px 14px 12px;row-gap:12px;column-gap:6px}
  html:not(.tab) .controls .seg{width:auto;grid-column:auto}
  html:not(.tab) .controls .opts{margin-left:auto}
  html:not(.tab) .controls .seg{padding:4px;gap:4px}
  html:not(.tab) .controls .seg button{height:38px;font-size:15px;padding:0 13px}
  html:not(.tab) .controls .ctl .bsel{height:38px;font-size:15px;padding-right:24px;border-radius:999px}
  html:not(.tab) .controls .repw .bsel{padding-left:32px}
  html:not(.tab) .repw svg{width:16px;height:16px;left:11px}
  html:not(.tab) .controls .opts{gap:6px}
  html:not(.tab) .controls #ctlrep .tbtn{height:38px;font-size:14.5px;padding:0 14px}
  html:not(.tab) .controls .class-row{row-gap:8px}
}
@media (max-width:380px){
  html:not(.tab) .controls{padding-left:10px;padding-right:10px}
  html:not(.tab) .controls .seg button{padding:0 9px;font-size:14px}
  html:not(.tab) .controls .ctl .bsel{padding-right:20px}
  html:not(.tab) .controls .ctl .bsel{font-size:14px}
}
#sheet{will-change:auto}
.dlp{text-align:center;margin:4px 0 0;font-size:13px}.dla{color:var(--accent,#2f6f8f);font-weight:600;text-decoration:none}.dls{color:var(--mut,#6b7680);margin-left:6px;font-variant-numeric:tabular-nums}
/* bottom player: speaker, [code/n] i/n, icons in the buttons (RYU 2026-11-23, like lao-app) */
.player .pspk{display:inline-flex;vertical-align:-3px;margin-right:6px;color:#e0a33a}.player .pspk svg{width:17px;height:17px}
.player .pw{font-variant-numeric:tabular-nums;opacity:.85}
.player button{display:inline-flex;align-items:center;gap:5px}.player .pico{display:inline-flex}.player .pico svg{width:12px;height:12px}
#pstop{background:transparent;color:var(--bg);box-shadow:inset 0 0 0 1.5px var(--bg)}
/* word cards: every row centred, the last one too (RYU 2026-11-23) */
.wcards{display:flex;flex-wrap:wrap;justify-content:center;gap:10px}.wcards>.wcard{flex:0 0 calc((100% - 30px)/4);min-width:0}
@media(max-width:900px){.wcards>.wcard{flex-basis:calc((100% - 20px)/3)}}
@media(max-width:600px){.wcards{gap:8px}.wcards>.wcard{flex-basis:calc((100% - 8px)/2)}}
.tpic{margin:8px 0 6px;max-width:440px;border-radius:12px;overflow:hidden;border:1px solid var(--line,#d8dee3)}.tpic svg{display:block;width:100%;height:auto}
.tdescd{margin:2px 0 8px;font-size:.85em;color:var(--mut,#6b7680)}.tdescd summary{cursor:pointer}
.gl{font-size:13.5px!important;text-align:right}
.gl .en{font-weight:600;color:var(--ink)}
.drill .line .gl{margin-right:-50px}
.wrep.on{background:var(--rev);border-color:var(--accent);color:var(--ink)}
/* speakers share one right edge; repeat buttons sit at the box's right edge (RYU 2026-11-23) */
.wrep.hrep,.word .wrep,.wrep.drep{margin-right:0!important}
.drill .dpat{display:flex;align-items:center;flex-wrap:wrap;gap:4px 10px}
.drill .dpat .drep{margin-left:auto}
.wrep.drep{position:static;flex:none;display:inline-flex;align-items:center;gap:6px}
.sec .dlg .line,.sec .drill .rows .line{padding-right:14px!important}
/* less space between the title, search, menu and bundle boxes (RYU 2026-11-24) */
.wrap{gap:8px}
/* search box: the same corner radius as the other boxes, text centred (RYU 2026-11-24) */
.search input{border-radius:16px;text-align:center;padding-left:32px;padding-right:32px}
@media (max-width:640px){.top,.search input{border-radius:12px}}
/* 학습 목표 list: a little smaller and tighter (RYU 2026-11-24) */
.band .tipbox{font-size:14px;line-height:1.3;gap:3px;padding:8px 12px}
/* wrapped lines start where the text after the dot starts */
.band .tipbox p{display:flex;gap:.45em;padding-left:0;text-indent:0}.band .tipbox p .tb{flex:none}.band .tipbox p>span:last-child{min-width:0}
@media (max-width:560px){.band .tipbox{font-size:13.5px;padding:7px 10px}}
/* bundle picture left of the 학습 목표 box (RYU 2026-11-24) */
.bandrow{display:flex;gap:16px;align-items:flex-start;margin-top:8px}
.bandpic{flex:0 0 200px;border-radius:12px;overflow:hidden;border:1px solid var(--line);line-height:0;background:var(--sheet)}
.bandpic svg{display:block;width:100%;height:auto}
.bandtxt{flex:1 1 0;min-width:0}.bandtxt>:first-child{margin-top:0}
@media (max-width:600px){.bandrow{display:block}.bandrow::after{content:"";display:block;clear:both}.bandpic{float:left;width:120px;margin:2px 10px 6px 0;border-radius:10px}.bandtxt .tipbox{clear:both}}
/* 모의 면접 (RYU 2026-11-24) */
.mkpick{border:1px solid var(--line);border-radius:14px;padding:14px 16px;margin:16px 0 0}
.mkpt{font-weight:700;margin-bottom:8px}
.mkareas{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:0 24px}
.mkarea{display:flex;align-items:center;gap:8px;padding:6px 4px;cursor:pointer;line-height:1.3}
.mkarea input{width:18px;height:18px;margin:0;accent-color:var(--accent)}
.mkarea small{color:var(--muted);margin-left:auto;white-space:nowrap}
.mkgo{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-top:10px}
.mkrate{display:inline-flex;align-items:center;gap:8px;font-weight:600}
.mkstart{font-weight:700;background:var(--accent);color:var(--sheet);border-color:var(--accent)}
.mock[hidden]{display:none}
.mock{border:1px solid var(--line);border-radius:14px;overflow:hidden;margin:16px 0}
.mkhead{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:12px 16px;background:var(--accent-soft)}
.mkn{font-weight:700;color:var(--accent)}
.mkpart{padding:12px 16px;border-top:1px solid var(--line)}
.mkchk{display:inline-flex;align-items:center;gap:8px;font-weight:600;cursor:pointer}
.mkchk input{width:18px;height:18px;margin:0}
.mkbody{margin-top:10px}.mkbody[hidden]{display:none}
.mkbody .k{font-size:18px;line-height:1.5}.mkbody .m{color:var(--muted);margin-top:2px}
.mkline+.mkline{margin-top:10px}
.mkplay{display:inline-flex;align-items:center;gap:6px;font-weight:600;white-space:nowrap;flex:none}
.mkn{min-width:0}
@media (max-width:600px){.mkhead{padding:10px 12px}.mkn{font-size:14px;line-height:1.35}.mkplay{padding-left:10px;padding-right:10px}}.mkplay.on{background:var(--accent-soft);border-color:var(--accent)}
.mk-a .mkplay{margin-top:10px}
.mk-t .tip p{margin:4px 0}
.mkfoot{padding:14px 16px;border-top:1px solid var(--line);display:flex;justify-content:space-between;align-items:flex-end;gap:12px}
.mkpic{flex:0 1 250px;min-width:0}.mkpic svg{display:block;width:100%;height:auto}
@media (max-width:600px){.mkpic{flex-basis:170px}}
.mknext{font-weight:700}
/* one side of every dialogue (면접관·손님·A) gets a faint tint so the two speakers are easy to tell apart (RYU 2026-11-24) */
.dlg .line.gu{background:color-mix(in srgb,var(--accent-soft) 45%,var(--sheet))}
.dlg .line.gu.now,.dlg .line.now{background:var(--accent-soft)}
.drill .nrows .line{grid-template-columns:24px minmax(0,1fr) 38px;column-gap:12px}.drill .nrows .line>.exn{grid-column:1;grid-row:1}.drill .nrows .line>div:not(.exn){grid-column:2;grid-row:1}.drill .nrows .line>.spk{grid-column:3;grid-row:1}
@media (max-width:600px){.drill .nrows .line{grid-template-columns:22px minmax(0,1fr) 34px;column-gap:10px}}
.sec .exs .line{padding-right:15px!important}
.drill .dpat{padding-right:0}
.drill .line>.spk{justify-self:end}
@media (max-width:640px){
  .sec .dlg .line,.sec .drill .rows .line{padding-right:12px!important}
  .sec .exs .line{padding-right:13px!important}
}
.controls .ctl>span.repw{display:inline-flex}
/* phone: the three 가리기 boxes on one line, without the notes in brackets (RYU 2026-11-24) */
@media (max-width:600px){.class-row .lnote{display:none}.controls .class-row{flex-wrap:nowrap;gap:0 10px;font-size:min(12.5px,3.3vw)}.class-row label{gap:3px}.class-row input{margin:0;width:15px;height:15px}}
@media (max-width:360px){.controls .class-row{gap:0 6px}}
/* 연속 재생 · 묶음 재생 like lao-app: one pair, outer ends round, inner ends nearly square; key badge filled (RYU 2026-11-23) */
.controls #ctlrep{gap:6px}
.controls #ctlrep .wrep.tbtn{border:1.5px solid var(--accent);color:var(--accent);background:var(--sheet);font-weight:600;display:inline-flex;align-items:center;gap:6px;padding:0 14px;height:34px}
.controls #ctlrep .wrep.tbtn:first-of-type{border-radius:999px 6px 6px 999px}
.controls #ctlrep .wrep.tbtn:last-of-type{border-radius:6px 999px 999px 6px}
.controls #ctlrep .wrep.tbtn .ico{color:var(--accent)}
.controls #ctlrep .kc{background:var(--accent-soft);border-color:var(--accent);color:var(--accent);opacity:1;margin-left:8px}
#ctlrep[data-on="chain"] .tbtn:first-of-type,#ctlrep[data-on="bundle"] .tbtn:last-of-type{background:var(--rev)!important;color:var(--ink)!important}

.opts .replab{margin-left:12px}
#ctlrep[hidden],#kbinfo[hidden],#band[hidden],#controls[hidden],#classRow[hidden]{display:none!important}
/* 묶음 전체 듣기 + 연속 듣기: own line, centred, both visible on phones (RYU 2026-11-23) */
.controls #ctlrep{grid-column:1 / -1;flex:1 0 100%;width:100%;justify-content:center;flex-wrap:nowrap;gap:8px}
.controls #ctlrep .tbtn{margin:0;min-width:0}
@media (max-width:360px){ .controls #ctlrep .tbtn{padding-left:9px;padding-right:9px;font-size:13px} }
.rowbtns{gap:8px;flex-wrap:wrap}
.seg .kc{margin-left:5px}

.info{line-height:1.7;font-size:15.5px}.info h2{font-size:19px;margin:18px 0 6px}.info h2:first-child{margin-top:0}.info p{margin:6px 0}.info ul{margin:4px 0;padding-left:20px}
.quizq.qen,.choice.qen,.qblank .qen{font-family:var(--display)}
.qblank .qen{font-size:clamp(19px,4.6vw,26px);line-height:1.45}.qblank .qlo{font-size:15px;color:var(--muted);margin-top:6px}
.qblank .blank{display:inline-block;min-width:3em;border-bottom:2px solid var(--accent);color:var(--accent);text-align:center}
.wcard .k{font-family:var(--display)}.wcard .ex>div:first-child{font-family:var(--display)}
.tscr{font-size:15px!important;color:var(--ink)}
.tqq{white-space:pre-line}
.tip .note-ko{text-align:left}
.tdesc{margin:0;font-size:14.5px;color:var(--ink)}
body:not(.show-lis) .tq.p34 .tqs,body:not(.show-lis) .tq.p34 .topt .ot{filter:none!important;user-select:auto}
.tq.p34 .tqs{font-weight:600}
.hit .k{font-family:var(--display)}
'''

if __name__ == "__main__":
    data, unused = build()
    rd = lambda n: open(os.path.join(H, n), encoding="utf8").read()
    js = f'const HE_VER = "v{VERSION}";\n' + rd("vol.js") + "\n" + rd("audiopack.js") + "\n" + rd("stats.js") + "\n" + rd("app.js") + "\n" + rd("intro.js") + "\n" + rd("ptr.js")   # v1.68: stats + intro (RYU 2026-11-27)
    nb = sum(1 for b in data["b"].values() if not b.get("info"))
    print("bundles", nb, "class", sum(1 for b in data["b"].values() if not b.get("self")), "unused source words", len(unused))
    # 1) single file preview (artifact)
    aud = {}   # the preview page (artifact) reads with the device voice: all mp3 inlined would pass the 16 MB limit
    for _b in data["b"].values(): voice_pass(_b)
    # key-word notes under every sentence (RYU 2026-11-23): written notes first, then words from the word lists
    from gloss import Glosser
    GL = Glosser(data["b"].values())
    def _merge(old, new, lim):
        out = [list(x) for x in (old or [])]; have = {x[0].lower() for x in out}
        for x in new:
            if len(out) >= lim: break
            if x[0].lower() not in have and not any(x[0].lower() in h or h in x[0].lower() for h in have): out.append(x); have.add(x[0].lower())
        return out
    for _b in data["b"].values():
        for w in _b.get("w", []):
            for p in w[4]:
                while len(p) < 5: p.append([])
                p[4] = _merge(p[4], GL.notes(p[0] + " / " + p[2], skip=[w[0]], limit=4), 4)
        for d in _b.get("d", []):
            while len(d) < 4: d.append([])
            d[3] = _merge(d[3], GL.notes(d[1], limit=4), 4)
        for dr in _b.get("dr", []):
            for x in dr[2]:
                while len(x) < 3: x.append([])
                x[2] = _merge(x[2], GL.notes(x[0], limit=4), 4)
    page = shell("", "<script>const DATA=" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\nconst AUD=" + json.dumps(aud) + ";\nconst APK=[];\n" + js + "</script>", nb)
    os.makedirs(os.path.join(H, "..", "preview"), exist_ok=True)
    open(os.path.join(H, "..", "preview", "hoteleng_app.html"), "w", encoding="utf8").write(page)
    print("preview", len(page))
    # 2) site for GitHub Pages
    site = os.path.join(H, "..", "site"); os.makedirs(site, exist_ok=True)
    aud2 = audio_map(data, False)
    open(os.path.join(site, "data.js"), "w", encoding="utf8").write("const DATA=" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\nconst AUD=" + json.dumps(aud2) + ";\n")
    open(os.path.join(site, "app.js"), "w", encoding="utf8").write(js)
    idx = ('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
           + shell(OG_TAGS, f'<script src="data.js?v={VERSION}"></script><script src="app.js?v={VERSION}"></script>', nb).replace("<title>", "<title>", 1) + "</body></html>")
    idx = idx.replace('<meta name="claude:viewport-fit-sides" content="cover">', '<link rel="manifest" href="manifest.webmanifest"><link rel="apple-touch-icon" href="icon-180.png"><link rel="icon" href="icon-192.png">'
                      '<meta name="theme-color" content="#17507a"><meta name="apple-mobile-web-app-capable" content="yes"><meta name="mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-title" content="HotelEng">')
    open(os.path.join(site, "index.html"), "w", encoding="utf8").write(idx)
    # PWA: service worker (app files + mp3 kept for offline use) and manifest, like lao-app (RYU 2026-11-23)
    os.makedirs(os.path.join(site, "img"), exist_ok=True); shutil.copy(os.path.join(H, "qr.svg"), os.path.join(site, "img", "qr.svg")); shutil.copy(os.path.join(H, "og.jpg"), os.path.join(site, "og.jpg"))   # intro QR (v1.68)
    os.makedirs(os.path.join(site, "img", "intro"), exist_ok=True)
    for _f in os.listdir(os.path.join(H, "introimg")): shutil.copy(os.path.join(H, "introimg", _f), os.path.join(site, "img", "intro", _f))   # RYU's intro photos
    open(os.path.join(site, "sw.js"), "w", encoding="utf8").write(open(os.path.join(H, "sw.js"), encoding="utf8").read().replace("__VER__", VERSION))
    json.dump({"name": "HotelEng · 호텔서비스 영어", "short_name": "HotelEng", "start_url": "./", "scope": "./", "display": "standalone", "background_color": "#eef2f6", "theme_color": "#17507a",
               "icons": [{"src": f"icon-{n}.png", "sizes": f"{n}x{n}", "type": "image/png", "purpose": "any"} for n in (180, 192, 512)]},
              open(os.path.join(site, "manifest.webmanifest"), "w", encoding="utf8"), ensure_ascii=False)
    # audio packs: clips.js reads the site just written, then data.js is written again with AUD = clip id + "." + home pack
    if not aud2:   # no mp3 source (audio/mp3.tar or HOTELENG_MP3): stop here, or audio_packs would delete every audio/p/*.bin (2026-11-28)
        sys.exit("STOP: mp3 원본이 없습니다. audio/mp3.tar 를 넣거나 HOTELENG_MP3=<mp3 폴더> 로 다시 실행하세요. site/ 는 음성 없이 만들어졌으니 배포하지 마세요.")
    packs, home = audio_packs(data, aud2)
    aud3 = {k: u.split("/")[-1][:-4] + "." + str(home[u.split("/")[-1][:-4]]) for k, u in aud2.items() if u.split("/")[-1][:-4] in home}
    open(os.path.join(site, "data.js"), "w", encoding="utf8").write("const DATA=" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\nconst AUD=" + json.dumps(aud3, ensure_ascii=False, separators=(",", ":")) + ";\nconst APK=" + json.dumps(packs, separators=(",", ":")) + ";\n")
    print("site audio clips", len(aud3), "of", len(aud2), "packs", len(packs), "MB", round(sum(os.path.getsize(os.path.join(H, "..", "audio", "p", c + ".bin")) for c, _ in packs) / 1e6, 1))
