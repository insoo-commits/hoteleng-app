# Builds the 예문보기 sample page for the hotel English app (one bundle: 프런트 > 체크인 > 체크인 기본 응대).
# Design = kor-app v2.52 (src/korapp_v252.css, copied from insoo-commits/kor-app index.html), content = Practical Hotel English.
#   python3 make_sample.py  ->  ../preview/hotel_english_sample.html
import html, re, os
H = os.path.dirname(os.path.abspath(__file__))
CSS = open(os.path.join(H, "korapp_v252.css"), encoding="utf8").read()
e = html.escape

SPK = '<button class="spk" type="button" aria-label="듣기"><span class="ico" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 5 6 9H3v6h3l5 4z" fill="currentColor"/><path d="M15.5 8.5a5 5 0 0 1 0 7"/><path d="M18.5 5.5a9 9 0 0 1 0 13"/></svg></span></button>'
REP = '<span class="ico" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="m17 2 4 4-4 4"/><path d="M3 11v-1a4 4 0 0 1 4-4h14"/><path d="m7 22-4-4 4-4"/><path d="M21 13v1a4 4 0 0 1-4 4H3"/></svg></span>'

# word, IPA, Korean, level, [(guest en, guest ko, staff en, staff ko, notes)]  -- sentences taken as-is from Practical Hotel English (Check-in)
WORDS = [
 ("reservation", "/ˌrezərˈveɪʃn/", "예약", "초급", [
  ("I have a reservation under the name Kim.", "김이라는 이름으로 예약했어요.", "Thank you, Mr. Kim. I've found your reservation for two nights.", "감사합니다, 김 선생님. 2박 예약 확인했습니다.", [("under the name ~", "~ 이름으로"), ("find", "찾다, 확인하다")]),
  ("I don't think I made a reservation. Do you have any rooms?", "예약을 안 한 것 같아요. 빈방 있나요?", "Let me check availability. Without a reservation, we have a deluxe room tonight.", "확인해 보겠습니다. 예약 없이 오늘 밤은 디럭스룸이 가능합니다.", [("Let me check ~", "~ 확인해 보겠습니다"), ("availability", "빈방 여부")])]),
 ("passport", "/ˈpæspɔːrt/", "여권", "초급", [
  ("Do you need my passport?", "여권이 필요한가요?", "Yes, may I see your passport, please? It's required for all international guests.", "네, 여권을 보여주시겠어요? 외국인 고객님은 모두 필요합니다.", [("May I see ~?", "~ 보여 주시겠어요?"), ("required", "필수인")]),
  ("Can I have my passport back now?", "이제 여권 돌려받을 수 있나요?", "Certainly. Here is your passport. Thank you for waiting.", "물론입니다. 여권 여기 있습니다. 기다려 주셔서 감사합니다.", [("Here is ~", "~ 여기 있습니다")])]),
 ("registration card", "/ˌredʒɪˈstreɪʃn kɑːrd/", "투숙 등록 카드", "중급", [
  ("What is this form?", "이 서류는 뭔가요?", "This is a registration card. Please fill in your address and sign at the bottom.", "투숙 등록 카드입니다. 주소를 적고 아래에 서명해 주세요.", [("fill in", "기입하다"), ("sign", "서명하다")]),
  ("Do I have to fill out the registration card again?", "등록 카드를 또 써야 하나요?", "I'm afraid so. We need a new registration card for each stay.", "죄송하지만 그렇습니다. 숙박할 때마다 새 등록 카드가 필요합니다.", [("I'm afraid so.", "죄송하지만 그렇습니다.")])]),
 ("deposit", "/dɪˈpɑːzɪt/", "보증금", "중급", [
  ("Why do you need a deposit?", "보증금은 왜 필요한가요?", "The deposit covers any extra charges, such as the minibar. It will be refunded at check-out.", "보증금은 미니바 같은 추가 요금을 위한 것이며, 체크아웃 때 환불됩니다.", [("cover", "충당하다"), ("be refunded", "환불되다")]),
  ("How much is the deposit?", "보증금은 얼마인가요?", "The deposit is 100,000 won per night, held on your credit card.", "보증금은 1박에 10만 원이며, 신용카드로 승인만 해둡니다.", [("per night", "1박당"), ("hold", "(카드 금액을) 잡아 두다")])]),
 ("valid ID", "/ˈvælɪd ˌaɪ ˈdiː/", "유효한 신분증", "중급", [
  ("Can I use my driver's license?", "운전면허증으로 해도 되나요?", "Yes, any valid ID with your photo is fine.", "네, 사진이 있는 유효한 신분증이면 됩니다.", [("driver's license", "운전면허증")]),
  ("My ID card expired last month.", "제 신분증이 지난달에 만료됐어요.", "I'm sorry, but we need a valid ID. Do you have your passport with you?", "죄송하지만 유효한 신분증이 필요합니다. 여권 가지고 계신가요?", [("expire", "만료되다")])]),
 ("floor", "/flɔːr/", "층", "초급", [
  ("Which floor is my room on?", "제 방은 몇 층인가요?", "Your room is on the 9th floor, and the elevators are on your right.", "객실은 9층이며, 엘리베이터는 오른쪽에 있습니다.", [("on your right", "오른쪽에")]),
  ("Could I have a room on a higher floor?", "더 높은 층으로 받을 수 있을까요?", "I'll try my best. I can offer you a room on the 15th floor.", "최선을 다해 보겠습니다. 15층 객실로 드릴 수 있습니다.", [("I'll try my best.", "최선을 다해 보겠습니다."), ("offer", "제공하다")])]),
 ("key card", "/ˈkiː kɑːrd/", "카드키", "초급", [
  ("My key card isn't working.", "카드키가 작동하지 않아요.", "I'm sorry about that. Let me reactivate your key card for you.", "불편을 드려 죄송합니다. 카드키를 다시 활성화해 드리겠습니다.", [("reactivate", "다시 활성화하다")]),
  ("Can I get a second key card?", "카드키 하나 더 받을 수 있을까요?", "Of course. Here is a second key card for room 805.", "물론입니다. 805호 카드키 하나 더 드리겠습니다.", [])]),
 ("breakfast", "/ˈbrekfəst/", "조식", "초급", [
  ("Is breakfast included?", "조식 포함인가요?", "Yes, breakfast is included for two people.", "네, 2인 조식이 포함되어 있습니다.", [("included", "포함된")]),
  ("What time is breakfast served?", "조식은 몇 시에 제공되나요?", "Breakfast is served from 6:30 to 10 a.m. at the restaurant on the 2nd floor.", "조식은 2층 레스토랑에서 오전 6시 30분부터 10시까지 제공됩니다.", [("be served", "제공되다")])]),
 ("early check-in", "/ˈɜːrli ˈtʃek ɪn/", "이른 체크인", "중급", [
  ("Is early check-in possible?", "일찍 체크인할 수 있나요?", "Early check-in is possible from 11 a.m. if a room is ready, for an extra fee.", "방이 준비되면 오전 11시부터 추가 요금으로 이른 체크인이 가능합니다.", [("extra fee", "추가 요금")]),
  ("Is there a charge for early check-in?", "이른 체크인에 요금이 있나요?", "Early check-in before noon is 30,000 won.", "정오 이전의 이른 체크인은 3만 원입니다.", [("charge", "요금"), ("noon", "정오")])]),
 ("upgrade", "/ˈʌpɡreɪd/", "객실 업그레이드", "실무", [
  ("Is an upgrade available?", "업그레이드 가능할까요?", "Good news. We can upgrade you to a suite for 50,000 won more.", "좋은 소식입니다. 5만 원 추가로 스위트룸 업그레이드가 가능합니다.", [("upgrade A to B", "A를 B로 업그레이드하다")]),
  ("It's our anniversary today.", "오늘이 저희 결혼기념일이에요.", "Congratulations! We've given you a free upgrade to a room with a view.", "축하드립니다! 전망 좋은 객실로 무료 업그레이드해 드렸습니다.", [("anniversary", "기념일"), ("a room with a view", "전망 좋은 객실")])]),
]

# whole scene, built from the lines above (new)
DIALOG = [
 ("S", "Good afternoon. Welcome to our hotel. How may I help you?", "안녕하세요. 저희 호텔에 오신 것을 환영합니다. 무엇을 도와드릴까요?", [("How may I help you?", "무엇을 도와드릴까요?")]),
 ("G", "Hi. I have a reservation under the name Kim.", "안녕하세요. 김이라는 이름으로 예약했어요.", []),
 ("S", "Thank you, Mr. Kim. May I see your passport, please?", "감사합니다, 김 선생님. 여권을 보여 주시겠어요?", []),
 ("G", "Sure. Here you are.", "네, 여기 있어요.", [("Here you are.", "여기 있어요.")]),
 ("S", "Please fill in this registration card and sign at the bottom.", "이 투숙 등록 카드를 작성하시고 아래에 서명해 주세요.", []),
 ("S", "We also need a deposit of 100,000 won per night. It will be refunded at check-out.", "1박에 10만 원의 보증금도 필요합니다. 체크아웃 때 환불됩니다.", []),
 ("G", "Okay. Is breakfast included?", "네. 조식 포함인가요?", []),
 ("S", "Yes. Breakfast is served from 6:30 to 10 a.m. on the 2nd floor.", "네. 조식은 2층에서 오전 6시 30분부터 10시까지 제공됩니다.", []),
 ("S", "Here is your key card. Your room is 1205, on the 12th floor. Enjoy your stay.", "카드키 여기 있습니다. 객실은 12층 1205호입니다. 편안한 시간 보내세요.", [("Enjoy your stay.", "편안한 시간 보내세요.")]),
]

# 바꿔 말하기 (substitution drill, new): pattern, Korean, [(sentence, Korean)]
DRILLS = [
 ("May I see your ~, please?", "~ 보여 주시겠어요? (정중한 요청)", [("May I see your passport, please?", "여권을 보여 주시겠어요?"), ("May I see your credit card, please?", "신용카드를 보여 주시겠어요?"), ("May I see your confirmation email, please?", "예약 확인 메일을 보여 주시겠어요?")]),
 ("~ is included.", "~ 포함입니다.", [("Breakfast is included.", "조식 포함입니다."), ("Wi-Fi is included.", "와이파이가 포함됩니다."), ("Tax and service charge are included.", "세금과 봉사료가 포함됩니다.")]),
 ("Your room is on the ~ floor.", "객실은 ~층입니다.", [("Your room is on the 12th floor.", "객실은 12층입니다."), ("Your room is on the 3rd floor.", "객실은 3층입니다."), ("Your room is on the top floor.", "객실은 맨 위층입니다.")]),
]

QA = [("\"보증금\"을 영어로?", "deposit"), ("\"May I see your passport, please?\"의 뜻은?", "여권을 보여 주시겠어요?"), ("\"투숙 등록 카드\"를 영어로?", "registration card"), ("\"Breakfast is included.\"의 뜻은?", "조식 포함입니다.")]

# TOEIC tie-in (new): part, question (en), choices, answer index, Korean explanation
TOEIC = [
 ("Part 2 · 질의응답", "Where can I pick up my key card?", ["(A) At the front desk.", "(B) It's a double room.", "(C) Yes, I picked it."], 0,
  "Where 질문에는 장소로 답합니다. (C)는 pick을 반복한 함정, Yes/No로 답할 수 없는 의문사 질문입니다."),
 ("Part 2 · 질의응답", "Is breakfast included in the room rate?", ["(A) On the second floor.", "(B) Yes, it's served until 10 a.m.", "(C) A double room, please."], 1,
  "포함 여부를 묻는 Yes/No 질문입니다. (A)는 장소, (C)는 객실 종류로 질문과 맞지 않습니다."),
 ("Part 5 · 단문 빈칸", "The deposit will be ------- to your card at check-out.", ["(A) refund", "(B) refunded", "(C) refunding", "(D) refunds"], 1,
  "will be 뒤에는 과거분사가 와서 수동태(환불되다)가 됩니다."),
 ("Part 5 · 단문 빈칸", "All guests must present a ------- photo ID when checking in.", ["(A) valid", "(B) validity", "(C) validate", "(D) validly"], 0,
  "관사 a와 명사 photo ID 사이에는 형용사가 옵니다. valid ID(유효한 신분증)는 호텔·여행 지문 빈출 표현입니다."),
]

def hw(sent, word):
    m = re.search(re.escape(word), sent, re.I)
    if not m: return e(sent)
    return e(sent[:m.start()]) + '<span class="hw">' + e(m.group(0)) + '</span>' + e(sent[m.end():])

def gl(notes):
    if not notes: return ""
    return '<div class="gl">※ ' + " · ".join(f'<span class="en">{e(a)}</span> (<span class="gm">{e(b)}</span>)' for a, b in notes) + '</div>'

WHO = {"G": "손님", "S": "직원"}

def words_html():
    out = []
    for w, ipa, ko, lv, exs in WORDS:
        rows = []
        for i, (ge, gk, se, sk, notes) in enumerate(exs, 1):
            rows.append(f'<div class="line ex pairx" data-say="{e(ge)}" data-say2="{e(se)}"><div class="exn">{i}</div>{SPK}<div>'
                        f'<div class="turn g"><span class="who">손님</span><div class="k">{hw(ge, w)}</div><div class="m">{e(gk)}</div></div>'
                        f'<div class="turn s"><span class="who">직원</span><div class="k">{hw(se, w)}</div><div class="m">{e(sk)}</div></div>'
                        f'{gl(notes)}</div></div>')
        out.append(f'<div class="word"><div class="line head" data-say="{e(w)}">{SPK}<div><div class="k">{e(w)}</div><div class="p">{e(ipa)}</div><div class="m">{e(ko)}</div><span class="lvl">{lv}</span></div>'
                   f'<button class="wrep" type="button">{REP}단어 반복</button></div><div class="exs">{"".join(rows)}</div></div>')
    return "".join(out)

def dialog_html():
    rows = []
    for i, (who, en, ko, notes) in enumerate(DIALOG, 1):
        rows.append(f'<div class="line {"st" if who=="S" else "gu"}" data-say="{e(en)}" data-who="{who}"><div class="exn">{i}</div>{SPK}<div>'
                    f'<div class="k"><span class="who">{WHO[who]}</span>{e(en)}</div><div class="m">{e(ko)}</div>{gl(notes)}</div></div>')
    return "".join(rows)

def drills_html():
    out = []
    for pat, ko, ss in DRILLS:
        rows = "".join(f'<div class="line" data-say="{e(s)}">{SPK}<div><div class="k">{e(s)}</div><div class="m">{e(k)}</div></div></div>' for s, k in ss)
        out.append(f'<div class="drill"><div class="dpat"><b>{e(pat)}</b><span>{e(ko)}</span></div><div class="rows">{rows}</div></div>')
    return "".join(out)

def qa_html():
    return "".join(f'<div class="qa"><div class="qq"><div class="exn">{i}</div><div>{e(q)}</div></div><div class="qr"><div class="a" hidden>{e(a)}</div><button class="btn" type="button">답 보기</button></div></div>' for i, (q, a) in enumerate(QA, 1))

def toeic_html():
    out = []
    for i, (part, q, ch, ans, why) in enumerate(TOEIC, 1):
        lis = part.startswith("Part 2")
        say = f' data-say="{e(q + " " + " ".join(c[1] + ". " + c[4:] for c in ch))}"' if lis else ""
        spk = SPK if lis else ""
        opts = "".join(f'<button type="button" class="topt" data-ok="{1 if j == ans else 0}"><span class="ol">{e(c[:3])}</span> <span class="ot">{e(c[4:])}</span></button>' for j, c in enumerate(ch))
        hint = '<p class="tnote">듣기 문제는 시험처럼 영어가 가려져 있어요. 🔊로 질문과 (A)(B)(C)를 듣고 풀어 보세요.</p>' if lis else ""
        out.append(f'<div class="tq{" lis" if lis else ""}"{say}><div class="tqh"><span class="exn">{i}</span><span class="tpart">{part}</span>{spk}</div>'
                   f'<p class="tqq">{e(q)}</p>{hint}<div class="topts">{opts}</div><p class="twhy" hidden>{e(why)}</p></div>')
    return "".join(out)

GROUPS = ["기초회화", "호텔기본", "프런트", "객실·시설", "식음료", "고객응대·실무", "TOEIC", "영어면접", "도움말"]
SUBS = ["예약", "체크인", "체크아웃", "고객 서비스", "안내"]

SCENE = '''<svg class="scene" viewBox="0 0 800 200" preserveAspectRatio="xMidYMax slice" aria-hidden="true">
<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="var(--sky1)"/><stop offset="1" stop-color="var(--sky2)"/></linearGradient></defs>
<rect width="800" height="200" fill="url(#sky)"/><circle cx="300" cy="92" r="18" fill="var(--sun)"/>
<path d="M0 160 L80 132 L160 146 L250 120 L340 142 L430 126 L520 144 L800 130 V200 H0Z" fill="var(--m1)"/>
<path d="M0 176 L120 160 L260 170 L400 156 L560 168 L800 158 V200 H0Z" fill="var(--m2)"/>
<g><rect x="560" y="44" width="120" height="146" fill="var(--wall)"/><rect x="552" y="36" width="136" height="10" rx="2" fill="var(--roof)"/>
<g fill="var(--sky1)" opacity=".85">''' + "".join(f'<rect x="{572+c*20}" y="{56+r*16}" width="10" height="9" rx="1"/>' for r in range(7) for c in range(5)) + '''</g>
<path d="M590 172 h60 v-6 h-60z" fill="var(--wood)"/><rect x="606" y="172" width="28" height="18" fill="var(--roof)"/>
<rect x="480" y="104" width="70" height="86" fill="var(--wall)" opacity=".8"/><rect x="474" y="98" width="82" height="8" rx="2" fill="var(--roof)"/>
<g fill="var(--sky1)" opacity=".7">''' + "".join(f'<rect x="{490+c*18}" y="{116+r*16}" width="9" height="8" rx="1"/>' for r in range(4) for c in range(3)) + '''</g></g>
<g><path d="M720 200 Q724 160 716 128" stroke="var(--wood)" stroke-width="5" fill="none"/>
<path d="M716 128 q-26 -6 -40 10 M716 128 q-20 -18 -38 -12 M716 128 q22 -16 40 -6 M716 128 q26 2 34 18 M716 128 q2 -20 -6 -30" stroke="var(--pine)" stroke-width="6" fill="none" stroke-linecap="round"/></g>
</svg>'''

EXTRA_CSS = '''
/* sample-only additions: speaker labels, level chip, drills, TOEIC, class toggles */
.lvl{font-size:12px;font-weight:700;color:var(--accent);background:var(--accent-soft);border-radius:999px;padding:1px 9px;align-self:center}
.turn{display:grid;grid-template-columns:auto minmax(0,1fr);column-gap:8px;align-items:baseline}
.turn+.turn{margin-top:6px}
.turn .k,.turn .m{grid-column:2}
.who{font-size:12px;font-weight:700;color:var(--muted);white-space:nowrap}
.turn.s .who,.dlg .line.st .who{color:var(--accent)}
.dlg .line .k .who{margin-right:8px}
.line .k{font-family:var(--display);font-weight:500}
.word>.line.head .k{font-family:var(--display)}
.gl .en{color:var(--ink);font-weight:600}
.drill+.drill{margin-top:14px}
.dpat{display:flex;flex-wrap:wrap;gap:4px 12px;align-items:baseline;padding:6px 12px;border-left:4px solid var(--accent);background:var(--accent-soft);border-radius:0 10px 10px 0}
.dpat b{font-family:var(--display);font-size:17px}
.dpat span{color:var(--muted);font-size:14px}
.drill .rows{border:1px solid var(--line);border-radius:10px;margin-top:6px;overflow:hidden}
.drill .line{grid-template-columns:minmax(0,1fr) 38px;padding:8px 12px}
.drill .line>div{grid-column:1;grid-row:1}.drill .line>.spk{grid-column:2;grid-row:1}
.seg .ll{display:inline!important}
.drill .line .k{font-size:16px}
.tq{border:1px solid var(--line);border-radius:12px;padding:10px 14px;display:flex;flex-direction:column;gap:8px}
.tq+.tq{margin-top:10px}
.tqh{display:flex;align-items:center;gap:10px}
.tqh .exn{display:grid;place-items:center;width:22px;height:22px;border-radius:50%;background:var(--accent-soft);color:var(--accent);font-size:12px;font-weight:700}
.tpart{font-size:13px;font-weight:700;color:var(--accent)}
.tqh .spk{margin-left:auto;width:34px;height:34px}
.tshow{order:2;display:inline-flex;align-items:center;gap:5px;font-size:13px;font-weight:500;color:var(--muted);cursor:pointer;white-space:nowrap}
.tshow input{accent-color:var(--accent)}
body:not(.show-lis) .tq.lis .tqq,body:not(.show-lis) .tq.lis .topt .ot{filter:blur(7px);user-select:none}
.topt .ol{font-weight:700}
.tqq{margin:0;font-family:var(--display);font-size:17px}
.tnote{margin:-4px 0 0;font-size:12.5px;color:var(--muted)}
.topts{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:6px}
.topt{text-align:left;border:1px solid var(--line);background:var(--sheet);color:var(--ink);border-radius:10px;padding:8px 12px;font:inherit;font-family:var(--display);font-size:15px;cursor:pointer}
.topt:hover:not(:disabled){border-color:var(--accent)}
.topt.right{border-color:var(--good);background:var(--good-soft)}
.topt.wrong{border-color:var(--bad);background:var(--bad-soft)}
.topt:disabled{cursor:default}
.twhy{margin:0;font-size:14px;color:var(--ink);background:var(--raise);border-radius:8px;padding:6px 10px}
.twhy b{color:var(--good)}
.class-row{display:flex;flex-wrap:wrap;justify-content:center;gap:6px 16px;width:100%;font-size:13px;color:var(--muted)}
.class-row label{display:inline-flex;align-items:center;gap:5px;cursor:pointer;white-space:nowrap}
.class-row input{accent-color:var(--accent)}
.hide-ko #view .m,.hide-ko #view .gm,.hide-ko #view .qa .a{filter:blur(6px);cursor:pointer;user-select:none}
.hide-en #view .k,.hide-en #view .tqq{filter:blur(7px);cursor:pointer;user-select:none}
.hide-st #view .dlg .line.st .k,.hide-st #view .turn.s .k{filter:blur(7px);cursor:pointer;user-select:none}
#view .show{filter:none!important}
.lesson{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:6px;margin:0;padding:0;list-style:none;counter-reset:st}
.lesson li{border:1px solid var(--line);border-radius:10px;padding:6px 10px;font-size:13.5px;line-height:1.45;counter-increment:st}
.lesson li b{display:block;color:var(--accent);font-size:13px}
.lesson li b::before{content:counter(st) ". "}
.groups .group.sep::before,.groups .group:last-child::after{content:"|";position:absolute;top:50%;transform:translate(-50%,-55%);color:var(--muted);opacity:.7;font-weight:400;pointer-events:none;border:0}
.groups .group.sep::before{left:-9px}
.groups .gsep+.group.sep::before{display:none!important}
.groups .gsep{flex:none;width:1.5px;height:1.05em;background:var(--muted);opacity:.55;align-self:center;margin-right:-8.5px;transform:translateY(-1px)}
.groups .group:last-child::after{left:calc(100% + 9px)}
.groups .group:last-child{margin-right:14px}
.band p.intro{font-size:14.5px;line-height:1.6}
.seg .sh{display:none}
@media (max-width:600px){.seg .lg{display:none}.seg .sh{display:inline}}
.sample-note{font-size:12.5px;color:var(--muted);text-align:center;margin:0}
'''

JS = r'''
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
let REP=1,RATE=1,run=0,cur=null;
const voices=()=>speechSynthesis.getVoices().filter(v=>/^en[-_]US/i.test(v.lang));
function pick(who){const v=voices();if(!v.length)return null;const f=v.find(x=>/female|samantha|jenny|aria|zira/i.test(x.name)),m=v.find(x=>/male|guy|david|alex|daniel/i.test(x.name)&&!/female/i.test(x.name));return who==="G"?(m||v[0]):(f||v[0])}
function say(t,who){return new Promise(r=>{const u=new SpeechSynthesisUtterance(t);u.lang="en-US";u.rate=RATE;const v=pick(who);if(v)u.voice=v;u.onend=u.onerror=r;speechSynthesis.speak(u)})}
async function playEls(els,label){stop();const my=++run;$("#player").hidden=false;document.body.classList.add("has-player");
  for(let k=0;k<els.length;k++){const el=els[k];if(my!==run)return;el.classList.add("now");el.scrollIntoView({block:"nearest",behavior:"smooth"});
    for(let i=0;i<REP;i++){if(my!==run)break;$("#pt").textContent=label||el.dataset.say;await say(el.dataset.say,el.dataset.who||"G");if(el.dataset.say2&&my===run)await say(el.dataset.say2,"S")}
    el.classList.remove("now")}
  if(my===run)stop()}
function stop(){run++;speechSynthesis.cancel();$$(".now").forEach(x=>x.classList.remove("now"));$("#player").hidden=true;document.body.classList.remove("has-player")}
document.addEventListener("click",ev=>{const b=ev.target.closest("button");
  const bl=ev.target.closest(".m,.k,.gm,.a,.tqq");if(bl&&!b&&getComputedStyle(bl).filter!=="none"){bl.classList.toggle("show");return}
  if(!b)return;
  if(b.classList.contains("spk")){const el=b.closest("[data-say]");if(el)playEls([el]);return}
  if(b.classList.contains("wrep")&&b.closest(".word")){playEls([...b.closest(".word").querySelectorAll("[data-say]")]);return}
  if(b.id==="dlgAll"){playEls($$(".dlg .line"));return}
  if(b.id==="playAll"){playEls($$("#view [data-say]").filter(x=>!x.closest(".tq")));return}
  if(b.id==="pstop"){stop();return}
  if(b.classList.contains("btn")&&b.closest(".qa")){const a=b.closest(".qa").querySelector(".a");a.hidden=!a.hidden;b.textContent=a.hidden?"답 보기":"답 숨기기";return}
  if(b.classList.contains("topt")){const q=b.closest(".tq");q.querySelectorAll(".topt").forEach(o=>{o.disabled=true;if(o.dataset.ok==="1")o.classList.add("right")});
    if(b.dataset.ok!=="1")b.classList.add("wrong");const w=q.querySelector(".twhy");w.innerHTML=(b.dataset.ok==="1"?"<b>정답입니다.</b> ":"<b>정답: "+q.querySelector('[data-ok="1"] .ol').textContent+"</b> ")+w.textContent;w.hidden=false;return}
  if(b.classList.contains("group")||b.classList.contains("sub")||b.classList.contains("pn")||b.classList.contains("relrow")||(b.dataset.mode&&b.dataset.mode!=="learn")){$("#soon").hidden=false;setTimeout(()=>$("#soon").hidden=true,2200)}
});
$("#repSel").onchange=e=>REP=+e.target.value;$("#rateSel").onchange=e=>RATE=+e.target.value;
for(const [id,c] of [["tKo","hide-ko"],["tEn","hide-en"],["tSt","hide-st"]])$("#"+id).onchange=e=>{document.body.classList.toggle(c,e.target.checked);$$("#view .show").forEach(x=>x.classList.remove("show"))};
$("#tShow").onchange=e=>document.body.classList.toggle("show-lis",e.target.checked);
document.addEventListener("keydown",e=>{if(e.key==="Escape")stop()});
speechSynthesis.getVoices();
'''

def page():
    SEP = {"기초회화", "TOEIC", "도움말"}   # RYU: | before 기초회화, TOEIC, 도움말 and after 도움말
    groups = "".join(f'<button class="group{" sep" if g in SEP else ""}" type="button" aria-pressed="{"true" if g=="프런트" else "false"}"><span class="gn">{g}</span></button>' for g in GROUPS)
    subs = "".join(f'<button class="sub" type="button" role="tab" aria-selected="{"true" if s=="체크인" else "false"}"><span class="code">{i:02d}</span><span class="name">{s}</span></button>' for i, s in enumerate(SUBS, 1))
    nW = len(WORDS); nS = sum(len(x[4]) * 2 for x in WORDS) + len(DIALOG) + sum(len(d[2]) for d in DRILLS)
    return f'''<title>호텔서비스 영어 예문보기</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=IBM+Plex+Sans+KR:wght@400;500;600&display=swap">
<style>{CSS}{EXTRA_CSS}</style>
<div class="wrap" id="app" data-g="K1">
  <header class="top">{SCENE}
    <div class="brand"><span class="eyebrow">호텔경영학과 · 기초 회화부터 실무 영어·TOEIC까지</span><h1>호텔서비스 영어</h1></div>
    <div class="stats"><span><b>8</b>대분류</span><span><b>990</b>단어</span><span><b>1,980</b>문장</span></div>
  </header>
  <label class="search" for="q"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
    <input id="q" type="search" placeholder="영어나 뜻으로 검색 (예: deposit, 보증금)" autocomplete="off"></label>
  <div class="menubox"><nav class="groups" aria-label="대분류"><span class="gsep" aria-hidden="true"></span>{groups}</nav><nav class="subs" role="tablist" aria-label="소분류">{subs}</nav>
    <div class="sinfo"><b>[3-02]</b> 체크인 · 3묶음 30단어 (미리보기는 첫 묶음만 열림)</div></div>
  <section class="sheet" id="sheet">
    <div class="band" id="band"><div class="bandin">
      <div class="dd" id="bsel"><button class="bsel ddb" id="bselBtn" type="button"><span class="ddn">[3-02-01]</span><span class="ddk">체크인 기본 응대</span><span class="ddo">Check-in Basics</span></button></div>
      <p class="intro">프런트에서 손님을 맞아 예약 확인, 신분 확인, 등록 카드, 보증금, 카드키 전달까지 체크인 한 번의 흐름을 영어로 익힙니다.</p>
      <div class="tipbox"><p>• 학습 목표: 체크인 절차를 영어로 안내하고 손님의 질문 4가지(예약·조식·이른 체크인·업그레이드)에 답할 수 있다.</p>
      <p>• 직원 문장은 May I…? / Could you…? / Please… 처럼 공손한 표현을 씁니다.</p>
      <p>• TOEIC 연계: Part 2 의문사 질문 응답, Part 5 수동태(will be refunded)와 형용사 자리(valid ID).</p></div>
    </div></div>
    <div class="controls" id="controls">
      <div class="seg" role="group" aria-label="학습 방식">
        <button data-mode="learn" type="button" aria-pressed="true"><span class="lg">문장보기</span><span class="sh">문장</span></button>
        <button data-mode="cards" type="button" aria-pressed="false"><span class="lg">주요단어</span><span class="sh">단어</span></button>
        <button data-mode="quiz" type="button" aria-pressed="false"><span class="lg">복습퀴즈</span><span class="sh">퀴즈</span></button>
      </div>
      <div class="opts"><label class="ctl"><span>횟수</span><select id="repSel" class="bsel"><option value="1">1회</option><option value="2">2회</option><option value="3">3회</option><option value="5">5회</option></select></label>
      <label class="ctl"><span>속도</span><select id="rateSel" class="bsel"><option value="0.8">×0.8</option><option value="0.9">×0.9</option><option value="1" selected>×1.0</option><option value="1.2">×1.2</option></select></label></div>
      <div class="rowbtns"><button class="wrep tbtn" type="button" id="playAll">{REP}묶음 전체 듣기</button></div>
      <div class="class-row" aria-label="수업용 가리기">
        <label><input type="checkbox" id="tKo">한국어 뜻 가리기</label>
        <label><input type="checkbox" id="tEn">영어 가리기 (통역 연습)</label>
        <label><input type="checkbox" id="tSt">직원 대사 가리기 (역할극)</label></div>
    </div>
    <div class="body" id="view">
      <section class="sec"><h3>체크인 대화<button class="wrep hrep" type="button" id="dlgAll">{REP}대화 반복</button></h3><div class="rows dlg">{dialog_html()}</div></section>
      <section class="sec"><h3>단어와 예문</h3>{words_html()}</section>
      <section class="sec"><h3>바꿔 말하기</h3>{drills_html()}</section>
      <section class="sec"><h3>정리</h3><div class="tip"><p class="note-ko">체크인은 ① 환영 인사 → ② 예약 확인(under the name ~) → ③ 신분 확인(May I see ~?) → ④ 등록 카드·서명 → ⑤ 보증금 안내 → ⑥ 카드키·객실 안내(Enjoy your stay.) 순서로 진행합니다.</p></div></section>
      <section class="sec"><h3>확인 문제</h3>{qa_html()}</section>
      <section class="sec"><h3>TOEIC 연계<label class="tshow"><input type="checkbox" id="tShow">듣기 문제 영어 보기</label></h3>{toeic_html()}</section>
      <div class="relbox"><div class="relhd">관련 묶음</div>
        <button class="relrow" type="button"><span class="rc">[3-01-02]</span><span>예약 변경·취소·노쇼</span><span class="ddo">Changes &amp; Cancellations</span></button>
        <button class="relrow" type="button"><span class="rc">[3-03-01]</span><span>체크아웃과 정산</span><span class="ddo">Check-out</span></button>
        <button class="relrow" type="button"><span class="rc">[6-01-01]</span><span>불만 처리와 사과</span><span class="ddo">Handling Complaints</span></button>
        <button class="relrow" type="button"><span class="rc">[7-01-01]</span><span>Part 1·2 사진 묘사와 질의응답</span><span class="ddo">TOEIC LC</span></button></div>
      <div class="pnrow"><button class="pn pv" type="button"><b>← 이전 묶음</b><small>[3-01-02] 예약 변경·취소·노쇼</small></button><button class="pn nx" type="button"><b>다음 묶음 →</b><small>[3-02-02] 객실 배정·업그레이드·초과 예약</small></button></div>
      <p class="sample-note" id="soon" hidden>미리보기에서는 이 한 페이지만 열려 있어요.</p>
    </div>
  </section>
  <div class="player" id="player" hidden><span class="t" id="pt"></span><button id="pstop" type="button"><span class="bt">정지</span></button></div>
  <p class="foot">🔊 소리는 기기의 영어 음성으로 읽습니다(정식 앱은 mp3 저장). 손님은 남성, 직원은 여성 음성으로 나눠 들려줍니다. 학습 기록 체크는 두지 않습니다.</p>
  <p class="ver">예문보기 샘플 · 이 페이지 {nW}단어 {nS}문장 · 예문 출처: Practical Hotel English (체크인) · 대화·바꿔 말하기·TOEIC 문항은 새로 작성</p>
</div>
<script>{JS}</script>'''

out = os.path.join(H, "..", "preview", "hotel_english_sample.html")
open(out, "w", encoding="utf8").write(page())
print("written", os.path.getsize(out))
