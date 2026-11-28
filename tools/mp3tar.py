#!/usr/bin/env python3
"""Keep a folder of source mp3 clips as ONE .tar file in the project folder (RYU 2026-11-26: the project folder
has a 50,000-file limit, and ~40,000 of its files were loose mp3 clips kept only for rebuilding the apps).

The tar is plain (no compression: mp3 does not shrink). Builds unpack it to local disk, work there, and save it back.

  python3 mp3tar.py path <x.tar>            unpack to a local cache folder (reused if the tar did not change), print the folder
  python3 mp3tar.py save <folder> <x.tar>   write the folder's *.mp3 back into the tar if anything was added, changed or deleted
  python3 mp3tar.py pack <folder> <x.tar>   first-time pack: tar the folder's *.mp3 and check names + sizes + bytes
  python3 mp3tar.py unpack <x.tar> <folder> unpack into any folder (to look at the clips by hand)
  python3 mp3tar.py frompacks <p dir> <folder>  take every mp3 back out of the audio packs (<p dir>/*.bin)

No tar yet? path() fills the cache from the audio packs next to it (<tar folder>/p/*.bin, 2026-11-28): each pack holds
its clips byte for byte, so the repository alone is enough to rebuild, and the first save() writes a full tar.

From Python: import mp3tar; d = mp3tar.path(tar); ...; mp3tar.save(d, tar)
"""
import hashlib, json, os, sys, tarfile

CACHE = os.environ.get("MP3TAR_CACHE", "/tmp/mp3cache")


def _listing(folder):
    return {f: os.path.getsize(os.path.join(folder, f)) for f in os.listdir(folder) if f.endswith(".mp3")}


def _tar_listing(tar):
    with tarfile.open(tar) as t:
        return {m.name: m.size for m in t.getmembers() if m.isfile()}


def _write(folder, tar):
    names = sorted(_listing(folder))
    tmp = tar + ".tmp"
    with tarfile.open(tmp, "w", format=tarfile.PAX_FORMAT) as t:
        for f in names:
            t.add(os.path.join(folder, f), arcname=f, recursive=False)
    # check: same names, same sizes, same bytes
    want = _listing(folder)
    with tarfile.open(tmp) as t:
        got = {}
        for m in t.getmembers():
            d = t.extractfile(m).read()
            if d != open(os.path.join(folder, m.name), "rb").read():
                raise SystemExit("mp3tar: bytes differ for " + m.name)
            got[m.name] = len(d)
    if got != want:
        raise SystemExit("mp3tar: tar listing does not match folder")
    os.replace(tmp, tar)
    return len(names)


def _stamp(tar):
    s = os.stat(tar)
    return [s.st_size, int(s.st_mtime)]


def path(tar):
    tar = os.path.abspath(tar)
    d = os.path.join(CACHE, hashlib.md5(tar.encode()).hexdigest()[:10])
    st = os.path.join(d, ".stamp.json")
    os.makedirs(d, exist_ok=True)
    if not os.path.exists(tar):           # no tar: take the clips out of the audio packs (or start empty)
        pdir = os.path.join(os.path.dirname(tar), "p")
        if os.path.isdir(pdir) and not any(f.endswith(".mp3") for f in os.listdir(d)):
            n = from_packs(pdir, d)
            print("mp3tar: no", os.path.basename(tar) + ",", n, "clips taken out of", pdir, file=sys.stderr)
        return d
    if os.path.exists(st) and json.load(open(st)) == _stamp(tar):
        return d
    for f in os.listdir(d):
        if f.endswith(".mp3"): os.remove(os.path.join(d, f))
    with tarfile.open(tar) as t:
        t.extractall(d, filter="data") if hasattr(tarfile, "data_filter") else t.extractall(d)
    json.dump(_stamp(tar), open(st, "w"))
    return d


def from_packs(pdir, folder):
    """audio pack = 4-byte little-endian header length N, N bytes of JSON [[clip id, offset, length], ...], then the
    mp3 bytes (offsets count from the end of the header). Writes <folder>/<clip id>.mp3; a clip found in several
    packs must have the same bytes in each."""
    import glob, struct
    os.makedirs(folder, exist_ok=True)
    got = {}
    for f in sorted(glob.glob(os.path.join(pdir, "*.bin"))):
        b = open(f, "rb").read()
        n = struct.unpack("<I", b[:4])[0]
        base = 4 + n
        for i, off, ln in json.loads(b[4:base]):
            d = b[base + off: base + off + ln]
            if len(d) != ln: raise SystemExit("mp3tar: pack cut short: " + f)
            if i in got:
                if got[i] != hashlib.md5(d).digest(): raise SystemExit("mp3tar: clip differs between packs: " + i)
                continue
            got[i] = hashlib.md5(d).digest()
            tmp = os.path.join(folder, i + ".mp3.part")
            open(tmp, "wb").write(d); os.replace(tmp, os.path.join(folder, i + ".mp3"))
    return len(got)


def save(folder, tar):
    tar = os.path.abspath(tar)
    if os.path.exists(tar) and _tar_listing(tar) == _listing(folder):
        # same names and sizes; a clip re-made with the same size is still caught by comparing bytes
        with tarfile.open(tar) as t:
            same = all(t.extractfile(m).read() == open(os.path.join(folder, m.name), "rb").read() for m in t.getmembers())
        if same:
            print("mp3tar: no change", tar); return
    n = _write(folder, tar)
    st = os.path.join(folder, ".stamp.json")
    if os.path.dirname(os.path.abspath(folder)) == os.path.abspath(CACHE):
        json.dump(_stamp(tar), open(st, "w"))
    print("mp3tar: saved", n, "clips to", tar)


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["path"]: print(path(a[1]))
    elif a[:1] == ["save"]: save(a[1], a[2])
    elif a[:1] == ["pack"]: print("packed", _write(a[1], a[2]), "clips into", a[2])
    elif a[:1] == ["unpack"]:
        os.makedirs(a[2], exist_ok=True)
        with tarfile.open(a[1]) as t: t.extractall(a[2])
        print("unpacked to", a[2])
    elif a[:1] == ["frompacks"]: print("took", from_packs(a[1], a[2]), "clips out of", a[1], "into", a[2])
    else: print(__doc__)
