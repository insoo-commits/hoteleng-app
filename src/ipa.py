# ARPAbet (CMU dict) -> American IPA, word by word. ipa("early check-in") -> "/ˈɝli ˈtʃɛk ɪn/"
import re, cmudict
D = cmudict.dict()
V = {"AA":"ɑ","AE":"æ","AH":"ʌ","AO":"ɔ","AW":"aʊ","AY":"aɪ","EH":"ɛ","ER":"ɝ","EY":"eɪ","IH":"ɪ","IY":"i","OW":"oʊ","OY":"ɔɪ","UH":"ʊ","UW":"u"}
C = {"B":"b","CH":"tʃ","D":"d","DH":"ð","F":"f","G":"ɡ","HH":"h","JH":"dʒ","K":"k","L":"l","M":"m","N":"n","NG":"ŋ","P":"p","R":"r","S":"s","SH":"ʃ","T":"t","TH":"θ","V":"v","W":"w","Y":"j","Z":"z","ZH":"ʒ"}
ONSET = {"pr","br","tr","dr","kr","ɡr","fr","θr","ʃr","pl","bl","kl","ɡl","fl","sl","sp","st","sk","sm","sn","sw","tw","kw","spr","str","skr","spl","skw","pj","bj","kj","mj","fj","hj","vj","ɡw","dw"}

OV = {"adr":"ˌeɪ di ˈɑr","aed":"ˌeɪ i ˈdi","cpr":"ˌsi pi ˈɑr","q&a":"ˌkju ən ˈeɪ","revpar":"ˈrɛvpɑr","wi":"ˈwaɪ","fi":"faɪ","childproof":"ˈtʃaɪldˌpruf",
"cloche":"kloʊʃ","contraindication":"ˌkɑntrəˌɪndɪˈkeɪʃən","corkage":"ˈkɔrkɪdʒ","corked":"kɔrkt","decanter":"dɪˈkæntɚ","deodorizer":"diˈoʊdəˌraɪzɚ",
"familiarization":"fəˌmɪljərəˈzeɪʃən","hanbok":"ˈhɑnbɑk","hanok":"ˈhɑnɑk","hypoallergenic":"ˌhaɪpoʊˌælɚˈdʒɛnɪk","makgeolli":"ˈmɑkɡəli",
"minibar":"ˈmɪniˌbɑr","notarize":"ˈnoʊtəˌraɪz","overset":"ˈoʊvɚˌsɛt","porte":"ˌpɔrt","cochère":"koʊˈʃɛr","soju":"ˈsoʊdʒu","sommelier":"ˌsʌməlˈjeɪ",
"soundproof":"ˈsaʊndˌpruf","sun":"sʌn","lounger":"ˈlaʊndʒɚ","table":"ˌtɑbəl","d'hôte":"ˈdoʊt","tannin":"ˈtænɪn","upsell":"ˈʌpˌsɛl","waitlist":"ˈweɪtˌlɪst",
"wayfinding":"ˈweɪˌfaɪndɪŋ","id":"ˌaɪ ˈdi","upgrade":"ˈʌpˌɡreɪd","ota":"ˌoʊ ti ˈeɪ","mc":"ˌɛm ˈsi","av":"ˌeɪ ˈvi","cctv":"ˌsi si ti ˈvi","mice":"maɪs",
"vip":"ˌvi aɪ ˈpi","pin":"pɪn","vat":"ˌvi eɪ ˈti","tv":"ˌti ˈvi","unesco":"juˈnɛskoʊ","à":"ˌɑ","la":"lə","carte":"ˈkɑrt","amuse":"əˌmjuz","bouche":"ˈbuʃ",
"rosé":"roʊˈzeɪ","omelet":"ˈɑmlət","benedict":"ˈbɛnəˌdɪkt","canapé":"ˈkænəpeɪ","hanbok":"ˈhɑnbɑk","sous":"su","décor":"deɪˈkɔr","gratuity":"ɡrəˈtuəti"}
def one(ph):
    syl = []  # list of (onset list, vowel, stress, coda)
    cons = []
    for p in ph:
        b = re.sub(r"\d", "", p)
        if b in V:
            s = int(p[-1]); v = V[b]
            if b == "AH" and s == 0: v = "ə"
            if b == "ER" and s == 0: v = "ɚ"
            if syl:
                # split cons between previous coda and this onset (max onset)
                k = len(cons)
                while k > 0 and ("".join(cons[k-1:]) in ONSET or len(cons[k-1:]) == 1):
                    if len(cons[k-1:]) > 1 and "".join(cons[k-1:]) not in ONSET: break
                    k -= 1
                syl[-1][3].extend(cons[:k]); on = cons[k:]
            else: on = cons
            syl.append([on, v, s, []]); cons = []
        else: cons.append(C[b])
    if syl: syl[-1][3].extend(cons)
    out = ""; nprim = sum(1 for x in syl if x[2] == 1)
    for on, v, s, co in syl:
        mark = "ˈ" if s == 1 and len(syl) > 1 else ("ˌ" if s == 2 and len(syl) > 1 else "")
        out += mark + "".join(on) + v + "".join(co)
    return out
def ipa(phrase):
    parts = []
    for w in re.split(r"[\s\-/]+", phrase.strip()):
        lw = w.lower().strip(".,")
        if lw in OV: parts.append(OV[lw]); continue
        k = re.sub(r"[^a-z']", "", lw.replace("é", "e").replace("à", "a").replace("ô","o"))
        if not k: continue
        if k not in D:
            k2 = k.rstrip("'s") if k.endswith("'s") else k
            if k2 not in D: return None
            k = k2
        parts.append(one(D[k][0]))
    return "/" + " ".join(parts) + "/" if parts else None
if __name__ == "__main__":
    for t in ["reservation","early check-in","key card","registration card","deposit","valid ID","upgrade","floor","RevPAR","amuse-bouche","porte-cochère","kids' menu"]: print(t, ipa(t))
