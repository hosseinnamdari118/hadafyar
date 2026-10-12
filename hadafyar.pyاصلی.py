# -*- coding: utf-8 -*-
"""
هدف‌یار — برنامه‌ریزی و رقابت مطالعه با اتاق‌های مطالعه و چت آنلاین
توسعه‌یافته توسط حسین نامداری

اجرا: Pydroid 3 (دکمه‌ی Run) یا IDLE ویندوز (کلید F5).
روی سرور: python hadafyar.py   (پورت از متغیر PORT خوانده می‌شود)
هیچ پکیجی لازم نیست.
"""
import asyncio
import base64
import hashlib
import json
import os
import socket
import time
import zlib

BUNDLE = {
    'app.js': (
        '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'
    ),
    'icons/icon-192.png': (
        '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'
        'rkJggjPJR6Q='
    ),
    'icons/icon-512.png': (
        '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'
        '/wFDIBPU'
    ),
    'icons/maskable-512.png': (
        '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'
    ),
    'index.html': (
        'eNqFVMFOGzEQvfMV7vbKZiGqqlLt8i+Od8K6deyVbQLcSlUCh/xBb70sjdpGASTEpd/hhVu/pDNeEpJIVS9re96blzeecfJXpRH+'
        'rAZW+ZE63MlpYYrroyIZ8oSV0haJ9SohCHiJywg8Z6Li1oEvkmM/TN8ly7DmIyiSsYST2lifMGG0B420E1n6qihhLAWk8bDLpJZe'
        'cpU6wRUU+7tsmZcOpS+EGYPdEvYVjCAVRhm7pv167+2e6Pe3uCU4YWXtpdFr3PYyzNvzP5+mT9PQhEX4ysJ1WLST0LQX7SXGwwKR'
        'm6cpC3OEb/GA21lonqbtRVgw/Nwj90t4QCVEvmGAdHDbEK39jBoIIX+DSz/TsMdJmFHOBIOkOGHtFYtO5hi9Iv1LXO7QyyTMtwri'
        'x77aqDv8JH8kEu2jRkPuKU1J/ZFZUEUy4loOwWEvKgvDl3PvBAYrbCNDCrqxjk17l9E33T/o92p9tMnlda0g9eZYVOn/87z0Cg63'
        'WpBnXXhd1vkzBa4CWNmOkZ5wjnSy50kcmPIMl1KOmSyjGUQZi4MKNsa8wViXADaCIy51hGjaEub5QOoSTosk3ScmwZGneaeKBJcw'
        'biVPFR+QO2zlr3D30uf1CSIJzIwK5Eso7lyRCAulxHsOM2zvLQ3Ec/3tOYZwOrr4PftHT/MMxajybllW7A13fuVOjnFKaqOkB7Kx'
        'SY23mVpj/AumTfdEDvOaxQvGdF6WUh+977+pT9EuVtaV2KC7GZrFSSW7Tbhh208JWT/Q8xUekP34nXy3v2ngr0kjzBnmP9CDiJFw'
        'F+a9PKvpwpY+dvJuw5wVsZ+9D47sruDsueVZ92/1F+GvHAg='
    ),
    'manifest.webmanifest': (
        'eNqlUMFKAzEUvPcrwnqtrRYU9FdEJGZjDW6TJZuKVQQV3fXQo1/gZUWQsioU/ySxN7/EebtbUKQnD9nNm5nMvPcuOoxFmo9ktMui'
        'UPhZuP66mi6mvvQV+7p6YP7JVyH3ZbgLBRhfgXtdTFm4ZyBuoHvyzyzc+Tk0t/4jFFGXPLNjY93BCudGEstMWJU6ZTRpViX5ma/8'
        'Gwpcn325mCKs+pVIzCMAONO1JFm4gQeoknr9oaWBSvaZo2m8yQGSY07z1L3NgN6Tf4HfO3rJ/ayHYFRv9L6dIVwDKpb4nPkXapF8'
        '6glgU9IAzaAJ10Oa8Ii3gytLpXVJuyvHsauxTQjt9VtQmFT+BGKVpQmfEIQHOuaJ0bKhjFVSO77cZIrVW65cQx5ycTK0ZqzjA2ES'
        'U0evbWxviMGgEbhjOZIrOMGdHJJ9BmovkvFYNDFdxFiD0qlT5SbRfi1XwuhaiYKxC3RqBXnWeJ++65s7g16KfcAgU+e1bwTsDIcw'
        'N2mmViM+lP1WmI5tarIa53oSscvuav+tzb/+wM5w/us/4tkJP0zkfzOWPghCzn7nsvMN3dt1Fw=='
    ),
    'style.css': (
        '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'
    ),
    'sw.js': (
        'eNqFVM1u3DYQvu9TTE6i8qNFDOQQG9siCIz2EKCBUcOHIgdGoix2uaQqcr3Z2gZswF374GOeIBc7AQrDcYC0b0LZtzxJZyhpvesi'
        'sA4S+X3D4fx96j+E+thf1IffDk5vTv2Zv4RvB+/BX/nL+gSBK8TrE395/REZhm+y8B/qw/rIn92c1jN4BIj9S9t6RsbH/iyGPfCf'
        '8NgVEset5/oQoeMO/wr+b38VHNQzJP/yF+T65hQe9nup0dbByxcvf16HAUQFz3g+5dWTnZVorSN/2SDutyjpR48hkjoT75LCjRTt'
        'rJsqkaTW0oaXZfJ7WI24lrmwLpmIt906HCaXfXo/efp8JSn19h302dMGfbPW61mh8oRn2fqO0O6VtE5oUTEMwDqu6HYmYhj8ALs9'
        'AJFMuHSb2knFUp4WwiamFJqFzOLEFbhmaTBPyecLpRglFndcoMKNdijLLXQm9TaL43ittx9/PxieOrnDnfh+NLgFaEIKS4BkKKaW'
        'xd2uuX9ow+nXlRlJKxJMEKEkl8rhNWwYyCE8GAygTWnEyw5vE86EEk4ghs+y89vkUiUxfotfLkcs2N2TYS5cWiyn18xFJf7AsRAJ'
        'fsfY3rU5Ma4UElpMYHPjFUM6QSQmXuYQ9iPhCpOFbKKf1n+NYG+PTiWmkttSB1yZlDtpdIe1FiV3heYjAQM62y8EV674M4oxGjeu'
        'NF3S76NM6pP6CPwXf379EZXA/Lm/JBGBPw8qIcn5z7Q7QUXOYo/M2fUFCg4lEkCS2mdSDqnpn1ZayJLo6lnocSVsaXS2JV3RdDmU'
        'ihK8U340nNeueZpC4IxiA2/RroCpKadYQTJIldGCheLNbe4b73LsKIjHwU+8cHZ/vmqqRTd07P48Zqw7ZsEWJ2vEu8S6jAJbUVea'
        'hpqsbYnmO3KbBAE/Lp9e/HHEsAoboXo46qKqTMXaob1nGLVxMpfNZOAop8O7uls0oOLZtnj/U+SSGkKE9EvYBTctxSpEE4zWTNC7'
        'xHvGmdjU2BpXGaVEtgquGgusWFsMheEt9Tc3FbC2lWByaAyo51Fu0rGN0Cuk3cxixwJ62+UWXwqR2r0VgmL0I25t9xdq9h/u7z+z'
    ),
}

PORT = int(os.environ.get("PORT") or os.environ.get("HADAFYAR_PORT") or "8000")
MAX_HISTORY = 150
MAX_TEXT = 600
MAX_PAYLOAD = 8 * 1024
MAX_ROOMS = 400
MAX_ROOMS_PER_OWNER = 5
MAX_JOINED = 1000
GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
ICONS = ["📚", "🎯", "🔥", "🌙", "⚡", "🧠", "🚀", "🏆", "🌿", "💎", "🦅", "⭐"]
THEMES = 8

MIME = {
    ".html": "text/html; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".webmanifest": "application/manifest+json; charset=utf-8",
    ".png": "image/png",
    ".svg": "image/svg+xml",
    ".woff2": "font/woff2",
}

FILES = {}
for _name, _b64 in BUNDLE.items():
    FILES["/" + _name] = zlib.decompress(base64.b64decode(_b64))
FILES["/"] = FILES["/index.html"]


def here():
    try:
        return os.path.dirname(os.path.abspath(__file__))
    except Exception:
        return os.getcwd()


# فونت اختیاری: اگر vazirmatn.woff2 کنار این فایل باشد، استفاده می‌شود
_font = os.path.join(here(), "vazirmatn.woff2")
if os.path.exists(_font):
    try:
        with open(_font, "rb") as f:
            FILES["/vazirmatn.woff2"] = f.read()
    except Exception:
        pass


def say(*a):
    try:
        print(*a)
    except Exception:
        try:
            print(" ".join(str(x) for x in a).encode("ascii", "replace").decode())
        except Exception:
            pass


# ------------------------------------------------------------------
# ذخیره‌ی اتاق‌ها
# ------------------------------------------------------------------
def data_path():
    for base in (here(), os.path.expanduser("~"), os.getcwd()):
        p = os.path.join(base, "hadafyar_data.json")
        try:
            with open(p, "a"):
                pass
            return p
        except Exception:
            continue
    return None


DATA_FILE = os.environ.get("HADAFYAR_DATA") or data_path()
rooms = {}
dirty = False


def now_ms():
    return int(time.time() * 1000)


def sha(s):
    return hashlib.sha256(("hadafyar|" + s).encode("utf-8")).hexdigest()


def uid_of(key):
    return hashlib.sha256(("hy-id|" + key).encode("utf-8")).hexdigest()[:12]


def rid():
    return os.urandom(4).hex()


def new_code():
    alphabet = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"
    while True:
        code = "".join(alphabet[b % len(alphabet)] for b in os.urandom(6))
        if not any(r["code"] == code for r in rooms.values()):
            return code


def make_room(name, slogan, goal, goal_h, icon, theme, private, owner="", owner_name="", rid_=None):
    return {
        "id": rid_ or rid(),
        "name": name,
        "slogan": slogan,
        "goal": goal,
        "goalH": goal_h,
        "icon": icon,
        "theme": theme,
        "private": private,
        "code": new_code(),
        "owner": owner,
        "ownerName": owner_name,
        "created": now_ms(),
        "msgs": [],
        "joined": [],
        "banned": {},
    }


def seed():
    base = [
        ("سالن عمومی کنکور", "با هم می‌خوانیم، با هم می‌رسیم", "هر روز یک قدم جلوتر از دیروز", 5, "📚", 0),
        ("ریاضی و فیزیک", "مسئله‌ها را یکی‌یکی می‌شکنیم", "حل ۲۰ تست تحلیلی در هر روز", 5, "🧠", 5),
        ("زیست و شیمی", "حفظ نه، فهم", "مرور یک فصل زیست در هر روز", 5, "🌿", 3),
        ("علوم انسانی", "کلمه‌ها قدرت‌اند", "خواندن و خلاصه‌نویسی هر روز", 4, "⭐", 4),
        ("تمرکز شبانه", "شب هم مال ماست", "دو ساعت مطالعه‌ی بی‌وقفه بعد از ۹ شب", 3, "🌙", 7),
    ]
    for i, (name, slogan, goal, gh, icon, theme) in enumerate(base):
        rid_ = "r%d" % (i + 1)
        rooms[rid_] = make_room(name, slogan, goal, gh, icon, theme, False, rid_=rid_)


def load():
    global rooms
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            raw = json.load(f).get("rooms", {}) or {}
    except Exception:
        raw = {}
    rooms = {}
    for k, r in raw.items():
        if not isinstance(r, dict) or "name" not in r:
            continue
        base = make_room(r.get("name", "اتاق"), "", "", 4, "📚", 0, False, rid_=k)
        base.update({x: r[x] for x in base if x in r})
        if not base.get("code"):
            base["code"] = new_code()
        rooms[k] = base
    if not rooms:
        seed()


def persist():
    global dirty
    if not dirty or not DATA_FILE:
        return
    dirty = False
    try:
        tmp = DATA_FILE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump({"rooms": rooms}, f, ensure_ascii=False)
        os.replace(tmp, DATA_FILE)
    except Exception as e:
        say("ذخیره نشد:", e)


# ------------------------------------------------------------------
# اتاق‌ها و کاربران
# ------------------------------------------------------------------
clients = set()


class Client:
    def __init__(self, writer):
        self.writer = writer
        self.uid = ""
        self.name = "ناشناس"
        self.room = None
        self.studying = False
        self.today_min = 0
        self.stamps = []
        self.open = True
        self.ready = False

    def send_raw(self, op, payload):
        if not self.open:
            return
        n = len(payload)
        if n < 126:
            head = bytes([0x80 | op, n])
        elif n < 65536:
            head = bytes([0x80 | op, 126]) + n.to_bytes(2, "big")
        else:
            head = bytes([0x80 | op, 127]) + n.to_bytes(8, "big")
        try:
            self.writer.write(head + payload)
        except Exception:
            self.open = False

    def send(self, obj):
        self.send_raw(1, json.dumps(obj, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))


def clean(s, n):
    s = "" if s is None else str(s)
    s = "".join(" " if (ord(c) < 32 or ord(c) == 127) else c for c in s)
    return s.strip()[:n]


def to_float(v, lo, hi, default):
    try:
        x = float(v)
    except Exception:
        return default
    return max(lo, min(hi, x))


def members(room_id):
    owner = rooms[room_id]["owner"] if room_id in rooms else ""
    lst = [
        {"uid": c.uid, "name": c.name, "studying": c.studying, "min": c.today_min, "owner": bool(owner) and c.uid == owner}
        for c in clients
        if c.room == room_id
    ]
    lst.sort(key=lambda m: (-m["min"], m["name"]))
    return lst


def online(room_id):
    return sum(1 for c in clients if c.room == room_id)


def is_mine(r, uid):
    return bool(uid) and (r["owner"] == uid or uid in r["joined"])


def public_info(r, uid="", full=False):
    mine = is_mine(r, uid)
    d = {
        "id": r["id"],
        "name": r["name"],
        "slogan": r["slogan"],
        "goal": r["goal"],
        "goalH": r["goalH"],
        "icon": r["icon"],
        "theme": r["theme"],
        "private": r["private"],
        "owner": r["owner"],
        "ownerName": r["ownerName"],
        "mine": mine,
        "online": online(r["id"]),
        "total": len(r["joined"]) + (1 if r["owner"] and r["owner"] not in r["joined"] else 0),
    }
    if mine or full:
        d["code"] = r["code"]
    return d


def room_list(uid):
    out = []
    for r in rooms.values():
        if r["private"] and not is_mine(r, uid):
            continue
        out.append(public_info(r, uid))
    out.sort(key=lambda r: (not r["mine"], -r["online"], r["name"]))
    return out


def to_room(room_id, obj):
    for c in list(clients):
        if c.room == room_id:
            c.send(obj)


_list_pending = False


def broadcast_rooms():
    global _list_pending
    if _list_pending:
        return
    _list_pending = True

    async def later():
        global _list_pending
        await asyncio.sleep(0.8)
        _list_pending = False
        for c in list(clients):
            if c.ready:
                c.send({"t": "rooms", "list": room_list(c.uid)})

    asyncio.ensure_future(later())


def leave(c, announce=True):
    if not c.room:
        return
    old = c.room
    c.room = None
    c.studying = False
    if announce:
        to_room(old, {"t": "sys", "room": old, "text": "%s از اتاق خارج شد" % c.name})
    to_room(old, {"t": "members", "room": old, "list": members(old)})
    broadcast_rooms()


def push_msg(room, m):
    global dirty
    room["msgs"].append(m)
    if len(room["msgs"]) > MAX_HISTORY:
        del room["msgs"][: len(room["msgs"]) - MAX_HISTORY]
    dirty = True


def enter(c, room):
    """ورود کاربر به اتاق (بعد از بررسی دسترسی)."""
    global dirty
    if c.uid in room["banned"]:
        return c.send({"t": "error", "text": "مدیر اتاق تو را حذف کرده؛ نمی‌توانی دوباره وارد شوی."})
    if c.uid not in room["joined"] and c.uid != room["owner"]:
        room["joined"].append(c.uid)
        if len(room["joined"]) > MAX_JOINED:
            del room["joined"][0]
        dirty = True
    if c.uid == room["owner"] and c.name != room["ownerName"]:
        room["ownerName"] = c.name
        dirty = True
    first = c.room != room["id"]
    if first:
        leave(c)
        c.room = room["id"]
    c.send({"t": "joined", "room": public_info(room, c.uid, True), "history": room["msgs"], "members": members(room["id"])})
    if first:
        to_room(room["id"], {"t": "sys", "room": room["id"], "text": "%s وارد کلاس شد" % c.name})
    to_room(room["id"], {"t": "members", "room": room["id"], "list": members(room["id"])})
    broadcast_rooms()


def read_fields(m, base=None):
    """خواندن و پاک‌سازی فیلدهای اتاق؛ در خطا (None, پیام) برمی‌گرداند."""
    name = clean(m.get("name"), 40)
    if len(name) < 2:
        return None, "نام اتاق حداقل دو حرف باشد."
    for r in rooms.values():
        if r["name"] == name and (base is None or r["id"] != base["id"]):
            return None, "اتاقی با این نام وجود دارد؛ نام دیگری انتخاب کن."
    icon = m.get("icon")
    try:
        theme = int(m.get("theme"))
    except Exception:
        theme = 0
    return {
        "name": name,
        "slogan": clean(m.get("slogan"), 70),
        "goal": clean(m.get("goal"), 90),
        "goalH": to_float(m.get("goalH"), 0.5, 16, 4),
        "icon": icon if icon in ICONS else ICONS[0],
        "theme": theme if 0 <= theme < THEMES else 0,
        "private": bool(m.get("private")),
    }, None


def on_message(c, raw):
    global dirty
    try:
        m = json.loads(raw)
    except Exception:
        return
    if not isinstance(m, dict):
        return
    t = m.get("t")

    if t == "hello":
        key = clean(m.get("key"), 80)
        if len(key) < 16:
            key = rid() + rid() + rid() + rid()  # هویت موقت
        c.uid = uid_of(key)
        c.name = clean(m.get("name"), 24) or "ناشناس"
        c.ready = True
        c.send({"t": "welcome", "uid": c.uid})
        if c.room:
            to_room(c.room, {"t": "members", "room": c.room, "list": members(c.room)})
        return

    if not c.ready:
        return

    if t == "rooms":
        c.send({"t": "rooms", "list": room_list(c.uid)})

    elif t == "create":
        if len(rooms) >= MAX_ROOMS:
            return c.send({"t": "error", "text": "تعداد اتاق‌ها به سقف رسیده."})
        if sum(1 for r in rooms.values() if r["owner"] == c.uid) >= MAX_ROOMS_PER_OWNER:
            return c.send({"t": "error", "text": "هر نفر حداکثر %d اتاق می‌تواند بسازد." % MAX_ROOMS_PER_OWNER})
        f, err = read_fields(m)
        if err:
            return c.send({"t": "error", "text": err})
        room = make_room(f["name"], f["slogan"], f["goal"], f["goalH"], f["icon"], f["theme"], f["private"], c.uid, c.name)
        rooms[room["id"]] = room
        dirty = True
        c.send({"t": "created", "id": room["id"]})
        enter(c, room)

    elif t == "join":
        room = rooms.get(clean(m.get("room"), 20))
        if not room:
            return c.send({"t": "error", "text": "این اتاق دیگر وجود ندارد."})
        if room["private"] and not is_mine(room, c.uid):
            return c.send({"t": "error", "text": "این اتاق خصوصی است؛ با کد دعوت وارد شو."})
        enter(c, room)

    elif t == "joinCode":
        code = clean(m.get("code"), 12).upper().replace(" ", "")
        room = next((r for r in rooms.values() if r["code"] == code), None)
        if not room:
            return c.send({"t": "error", "text": "کدی با این مشخصات پیدا نشد."})
        enter(c, room)

    elif t == "leave":
        leave(c)
        c.send({"t": "left"})

    elif t == "msg":
        if not c.room or c.room not in rooms:
            return
        text = clean(m.get("text"), MAX_TEXT)
        if not text:
            return
        now = now_ms()
        c.stamps = [x for x in c.stamps if now - x < 8000]
        if len(c.stamps) >= 6:
            return c.send({"t": "error", "text": "آرام‌تر؛ پیام‌ها خیلی پشت‌سرهم بودند."})
        c.stamps.append(now)
        msg = {"t": "msg", "room": c.room, "uid": c.uid, "name": c.name, "text": text, "ts": now}
        push_msg(rooms[c.room], msg)
        to_room(c.room, msg)

    elif t == "status":
        c.studying = bool(m.get("studying"))
        try:
            v = int(round(float(m.get("todayMin") or 0)))
        except Exception:
            v = 0
        c.today_min = max(0, min(1440, v))
        if c.room:
            to_room(c.room, {"t": "members", "room": c.room, "list": members(c.room)})

    # ---------- دستورهای مدیر اتاق ----------
    elif t in ("kick", "edit", "delete", "bans", "unban"):
        room = rooms.get(c.room) if c.room else None
        if not room:
            return
        if not room["owner"] or room["owner"] != c.uid:
            return c.send({"t": "error", "text": "فقط مدیر اتاق می‌تواند این کار را انجام دهد."})

        if t == "kick":
            target = clean(m.get("uid"), 20)
            if not target or target == c.uid:
                return
            victims = [x for x in clients if x.room == room["id"] and x.uid == target]
            if not victims:
                return c.send({"t": "error", "text": "این عضو دیگر در اتاق نیست."})
            room["banned"][target] = victims[0].name
            dirty = True
            for v in victims:
                v.send({"t": "kicked", "room": room["id"], "reason": "kick"})
                v.room = None
                v.studying = False
            msg = {"t": "sys", "room": room["id"], "text": "%s توسط مدیر از اتاق حذف شد" % victims[0].name}
            to_room(room["id"], msg)
            to_room(room["id"], {"t": "members", "room": room["id"], "list": members(room["id"])})
            broadcast_rooms()

        elif t == "edit":
            f, err = read_fields(m, room)
            if err:
                return c.send({"t": "error", "text": err})
            room.update(f)
            dirty = True
            for x in list(clients):
                if x.room == room["id"]:
                    x.send({"t": "roomInfo", "room": public_info(room, x.uid, True)})
            c.send({"t": "ok", "text": "اتاق به‌روز شد."})
            broadcast_rooms()

        elif t == "delete":
            rid_ = room["id"]
            for x in list(clients):
                if x.room == rid_:
                    x.send({"t": "kicked", "room": rid_, "reason": "deleted"})
                    x.room = None
                    x.studying = False
            del rooms[rid_]
            dirty = True
            broadcast_rooms()

        elif t == "bans":
            c.send({"t": "bans", "list": [{"uid": k, "name": v} for k, v in room["banned"].items()]})

        elif t == "unban":
            target = clean(m.get("uid"), 20)
            if target in room["banned"]:
                del room["banned"][target]
                dirty = True
            c.send({"t": "bans", "list": [{"uid": k, "name": v} for k, v in room["banned"].items()]})


# ------------------------------------------------------------------
# HTTP + WebSocket (فقط کتابخانه‌ی استاندارد)
# ------------------------------------------------------------------
async def http_reply(writer, code, body, ctype="text/plain; charset=utf-8", head_only=False, extra=""):
    reason = {200: "OK", 400: "Bad Request", 404: "Not Found", 405: "Method Not Allowed"}.get(code, "OK")
    head = "HTTP/1.1 %d %s\r\nContent-Type: %s\r\nContent-Length: %d\r\nConnection: close\r\n%s\r\n" % (
        code, reason, ctype, len(body), extra,
    )
    writer.write(head.encode("latin-1") + (b"" if head_only else body))
    await writer.drain()


async def ws_loop(reader, writer, client):
    frags = []
    frag_len = 0
    while True:
        b0, b1 = await reader.readexactly(2)
        fin = bool(b0 & 0x80)
        op = b0 & 0x0F
        masked = bool(b1 & 0x80)
        ln = b1 & 0x7F
        if ln == 126:
            ln = int.from_bytes(await reader.readexactly(2), "big")
        elif ln == 127:
            ln = int.from_bytes(await reader.readexactly(8), "big")
        if not masked or ln > MAX_PAYLOAD:
            return
        mask = await reader.readexactly(4)
        data = bytearray(await reader.readexactly(ln))
        for i in range(ln):
            data[i] ^= mask[i & 3]
        data = bytes(data)
        if op == 8:
            client.send_raw(8, b"")
            return
        if op == 9:
            client.send_raw(10, data)
        elif op in (0, 1, 2):
            frags.append(data)
            frag_len += len(data)
            if frag_len > MAX_PAYLOAD:
                return
            if fin:
                msg = b"".join(frags).decode("utf-8", "replace")
                frags, frag_len = [], 0
                on_message(client, msg)


async def handle(reader, writer):
    client = None
    try:
        try:
            raw = await asyncio.wait_for(reader.readuntil(b"\r\n\r\n"), 15)
        except Exception:
            return
        lines = raw.decode("latin-1").split("\r\n")
        parts = lines[0].split(" ")
        if len(parts) < 2:
            return
        method, target = parts[0], parts[1]
        headers = {}
        for ln in lines[1:]:
            if ":" in ln:
                k, v = ln.split(":", 1)
                headers[k.strip().lower()] = v.strip()

        if headers.get("upgrade", "").lower() == "websocket" and headers.get("sec-websocket-key"):
            accept = base64.b64encode(hashlib.sha1((headers["sec-websocket-key"] + GUID).encode()).digest()).decode()
            writer.write(
                (
                    "HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n"
                    "Sec-WebSocket-Accept: %s\r\n\r\n" % accept
                ).encode()
            )
            await writer.drain()
            client = Client(writer)
            clients.add(client)
            await ws_loop(reader, writer, client)
            return

        if method not in ("GET", "HEAD"):
            return await http_reply(writer, 405, b"405")
        path = target.split("?", 1)[0].split("#", 1)[0]
        if path == "/healthz":
            return await http_reply(writer, 200, b"ok")
        if path.endswith("/"):
            path = "/"
        body = FILES.get(path)
        if body is None:
            return await http_reply(writer, 404, "پیدا نشد".encode("utf-8"))
        ext = os.path.splitext(path)[1].lower() if path != "/" else ".html"
        extra = "Cache-Control: no-cache\r\n" if ext == ".html" or path == "/sw.js" else "Cache-Control: public, max-age=3600\r\n"
        await http_reply(writer, 200, body, MIME.get(ext, "application/octet-stream"), method == "HEAD", extra)
    except (asyncio.IncompleteReadError, ConnectionError, OSError):
        pass
    except Exception as e:
        say("خطا:", e)
    finally:
        if client:
            client.open = False
            clients.discard(client)
            leave(client)
        try:
            writer.close()
        except Exception:
            pass


async def background():
    tick = 0
    while True:
        await asyncio.sleep(10)
        tick += 1
        persist()
        if tick % 3 == 0:
            for c in list(clients):
                c.send_raw(9, b"")


def lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("10.255.255.255", 1))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return None


async def main():
    server = None
    port = PORT
    for _ in range(20):
        try:
            server = await asyncio.start_server(handle, "0.0.0.0", port, limit=65536)
            break
        except OSError:
            port += 1
    if server is None:
        say("هیچ پورت آزادی پیدا نشد. برنامه‌های دیگر را ببند و دوباره اجرا کن.")
        return
    ip = lan_ip()
    say("=" * 52)
    say("   هدف‌یار اجرا شد ✅   (توسعه‌یافته توسط حسین نامداری)")
    say("=" * 52)
    say("روی همین دستگاه، این آدرس را در Chrome باز کن:")
    say("      http://localhost:%d" % port)
    if ip and ip != "127.0.0.1":
        say("")
        say("برای دوستانت (فقط وقتی به همین وای‌فای وصل‌اند):")
        say("      http://%s:%d" % (ip, port))
    say("")
    say("برای خاموش کردن: دکمه‌ی Stop (یا بستن پنجره).")
    say("-" * 52)
    if not (os.environ.get("HADAFYAR_NOBROWSER") or os.environ.get("PORT")):
        try:
            import webbrowser

            webbrowser.open("http://localhost:%d" % port)
        except Exception:
            pass
    asyncio.ensure_future(background())
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    load()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    finally:
        dirty = True
        persist()
        say("هدف‌یار متوقف شد.")
