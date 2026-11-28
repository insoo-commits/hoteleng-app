# TOEIC question bank for the TOEIC menu (RYU 2026-11-23: TOEIC 메뉴만 10배, drawn at random).
# Same tuple as content: (part, question, [choices], answer index, explanation[, script]).
# build.py adds BANK[title] to the TOEIC bundle with that title; 미니 모의고사 draws from all of them by part.
P5 = "Part 5 · 단문 빈칸"
P6 = "Part 6 · 장문 빈칸"

B56 = [
 (P5, "All guests are asked to ------- their room keys at the front desk.", ["return", "returning", "returned", "returns"], 0, "be asked to + 동사원형이므로 return입니다."),
 (P5, "The restaurant on the top floor is ------- for its ocean view.", ["known", "knowing", "know", "knows"], 0, "be known for = ~로 알려져 있다."),
 (P5, "Breakfast is served ------- 6:30 and 10:00 a.m.", ["from", "between", "during", "within"], 1, "between A and B = A와 B 사이에."),
 (P5, "Ms. Lee will ------- the conference room for the sales meeting.", ["reserve", "reservation", "reserved", "reserving"], 0, "조동사 will 뒤에는 동사원형입니다."),
 (P5, "Please contact the concierge if you need ------- with your luggage.", ["assist", "assistance", "assistant", "assisted"], 1, "need의 목적어 자리이므로 명사 assistance(도움)입니다."),
 (P5, "The hotel shuttle leaves ------- 30 minutes from the main entrance.", ["every", "each", "all", "some"], 0, "every + 숫자 + 복수명사 = ~마다."),
 (P5, "Guests ------- stay more than five nights receive a free dinner.", ["who", "which", "whose", "whom"], 0, "사람 선행사(Guests)를 꾸미는 주격 관계대명사 who."),
 (P5, "The spa is closed today ------- the annual maintenance.", ["because of", "because", "although", "so that"], 0, "뒤에 명사구가 오므로 전치사 because of입니다."),
 (P5, "Mr. Kim has worked at the hotel ------- 2015.", ["since", "for", "from", "until"], 0, "현재완료 + since + 과거 시점."),
 (P5, "The new lobby design is much ------- than the old one.", ["brighter", "bright", "brightest", "brightly"], 0, "than이 있으므로 비교급 brighter."),
 (P5, "Room service is available ------- the night.", ["throughout", "among", "beside", "onto"], 0, "throughout the night = 밤새 내내."),
 (P5, "Please ------- the form and give it to the receptionist.", ["complete", "completion", "completely", "completed"], 0, "Please 뒤 명령문은 동사원형."),
 (P5, "The manager asked the staff to be ------- with every guest.", ["polite", "politely", "politeness", "politest"], 0, "be동사 뒤 보어 자리이므로 형용사 polite."),
 (P5, "The hotel offers a 10% discount ------- groups of ten or more.", ["to", "of", "at", "by"], 0, "offer A to B = B에게 A를 제공하다."),
 (P5, "Our chef ------- fresh ingredients from local farms every morning.", ["buys", "buy", "buying", "to buy"], 0, "주어가 3인칭 단수이고 습관이므로 buys."),
 (P5, "If the room is not clean, we ------- it immediately.", ["will clean", "cleaned", "had cleaned", "cleaning"], 0, "조건절 현재시제 + 주절 will + 동사원형."),
 (P5, "The banquet hall can ------- up to 300 people.", ["accommodate", "accommodation", "accommodating", "accommodated"], 0, "can 뒤 동사원형. accommodate = 수용하다."),
 (P5, "------- the heavy rain, the outdoor wedding went ahead as planned.", ["Despite", "Although", "Because", "Unless"], 0, "뒤에 명사구(the heavy rain)이므로 전치사 Despite."),
 (P5, "Please let us know ------- you have any food allergies.", ["if", "what", "which", "who"], 0, "~인지/~라면을 나타내는 접속사 if."),
 (P5, "The checkout time has been ------- to 12 p.m.", ["extended", "extend", "extension", "extending"], 0, "has been + 과거분사 (수동태 완료)."),
 (P5, "The front desk staff speak English, Chinese, ------- Japanese.", ["and", "but", "or", "so"], 0, "A, B, and C로 나열합니다."),
 (P5, "This voucher is valid ------- the end of the month.", ["until", "by", "since", "during"], 0, "계속되다가 끝나는 시점 = until."),
 (P5, "The guest was ------- with the quick service.", ["satisfied", "satisfying", "satisfy", "satisfaction"], 0, "사람이 만족한 것이므로 과거분사 satisfied."),
 (P5, "The hotel's new website is very easy to -------.", ["use", "using", "used", "uses"], 0, "easy to + 동사원형."),
 (P5, "Ms. Park is responsible ------- training new employees.", ["for", "to", "with", "about"], 0, "be responsible for = ~을 책임지다."),
 (P5, "Neither the pool ------- the gym is open after 10 p.m.", ["nor", "or", "and", "but"], 0, "neither A nor B."),
 (P5, "The conference ------- next Monday at the Grand Ballroom.", ["will be held", "held", "was held", "has held"], 0, "next Monday(미래) + 행사는 열리는 것이므로 will be held."),
 (P5, "Please keep your valuables in the ------- safe in your room.", ["electronic", "electron", "electronically", "electricity"], 0, "명사 safe를 꾸미는 형용사 electronic."),
 (P5, "Our staff will be happy to help you ------- your stay.", ["during", "while", "when", "meanwhile"], 0, "뒤에 명사(your stay)이므로 전치사 during."),
 (P5, "The receptionist ------- the guest's passport and returned it.", ["checked", "check", "checking", "to check"], 0, "and returned(과거)와 시제를 맞춰 checked."),
 (P5, "This is the ------- hotel in the city.", ["oldest", "older", "old", "most old"], 0, "the + 최상급 oldest."),
 (P5, "We apologize ------- the inconvenience.", ["for", "to", "about", "with"], 0, "apologize for + 이유."),
 (P5, "The lounge will be closed ------- renovation until May 1.", ["for", "at", "by", "on"], 0, "closed for renovation = 보수 공사로 닫힌."),
 (P5, "Guests can ------- free Wi-Fi in all public areas.", ["access", "accessible", "accessibility", "accessing"], 0, "can + 동사원형 access(이용하다)."),
 (P5, "The tour guide spoke ------- so everyone could understand.", ["slowly", "slow", "slower", "slowness"], 0, "동사 spoke를 꾸미는 부사 slowly."),
 (P5, "Mr. Brown asked for a room ------- a view of the mountains.", ["with", "of", "for", "at"], 0, "a room with a view = 전망이 있는 방."),
 (P5, "------- you need anything else, please call extension 0.", ["Should", "Would", "Could", "Might"], 0, "If you should need의 도치 = Should you need."),
 (P5, "The housekeeping team cleans more than 200 rooms -------.", ["daily", "day", "days", "dairy"], 0, "동사구를 꾸미는 부사 daily(매일)."),
 (P5, "The hotel is ------- located near Jeonju Station.", ["conveniently", "convenient", "convenience", "conveniences"], 0, "과거분사 located를 꾸미는 부사 conveniently."),
 (P5, "Tickets for the city tour can be purchased ------- the concierge desk.", ["at", "in", "on", "to"], 0, "특정 지점(데스크)에서는 at."),
]
B56 += [
 (P5, "The hotel ------- a new fitness center last year.", ["opened", "opens", "will open", "has been opened"], 0, "last year(과거)이므로 opened."),
 (P5, "Guests are reminded that smoking is not ------- in the rooms.", ["permitted", "permit", "permission", "permitting"], 0, "be + 과거분사 수동태 permitted(허용된)."),
 (P5, "The sales team is preparing a ------- for the travel agency.", ["proposal", "propose", "proposed", "proposing"], 0, "관사 a 뒤 명사 자리 proposal(제안서)."),
 (P5, "Please arrive at least 15 minutes ------- your tour starts.", ["before", "ago", "early", "prior"], 0, "뒤에 절(your tour starts)이 오므로 접속사 before."),
 (P5, "The bellman carried the bags to the room -------.", ["himself", "him", "his", "he"], 0, "강조의 재귀대명사 himself(직접)."),
 (P5, "Ms. Choi is ------- qualified for the front office manager position.", ["highly", "high", "height", "higher"], 0, "형용사 qualified를 꾸미는 부사 highly."),
 (P5, "The minibar items will be ------- to your room bill.", ["charged", "charge", "charging", "charges"], 0, "will be + 과거분사 (청구되다)."),
 (P5, "We look forward to ------- you again soon.", ["welcoming", "welcome", "welcomed", "be welcomed"], 0, "look forward to + 동명사(-ing)."),
 (P5, "------- of the guests enjoyed the cooking class.", ["Most", "Almost", "Mostly", "The most"], 0, "Most of the + 복수명사 = 대부분의 ~."),
 (P5, "The airport limousine is ------- than a taxi.", ["cheaper", "cheap", "cheapest", "more cheap"], 0, "than이 있으므로 비교급 cheaper."),
 (P5, "The event coordinator will contact you ------- email.", ["by", "with", "on", "in"], 0, "연락 수단은 by email."),
 (P5, "All rooms ------- a coffee machine and a minibar.", ["include", "includes", "including", "to include"], 0, "주어가 복수(All rooms)이므로 include."),
 (P5, "The hotel received ------- reviews for its friendly staff.", ["positive", "positively", "positivity", "position"], 0, "명사 reviews를 꾸미는 형용사 positive."),
 (P5, "Due to the snow, many flights were -------.", ["delayed", "delaying", "delay", "delays"], 0, "were + 과거분사 수동태 (지연되었다)."),
 (P5, "The restaurant is ------- busy on Friday evenings.", ["especially", "special", "specialty", "specialize"], 0, "형용사 busy를 꾸미는 부사 especially."),
 (P5, "Ms. Yoon, ------- is our new spa manager, has ten years of experience.", ["who", "which", "what", "whose"], 0, "사람 선행사 + 콤마 뒤 주격 관계대명사 who."),
 (P5, "Please do not leave your bags ------- in the lobby.", ["unattended", "attend", "attending", "attendance"], 0, "leave + 목적어 + 형용사(unattended = 지켜보는 사람 없이)."),
 (P5, "The check-in process takes ------- five minutes.", ["about", "around of", "near", "almost of"], 0, "about + 숫자 = 약."),
 (P5, "Our hotel is ------- walking distance of the Hanok Village.", ["within", "inside", "between", "among"], 0, "within walking distance of ~ = ~에서 걸어갈 수 있는 거리."),
 (P5, "The chef recommends ------- the fish with white wine.", ["pairing", "pair", "to pair", "paired"], 0, "recommend + 동명사."),
 (P5, "Housekeeping will ------- fresh towels every day.", ["provide", "provision", "providing", "provided"], 0, "will + 동사원형."),
 (P5, "This room is not as large ------- the suite.", ["as", "than", "like", "so"], 0, "not as A as B."),
 (P5, "Please ------- us know your arrival time.", ["let", "make", "have", "allow"], 0, "let us know = 알려 주세요."),
 (P5, "The guest's complaint was handled ------- and politely.", ["quickly", "quick", "quickness", "quicker"], 0, "동사 handled를 꾸미는 부사 quickly."),
 (P5, "Free parking is available ------- hotel guests only.", ["for", "to", "with", "at"], 0, "available for + 대상."),
 (P5, "The museum is closed ------- Mondays.", ["on", "in", "at", "by"], 0, "요일 앞에는 on."),
 (P5, "The front desk is open 24 hours a day, seven days a -------.", ["week", "weekly", "weekend", "weeks"], 0, "seven days a week = 일주일 내내."),
 (P5, "Mr. Lopez was ------- to receive a room upgrade.", ["pleased", "pleasing", "pleasure", "please"], 0, "감정을 느낀 사람이므로 과거분사 pleased."),
 (P5, "The banquet menu must be confirmed ------- three days before the event.", ["at least", "at last", "at once", "at all"], 0, "at least = 적어도."),
 (P5, "------- guest receives a welcome drink at check-in.", ["Each", "All", "Both", "Many"], 0, "단수 명사 guest 앞에는 Each."),
 (P5, "The hotel will ------- a wine tasting event on Friday.", ["host", "hosting", "hosted", "hosts"], 0, "will + 동사원형 host(주최하다)."),
 (P5, "Our rooms are cleaned ------- by professional staff.", ["regularly", "regular", "regulate", "regulation"], 0, "수동태 동사를 꾸미는 부사 regularly."),
 (P5, "The conference room is ------- with a projector and a screen.", ["equipped", "equipment", "equip", "equipping"], 0, "be equipped with = ~을 갖추고 있다."),
 (P5, "Please call room service ------- you would like breakfast in your room.", ["if", "unless", "whether", "although"], 0, "조건 = if."),
 (P5, "The receptionist apologized for the ------- in the bill.", ["mistake", "mistaken", "mistakenly", "mistook"], 0, "관사 the 뒤 명사 mistake."),
 (P5, "The new menu will be introduced ------- next month.", ["starting", "started", "starts", "start"], 0, "starting + 시점 = ~부터."),
 (P5, "Guests must show a ------- ID when checking in.", ["valid", "validate", "validity", "validly"], 0, "명사 ID를 꾸미는 형용사 valid."),
 (P5, "The tour was canceled because not ------- people signed up.", ["enough", "many enough", "too", "very"], 0, "enough + 명사 = 충분한 ~."),
 (P5, "Mr. Han ------- the hotel for 20 years before he retired.", ["had managed", "manages", "will manage", "is managing"], 0, "과거(retired)보다 앞선 기간이므로 과거완료 had managed."),
 (P5, "Please keep the receipt ------- you need a refund.", ["in case", "in spite of", "instead of", "because of"], 0, "in case + 절 = ~할 경우에 대비해."),
]
P6Q = "\n\n빈칸에 알맞은 말은?"
B56 += [
 (P6, "Dear Ms. Allen,\nThank you for your reservation. We have reserved a deluxe room for you from May 2 to May 4. -------, breakfast is included in your rate." + P6Q, ["In addition", "However", "Otherwise", "Instead"], 0, "좋은 정보에 정보를 하나 더 더하므로 In addition."),
 (P6, "Our rooftop bar is very popular on weekends. -------, we recommend that you reserve a table in advance." + P6Q, ["Therefore", "However", "Instead", "Otherwise"], 0, "인기가 많다 → 그래서 예약 권장 = Therefore."),
 (P6, "The hotel gym is free for all guests. -------, personal training sessions cost 50,000 won per hour." + P6Q, ["However", "Therefore", "For example", "Similarly"], 0, "무료 ↔ 유료로 대조되므로 However."),
 (P6, "We offer many services for business travelers. -------, guests can use our meeting rooms and printers 24 hours a day." + P6Q, ["For example", "However", "Otherwise", "Nevertheless"], 0, "서비스의 예를 드는 문장이므로 For example."),
 (P6, "Please return your key card at check-out. -------, a fee of 10,000 won will be charged." + P6Q, ["Otherwise", "Moreover", "Likewise", "Meanwhile"], 0, "반납하지 않으면 요금 = Otherwise(그렇지 않으면)."),
 (P6, "The elevators will be inspected on Tuesday morning. ------- this time, please use the stairs or the service elevator." + P6Q, ["During", "While", "Since", "Until"], 0, "뒤에 명사(this time)이므로 전치사 During."),
 (P6, "Thank you for staying with us. We hope you ------- your stay. Please leave a review on our website." + P6Q, ["enjoyed", "enjoy", "enjoying", "will enjoy"], 0, "투숙이 끝난 뒤이므로 과거 enjoyed."),
 (P6, "Dear guests,\nThe hotel restaurant will close early tonight for a private event. Room service will ------- be available until midnight." + P6Q, ["still", "yet", "already", "ever"], 0, "식당은 닫지만 룸서비스는 여전히 가능 = still."),
 (P6, "To: All staff\nThe new uniforms have arrived. Please pick ------- up from the housekeeping office by Friday." + P6Q, ["them", "it", "they", "those ones"], 0, "uniforms(복수)를 받는 목적격 them."),
 (P6, "We are pleased to announce that our new spa will open on June 1. To celebrate, all treatments will be 20% off ------- the first week." + P6Q, ["for", "since", "by", "until"], 0, "for + 기간(the first week)."),
 (P6, "Dear Mr. Park,\nI am writing to ------- your booking for a meeting room on March 10." + P6Q, ["confirm", "confirmation", "confirmed", "confirming"], 0, "to부정사 뒤에는 동사원형 confirm."),
 (P6, "The airport shuttle runs every hour. Guests who wish to use it should ------- at the front desk the day before." + P6Q, ["sign up", "signing up", "signed up", "to sign up"], 0, "should + 동사원형."),
 (P6, "Please note that the outdoor pool is not heated. -------, it may be too cold for swimming in May." + P6Q, ["As a result", "In contrast", "For instance", "Even so"], 0, "난방이 안 됨 → 결과적으로 추움 = As a result."),
 (P6, "Thank you for your feedback. We are sorry that your room was noisy. We have shared your comments with our engineering team, and they are working to ------- the problem." + P6Q, ["fix", "fixing", "fixed", "fixes"], 0, "to부정사 뒤 동사원형 fix."),
 (P6, "Welcome to the Jeonju Grand Hotel! Your comfort is our top -------. Please call us if you need anything." + P6Q, ["priority", "prior", "prioritize", "priorly"], 0, "top 뒤 명사 자리 priority(우선순위)."),
 (P6, "We are hiring part-time banquet servers. Applicants should be friendly and able to work on weekends. Experience is helpful ------- not necessary." + P6Q, ["but", "and", "so", "or"], 0, "도움이 되지만 필수는 아님 = but."),
 (P6, "Dear valued guest,\nYour flight has been ------- by two hours. We have arranged a late check-out for you at no extra cost." + P6Q, ["delayed", "delaying", "delay", "delays"], 0, "has been + 과거분사."),
 (P6, "Guests can borrow umbrellas from the bell desk. Please return ------- when you check out." + P6Q, ["them", "it", "theirs", "one"], 0, "umbrellas(복수)를 받는 them."),
 (P6, "Our cooking class is held every Saturday. It is suitable for beginners, ------- no experience is needed." + P6Q, ["so", "but", "or", "yet"], 0, "초보자에게 적합 → 그래서 경험 불필요 = so."),
 (P6, "The lobby café will be closed on Monday. ------- will reopen on Tuesday at 7 a.m." + P6Q, ["It", "They", "We", "This one's"], 0, "The lobby café(단수)를 받는 대명사 It."),
]

P2 = "Part 2 · 질의응답"
B12 = [
 (P2, "Where is the business center?", ["It's on the second floor.", "Yes, it's busy.", "At 9 o'clock."], 0, "Where → 장소."),
 (P2, "When does the pool close?", ["At 10 p.m.", "Near the gym.", "No, it's open."], 0, "When → 시간."),
 (P2, "Who is in charge of the wedding banquet?", ["Ms. Kim from the events team.", "In the grand ballroom.", "It was a lovely wedding."], 0, "Who → 사람·부서."),
 (P2, "Why was the shuttle late?", ["There was heavy traffic.", "It leaves every hour.", "At the main entrance."], 0, "Why → 이유."),
 (P2, "How much is the airport taxi?", ["About 30,000 won.", "It takes an hour.", "Yes, I'll take a taxi."], 0, "How much → 가격."),
 (P2, "Could you bring me some extra towels?", ["Sure, I'll send them right away.", "They're very soft.", "No, I didn't bring it."], 0, "부탁 → 수락."),
 (P2, "Why don't we eat at the hotel restaurant tonight?", ["That's a good idea.", "Because it was closed.", "I ate at seven."], 0, "Why don't we ~? = 제안 → 동의."),
 (P2, "Would you like a window seat or an aisle seat?", ["A window seat, please.", "Yes, I would.", "It's a nice seat."], 0, "선택 의문문 → 하나 선택."),
 (P2, "Did you send the invoice to the travel agency?", ["Yes, this morning.", "The agency is downtown.", "I'll travel next week."], 0, "Did you ~? → Yes/No + 정보."),
 (P2, "Isn't the restaurant open on Sundays?", ["Only for lunch.", "I opened the window.", "It's a nice restaurant."], 0, "부정 의문문도 사실대로 답합니다."),
 (P2, "How long will the renovation take?", ["About three weeks.", "It's very long.", "In the lobby."], 0, "How long → 기간."),
 (P2, "Which room did the guest complain about?", ["Room 1204, I think.", "He complained yesterday.", "It's a nice room."], 0, "Which room → 특정 방."),
 (P2, "The printer in the business center isn't working.", ["I'll call the technician.", "It printed fifty pages.", "Yes, I'm working."], 0, "문제 제기(평서문) → 해결책 제시."),
 (P2, "Where should I put these boxes?", ["In the storage room, please.", "They're heavy boxes.", "Yesterday afternoon."], 0, "Where → 장소."),
 (P2, "When will the new manager start?", ["Next Monday.", "At the front office.", "He's very kind."], 0, "When → 시점."),
 (P2, "Do you have any rooms available tonight?", ["Let me check for you.", "Yes, it's tonight.", "I'd like a room."], 0, "모를 때: Let me check."),
 (P2, "Who left this bag in the lobby?", ["I'm not sure. Let me ask the bellman.", "It's a leather bag.", "On the sofa."], 0, "I'm not sure도 자주 정답입니다."),
 (P2, "Should I book the tour today or tomorrow?", ["Today would be better.", "Yes, you should.", "It's a city tour."], 0, "선택 의문문 → 하나 선택."),
 (P2, "How was your stay with us?", ["It was wonderful, thanks.", "I stayed three nights.", "At the Grand Hotel."], 0, "How was ~? → 소감."),
 (P2, "Can I pay by credit card?", ["Of course. We accept all major cards.", "The card is in the room.", "I paid yesterday."], 0, "허락 요청 → 수락."),
 (P2, "Why is the lobby so crowded?", ["A tour group just arrived.", "It's a big lobby.", "On the first floor."], 0, "Why → 이유."),
 (P2, "What time is check-out?", ["It's at noon.", "I checked out.", "About two days."], 0, "What time → 시각."),
 (P2, "Has the conference room been set up?", ["Yes, it's ready.", "I set my alarm.", "It's on the third floor."], 0, "완료 여부 → Yes + 상태."),
 (P2, "Who should I talk to about a refund?", ["The front office manager.", "About 50,000 won.", "Yes, it's refundable."], 0, "Who → 사람."),
 (P2, "Would you mind waiting for a few minutes?", ["Not at all.", "Yes, I'm waiting.", "A few minutes ago."], 0, "Would you mind ~? → Not at all(괜찮아요)."),
 (P2, "Where can I exchange money?", ["At the bank next door.", "The rate is good.", "Yes, I changed it."], 0, "Where → 장소."),
 (P2, "How often do you clean the pool?", ["Every morning.", "It's a clean pool.", "About 25 meters."], 0, "How often → 빈도."),
 (P2, "Are you coming to the staff meeting?", ["Yes, I'll be there.", "It was a long meeting.", "In meeting room B."], 0, "Are you ~? → Yes/No."),
 (P2, "I'd like to change my room.", ["Is there a problem with it?", "It's a nice change.", "Yes, it's room 302."], 0, "요청 → 이유를 묻는 응답."),
 (P2, "When did the guests check in?", ["About an hour ago.", "At the front desk.", "For three nights."], 0, "When(과거) → 과거 시점."),
 (P2, "What's the Wi-Fi password?", ["It's on your key card holder.", "It's very fast.", "Yes, it's free."], 0, "정보 요청 → 찾는 곳 안내."),
 (P2, "Who's going to pick up the guests at the airport?", ["Our driver, Mr. Lee.", "At 3 p.m.", "Incheon Airport."], 0, "Who → 사람."),
 (P2, "Why don't you take a break?", ["Thanks, I will.", "It's broken.", "Because I'm tired."], 0, "제안 → 수락."),
 (P2, "Do you know where the nearest pharmacy is?", ["There's one across the street.", "Yes, I know him.", "It sells medicine."], 0, "간접 의문문(where) → 장소."),
 (P2, "How many guests are expected at the party?", ["About eighty.", "It's a big party.", "On Saturday night."], 0, "How many → 수."),
 (P2, "Shall I call a taxi for you?", ["Yes, please.", "It's a yellow taxi.", "I called yesterday."], 0, "Shall I ~? 제안 → Yes, please."),
 (P2, "The guest in 805 wants a late check-out.", ["We can give her until 2 p.m.", "She checked in late.", "Room 805 is a suite."], 0, "요청 전달 → 해결책."),
 (P2, "Where did you put the guest list?", ["On your desk.", "About 200 guests.", "Yes, I listed them."], 0, "Where → 장소."),
 (P2, "Is breakfast included in the price?", ["Yes, it's served from 7 to 10.", "The price is high.", "I had breakfast."], 0, "포함 여부 → Yes + 정보."),
 (P2, "How do I get to the hanok village?", ["Take bus number 5.", "It's a nice village.", "About an hour ago."], 0, "How do I get to ~? → 교통편."),
 (P2, "Which floor is the gym on?", ["The third floor.", "It's open 24 hours.", "Yes, it's on."], 0, "Which floor → 층."),
 (P2, "Why hasn't the room been cleaned yet?", ["The housekeeper is on her way.", "It's a clean room.", "Yesterday morning."], 0, "Why → 이유·상황."),
 (P2, "Can you recommend a good restaurant?", ["Sure, try the Korean place downstairs.", "Yes, it's recommended.", "I ate there."], 0, "추천 요청 → 추천."),
 (P2, "Who answered the phone at the front desk?", ["Minji did.", "The phone is new.", "About ten calls."], 0, "Who → 사람."),
 (P2, "When is the payment due?", ["By the end of the month.", "About 300 dollars.", "Yes, it's paid."], 0, "When → 시점."),
 (P2, "Would you like me to carry your bags?", ["That would be great, thanks.", "They're my bags.", "Yes, I carried them."], 0, "Would you like me to ~? → 수락."),
 (P2, "Don't you have a smaller room?", ["Yes, a single room is available.", "It's a small hotel.", "No, I don't like it."], 0, "부정 의문문 → 사실대로."),
 (P2, "How was the conference?", ["It went very well.", "In the ballroom.", "About 150 people."], 0, "How was ~? → 소감."),
 (P2, "Where's the closest ATM?", ["Next to the convenience store.", "I need some cash.", "Yes, it's close."], 0, "Where → 장소."),
 (P2, "Could you spell your last name, please?", ["Sure, it's K-I-M.", "It's my name.", "I'm last in line."], 0, "부탁 → 수락 + 정보."),
 (P2, "The air conditioner in my room is too loud.", ["I'll send an engineer right away.", "It's very cold.", "Yes, it's on."], 0, "불만 → 해결책."),
 (P2, "Who's giving the keynote speech?", ["The CEO of the company.", "It starts at nine.", "It was a great speech."], 0, "Who → 사람."),
 (P2, "Are there any vegetarian dishes?", ["Yes, the bibimbap is vegetarian.", "The dish is hot.", "I'm not hungry."], 0, "Are there ~? → Yes + 예시."),
 (P2, "When can I pick up my laundry?", ["After 5 p.m. today.", "At the laundry room.", "Yes, it's clean."], 0, "When → 시간."),
 (P2, "Why did the guest cancel his booking?", ["His flight was canceled.", "He booked online.", "Yes, it's free."], 0, "Why → 이유."),
 (P2, "Have you ever been to Jeonju?", ["Yes, twice.", "It's in Korea.", "I'll go tomorrow."], 0, "경험 → Yes + 횟수."),
 (P2, "What do you think of the new menu?", ["I like it a lot.", "It's on the table.", "Yes, I think so."], 0, "의견 → 의견."),
 (P2, "How far is the station from here?", ["About ten minutes on foot.", "It's a big station.", "At 3:20."], 0, "How far → 거리·시간."),
 (P2, "Is the spa open today?", ["No, it's closed for cleaning.", "It's a nice spa.", "Yes, I'm open."], 0, "Is ~? → Yes/No + 이유."),
 (P2, "Who's responsible for the lost and found?", ["The housekeeping office.", "I found it in the lobby.", "Yes, it's lost."], 0, "Who → 부서."),
 (P2, "Can I leave my luggage here after check-out?", ["Of course. The bell desk can keep it.", "It's heavy luggage.", "I checked out."], 0, "허락 요청 → 수락 + 안내."),
 (P2, "Where will the farewell dinner be held?", ["In the garden restaurant.", "At 7 p.m.", "It was delicious."], 0, "Where → 장소."),
 (P2, "Do you want to share a taxi to the airport?", ["Sure, that would save money.", "It's a big taxi.", "I shared it."], 0, "제안 → 동의."),
 (P2, "Which credit cards do you accept?", ["Visa and Mastercard.", "Yes, we accept them.", "About 20,000 won."], 0, "Which → 종류."),
 (P2, "Wasn't the meeting moved to Thursday?", ["Yes, I just heard.", "It's a big meeting.", "I moved last year."], 0, "부정 의문문 → 확인."),
 (P2, "How can I reach the operator?", ["Just dial 0.", "It's a reach-in fridge.", "She's very kind."], 0, "How → 방법."),
 (P2, "Why is room 302 still marked dirty?", ["The guest just checked out.", "It's a dirty room.", "On the third floor."], 0, "Why → 이유."),
 (P2, "Would you prefer tea or coffee?", ["Coffee, please.", "Yes, I prefer it.", "It's hot."], 0, "선택 의문문 → 하나 선택."),
 (P2, "Who should I give this package to?", ["Leave it at the front desk.", "It's a big package.", "Yes, it's a gift."], 0, "Who → 간접적으로 장소를 안내하는 답도 정답."),
 (P2, "When does the next shuttle leave?", ["In fifteen minutes.", "From the main gate.", "It's free."], 0, "When → 시간."),
 (P2, "Did the guest like the room upgrade?", ["She was very happy with it.", "It's on the 20th floor.", "Yes, it's upgraded."], 0, "Did ~? → 반응 서술."),
 (P2, "How about meeting in the lobby at six?", ["Six works for me.", "It's a big lobby.", "I met him at six."], 0, "How about ~? 제안 → 동의."),
 (P2, "Where are the extra blankets kept?", ["In the closet.", "They're warm.", "Yes, I kept them."], 0, "Where → 장소."),
 (P2, "What's today's special?", ["Grilled salmon with salad.", "It's very special.", "Today is Monday."], 0, "What → 내용."),
 (P2, "Is it possible to extend my stay?", ["Let me check our availability.", "It's a long stay.", "Yes, I stayed."], 0, "모를 때: Let me check."),
 (P2, "Who designed the new lobby?", ["A famous local architect.", "It's very bright.", "Last year."], 0, "Who → 사람."),
 (P2, "How long have you worked here?", ["For about five years.", "Until 6 p.m.", "Here in Jeonju."], 0, "How long → 기간."),
 (P2, "Can you show me how to use the safe?", ["Sure, enter a four-digit code first.", "It's a safe hotel.", "I showed him."], 0, "방법 요청 → 설명."),
 (P2, "Why don't we offer a free drink to the waiting guests?", ["That's a great idea.", "Because they're free.", "They waited an hour."], 0, "제안 → 동의."),
 (P2, "Where does this bus go?", ["To Jeonju Station.", "Every ten minutes.", "It's bus 12."], 0, "Where → 목적지."),
]

P3 = "Part 3 · 짧은 대화"
P4 = "Part 4 · 짧은 담화"
def S(part, script, *qs):
    """one script, several questions: (question, [answer first, wrong, wrong, wrong], explanation)"""
    return [(part, q, opts, 0, why, script) for q, opts, why in qs]

B3 = []
B3 += S(P3, "M: Hi, I'm checking out of room 512. Here's my key card.\nW: Thank you, Mr. Davis. Did you have anything from the minibar?\nM: Just two bottles of water.\nW: Those are complimentary. Your total is 240,000 won. Would you like a receipt by email?",
 ("Where most likely are the speakers?", ["At a hotel front desk", "At a restaurant", "At an airport", "At a bank"], "check out, room, key card로 호텔 프런트임을 알 수 있습니다."),
 ("What did the man take from the minibar?", ["Water", "Juice", "Beer", "Snacks"], "two bottles of water라고 했습니다."),
 ("What does the woman offer?", ["To email a receipt", "To call a taxi", "To store his luggage", "To upgrade his room"], "Would you like a receipt by email?"))
B3 += S(P3, "W: Excuse me, the air conditioner in my room is making a strange noise.\nM: I'm sorry about that. What's your room number?\nW: It's 1108. I couldn't sleep at all last night.\nM: I'll send a technician right away. If it can't be fixed, we'll move you to another room.",
 ("What is the woman's problem?", ["Her air conditioner is noisy", "Her room is too small", "She lost her key", "Her bill is wrong"], "air conditioner is making a strange noise."),
 ("What does the man ask for?", ["A room number", "A credit card", "A passport", "A phone number"], "What's your room number?"),
 ("What will the man probably do next?", ["Send a technician", "Give a refund", "Call a taxi", "Bring breakfast"], "I'll send a technician right away."))
B3 += S(P3, "M: Good evening. Do you have a table for four?\nW: Do you have a reservation?\nM: No, we don't.\nW: I'm afraid we're fully booked until eight. Would you like to wait in the bar? I can call you when a table is ready.",
 ("Where does the conversation take place?", ["At a restaurant", "At a hotel room", "At a museum", "At a train station"], "table for four, reservation, bar로 식당입니다."),
 ("How many people are in the man's group?", ["Four", "Two", "Six", "Eight"], "a table for four."),
 ("What does the woman suggest?", ["Waiting in the bar", "Coming back tomorrow", "Ordering takeout", "Sitting outside"], "Would you like to wait in the bar?"))
B3 += S(P3, "W: Hello, I'd like to book a city tour for tomorrow.\nM: Sure. We have a morning tour at nine and an afternoon tour at two.\nW: The morning one, please. Does it include lunch?\nM: No, but it ends at a popular market, so you can eat there.",
 ("What does the woman want to do?", ["Book a tour", "Rent a car", "Cancel a reservation", "Change rooms"], "book a city tour."),
 ("What time does the woman's tour start?", ["At 9:00", "At 2:00", "At 10:00", "At 12:00"], "The morning one(9시)을 골랐습니다."),
 ("Where does the tour end?", ["At a market", "At the hotel", "At a museum", "At a palace"], "it ends at a popular market."))
B3 += S(P3, "M: Housekeeping. May I clean your room now?\nW: Could you come back in an hour? I'm on a conference call.\nM: Of course. Do you need anything else?\nW: Yes, could you bring two more towels later?",
 ("Who most likely is the man?", ["A housekeeper", "A chef", "A driver", "A receptionist"], "Housekeeping. May I clean your room?"),
 ("Why can't the woman let the man in?", ["She is on a call", "She is sleeping", "She is leaving", "She is sick"], "I'm on a conference call."),
 ("What does the woman ask for?", ["Towels", "Pillows", "Coffee", "A newspaper"], "two more towels."))
B3 += S(P3, "W: Hi, I'm calling about my reservation for next Friday. I need to change it.\nM: Certainly. What's your name, please?\nW: Emma Stone. I'd like to arrive on Saturday instead.\nM: No problem. There's no fee because it's more than three days before arrival.",
 ("Why is the woman calling?", ["To change a reservation", "To make a complaint", "To ask about parking", "To cancel a tour"], "I need to change it."),
 ("When does the woman want to arrive?", ["On Saturday", "On Friday", "On Sunday", "On Thursday"], "arrive on Saturday instead."),
 ("Why is there no fee?", ["She changed it early enough", "She is a member", "The hotel made a mistake", "It is a holiday"], "more than three days before arrival."))
B3 += S(P3, "M: Excuse me, which bus goes to the airport?\nW: The airport limousine stops right in front of the hotel. It comes every 30 minutes.\nM: How much is it?\nW: It's 15,000 won. You can buy a ticket here at the concierge desk.",
 ("What does the man want to know?", ["How to get to the airport", "Where to eat dinner", "When check-out is", "How to use the safe"], "which bus goes to the airport?"),
 ("How often does the limousine come?", ["Every 30 minutes", "Every 10 minutes", "Every hour", "Twice a day"], "It comes every 30 minutes."),
 ("Where can the man buy a ticket?", ["At the concierge desk", "On the bus", "At the airport", "Online only"], "buy a ticket here at the concierge desk."))
B3 += S(P3, "W: Did you finish the seating chart for the Kim wedding?\nM: Almost. The bride's family added ten more guests this morning.\nW: Then we'll need another table. Can you tell the kitchen too?\nM: Sure, I'll call the chef after lunch.",
 ("What are the speakers discussing?", ["A wedding event", "A staff party", "A cooking class", "A business trip"], "the seating chart for the Kim wedding."),
 ("What changed this morning?", ["More guests were added", "The date changed", "The menu changed", "The room changed"], "added ten more guests."),
 ("What will the man do after lunch?", ["Call the chef", "Visit the bride", "Print the menu", "Order flowers"], "I'll call the chef after lunch."))
B3 += S(P3, "M: I'd like to stay one more night. Is that possible?\nW: Let me check... Yes, your room is available tomorrow too.\nM: Great. Is the rate the same?\nW: It's a little higher on Saturdays, 180,000 won instead of 150,000.",
 ("What does the man want to do?", ["Extend his stay", "Check out early", "Change rooms", "Book a tour"], "stay one more night."),
 ("What does the woman say about the room?", ["It is available", "It is being cleaned", "It is fully booked", "It is too small"], "your room is available tomorrow too."),
 ("How much is the Saturday rate?", ["180,000 won", "150,000 won", "200,000 won", "120,000 won"], "180,000 won instead of 150,000."))
B3 += S(P3, "W: Excuse me, I left my sunglasses by the pool this afternoon.\nM: Let me check the lost and found. What do they look like?\nW: They're black with a gold logo.\nM: Here they are. Please sign this form before you take them.",
 ("What did the woman lose?", ["Sunglasses", "A phone", "A towel", "A wallet"], "I left my sunglasses."),
 ("Where did she leave the item?", ["By the pool", "In the gym", "In the lobby", "At the restaurant"], "by the pool."),
 ("What does the man ask her to do?", ["Sign a form", "Show her passport", "Pay a fee", "Come back later"], "Please sign this form."))
B3 += S(P3, "M: Hi, this is Tom from room 407. I ordered room service 40 minutes ago, but it hasn't arrived.\nW: I'm very sorry, sir. Let me check with the kitchen.\nW: Your order is on its way now. We'll take 20 percent off your bill for the delay.",
 ("Why is the man calling?", ["His order is late", "His room is dirty", "He wants a taxi", "He lost his key"], "it hasn't arrived."),
 ("How long has the man waited?", ["40 minutes", "20 minutes", "An hour", "10 minutes"], "40 minutes ago."),
 ("What does the woman offer?", ["A discount", "A free night", "A new room", "A free drink"], "20 percent off your bill."))
B3 += S(P3, "W: Good morning. Is the gym open now?\nM: Yes, it opens at six. You'll need your key card to enter.\nW: Do I need to bring a towel?\nM: No, towels and water are provided inside.",
 ("What does the woman ask about?", ["The gym", "The spa", "Breakfast", "The pool bar"], "Is the gym open now?"),
 ("What does she need to enter?", ["Her key card", "A ticket", "Her passport", "A membership card"], "You'll need your key card."),
 ("What is provided inside?", ["Towels and water", "Shoes and clothes", "Snacks", "Lockers only"], "towels and water are provided."))
B3 += S(P3, "M: The printer in the business center isn't working.\nW: Oh, sorry. It's been slow all morning. You can use the one in the sales office.\nM: Where's that?\nW: Behind the front desk. I'll show you the way.",
 ("What is the problem?", ["A printer isn't working", "The Wi-Fi is down", "A meeting room is booked", "The elevator is broken"], "The printer isn't working."),
 ("What does the woman suggest?", ["Using another printer", "Coming back later", "Calling a technician", "Emailing the file"], "use the one in the sales office."),
 ("What will the woman do next?", ["Show the man the way", "Fix the printer", "Print the file for him", "Call her manager"], "I'll show you the way."))
B3 += S(P3, "W: We have a group of 30 students arriving tomorrow. Are their rooms ready?\nM: Yes, fifteen twin rooms on the 5th floor.\nW: Good. Their bus arrives at 2, but check-in is at 3.\nM: We can store their luggage and give them welcome drinks in the lobby.",
 ("Who is arriving tomorrow?", ["A student group", "A wedding party", "A sports team", "A business group"], "a group of 30 students."),
 ("How many rooms are reserved?", ["Fifteen", "Thirty", "Five", "Ten"], "fifteen twin rooms."),
 ("What does the man suggest for the early arrival?", ["Storing luggage and serving drinks", "Early check-in for all", "A city tour", "Lunch at the restaurant"], "store their luggage and give them welcome drinks."))
B3 += S(P3, "M: Hello, I'd like a wake-up call tomorrow morning.\nW: Certainly. What time?\nM: 5:30. I have an early flight.\nW: All right. Would you like a breakfast box too? The restaurant doesn't open until 6:30.",
 ("What does the man request?", ["A wake-up call", "A taxi", "A late check-out", "Extra pillows"], "a wake-up call."),
 ("Why does the man need to get up early?", ["He has an early flight", "He has a meeting", "He is going hiking", "He wants breakfast"], "I have an early flight."),
 ("What does the woman offer?", ["A breakfast box", "A free taxi", "An airport shuttle", "A room upgrade"], "Would you like a breakfast box too?"))
B3 += S(P3, "W: Hi, I'm interested in the front desk position.\nM: Thanks for coming. Do you have any hotel experience?\nW: Yes, I worked part-time at a guesthouse in Jeonju for a year.\nM: Great. Can you start next month? We need someone for the weekend shift.",
 ("What is the purpose of the conversation?", ["A job interview", "A room booking", "A complaint", "A training class"], "interested in the front desk position."),
 ("Where did the woman work before?", ["At a guesthouse", "At a restaurant", "At a travel agency", "At a bank"], "worked part-time at a guesthouse."),
 ("What shift does the man mention?", ["The weekend shift", "The night shift", "The morning shift", "The holiday shift"], "the weekend shift."))
B3 += S(P3, "M: Can I pay for dinner with my room key?\nW: Yes, just sign the bill and write your room number.\nM: Will the charge be on my final bill?\nW: That's right. You'll pay everything at check-out.",
 ("What does the man want to do?", ["Charge dinner to his room", "Pay in cash", "Split the bill", "Get a refund"], "pay for dinner with my room key."),
 ("What does the woman ask him to write?", ["His room number", "His phone number", "His email", "His passport number"], "write your room number."),
 ("When will the man pay?", ["At check-out", "Right now", "Tomorrow morning", "Next month"], "pay everything at check-out."))
B3 += S(P3, "W: Our flight was canceled, so we need a room for tonight.\nM: I'm sorry to hear that. We have a double room left.\nW: Perfect. Do you have an airport shuttle tomorrow morning?\nM: Yes, the first one leaves at 6. I'll reserve two seats for you.",
 ("Why does the woman need a room?", ["Her flight was canceled", "Her hotel was full", "She missed a train", "She arrived early"], "Our flight was canceled."),
 ("What kind of room is available?", ["A double room", "A suite", "A single room", "A twin room"], "a double room left."),
 ("What will the man do?", ["Reserve shuttle seats", "Call the airline", "Give a discount", "Book a taxi"], "I'll reserve two seats for you."))
B3 += S(P3, "M: The guests in 902 said their room smells of smoke.\nW: But it's a non-smoking room. Did the last guest smoke?\nM: Maybe. Let's move them to 905 and clean 902 with the deodorizer.\nW: OK. I'll also add a cleaning fee to the last guest's bill.",
 ("What is the problem with room 902?", ["It smells of smoke", "The TV is broken", "It is too cold", "The bed is small"], "their room smells of smoke."),
 ("What will happen to the guests?", ["They will move to another room", "They will get a refund", "They will check out", "They will get a free dinner"], "move them to 905."),
 ("What will the woman do?", ["Add a fee to a bill", "Call the police", "Open the windows", "Write a review"], "add a cleaning fee to the last guest's bill."))
B3 += S(P3, "W: Excuse me, is there a pharmacy near here? I have a headache.\nM: There's one across the street, but it closes at 9. It's 9:30 now.\nW: Oh no.\nM: Don't worry. We have some basic medicine at the front desk. I'll get you some.",
 ("What is the woman's problem?", ["She has a headache", "She lost her bag", "She is hungry", "She missed a bus"], "I have a headache."),
 ("Why can't she go to the pharmacy?", ["It is closed", "It is too far", "It is out of medicine", "It is under renovation"], "it closes at 9. It's 9:30 now."),
 ("What will the man do?", ["Get her some medicine", "Call a doctor", "Call a taxi", "Take her to a hospital"], "I'll get you some."))
B3 += S(P3, "M: How was the cooking class this morning?\nW: It was great! We made bibimbap and kimchi pancakes.\nM: Would you recommend it to other guests?\nW: Definitely. But it's only on Saturdays, so they should book early.",
 ("What did the woman do this morning?", ["Took a cooking class", "Went shopping", "Visited a museum", "Played golf"], "the cooking class this morning."),
 ("What did they make?", ["Bibimbap and pancakes", "Kimchi stew", "Bread and cake", "Dumplings"], "bibimbap and kimchi pancakes."),
 ("What does the woman advise?", ["Booking early", "Coming hungry", "Bringing an apron", "Paying in cash"], "they should book early."))
B3 += S(P3, "W: I'd like to rent a car for two days.\nM: Do you have an international driving permit?\nW: Yes, here it is.\nM: Thank you. The car will be at the main entrance in 20 minutes. Please return it with a full tank.",
 ("What does the woman want to do?", ["Rent a car", "Buy a ticket", "Book a room", "Exchange money"], "rent a car for two days."),
 ("What document does the man ask for?", ["A driving permit", "A passport", "A credit card", "A room key"], "an international driving permit."),
 ("What should the woman do when she returns the car?", ["Fill the gas tank", "Wash the car", "Pay a deposit", "Call the hotel"], "return it with a full tank."))
B3 += S(P3, "M: Welcome to the spa. Do you have an appointment?\nW: Yes, a 60-minute massage at 4 under Park.\nM: Thank you, Ms. Park. Please fill out this health form first.\nW: Sure. Can I have a female therapist?\nM: Of course. Yuna will be with you in a few minutes.",
 ("Where are the speakers?", ["At a spa", "At a hospital", "At a gym", "At a salon"], "Welcome to the spa."),
 ("What does the man ask the woman to do?", ["Fill out a form", "Pay in advance", "Change clothes", "Wait outside"], "fill out this health form."),
 ("What does the woman request?", ["A female therapist", "A longer massage", "A quiet room", "A discount"], "Can I have a female therapist?"))
B3 += S(P3, "W: The ballroom projector stopped working during the presentation.\nM: I'll bring a spare one from the storage room.\nW: How long will it take?\nM: About five minutes. Maybe the speaker can take a short coffee break.",
 ("What is the problem?", ["A projector stopped working", "The ballroom is too hot", "The speaker is late", "The microphones are missing"], "The ballroom projector stopped working."),
 ("What will the man bring?", ["A spare projector", "Coffee", "A microphone", "A laptop"], "I'll bring a spare one."),
 ("What does the man suggest?", ["A short coffee break", "Ending the meeting", "Moving rooms", "Calling the speaker"], "take a short coffee break."))
B3 += S(P3, "M: I booked through a travel website, but you can't find my reservation?\nW: I'm sorry. Do you have the confirmation email?\nM: Yes, it's on my phone.\nW: Thank you. The website sent it to our sister hotel. Don't worry, we have a room for you here at the same rate.",
 ("What is the man's problem?", ["His reservation can't be found", "His room is too small", "His card was declined", "He lost his phone"], "you can't find my reservation?"),
 ("What does the woman ask for?", ["A confirmation email", "A passport", "A deposit", "A phone number"], "Do you have the confirmation email?"),
 ("What caused the problem?", ["It was sent to another hotel", "The man booked the wrong date", "The hotel was overbooked", "The website was closed"], "The website sent it to our sister hotel."))

B4 = []
B4 += S(P4, "Attention, guests. The outdoor pool will close at 6 p.m. today because of a private event. The indoor pool on the B1 level will stay open until 10 p.m. Towels are available at the spa reception. Thank you for your understanding.",
 ("Why will the outdoor pool close early?", ["Because of a private event", "Because of the weather", "Because of cleaning", "Because of a repair"], "because of a private event."),
 ("Where is the indoor pool?", ["On the B1 level", "On the rooftop", "Next to the lobby", "On the 3rd floor"], "The indoor pool on the B1 level."),
 ("Where can guests get towels?", ["At the spa reception", "At the front desk", "In their rooms", "At the pool bar"], "Towels are available at the spa reception."))
B4 += S(P4, "Hi, this is Jenny from Hana Travel. I'm calling about our group booking for May 10. We now have 25 people instead of 20, so we need three more twin rooms. Please call me back at 010-2345-6789. Thank you.",
 ("Why is the speaker calling?", ["To change a group booking", "To cancel a tour", "To complain about a room", "To ask about prices"], "I'm calling about our group booking."),
 ("How many people are in the group now?", ["25", "20", "30", "23"], "25 people instead of 20."),
 ("What does the speaker ask the listener to do?", ["Call her back", "Send an email", "Visit her office", "Reserve a bus"], "Please call me back."))
B4 += S(P4, "Welcome to the Jeonju Hanok Village walking tour. My name is Minho, and I'll be your guide today. The tour takes about two hours. We'll visit Gyeonggijeon Shrine and a traditional tea house. Please stay with the group and don't forget to drink water.",
 ("Who is the speaker?", ["A tour guide", "A hotel manager", "A bus driver", "A chef"], "I'll be your guide today."),
 ("How long is the tour?", ["About two hours", "About one hour", "Half a day", "All day"], "The tour takes about two hours."),
 ("What are listeners asked to do?", ["Stay with the group", "Buy tickets", "Take photos", "Wear hanbok"], "Please stay with the group."))
B4 += S(P4, "Good morning, everyone. Before we open the restaurant, I have some news. Starting next Monday, we'll have a new seasonal menu with local ingredients. Please read the menu notes in the staff room so you can explain the dishes to guests.",
 ("Who is the speaker probably talking to?", ["Restaurant staff", "Hotel guests", "Students", "Tour members"], "Before we open the restaurant … staff room."),
 ("What will start next Monday?", ["A new seasonal menu", "A cooking class", "New opening hours", "A staff party"], "a new seasonal menu."),
 ("What should the listeners do?", ["Read the menu notes", "Taste every dish", "Work extra hours", "Call the chef"], "Please read the menu notes."))
B4 += S(P4, "Thank you for calling the Seoul Grand Hotel. Our front desk is busy at the moment. For reservations, press 1. For restaurant bookings, press 2. To speak to the operator, please stay on the line.",
 ("What kind of message is this?", ["A recorded phone message", "A radio ad", "A tour talk", "A safety announcement"], "Thank you for calling … press 1."),
 ("What should callers press for restaurant bookings?", ["2", "1", "0", "3"], "For restaurant bookings, press 2."),
 ("How can callers speak to the operator?", ["By staying on the line", "By pressing 9", "By sending an email", "By calling later"], "please stay on the line."))
B4 += S(P4, "Attention, all guests. We will test the fire alarm system today between 2 and 3 p.m. You may hear the alarm several times. There is no need to leave the building. We apologize for any inconvenience.",
 ("What is the announcement about?", ["A fire alarm test", "A real fire", "A power outage", "A water problem"], "test the fire alarm system."),
 ("When will the test take place?", ["Between 2 and 3 p.m.", "In the morning", "At midnight", "Tomorrow"], "between 2 and 3 p.m."),
 ("What are guests told?", ["They don't need to leave", "They must go outside", "They should call the front desk", "They should close their windows"], "There is no need to leave the building."))
B4 += S(P4, "Hello, Mr. Brown. This is Sora from the concierge desk. Your dinner reservation at the Korean restaurant is confirmed for 7 p.m. tonight. A taxi will be waiting at the main entrance at 6:40. Enjoy your evening!",
 ("Who is the speaker?", ["A concierge", "A chef", "A taxi driver", "A tour guide"], "This is Sora from the concierge desk."),
 ("What time is the dinner reservation?", ["7 p.m.", "6:40 p.m.", "6 p.m.", "8 p.m."], "confirmed for 7 p.m."),
 ("What has the speaker arranged?", ["A taxi", "A tour", "A massage", "A wake-up call"], "A taxi will be waiting."))
B4 += S(P4, "Welcome aboard the hotel shuttle to Incheon Airport. The trip will take about one hour, depending on traffic. Free bottled water is in the pocket in front of you. Please keep your seat belt fastened at all times.",
 ("Where is the speaker?", ["On a shuttle bus", "On a plane", "In a hotel lobby", "On a train"], "Welcome aboard the hotel shuttle."),
 ("How long will the trip take?", ["About one hour", "About 30 minutes", "Two hours", "Fifteen minutes"], "about one hour."),
 ("What is offered for free?", ["Bottled water", "Snacks", "Newspapers", "Wi-Fi"], "Free bottled water."))
B4 += S(P4, "Good afternoon, team. As you know, the hotel is fully booked this weekend because of the film festival. Housekeeping will need extra help on Saturday. If you can work an extra shift, please tell your supervisor by Thursday.",
 ("Why is the hotel fully booked?", ["Because of a film festival", "Because of a holiday", "Because of a conference", "Because of a wedding"], "because of the film festival."),
 ("Which department needs help?", ["Housekeeping", "The kitchen", "The front desk", "Security"], "Housekeeping will need extra help."),
 ("What should interested staff do?", ["Tell their supervisor", "Sign a form", "Email the manager", "Come early on Friday"], "please tell your supervisor by Thursday."))
B4 += S(P4, "Hi, this is Ken from room 1203. I'd like to report a problem. The TV remote control isn't working, and I think it needs new batteries. Could someone bring new ones? I'll be in the room until 8. Thanks.",
 ("Why is the speaker calling?", ["To report a problem", "To order food", "To book a tour", "To ask for directions"], "I'd like to report a problem."),
 ("What is not working?", ["The TV remote", "The air conditioner", "The shower", "The lights"], "The TV remote control isn't working."),
 ("What does the speaker ask for?", ["New batteries", "A new room", "A technician", "A refund"], "Could someone bring new ones(batteries)?"))
B4 += S(P4, "Ladies and gentlemen, welcome to the Hotel Management Seminar. Our first speaker is Dr. Kim, the general manager of the Jeonju Grand Hotel. She will talk about service quality. Lunch will be served in the garden room after her talk.",
 ("Where is the talk taking place?", ["At a seminar", "At a wedding", "At a restaurant opening", "At a job interview"], "welcome to the Hotel Management Seminar."),
 ("Who is Dr. Kim?", ["A general manager", "A chef", "A professor of history", "A travel agent"], "the general manager of the Jeonju Grand Hotel."),
 ("What will happen after the talk?", ["Lunch will be served", "A tour will start", "A video will be shown", "Guests will check in"], "Lunch will be served … after her talk."))
B4 += S(P4, "Attention, shoppers. Our hotel gift shop is having a special sale this week. All Korean cosmetics are 30 percent off until Sunday. Show your room key at the counter and receive a free gift with any purchase.",
 ("What is being advertised?", ["A gift shop sale", "A new restaurant", "A spa package", "A city tour"], "Our hotel gift shop is having a special sale."),
 ("How long will the sale last?", ["Until Sunday", "Until Friday", "One day", "One month"], "until Sunday."),
 ("How can customers get a free gift?", ["By showing a room key", "By spending 100,000 won", "By joining online", "By writing a review"], "Show your room key … receive a free gift."))
B4 += S(P4, "Good evening. This is your captain speaking. Because of strong winds in Jeju, our landing will be delayed by about 20 minutes. Please stay in your seats with your seat belts on. Flight attendants will come around with water shortly.",
 ("Who is the speaker?", ["A pilot", "A hotel manager", "A tour guide", "A bus driver"], "This is your captain speaking."),
 ("Why will the landing be delayed?", ["Because of strong winds", "Because of heavy traffic", "Because of a mechanical problem", "Because of a late passenger"], "Because of strong winds."),
 ("What will flight attendants do?", ["Bring water", "Serve meals", "Sell duty-free goods", "Check tickets"], "come around with water."))
B4 += S(P4, "Hi, Ms. Lee. This is Daniel from the sales team at the Riverside Hotel. Thank you for your interest in our meeting rooms. I've attached our price list to an email. I'd be happy to show you the rooms. Are you free on Wednesday afternoon?",
 ("What is the purpose of the call?", ["To follow up on an inquiry", "To cancel a meeting", "To ask for payment", "To apologize for a mistake"], "Thank you for your interest in our meeting rooms."),
 ("What did the speaker send?", ["A price list", "A contract", "A map", "A menu"], "I've attached our price list."),
 ("What does the speaker want to do?", ["Show the meeting rooms", "Change the date", "Lower the price", "Book a table"], "I'd be happy to show you the rooms."))
B4 += S(P4, "Welcome to our breakfast buffet. Hot dishes are on your left, and fresh fruit and salad are on your right. Our chef is making omelets at the egg station. Breakfast is served until 10:30. Enjoy your meal.",
 ("Where is the speaker?", ["At a breakfast buffet", "At a cooking class", "At a market", "At a bar"], "Welcome to our breakfast buffet."),
 ("What is the chef making?", ["Omelets", "Pancakes", "Toast", "Noodles"], "making omelets at the egg station."),
 ("Until what time is breakfast served?", ["10:30", "10:00", "11:00", "9:30"], "served until 10:30."))
B4 += S(P4, "This is a message for all hotel staff. Starting tomorrow, all employees must wear their name tags at work. New name tags are ready in the human resources office. Please pick yours up before your shift.",
 ("Who is the message for?", ["Hotel staff", "Hotel guests", "Tour groups", "Job applicants"], "a message for all hotel staff."),
 ("What must employees do starting tomorrow?", ["Wear name tags", "Work longer hours", "Wear new uniforms", "Use a new computer system"], "must wear their name tags."),
 ("Where can employees get the new item?", ["In the human resources office", "At the front desk", "In the staff cafeteria", "From their supervisor"], "ready in the human resources office."))
B4 += S(P4, "Thank you for joining the hanji craft class. Today you'll make a small lamp with traditional Korean paper. The class takes 90 minutes. Please put on an apron, and be careful with the scissors. You can take your lamp home after it dries.",
 ("What will listeners make?", ["A paper lamp", "A clay cup", "A fan", "A painting"], "make a small lamp with traditional Korean paper."),
 ("How long is the class?", ["90 minutes", "60 minutes", "Two hours", "30 minutes"], "The class takes 90 minutes."),
 ("What are listeners asked to do?", ["Put on an apron", "Bring their own paper", "Pay at the door", "Take photos"], "Please put on an apron."))
B4 += S(P4, "Good morning, Jeonju! Here's today's weather. It will be sunny and warm this morning, but rain is expected after 4 p.m. If you're going out tonight, take an umbrella. Tomorrow will be clear and cooler.",
 ("What is the talk about?", ["The weather", "Traffic", "A festival", "A sports game"], "Here's today's weather."),
 ("When is rain expected?", ["After 4 p.m.", "This morning", "Tomorrow", "At noon"], "rain is expected after 4 p.m."),
 ("What does the speaker advise?", ["Taking an umbrella", "Staying home", "Wearing a jacket", "Leaving early"], "take an umbrella."))

def R7(kind, text, *qs):
    return [("Part 7 · " + kind, text + "\n\nQ. " + q, opts, 0, why) for q, opts, why in qs]

B7 = []
B7 += R7("공지", "NOTICE\nThe hotel lobby will be under renovation from March 2 to March 20. During this time, please use the side entrance on Daehak-ro. The front desk has moved temporarily to the 2nd floor. We are sorry for any inconvenience.",
 ("What is the notice mainly about?", ["Lobby renovation", "A new restaurant", "A price change", "A fire drill"], "The hotel lobby will be under renovation."),
 ("Where is the front desk during the renovation?", ["On the 2nd floor", "At the side entrance", "In the restaurant", "On Daehak-ro"], "moved temporarily to the 2nd floor."),
 ("How long will the renovation last?", ["About three weeks", "One week", "Two days", "Two months"], "March 2 to March 20(약 3주)."))
B7 += R7("이메일", "To: Kevin Lee\nFrom: Jeonju Grand Hotel\nSubject: Your upcoming stay\n\nDear Mr. Lee,\nWe look forward to welcoming you on April 12. Your room is a deluxe twin, and breakfast is included. Check-in starts at 3 p.m. If you arrive early, we can keep your luggage. Free airport pickup is available if you send us your flight number by April 10.",
 ("What is the purpose of the email?", ["To give information before a stay", "To ask for payment", "To apologize for a problem", "To offer a job"], "We look forward to welcoming you … 투숙 전 안내."),
 ("What is included in Mr. Lee's booking?", ["Breakfast", "Dinner", "A spa treatment", "A city tour"], "breakfast is included."),
 ("What should Mr. Lee do to get a free pickup?", ["Send his flight number", "Pay a deposit", "Call the hotel", "Arrive before 3 p.m."], "if you send us your flight number by April 10."))
B7 += R7("문자 대화", "Jisu (10:02): The bus to the market is full. Can we take a taxi?\nMark (10:03): Sure. How much will it cost?\nJisu (10:04): About 8,000 won. We can share it.\nMark (10:05): Sounds good. I'll meet you at the hotel entrance in five minutes.",
 ("Why does Jisu suggest a taxi?", ["The bus is full", "It is raining", "They are late", "The market is far"], "The bus to the market is full."),
 ("What does Mark mean by \"Sounds good\"?", ["He agrees with the plan", "He likes the music", "He wants to pay alone", "He will take the bus"], "공유 택시 제안에 동의하는 말입니다."),
 ("Where will they meet?", ["At the hotel entrance", "At the market", "At the bus stop", "In the lobby café"], "meet you at the hotel entrance."))
B7 += R7("후기", "★★★★☆ Great location, small rooms\nI stayed three nights at the City Hotel. It's only five minutes from the station, and the staff were very kind. The breakfast had many choices. However, our room was small for two people, and the Wi-Fi was slow in the evening. I would stay here again for a short trip.",
 ("What did the writer like?", ["The location and the staff", "The room size", "The Wi-Fi", "The price"], "five minutes from the station, the staff were very kind."),
 ("What was a problem?", ["The Wi-Fi was slow", "The breakfast was cold", "The staff were rude", "The station was far"], "the Wi-Fi was slow in the evening."),
 ("What is suggested about the writer?", ["She would return for a short trip", "She will never come back", "She stayed one night", "She traveled alone"], "I would stay here again for a short trip."))
B7 += R7("광고", "Jeonju Hanok Stay\nExperience a night in a traditional Korean house!\n- Floor beds and heated ondol floors\n- Free Korean breakfast\n- Tea ceremony every evening at 7\n- 10% off for stays of three nights or more\nBook at www.hanokstay.kr",
 ("What is being advertised?", ["A traditional house to stay in", "A cooking school", "A tea shop", "A furniture store"], "Experience a night in a traditional Korean house!"),
 ("What happens every evening?", ["A tea ceremony", "A cooking class", "A concert", "A city tour"], "Tea ceremony every evening at 7."),
 ("How can guests get a discount?", ["By staying three nights or more", "By booking by phone", "By paying in cash", "By coming in winter"], "10% off for stays of three nights or more."))
B7 += R7("공지", "To all staff:\nThe staff cafeteria will close at 2 p.m. on Friday for a deep cleaning. Lunch boxes will be available in the training room from 11:30. Please return the empty boxes to the kitchen. Thank you.\n- Human Resources",
 ("Why will the cafeteria close early?", ["For a deep cleaning", "For a staff party", "For a holiday", "For a repair"], "for a deep cleaning."),
 ("Where can staff get lunch?", ["In the training room", "In the lobby", "At the restaurant", "Outside the hotel"], "Lunch boxes will be available in the training room."),
 ("Who wrote the notice?", ["Human Resources", "The chef", "The general manager", "Housekeeping"], "- Human Resources."))
B7 += R7("이메일", "Dear Ms. Park,\nThank you for choosing our hotel for your company's year-end party on December 20. As requested, we have reserved the Garden Hall for 60 people. The buffet costs 55,000 won per person. Please confirm the final number of guests by December 13. A 30% deposit is required to complete the booking.\nBest regards,\nTom Choi, Event Manager",
 ("What event is Ms. Park planning?", ["A year-end party", "A wedding", "A conference", "A birthday party"], "your company's year-end party."),
 ("By when must Ms. Park confirm the number of guests?", ["December 13", "December 20", "December 1", "December 31"], "by December 13."),
 ("What is required to complete the booking?", ["A deposit", "A signed menu", "A guest list", "A site visit"], "A 30% deposit is required."))
B7 += R7("문자 대화", "Front Desk (14:10): Hello Ms. Wang, your room is ready earlier than expected.\nMs. Wang (14:12): That's great! I'm still at the museum, though.\nFront Desk (14:13): No problem. Your luggage is already in the room.\nMs. Wang (14:15): Perfect, thank you so much!",
 ("Why did the front desk send a message?", ["The room is ready early", "The museum is closed", "Her luggage is lost", "Her payment failed"], "your room is ready earlier than expected."),
 ("Where is Ms. Wang now?", ["At the museum", "In the lobby", "At the airport", "In her room"], "I'm still at the museum."),
 ("What is true about her luggage?", ["It is in her room", "It is at the museum", "It is at the bell desk", "It is still at the airport"], "Your luggage is already in the room."))
B7 += R7("안내문", "WELCOME TO YOUR ROOM\n- Wi-Fi: Grand_Guest / password: welcome2026\n- Breakfast: 6:30–10:00, 1st floor restaurant\n- Late check-out until 2 p.m.: 30,000 won\n- Laundry bags are in the closet. Items returned the next day by 6 p.m.\n- Dial 0 for the front desk, 3 for room service",
 ("Where is breakfast served?", ["In the 1st floor restaurant", "In the room", "On the rooftop", "In the lobby"], "1st floor restaurant."),
 ("How much is late check-out?", ["30,000 won", "Free", "20,000 won", "50,000 won"], "Late check-out until 2 p.m.: 30,000 won."),
 ("What number should guests dial for room service?", ["3", "0", "9", "1"], "3 for room service."))
B7 += R7("광고", "Riverside Hotel Spa – Autumn Special\nEnjoy a 90-minute aromatherapy massage and a foot bath for only 120,000 won (regular price 160,000 won). Available Monday to Thursday only, from September 1 to November 30. Hotel guests get a free herbal tea. Reservations are required.",
 ("What is the regular price of the package?", ["160,000 won", "120,000 won", "90,000 won", "200,000 won"], "regular price 160,000 won."),
 ("When is the special NOT available?", ["On Saturdays", "On Mondays", "On Wednesdays", "In October"], "Monday to Thursday only → 토요일은 안 됩니다."),
 ("What do hotel guests receive?", ["A free herbal tea", "A free massage", "A room upgrade", "A gift card"], "Hotel guests get a free herbal tea."))
B7 += R7("메모", "MEMO\nTo: Front desk staff\nFrom: Sujin Han, Front Office Manager\nA large group from Japan will arrive at about 4 p.m. tomorrow. Their room keys are ready in envelopes. Please give each guest a city map and explain the breakfast time. Two staff members who speak Japanese will help at the desk.",
 ("Who is the memo for?", ["Front desk staff", "Guests from Japan", "Housekeeping", "The restaurant"], "To: Front desk staff."),
 ("What should staff give each guest?", ["A city map", "A free drink", "A gift", "A coupon"], "give each guest a city map."),
 ("How will the hotel help the group?", ["Japanese-speaking staff will assist", "A guide will meet them", "They will get a discount", "A bus will pick them up"], "Two staff members who speak Japanese will help."))
B7 += R7("이메일", "Dear Mr. Garcia,\nThank you for your feedback about your stay last week. We are sorry that the noise from the street kept you awake. We have now installed new windows on the street side of the hotel. As a thank-you for your comments, we would like to offer you a free night on your next visit.\nSincerely,\nAnna Yoon, Guest Relations",
 ("Why did Ms. Yoon write the email?", ["To respond to a complaint", "To confirm a booking", "To advertise a sale", "To ask for payment"], "Thank you for your feedback … We are sorry."),
 ("What was Mr. Garcia's problem?", ["Street noise", "A dirty room", "A late breakfast", "A wrong bill"], "the noise from the street kept you awake."),
 ("What is offered to Mr. Garcia?", ["A free night", "A refund", "A free dinner", "A room upgrade"], "offer you a free night on your next visit."))
B7 += R7("일정표", "Jeonju One-Day Tour\n09:00 Meet at the hotel lobby\n09:30 Jeonju Hanok Village walking tour\n11:30 Bibimbap lunch (included)\n13:00 Hanji museum\n15:00 Free time at Nambu Market\n17:00 Return to the hotel\nPrice: 45,000 won per person (children under 10: 25,000 won)",
 ("Where does the tour start?", ["At the hotel lobby", "At Nambu Market", "At the museum", "At the train station"], "Meet at the hotel lobby."),
 ("What is included in the price?", ["Lunch", "Dinner", "Shopping money", "A hanbok rental"], "Bibimbap lunch (included)."),
 ("How much is the tour for an 8-year-old child?", ["25,000 won", "45,000 won", "Free", "35,000 won"], "children under 10: 25,000 won."))
B7 += R7("문자 대화", "Manager (08:15): Minji, can you cover the front desk from 2 to 4 today? Junho is sick.\nMinji (08:20): I have a class until 1, but I can be there by 1:45.\nManager (08:21): That works. Thanks a lot!\nMinji (08:22): No problem.",
 ("Why does the manager need help?", ["A coworker is sick", "There is a big group", "The desk is broken", "She is going on vacation"], "Junho is sick."),
 ("What is suggested about Minji?", ["She is a student", "She is the manager", "She is sick", "She works at night"], "I have a class until 1 → 학생입니다."),
 ("What does the manager mean by \"That works\"?", ["The time is fine", "The computer is working", "Minji should work harder", "The class is good"], "1시 45분 도착이 괜찮다는 뜻입니다."))
B7 += R7("공지", "PARKING INFORMATION\nHotel guests can park for free for up to 24 hours. Please register your car number at the front desk when you check in. After 24 hours, parking costs 2,000 won per hour. Visitors who are not staying at the hotel pay 3,000 won per hour. The parking lot is closed from 1 a.m. to 5 a.m.",
 ("What must guests do to park for free?", ["Register their car number", "Pay a deposit", "Show a parking ticket", "Park outside"], "register your car number at the front desk."),
 ("How much do non-guests pay per hour?", ["3,000 won", "2,000 won", "Free", "5,000 won"], "Visitors … pay 3,000 won per hour."),
 ("When is the parking lot closed?", ["From 1 a.m. to 5 a.m.", "All day Sunday", "From midnight to 6 a.m.", "During check-in"], "closed from 1 a.m. to 5 a.m."))
B7 += R7("구인 광고", "NOW HIRING: Banquet Servers (part-time)\nJeonju Grand Hotel is looking for friendly banquet servers for weekend weddings and events.\n- Hours: Saturday and Sunday, 10 a.m.–4 p.m.\n- Pay: 12,000 won per hour, free lunch\n- Basic English is helpful. No experience needed; training is provided.\nSend your resume to jobs@jeonjugrand.com by June 15.",
 ("What kind of job is advertised?", ["Banquet server", "Front desk clerk", "Chef", "Driver"], "Banquet Servers."),
 ("What is NOT mentioned as a benefit?", ["Free parking", "Free lunch", "Training", "Hourly pay"], "주차는 언급되지 않았습니다."),
 ("How should people apply?", ["By sending a resume by email", "By visiting the hotel", "By calling the manager", "By filling out a form online"], "Send your resume to jobs@….")) 
B7 += R7("영수증", "JEONJU GRAND HOTEL — Guest Folio\nGuest: Sarah Miller  Room: 708\nRoom (2 nights)  300,000\nMinibar  12,000\nLaundry  18,000\nRestaurant (dinner)  64,000\nTax & service  39,400\nTOTAL  433,400 won\nPaid by credit card",
 ("How many nights did Ms. Miller stay?", ["Two", "One", "Three", "Seven"], "Room (2 nights)."),
 ("Which charge was the highest after the room?", ["Restaurant", "Laundry", "Minibar", "Tax & service"], "Restaurant (dinner) 64,000."),
 ("How did Ms. Miller pay?", ["By credit card", "In cash", "By bank transfer", "With a voucher"], "Paid by credit card."))
B7 += R7("이메일", "Hi Daniel,\nI'm writing about the hotel management workshop next Thursday. The room has changed from Room 301 to the Lake Hall because more people signed up. Lunch will still be served at noon. Could you bring the projector from the office? Thanks!\nYuna",
 ("Why has the room changed?", ["More people signed up", "Room 301 is being repaired", "The date changed", "Lunch is served there"], "because more people signed up."),
 ("Where will the workshop be held now?", ["In the Lake Hall", "In Room 301", "In the office", "In the restaurant"], "to the Lake Hall."),
 ("What does Yuna ask Daniel to do?", ["Bring a projector", "Order lunch", "Send invitations", "Book a room"], "Could you bring the projector?"))
B7 += R7("안내문", "LOST AND FOUND\nItems left in rooms are kept for 30 days. Valuable items such as phones, wallets, and jewelry are kept in the security office. To get an item back, please show your ID and booking number. We can also send items by courier; the guest pays the shipping fee.",
 ("How long are lost items kept?", ["30 days", "7 days", "One year", "90 days"], "kept for 30 days."),
 ("Where are valuable items kept?", ["In the security office", "At the front desk", "In the housekeeping room", "In the guest's room"], "kept in the security office."),
 ("Who pays to send an item by courier?", ["The guest", "The hotel", "The courier company", "Housekeeping"], "the guest pays the shipping fee."))
B7 += R7("후기", "★★★★★ Perfect for families!\nWe stayed at the Sunny Resort with our two kids for four nights. The kids' club had fun activities every day, and the pool was clean and safe with a lifeguard. The family room was big enough for all of us. The only downside was the long line at breakfast on Sunday.",
 ("Who did the writer travel with?", ["Her family", "Her coworkers", "Her friends", "A tour group"], "with our two kids."),
 ("What did the writer say about the pool?", ["It was clean and safe", "It was closed", "It was too small", "It was cold"], "the pool was clean and safe."),
 ("What was the only problem?", ["A long breakfast line", "A small room", "A rude lifeguard", "A dirty pool"], "the long line at breakfast on Sunday."))

P1 = "Part 1 · 사진 묘사"
B12 += [
 (P1, "사진: 남자가 책상에서 노트북으로 타이핑하고 있다.", ["He's typing on a laptop.", "He's reading a newspaper.", "He's drinking coffee.", "He's hanging a picture."], 0, "노트북으로 타이핑하는 동작을 묘사했습니다."),
 (P1, "사진: 여자가 잔에 물을 따르고 있다.", ["She's pouring water into a glass.", "She's washing the dishes.", "She's setting up chairs.", "She's opening a bottle of wine."], 0, "pouring water into a glass가 정확합니다."),
 (P1, "사진: 침대 위에 수건이 개어져 있다.", ["Some towels have been folded on the bed.", "A woman is making the bed.", "Towels are hanging on the wall.", "The bed is being moved."], 0, "사람이 없으므로 상태(have been folded)."),
 (P1, "사진: 두 사람이 로비에서 악수하고 있다.", ["They're shaking hands.", "They're carrying boxes.", "They're sitting on a sofa.", "They're waving goodbye."], 0, "악수하는 동작 = shaking hands."),
 (P1, "사진: 남자가 계단을 올라가고 있다.", ["He's walking up the stairs.", "He's taking an elevator.", "He's cleaning the stairs.", "He's sitting on the steps."], 0, "계단을 올라가는 동작 = walking up the stairs."),
 (P1, "사진: 수영장 옆에 선베드가 줄지어 놓여 있다.", ["Some lounge chairs have been lined up by the pool.", "People are swimming in the pool.", "A lifeguard is blowing a whistle.", "The pool is being cleaned."], 0, "사람이 없으므로 상태(have been lined up)."),
 (P1, "사진: 여자가 진공청소기로 바닥을 청소하고 있다.", ["She's vacuuming the floor.", "She's making the bed.", "She's opening the curtains.", "She's folding towels."], 0, "진공청소기로 청소 = vacuuming."),
 (P1, "사진: 남자가 지도를 보고 있다.", ["He's looking at a map.", "He's taking a photo.", "He's buying a ticket.", "He's crossing the street."], 0, "지도를 보는 동작."),
 (P1, "사진: 버스가 호텔 앞에 서 있다.", ["A bus is parked in front of the hotel.", "Passengers are getting off a bus.", "A man is driving a taxi.", "A bus is being washed."], 0, "사람이 없는 장면, 버스가 서 있는 상태."),
 (P1, "사진: 여자가 여행 가방을 끌고 걸어가고 있다.", ["She's pulling a suitcase.", "She's opening a suitcase.", "She's lifting a box.", "She's sitting on a bench."], 0, "가방을 끌고 가는 동작 = pulling a suitcase."),
 (P1, "사진: 요리사가 프라이팬으로 요리하고 있다.", ["A chef is cooking in a pan.", "A chef is washing a pan.", "A waiter is serving food.", "A chef is cutting bread."], 0, "프라이팬으로 요리 = cooking in a pan."),
 (P1, "사진: 선반에 와인병들이 진열되어 있다.", ["Wine bottles have been arranged on shelves.", "A man is pouring wine.", "Bottles are being thrown away.", "Some glasses are on a table."], 0, "사람이 없으므로 상태(have been arranged)."),
 (P1, "사진: 남자가 전화 통화를 하고 있다.", ["He's talking on the phone.", "He's typing on a keyboard.", "He's writing a letter.", "He's turning on a lamp."], 0, "전화 통화 = talking on the phone."),
]
# RYU 2026-11-25: "TOEIC 문제를 총 1000문제로", "추가하는 문제들은 다양한 영역에서 나오게, 호텔 분야가 아니어도 됨".
# The additions live in tqbank_p*.py (office, bank, shop, factory, hospital, IT, transport, school, housing …).
from tqbank_p1 import B1X
from tqbank_p2 import B2X
from tqbank_p34 import B3X, B4X
from tqbank_p5 import B5X
from tqbank_p5b import B5Y
from tqbank_p6 import B6X
from tqbank_p7 import B7X
B5X = B5X[::3]   # hotel sentences: every third one, the rest of Part 5 comes from other fields (B5Y)
BANK = {}
for _q in B12 + B2X + B1X + B3 + B3X + B4 + B4X + B56 + B5X + B5Y + B6X + B7 + B7X:
    BANK.setdefault(_q[0].split(" ·")[0], []).append(_q)
