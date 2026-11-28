# mp3 clips for chosen bundles (edge-tts, 16 kbps mono). python3 make_audio.py 3-02-01 [more codes]
# Keys match app.js clipKey(): "voice|text", voice m / f / m2 / f2 (a bundle's vo map sets a speaker's voice).
import asyncio, hashlib, json, os, re, ssl, subprocess, sys
import edge_tts, edge_tts.communicate as C
if os.path.exists('/root/.ccr/ca-bundle.crt'): C._SSL_CTX = ssl.create_default_context(cafile='/root/.ccr/ca-bundle.crt')
H = os.path.dirname(os.path.abspath(__file__)); ADIR = os.path.join(H, "..", "audio"); os.makedirs(ADIR, exist_ok=True)
# RYU 2026-11-26: the mp3 files are kept in ../audio/mp3.tar (not 14,000 loose files). New clips are made in the unpacked
# local copy and saved back into the tar at the end; index.json stays in ../audio.
sys.path.insert(0, "/mnt/project-files/tools"); sys.path.insert(0, os.path.join(H, "..", "tools")); import mp3tar
TAR = os.path.join(ADIR, "mp3.tar"); OUT = mp3tar.path(TAR)
# RYU 2026-11-23: no man's voice on the phone. en-US-GuyNeural now comes back with a woman's pitch (~200 Hz), so the men are
# Christopher (~118 Hz) and Eric (~115 Hz). Men's files carry the voice name in their file name, so phones that saved the
# old (wrong) files download the new ones instead of reusing them.
# RYU 2026-11-24: Christopher/Eric sounded low and slow → Andrew (RYU chose, after trying Steffan) and Brian (second man, faster).
VOICE = {"m": "en-US-AndrewNeural", "f": "en-US-JennyNeural", "m2": "en-US-BrianNeural", "f2": "en-US-AriaNeural"}
def fname(v, k): return hashlib.md5((k + "@" + VOICE[v] if v[0] == "m" else k).encode()).hexdigest()[:12] + ".mp3"
def keys(*codes):
    """every [voice, text] app.js can play in these bundles (clips.js runs app.js clipsOf in a headless page)"""
    out = subprocess.run(["node", os.path.join(H, "clips.js"), *codes], capture_output=True, text=True, check=True, cwd="/tmp").stdout
    return {(v, t) for v, t in json.loads(out)}
idx_p = os.path.join(ADIR, "index.json")
IDX = json.load(open(idx_p)) if os.path.exists(idx_p) else {}
codes = sys.argv[1:]
if codes == ["all"]:   # every class bundle (not the 도움말 pages); the index is rebuilt so it only lists clips the app can play
    js = open(os.path.join(H, "..", "site", "data.js"), encoding="utf8").read()
    D = json.loads(js[js.index("=") + 1:js.index(";\nconst AUD")])
    codes = [c for c, b in D["b"].items() if not b.get("info")]; IDX = {}
todo = []
if True:
    for v, t in sorted(keys(*codes)):
        k = v + "|" + t.strip(); fn = fname(v, k)
        IDX[k] = fn
        if not os.path.exists(os.path.join(OUT, fn)): todo.append((v, t, fn))
print("clips", len(IDX), "to make", len(todo), flush=True)
P = os.environ.get("HTTPS_PROXY")
async def one(v, t, fn):
    part = os.path.join(OUT, fn + ".part")
    for a in range(6):
        try:
            await edge_tts.Communicate(t, VOICE[v], proxy=P).save(part)
            if os.path.getsize(part) < 500: raise RuntimeError("short")
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "mp3", "-i", part, "-ar", "16000", "-ac", "1", "-c:a", "libmp3lame", "-b:a", "16k", "-f", "mp3", os.path.join(OUT, fn)], check=True)
            os.remove(part); return True
        except Exception as e:
            print("retry", fn, e, flush=True); await asyncio.sleep(2 ** a)
    return False
async def main():
    q = todo[::-1]; fails = []
    async def w():
        while q:
            x = q.pop()
            if not await one(*x): fails.append(x[2])
    await asyncio.gather(*[w() for _ in range(int(os.environ.get("NW", "8")))])
    print("failed", fails)
asyncio.run(main())
json.dump(IDX, open(idx_p, "w"), ensure_ascii=False, indent=0)
mp3tar.save(OUT, TAR)
