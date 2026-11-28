# 7 TOEIC — hotel / travel / business settings. Listening = Part 1-4 (text hidden until 듣기 문제 영어 보기).
def W(w, ko, lv, *pairs): return (w, None, ko, lv, list(pairs))
T = {"wl": ["질문", "응답"], "ww": ["A", "B"], "ord": ["sm", "tq", "w", "dr", "qa"], "tqt": "연습 문제", "wt": "빈출 단어와 문장", "drt": "자주 나오는 표현"}

SUBS = [
{"n": "LC 듣기", "b": [
 dict(T, **{"t": "Part 1·2 사진 묘사와 질의응답", "en": "TOEIC LC Part 1 & 2",
  "i": "Part 1(사진 묘사)과 Part 2(질의응답)의 문제 유형과 풀이 전략을 호텔·여행 장면으로 연습합니다.",
  "tp": ["Part 1: 사진에 '보이는 것'만 고릅니다. 사람이 있으면 동작(is ~ing), 사물만 있으면 상태(is placed / has been ~ed).",
         "Part 2: 질문의 첫 단어(의문사)를 놓치지 마세요. 같은 단어·비슷한 발음이 들리는 보기는 대부분 함정입니다.",
         "연습 방법: 🔊로 듣고 답을 고른 뒤, '듣기 문제 영어 보기'에 체크해 스크립트를 확인하세요."],
  "sm": ["Part 1 함정: ① 사진에 없는 사물 ② 동작은 맞지만 대상이 틀림 ③ is being ~ed(지금 ~되는 중)와 has been ~ed(이미 ~되어 있음) 혼동",
         "Part 2 정답 패턴: Where → 장소 / When → 시간 / Who → 사람·부서 / Why → 이유(Because 생략 많음) / 부탁(Could you ~?) → Sure, I'll ~ / 제안(Why don't we ~?) → That's a good idea. / 모를 때 I'm not sure. Let me check.도 자주 정답입니다."],
  "tq": [("Part 1 · 사진 묘사", "사진: 여자가 프런트 데스크에서 카드키를 건네고 있다.", ["She's handing a key card to a guest.", "She's typing on a laptop.", "She's opening a suitcase.", "She's cleaning the counter."], 0, "동작(handing)과 대상(key card)이 모두 맞는 (A)가 정답입니다.", "(A) She's handing a key card to a guest. (B) She's typing on a laptop. (C) She's opening a suitcase. (D) She's cleaning the counter."),
         ("Part 1 · 사진 묘사", "사진: 빈 레스토랑에 테이블마다 접시와 잔이 놓여 있다.", ["Some diners are eating.", "Tables have been set for a meal.", "A waiter is pouring water.", "Chairs are being stacked."], 1, "사람이 없는 사진이므로 상태를 나타내는 have been set이 정답입니다. (C)(D)는 사람이 필요합니다.", "(A) Some diners are eating. (B) Tables have been set for a meal. (C) A waiter is pouring water. (D) Chairs are being stacked."),
         ("Part 1 · 사진 묘사", "사진: 남자가 객실 창문의 커튼을 열고 있다.", ["He's opening the curtains.", "He's looking out of a car.", "He's making the bed.", "He's closing a door."], 0, "커튼을 여는 동작을 정확히 묘사했습니다.", "(A) He's opening the curtains. (B) He's looking out of a car. (C) He's making the bed. (D) He's closing a door."),
         ("Part 2 · 질의응답", "When does the conference start?", ["At 9 tomorrow morning.", "In the Grand Ballroom.", "Mr. Lee is the speaker."], 0, "When → 시간."),
         ("Part 2 · 질의응답", "Who's going to pick up the guests at the airport?", ["Our driver, Mr. Cho.", "At Terminal 1.", "They picked a nice hotel."], 0, "Who → 사람. (C)는 pick을 반복한 함정입니다."),
         ("Part 2 · 질의응답", "Why was the flight delayed?", ["Because of heavy snow.", "Gate 15.", "It was a long flight."], 0, "Why → 이유."),
         ("Part 2 · 질의응답", "Could you print this boarding pass for me?", ["Sure, give me a minute.", "The printer is new.", "I boarded at 10."], 0, "부탁에는 수락하는 응답이 정답입니다."),
         ("Part 2 · 질의응답", "Why don't we have lunch at the new Italian place?", ["That sounds great.", "I had pasta.", "It's on the 3rd floor."], 0, "Why don't we ~? 는 이유가 아니라 제안입니다. 동의하는 응답이 정답입니다."),
         ("Part 2 · 질의응답", "The room is ready, isn't it?", ["Yes, you can go up now.", "I'm ready to go.", "It's a twin room."], 0, "부가 의문문(~, isn't it?)은 Yes/No 질문처럼 답합니다."),
         ("Part 2 · 질의응답", "Which floor is the gym on?", ["I'm not sure. Let me check.", "It's very large.", "I go there every day."], 0, "모른다는 응답(I'm not sure. Let me check.)도 자주 정답입니다.")],
  "w": [W("is being ~ed", "~되는 중이다", "중", ("Is the room being cleaned?", "방이 청소되는 중인가요?", "Yes, it's being cleaned now.", "네, 지금 청소 중이에요."), ("Are the tables being set?", "테이블이 차려지는 중인가요?", "Yes, the staff are setting them now.", "네, 직원들이 지금 차리고 있어요.")),
        W("has been ~ed", "~되어 있다 (완료)", "중", ("Has the luggage been delivered?", "짐이 배달되었나요?", "Yes, it has been delivered to your room.", "네, 객실로 배달되었습니다."), ("Has the meeting been canceled?", "회의가 취소되었나요?", "No, it's been moved to Friday.", "아니요, 금요일로 옮겨졌어요.")),
        W("in charge of", "~을 담당하는", "중", ("Who's in charge of the event?", "행사 담당자가 누구예요?", "Ms. Han is in charge of it.", "한 과장이 담당해요."), ("I'm in charge of the front desk tonight.", "오늘 밤 프런트 책임자는 저예요.", "Good to know.", "알겠어요.")),
        W("delayed", "지연된", "중", ("Why is the shuttle late?", "셔틀이 왜 늦어요?", "It was delayed by traffic.", "교통 체증으로 지연됐어요."), ("Is your flight delayed?", "비행기가 지연됐어요?", "Yes, by two hours.", "네, 두 시간이요.")),
        W("Why don't we ~?", "~하는 게 어때요? (제안)", "중", ("Why don't we take a taxi?", "택시 타는 게 어때요?", "Good idea. It's raining.", "좋아요. 비가 오네요."), ("Why don't we meet at 3?", "3시에 만나는 게 어때요?", "That works for me.", "저는 좋아요.")),
        W("pick up", "데리러 가다, 찾아오다", "중", ("Can you pick me up at the station?", "역으로 데리러 와 줄래요?", "Sure, what time?", "네, 몇 시에요?"), ("Where do I pick up my laundry?", "세탁물은 어디서 찾아요?", "At the front desk after 5.", "5시 이후 프런트에서요.")),
        W("sign up", "등록하다, 신청하다", "중", ("How do I sign up for the tour?", "투어는 어떻게 신청해요?", "Just sign up at the concierge desk.", "컨시어지 데스크에서 신청하세요."), ("Did you sign up for the workshop?", "워크숍 신청했어요?", "Yes, I signed up yesterday.", "네, 어제 했어요.")),
        W("available", "이용 가능한, 시간이 되는", "중", ("Are you available this afternoon?", "오늘 오후에 시간 돼요?", "Yes, after 2.", "네, 2시 이후에요."), ("Is the meeting room available?", "회의실 이용 가능해요?", "Yes, it's free until noon.", "네, 정오까지 비어 있어요.")),
        W("I'm not sure", "잘 모르겠어요", "하", ("When will the manager be back?", "매니저는 언제 돌아와요?", "I'm not sure. Let me ask.", "잘 모르겠어요. 물어볼게요."), ("Is the pool open today?", "오늘 수영장 열어요?", "I'm not sure, but I'll check.", "잘 모르겠지만 확인해 볼게요.")),
        W("set up", "준비하다, 설치하다", "중", ("Who will set up the projector?", "프로젝터는 누가 설치해요?", "The AV team will set it up.", "AV팀이 설치할 거예요."), ("The room is set up for 50 people.", "방이 50명용으로 준비되어 있어요.", "Perfect, thank you.", "완벽해요, 고마워요."))],
  "dr": [("~ is being ...ed.", "~이 ...되는 중이다. (Part 1)", [("The room is being cleaned.", "방이 청소되는 중이다."), ("The tables are being set.", "테이블이 차려지는 중이다."), ("A car is being parked.", "차가 주차되는 중이다.")]),
         ("~ has been ...ed.", "~이 ...되어 있다. (Part 1)", [("Tables have been set for dinner.", "테이블이 저녁 식사용으로 차려져 있다."), ("Towels have been folded on the bed.", "수건이 침대 위에 개어져 있다."), ("A sign has been placed by the door.", "문 옆에 표지판이 놓여 있다.")]),
         ("Let me ~.", "제가 ~할게요. (Part 2 정답 단골)", [("Let me check.", "확인해 볼게요."), ("Let me ask the manager.", "매니저에게 물어볼게요."), ("Let me find out for you.", "알아봐 드릴게요.")])],
  "qa": [("Part 2에서 Why don't we ~? 는 무슨 뜻?", "~하는 게 어때요? (제안)"), ("사람이 없는 Part 1 사진에서 자주 정답인 형태는?", "has / have been + 과거분사 (~되어 있다)"), ("Part 2에서 같은 단어가 반복되는 보기는?", "대부분 함정"), ("\"I'm not sure. Let me check.\"의 뜻은?", "잘 모르겠어요. 확인해 볼게요.")],
  "rel": ["7-01-02", "3-02-01", "1-04-02"]}),
 dict(T, **{"t": "Part 3·4 대화와 담화", "en": "TOEIC LC Part 3 & 4",
  "i": "Part 3(두세 사람의 대화)과 Part 4(안내 방송·전화 메시지)를 호텔·출장 상황으로 연습합니다. 질문을 먼저 읽고 듣는 습관을 익힙니다.",
  "tp": ["듣기 전에 질문을 먼저 읽고 무엇을 들어야 할지(장소, 문제, 다음 행동)를 정합니다.",
         "자주 나오는 질문: Where most likely ~? / What is the problem? / What will the man probably do next?",
         "정답은 대화의 말을 그대로 쓰지 않고 바꿔 말하는(paraphrase) 경우가 많습니다. 예: book a table → make a reservation."],
  "sm": ["Part 3·4 질문 3종: ① 주제·장소(첫 부분에 나옴) ② 세부 정보(숫자·시간·이유) ③ 다음 행동(마지막 부분: I'll ~ / Let me ~)",
         "바꿔 말하기 예: call back → return a call / fix → repair / cheap → affordable / ticket → admission / boss → supervisor"],
  "tq": [("Part 3 · 짧은 대화", "Where most likely are the speakers?", ["At a hotel front desk", "At an airport", "At a restaurant", "At a train station"], 0, "check in, room, key card 같은 단어로 호텔 프런트임을 알 수 있습니다.", "M: Hi, I'd like to check in. The name is Wilson.\nW: Welcome, Mr. Wilson. You're in room 804. Here's your key card.\nM: Thanks. Is there a gym in the hotel?\nW: Yes, on the 3rd floor. It's open 24 hours."),
         ("Part 3 · 짧은 대화", "What will the woman probably do next?", ["Call a taxi", "Send a technician", "Change the man's room", "Check the bill"], 1, "마지막 문장 I'll send a technician up right away 가 다음 행동입니다.", "M: Excuse me, the heater in my room isn't working.\nW: I'm sorry about that. What's your room number?\nM: It's 1102.\nW: I'll send a technician up right away."),
         ("Part 3 · 짧은 대화", "What is the problem?", ["A reservation is missing.", "A room is too noisy.", "A flight is canceled.", "A bill is incorrect."], 0, "I can't find your name in our system 이라는 말에서 예약이 없다는 것을 알 수 있습니다.", "W: Good evening. I have a reservation for tonight. Emma Clark.\nM: Let me see... I'm sorry, I can't find your name in our system.\nW: But I booked it online last week.\nM: Could you show me the confirmation email?"),
         ("Part 4 · 짧은 담화", "What is the purpose of the announcement?", ["To announce a pool closure", "To introduce a new chef", "To explain a fire drill", "To promote a spa discount"], 2, "fire drill(소방 훈련)을 안내하는 방송입니다.", "Good morning, guests. This is a reminder that we will hold a fire drill today at 11 a.m. You will hear the fire alarm for about two minutes. There is no need to leave your room. We apologize for any inconvenience."),
         ("Part 4 · 짧은 담화", "What is the listener asked to do?", ["Visit the hotel", "Return a call", "Pay a deposit", "Cancel a booking"], 1, "please call me back(다시 전화해 달라)을 return a call로 바꿔 말했습니다.", "Hello, Ms. Rivera. This is Jun from the Seoul Grand Hotel. I'm calling about your reservation next week. We need your arrival time to arrange the airport pickup. Please call me back at 02-123-4567. Thank you."),
         ("Part 4 · 짧은 담화", "How long will the lobby renovation take?", ["One week", "Two weeks", "One month", "Three months"], 1, "for two weeks 라고 말합니다.", "Attention, staff. Starting next Monday, the main lobby will be closed for renovation for two weeks. During this time, guests will check in at the temporary desk on the second floor. Please guide guests there.")],
  "w": [W("most likely", "아마, ~일 가능성이 가장 높은", "중", ("Where are they most likely?", "그들은 아마 어디에 있나요?", "Probably in a restaurant.", "아마 식당이요."), ("Who most likely is the woman?", "여자는 아마 누구인가요?", "She's probably a hotel receptionist.", "아마 호텔 접수원일 거예요.")),
        W("purpose", "목적", "중", ("What's the purpose of your visit?", "방문 목적이 뭐예요?", "I'm here on business.", "출장이에요."), ("What's the purpose of the call?", "전화한 목적이 뭐예요?", "To confirm a booking.", "예약을 확인하려고요.")),
        W("return a call", "답신 전화를 하다", "상", ("Did you return Mr. Kim's call?", "김 선생님께 답신 전화했어요?", "Yes, I called him back this morning.", "네, 오늘 아침에 다시 걸었어요."), ("Please return my call when you can.", "가능할 때 답신 전화 주세요.", "I will. Thank you.", "그럴게요. 고마워요.")),
        W("announcement", "안내 방송, 공지", "중", ("Did you hear the announcement?", "안내 방송 들었어요?", "Yes, the pool closes early today.", "네, 오늘 수영장이 일찍 닫는대요."), ("I'd like to make an announcement.", "공지 사항이 있습니다.", "Everyone, please listen.", "모두 들어 주세요.")),
        W("renovation", "보수 공사", "상", ("Why is the lobby closed?", "로비가 왜 닫혔어요?", "It's under renovation.", "보수 공사 중이에요."), ("How long will the renovation take?", "공사는 얼마나 걸려요?", "About two weeks.", "2주쯤이요.")),
        W("temporary", "임시의", "상", ("Where do I check in?", "어디서 체크인해요?", "At the temporary desk on the 2nd floor.", "2층 임시 데스크에서요."), ("Is this a temporary job?", "임시직이에요?", "Yes, it's for the summer.", "네, 여름 동안이에요.")),
        W("reminder", "다시 알림, 상기시키는 것", "상", ("This is a reminder about your appointment.", "예약을 다시 알려 드립니다.", "Thanks. I almost forgot.", "고마워요. 깜빡할 뻔했어요."), ("Can you send me a reminder?", "알림 좀 보내 줄래요?", "Sure, I'll text you the day before.", "네, 하루 전에 문자 드릴게요.")),
        W("arrange", "준비하다, 마련하다", "중", ("Can you arrange a pickup?", "픽업 준비해 줄 수 있어요?", "Yes, I'll arrange a car for 3 p.m.", "네, 오후 3시로 차를 준비할게요."), ("Who arranged the meeting?", "회의는 누가 잡았어요?", "Ms. Lee did.", "이 과장이요.")),
        W("technician", "기술자, 수리 기사", "상", ("The Wi-Fi isn't working.", "와이파이가 안 돼요.", "I'll send a technician.", "기사를 보내 드릴게요."), ("When will the technician come?", "기사는 언제 와요?", "Within 30 minutes.", "30분 안에요.")),
        W("inconvenience", "불편", "중", ("Sorry for the inconvenience.", "불편을 드려 죄송합니다.", "That's all right.", "괜찮아요."), ("Was there any inconvenience?", "불편한 점 있으셨어요?", "No, everything was perfect.", "아니요, 다 완벽했어요."))],
  "dr": [("I'm calling about ~.", "~ 때문에 전화드립니다. (Part 4 메시지 첫 문장)", [("I'm calling about your reservation.", "예약 때문에 전화드립니다."), ("I'm calling about the job interview.", "면접 때문에 전화드립니다."), ("I'm calling about your lost bag.", "잃어버리신 가방 때문에 전화드립니다.")]),
         ("Please call me back at ~.", "~로 다시 전화 주세요.", [("Please call me back at 02-123-4567.", "02-123-4567로 다시 전화 주세요."), ("Please call me back at your convenience.", "편하실 때 다시 전화 주세요."), ("Please call me back before 5 p.m.", "오후 5시 전에 다시 전화 주세요.")]),
         ("We apologize for ~.", "~에 대해 사과드립니다. (안내 방송 마무리)", [("We apologize for any inconvenience.", "불편을 드려 죄송합니다."), ("We apologize for the delay.", "지연에 대해 사과드립니다."), ("We apologize for the noise.", "소음에 대해 사과드립니다.")])],
  "qa": [("Part 3·4에서 듣기 전에 먼저 할 일은?", "질문(과 보기)을 먼저 읽기"), ("call me back을 바꿔 말한 표현은?", "return a call"), ("'다음 행동' 질문의 정답은 대화의 어디에 주로 나오나요?", "마지막 부분"), ("\"temporary\"의 뜻은?", "임시의")],
  "rel": ["7-01-01", "7-03-01", "3-04-02"]})]},
{"n": "RC 읽기", "b": [
 dict(T, **{"t": "Part 5·6 문법과 어휘", "en": "TOEIC RC Part 5 & 6",
  "i": "Part 5(단문 빈칸)와 Part 6(장문 빈칸)에 자주 나오는 문법(품사 자리, 시제, 수동태, 전치사·접속사)을 호텔 문장으로 정리합니다.",
  "tp": ["빈칸 앞뒤만 보고 풀 수 있는 '품사 문제'를 먼저 빠르게 풉니다. 관사 뒤 = 명사, 명사 앞 = 형용사, 동사 옆 = 부사.",
         "시제 문제는 시간 단서(yesterday, next week, since, by the time)를 찾습니다.",
         "Part 6는 앞뒤 문장의 흐름(접속부사 However, Therefore, In addition)을 봅니다."],
  "sm": ["품사 자리: a/the/소유격 + ___ + 전치사 → 명사 / a + ___ + 명사 → 형용사 / be + ___ + p.p. 또는 동사 앞뒤 → 부사 / will·can + ___ → 동사원형",
         "접속사 vs 전치사: although / because / while + 주어·동사, despite / because of / during + 명사. 접속부사: However(그러나), Therefore(그러므로), In addition(게다가), For example(예를 들어)"],
  "tq": [("Part 5 · 단문 빈칸", "The hotel received many positive ------- from guests last year.", ["review", "reviews", "reviewed", "reviewing"], 1, "형용사 positive 뒤, many가 있으므로 복수 명사 reviews."),
         ("Part 5 · 단문 빈칸", "Ms. Tanaka responded ------- to the guest's complaint.", ["quick", "quickly", "quicker", "quickness"], 1, "동사 responded를 꾸미는 부사."),
         ("Part 5 · 단문 빈칸", "The restaurant will be closed ------- the holiday.", ["while", "during", "although", "because"], 1, "뒤에 명사(the holiday)만 있으므로 전치사 during."),
         ("Part 5 · 단문 빈칸", "------- the room was small, it was very clean.", ["Despite", "Although", "Because of", "However"], 1, "뒤에 주어+동사가 있고 '~에도 불구하고'이므로 접속사 Although."),
         ("Part 5 · 단문 빈칸", "By the time the guests arrived, the staff ------- the ballroom.", ["decorate", "decorates", "had decorated", "will decorate"], 2, "손님이 도착한 과거 시점보다 먼저 끝난 일이므로 과거완료 had decorated."),
         ("Part 5 · 단문 빈칸", "All rooms ------- with free high-speed Wi-Fi.", ["equip", "are equipped", "equipping", "have equipped"], 1, "방이 '갖춰진' 것이므로 수동태 are equipped (be equipped with)."),
         ("Part 6 · 장문 빈칸", "Thank you for choosing the Seoul Grand Hotel. Your room has been upgraded to a suite. -------, you will have access to the executive lounge.\n\n빈칸에 알맞은 말은?", ["However", "In addition", "For example", "Instead"], 1, "좋은 소식에 혜택을 하나 더 더하므로 In addition(게다가)."),
         ("Part 6 · 장문 빈칸", "The pool will be closed for cleaning on Monday. -------, guests may use the pool at our sister hotel next door.\n\n빈칸에 알맞은 말은?", ["Therefore", "Instead", "Similarly", "For instance"], 1, "닫는 대신 다른 곳을 이용하라는 내용이므로 Instead(대신)."),
         ("Part 5 · 단문 빈칸", "The manager asked the staff to ------- the new check-in procedure.", ["follow", "following", "followed", "follows"], 0, "ask + 사람 + to 동사원형."),
         ("Part 5 · 단문 빈칸", "This is the ------- hotel in the city.", ["old", "older", "oldest", "most old"], 2, "the + 최상급 + in the city.")],
  "w": [W("equipped with", "~을 갖춘", "상", ("Is the room equipped with a kitchen?", "방에 주방이 갖춰져 있어요?", "Yes, it's equipped with a small kitchen.", "네, 작은 주방이 있어요."), ("The meeting room is equipped with a projector.", "회의실에 프로젝터가 갖춰져 있어요.", "Great, we'll need it.", "좋아요, 필요할 거예요.")),
        W("although", "비록 ~이지만", "중", ("How was the hotel?", "호텔 어땠어요?", "Although it was old, it was very clean.", "오래됐지만 아주 깨끗했어요."), ("Did you enjoy the tour?", "투어 즐거웠어요?", "Yes, although it rained a little.", "네, 비가 좀 오긴 했지만요.")),
        W("despite", "~에도 불구하고", "상", ("Did the event go well?", "행사 잘됐어요?", "Yes, despite the bad weather.", "네, 날씨가 나빴는데도요."), ("Despite the delay, we arrived on time.", "지연에도 불구하고 제시간에 도착했어요.", "That's lucky.", "운이 좋았네요.")),
        W("however", "그러나", "중", ("Is the pool open?", "수영장 열어요?", "Yes. However, it closes early today.", "네. 하지만 오늘은 일찍 닫아요."), ("The room is nice. However, it's noisy.", "방은 좋아요. 그런데 시끄러워요.", "I'll find you a quieter room.", "더 조용한 방을 찾아 드릴게요.")),
        W("in addition", "게다가", "상", ("What's included?", "뭐가 포함돼요?", "Breakfast. In addition, parking is free.", "조식이요. 게다가 주차도 무료예요."), ("In addition to the spa, we have a pool.", "스파 외에 수영장도 있어요.", "Wonderful.", "멋지네요.")),
        W("therefore", "그러므로", "상", ("Why is the price higher?", "가격이 왜 더 높아요?", "It's peak season. Therefore, rates are higher.", "성수기라서요. 그래서 요금이 높아요."), ("The road is closed. Therefore, the bus will be late.", "도로가 막혀서 버스가 늦을 거예요.", "Thanks for letting us know.", "알려 줘서 고마워요.")),
        W("instead", "대신에", "중", ("The pool is closed.", "수영장이 닫았어요.", "You can use the spa instead.", "대신 스파를 이용하실 수 있어요."), ("Can I have tea instead of coffee?", "커피 대신 차 받을 수 있어요?", "Of course.", "물론이죠.")),
        W("procedure", "절차", "상", ("What's the check-in procedure?", "체크인 절차가 어떻게 돼요?", "Show your ID and sign the form.", "신분증을 보여 주고 서류에 서명하세요."), ("Please follow the safety procedure.", "안전 절차를 따라 주세요.", "Understood.", "알겠습니다.")),
        W("respond", "응답하다", "중", ("Did the hotel respond to your email?", "호텔이 이메일에 답했어요?", "Yes, they responded within an hour.", "네, 한 시간 안에 답했어요."), ("Please respond by Friday.", "금요일까지 답해 주세요.", "I will.", "그럴게요.")),
        W("positive", "긍정적인", "중", ("How are the reviews?", "후기가 어때요?", "Most of them are positive.", "대부분 긍정적이에요."), ("Thank you for your positive feedback.", "좋은 의견 감사합니다.", "You deserve it!", "그럴 만해요!"))],
  "dr": [("be equipped with ~", "~을 갖추고 있다", [("All rooms are equipped with free Wi-Fi.", "모든 객실에 무료 와이파이가 있습니다."), ("The gym is equipped with new machines.", "체육관에 새 기구가 갖춰져 있습니다."), ("The ballroom is equipped with a sound system.", "연회장에 음향 시설이 갖춰져 있습니다.")]),
         ("Although ~, ...", "~이지만 ...", [("Although the room was small, it was clean.", "방은 작았지만 깨끗했다."), ("Although it rained, the event was a success.", "비가 왔지만 행사는 성공적이었다."), ("Although he was tired, he smiled at the guests.", "그는 피곤했지만 손님에게 미소 지었다.")]),
         ("In addition, ~", "게다가 ~", [("In addition, parking is free.", "게다가 주차는 무료입니다."), ("In addition, guests can use the lounge.", "게다가 손님은 라운지를 이용할 수 있습니다."), ("In addition, we offer a free airport shuttle.", "게다가 무료 공항 셔틀을 제공합니다.")])],
  "qa": [("관사 뒤, 전치사 앞 빈칸의 품사는?", "명사"), ("although와 despite의 차이는?", "although + 주어·동사 / despite + 명사"), ("\"In addition\"의 뜻은?", "게다가"), ("will 뒤 빈칸에 오는 형태는?", "동사원형")],
  "rel": ["7-02-02", "7-03-01", "1-04-01"]}),
 dict(T, **{"t": "Part 7 독해", "en": "TOEIC RC Part 7",
  "i": "Part 7에 자주 나오는 호텔 관련 글(이메일, 공지, 광고, 문자 대화, 후기)을 읽고 주제·세부 정보·추론 문제를 푸는 연습을 합니다.",
  "tp": ["질문을 먼저 읽고, 질문의 핵심어(날짜, 이름, 숫자)를 지문에서 찾아 그 주변을 읽습니다.",
         "NOT 문제(What is NOT mentioned?)는 보기 하나하나를 지문과 대조합니다.",
         "문자 대화의 의도 파악 문제(What does she mean by ~?)는 앞뒤 메시지를 함께 읽습니다."],
  "sm": ["Part 7 질문 유형: 주제·목적(What is the purpose of ~? → 첫 부분) / 세부 정보(When, How much → 핵심어 찾기) / 추론(What is suggested / implied? → 직접 쓰여 있지 않음) / NOT(언급되지 않은 것) / 의도 파악(문자 대화)",
         "호텔 지문 빈출: confirmation(예약 확인), itinerary(일정표), complimentary(무료의), amenities(편의 시설), valid(유효한), expire(만료되다), refund(환불), voucher(쿠폰)"],
  "tq": [("Part 7 · 이메일", "From: reservations@seoulgrand.com\nTo: Laura Kim\nSubject: Booking Confirmation #SG4471\n\nDear Ms. Kim,\nThank you for booking with us. Your deluxe room is reserved for March 12–14 (2 nights). Your rate includes breakfast and complimentary airport pickup. Please let us know your flight number at least 48 hours before arrival.\n\nQ. What is the purpose of the email?", ["To confirm a booking", "To cancel a reservation", "To advertise a new hotel", "To request a payment"], 0, "제목 Booking Confirmation과 첫 문장으로 예약 확인이 목적임을 알 수 있습니다."),
         ("Part 7 · 이메일", "(위 이메일)\n\nQ. What must Ms. Kim do before she arrives?", ["Pay a deposit", "Send her flight number", "Choose a room", "Book breakfast"], 1, "Please let us know your flight number at least 48 hours before arrival."),
         ("Part 7 · 이메일", "(위 이메일)\n\nQ. What is NOT included in Ms. Kim's rate?", ["Breakfast", "Airport pickup", "Two nights' stay", "Dinner"], 3, "조식, 공항 픽업, 2박은 언급되었지만 저녁 식사는 없습니다."),
         ("Part 7 · 공지", "NOTICE TO GUESTS\nThe outdoor pool will be closed from July 3 to July 5 for maintenance. During this time, guests may use the indoor pool on the B1 level free of charge. Towels are available at the spa reception. We apologize for any inconvenience.\n\nQ. Where can guests get towels?", ["At the outdoor pool", "At the front desk", "At the spa reception", "In their rooms"], 2, "Towels are available at the spa reception."),
         ("Part 7 · 문자 대화", "Jisu (2:10 p.m.): The guest in 1205 wants to check out at 3. Is that OK?\nMr. Han (2:12 p.m.): We're fully booked tonight.\nJisu (2:13 p.m.): So I should tell her no?\nMr. Han (2:14 p.m.): Offer 1 p.m. and free luggage storage.\n\nQ. What does Mr. Han mean when he writes, \"We're fully booked tonight\"?", ["The hotel has no rooms for new guests.", "The room must be ready for the next guest.", "The guest should book another night.", "Jisu should work late tonight."], 1, "만실이라 다음 손님을 위해 방을 준비해야 하므로 늦은 체크아웃이 어렵다는 뜻입니다."),
         ("Part 7 · 후기", "★★★★☆ \"Great location, friendly staff\"\nThe hotel is a five-minute walk from the subway, and the staff were very helpful. Our room was clean, but the Wi-Fi was slow in the evening. Breakfast had many choices. I would stay here again. — Mia, Australia\n\nQ. What is suggested about Mia?", ["She will probably return to the hotel.", "She did not eat breakfast.", "She traveled by car.", "She complained to the manager."], 0, "I would stay here again(다시 묵겠다)에서 다시 올 것임을 추론할 수 있습니다.")],
  "w": [W("confirmation", "확인 (예약 확인)", "중", ("Did you get the confirmation?", "확인 메일 받았어요?", "Yes, it came this morning.", "네, 오늘 아침에 왔어요."), ("Here's your confirmation number.", "예약 확인 번호입니다.", "Thank you. I'll write it down.", "고마워요. 적어 둘게요.")),
        W("complimentary", "무료의", "상", ("Is the water complimentary?", "물은 무료예요?", "Yes, two bottles a day are complimentary.", "네, 하루 두 병은 무료예요."), ("We offer a complimentary shuttle.", "무료 셔틀을 운행합니다.", "How often does it run?", "얼마나 자주 다녀요?")),
        W("itinerary", "여행 일정표", "상", ("Can you send me the itinerary?", "일정표 보내 줄래요?", "Sure. I'll email it today.", "네. 오늘 메일로 보낼게요."), ("What's on the itinerary for day two?", "둘째 날 일정이 뭐예요?", "A tour of the palace.", "궁 투어예요.")),
        W("maintenance", "유지 보수", "중", ("Why is the elevator stopped?", "엘리베이터가 왜 멈췄어요?", "It's under maintenance.", "점검 중이에요."), ("Maintenance is scheduled for Monday.", "월요일에 정비가 예정되어 있어요.", "How long will it take?", "얼마나 걸려요?")),
        W("valid", "유효한", "중", ("Is this coupon still valid?", "이 쿠폰 아직 유효해요?", "Yes, it's valid until June 30.", "네, 6월 30일까지 유효해요."), ("You need a valid passport.", "유효한 여권이 필요해요.", "Mine expires next year.", "제 건 내년에 만료돼요.")),
        W("expire", "만료되다", "상", ("When does the offer expire?", "할인은 언제 끝나요?", "It expires at the end of the month.", "월말에 끝나요."), ("My card has expired.", "카드가 만료됐어요.", "Do you have another card?", "다른 카드 있으세요?")),
        W("voucher", "쿠폰, 상품권", "상", ("Can I use this breakfast voucher?", "이 조식 쿠폰 써도 돼요?", "Yes, just give it to the staff.", "네, 직원에게 주세요."), ("Here's a voucher for a free drink.", "무료 음료 쿠폰입니다.", "Thank you!", "고마워요!")),
        W("location", "위치", "중", ("How's the hotel's location?", "호텔 위치는 어때요?", "It's close to the subway.", "지하철과 가까워요."), ("Our new location opens in May.", "새 지점이 5월에 열어요.", "Where is it?", "어디예요?")),
        W("suggest", "시사하다, 제안하다", "중", ("What do you suggest?", "뭘 제안하세요?", "I suggest booking early.", "일찍 예약하시길 제안해요."), ("The review suggests the staff were friendly.", "후기를 보면 직원이 친절했던 것 같아요.", "That's good to hear.", "다행이네요.")),
        W("mention", "언급하다", "중", ("Did the guest mention any problems?", "손님이 문제를 언급했어요?", "Yes, she mentioned the slow Wi-Fi.", "네, 와이파이가 느리다고 했어요."), ("As mentioned, check-out is at 11.", "말씀드린 대로 체크아웃은 11시예요.", "Got it.", "알겠어요."))],
  "dr": [("~ is valid until ...", "~은 ...까지 유효합니다.", [("This coupon is valid until June 30.", "이 쿠폰은 6월 30일까지 유효합니다."), ("The voucher is valid until the end of the year.", "쿠폰은 연말까지 유효합니다."), ("Your membership is valid until 2028.", "회원 자격은 2028년까지 유효합니다.")]),
         ("Please let us know ~.", "~을 알려 주세요.", [("Please let us know your flight number.", "항공편 번호를 알려 주세요."), ("Please let us know your arrival time.", "도착 시간을 알려 주세요."), ("Please let us know if you have any questions.", "궁금한 점이 있으면 알려 주세요.")]),
         ("~ is available at ...", "~은 ...에서 받을 수 있습니다.", [("Towels are available at the spa reception.", "수건은 스파 접수처에서 받을 수 있습니다."), ("Maps are available at the front desk.", "지도는 프런트에서 받을 수 있습니다."), ("Umbrellas are available at the entrance.", "우산은 입구에서 받을 수 있습니다.")])],
  "qa": [("\"complimentary\"의 뜻은?", "무료의"), ("NOT 문제는 어떻게 푸나요?", "보기를 하나씩 지문과 대조한다"), ("추론(suggested) 문제의 특징은?", "답이 지문에 그대로 쓰여 있지 않다"), ("\"itinerary\"의 뜻은?", "여행 일정표")],
  "rel": ["7-02-01", "7-03-01", "6-02-01"]})]},
{"n": "모의고사", "b": [
 dict(T, **{"t": "미니 모의고사", "en": "TOEIC Mini Test",
  "i": "Part 1부터 Part 7까지 한 문제 유형씩, 모두 14문제로 된 짧은 모의고사입니다. 시험처럼 시간을 재고 풀어 보세요. (권장 시간 15분)",
  "tp": ["듣기(1–7번)는 '듣기 문제 영어 보기'를 끈 상태에서 🔊로 한 번만 듣고 푸세요.",
         "읽기(8–14번)는 한 문제에 1분 이내를 목표로 합니다.",
         "다 푼 뒤 틀린 문제의 해설을 읽고, 관련 묶음으로 돌아가 복습하세요."],
  "ord": ["tq", "sm"], "tqt": "미니 모의고사 (14문제)",
  "sm": ["점수 보기: 12–14개 매우 좋음 / 9–11개 좋음 / 6–8개 기본기 복습 필요 / 5개 이하 1 기초회화와 7 TOEIC 묶음부터 다시",
         "복습 순서: 틀린 Part의 묶음(7-01-01 Part 1·2, 7-01-02 Part 3·4, 7-02-01 Part 5·6, 7-02-02 Part 7)을 다시 보세요."],
  "tq": [("Part 1 · 사진 묘사", "사진: 벨맨이 짐 카트에 가방을 싣고 있다.", ["A bellhop is loading bags onto a cart.", "A woman is unpacking a suitcase.", "Bags are being carried up the stairs.", "A cart is parked in the garage."], 0, "짐을 카트에 싣는(loading onto) 동작을 묘사한 (A)가 정답입니다.", "(A) A bellhop is loading bags onto a cart. (B) A woman is unpacking a suitcase. (C) Bags are being carried up the stairs. (D) A cart is parked in the garage."),
         ("Part 2 · 질의응답", "Where should I leave the room key?", ["At the front desk, please.", "Yes, you can leave now.", "It's a key card."], 0, "Where → 장소."),
         ("Part 2 · 질의응답", "Haven't you met the new chef yet?", ["No, not yet.", "The meat is fresh.", "In the kitchen."], 0, "부정 의문문도 일반 의문문처럼 답합니다: 아직 못 만났으면 No."),
         ("Part 2 · 질의응답", "Should we hold the meeting in the morning or the afternoon?", ["The afternoon works better for me.", "Yes, we should.", "It was a long meeting."], 0, "선택 의문문에는 하나를 고릅니다."),
         ("Part 3 · 짧은 대화", "What does the man want to do?", ["Extend his stay", "Change rooms", "Cancel a tour", "Order breakfast"], 0, "stay one more night = 숙박 연장(extend his stay).", "M: Hi, I'm in room 708. Could I stay one more night?\nW: Let me check... Yes, your room is available tomorrow night too.\nM: Great. Is the rate the same?\nW: Yes, it's the same rate."),
         ("Part 3 · 짧은 대화", "What will the woman probably do next?", ["Check the man's bill", "Call a taxi", "Give the man a map", "Book a restaurant"], 0, "Let me check your bill 이 다음 행동입니다.", "M: I think there's a mistake on my bill. I didn't use the minibar.\nW: I'm sorry about that. Let me check your bill right now.\nM: Thank you."),
         ("Part 4 · 짧은 담화", "What are listeners asked to do?", ["Gather in the lobby", "Bring their passports", "Return to the bus by 4 p.m.", "Buy tickets online"], 2, "Please be back on the bus by 4 p.m. 을 바꿔 말한 (C)가 정답입니다.", "Welcome to Gyeongju, everyone. We will now have two hours of free time to explore the market. Please be back on the bus by 4 p.m. so we can arrive at the hotel before dinner."),
         ("Part 5 · 단문 빈칸", "The hotel offers a ------- airport shuttle every 30 minutes.", ["compliment", "complimentary", "complimenting", "compliments"], 1, "관사 a와 명사 airport shuttle 사이에는 형용사가 옵니다."),
         ("Part 5 · 단문 빈칸", "Guests must check out ------- 11 a.m.", ["by", "until", "since", "during"], 0, "마감 시점 = by."),
         ("Part 5 · 단문 빈칸", "The new spa has been very popular ------- it opened last month.", ["since", "for", "during", "when"], 0, "현재완료 + since + 시작 시점."),
         ("Part 6 · 장문 빈칸", "We are pleased to announce that our rooftop restaurant will reopen on May 1. -------, all guests will receive a free dessert during the first week.\n\n빈칸에 알맞은 말은?", ["However", "To celebrate", "Otherwise", "Instead"], 1, "재개장을 기념해 무료 디저트를 주는 흐름이므로 To celebrate(기념하여)."),
         ("Part 7 · 공지", "STAFF NOTICE\nFrom June 1, all front desk staff must wear the new name tags. Please pick them up from Human Resources on the 2nd floor by May 28. Old name tags should be returned at the same time.\n\nQ. What should staff do by May 28?", ["Wear new uniforms", "Collect new name tags", "Visit the front desk", "Attend a training"], 1, "pick them up(name tags) by May 28 = 새 이름표를 받아 가기."),
         ("Part 7 · 공지", "(위 공지)\n\nQ. Where is Human Resources?", ["On the 1st floor", "On the 2nd floor", "At the front desk", "In the basement"], 1, "Human Resources on the 2nd floor."),
         ("Part 7 · 문자 대화", "Ken (9:02): The bus for the airport is full.\nAmy (9:03): Can we book a taxi for the Lee family?\nKen (9:05): I already did.\n\nQ. What does Ken mean when he writes, \"I already did\"?", ["He booked a taxi.", "He took the bus.", "He called the Lee family.", "He checked out."], 0, "Amy의 제안(taxi를 예약하자)에 이미 했다고 답한 것입니다.")],
  "qa": [("부정 의문문 \"Haven't you met him?\" — 아직 못 만났다면?", "No, not yet."), ("현재완료와 함께 쓰는 '~ 이후로'는?", "since"), ("\"I already did\" 같은 의도 파악 문제는 어떻게 푸나요?", "바로 앞 메시지와 연결해 읽는다"), ("관사와 명사 사이 빈칸의 품사는?", "형용사")],
  "rel": ["7-01-01", "7-01-02", "7-02-01", "7-02-02"]})]}]

# ---------- one bundle per Part: LC 4 (Part 1–4) + RC 3 (Part 5–7) (RYU 2026-11-23: "lc 4개 rc 3개") ----------
# The two-part bundles above are cut by Part; each new bundle draws 10 questions at random from the bank (content/tqbank.py).
def _by_part(b1, b2, spec):
    old = {x["t"]: x for x in (b1, b2)}
    out = []
    for s in spec:
        src = old[s["from"]]
        nb = dict(T, **{"t": s["t"], "en": s["en"], "i": s["i"], "tqpart": s["part"]})
        nb["tp"] = [src["tp"][i] for i in s.get("tp", [])] + s.get("tp+", [])
        nb["sm"] = [src["sm"][i] for i in s.get("sm", [])] + s.get("sm+", [])
        nb["w"] = [w for w in src["w"] if w[0] in s["w"]] + s.get("w+", [])
        nb["dr"] = [d for d in src["dr"] if d[0] in s.get("dr", [])] + s.get("dr+", [])
        nb["qa"] = [src["qa"][i] for i in s.get("qa", [])] + s.get("qa+", [])
        nb["tq"] = [q for q in src["tq"] if q[0].startswith(s["part"] + " ")]
        nb["rel"] = s["rel"]
        out.append(nb)
    return out

_LC1, _LC2 = SUBS[0]["b"]
_RC1, _RC2 = SUBS[1]["b"]
SUBS[0]["b"] = _by_part(_LC1, _LC2, [
 {"from": _LC1["t"], "part": "Part 1", "t": "Part 1 사진 묘사", "en": "TOEIC LC Part 1",
  "i": "Part 1(사진 묘사): 그림을 보고 네 문장 중 그림을 바르게 설명한 것을 고릅니다. 호텔·여행 장면으로 연습합니다.",
  "tp": [0, 2], "tp+": ["정답이 아닌 보기는 사진에 없는 사물이나, 맞는 사물에 틀린 동작을 붙인 경우가 많습니다."],
  "sm": [0], "sm+": ["사람 사진 → 주어 + is/are ~ing (She's handing ~ / They're walking ~). 사물 사진 → ~ is placed / has been ~ed / There are ~."],
  "w": ["is being ~ed", "has been ~ed", "set up", "pick up"], "dr": ["~ is being ...ed.", "~ has been ...ed."],
  "qa": [1], "qa+": [("사람이 있는 Part 1 사진에서 자주 정답인 형태는?", "주어 + is/are + ~ing (동작)"), ("\"Tables have been set.\"의 뜻은?", "테이블이 차려져 있다.")],
  "rel": ["7-01-02", "3-02-01", "1-04-02"]},
 {"from": _LC1["t"], "part": "Part 2", "t": "Part 2 질의응답", "en": "TOEIC LC Part 2",
  "i": "Part 2(질의응답): 질문 하나와 세 개의 응답을 듣고 가장 알맞은 응답을 고릅니다. 시험지에는 아무것도 쓰여 있지 않습니다.",
  "tp": [1, 2], "tp+": ["의문사가 없는 질문(Do/Is/Can ~?)과 부탁·제안, 평서문(문제 제기)에 대한 응답도 자주 나옵니다."],
  "sm": [1], "w": ["in charge of", "delayed", "Why don't we ~?", "sign up", "available", "I'm not sure"], "dr": ["Let me ~."],
  "qa": [0, 2, 3], "rel": ["7-01-01", "7-01-03", "1-04-02"]},
 {"from": _LC2["t"], "part": "Part 3", "t": "Part 3 짧은 대화", "en": "TOEIC LC Part 3",
  "i": "Part 3(짧은 대화): 두세 사람의 대화를 듣고 장소, 문제, 다음 행동을 묻는 질문에 답합니다. 질문을 먼저 읽고 듣는 습관을 익힙니다.",
  "tp": [0, 1, 2], "sm": [0, 1], "w": ["most likely", "arrange", "technician", "return a call"],
  "dr+": [("What is the problem?", "문제가 무엇인가요? (Part 3 질문)", [("What is the man's problem?", "남자의 문제는 무엇인가요?"), ("What is the woman worried about?", "여자는 무엇을 걱정하나요?"), ("Why is the man calling?", "남자는 왜 전화하나요?")]),
          ("What will ~ probably do next?", "~은 다음에 무엇을 할 것 같나요?", [("What will the woman probably do next?", "여자는 다음에 무엇을 할 것 같나요?"), ("What does the man offer to do?", "남자는 무엇을 해 주겠다고 하나요?"), ("What does the woman suggest?", "여자는 무엇을 제안하나요?")])],
  "qa": [0, 1, 2], "rel": ["7-01-04", "7-01-02", "3-04-02"]},
 {"from": _LC2["t"], "part": "Part 4", "t": "Part 4 짧은 담화", "en": "TOEIC LC Part 4",
  "i": "Part 4(짧은 담화): 한 사람이 말하는 안내 방송, 전화 메시지, 투어 안내를 듣고 목적, 세부 정보, 요청 사항을 묻는 질문에 답합니다.",
  "tp": [0], "tp+": ["담화 종류를 먼저 파악하세요: 안내 방송(Attention, guests ~), 전화 메시지(Hi, this is ~. I'm calling about ~), 투어 안내(Welcome to ~)", "목적은 첫 두 문장에, 요청 사항(Please ~)은 마지막 부분에 자주 나옵니다."],
  "sm": [1], "sm+": ["Part 4 빈출 질문: What is the purpose of the message? / Who most likely is the speaker? / What are listeners asked to do?"],
  "w": ["purpose", "announcement", "renovation", "temporary", "reminder", "inconvenience"],
  "dr": ["I'm calling about ~.", "Please call me back at ~.", "We apologize for ~."],
  "qa": [3], "qa+": [("Part 4에서 '목적' 질문의 답은 주로 어디에 나오나요?", "처음 한두 문장"), ("\"What are listeners asked to do?\"의 뜻은?", "듣는 사람들은 무엇을 하라고 요청받나요?")],
  "rel": ["7-01-03", "7-03-01", "3-04-02"]}])
SUBS[1]["b"] = _by_part(_RC1, _RC2, [
 {"from": _RC1["t"], "part": "Part 5", "t": "Part 5 단문 빈칸", "en": "TOEIC RC Part 5",
  "i": "Part 5(단문 빈칸): 한 문장의 빈칸에 알맞은 단어를 고릅니다. 품사 자리, 시제, 수동태, 전치사·접속사를 호텔 문장으로 정리합니다.",
  "tp": [0, 1], "tp+": ["어휘 문제는 빈칸 뒤 단어와 짝(be equipped with, be responsible for)을 기억해 두면 빨리 풉니다."],
  "sm": [0, 1], "w": ["equipped with", "although", "despite", "procedure", "respond", "positive"], "dr": ["be equipped with ~", "Although ~, ..."],
  "qa": [0, 1, 3], "rel": ["7-02-02", "7-03-01", "1-04-01"]},
 {"from": _RC1["t"], "part": "Part 6", "t": "Part 6 장문 빈칸", "en": "TOEIC RC Part 6",
  "i": "Part 6(장문 빈칸): 이메일·공지 같은 짧은 글의 빈칸에 알맞은 말을 고릅니다. 앞뒤 문장의 흐름을 읽는 연습을 합니다.",
  "tp": [2], "tp+": ["빈칸 앞 문장과 뒤 문장의 관계를 보세요: 더하기(In addition), 반대(However), 결과(Therefore), 예시(For example), 대신(Instead).", "대명사(it, them, they)가 가리키는 말과 시제(이미 끝난 일인지)도 앞뒤 문장에서 확인합니다."],
  "sm+": ["접속부사: However(그러나) / Therefore·As a result(그래서) / In addition·Moreover(게다가) / For example(예를 들어) / Instead(대신) / Otherwise(그렇지 않으면)"],
  "w": ["however", "in addition", "therefore", "instead"], "dr": ["In addition, ~"],
  "dr+": [("However, ~.", "그러나 ~. (앞 문장과 반대)", [("The gym is free. However, classes cost extra.", "헬스장은 무료입니다. 그러나 수업은 추가 요금이 있습니다."), ("The pool is open. However, the sauna is closed.", "수영장은 엽니다. 그러나 사우나는 닫습니다."), ("Breakfast is included. However, room service is not.", "조식은 포함입니다. 그러나 룸서비스는 아닙니다.")])],
  "qa": [2], "qa+": [("'그렇지 않으면'을 뜻하는 접속부사는?", "Otherwise"), ("앞 문장이 원인, 뒤 문장이 결과일 때 쓰는 말은?", "Therefore / As a result")],
  "rel": ["7-02-01", "7-02-03", "1-04-01"]}])
SUBS[1]["b"].append(_RC2)
_RC2["t"], _RC2["en"], _RC2["tqpart"], _RC2["rel"] = "Part 7 독해", "TOEIC RC Part 7", "Part 7", ["7-02-02", "7-03-01", "6-02-01"]
SUBS[2]["b"][0]["rel"] = ["7-01-01", "7-01-03", "7-02-01", "7-02-03"]
SUBS[2]["b"][0]["tqpart"] = "all"

# ── 빈출 단어·문장 (RYU 2026-11-23): words and phrases taken out of the Part bundles into their own sub,
#    grouped by theme, placed before 모의고사. Part bundles keep strategy (sm), questions (tq) and quiz (qa).
_PW = {}; _PD = {}
for _s in SUBS[:2]:
    for _b in _s["b"]:
        for _w in _b.pop("w", []): _PW[_w[0]] = _w
        for _d in _b.pop("dr", []): _PD[_d[0]] = _d
        _b["ord"] = ["sm", "tq", "qa"]
VT = {"wl": ["질문", "응답"], "ww": ["A", "B"], "ord": ["w", "dr", "qa"], "wt": "빈출 단어와 문장", "drt": "자주 나오는 표현"}
_NEW = {
 "lean against": W("lean against", "~에 기대다", "중", ("Is the bicycle leaning against the wall?", "자전거가 벽에 기대어 있나요?", "Yes, next to the entrance.", "네, 입구 옆에요."), ("A man is leaning against the counter.", "한 남자가 카운터에 기대어 있어요.", "He's waiting for a taxi.", "택시를 기다리고 있어요.")),
 "stack": W("stack", "쌓다, 더미", "중", ("Where are the chairs?", "의자는 어디 있나요?", "They're stacked in the corner.", "구석에 쌓여 있어요."), ("Plates are stacked on the shelf.", "접시가 선반에 쌓여 있어요.", "I'll take some.", "몇 개 가져갈게요.")),
 "hang": W("hang", "걸다, 걸려 있다", "중", ("Where should I hang my coat?", "코트는 어디에 걸까요?", "On the hook by the door.", "문 옆 고리에요."), ("A painting is hanging on the wall.", "그림이 벽에 걸려 있어요.", "It's beautiful.", "아름답네요.")),
 "line up": W("line up", "줄을 서다", "중", ("Why are people lining up?", "사람들이 왜 줄을 서 있나요?", "They're waiting for the shuttle.", "셔틀을 기다리고 있어요."), ("Guests are lining up at the buffet.", "손님들이 뷔페에 줄을 서 있어요.", "Let's add more plates.", "접시를 더 놓읍시다.")),
 "attention": W("attention", "주목, 주의", "중", ("Attention, please. The pool will close at nine.", "안내 말씀드립니다. 수영장은 9시에 문을 닫습니다.", "Thanks for letting us know.", "알려 줘서 고마워요."), ("May I have your attention?", "잠시 주목해 주시겠어요?", "Sure, go ahead.", "네, 말씀하세요.")),
 "postpone": W("postpone", "연기하다", "상", ("Why was the tour postponed?", "투어가 왜 연기됐나요?", "Because of the heavy rain.", "폭우 때문에요."), ("The meeting is postponed until Friday.", "회의가 금요일로 연기됐어요.", "I'll update my schedule.", "일정을 고칠게요.")),
 "register": W("register", "등록하다", "중", ("Where do I register for the conference?", "회의 등록은 어디서 하나요?", "At the desk in the lobby.", "로비 데스크에서요."), ("Please register by Friday.", "금요일까지 등록해 주세요.", "I'll do it today.", "오늘 할게요.")),
 "shuttle": W("shuttle", "셔틀(버스)", "중", ("How often does the shuttle run?", "셔틀은 얼마나 자주 다니나요?", "Every thirty minutes.", "30분마다요."), ("The airport shuttle leaves from the main entrance.", "공항 셔틀은 정문에서 출발합니다.", "Thank you.", "고마워요.")),
}
_PW.update(_NEW)
def _vb(t, en, i, tp, ws, ds, qa, rel):
    return dict(VT, **{"t": t, "en": en, "i": i, "tp": tp, "w": [_PW[x] for x in ws], "dr": [_PD[x] for x in ds if x in _PD] + [x for x in ds if not isinstance(x, str)], "qa": qa, "rel": rel})
_VOCAB = {"n": "빈출 단어·문장", "b": [
 _vb("듣기 빈출 ① 사진·동작", "TOEIC Words: Pictures & Actions", "Part 1 사진 문제에 자주 나오는 동작·상태 표현을 모았습니다.",
     ["사람 사진은 is/are ~ing(동작), 사물 사진은 is placed / has been ~ed / is being ~ed(상태)로 묘사합니다.", "관련 문제: 7-01-01 Part 1 사진 묘사"],
     ["is being ~ed", "has been ~ed", "set up", "pick up", "lean against", "stack", "hang", "line up"],
     ["~ is being ...ed.", "~ has been ...ed."],
     [("\"Chairs are stacked in the corner.\"의 뜻은?", "의자가 구석에 쌓여 있다."), ("\"lean against\"의 뜻은?", "~에 기대다"), ("\"line up\"의 뜻은?", "줄을 서다"), ("\"A painting is hanging on the wall.\"의 뜻은?", "그림이 벽에 걸려 있다.")],
     ["7-01-01", "7-03-02"]),
 _vb("듣기 빈출 ② 질문·대화", "TOEIC Words: Questions & Conversations", "Part 2·3 질문과 대화에 자주 나오는 표현을 모았습니다.",
     ["Part 2는 질문의 첫 단어(Who/When/Where/Why don't we ~?)를 꼭 들으세요.", "관련 문제: 7-01-02 Part 2, 7-01-03 Part 3"],
     ["in charge of", "delayed", "Why don't we ~?", "sign up", "available", "I'm not sure", "most likely", "arrange", "technician", "return a call"],
     ["Let me ~.", "What is the problem?", "What will ~ probably do next?"],
     [("\"Who's in charge of the event?\"의 뜻은?", "행사 담당자가 누구인가요?"), ("\"most likely\"의 뜻은?", "아마, ~일 가능성이 가장 높은"), ("\"return a call\"의 뜻은?", "회신 전화를 하다"), ("\"Why don't we ~?\"는 무엇을 하는 말인가요?", "제안 (~하는 게 어때요?)")],
     ["7-01-02", "7-01-03", "7-03-01"]),
 _vb("듣기 빈출 ③ 안내·방송", "TOEIC Words: Announcements", "Part 4 안내 방송과 전화 메시지에 자주 나오는 표현을 모았습니다.",
     ["안내 방송은 Attention, please. 로 시작하고, 목적은 첫 두 문장, 요청은 마지막 Please ~ 에 나옵니다.", "관련 문제: 7-01-04 Part 4 짧은 담화"],
     ["attention", "purpose", "announcement", "renovation", "temporary", "reminder", "inconvenience", "postpone", "register", "shuttle"],
     ["I'm calling about ~.", "Please call me back at ~.", "We apologize for ~."],
     [("\"We apologize for the inconvenience.\"의 뜻은?", "불편을 드려 죄송합니다."), ("\"postpone\"의 뜻은?", "연기하다"), ("\"temporary\"의 뜻은?", "임시의"), ("\"What is the purpose of the announcement?\"의 뜻은?", "안내 방송의 목적은 무엇인가요?")],
     ["7-01-04", "7-03-02"]),
 _vb("읽기 빈출 ① 문법·연결어", "TOEIC Words: Grammar & Linking Words", "Part 5·6에 자주 나오는 짝 표현과 연결어(접속사·접속부사)를 모았습니다.",
     ["although + 문장, despite + 명사. However·Therefore·In addition은 문장 앞에서 앞뒤 흐름을 이어 줍니다.", "관련 문제: 7-02-01 Part 5, 7-02-02 Part 6"],
     ["equipped with", "although", "despite", "however", "in addition", "therefore", "instead", "procedure", "respond", "positive"],
     ["be equipped with ~", "Although ~, ...", "In addition, ~", "However, ~."],
     [("although와 despite의 차이는?", "although + 문장, despite + 명사"), ("\"그러므로\"를 뜻하는 접속부사는?", "Therefore"), ("\"The room is equipped with a minibar.\"의 뜻은?", "객실에 미니바가 갖춰져 있다."), ("\"instead\"의 뜻은?", "대신에")],
     ["7-02-01", "7-02-02", "7-03-04"]),
 _vb("읽기 빈출 ② 이메일·문서", "TOEIC Words: E-mails & Documents", "Part 7 이메일, 공지, 쿠폰, 일정표에 자주 나오는 단어를 모았습니다.",
     ["지문을 읽기 전에 질문의 핵심 단어(valid, expire, complimentary 등)를 먼저 보고 지문에서 찾으세요.", "관련 문제: 7-02-03 Part 7 독해"],
     ["confirmation", "complimentary", "itinerary", "maintenance", "valid", "expire", "voucher", "location", "suggest", "mention"],
     [x for x in _PD if x not in ("~ is being ...ed.", "~ has been ...ed.", "Let me ~.", "What is the problem?", "What will ~ probably do next?", "I'm calling about ~.", "Please call me back at ~.", "We apologize for ~.", "be equipped with ~", "Although ~, ...", "In addition, ~", "However, ~.")],
     [("\"complimentary\"의 뜻은?", "무료의"), ("\"The voucher is valid until May 31.\"의 뜻은?", "쿠폰은 5월 31일까지 유효하다."), ("\"itinerary\"의 뜻은?", "여행 일정표"), ("\"expire\"의 뜻은?", "만료되다")],
     ["7-02-03", "7-03-04"]),
]}
_WORDS = {"n": "빈출 단어", "b": []}
for _b in _VOCAB["b"]:
    _b["t"] = _b["t"].replace("빈출", "단어"); _b["dr"] = []; _b["ord"] = ["w", "qa"]
    _WORDS["b"].append(_b)
_VOCAB = _WORDS
def _eb(t, en, i, tp, ds, qa, rel):
    return dict(VT, **{"t": t, "en": en, "i": i, "tp": tp, "ord": ["dr", "qa"], "dr": [_PD[x] for x in ds], "qa": qa, "rel": rel})
_EXPR = {"n": "자주 나오는 표현", "b": [
 _eb("듣기 표현 ① 사진·응답", "TOEIC Patterns: Pictures & Responses", "Part 1·2에 자주 나오는 문장 틀을 모았습니다.",
     ["is being ~ed = 지금 ~되는 중(사람이 하고 있음), has been ~ed = 이미 ~되어 있음(상태).", "관련 문제: 7-01-01 Part 1, 7-01-02 Part 2"],
     ["~ is being ...ed.", "~ has been ...ed.", "Let me ~."],
     [("\"The table is being cleaned.\"과 \"The table has been cleaned.\"의 차이는?", "지금 닦는 중 / 이미 닦여 있음"), ("\"Let me check.\"의 뜻은?", "확인해 볼게요.")],
     ["7-01-01", "7-03-01"]),
 _eb("듣기 표현 ② 대화·안내 질문", "TOEIC Patterns: Conversations & Talks", "Part 3·4의 질문 문장과 전화 메시지·안내 방송의 문장 틀을 모았습니다.",
     ["질문을 먼저 읽어 두면 무엇을 들어야 할지 알 수 있습니다.", "관련 문제: 7-01-03 Part 3, 7-01-04 Part 4"],
     ["What is the problem?", "What will ~ probably do next?", "I'm calling about ~.", "Please call me back at ~.", "We apologize for ~."],
     [("\"What will the woman probably do next?\"의 뜻은?", "여자는 다음에 무엇을 할 것 같나요?"), ("\"I'm calling about ~.\"는 담화의 무엇을 알려 주나요?", "전화한 목적"), ("\"We apologize for the delay.\"의 뜻은?", "지연되어 죄송합니다.")],
     ["7-01-03", "7-01-04", "7-03-03"]),
 _eb("읽기 표현 ① 문법·연결", "TOEIC Patterns: Grammar & Linking", "Part 5·6에 자주 나오는 짝 표현과 연결어 문장 틀을 모았습니다.",
     ["빈칸 앞뒤 문장의 관계(더하기, 반대)를 보고 In addition / However를 고릅니다.", "관련 문제: 7-02-01 Part 5, 7-02-02 Part 6"],
     ["be equipped with ~", "Although ~, ...", "In addition, ~", "However, ~."],
     [("\"Although\" 뒤에는 무엇이 오나요?", "주어 + 동사 (문장)"), ("앞 문장에 더할 때 쓰는 연결어는?", "In addition"), ("앞 문장과 반대일 때 쓰는 연결어는?", "However")],
     ["7-02-01", "7-02-02", "7-03-04"]),
 _eb("읽기 표현 ② 이메일·문서", "TOEIC Patterns: E-mails & Documents", "Part 7 이메일, 공지, 쿠폰에 자주 나오는 문장 틀을 모았습니다.",
     ["질문의 핵심 단어를 먼저 보고 지문에서 같은 문장 틀을 찾으세요.", "관련 문제: 7-02-03 Part 7 독해"],
     [x for x in _PD if x not in ("~ is being ...ed.", "~ has been ...ed.", "Let me ~.", "What is the problem?", "What will ~ probably do next?", "I'm calling about ~.", "Please call me back at ~.", "We apologize for ~.", "be equipped with ~", "Although ~, ...", "In addition, ~", "However, ~.")],
     [("Part 7에서 질문을 먼저 읽는 이유는?", "지문에서 찾을 정보를 미리 알기 위해"), ("\"complimentary\"가 문서에 나오면 무슨 뜻인가요?", "무료의")],
     ["7-02-03", "7-03-05"]),
]}
_left = set(_PW) - {w[0] for b in _VOCAB["b"] for w in b["w"]}
assert not _left, _left
SUBS[2:2] = [_VOCAB, _EXPR]
for _s in SUBS:
    for _b in _s["b"]:
        _b["rel"] = [r if r != "7-03-01" else "7-05-01" for r in _b.get("rel", [])]
SUBS[4]["b"][0]["sm"] = [x.replace("복습 순서: 틀린 Part의 묶음(7-01-01 Part 1·2, 7-01-02 Part 3·4, 7-02-01 Part 5·6, 7-02-02 Part 7)을 다시 보세요.", "복습 순서: 틀린 Part의 묶음(LC 7-01-01~04, RC 7-02-01~03)과 빈출 단어(7-03), 자주 나오는 표현(7-04)을 다시 보세요.") for x in SUBS[4]["b"][0]["sm"]]
# rel links between Part bundles (7-01/02), 빈출 단어 (7-03) and 자주 나오는 표현 (7-04)
_R = {"7-01-01": ["7-03-01", "7-04-01"], "7-01-02": ["7-03-02", "7-04-01"], "7-01-03": ["7-03-02", "7-04-02"], "7-01-04": ["7-03-03", "7-04-02"],
      "7-02-01": ["7-03-04", "7-04-03"], "7-02-02": ["7-03-04", "7-04-03"], "7-02-03": ["7-03-05", "7-04-04"]}
for _si, _s in enumerate(SUBS[:2], 1):
    for _bi, _b in enumerate(_s["b"], 1): _b["rel"] = _R["7-%02d-%02d" % (_si, _bi)] + _b["rel"][:2]
for _b, _r in zip(SUBS[2]["b"], [["7-04-01", "7-01-01"], ["7-04-01", "7-01-02", "7-01-03"], ["7-04-02", "7-01-04"], ["7-04-03", "7-02-01", "7-02-02"], ["7-04-04", "7-02-03"]]): _b["rel"] = _r
for _b, _r in zip(SUBS[3]["b"], [["7-03-01", "7-01-01", "7-01-02"], ["7-03-02", "7-03-03", "7-01-03", "7-01-04"], ["7-03-04", "7-02-01", "7-02-02"], ["7-03-05", "7-02-03"]]): _b["rel"] = _r
# 확인 문제 (qa) follow 빈출 단어 (RYU 2026-11-23): Part bundles' qa move into the matching word bundle; 표현 bundles have none
_QM = {"7-01-01": 0, "7-01-02": 1, "7-01-03": 1, "7-01-04": 2, "7-02-01": 3, "7-02-02": 3, "7-02-03": 4}
for _si, _s in enumerate(SUBS[:2], 1):
    for _bi, _b in enumerate(_s["b"], 1):
        _wb = SUBS[2]["b"][_QM["7-%02d-%02d" % (_si, _bi)]]
        _wb["qa"] = _wb["qa"] + [q for q in _b.pop("qa", []) if q not in _wb["qa"]]
        _b["ord"] = ["sm", "tq"]
for _b in SUBS[3]["b"]: _b["qa"] = []; _b["ord"] = ["dr"]
# 중복 정리 (RYU 2026-11-24): sentence patterns stay only in 자주 나오는 표현; 빈출 단어 gets plain words instead
_DUPW = {"is being ~ed", "has been ~ed", "equipped with", "although", "however", "in addition"}
_ADDW = [
 [W("load", "싣다", "중", ("Are the bags being loaded?", "가방을 싣고 있나요?", "Yes, onto the shuttle.", "네, 셔틀에요."), ("A man is loading boxes into a truck.", "한 남자가 트럭에 상자를 싣고 있어요.", "It's the new furniture.", "새 가구예요.")),
  W("board", "탑승하다, 타다", "중", ("When can we board the bus?", "버스는 언제 탈 수 있나요?", "In ten minutes.", "10분 후에요."), ("Passengers are boarding the plane.", "승객들이 비행기에 탑승하고 있어요.", "We're next.", "다음은 우리예요."))],
 [W("due to", "~ 때문에", "상", ("Why was the flight canceled?", "비행기가 왜 취소됐나요?", "Due to bad weather.", "날씨가 나빠서요."), ("The pool is closed due to repairs.", "수리 때문에 수영장이 닫혀 있어요.", "When will it open?", "언제 열어요?")),
  W("unless", "~하지 않으면", "상", ("Can I check out late?", "늦게 체크아웃해도 되나요?", "Unless the room is booked, yes.", "방이 예약되어 있지 않으면 됩니다."), ("Unless you call, we'll keep the room.", "전화 주시지 않으면 방을 그대로 두겠습니다.", "Thank you.", "고마워요.")),
  W("as a result", "그 결과", "상", ("Did the new menu help?", "새 메뉴가 도움이 됐나요?", "Yes. As a result, sales went up.", "네. 그 결과 매출이 올랐어요."), ("It snowed a lot. As a result, the tour was canceled.", "눈이 많이 왔어요. 그 결과 투어가 취소됐어요.", "That's too bad.", "안타깝네요.")),
  W("otherwise", "그렇지 않으면", "상", ("Should I book now?", "지금 예약해야 하나요?", "Yes. Otherwise, it may be full.", "네. 그렇지 않으면 꽉 찰 수도 있어요."), ("Please arrive by six. Otherwise, we'll cancel the table.", "6시까지 와 주세요. 그렇지 않으면 자리를 취소합니다.", "Okay, we'll be on time.", "네, 제시간에 갈게요."))],
]
SUBS[2]["b"][0]["w"] = [w for w in SUBS[2]["b"][0]["w"] if w[0] not in _DUPW] + _ADDW[0]
SUBS[2]["b"][3]["w"] = [w for w in SUBS[2]["b"][3]["w"] if w[0] not in _DUPW] + _ADDW[1]
SUBS[2]["b"][3]["qa"] = [q if "equipped" not in q[0] else ("\"due to\" 뒤에는 무엇이 오나요?", "명사 (due to bad weather)") for q in SUBS[2]["b"][3]["qa"]]
SUBS[2]["b"][0]["qa"] = [q for q in SUBS[2]["b"][0]["qa"]] + [("\"Passengers are boarding the plane.\"의 뜻은?", "승객들이 비행기에 탑승하고 있다.")]
# 표현 ② 이메일·문서: patterns that repeated the words valid / available → other Part 7 patterns
SUBS[3]["b"][3]["dr"] = [d for d in SUBS[3]["b"][3]["dr"] if d[0] not in ("~ is valid until ...", "~ is available at ...")] + [
 ("Please note that ~.", "~에 유의해 주세요. (공지·이메일)", [("Please note that the pool closes at 9 p.m.", "수영장은 오후 9시에 닫는다는 점에 유의해 주세요."), ("Please note that parking is limited.", "주차 공간이 한정되어 있다는 점에 유의해 주세요."), ("Please note that check-out is at 11 a.m.", "체크아웃은 오전 11시라는 점에 유의해 주세요.")]),
 ("We are pleased to ~.", "~하게 되어 기쁩니다. (안내·초대 이메일)", [("We are pleased to confirm your reservation.", "예약을 확정하게 되어 기쁩니다."), ("We are pleased to announce our new spa.", "새 스파를 알려 드리게 되어 기쁩니다."), ("We are pleased to offer you a free upgrade.", "무료 업그레이드를 제공해 드리게 되어 기쁩니다.")])]
for _b in SUBS[2]["b"]:
    _seen = set(); _b["qa"] = [q for q in _b["qa"] if not (q[0] in _seen or _seen.add(q[0]))]

# 미니 모의고사 25문제 (RYU 2026-11-24: 14문제는 너무 적다, 25문제쯤): real TOEIC 200 questions scaled to 1/8, drawn from the bank
_mini = SUBS[4]["b"][0]
_mini.update({"tqk": {"Part 1": 1, "Part 2": 3, "Part 3": 5, "Part 4": 4, "Part 5": 4, "Part 6": 2, "Part 7": 6}, "tqt": "미니 모의고사 (25문제)",
  "i": "실제 토익(200문제)의 Part별 비율을 1/8로 줄인 25문제 모의고사입니다. 듣기 13문제(Part 1 1, Part 2 3, Part 3 5, Part 4 4), 읽기 12문제(Part 5 4, Part 6 2, Part 7 6). 시험처럼 시간을 재고 풀어 보세요. (권장 시간 20분)",
  "tp": ["듣기(1–13번)는 '듣기 문제 영어 보기'를 끈 상태에서 🔊로 한 번만 듣고 푸세요.", "읽기(14–25번)는 한 문제에 1분 이내를 목표로 합니다.", "🔀 다른 문제를 누르면 문제은행에서 새 25문제가 나옵니다. 틀린 문제는 해설을 읽고 관련 묶음으로 돌아가 복습하세요."],
  "sm": ["점수 보기: 23–25개 매우 좋음 / 18–22개 좋음 / 13–17개 기본기 복습 필요 / 12개 이하 Part 묶음과 빈출 단어부터 다시", _mini["sm"][1]]})
# 실전 모의고사 50문제 (RYU 2026-11-24 chose "+ 50문제 실전형"): real TOEIC scaled to 1/4
_m50 = dict(_mini, **{"t": "실전 모의고사 50문제", "en": "TOEIC Practice Test (50)",
  "i": "실제 토익(200문제)의 Part별 비율을 1/4로 줄인 50문제 모의고사입니다. 듣기 25문제(Part 1 2, Part 2 6, Part 3 9, Part 4 8), 읽기 25문제(Part 5 8, Part 6 4, Part 7 13). 권장 시간 약 35분.",
  "tp": ["듣기는 '듣기 문제 영어 보기'를 끈 상태에서 🔊로 한 번만 듣고 푸세요.", "읽기는 Part 5·6을 10분 안에 끝내고 Part 7에 시간을 쓰세요.", "🔀 다른 문제를 누르면 문제은행에서 새 50문제가 나옵니다."],
  "tqt": "실전 모의고사 (50문제)", "tqk": {"Part 1": 2, "Part 2": 6, "Part 3": 9, "Part 4": 8, "Part 5": 8, "Part 6": 4, "Part 7": 13},
  "sm": ["점수 보기: 45–50개 매우 좋음 / 38–44개 좋음 / 30–37개 기본기 복습 필요 / 29개 이하 Part 묶음과 빈출 단어부터 다시", _mini["sm"][1]],
  "rel": ["7-05-01", "7-01-03", "7-02-03"]})
SUBS[4]["b"].append(_m50)
_mini["rel"] = ["7-05-02"] + _mini["rel"][:3]
