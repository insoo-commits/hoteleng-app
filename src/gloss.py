# Key-word notes under each sentence: "※ word(뜻), word(뜻)" (RYU 2026-11-23, like lao-app).
# Source: the app's own word list (its Korean meanings were written for hotel use) + content/glossary.py for other useful words.
# Left out: very easy words (BASIC), the sentence's own headword, and pattern entries with "~".
import re
try:
    from glossary import EXTRA
except Exception:
    EXTRA = {}
try:
    from senses import SENSE
except Exception:
    SENSE = {}

def sense(hw, text, ko):
    """the meaning that fits this sentence (first), then another meaning; None = this note doesn't fit the sentence"""
    r = SENSE.get(hw)
    if r is None: return ko
    if isinstance(r, str): return r
    for rx, v in r:
        if rx == "" or re.search(rx, text, re.I): return v
    return ko

BASIC = set("""a an the and or but so if then than as at by for from in into of off on onto out over to up with  about after again all  am are be been being
before can could did do does done    get gets got go goes going gone good great had has have he her here hers him his how i i'd i'll i'm i've is it it's its
just let let's like little lot lots make many may me more most much must my no not now of okay on one only our ours please put really right said say says see she should so
some sure take tell thank thanks that that's the their them there there's these they this those time too two three four five six seven eight nine ten us very want was
we we'll we're we've well were what what's when where which who why will would yes you you'd you'll you're you've your yours hello hi bye yes no ok sorry
day days week night nights morning evening today tomorrow tonight yesterday year month new old big small hot cold come came give gave know    want work look 
here there back other  any anything something nothing everything everyone someone way thing things man woman people person friend family name number room rooms
open close help call eat drink buy pay play read write speak talk  leave  start stop wait walk run sit stand sleep live like love  think  ask 
first last next   easy  long short high low   fast slow free  nice fine happy sad sure  right  left""".split())

# everyday words most students know: shown when there is room, but left out first when a sentence has more notes than fit
EASY = set("""hear glad need use every minute hour stay try each ready door show made list early late later under best per kid add same side another
full still house area meet job end sweet also train bank half home office own station welcome children cash lost feel market face birthday hand city
while pillow less around few problem far cheap else exit wet gift shoes wash dry toilet chair snack seat breakfast lunch dinner fire wife husband plan bad
part become season top view tap site age once salt knife rain straight expensive sale found sink holiday weekend both yet beautiful money sell leg life
form daughter son student idea sister text path stairs garden coin heavy umbrella repeat never subway museum festival doctor cooking blanket toothbrush
clothes wall window quick fruit sugar kitchen cook together travel movie thousand sent building smile voice type soon slowly young space pull arm swim
swimming relax quiet follow of course book press find wrong answer hard different university hospital police medicine angry busy guest staff floor
bring send until price clean taxi enjoy menu special main group tour fresh important outside local company near glass online often dish large paper
trip date closed towel child""".split())

# words with several meanings: a wrong meaning is worse than none, so they get no note
AMBIG = set("""change stop back signature proposal present fine light rest ring party right left state sign miss match cover case run order check note
spring fall club mean kind bear last even point line rate card table tip charge store leave address hold iron court bar draft shot neat rocks
body cellar tissue scrub safe meeting stock trail board deck setting serving label sheet suit tie pass deal pitch""".split())

def _forms(w, adj=False):
    w = w.lower()
    out = {w, w + "s", w + "es", w + "ed", w + "d", w + "ing"}
    if w.endswith("e"): out |= {w[:-1] + "ing"}
    if w.endswith("y"): out |= {w[:-1] + "ies", w[:-1] + "ied"}
    if re.search(r"[^aeiou][aeiou][bdgmnpt]$", w): out |= {w + w[-1] + "ed", w + w[-1] + "ing"}
    if adj and " " not in w:   # quieter, cheapest, quietly (adjectives only, so corn never matches corner)
        out |= {w + "er", w + "est", w + "ly"}
        if w.endswith("e"): out |= {w + "r", w + "st"}
        if w.endswith("y"): out |= {w[:-1] + "ier", w[:-1] + "iest", w[:-1] + "ily"}
        if re.search(r"[^aeiou][aeiou][bdgmnpt]$", w): out |= {w + w[-1] + "er", w + w[-1] + "est"}
    return out

def _short_ko(ko):
    ko = re.sub(r"\s*\(.*?\)", "", ko).strip()
    return re.split(r"\s*[,/;·]\s*", ko)[0].strip() or ko

class Glosser:
    def __init__(self, bundles):
        ent = {}
        for b in bundles:
            for w in b.get("w", []):
                hw, ko, lv = w[0], w[2], w[3] if len(w) > 3 else ""
                if "~" in hw or not ko or hw.lower() in ent or hw.lower() in AMBIG: continue
                single = " " not in hw.strip()
                if single and (hw.lower() in BASIC or (lv in ("하", "초급") and len(hw) <= 5)): continue
                ent[hw.lower()] = _short_ko(ko)
        for k, v in EXTRA.items():
            if k.lower() not in AMBIG: ent[k.lower()] = v   # hand-written meanings win
        # words with several meanings are noted only where senses.py says which meaning the sentence uses
        for k, v in SENSE.items():
            if k not in ent and (isinstance(v, str) or any(rx == "" and m for rx, m in v) or True):
                ent[k] = v if isinstance(v, str) else next((m for rx, m in v if m), "")
        # longest first, so "front desk" wins over "desk"
        self.items = sorted(ent.items(), key=lambda kv: -len(kv[0]))
        self.rx = []
        for hw, ko in self.items:
            parts = hw.split()
            last = "(?:" + "|".join(sorted((re.escape(f) for f in _forms(parts[-1], re.search(r"(한|운|은|인|쁜|픈|른|든|싼|큰|긴|센|ㄴ)$", ko) is not None)), key=len, reverse=True)) + ")"
            pat = r"(?<![\w-])" + r"\s+".join([re.escape(p) for p in parts[:-1]] + [last]) + r"(?![\w-])"
            self.rx.append((hw, ko, re.compile(pat, re.I)))
    def notes(self, text, skip=(), limit=3):
        t = text; out = []; skip = {s.lower() for s in skip}
        # the sentence's own headword is blanked first, so its parts are not noted either
        for hw, ko, rx in self.rx:
            if hw in skip: t = rx.sub(lambda m: " " * len(m.group(0)), t)
        for sk in skip:
            if "~" not in sk: t = re.sub(r"(?i)(?<![\w-])" + re.escape(sk) + r"\w*", lambda m: " " * len(m.group(0)), t)
        for hw, ko, rx in self.rx:
            m = rx.search(t)
            if not m or hw in skip: continue
            k2 = sense(hw, text, ko)
            if k2: out.append([m.group(0) if m.group(0).lower() == hw else hw, k2, m.start(), hw])
            t = t[:m.start()] + " " * (m.end() - m.start()) + t[m.end():]
        # more words than room: keep the harder ones (phrases and less common words first, easy everyday words last)
        # (RYU 2026-11-23: "relieved" was left out while "hear" was shown)
        if len(out) > limit:
            out.sort(key=lambda x: (x[3] in EASY, " " not in x[3], -len(x[3])))
            out = out[:limit]
        out.sort(key=lambda x: x[2])
        return [[x[0], x[1]] for x in out]
