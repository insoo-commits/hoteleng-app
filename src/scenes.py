# Bundle pictures (RYU 2026-11-24: "학습목표 칸의 좌측에 현재 묶음의 대화와 관련 있는 간단한 그림").
# One flat drawing per kind of scene (front desk, restaurant, interview …), made with the helpers of pics.py;
# RULES picks the scene of a bundle from "menu|sub|title" (first match wins).
import re
from pics import PICS, svg, r, c, ln, person, suitcase, cart, floor, desk, bed, towel, glass, bottle, set_table, chair, lounger, W, H, INK, SKIN

def t(x, y, s, size=13, fill="#f3e2b3", anchor="middle", extra=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-family="sans-serif" {extra}>{s}</text>'
def wall(col="#e6ded2", fl="#cdbfa9", y=205): return r(0, 0, W, y, col) + floor(y, fl)
def window(x, y, w=70, h=90): return r(x, y, w, h, "#d9e6ea", 3, 'stroke="#b8a888" stroke-width="4"')
def plant(x, y): return r(x, y, 34, 55, "#7d9b76", 6) + c(x + 17, y - 10, 22, "#6e9a64")
def counter(x, y, w, h=100): return r(x, y, w, h, "#8a6a4a", 4) + r(x - 6, y - 8, w + 12, 12, "#a5825c", 3) + r(x + 20, y + 20, w - 40, 4, "#7a5a3a")
def bubble(x, y, s, w=46, col="#ffffff"):
    # RYU 2026-11-24: a bubble never covers a head: move it up, or sideways when there is no room above
    import pics as _P
    for hx, hy, hr in list(_P.HEADS):
        if hx + hr > x - 8 and hx - hr < x + w + 8 and hy - hr < y + 42 and hy + hr > y:
            ny = hy - hr - 42
            if ny >= 2: y = ny
            else:
                y = max(2, y)
                x = hx + hr + 10 if hx < x + w / 2 else hx - hr - w - 10
                x = min(max(10, x), 400 - w - 10)
    return f'<path d="M{x},{y} h{w} a8,8 0 0 1 8,8 v14 a8,8 0 0 1 -8,8 h-{w-16} l-10,10 l2,-10 h-8 a8,8 0 0 1 -8,-8 v-14 a8,8 0 0 1 8,-8 z" fill="{col}" stroke="{INK}" stroke-width="1.5"/>' + t(x + w / 2, y + 20, s, 14, INK, extra='font-weight="700"')
def cup(x, y, col="#ffffff"): return r(x - 9, y - 16, 18, 16, col, 3, f'stroke="{INK}" stroke-width="1.2"') + f'<path d="M{x+9},{y-12} q8,0 0,8" stroke="{INK}" stroke-width="1.5" fill="none"/>'
def sign(x, y, w, s, col="#2f4f66"): return r(x, y, w, 26, col, 3) + t(x + w / 2, y + 18, s, 13, "#f3e2b3", extra='letter-spacing="3"')
def car(x, y, col, roof=None):
    return "".join([r(x, y, 190, 44, col, 12), f'<path d="M{x+36},{y} l18,-34 h74 l22,34 z" fill="{col}"/>', f'<path d="M{x+48},{y-2} l12,-26 h28 v26 z" fill="#b9d3e0"/>', f'<path d="M{x+94},{y-2} v-26 h30 l16,26 z" fill="#b9d3e0"/>',
                    c(x + 44, y + 44, 15, INK), c(x + 146, y + 44, 15, INK), c(x + 44, y + 44, 6, "#9a9a9a"), c(x + 146, y + 44, 6, "#9a9a9a"), roof or ""])

STAFF, STAFF2, GUEST, GUEST2 = "#2f4f66", "#24323f", "#b55d4c", "#3b4a5a"
HAIR, HAIR2 = "#2b1d16", "#4a3426"
S = {}
# ---- scenes taken from the TOEIC Part 1 drawings
for k, q in [("frontdesk", "사진: 여자가 프런트 데스크에서 카드키를 건네고 있다."), ("handshake", "사진: 두 사람이 로비에서 악수하고 있다."), ("phone", "사진: 남자가 전화 통화를 하고 있다."),
             ("laptop", "사진: 남자가 책상에서 노트북으로 타이핑하고 있다."), ("pour", "사진: 여자가 잔에 물을 따르고 있다."), ("tables", "사진: 빈 레스토랑에 테이블마다 접시와 잔이 놓여 있다."),
             ("buffet", "사진: 뷔페 테이블 위에 과일 접시들이 줄지어 놓여 있다."), ("towels", "사진: 침대 위에 수건이 개어져 있다."), ("vacuum", "사진: 여자가 진공청소기로 바닥을 청소하고 있다."),
             ("map", "사진: 남자가 지도를 보고 있다."), ("bus", "사진: 버스가 호텔 앞에 서 있다."), ("travel", "사진: 여자가 여행 가방을 끌고 걸어가고 있다."),
             ("bellcart", "사진: 벨맨이 짐 카트에 가방을 싣고 있다."), ("chef", "사진: 요리사가 프라이팬으로 요리하고 있다."), ("wine", "사진: 선반에 와인병들이 진열되어 있다."),
             ("pool", "사진: 수영장 옆에 선베드가 줄지어 놓여 있다."), ("sign", "사진: 엘리베이터 옆에 안내 표지판이 서 있다."), ("room", "사진: 남자가 객실 창문의 커튼을 열고 있다.")]:
    S[k] = PICS[q]

# ---- new scenes
S["interview"] = svg("".join([wall("#e6e2da", "#c9c0b2", 200), window(30, 30, 80, 70), r(150, 24, 100, 60, "#ffffff", 3, 'stroke="#8a8a8a" stroke-width="3"'), ln([(164, 66), (186, 48), (204, 58), (236, 38)], "#5b7fa6", 3),
    person(130, 206, STAFF, STAFF2, HAIR, arms=[[(0, 0), (10, 26), (24, 34)]]), person(215, 206, "#6d6d6d", STAFF2, HAIR2, female=True, arms=[[(0, 0), (-10, 26), (-22, 34)]]),
    r(60, 140, 230, 90, "#8a6a4a", 4), r(54, 132, 242, 12, "#a5825c", 3), r(120, 122, 34, 10, "#ffffff", 1, f'stroke="{INK}" stroke-width="1"'), r(196, 118, 40, 14, "#3d4a55", 2),
    person(330, 262, "#e9a15b", GUEST2, HAIR, back=True), bubble(246, 60, "Q?", 40)]))
S["greet"] = svg("".join([wall(), window(30, 40, 60, 110), plant(330, 150), c(330, 50, 22, "#f6c453"),
    person(150, 232, "#5b7fa6", GUEST2, HAIR, arms=[[(0, 0), (16, -10), (30, -34)], [(0, 0), (-6, 30), (-6, 44)]]),
    person(250, 232, "#c25e4f", GUEST2, HAIR2, female=True, arms=[[(0, 0), (-16, -10), (-30, -34)], [(0, 0), (6, 30), (6, 44)]]), bubble(176, 30, "Hi!", 40)]))
S["checkout"] = svg("".join([wall(), sign(70, 20, 260, "CASHIER"), person(150, 210, STAFF, STAFF2, HAIR, female=True, arms=[[(0, 0), (30, 20), (56, 22)]]),
    counter(40, 140, 320), r(196, 112, 30, 22, "#3d4a55", 3), r(200, 100, 22, 14, "#ffffff", 1, f'stroke="{INK}" stroke-width="1"'), r(250, 116, 40, 22, "#fdfaf3", 1, f'stroke="{INK}" stroke-width="1"'), ln([(256, 123), (284, 123)], "#9aa7b1", 2), ln([(256, 130), (276, 130)], "#9aa7b1", 2),
    person(300, 262, GUEST, GUEST2, HAIR2, arms=[[(0, 0), (-30, 14), (-54, 6)]], back=True), r(232, 100, 24, 15, "#e8b23b", 2), suitcase(336, 196, 40, 56, "#5b7fa6")]))
S["complaint"] = svg("".join([wall(), sign(70, 20, 260, "RECEPTION"), person(140, 210, STAFF, STAFF2, HAIR, female=True, arms=[[(0, 0), (16, 22), (30, 30)], [(0, 0), (-14, 22), (-26, 30)]]),
    counter(40, 140, 320), person(290, 262, GUEST, GUEST2, HAIR2, arms=[[(0, 0), (-26, -6), (-44, -26)]], back=True),
    ln([(318, 96), (330, 84)], "#e85d4a", 4), ln([(326, 106), (342, 100)], "#e85d4a", 4), ln([(306, 90), (310, 74)], "#e85d4a", 4), bubble(182, 58, "Sorry", 60)]))
S["reservation"] = svg("".join([wall("#e6e2da", "#c9c0b2", 200), r(40, 30, 110, 96, "#ffffff", 4, 'stroke="#8a8a8a" stroke-width="3"'), r(40, 30, 110, 22, "#c25e4f", 4),
    "".join(r(52 + (i % 5) * 19, 62 + (i // 5) * 20, 12, 12, "#e85d4a" if i == 7 else "#dfe6ea", 2) for i in range(15)),
    desk(210, 160, 160), r(240, 148, 56, 12, "#3d4a55", 2), '<path d="M244,148 L254,110 L304,110 L298,148 Z" fill="#56646f"/>',
    person(200, 232, STAFF, STAFF2, HAIR, female=True, arms=[[(0, 0), (24, 24), (50, 28)], [(0, 0), (14, 4), (4, -16)]]), r(211, 88, 8, 24, INK, 3), c(219, 108, 5.5, SKIN)]))
S["concierge"] = svg("".join([wall(), sign(110, 20, 180, "CONCIERGE"), person(140, 210, STAFF, STAFF2, HAIR, arms=[[(0, 0), (30, 14), (60, 6)]]),
    counter(40, 140, 320), r(200, 96, 70, 46, "#fdfaf3", 2, f'stroke="{INK}" stroke-width="1.5"'), ln([(208, 106), (230, 126), (262, 110)], "#e85d4a", 2), ln([(214, 134), (250, 102)], "#7cbf5a", 2), c(246, 114, 4, "#e85d4a"),
    person(310, 262, "#6d8c5e", GUEST2, HAIR2, female=True, back=True)]))
S["restaurant"] = svg("".join([r(0, 0, W, 180, "#efe4d2"), floor(180, "#b89a76"), window(300, 30, 70, 90),
    person(120, 232, "#ffffff", "#24323f", HAIR, arms=[[(0, 0), (26, 10), (44, 6)], [(0, 0), (10, 30), (8, 44)]]), r(160, 100, 26, 34, "#fdfaf3", 2, f'stroke="{INK}" stroke-width="1.5"'), ln([(165, 110), (181, 110)], "#9aa7b1", 2), ln([(165, 118), (181, 118)], "#9aa7b1", 2),
    set_table(270, 176), person(330, 240, GUEST, GUEST2, HAIR2, female=True, arms=[[(0, 0), (-24, 20), (-40, 26)]], scale=0.9)]))
S["roomservice"] = svg("".join([wall("#e9e2d6", "#b9a58c", 200), r(230, 30, 110, 170, "#8a6a4a", 3), r(240, 40, 90, 150, "#a5825c", 2), c(248, 120, 5, "#e8b23b"), r(270, 56, 30, 16, "#f3e2b3", 2), t(285, 68, "1205", 10, INK),
    person(140, 232, STAFF, STAFF2, HAIR, arms=[[(0, 0), (30, 14), (56, 10)], [(0, 0), (-6, 30), (-6, 44)]]),
    '<ellipse cx="204" cy="118" rx="34" ry="5" fill="#c3cbd0"/>', '<path d="M178,116 a26,22 0 0 1 52,0 z" fill="#dfe6ea" stroke="#9fb3c1" stroke-width="2"/>', c(204, 92, 4, "#9fb3c1")]))
S["bar"] = svg("".join([r(0, 0, W, 200, "#3b3440"), floor(200, "#5a4636"), r(40, 30, 320, 8, "#a5825c"), "".join(bottle(64 + j * 36, 30, ["#6a1f2b", "#2f5a3a", "#c9a34a", "#5b7fa6"][j % 4]) for j in range(9)),
    person(200, 212, "#ffffff", "#24323f", HAIR, arms=[[(0, 0), (26, 4), (40, -14)], [(0, 0), (-22, 16), (-34, 24)]]), r(234, 86, 14, 26, "#c3cbd0", 4),
    counter(30, 150, 340, 90), '<path d="M120,112 l28,0 l-14,20 z" fill="#f2a65a" stroke="#ffffff" stroke-width="1.5"/>', ln([(134, 132), (134, 146)], "#ffffff", 2), ln([(126, 146), (142, 146)], "#ffffff", 2), glass(290, 146)]))
S["cafe"] = svg("".join([r(0, 0, W, 200, "#efe4d2"), floor(200, "#b89a76"), r(40, 24, 150, 64, "#3d4a55", 4), t(115, 48, "COFFEE", 13, "#ffffff", extra='letter-spacing="2"'), ln([(60, 62), (170, 62)], "#9aa7b1", 2), ln([(60, 74), (150, 74)], "#9aa7b1", 2),
    person(250, 212, "#6d8c5e", "#24323f", HAIR, female=True, arms=[[(0, 0), (-30, 16), (-56, 16)]]), counter(30, 150, 340, 90),
    r(300, 96, 44, 54, "#56646f", 4), r(310, 126, 24, 6, "#3d4a55"), cup(180, 144), ln([(176, 118), (180, 108)], "#b8a888", 2), ln([(184, 118), (188, 106)], "#b8a888", 2), cup(110, 144, "#f3e2b3")]))
S["banquet"] = svg("".join([r(0, 0, W, 170, "#e9e2f0"), floor(170, "#b9a5c0"), r(120, 20, 160, 80, "#ffffff", 3, 'stroke="#8a8a8a" stroke-width="3"'), t(200, 66, "WELCOME", 16, "#5b4a7a", extra='letter-spacing="3" font-weight="700"'),
    "".join('<ellipse cx="%d" cy="%d" rx="52" ry="14" fill="#ffffff" stroke="#d3cfc6" stroke-width="2"/>' % (x, y) + r(x - 4, y + 2, 8, 34, "#d3cfc6") + c(x, y - 8, 7, "#e85d4a") + c(x - 5, y - 13, 5, "#f6c453") + r(x - 1, y - 6, 2, 8, "#6e9a64")
            + "".join(c(x + dx, y + 2, 5, "#dfe6ea", 'stroke="#9fb3c1" stroke-width="1"') for dx in (-34, -17, 17, 34)) for x, y in [(90, 196), (210, 216), (320, 192)]),
    person(52, 168, STAFF, STAFF2, HAIR, scale=0.7, arms=[[(0, 0), (20, 14), (36, 12)]])]))
S["meeting"] = svg("".join([wall("#e6e2da", "#c9c0b2", 200), r(150, 24, 200, 110, "#ffffff", 3, 'stroke="#8a8a8a" stroke-width="3"'), "".join(r(176 + i * 34, 112 - h, 20, h, col) for i, (h, col) in enumerate([(28, "#9fb3c1"), (44, "#9fb3c1"), (38, "#9fb3c1"), (66, "#5b7fa6"), (76, "#e8743b")])), ln([(176, 80), (220, 62), (256, 68), (322, 34)], "#e85d4a", 2.5),
    person(100, 232, STAFF, STAFF2, HAIR, female=True, arms=[[(0, 0), (30, -10), (56, -30)], [(0, 0), (-6, 30), (-6, 44)]]),
    person(250, 268, "#6d6d6d", GUEST2, HAIR2, back=True, scale=0.9), person(330, 268, GUEST, GUEST2, HAIR, back=True, scale=0.9)]))
S["repair"] = svg("".join([wall("#e9e2d6", "#b9a58c", 200), r(190, 30, 150, 44, "#ffffff", 6, 'stroke="#c9ced2" stroke-width="3"'), "".join(ln([(204, 54 + i * 6), (326, 54 + i * 6)], "#c9ced2", 2) for i in range(3)), c(322, 42, 3, "#e85d4a"),
    r(214, 150, 76, 82, "#c3cbd0", 2), r(206, 144, 92, 8, "#9aa3a9", 2), ln([(224, 152), (224, 232)], "#9aa3a9", 3), ln([(280, 152), (280, 232)], "#9aa3a9", 3), ln([(224, 176), (280, 176)], "#9aa3a9", 3), ln([(224, 204), (280, 204)], "#9aa3a9", 3),
    person(250, 150, "#e8b23b", "#3b4a5a", HAIR, arms=[[(0, 0), (10, -24), (18, -46)], [(0, 0), (-12, -20), (-10, -42)]], cap="#e8743b", scale=0.9),
    r(60, 196, 60, 34, "#c25e4f", 4), r(78, 186, 24, 12, "#c25e4f", 3), ln([(120, 150), (140, 190)], "#56646f", 5)]))
S["laundry"] = svg("".join([wall("#e9e2d6", "#b9a58c", 200), ln([(40, 36), (360, 36)], "#8a8a8a", 4),
    "".join(ln([(x, 36), (x, 50)], "#8a8a8a", 3) + f'<path d="M{x-26},{56} l26,-8 l26,8 l-8,10 v60 h-36 v-60 z" fill="{col}"/>' for x, col in [(90, "#ffffff"), (170, "#5b7fa6"), (250, "#c25e4f")]),
    person(330, 232, "#7a8a96", "#2c3a48", HAIR, female=True, arms=[[(0, 0), (-26, 20), (-46, 26)], [(0, 0), (-20, 30), (-40, 38)]]), r(244, 150, 60, 20, "#ffffff", 3, 'stroke="#d3cfc6" stroke-width="2"'), r(244, 168, 60, 14, "#cfe3ee", 3)]))
S["lostfound"] = svg("".join([wall(), sign(100, 20, 200, "LOST &amp; FOUND"), r(60, 70, 280, 8, "#a5825c"), r(60, 130, 280, 8, "#a5825c"),
    r(80, 46, 30, 24, "#c25e4f", 4), r(130, 52, 40, 18, "#3d4a55", 3), c(200, 58, 12, "#e8b23b"), r(240, 40, 14, 30, "#5b7fa6", 3), r(290, 50, 34, 20, "#6d8c5e", 4),
    r(84, 108, 44, 22, "#5b7fa6", 4), '<path d="M160,130 q14,-40 28,0 z" fill="#3b4a5a"/>', ln([(174, 96), (174, 86)], "#3b4a5a", 3), r(220, 112, 26, 18, "#f3e2b3", 2), r(270, 104, 40, 26, "#8a6a4a", 4),
    person(200, 250, STAFF, STAFF2, HAIR, female=True, arms=[[(0, 0), (30, 6), (52, -10)], [(0, 0), (-6, 30), (-6, 44)]], scale=0.85)]))
S["fitness"] = svg("".join([wall("#e3e7e9", "#b8bfc4", 200), window(30, 30, 120, 90),
    r(210, 196, 150, 12, "#3d4a55", 4), ln([(350, 196), (336, 110)], "#56646f", 6), r(310, 100, 50, 16, "#3d4a55", 4), ln([(336, 130), (300, 150)], "#56646f", 4),
    person(270, 196, "#e8743b", "#24323f", HAIR, arms=[[(0, 0), (22, 14), (36, 6)], [(0, 0), (-14, 20), (-4, 34)]], lean=5),
    r(60, 214, 60, 8, "#56646f", 3), r(52, 204, 12, 28, INK, 3), r(116, 204, 12, 28, INK, 3), c(160, 220, 16, "#5b7fa6")]))
S["spa"] = svg("".join([r(0, 0, W, 200, "#e8efe6"), floor(200, "#c2cdb8"), r(80, 150, 240, 16, "#ffffff", 6, 'stroke="#d3cfc6" stroke-width="2"'), r(100, 166, 10, 50, "#8a6a4a"), r(290, 166, 10, 50, "#8a6a4a"),
    r(110, 132, 180, 20, "#cfe3ee", 8), c(104, 136, 13, SKIN), f'<path d="M92,134 q12,-18 24,0 z" fill="{HAIR}"/>',
    person(330, 232, "#ffffff", "#7a8a96", HAIR2, female=True, arms=[[(0, 0), (-26, 12), (-48, 16)], [(0, 0), (-20, 22), (-40, 22)]]),
    r(40, 176, 26, 40, "#8a6a4a", 3), c(53, 166, 8, "#f6c453"), ln([(53, 158), (53, 150)], "#e8743b", 3), plant(20, 80)]))
S["kids"] = svg("".join([wall("#fdf3d6", "#e3c98f", 200), "".join(c(40 + i * 60, 30, 10, col) for i, col in enumerate(["#e85d4a", "#f6c453", "#7cbf5a", "#5b7fa6", "#c58ad0", "#e8743b"])),
    r(60, 190, 34, 34, "#e85d4a", 4), r(96, 190, 34, 34, "#5b7fa6", 4), r(78, 156, 34, 34, "#f6c453", 4), t(77, 213, "A", 18, "#ffffff", extra='font-weight="700"'), t(113, 213, "B", 18, "#ffffff", extra='font-weight="700"'), t(95, 179, "C", 18, INK, extra='font-weight="700"'),
    person(200, 232, "#7cbf5a", "#3b4a5a", HAIR, scale=0.7, arms=[[(0, 0), (20, -6), (34, -24)], [(0, 0), (-18, 10), (-30, 4)]]), c(240, 150, 14, "#e85d4a"),
    person(310, 232, STAFF, STAFF2, HAIR2, female=True, arms=[[(0, 0), (-24, 14), (-44, 12)], [(0, 0), (6, 30), (6, 44)]])]))
S["emergency"] = svg("".join([wall(), r(40, 30, 70, 70, "#ffffff", 6, 'stroke="#c9ced2" stroke-width="3"'), r(66, 44, 18, 42, "#e85d4a"), r(54, 56, 42, 18, "#e85d4a"),
    r(300, 60, 44, 90, "#e85d4a", 8), r(312, 46, 20, 16, "#3d4a55", 3), ln([(332, 54), (350, 70)], INK, 4), r(304, 92, 36, 14, "#ffffff", 2),
    person(160, 232, STAFF, STAFF2, HAIR, female=True, arms=[[(0, 0), (16, -4), (8, -22)], [(0, 0), (24, 16), (44, 20)]]), r(166, 98, 8, 22, INK, 3), bubble(190, 44, "119", 48)]))
S["lounge"] = svg("".join([r(0, 0, W, 200, "#ece6dc"), floor(200, "#a8927a"), window(40, 30, 140, 90), r(230, 150, 130, 50, "#5b7fa6", 10), r(222, 120, 22, 80, "#4f6f92", 8), r(346, 120, 22, 80, "#4f6f92", 8), r(240, 126, 110, 34, "#6b8db3", 8),
    r(90, 176, 90, 8, "#8a6a4a", 3), r(130, 184, 10, 36, "#8a6a4a"), cup(116, 176), r(144, 164, 30, 12, "#fdfaf3", 1, f'stroke="{INK}" stroke-width="1"'),
    person(60, 232, STAFF, STAFF2, HAIR, female=True, arms=[[(0, 0), (20, 14), (40, 10)]], scale=0.9)]))
S["sales"] = S["meeting"]
S["weather"] = svg("".join([r(0, 0, W, 200, "#cfe3ee"), r(0, 200, W, 60, "#b7cf9c"), c(90, 70, 32, "#f6c453"), "".join(ln([(90 + 44 * dx, 70 + 44 * dy), (90 + 56 * dx, 70 + 56 * dy)], "#f6c453", 4) for dx, dy in [(1, 0), (0.7, 0.7), (0, 1), (-0.7, 0.7), (-1, 0), (-0.7, -0.7), (0, -1), (0.7, -0.7)]),
    c(270, 64, 26, "#ffffff"), c(300, 54, 32, "#ffffff"), c(334, 68, 24, "#ffffff"), r(262, 66, 80, 26, "#ffffff", 12), "".join(ln([(276 + i * 22, 104), (270 + i * 22, 122)], "#5b9bd5", 3) for i in range(4)),
    person(280, 232, "#c25e4f", GUEST2, HAIR, female=True, arms=[[(0, 0), (-8, 14), (0, 28)], [(0, 0), (6, 30), (6, 44)]]), '<path d="M222,82 a44,36 0 0 1 88,0 z" fill="#e8743b"/>', ln([(266, 82), (266, 150)], INK, 3)]))
S["korea"] = svg("".join([r(0, 0, W, 190, "#dfeaf0"), r(0, 190, W, 70, "#c9bfa8"), '<path d="M40,96 q160,-70 320,0 l-18,10 q-142,-52 -284,0 z" fill="#3d4a55"/>', r(90, 104, 220, 86, "#f2e9d8"), "".join(r(96 + i * 44, 104, 8, 86, "#8a5a3a") for i in range(6)),
    r(150, 130, 40, 60, "#fdfaf3", 1, 'stroke="#8a5a3a" stroke-width="3"'), r(210, 130, 40, 60, "#fdfaf3", 1, 'stroke="#8a5a3a" stroke-width="3"'), ln([(170, 130), (170, 190)], "#8a5a3a", 2), ln([(230, 130), (230, 190)], "#8a5a3a", 2),
    '<ellipse cx="330" cy="226" rx="40" ry="14" fill="#3d4a55"/>', '<ellipse cx="330" cy="220" rx="34" ry="10" fill="#fdfaf3"/>', c(318, 218, 6, "#7cbf5a"), c(332, 222, 6, "#e8743b"), c(344, 216, 6, "#f6c453"), c(330, 214, 5, "#e85d4a"),
    person(60, 240, "#c58ad0", "#e85d4a", HAIR, female=True, scale=0.8, arms=[[(0, 0), (16, 20), (30, 26)]])]))
S["numbers"] = svg("".join([wall("#e6e2da", "#c9c0b2", 200), c(90, 90, 46, "#ffffff", f'stroke="{INK}" stroke-width="4"'), ln([(90, 90), (90, 58)], INK, 4), ln([(90, 90), (112, 100)], INK, 4), c(90, 90, 4, "#e85d4a"),
    r(170, 46, 100, 96, "#ffffff", 4, 'stroke="#8a8a8a" stroke-width="3"'), r(170, 46, 100, 24, "#c25e4f", 4), t(220, 118, "24", 40, INK, extra='font-weight="700"'),
    f'<path d="M300,70 h60 l16,22 l-16,22 h-60 z" fill="#f6c453" stroke="{INK}" stroke-width="2"/>', c(362, 92, 4, "#ffffff"), t(328, 98, "$50", 16, INK, extra='font-weight="700"'),
    counter(60, 170, 280, 70), r(170, 140, 50, 26, "#3d4a55", 3), r(176, 126, 38, 16, "#cfe3ee", 2)]))
S["shopping"] = svg("".join([wall("#efe4d2", "#b89a76", 200), ln([(40, 50), (220, 50)], "#8a8a8a", 4), ln([(50, 50), (50, 200)], "#8a8a8a", 4), ln([(210, 50), (210, 200)], "#8a8a8a", 4),
    "".join(f'<path d="M{x-18},{66} l18,-10 l18,10 l-6,8 v70 h-24 v-70 z" fill="{col}"/>' for x, col in [(84, "#c25e4f"), (128, "#5b7fa6"), (172, "#6d8c5e")]),
    person(290, 232, "#c58ad0", GUEST2, HAIR, female=True, arms=[[(0, 0), (-28, 10), (-46, -6)], [(0, 0), (8, 30), (10, 44)]]), r(296, 176, 30, 34, "#f6c453", 3), '<path d="M302,176 q9,-16 18,0" stroke="#3d4a55" stroke-width="2.5" fill="none"/>']))
S["sick"] = svg("".join([wall("#e3eef2", "#b8c9cf", 200), r(40, 30, 70, 70, "#ffffff", 6, 'stroke="#c9ced2" stroke-width="3"'), r(66, 44, 18, 42, "#5bb38a"), r(54, 56, 42, 18, "#5bb38a"),
    person(170, 232, "#7a8a96", GUEST2, HAIR, arms=[[(0, 0), (8, -8), (2, -30)], [(0, 0), (-10, 26), (-2, 40)]], lean=-4),
    person(280, 232, "#ffffff", "#5b7fa6", HAIR2, female=True, arms=[[(0, 0), (-26, 12), (-46, 8)], [(0, 0), (6, 30), (6, 44)]]), r(224, 110, 20, 26, "#fdfaf3", 2, f'stroke="{INK}" stroke-width="1.5"'), r(230, 118, 8, 3, "#e85d4a"), r(232.5, 115.5, 3, 8, "#e85d4a")]))
S["taxi"] = svg("".join([r(0, 0, W, 190, "#dfeaf0"), r(0, 190, W, 70, "#9a9a9a"), r(0, 186, W, 6, "#cfc6b8"), r(20, 60, 110, 130, "#c9b79c"), r(34, 80, 26, 30, "#a9d3ea"), r(76, 80, 26, 30, "#a9d3ea"), r(34, 130, 26, 30, "#a9d3ea"),
    car(150, 170, "#f2c230", r(232, 124, 34, 13, "#3d4a55", 3) + t(249, 134, "TAXI", 9, "#f6e7a8")),
    person(120, 240, GUEST, GUEST2, HAIR, arms=[[(0, 0), (20, -10), (34, -34)]], scale=0.8), suitcase(60, 200, 34, 44, "#5b7fa6")]))
S["train"] = svg("".join([r(0, 0, W, 190, "#dfeaf0"), r(0, 190, W, 70, "#b9b3a6"), r(110, 70, 320, 110, "#5b7fa6", 14), r(110, 150, 320, 10, "#e8743b"), "".join(r(136 + i * 62, 90, 44, 40, "#cfe3ee", 4) for i in range(5)), r(96, 180, 320, 8, "#56646f"),
    r(20, 40, 70, 44, "#2f4f66", 4), t(55, 58, "10:30", 13, "#f6e7a8"), t(55, 74, "BUSAN", 11, "#ffffff"), ln([(55, 84), (55, 190)], "#56646f", 4),
    person(70, 244, "#6d8c5e", GUEST2, HAIR, female=True, arms=[[(0, 0), (20, 16), (36, 14)]], scale=0.8), r(102, 150, 22, 13, "#fdfaf3", 1, f'stroke="{INK}" stroke-width="1"')]))
S["message"] = svg("".join([wall("#e6e2da", "#c9c0b2", 200), r(140, 30, 120, 190, INK, 14), r(148, 46, 104, 150, "#f4f7f9", 4), c(200, 208, 6, "#56646f"),
    r(156, 56, 64, 22, "#dfe6ea", 8), r(180, 86, 64, 22, "#5b7fa6", 8), r(156, 116, 50, 22, "#dfe6ea", 8), r(170, 146, 74, 22, "#5b7fa6", 8),
    r(290, 80, 80, 54, "#ffffff", 4, f'stroke="{INK}" stroke-width="2"'), ln([(290, 82), (330, 110), (370, 82)], INK, 2), c(60, 100, 26, "#f6c453"), t(60, 108, "@", 26, INK, extra='font-weight="700"')]))
S["opinion"] = svg("".join([wall(), window(30, 40, 60, 110), plant(340, 150),
    person(140, 232, "#5b7fa6", GUEST2, HAIR, arms=[[(0, 0), (20, 4), (34, -10)], [(0, 0), (-6, 30), (-6, 44)]]), person(260, 232, "#6d8c5e", GUEST2, HAIR2, female=True, arms=[[(0, 0), (-18, 18), (-30, 22)], [(0, 0), (6, 30), (6, 44)]]),
    bubble(90, 36, "I like…", 76), bubble(226, 30, "Me too!", 80)]))
S["toeic_l"] = svg("".join([wall("#e6e2da", "#c9c0b2", 200), desk(60, 170, 280), r(110, 120, 110, 50, "#fdfaf3", 2, f'stroke="{INK}" stroke-width="1.5"'), "".join(c(128 + j * 22, 136 + i * 18, 6, "#3d4a55" if (i, j) in ((0, 1), (1, 3)) else "#ffffff", f'stroke="{INK}" stroke-width="1.2"') for i in range(2) for j in range(4)),
    ln([(250, 130), (290, 160)], "#e8b23b", 5), '<path d="M150,70 a50,50 0 0 1 100,0" stroke="#3d4a55" stroke-width="7" fill="none"/>', r(140, 66, 20, 34, "#3d4a55", 6), r(240, 66, 20, 34, "#3d4a55", 6),
    "".join(ln([(290 + i * 14, 70 - h), (290 + i * 14, 70 + h)], "#5b7fa6", 4) for i, h in enumerate([8, 18, 26, 14, 22, 10]))]))
S["toeic_r"] = svg("".join([wall("#e6e2da", "#c9c0b2", 200), desk(60, 180, 280), r(90, 50, 110, 130, "#fdfaf3", 2, f'stroke="{INK}" stroke-width="1.5"'), "".join(ln([(102, 70 + i * 14), (188 - (i % 3) * 14, 70 + i * 14)], "#9aa7b1", 2.5) for i in range(7)), r(120, 96, 34, 8, "#f6c453"),
    r(220, 70, 110, 110, "#fdfaf3", 2, f'stroke="{INK}" stroke-width="1.5"'), "".join(t(236, 96 + i * 22, "ABCD"[i], 13, INK, "start") + c(262, 92 + i * 22, 6, "#3d4a55" if i == 2 else "#ffffff", f'stroke="{INK}" stroke-width="1.2"') + ln([(276, 92 + i * 22), (318, 92 + i * 22)], "#9aa7b1", 2.5) for i in range(4)),
    ln([(340, 120), (366, 170)], "#e8b23b", 5)]))
S["words"] = svg("".join([wall("#e6e2da", "#c9c0b2", 200), "".join(r(x, y, 110, 70, "#fdfaf3", 6, f'stroke="{INK}" stroke-width="1.5" transform="rotate({a} {x+55} {y+35})"') for x, y, a in [(60, 60, -8), (150, 90, 5), (240, 56, 9)]),
    t(115, 100, "book", 18, INK, extra='font-weight="700" transform="rotate(-8 115 95)"'), t(205, 132, "stay", 18, INK, extra='font-weight="700" transform="rotate(5 205 125)"'), t(295, 98, "guest", 18, INK, extra='font-weight="700" transform="rotate(9 295 91)"'),
    desk(60, 190, 280, 40)]))
S["manner"] = svg("".join([wall(), window(30, 40, 60, 110), plant(340, 150), r(150, 30, 100, 150, "#d9e6ea", 3, 'stroke="#b8a888" stroke-width="5"'), ln([(200, 30), (200, 180)], "#b8a888", 4),
    person(120, 232, STAFF, STAFF2, HAIR, female=True, arms=[[(0, 0), (30, 14), (58, 20)], [(0, 0), (-6, 30), (-6, 44)]], lean=6), person(280, 232, GUEST, GUEST2, HAIR2, arms=[[(0, 0), (-6, 30), (-6, 44)]]), suitcase(310, 186, 40, 46, "#5b7fa6")]))
S["dept"] = svg("".join([r(0, 0, W, 200, "#dfeaf0"), r(0, 200, W, 60, "#b9b3a6"), r(110, 30, 180, 170, "#c9b79c"), r(100, 22, 200, 14, "#8a6a4a"), sign(150, 44, 100, "HOTEL"),
    "".join(r(126 + j * 40, 84 + i * 34, 26, 22, "#a9d3ea") for i in range(3) for j in range(4)), r(184, 164, 32, 36, "#56646f", 3),
    person(50, 240, STAFF, STAFF2, HAIR, scale=0.75), person(350, 240, "#ffffff", "#3b4a5a", HAIR2, cap="#ffffff", scale=0.75), person(84, 248, "#7a8a96", "#2c3a48", HAIR, female=True, scale=0.75)]))
S["valet"] = svg("".join([r(0, 0, W, 190, "#e9e4da"), r(0, 190, W, 70, "#9a9a9a"), r(0, 186, W, 6, "#cfc6b8"), sign(20, 20, 140, "VALET"), r(30, 46, 120, 140, "#7a8a96"), r(44, 60, 92, 126, "#b9d3e0"),
    car(190, 170, "#5b7fa6"), person(130, 240, "#8a2f2f", STAFF2, HAIR, arms=[[(0, 0), (24, 14), (44, 8)]], cap="#8a2f2f", scale=0.85), c(170, 118, 5, "#e8b23b")]))
S["vip"] = svg("".join([wall(), sign(70, 20, 260, "RECEPTION"), person(150, 210, STAFF, STAFF2, HAIR, female=True, arms=[[(0, 0), (34, 14), (62, 6)]]), counter(40, 140, 320),
    f'<path d="M206,120 q-10,-20 6,-26 q-2,-14 10,-10 q10,-10 16,2 q14,0 8,14 q8,12 -8,20 z" fill="#e85d4a"/>', ln([(222, 122), (222, 140)], "#6e9a64", 3),
    person(300, 262, "#24323f", "#24323f", HAIR2, back=True), '<path d="M284,70 l8,12 l8,-14 l8,14 l8,-12 l-3,22 h-26 z" fill="#f6c453" stroke="#c9932b" stroke-width="1.5"/>']))

RULES = [
 # 영어면접, TOEIC
 (r"^영어면접\|", "interview"),
 (r"^TOEIC\|(빈출 단어|자주 나오는 표현)", "words"), (r"^TOEIC\|.*(Part [1-4]|듣기|LC)", "toeic_l"), (r"^TOEIC\|", "toeic_r"),
 # 기초회화
 (r"^기초회화\|기본 인사", "greet"), (r"^기초회화\|만남\|첫 만남", "handshake"), (r"^기초회화\|만남", "opinion"),
 (r"^기초회화\|숫자·시간", "numbers"), (r"로비와 식당|식당에서$", "restaurant"), (r"수영장·객실·엘리베이터", "sign"), (r"지도와 길 묻기|길 묻기|공원에서", "map"), (r"궁 관람", "korea"),
 (r"짐 맡기기", "bellcart"), (r"식당 예약 부탁", "concierge"), (r"지난 주말|다음 달 여행", "travel"), (r"감사와 사과", "greet"), (r"안도와 피곤함", "opinion"), (r"옷 가게", "shopping"),
 (r"^기초회화\|전화\|전화로 예약", "reservation"), (r"^기초회화\|전화", "phone"), (r"^기초회화\|날씨", "weather"), (r"^기초회화\|한국·전주", "korea"), (r"^기초회화\|좋아하는 것", "opinion"),
 (r"^기초회화\|몸 상태.*도움 요청하기", "emergency"), (r"^기초회화\|몸 상태", "sick"), (r"택시", "taxi"), (r"기차", "train"), (r"^기초회화\|이동과 교통", "bus"), (r"^기초회화\|짧은 메시지", "message"),
 # 호텔기본
 (r"^호텔기본\|부서·직무", "dept"), (r"^호텔기본\|객실·요금", "room"), (r"^호텔기본\|서비스 매너", "manner"), (r"^호텔기본\|시설 안내", "sign"),
 # 프런트
 (r"^프런트\|예약", "reservation"), (r"^프런트\|체크인", "frontdesk"), (r"^프런트\|체크아웃", "checkout"),
 (r"발레|벨·도어", "bellcart"), (r"전화 연결|메시지 받기|전화 응대", "phone"), (r"^프런트\|고객 서비스", "frontdesk"),
 (r"교통", "bus"), (r"쇼핑", "shopping"), (r"대행 예약", "concierge"), (r"^프런트\|안내", "map"),
 # 객실·시설
 (r"세탁", "laundry"), (r"분실물", "lostfound"), (r"청소 시간", "vacuum"), (r"^객실·시설\|객실 정비", "towels"), (r"^객실·시설\|시설 관리", "repair"),
 (r"수영장", "pool"), (r"스파", "spa"), (r"키즈", "kids"), (r"^객실·시설\|레저", "fitness"),
 # 식음료
 (r"주방|조리법", "chef"), (r"빈자리|자리 안내", "tables"), (r"^식음료\|레스토랑", "restaurant"),
 (r"\|[^|]*(룸서비스|배달 요금)[^|]*$", "roomservice"), (r"카페", "cafe"), (r"^식음료\|조식", "buffet"),
 (r"와인 (기본|중급|심화)", "wine"), (r"^식음료\|바·와인", "bar"), (r"회의·행사|장비와 패키지", "meeting"), (r"^식음료\|연회", "banquet"),
 # 고객응대·실무
 (r"VIP", "vip"), (r"응급|안전", "emergency"), (r"라운지", "lounge"), (r"^고객응대·실무\|고객 응대", "complaint"),
 (r"이메일", "laptop"), (r"단체·여행사", "bus"), (r"^고객응대·실무\|영업", "sales"),
]
def scene_of(menu, sub, title):
    key = "|".join([menu, sub, title])
    for pat, k in RULES:
        if re.search(pat, key): return k
    return None
