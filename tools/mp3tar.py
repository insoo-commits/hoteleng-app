#!/usr/bin/env python3
"""Keep a folder of source mp3 clips as ONE .tar file in the project folder (RYU 2026-11-26: the project folder
has a 50,000-file limit, and ~40,000 of its files were loose mp3 clips kept only for rebuilding the apps).

The tar is plain (no compression: mp3 does not shrink). Builds unpack it to local disk, work there, and save it back.

  python3 mp3tar.py path <x.tar>            unpack to a local cache folder (reused if the tar did not change), print the folder
  python3 mp3tar.py save <folder> <x.tar>   write the folder's *.mp3 back into the tar if anything was added, changed or deleted
  python3 mp3tar.py pack <folder> <x.tar>   first-time pack: tar the folder's *.mp3 and check names + sizes + bytes
  python3 mp3tar.py unpack <x.tar> <folder> unpack into any folder (to look at the clips by hand)

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
    if not os.path.exists(tar):           # nothing packed yet: start empty
        return d
    if os.path.exists(st) and json.load(open(st)) == _stamp(tar):
        return d
    for f in os.listdir(d):
        if f.endswith(".mp3"): os.remove(os.path.join(d, f))
    with tarfile.open(tar) as t:
        t.extractall(d, filter="data") if hasattr(tarfile, "data_filter") else t.extractall(d)
    json.dump(_stamp(tar), open(st, "w"))
    return d


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
    else: print(__doc__)
