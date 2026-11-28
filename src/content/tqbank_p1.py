# TOEIC bank, Part 1 additions from many settings (RYU 2026-11-25). Pictures: src/pics_b.py (same keys).
# Answer is always the FIRST choice; build.py shuffles.
P1 = "Part 1 · 사진 묘사"
_Q = [
 ("사진: 여자가 복사기를 사용하고 있다.", ["She's using a photocopier.", "She's fixing a computer.", "She's opening a window.", "She's carrying some paper."], "복사기를 사용하는 동작 = using a photocopier."),
 ("사진: 남자가 화이트보드에 글을 쓰고 있다.", ["He's writing on a whiteboard.", "He's cleaning a window.", "He's hanging a picture.", "He's reading a book."], "화이트보드에 쓰는 동작 = writing on a whiteboard."),
 ("사진: 사람들이 버스 정류장에서 기다리고 있다.", ["Some people are waiting at a bus stop.", "Some people are getting on a bus.", "Some people are crossing the road.", "Some people are sitting on a bench."], "버스는 없고 사람들이 서서 기다리는 장면입니다."),
 ("사진: 여자가 쇼핑 카트를 밀고 있다.", ["She's pushing a shopping cart.", "She's paying at a counter.", "She's putting items on a shelf.", "She's carrying a basket."], "카트를 미는 동작 = pushing a shopping cart."),
 ("사진: 남자가 상자를 들고 있다.", ["He's carrying a box.", "He's opening a box.", "He's stacking boxes on a shelf.", "He's driving a forklift."], "상자를 들고 있는 동작 = carrying a box."),
 ("사진: 자전거들이 건물 앞에 세워져 있다.", ["Some bicycles are parked in front of a building.", "Some people are riding bicycles.", "A bicycle is being repaired.", "Some bicycles are being loaded onto a truck."], "사람이 없고 자전거가 세워져 있는 상태입니다."),
 ("사진: 여자가 식물에 물을 주고 있다.", ["She's watering a plant.", "She's planting a tree.", "She's picking some flowers.", "She's washing a window."], "식물에 물을 주는 동작 = watering a plant."),
 ("사진: 남자가 사다리 위에 서 있다.", ["He's standing on a ladder.", "He's carrying a ladder.", "He's climbing some stairs.", "He's sitting on a stool."], "사다리 위에 서 있는 모습 = standing on a ladder."),
 ("사진: 책상 위에 서류가 쌓여 있다.", ["Some papers have been stacked on a desk.", "A man is filing some papers.", "Some papers are scattered on the floor.", "A desk is being moved."], "사람이 없으므로 상태(have been stacked)."),
 ("사진: 여자가 책장에서 책을 꺼내고 있다.", ["She's taking a book from a shelf.", "She's reading a newspaper.", "She's dusting a table.", "She's buying a magazine."], "책장에서 책을 꺼내는 동작."),
 ("사진: 남자가 벽에 페인트를 칠하고 있다.", ["He's painting a wall.", "He's hanging wallpaper.", "He's washing the floor.", "He's building a fence."], "벽을 칠하는 동작 = painting a wall."),
 ("사진: 회의실 탁자 둘레에 의자들이 놓여 있다.", ["Some chairs have been placed around a table.", "People are having a meeting.", "Some chairs are stacked in a corner.", "A table is being cleaned."], "사람이 없으므로 상태(have been placed)."),
 ("사진: 남자가 우산을 쓰고 걸어가고 있다.", ["He's holding an umbrella.", "He's closing an umbrella.", "He's buying an umbrella.", "He's waiting for a taxi."], "우산을 들고 있는 모습 = holding an umbrella."),
 ("사진: 트럭에 상자들이 실려 있다.", ["Some boxes have been loaded onto a truck.", "A man is unloading a truck.", "A truck is being washed.", "Some boxes are floating in the water."], "사람이 없으므로 상태(have been loaded)."),
]
B1X = [(P1, q, o, 0, w) for q, o, w in _Q]
