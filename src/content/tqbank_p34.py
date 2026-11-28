# TOEIC bank, Part 3 and Part 4 additions from many fields (RYU 2026-11-25). Answer is always the FIRST choice; build.py shuffles.
P3 = "Part 3 · 짧은 대화"
P4 = "Part 4 · 짧은 담화"
def S(part, script, *qs):
    return [(part, q, opts, 0, why, script) for q, opts, why in qs]

B3X = []
B3X += S(P3, "M: Hi, I bought this blender here last week, but it stopped working yesterday.\nW: I'm sorry about that. Do you have the receipt?\nM: Yes, here it is.\nW: Thank you. Would you like a refund or a new one?\nM: A new one, please.",
 ("Where most likely are the speakers?", ["At an electronics store", "At a restaurant", "At a bank", "At a post office"], "bought this blender here, receipt, refund로 매장임을 알 수 있습니다."),
 ("What is the problem with the blender?", ["It stopped working.", "It is too loud.", "It is the wrong color.", "It arrived late."], "it stopped working yesterday."),
 ("What does the man decide to do?", ["Get a new blender", "Get his money back", "Repair it himself", "Buy a different brand"], "A new one, please."))
B3X += S(P3, "W: Good morning. I'd like to open a savings account.\nM: Certainly. May I see your ID?\nW: Here's my passport. How much do I need to deposit?\nM: The minimum is ten dollars. Would you also like a debit card?\nW: Yes, please.",
 ("Where does the conversation take place?", ["At a bank", "At an airport", "At a library", "At a clinic"], "open a savings account, deposit, debit card."),
 ("What does the woman show the man?", ["Her passport", "Her driver's license", "Her student card", "Her credit card"], "Here's my passport."),
 ("What is the minimum deposit?", ["Ten dollars", "Five dollars", "Fifty dollars", "One hundred dollars"], "The minimum is ten dollars."))
B3X += S(P3, "M: Sarah, have you finished the slides for Thursday's client meeting?\nW: Almost. I'm still waiting for the sales numbers from the finance team.\nM: I see. Can you send me a draft by tomorrow noon?\nW: Sure. I'll call finance right now and ask them to hurry.",
 ("What are the speakers discussing?", ["Slides for a client meeting", "A job interview", "A business trip", "A new office"], "the slides for Thursday's client meeting."),
 ("What is the woman waiting for?", ["Sales numbers", "A new computer", "A client's email", "Her manager's signature"], "waiting for the sales numbers from the finance team."),
 ("What will the woman do next?", ["Call the finance team", "Cancel the meeting", "Print the slides", "Go to lunch"], "I'll call finance right now."))
B3X += S(P3, "W: Hello, I have an appointment with Dr. Patel at 2:30.\nM: Your name, please?\nW: Linda Brooks.\nM: Thank you, Ms. Brooks. The doctor is running about 20 minutes late. Please fill out this form while you wait.\nW: All right. Is there a water fountain nearby?\nM: Yes, just down the hall.",
 ("Where are the speakers?", ["At a doctor's office", "At a law firm", "At a gym", "At a school"], "appointment with Dr. Patel, the doctor."),
 ("What does the man say about the doctor?", ["He is running late.", "He is on vacation.", "He has left for the day.", "He is new."], "running about 20 minutes late."),
 ("What does the man ask the woman to do?", ["Fill out a form", "Come back tomorrow", "Pay in advance", "Call the doctor"], "Please fill out this form while you wait."))
B3X += S(P3, "M: Excuse me, does this train go to Central Station?\nW: No, this is the express to the airport. You need the green line on platform 4.\nM: Oh, thank you. When is the next one?\nW: In about five minutes. You'd better hurry.",
 ("Where does the man want to go?", ["Central Station", "The airport", "City Hall", "The harbor"], "does this train go to Central Station?"),
 ("Which platform should the man go to?", ["Platform 4", "Platform 1", "Platform 5", "Platform 7"], "the green line on platform 4."),
 ("When does the next train leave?", ["In about five minutes", "In one hour", "In thirty minutes", "Tomorrow morning"], "In about five minutes."))
B3X += S(P3, "W: Hi, I ordered a desk from your website two weeks ago, but it still hasn't arrived.\nM: I'm sorry. Could I have your order number?\nW: It's 58214.\nM: Let me see... It seems the truck was delayed by the snowstorm. It should arrive this Friday.\nW: Friday? Can I get free shipping, then?\nM: Yes, we'll refund the delivery fee.",
 ("Why is the woman calling?", ["Her order has not arrived.", "She wants to buy a chair.", "She received the wrong item.", "She wants to change her address."], "it still hasn't arrived."),
 ("What caused the delay?", ["A snowstorm", "A computer error", "A wrong address", "A holiday"], "the truck was delayed by the snowstorm."),
 ("What does the man offer to do?", ["Refund the delivery fee", "Send a second desk", "Give her a coupon", "Deliver it today"], "we'll refund the delivery fee."))
B3X += S(P3, "M: Thanks for coming in, Ms. Reyes. Why do you want to work for our company?\nW: I've used your accounting software for years, and I'd love to help improve it.\nM: Good to hear. Do you have experience leading a team?\nW: Yes, I managed five programmers at my last job.\nM: Excellent. We'll contact you by the end of the week.",
 ("What is the purpose of the conversation?", ["A job interview", "A sales call", "A product demonstration", "A customer complaint"], "Why do you want to work for our company?"),
 ("What does the company make?", ["Accounting software", "Office furniture", "Mobile phones", "Medical equipment"], "your accounting software."),
 ("When will the woman hear from the company?", ["By the end of the week", "In a month", "Tomorrow morning", "Next year"], "We'll contact you by the end of the week."))
B3X += S(P3, "W: The air conditioner in the meeting room is leaking water again.\nM: Really? The repairman fixed it only last month.\nW: I know. Maybe we should just buy a new one.\nM: Let's ask for a price first. I'll call a few stores this afternoon.",
 ("What is the problem?", ["An air conditioner is leaking.", "A window is broken.", "A light is out.", "A door is locked."], "The air conditioner ... is leaking water again."),
 ("When was the air conditioner last repaired?", ["Last month", "Last week", "Yesterday", "Last year"], "fixed it only last month."),
 ("What will the man do this afternoon?", ["Call some stores", "Fix the machine himself", "Move the meeting", "Buy a fan"], "I'll call a few stores this afternoon."))
B3X += S(P3, "M: I'd like to send this package to Canada. How long will it take?\nW: Regular mail takes about ten days. Express takes three.\nM: How much is express?\nW: Forty-two dollars. Regular is eighteen.\nM: It's a birthday gift for next week, so I'll take express.",
 ("Where are the speakers?", ["At a post office", "At a gift shop", "At an airport", "At a bookstore"], "send this package, regular mail, express."),
 ("How long does express mail take?", ["Three days", "Ten days", "One day", "Two weeks"], "Express takes three."),
 ("Why does the man choose express mail?", ["The gift must arrive by next week.", "It is cheaper.", "The package is heavy.", "Regular mail is closed."], "It's a birthday gift for next week."))
B3X += S(P3, "W: Did you hear that our office is moving to the Parker Building in March?\nM: Yes. It's closer to the subway, so my commute will be shorter.\nW: Lucky you. It'll take me twenty minutes longer.\nM: Why don't you ask about working from home twice a week? The company allows it now.",
 ("What are the speakers talking about?", ["An office move", "A new employee", "A company dinner", "A subway delay"], "our office is moving to the Parker Building."),
 ("Why is the man pleased?", ["His commute will be shorter.", "He got a promotion.", "He will get a bigger desk.", "He can park for free."], "my commute will be shorter."),
 ("What does the man suggest?", ["Asking to work from home", "Buying a car", "Moving to a new apartment", "Changing jobs"], "Why don't you ask about working from home twice a week?"))
B3X += S(P3, "M: Welcome to Fit Zone. Are you interested in a membership?\nW: Yes. How much is it per month?\nM: It's fifty dollars, but if you sign up for a year, it's forty a month.\nW: Does that include the swimming pool?\nM: Yes, and two free sessions with a personal trainer.",
 ("Where is the conversation taking place?", ["At a fitness center", "At a swimming school", "At a sports store", "At a hospital"], "Fit Zone, membership, personal trainer."),
 ("How much is the monthly fee with a one-year contract?", ["Forty dollars", "Fifty dollars", "Twenty dollars", "Sixty dollars"], "if you sign up for a year, it's forty a month."),
 ("What is included in the membership?", ["Use of the swimming pool", "Free parking", "A free T-shirt", "Yoga classes every day"], "Does that include the swimming pool? - Yes."))
B3X += S(P3, "W: Hi, I'm looking for a two-bedroom apartment near the university.\nM: We have one on Oak Street. It's 900 dollars a month.\nW: Is it furnished?\nM: Yes, and it has a washing machine. Would you like to see it this afternoon?\nW: I have class until three. How about four o'clock?",
 ("Who most likely is the man?", ["A real estate agent", "A professor", "A furniture salesman", "A bank teller"], "아파트를 소개하고 보여 주는 사람 = 부동산 중개인."),
 ("How much is the rent?", ["900 dollars a month", "700 dollars a month", "1,200 dollars a month", "400 dollars a month"], "It's 900 dollars a month."),
 ("When does the woman want to see the apartment?", ["At four o'clock", "At three o'clock", "Tomorrow morning", "Right now"], "How about four o'clock?"))
B3X += S(P3, "M: The new software update deleted some of my files.\nW: Don't worry. Everything is backed up on the server every night.\nM: That's a relief. How do I get them back?\nW: I'll do it for you. Just give me your employee number.",
 ("What is the man's problem?", ["Some files were deleted.", "His computer won't turn on.", "He forgot his password.", "His screen is broken."], "deleted some of my files."),
 ("How often is the data backed up?", ["Every night", "Every week", "Once a month", "Every hour"], "backed up on the server every night."),
 ("What does the woman ask for?", ["His employee number", "His password", "His phone", "His laptop"], "Just give me your employee number."))
B3X += S(P3, "W: Welcome to Bella's. Are you ready to order?\nM: What do you recommend?\nW: The mushroom risotto is our most popular dish. Today's special is grilled salmon.\nM: I'll have the salmon. And could I get the salad dressing on the side?\nW: Of course.",
 ("Who most likely is the woman?", ["A server", "A chef", "A cashier at a supermarket", "A food critic"], "Are you ready to order?"),
 ("What is today's special?", ["Grilled salmon", "Mushroom risotto", "Steak", "Chicken salad"], "Today's special is grilled salmon."),
 ("What does the man ask for?", ["Dressing on the side", "A glass of wine", "A table by the window", "The bill"], "could I get the salad dressing on the side?"))
B3X += S(P3, "M: Did the parts from the supplier arrive this morning?\nW: Only half of them. The rest will come on Wednesday.\nM: That's a problem. We can't start the production line without them.\nW: I know. I've already asked the supplier to send them by air.",
 ("Where do the speakers most likely work?", ["At a factory", "At a travel agency", "At a school", "At a law office"], "parts, production line."),
 ("What is the problem?", ["Only half of the parts arrived.", "A machine broke down.", "A worker is absent.", "The parts are the wrong size."], "Only half of them."),
 ("What has the woman already done?", ["Asked for air delivery", "Canceled the order", "Found a new supplier", "Stopped the line"], "asked the supplier to send them by air."))
B3X += S(P3, "W: I'd like to return these books, and I also want to borrow this one.\nM: These two are three days late, so there's a fine of sixty cents.\nW: Oh, sorry. Here you go.\nM: Thanks. The new book is due in two weeks. You can renew it online.",
 ("Where are the speakers?", ["At a library", "At a bookstore", "At a school office", "At a printing shop"], "return, borrow, fine, due."),
 ("Why does the woman pay a fine?", ["Her books are late.", "She lost a book.", "She damaged a book.", "She has no library card."], "three days late."),
 ("When is the new book due?", ["In two weeks", "In three days", "In one month", "Tomorrow"], "due in two weeks."))
B3X += S(P3, "M: Our website traffic went down ten percent last month.\nW: I noticed. I think we need more videos on social media.\nM: Good idea. Do we have a budget for that?\nW: A small one. I'll write a plan and show it to you on Monday.",
 ("What problem do the speakers mention?", ["Website traffic decreased.", "A video was deleted.", "The budget was cut.", "A client complained."], "website traffic went down ten percent."),
 ("What does the woman suggest?", ["Making more videos", "Hiring a designer", "Lowering prices", "Closing the website"], "we need more videos on social media."),
 ("What will the woman do by Monday?", ["Write a plan", "Meet a client", "Buy a camera", "Post a video"], "I'll write a plan and show it to you on Monday."))
B3X += S(P3, "W: I'd like to exchange 500 US dollars for euros.\nM: Sure. Today's rate is 0.92 euros per dollar. There's a three-dollar service fee.\nW: That's fine. Can I have small bills?\nM: Of course. Please sign here.",
 ("What does the woman want to do?", ["Exchange money", "Open an account", "Pay a bill", "Send money abroad"], "exchange 500 US dollars for euros."),
 ("How much is the service fee?", ["Three dollars", "Five dollars", "Ninety-two cents", "Ten dollars"], "a three-dollar service fee."),
 ("What does the woman ask for?", ["Small bills", "A receipt", "Coins", "A new card"], "Can I have small bills?"))
B3X += S(P3, "M: Jane, the client loved your design for the coffee package.\nW: Really? That's great. Did they ask for any changes?\nM: Just one. They want the logo a little bigger.\nW: No problem. I'll send the new version before lunch.",
 ("What did the client think of the design?", ["They loved it.", "They rejected it.", "They have not seen it.", "They found it too expensive."], "the client loved your design."),
 ("What change does the client want?", ["A bigger logo", "A different color", "A new name", "A smaller box"], "They want the logo a little bigger."),
 ("When will the woman send the new version?", ["Before lunch", "Tomorrow", "Next week", "After the meeting"], "before lunch."))
B3X += S(P3, "W: Excuse me, my car won't start. Can you take a look?\nM: Sure. When did you last change the battery?\nW: About five years ago.\nM: That's probably the problem. A new one is 120 dollars, and it'll take thirty minutes.\nW: OK, go ahead. I'll wait in the café next door.",
 ("Who most likely is the man?", ["A mechanic", "A taxi driver", "A car salesman", "A police officer"], "차를 점검하고 배터리를 교체하는 사람 = 정비사."),
 ("What does the man think is the problem?", ["The battery is old.", "The car is out of gas.", "A tire is flat.", "The key is broken."], "About five years ago. - That's probably the problem."),
 ("Where will the woman wait?", ["In a café", "In her car", "At home", "In the office"], "I'll wait in the café next door."))
B3X += S(P3, "M: Are you going to the technology conference in Berlin next month?\nW: I'd like to, but my manager hasn't approved the travel budget yet.\nM: The early registration discount ends this Friday.\nW: Then I'd better talk to her today.",
 ("What event are the speakers discussing?", ["A technology conference", "A music festival", "A job fair", "A company picnic"], "the technology conference in Berlin."),
 ("What is the woman waiting for?", ["Approval of her travel budget", "A new passport", "An invitation letter", "Her plane ticket"], "my manager hasn't approved the travel budget yet."),
 ("What happens on Friday?", ["A discount ends.", "The conference starts.", "The manager returns.", "The flight leaves."], "The early registration discount ends this Friday."))
B3X += S(P3, "W: Thanks for calling City Power. How can I help you?\nM: My electricity bill is twice as high as last month's. I think there's a mistake.\nW: Let me check. Ah, the meter was read incorrectly. I'm sorry about that.\nM: So what should I do?\nW: Nothing. We'll send you a corrected bill within three days.",
 ("Why is the man calling?", ["His bill seems too high.", "His power is out.", "He is moving house.", "He wants to pay by card."], "My electricity bill is twice as high as last month's."),
 ("What caused the problem?", ["The meter was read incorrectly.", "The price went up.", "He used more power.", "He paid late."], "the meter was read incorrectly."),
 ("What will the company do?", ["Send a corrected bill", "Visit his house", "Cut off the power", "Give him a new meter"], "We'll send you a corrected bill within three days."))
B3X += S(P3, "M: How's the new intern doing?\nW: Very well. She learns fast, and she already handles customer emails alone.\nM: That's good. Do you think we should offer her a full-time job?\nW: Definitely. Her internship ends in August, so we should decide soon.",
 ("Who are the speakers talking about?", ["An intern", "A customer", "A manager", "A supplier"], "the new intern."),
 ("What does the woman say about the intern?", ["She learns fast.", "She is often late.", "She wants to quit.", "She needs more training."], "She learns fast."),
 ("When does the internship end?", ["In August", "In March", "In December", "Next week"], "Her internship ends in August."))
B3X += S(P3, "W: Hi, I'd like two tickets for the seven o'clock showing of 'Blue Ocean.'\nM: I'm sorry, that showing is sold out. We have seats for 9:15.\nW: Hmm, that's a bit late. Is there anything earlier?\nM: There's a 5:30 show, but only front-row seats are left.\nW: We'll take the 9:15, then.",
 ("Where is the woman?", ["At a movie theater", "At a train station", "At a concert hall", "At a museum"], "showing, seats, show."),
 ("Why can't the woman see the seven o'clock show?", ["It is sold out.", "It was canceled.", "It already started.", "It is too expensive."], "that showing is sold out."),
 ("Which show does the woman choose?", ["The 9:15 show", "The 5:30 show", "The 7:00 show", "Tomorrow's show"], "We'll take the 9:15, then."))

B4X = []
B4X += S(P4, "Attention, shoppers. Today only, all fresh fruit and vegetables are 20 percent off. You'll find them in aisle one, near the entrance. Also, don't forget to try our new bakery on the second floor. The store will close at 10 p.m. tonight. Thank you for shopping at Green Market.",
 ("Where is the announcement being made?", ["At a supermarket", "At a bakery school", "At a farm", "At a restaurant"], "shoppers, aisle, Green Market."),
 ("What is on sale today?", ["Fruit and vegetables", "Bread", "Meat", "Drinks"], "all fresh fruit and vegetables are 20 percent off."),
 ("Where is the new bakery?", ["On the second floor", "In aisle one", "Near the entrance", "Outside the store"], "our new bakery on the second floor."))
B4X += S(P4, "Hello, this is Mark from Sunrise Dental Clinic. I'm calling to remind you of your appointment with Dr. Lee on Tuesday at 10 a.m. If you need to change the time, please call us at 555-0142 by Monday. Please bring your insurance card. Thank you.",
 ("What is the purpose of the message?", ["To remind someone of an appointment", "To cancel an appointment", "To sell insurance", "To ask for payment"], "calling to remind you of your appointment."),
 ("When is the appointment?", ["Tuesday at 10 a.m.", "Monday at 10 a.m.", "Tuesday at 2 p.m.", "Friday at 9 a.m."], "on Tuesday at 10 a.m."),
 ("What should the listener bring?", ["An insurance card", "A passport", "A toothbrush", "Cash"], "Please bring your insurance card."))
B4X += S(P4, "Good morning, passengers. This is the 8:15 express train to Daejeon. Because of signal problems, we will leave about ten minutes late. The café car is in car number 4. We are sorry for the delay and thank you for traveling with Korea Rail.",
 ("Where is the announcement being made?", ["On a train", "On a plane", "At a bus stop", "On a ferry"], "express train, café car."),
 ("Why is the departure delayed?", ["Signal problems", "Bad weather", "A late passenger", "A staff shortage"], "Because of signal problems."),
 ("Where is the café car?", ["In car number 4", "In car number 1", "At the back of the train", "In car number 8"], "The café car is in car number 4."))
B4X += S(P4, "Hi, everyone. Before we start today's meeting, I have an announcement. Our company has just signed a contract with a large retail chain in Vietnam. This means we'll need to hire ten more people in the sales team. If you know someone who would be a good fit, please tell human resources.",
 ("What is the announcement about?", ["A new contract", "A new office", "A salary increase", "A company trip"], "signed a contract with a large retail chain."),
 ("What will the company need to do?", ["Hire more salespeople", "Close a store", "Move to Vietnam", "Cut costs"], "hire ten more people in the sales team."),
 ("What are listeners asked to do?", ["Recommend people to human resources", "Work on weekends", "Learn Vietnamese", "Sign a contract"], "If you know someone who would be a good fit, please tell human resources."))
B4X += S(P4, "You've reached the office of Baker and Sons Law Firm. Our office hours are Monday to Friday, 9 a.m. to 6 p.m. We are closed now. If this is an emergency, please press 1 to reach the lawyer on duty. Otherwise, leave a message after the tone.",
 ("What kind of business is this?", ["A law firm", "A bakery", "A bank", "A hospital"], "Baker and Sons Law Firm."),
 ("When is the office open?", ["Monday to Friday", "Every day", "Weekends only", "Monday to Saturday"], "Monday to Friday, 9 a.m. to 6 p.m."),
 ("What should a caller do in an emergency?", ["Press 1", "Call back tomorrow", "Send an email", "Visit the office"], "please press 1 to reach the lawyer on duty."))
B4X += S(P4, "Welcome to the City Science Museum. My name is Laura, and I'll show you around for the next hour. We'll start with the space exhibit and finish at the dinosaur hall. Photos are allowed, but please don't use a flash. The gift shop is next to the exit.",
 ("Who is the speaker?", ["A tour guide", "A scientist", "A shop clerk", "A photographer"], "I'll show you around."),
 ("How long is the tour?", ["One hour", "Thirty minutes", "Two hours", "All day"], "for the next hour."),
 ("What are visitors asked not to do?", ["Use a flash", "Take photos", "Talk loudly", "Touch the exhibits"], "please don't use a flash."))
B4X += S(P4, "This is a message for Ms. Cho. This is Peter from QuickFix Computers. Your laptop is ready. We replaced the screen and cleaned the keyboard. The total is 180 dollars. We're open until 7 p.m. today. Please bring your repair ticket when you come.",
 ("What was done to the laptop?", ["The screen was replaced.", "The battery was replaced.", "The memory was upgraded.", "A program was installed."], "We replaced the screen."),
 ("How much is the repair?", ["180 dollars", "80 dollars", "118 dollars", "280 dollars"], "The total is 180 dollars."),
 ("What should Ms. Cho bring?", ["Her repair ticket", "Her charger", "Her ID card", "A new keyboard"], "Please bring your repair ticket."))
B4X += S(P4, "And now for the traffic report. There's been an accident on Highway 5 near exit 12, and two lanes are closed. Drivers should expect delays of up to forty minutes. We recommend using Route 9 instead. We'll have another update in fifteen minutes.",
 ("What is the report mainly about?", ["A traffic accident", "The weather", "A new highway", "A bus strike"], "There's been an accident on Highway 5."),
 ("How long could the delays be?", ["Up to forty minutes", "Five minutes", "Fifteen minutes", "Two hours"], "delays of up to forty minutes."),
 ("What does the speaker recommend?", ["Using Route 9", "Taking the subway", "Staying home", "Leaving early tomorrow"], "We recommend using Route 9 instead."))
B4X += S(P4, "Thank you all for coming to Mr. Jensen's retirement party. Mr. Jensen has worked at our factory for thirty-two years, the last ten as plant manager. He plans to travel around Europe with his wife. Please join me in thanking him for his hard work.",
 ("What is the occasion?", ["A retirement party", "A wedding", "A product launch", "A birthday"], "Mr. Jensen's retirement party."),
 ("How long has Mr. Jensen worked at the factory?", ["Thirty-two years", "Ten years", "Twenty years", "Forty years"], "for thirty-two years."),
 ("What does Mr. Jensen plan to do?", ["Travel around Europe", "Start a business", "Write a book", "Move to the country"], "He plans to travel around Europe with his wife."))
B4X += S(P4, "Are you tired of slow internet? Switch to FiberNet today! For only 29 dollars a month, you get the fastest internet in the city. Sign up before June 30 and get the first month free. Call 555-7788 or visit our website.",
 ("What is being advertised?", ["An internet service", "A mobile phone", "A computer", "A TV channel"], "Switch to FiberNet... the fastest internet."),
 ("How much does the service cost per month?", ["29 dollars", "19 dollars", "39 dollars", "30 dollars"], "For only 29 dollars a month."),
 ("What do customers get if they sign up before June 30?", ["A free first month", "A free phone", "A 50 percent discount", "A free laptop"], "get the first month free."))
B4X += S(P4, "Good afternoon, everyone. This is your safety officer. Tomorrow at 10 a.m., we will have a fire drill for the whole building. When you hear the alarm, please use the stairs, not the elevators, and gather in the parking lot. The drill will take about fifteen minutes.",
 ("What will happen tomorrow at 10 a.m.?", ["A fire drill", "A staff meeting", "An elevator repair", "A power cut"], "we will have a fire drill."),
 ("What should people use during the drill?", ["The stairs", "The elevators", "The back door only", "Their cars"], "please use the stairs, not the elevators."),
 ("Where should people gather?", ["In the parking lot", "In the lobby", "On the roof", "In the cafeteria"], "gather in the parking lot."))
B4X += S(P4, "Hi, this is Angela Ruiz from Star Printing. I'm calling about your order of 500 business cards. We found a spelling mistake in the email address, so we stopped printing. Could you call me back to confirm the correct address? My number is 555-2020. We can still deliver by Thursday if we hear from you today.",
 ("What did the listener order?", ["Business cards", "Posters", "Envelopes", "Calendars"], "your order of 500 business cards."),
 ("What problem did the speaker find?", ["A spelling mistake", "A wrong color", "A missing logo", "A wrong price"], "a spelling mistake in the email address."),
 ("When can the order be delivered if the listener calls today?", ["By Thursday", "By Monday", "Today", "Next month"], "We can still deliver by Thursday."))
B4X += S(P4, "Welcome to tonight's cooking class. Today we're making fresh pasta. First, wash your hands and put on an apron. Each table has flour, eggs, and olive oil. If you have a food allergy, please tell me before we begin. At the end, we'll all eat together.",
 ("What will the listeners learn to make?", ["Fresh pasta", "Bread", "Pizza", "A cake"], "Today we're making fresh pasta."),
 ("What should the listeners do first?", ["Wash their hands", "Boil water", "Cut vegetables", "Read the recipe"], "First, wash your hands."),
 ("Who should speak to the instructor before the class begins?", ["People with a food allergy", "People without an apron", "People who arrived late", "People who paid in cash"], "If you have a food allergy, please tell me."))
B4X += S(P4, "Attention, passengers on Flight 208 to London. The departure gate has changed from gate 14 to gate 22. Boarding will begin at 3:40 p.m. Please have your passport and boarding pass ready. Passengers with small children may board first.",
 ("What has changed?", ["The departure gate", "The departure time", "The destination", "The airline"], "The departure gate has changed."),
 ("When does boarding begin?", ["At 3:40 p.m.", "At 2:08 p.m.", "At 2:20 p.m.", "At 4:30 p.m."], "Boarding will begin at 3:40 p.m."),
 ("Who may board first?", ["Passengers with small children", "Business travelers", "Passengers without bags", "Tour groups"], "Passengers with small children may board first."))
B4X += S(P4, "Good morning. Here's the business news. Carmaker Novo announced yesterday that it will open a new battery factory in Ulsan next year. The factory will create about 800 jobs. The company's stock price rose four percent after the news.",
 ("What did Novo announce?", ["A new factory", "A new car model", "A price cut", "A new president"], "it will open a new battery factory."),
 ("How many jobs will be created?", ["About 800", "About 80", "About 400", "About 8,000"], "about 800 jobs."),
 ("What happened to the company's stock price?", ["It rose four percent.", "It fell four percent.", "It did not change.", "It doubled."], "stock price rose four percent."))
B4X += S(P4, "Hello, and welcome to your first day at Bright Bank. I'm Helen from human resources. This morning, you'll get your ID cards and watch a short video about our company. After lunch, your team leaders will show you your desks. If you have any questions, my office is on the third floor.",
 ("Who are the listeners?", ["New employees", "Bank customers", "Team leaders", "Video producers"], "welcome to your first day at Bright Bank."),
 ("What will the listeners do this morning?", ["Get ID cards and watch a video", "Meet customers", "Open accounts", "Take a test"], "you'll get your ID cards and watch a short video."),
 ("Where is the speaker's office?", ["On the third floor", "On the first floor", "Next to the cafeteria", "In another building"], "my office is on the third floor."))
B4X += S(P4, "Thank you for calling Metro Water. We know that some homes in the Hillside area have no water this morning. A pipe broke last night, and our team is repairing it now. Water should return by 2 p.m. Free bottled water is available at the Hillside Community Center.",
 ("What is the problem?", ["Some homes have no water.", "The water is dirty.", "The bill is wrong.", "The office is closed."], "some homes ... have no water."),
 ("What caused the problem?", ["A broken pipe", "Heavy rain", "A power cut", "Road work"], "A pipe broke last night."),
 ("Where can people get free bottled water?", ["At the community center", "At the water company", "At City Hall", "At a supermarket"], "available at the Hillside Community Center."))
B4X += S(P4, "Ladies and gentlemen, the concert will begin in ten minutes. Please turn off your mobile phones and take your seats. Recording is not allowed during the performance. There will be a twenty-minute break after the first half. Enjoy the show.",
 ("When will the concert begin?", ["In ten minutes", "In twenty minutes", "In one hour", "Right now"], "will begin in ten minutes."),
 ("What is not allowed?", ["Recording", "Clapping", "Standing up", "Drinking water"], "Recording is not allowed."),
 ("How long is the break?", ["Twenty minutes", "Ten minutes", "Thirty minutes", "Five minutes"], "a twenty-minute break."))
B4X += S(P4, "Hi, team. A quick update on the mobile app project. Testing finished yesterday, and we found only three small bugs. The developers will fix them by Wednesday. That means we can launch the app on Friday as planned. Great work, everyone.",
 ("What project is the speaker talking about?", ["A mobile app", "A website", "A TV ad", "A new office"], "the mobile app project."),
 ("How many bugs were found?", ["Three", "Thirteen", "None", "Thirty"], "only three small bugs."),
 ("When will the app be launched?", ["On Friday", "On Wednesday", "Yesterday", "Next month"], "launch the app on Friday as planned."))
B4X += S(P4, "Good evening. Here is the weather for the weekend. Saturday will be cloudy with a high of 12 degrees. Heavy snow is expected on Sunday morning, so roads may be icy. If you must drive, please leave early and drive slowly.",
 ("What will the weather be like on Saturday?", ["Cloudy", "Sunny", "Rainy", "Snowy"], "Saturday will be cloudy."),
 ("What is expected on Sunday morning?", ["Heavy snow", "Strong wind", "Fog", "A heat wave"], "Heavy snow is expected on Sunday morning."),
 ("What does the speaker advise drivers to do?", ["Leave early and drive slowly", "Take the highway", "Stay in the left lane", "Use the bus lane"], "please leave early and drive slowly."))
B4X += S(P4, "Thank you for visiting Lakeside Furniture. This month, we're celebrating our tenth anniversary. Every sofa is 15 percent off, and delivery is free within the city. If you join our members' club today, you'll also receive a 20-dollar gift card.",
 ("What is the store celebrating?", ["Its tenth anniversary", "A new branch", "The new year", "Its first sale"], "our tenth anniversary."),
 ("What is 15 percent off?", ["Sofas", "Beds", "Tables", "Lamps"], "Every sofa is 15 percent off."),
 ("What do new club members receive?", ["A gift card", "A free sofa", "Free delivery for a year", "A catalog"], "you'll also receive a 20-dollar gift card."))
