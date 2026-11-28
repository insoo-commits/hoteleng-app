# TOEIC bank, Part 7 additions from many fields (RYU 2026-11-25). Answer is always the FIRST choice; build.py shuffles.
def R7(kind, text, *qs):
    return [("Part 7 · " + kind, text + "\n\nQ. " + q, opts, 0, why) for q, opts, why in qs]

B7X = []
B7X += R7("공지", "NOTICE\nThe Elm Street Library will be closed from July 1 to July 14 while new carpets are installed. Books can be returned to the box outside the main door. No late fees will be charged during this time. The library will reopen on July 15 at 9 a.m.",
 ("Why will the library be closed?", ["New carpets are being installed.", "The staff are on vacation.", "The building is being sold.", "New books are arriving."], "while new carpets are installed."),
 ("Where can people return books during the closure?", ["In a box outside the main door", "At City Hall", "At another library", "By mail only"], "returned to the box outside the main door."),
 ("What is true about late fees?", ["They will not be charged during the closure.", "They will double.", "They must be paid online.", "They start on July 1."], "No late fees will be charged during this time."))
B7X += R7("이메일", "To: All employees\nFrom: IT Department\nSubject: Password change\n\nFor security reasons, all employees must change their email passwords by Friday, March 8. Your new password must have at least ten characters, including one number. If you do not change it in time, your account will be locked. For help, call extension 400.",
 ("What are employees asked to do?", ["Change their passwords", "Buy new computers", "Attend a meeting", "Delete old emails"], "must change their email passwords."),
 ("What is required for the new password?", ["At least ten characters", "Only numbers", "The employee's name", "Exactly eight letters"], "at least ten characters, including one number."),
 ("What happens if an employee misses the deadline?", ["The account will be locked.", "A fee will be charged.", "The password will be mailed.", "The computer will be replaced."], "your account will be locked."))
B7X += R7("문자 대화", "Dana (9:12): Are you at the office yet? The client just arrived.\nLeo (9:13): Not yet. My train is stuck between stations.\nDana (9:14): OK. I'll take her to the meeting room and get her some coffee.\nLeo (9:15): Thanks. I should be there in fifteen minutes. The samples are on my desk.",
 ("Why is Leo late?", ["His train is delayed.", "He overslept.", "He is at another meeting.", "His car broke down."], "My train is stuck between stations."),
 ("What will Dana do?", ["Take the client to the meeting room", "Cancel the meeting", "Pick Leo up", "Send the samples by mail"], "I'll take her to the meeting room."),
 ("Where are the samples?", ["On Leo's desk", "In the meeting room", "On the train", "At the client's office"], "The samples are on my desk."))
B7X += R7("후기", "★★★★★ Best vacuum I've owned\nI bought the CleanMax 300 two months ago. It's light, quiet, and strong enough to pick up pet hair from the carpet. The battery lasts about fifty minutes. My only complaint is that the dust box is small, so I have to empty it often. Still, I'd recommend it to anyone with pets.",
 ("What product is being reviewed?", ["A vacuum cleaner", "A washing machine", "A pet bed", "A carpet"], "Best vacuum I've owned."),
 ("How long does the battery last?", ["About fifty minutes", "About two hours", "About fifteen minutes", "About two months"], "The battery lasts about fifty minutes."),
 ("What does the reviewer NOT like?", ["The small dust box", "The noise", "The weight", "The price"], "My only complaint is that the dust box is small."))
B7X += R7("광고", "SPRING SALE at Urban Bikes\nMarch 20–31 only!\n- All city bikes: 25% off\n- Helmets: buy one, get one free\n- Free safety check for any bike bought from us\nOpen 10 a.m.–8 p.m. every day. Find us across from Lake Station, exit 3.",
 ("How long does the sale last?", ["From March 20 to 31", "All of March", "One weekend", "Until the end of spring"], "March 20–31 only!"),
 ("What is the offer on helmets?", ["Buy one, get one free", "25% off", "Free with any bike", "Half price"], "Helmets: buy one, get one free."),
 ("Where is the store?", ["Across from Lake Station", "Inside Lake Station", "Next to a park", "In a shopping mall"], "across from Lake Station, exit 3."))
B7X += R7("안내문", "HOW TO USE THE OFFICE COFFEE MACHINE\n1. Fill the water tank to the MAX line.\n2. Put a coffee capsule in the top slot.\n3. Place your cup under the nozzle and press the green button.\n4. Throw the used capsule in the recycling bin.\nIf the red light blinks, the machine needs cleaning. Please call the office manager.",
 ("What should a user do first?", ["Fill the water tank", "Press the green button", "Insert a capsule", "Call the office manager"], "1. Fill the water tank."),
 ("Where should used capsules go?", ["In the recycling bin", "In the water tank", "In the top slot", "On the desk"], "Throw the used capsule in the recycling bin."),
 ("What does a blinking red light mean?", ["The machine needs cleaning.", "The coffee is ready.", "The water is too hot.", "The capsule is empty."], "If the red light blinks, the machine needs cleaning."))
B7X += R7("메모", "MEMO\nTo: All department heads\nFrom: Rosa Diaz, Finance Director\nBudget requests for next year are due on October 15. Please use the new online form; paper forms will not be accepted. Requests for new equipment over 5,000 dollars must include two price quotes. I will hold a question-and-answer session on October 3 at 2 p.m. in room 501.",
 ("What is due on October 15?", ["Budget requests", "Price quotes for all items", "Paper forms", "Travel reports"], "Budget requests for next year are due on October 15."),
 ("How should requests be submitted?", ["Using an online form", "On paper", "By phone", "In person"], "Please use the new online form."),
 ("What is needed for equipment over 5,000 dollars?", ["Two price quotes", "The director's signature", "A photo of the equipment", "A meeting with Ms. Diaz"], "must include two price quotes."))
B7X += R7("일정표", "Sales Training Day — Friday, May 9\n09:00 Welcome and coffee\n09:30 Understanding our new products (Mr. Ito)\n11:00 Handling customer complaints (Ms. Park)\n12:30 Lunch (cafeteria, free)\n13:30 Role-play practice in small groups\n15:30 Quiz and closing\nPlease bring your laptop.",
 ("Who will speak about new products?", ["Mr. Ito", "Ms. Park", "The sales director", "A customer"], "Understanding our new products (Mr. Ito)."),
 ("What happens at 1:30 p.m.?", ["Role-play practice", "Lunch", "A quiz", "A product talk"], "13:30 Role-play practice in small groups."),
 ("What should participants bring?", ["A laptop", "Lunch", "A product sample", "A name tag"], "Please bring your laptop."))
B7X += R7("구인 광고", "WANTED: Office Assistant\nGreen Leaf Accounting is looking for a full-time office assistant.\n- Answer phones and greet visitors\n- Order office supplies\n- Good computer skills required\n- Hours: Mon–Fri, 9 a.m.–5 p.m.\n- Salary: 2,300 dollars per month plus health insurance\nEmail your resume to hr@greenleaf.example by April 20.",
 ("What kind of company placed the ad?", ["An accounting firm", "A flower shop", "A computer store", "A hospital"], "Green Leaf Accounting."),
 ("What is one duty of the job?", ["Ordering office supplies", "Repairing computers", "Visiting clients", "Preparing tax reports"], "Order office supplies."),
 ("What is included in addition to the salary?", ["Health insurance", "A company car", "Free lunch", "A laptop"], "plus health insurance."))
B7X += R7("영수증", "FRESH MART — Receipt\nDate: June 3, 18:42\nMilk 1L  2.50\nEggs (12)  3.80\nApples 1kg  4.20\nBread  2.00\nMembers' discount  -1.25\nTOTAL  11.25 dollars\nPaid: cash 20.00 / Change 8.75\nReturns accepted within 7 days with this receipt.",
 ("What was the most expensive item?", ["Apples", "Eggs", "Milk", "Bread"], "Apples 1kg 4.20이 가장 비쌉니다."),
 ("How did the customer pay?", ["In cash", "By credit card", "By mobile phone", "With a gift card"], "Paid: cash 20.00."),
 ("What is needed to return an item?", ["The receipt", "A member's card", "A photo ID", "The original bag"], "Returns accepted within 7 days with this receipt."))
B7X += R7("이메일", "Dear Mr. Olsen,\nThank you for your order of 40 office chairs (model K-12). Unfortunately, only 25 are in stock now. We can send these on Monday and the other 15 two weeks later. If you prefer to wait and receive them all at once, please let us know by Friday. We are sorry for the trouble and will take 5% off your total.\nSincerely,\nMina Seo, Comfort Office Supply",
 ("What did Mr. Olsen order?", ["Office chairs", "Desks", "Computers", "Bookshelves"], "your order of 40 office chairs."),
 ("How many chairs can be sent on Monday?", ["25", "15", "40", "12"], "only 25 are in stock now. We can send these on Monday."),
 ("What does the company offer because of the problem?", ["A 5% discount", "Free chairs", "Faster shipping", "A full refund"], "will take 5% off your total."))
B7X += R7("공지", "ATTENTION, RESIDENTS\nThe water will be turned off in Maple Apartments on Wednesday, April 16, from 10 a.m. to 3 p.m. Workers will replace old pipes in the basement. Please store enough water before that time and do not use the washing machines. If you have questions, call the management office at 555-0199.",
 ("What will happen on April 16?", ["The water will be turned off.", "The power will be cut.", "The elevator will be repaired.", "The basement will be painted."], "The water will be turned off."),
 ("Why is the work being done?", ["To replace old pipes", "To clean the water tank", "To install washing machines", "To fix the heating"], "Workers will replace old pipes."),
 ("What are residents asked to do?", ["Store water in advance", "Leave the building", "Move their cars", "Call a plumber"], "Please store enough water before that time."))
B7X += R7("문자 대화", "Amy (17:40): Did you book the restaurant for Friday's team dinner?\nBen (17:42): Yes, Luigi's at 7. A table for twelve.\nAmy (17:43): Oh, two more people from the Busan office are coming.\nBen (17:45): No problem. I'll call them now and change it to fourteen.",
 ("What is planned for Friday?", ["A team dinner", "A client meeting", "A trip to Busan", "A cooking class"], "Friday's team dinner."),
 ("What time is the reservation?", ["7 o'clock", "5:40", "12 o'clock", "2 o'clock"], "Luigi's at 7."),
 ("What will Ben do next?", ["Call the restaurant", "Cancel the dinner", "Email the Busan office", "Choose another restaurant"], "I'll call them now and change it to fourteen."))
B7X += R7("후기", "★★☆☆☆ Slow delivery, good product\nI ordered a pair of running shoes from SportsNow. The website said three days, but they took almost two weeks to arrive, and nobody answered my emails. The shoes themselves are comfortable and fit perfectly. I like the product, but I will probably buy from a local store next time.",
 ("What did the reviewer buy?", ["Running shoes", "A sports bag", "A bicycle", "A watch"], "a pair of running shoes."),
 ("What was the main problem?", ["The delivery was slow.", "The shoes were too small.", "The price was too high.", "The color was wrong."], "they took almost two weeks to arrive."),
 ("What will the reviewer probably do next time?", ["Buy from a local store", "Order from the same website", "Ask for a refund", "Buy a larger size"], "I will probably buy from a local store next time."))
B7X += R7("광고", "LEARN SPANISH IN 12 WEEKS!\nCity Language Center — evening classes for busy adults\n- Tuesdays and Thursdays, 7–9 p.m.\n- Maximum 10 students per class\n- Native-speaking teachers\n- Course fee: 360 dollars (books included)\nNew classes start September 2. Register online before August 20 and save 10%.",
 ("Who are the classes for?", ["Busy adults", "Children", "Spanish teachers", "University professors"], "evening classes for busy adults."),
 ("How often do the classes meet?", ["Twice a week", "Every day", "Once a week", "Once a month"], "Tuesdays and Thursdays."),
 ("How can students get a discount?", ["By registering before August 20", "By bringing a friend", "By paying in cash", "By buying the books"], "Register online before August 20 and save 10%."))
B7X += R7("안내문", "RETURN POLICY — Home Style Store\nYou may return most items within 30 days if they are unused and in the original box. Please bring your receipt. Refunds are made to the card you paid with. Sale items can be exchanged but not refunded. Sorry, we cannot accept returns of bedding or towels for health reasons.",
 ("How long do customers have to return items?", ["30 days", "7 days", "14 days", "One year"], "within 30 days."),
 ("What is true about sale items?", ["They can only be exchanged.", "They can be refunded in cash.", "They cannot be returned or exchanged.", "They have a longer return period."], "Sale items can be exchanged but not refunded."),
 ("Which item cannot be returned?", ["Towels", "Lamps", "Chairs", "Clocks"], "we cannot accept returns of bedding or towels."))
B7X += R7("메모", "To: Warehouse staff\nFrom: Paul Meyer, Operations Manager\nBeginning Monday, the morning shift will start at 6 a.m. instead of 7 a.m. because of the larger number of holiday orders. The shift will end one hour earlier, at 2 p.m. This schedule will continue until January 5. Free breakfast will be available in the break room from 5:30.",
 ("What is changing?", ["The start time of the morning shift", "The location of the warehouse", "The number of workers", "The lunch menu"], "the morning shift will start at 6 a.m. instead of 7 a.m."),
 ("Why is the change being made?", ["There are more holiday orders.", "The manager is on vacation.", "The trucks arrive later.", "The building opens late."], "because of the larger number of holiday orders."),
 ("What will be available from 5:30?", ["Free breakfast", "A shuttle bus", "New uniforms", "Extra pay"], "Free breakfast will be available in the break room from 5:30."))
B7X += R7("일정표", "Dr. Emily Shaw — Tuesday schedule\n08:30 Staff meeting\n09:00–12:00 Patient appointments\n12:00 Lunch with Dr. Kato (hospital café)\n13:30 Surgery, operating room 2\n16:00 Phone call with the insurance company\n17:00 Lecture to nursing students, room 110",
 ("What does Dr. Shaw do in the morning?", ["She sees patients.", "She performs surgery.", "She gives a lecture.", "She visits a café."], "09:00–12:00 Patient appointments."),
 ("Who will she have lunch with?", ["Dr. Kato", "Nursing students", "An insurance agent", "Her patients"], "Lunch with Dr. Kato."),
 ("Where is the lecture?", ["In room 110", "In operating room 2", "In the hospital café", "In the staff room"], "Lecture to nursing students, room 110."))
B7X += R7("구인 광고", "DELIVERY DRIVERS NEEDED\nFastBox is hiring part-time drivers for evenings and weekends.\n- You must be 21 or older and have your own car.\n- Earn 18 dollars an hour plus fuel costs.\n- Choose your own hours with our mobile app.\nApply at www.fastbox.example/jobs. Interviews are held every Wednesday.",
 ("What must applicants have?", ["Their own car", "A truck license", "A university degree", "Five years of experience"], "have your own car."),
 ("How much do drivers earn per hour?", ["18 dollars", "21 dollars", "12 dollars", "8 dollars"], "Earn 18 dollars an hour."),
 ("When are interviews held?", ["Every Wednesday", "Every weekend", "Every evening", "Once a month"], "Interviews are held every Wednesday."))
B7X += R7("영수증", "CITY PARKING — Receipt\nLocation: Main Street Garage\nEntry: 09:05  Exit: 14:35\nTime: 5 hours 30 minutes\nRate: 2 dollars per 30 minutes\nAmount: 22.00\nShopping discount (Star Mall): -4.00\nTotal paid: 18.00 dollars (card)",
 ("How long was the car parked?", ["Five and a half hours", "Two hours", "Nine hours", "Fourteen hours"], "Time: 5 hours 30 minutes."),
 ("Why did the driver get a discount?", ["For shopping at Star Mall", "For parking early", "For paying in cash", "For being a member"], "Shopping discount (Star Mall)."),
 ("How much did the driver pay?", ["18 dollars", "22 dollars", "4 dollars", "26 dollars"], "Total paid: 18.00 dollars."))
B7X += R7("이메일", "Hi Carla,\nI've looked at the photos for our new catalog. Most of them are great, but the ones of the kitchen tools are too dark. Could we take those again next Tuesday? The studio is free in the morning. Also, the printer needs the final files by the 20th, so we don't have much time.\nThanks,\nJoe",
 ("What is the problem with some photos?", ["They are too dark.", "They are too small.", "They show the wrong products.", "They were lost."], "the ones of the kitchen tools are too dark."),
 ("When does Joe want to take the photos again?", ["Next Tuesday", "Today", "On the 20th", "Next month"], "Could we take those again next Tuesday?"),
 ("What must happen by the 20th?", ["The printer must receive the final files.", "The studio must be cleaned.", "The catalog must be mailed.", "The tools must be returned."], "the printer needs the final files by the 20th."))
B7X += R7("공지", "RIVERDALE COMMUNITY CENTER\nFree Computer Classes for Seniors\nLearn how to send email, shop online, and make video calls. Classes meet every Monday from 10 a.m. to noon, starting February 3. No computer is needed; we provide laptops. Space is limited to 15 people. Sign up at the front desk.",
 ("Who are the classes for?", ["Seniors", "Children", "Computer engineers", "Shop owners"], "Free Computer Classes for Seniors."),
 ("What will participants learn?", ["How to send email", "How to repair laptops", "How to build websites", "How to sell computers"], "Learn how to send email."),
 ("How can people join?", ["By signing up at the front desk", "By calling the teacher", "By paying a fee online", "By bringing a laptop"], "Sign up at the front desk."))
B7X += R7("문자 대화", "Customer (11:02): Hi, my internet has been down since this morning.\nAgent (11:03): I'm sorry. Is the light on your modem red or green?\nCustomer (11:04): It's red.\nAgent (11:05): Please unplug the modem, wait thirty seconds, and plug it in again.\nCustomer (11:08): It's green now, and it's working. Thank you!",
 ("What is the customer's problem?", ["The internet is not working.", "The bill is too high.", "The phone is broken.", "The TV has no sound."], "my internet has been down."),
 ("What color was the modem light at first?", ["Red", "Green", "Blue", "Yellow"], "It's red."),
 ("What did the agent tell the customer to do?", ["Unplug the modem and plug it in again", "Buy a new modem", "Wait for a technician", "Call another number"], "unplug the modem, wait thirty seconds, and plug it in again."))
B7X += R7("후기", "★★★★☆ A helpful course\nI took the three-day Excel course at Smart Skills Academy. The teacher explained everything slowly and gave us real examples from business. By the last day, I could make charts and simple reports. The classroom was a little cold, and the course book cost extra. Overall, it was worth the money.",
 ("What did the reviewer study?", ["Excel", "English", "Photography", "Accounting law"], "the three-day Excel course."),
 ("What does the reviewer say about the teacher?", ["The teacher explained things slowly.", "The teacher was often late.", "The teacher spoke too fast.", "The teacher changed every day."], "The teacher explained everything slowly."),
 ("What was NOT included in the course price?", ["The course book", "The classroom", "The examples", "The charts"], "the course book cost extra."))
B7X += R7("광고", "MOVING? LET US HELP!\nStrong Arms Moving Company\n- Homes and offices, anywhere in the country\n- Free boxes and packing tape\n- Fully insured: we pay for anything we break\n- 10% off for moves on weekdays\nCall 555-6000 for a free price estimate. We answer 24 hours a day.",
 ("What service is advertised?", ["Moving", "Cleaning", "Insurance", "Box making"], "Strong Arms Moving Company."),
 ("What does the company give for free?", ["Boxes and tape", "A truck", "Furniture", "Storage for a year"], "Free boxes and packing tape."),
 ("When can customers get a discount?", ["On weekdays", "On weekends", "At night", "In winter"], "10% off for moves on weekdays."))
B7X += R7("안내문", "VISITOR INFORMATION — Hillman Factory Tour\nTours start at 10 a.m. and 2 p.m., Monday to Friday, and last 45 minutes. All visitors must wear closed shoes and the safety glasses we provide. Children under eight are not allowed on the factory floor. Photos may be taken only in the visitor center.",
 ("How long is a tour?", ["45 minutes", "Two hours", "10 minutes", "One day"], "last 45 minutes."),
 ("What must visitors wear?", ["Closed shoes", "A uniform", "Gloves", "A name tag"], "must wear closed shoes and the safety glasses."),
 ("Where can visitors take photos?", ["In the visitor center", "On the factory floor", "Everywhere", "Nowhere"], "Photos may be taken only in the visitor center."))
B7X += R7("메모", "To: All staff\nFrom: Office Management\nThe third-floor meeting rooms will get new video equipment next week. Rooms 3A and 3B will be closed on Monday and Tuesday. Please use the rooms on the fifth floor instead and book them through the online calendar. A short training on the new equipment will be given on Wednesday at 4 p.m.",
 ("What will be installed?", ["Video equipment", "New carpets", "Air conditioners", "Coffee machines"], "new video equipment."),
 ("Which rooms should staff use on Monday?", ["Rooms on the fifth floor", "Rooms 3A and 3B", "The cafeteria", "Rooms in another building"], "Please use the rooms on the fifth floor instead."),
 ("What will happen on Wednesday?", ["A training session", "A room closure", "A staff party", "A fire drill"], "A short training on the new equipment will be given on Wednesday."))
B7X += R7("일정표", "Flight Itinerary — Ms. Hana Jung\nMay 6  KE 901  Seoul (ICN) 13:20 → Paris (CDG) 18:30\nMay 6–9  Hotel Lumière, Paris\nMay 10  AF 1680  Paris (CDG) 09:15 → London (LHR) 09:40\nMay 12  KE 908  London (LHR) 19:35 → Seoul (ICN) 15:30 (+1 day)\nBaggage: 1 bag, 23 kg",
 ("Where does Ms. Jung go first?", ["Paris", "London", "Seoul", "Rome"], "Seoul → Paris가 첫 비행입니다."),
 ("When does she fly to London?", ["On May 10", "On May 6", "On May 9", "On May 12"], "May 10 Paris → London."),
 ("How much baggage can she check?", ["One bag of 23 kg", "Two bags", "No bags", "One bag of 32 kg"], "Baggage: 1 bag, 23 kg."))
B7X += R7("구인 광고", "JOIN OUR TEAM — Nurse (night shift)\nSt. Mary's Hospital has an opening for a registered nurse.\n- At least three years of hospital experience\n- Shift: 10 p.m.–6 a.m., four nights a week\n- Night-shift bonus and free parking\n- Start date: July 1\nTo apply, send your resume and license number to nursing@stmarys.example.",
 ("How much experience is required?", ["At least three years", "None", "One year", "Ten years"], "At least three years of hospital experience."),
 ("How many nights a week is the job?", ["Four", "Six", "Seven", "Two"], "four nights a week."),
 ("What benefit is mentioned?", ["Free parking", "Free housing", "A company phone", "Free meals"], "Night-shift bonus and free parking."))
B7X += R7("영수증", "TECH WORLD — Invoice No. 4471\nCustomer: Hill & Co.\n3 × Laser printer LP-20 @ 250.00  750.00\n10 × Ink cartridge @ 30.00  300.00\nDelivery  25.00\nSubtotal  1,075.00\nTax (10%)  107.50\nTOTAL DUE  1,182.50 dollars\nPayment due within 30 days.",
 ("How many printers were ordered?", ["Three", "Ten", "Twenty", "One"], "3 × Laser printer."),
 ("How much is the delivery charge?", ["25 dollars", "30 dollars", "107.50 dollars", "Free"], "Delivery 25.00."),
 ("When must the invoice be paid?", ["Within 30 days", "Immediately", "Within 10 days", "By the end of the year"], "Payment due within 30 days."))
B7X += R7("이메일", "Dear Ms. Foster,\nThis is to confirm your appointment with our tax advisor, Mr. Nam, on Thursday, February 12, at 3 p.m. Please bring last year's tax return and your salary statements. The first meeting is free and takes about 40 minutes. Our office is on the 6th floor of the Hanbit Building, above the bank.\nBest regards,\nClear Tax Services",
 ("What is the purpose of the email?", ["To confirm an appointment", "To send a bill", "To offer a job", "To cancel a meeting"], "This is to confirm your appointment."),
 ("What should Ms. Foster bring?", ["Last year's tax return", "Her passport", "A bank card", "A signed contract"], "Please bring last year's tax return."),
 ("How much does the first meeting cost?", ["It is free.", "40 dollars", "12 dollars", "It depends on the time."], "The first meeting is free."))
B7X += R7("공지", "CUSTOMER NOTICE — Bank of Hanul\nOur online and mobile banking services will not be available on Sunday, June 8, from midnight to 6 a.m. because of a system upgrade. ATMs will work as usual. After the upgrade, you will be able to log in with your fingerprint. We apologize for the inconvenience.",
 ("What will be unavailable on June 8?", ["Online and mobile banking", "ATMs", "All branches", "Credit cards"], "Our online and mobile banking services will not be available."),
 ("Why is the service stopping?", ["For a system upgrade", "For a holiday", "Because of a power cut", "Because of a move"], "because of a system upgrade."),
 ("What new feature will be added?", ["Fingerprint login", "Free transfers", "A new card design", "Longer branch hours"], "you will be able to log in with your fingerprint."))
B7X += R7("문자 대화", "Mom (15:20): Can you pick up some milk on your way home?\nJake (15:22): Sure. Anything else?\nMom (15:23): Eggs, if they're on sale. And Grandma is coming for dinner at 6:30.\nJake (15:24): OK. My class ends at 5, so I'll be home before 6.",
 ("What does Mom ask Jake to buy?", ["Milk", "Bread", "Rice", "Juice"], "Can you pick up some milk?"),
 ("Who is coming for dinner?", ["Grandma", "Jake's teacher", "A neighbor", "Jake's friend"], "Grandma is coming for dinner."),
 ("When does Jake's class end?", ["At 5", "At 6", "At 6:30", "At 3:20"], "My class ends at 5."))
B7X += R7("후기", "★★★☆☆ Nice café, but too noisy\nBean House has excellent coffee and the best cheesecake in town. Prices are fair, and the staff remember your name. However, the tables are very close together, and the music is loud. It is not a good place to study or have a meeting. I go there only to take coffee out.",
 ("What does the reviewer praise?", ["The coffee and cheesecake", "The quiet atmosphere", "The large tables", "The music"], "excellent coffee and the best cheesecake in town."),
 ("What is the reviewer's complaint?", ["It is noisy.", "It is expensive.", "The staff are rude.", "The coffee is weak."], "the music is loud."),
 ("How does the reviewer usually use the café?", ["For takeout coffee", "For studying", "For meetings", "For lunch"], "I go there only to take coffee out."))
B7X += R7("광고", "SUNSHINE CAR RENTAL\nWeekend special: rent any small car from Friday 6 p.m. to Monday 9 a.m. for only 99 dollars!\n- Unlimited kilometers\n- Insurance included\n- Child seats available for 5 dollars a day\nDrivers must be 23 or older with a license held for at least one year. Book online or at our airport desk.",
 ("How much is the weekend special?", ["99 dollars", "5 dollars a day", "23 dollars", "199 dollars"], "for only 99 dollars!"),
 ("What costs extra?", ["A child seat", "Insurance", "Extra kilometers", "Booking online"], "Child seats available for 5 dollars a day."),
 ("Who can rent a car?", ["Drivers aged 23 or older", "Anyone with a passport", "Drivers aged 18 or older", "Only airport passengers"], "Drivers must be 23 or older."))
B7X += R7("안내문", "RECYCLING GUIDE — Oak Hill Apartments\n- Paper and boxes: blue bin (flatten boxes first)\n- Plastic bottles and cans: yellow bin (rinse them)\n- Glass: green bin\n- Food waste: brown bin, collected every day\nRecycling trucks come on Tuesdays and Fridays at 7 a.m. Please do not leave bags outside the bins.",
 ("Which bin is for paper?", ["The blue bin", "The yellow bin", "The green bin", "The brown bin"], "Paper and boxes: blue bin."),
 ("What should residents do with plastic bottles?", ["Rinse them", "Flatten them", "Break them", "Put them in bags"], "yellow bin (rinse them)."),
 ("How often is food waste collected?", ["Every day", "Twice a week", "Once a week", "Every Tuesday"], "Food waste: brown bin, collected every day."))
B7X += R7("메모", "MEMO\nTo: All teachers\nFrom: Principal Adams\nParent-teacher meetings will be held on Thursday, November 20, from 4 to 8 p.m. Each meeting is 15 minutes long. Parents will book times online starting next Monday. Please prepare a short report on each student. Dinner will be provided in the teachers' lounge at 6 p.m.",
 ("What event is the memo about?", ["Parent-teacher meetings", "A school festival", "A staff party", "Final exams"], "Parent-teacher meetings will be held."),
 ("How long is each meeting?", ["15 minutes", "One hour", "Four hours", "30 minutes"], "Each meeting is 15 minutes long."),
 ("What should teachers prepare?", ["A report on each student", "Dinner", "An online calendar", "A class schedule"], "Please prepare a short report on each student."))
B7X += R7("일정표", "Grand Opening Week — Pine Mall\nMon: Ribbon cutting at 10 a.m., free coffee for the first 200 visitors\nTue: Kids' painting contest, 2 p.m.\nWed: Fashion show, 6 p.m., center stage\nThu: Cooking show with Chef Romano, 3 p.m.\nFri–Sun: 30% off at all stores, live music every evening",
 ("What happens on Monday?", ["A ribbon cutting", "A fashion show", "A cooking show", "A painting contest"], "Mon: Ribbon cutting at 10 a.m."),
 ("When is the fashion show?", ["Wednesday at 6 p.m.", "Tuesday at 2 p.m.", "Thursday at 3 p.m.", "Monday at 10 a.m."], "Wed: Fashion show, 6 p.m."),
 ("What is offered from Friday to Sunday?", ["30% off at all stores", "Free coffee", "Free parking", "A cooking class"], "Fri–Sun: 30% off at all stores."))
B7X += R7("구인 광고", "SUMMER JOBS at Lakeview Amusement Park\nWe need 40 friendly people for ticket sales, food stands, and ride operation from June 15 to August 31.\n- Age 18 or older\n- Free uniform and one free meal per shift\n- Free park tickets for your family\nCome to our job fair on May 10, 10 a.m.–3 p.m., at the park's main gate.",
 ("When does the job period end?", ["August 31", "June 15", "May 10", "September 30"], "from June 15 to August 31."),
 ("What do workers receive for free?", ["A uniform", "A car", "A phone", "Housing"], "Free uniform and one free meal per shift."),
 ("How can people apply?", ["By going to a job fair", "By sending an email", "By calling the park", "By visiting a website"], "Come to our job fair on May 10."))
B7X += R7("영수증", "BOOKWORLD ONLINE — Order Confirmation\nOrder date: Oct 2\n1 × 'Business English Basics'  18.00\n2 × 'TOEIC Vocabulary 1000' @ 12.00  24.00\nShipping (standard, 3–5 days)  4.00\nCoupon WELCOME10  -4.20\nTotal charged to card  41.80 dollars\nDeliver to: 14 Garden Road",
 ("How many books were ordered in total?", ["Three", "Two", "One", "Four"], "1권 + 2권 = 3권."),
 ("How long will standard shipping take?", ["3 to 5 days", "One day", "Two weeks", "10 days"], "Shipping (standard, 3–5 days)."),
 ("What lowered the total price?", ["A coupon", "Free shipping", "A student discount", "A gift card"], "Coupon WELCOME10 -4.20."))
B7X += R7("이메일", "Dear customer,\nThank you for shopping at Garden Tools Direct. Your lawn mower (order 7731) was sent today and should reach you by Thursday. The driver will call you one hour before delivery. Please check the box when it arrives; if anything is damaged, send us a photo within 48 hours and we will replace it for free.\nCustomer Care Team",
 ("What was ordered?", ["A lawn mower", "A garden chair", "A water hose", "A tool box"], "Your lawn mower (order 7731)."),
 ("What will the driver do before delivery?", ["Call the customer", "Send a photo", "Email the invoice", "Check the box"], "The driver will call you one hour before delivery."),
 ("What should the customer do if the item is damaged?", ["Send a photo within 48 hours", "Return it to the store", "Call the driver", "Pay for the repair"], "send us a photo within 48 hours."))
