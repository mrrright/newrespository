#!/usr/bin/env python3
"""A „Sötét mező" KLWP preset generátora.

Használat:  python3 -I build.py [kimeneti.klwp]
Terv:       docs/klwp-sotet-mezo.md

A fájlszerkezet 17 valódi KLWP preset (version 17) elemzésén alapul
(.claude/skills/klwp/reference/fajlformatum.md). KÍSÉRLETI: hogy a KLWP
betölti-e, azt csak a telefonon lehet kipróbálni.
"""
import io
import json
import os
import sys
import time
import uuid
import zipfile

from PIL import Image, ImageDraw

W, H = 720.0, 1600.0          # a mintafájlok szerkesztési mérete (tartalékértékekhez)
KOD = "cjal"                  # hal: jobb fent (c) → bal lent (j) → bal fent (a) → jobb lent (l)

GOOGLE = ("intent:#Intent;action=android.intent.action.MAIN;category=android.intent.category.LAUNCHER;"
          "component=com.google.android.googlequicksearchbox/.SearchActivity;"
          "S.org.kustom.intent.label=Google;end")
NOVA_DRAWER = ("intent:#Intent;action=com.teslacoilsw.launcher.ACTION;launchFlags=0x10000000;"
               "component=com.teslacoilsw.launcher/.NovaShortcutHandler;"
               "S.LAUNCHER_ACTION=APP_DRAWER;S.org.kustom.intent.label=Nova%20action;end")

# ---------------------------------------------------------------- segédek

def node(itype, title=None, props=None, f=None, g=None, events=None, anims=None, items=None):
    """Egy elem. props: fix értékek; f: {mező: képlet} (toggle 10); g: {mező: globális} (toggle 100)."""
    n = {"internal_type": itype}
    if title:
        n["internal_title"] = title
    n.update(props or {})
    toggles, formulas, globs = {}, {}, {}
    for k, v in (f or {}).items():
        toggles[k], formulas[k] = 10, v
    for k, v in (g or {}).items():
        toggles[k], globs[k] = 100, v
    if toggles:
        n["internal_toggles"] = toggles
    if formulas:
        n["internal_formulas"] = formulas
    if globs:
        n["internal_globals"] = globs
    if events:
        n["internal_events"] = events
    if anims:
        n["internal_animations"] = anims
    if items is not None:
        n["viewgroup_items"] = items
    return n


def vis(cond):
    return {"config_visible": f"$if({cond},always,remove)$"}


def rect(w, h, color="#00000000", fw=None, fh=None, fcolor=None, anchor=None, extra_f=None, title=None,
         shape="RECT", props=None):
    p = {"shape_type": shape, "shape_width": float(fw or 10), "shape_height": float(fh or 10),
         "paint_color": color}
    if anchor:
        p["position_anchor"] = anchor
    p.update(props or {})
    f = {"shape_width": w, "shape_height": h}
    if fcolor:
        f["paint_color"] = fcolor
    f.update(extra_f or {})
    return node("ShapeModule", title, p, f)


def text(expr, size="$(si(rwidth)+si(rheight))/75$", color="$gv(c_txt)$", anchor=None, title=None,
         extra_f=None, align="CENTER"):
    p = {"text_expression": expr, "text_size": 20.0, "text_align": align, "paint_color": "#FFE6E6E6"}
    if anchor:
        p["position_anchor"] = anchor
    f = {"text_size": size, "paint_color": color}
    f.update(extra_f or {})
    return node("TextModule", title, p, f)


def overlap(items, title=None, anchor=None, f=None, events=None, anims=None, props=None):
    p = dict(props or {})
    if anchor:
        p["position_anchor"] = anchor
    return node("OverlapLayerModule", title, p, f, events=events, anims=anims, items=items)


def stack(items, stacking, title=None, anchor=None, f=None, events=None, anims=None):
    p = {"config_stacking": stacking}
    if anchor:
        p["position_anchor"] = anchor
    return node("StackLayerModule", title, p, f, events=events, anims=anims, items=items)


def kf(pos, prop, val):
    return {"position": pos, "value": float(val), "property": prop, "ease": "STRAIGHT"}


def anim(atype, keys, duration=3.0, delay=None, formula=None, ease="STRAIGHT", anchor=None, trigger=None,
         type_formula=None):
    a = {"type": atype, "action": "ADVANCED", "ease": ease, "duration": float(duration), "animator": keys}
    if delay is not None:
        a["delay"] = float(delay)
    if formula:
        a["formula"] = formula
    if anchor:
        a["anchor"] = anchor
    if trigger:
        a["trigger"] = trigger
    if type_formula:
        a["internal_toggles"] = {"type": 10}
        a["internal_formulas"] = {"type": type_formula}
    return a


def appear(keys0, keys1, delay=None):
    """Megjelenési animáció a mintafájlok VISIBILITY mintája szerint (0% kezdő, 100% vég, ease INVERTED)."""
    return anim("VISIBILITY", [kf(0, k, v) for k, v in keys0] + [kf(100, k, v) for k, v in keys1],
                duration=3.0, delay=delay, ease="INVERTED")


def ev_switch(glob, value):
    return {"type": "SINGLE_TAP", "action": "SWITCH_GLOBAL", "switch": glob, "switch_text": value}


# Vezérlőgombok mellé: frissíti a nyitva tartás idejét, a kódot és az állapotot nem változtatja.
EV_REFRESH = ev_switch("st", '$"t"+tc(lpad,gv(now),5,0)+if(gv(open)=1,"o","c")+gv(sq)$')


def ev_zone(letter):
    tail = 'tc(cut,gv(sq),1,3)+"%s"' % letter
    return ev_switch("st", '$"t"+tc(lpad,gv(now),5,0)+if(gv(open)=1|%s=gv(kod),"o","c")+%s$' % (tail, tail))


def button(label_node, w, h, events, title=None, f=None):
    """Érinthető gomb: átlátszó alakzat (az érintési felület) + felirat."""
    return overlap([rect(w, h), label_node], title=title, f=f, events=events + [EV_REFRESH])


# ---------------------------------------------------------------- globálisok

def globals_list():
    g = {}

    def add(name, gtype, desc, **kw):
        d = {"index": len(g) + 1, "type": gtype, "title": name, "description": desc}
        d.update(kw)
        g[name] = d

    add("c_bg", "COLOR", "háttér (AMOLED fekete)", value="#FF000000")
    add("c_line", "COLOR", "nyugalmi vonalak", value="#FF2A2A2A")
    add("c_txt", "COLOR", "szöveg", value="#FFE6E6E6")
    add("c_dim", "COLOR", "halvány szöveg", toggles=10, global_formula="$ce(gv(c_txt),alpha,50)$")
    add("c_acc", "COLOR", "kiemelőszín", value="#FF7FDBFF")
    add("lw", "NUMBER", "vonalvastagság", value=2.0, min=0, max=720, toggles=10,
        global_formula="$si(rwidth)/360$")
    add("kod", "TEXT", "kopogó kód: a zónák betűi (a b c / d e f / g h i / j k l)", value=KOD)
    add("nyitido", "NUMBER", "vezérlés nyitva tartása (mp)", value=45.0, min=0, max=720)
    add("felfedido", "NUMBER", "felfedés ideje (mp)", value=6.0, min=0, max=720)
    add("forgat", "SWITCH", "óránkénti átrendeződés", value=1)
    add("debug", "SWITCH", "hibakereső sor", value=1)
    add("st", "TEXT", "ÁLLAPOT – ne módosítsd", value="t00000cxxxx")
    add("now", "TEXT", "a nap eltelt másodpercei", value="$df(H)*3600+df(mm)*60+df(ss)$")
    add("tt", "TEXT", "utolsó koppintás ideje", value="$tc(cut,gv(st),1,5)$")
    add("fl", "TEXT", "o = nyitva, c = zárva", value="$tc(cut,gv(st),6,1)$")
    add("sq", "TEXT", "utolsó 4 zóna", value="$tc(cut,gv(st),7,4)$")
    add("z", "TEXT", "utolsó zóna", value="$tc(cut,gv(st),10,1)$")
    add("age", "TEXT", "mp az utolsó koppintás óta",
        value="$if(gv(now)>=gv(tt),gv(now)-gv(tt),gv(now)+86400-gv(tt))$")
    add("open", "TEXT", "nyitva van-e a vezérlés",
        value='$if(gv(fl)="o"&gv(age)<gv(nyitido)&si(locked)=0,1,0)$')
    add("rot", "TEXT", "átrendeződési eltolás", value="$if(gv(forgat)=1,df(H)%9,0)$")
    add("grp", "TEXT", "megnyitott app-csoport (0 = nincs)", value="0")
    return g


# ---------------------------------------------------------------- nyugalom: napvonal

def day_line():
    track = rect("$si(rwidth)*0.8$", "$gv(lw)$", fw=576, fh=2, fcolor="$ce(gv(c_line),alpha,40)$",
                 anchor="CENTERLEFT", title="Teljes nap")
    prog = rect("$si(rwidth)*0.8*(df(H)*60+df(mm))/1440$", "$gv(lw)$", fw=300, fh=2,
                fcolor="$gv(c_line)$", anchor="CENTERLEFT", title="Eltelt nap")
    dot = rect("$gv(lw)*4$", "$gv(lw)*4$", fw=8, fh=8, shape="CIRCLE", anchor="CENTERLEFT", title="Akkupont",
               fcolor="$if(bi(level)<20,#FFFF5252,gv(c_dim))$",
               extra_f={"position_offset_x": "$si(rwidth)*0.8*bi(level)/100-gv(lw)*2$"},
               props={"position_offset_x": 400.0})
    dot["internal_animations"] = [anim("LOOP_2W", [kf(0, "SCALE_XY", 1), kf(100, "SCALE_XY", 1.6)],
                                       duration=10, type_formula="$if(bi(source)=Battery,disabled,loop_2w)$")]
    return overlap(
        [track, prog, dot], title="Napvonal", anchor="CENTERLEFT",
        props={"position_padding_left": 72.0, "position_offset_y": 0.0},
        f={"position_padding_left": "$si(rwidth)*0.1$", "position_offset_y": "$(df(mm)%5-2)*2$"},
        anims=[
            anim("LOOP_2W", [kf(0, "Y_OFFSET", 0), kf(25, "Y_OFFSET", -6), kf(50, "Y_OFFSET", 0),
                             kf(75, "Y_OFFSET", 6), kf(100, "Y_OFFSET", 0)], duration=20),
            anim("FORMULA", [kf(0, "SCALE_X", 1), kf(0, "OPACITY", 0), kf(100, "SCALE_X", 0),
                             kf(100, "OPACITY", 100)], duration=3, formula="$gv(open)$"),
        ])


# ---------------------------------------------------------------- felfedés: 12 zóna

ZONES = {
    "a": ("[b]$df(HH:mm)$[/b]", "$df(EEEE)$, $df(MMMM d)$"),
    "b": ("[b]$wi(temp)$°[/b]", "$tc(cap,wi(cond))$ · hőérzet $wi(flik)$°"),
    "c": ('$if(ci(title, 0)="","nincs esemény",ci(title, 0))$', '$df("EEE HH:mm", ci(start, 0))$'),
    "d": ('$if(mi(title)="","csend",mi(title))$', "$mi(artist)$"),
    "f": ("[b]$ni(count)$[/b]", "$ni(0, text)$"),
    "g": ("[b]$bi(level)$%[/b]", "$if(bi(source)=Battery,merül,tölt)$"),
    "h": ("ébresztés", '$df("EEE HH:mm", si(alarmd))$'),
    "i": ("holnap ↓$wf(min, 1)$° ↑$wf(max, 1)$°", "$tc(cap,wf(cond, 1))$"),
}


def frame(fw, fh):
    """4 vonal, amelyek egymás után „megrajzolódnak"."""
    lines = []
    specs = [  # (anchor, w, h, prop, anim_anchor)
        ("TOP", fw, "$gv(lw)$", "SCALE_X", "MODULE_LEFT"),
        ("CENTERRIGHT", "$gv(lw)$", fh, "SCALE_Y", "MODULE_TOP"),
        ("BOTTOM", fw, "$gv(lw)$", "SCALE_X", "MODULE_RIGHT"),
        ("CENTERLEFT", "$gv(lw)$", fh, "SCALE_Y", "MODULE_TOP"),
    ]
    for i, (anc, w, h, prop, aanc) in enumerate(specs):
        r = rect(w, h, fw=2, fh=2, fcolor="$gv(c_dim)$", anchor=anc)
        a = appear([(prop, 0), ("OPACITY", 100)], [(prop, 1), ("OPACITY", 0)], delay=i)
        a["anchor"] = aanc
        r["internal_animations"] = [a]
        lines.append(r)
    return lines


def zone(letter, idx):
    col, row = idx % 3, idx // 3
    zw, zh = "$si(rwidth)/3$", "$si(rheight)/4$"
    items = [rect(zw, zh, fw=W / 3, fh=H / 4, title="Érintési felület")]
    if letter in ZONES:
        l1, l2 = ZONES[letter]
        fw, fh = "$si(rwidth)/3*0.85$", "$si(rheight)/4*0.5$"
        content = overlap(
            [rect(fw, fh, fw=200, fh=200)] + frame(fw, fh) + [
                stack([text(l1, size="$(si(rwidth)+si(rheight))/55$"),
                       text(l2, size="$(si(rwidth)+si(rheight))/110$", color="$gv(c_dim)$")],
                      "VERTICAL_CENTER", anchor="CENTER")],
            title="Tartalom " + letter, anchor="CENTER",
            f=vis('gv(z)="%s"&gv(age)<gv(felfedido)&gv(open)=0' % letter),
            anims=[appear([("Y_OFFSET", 10), ("OPACITY", 100)], [("Y_OFFSET", 0), ("OPACITY", 0)])])
        items.append(content)
    return overlap(items, title="Zóna " + letter, anchor="TOPLEFT",
                   props={"position_offset_x": W / 3 * col, "position_offset_y": H / 4 * row},
                   f={"position_offset_x": "$si(rwidth)/3*%d$" % col,
                      "position_offset_y": "$si(rheight)/4*%d$" % row},
                   events=[ev_zone(letter)])


# ---------------------------------------------------------------- vezérlés

CW, CH = "$si(rwidth)*0.8/3$", "$si(rheight)*0.2$"
SMALL = "$(si(rwidth)+si(rheight))/110$"
MID = "$(si(rwidth)+si(rheight))/70$"


def grid_lines():
    out = []
    for i in range(4):
        r = rect("$si(rwidth)*0.8$", "$gv(lw)$", fw=576, fh=2, fcolor="$gv(c_dim)$", anchor="TOPLEFT",
                 title="Rács vízszintes %d" % i,
                 extra_f=dict(vis("gv(open)=1"), position_offset_x="$si(rwidth)*0.1$",
                              position_offset_y="$si(rheight)*(0.2+0.2*%d)$" % i))
        r["internal_animations"] = [anim("FORMULA", [kf(0, "SCALE_X", 0), kf(100, "SCALE_X", 1)], duration=3,
                                         delay=i, formula="$gv(open)$",
                                         anchor="MODULE_LEFT" if i % 2 == 0 else "MODULE_RIGHT")]
        out.append(r)
    for i in range(4):
        r = rect("$gv(lw)$", "$si(rheight)*0.6$", fw=2, fh=960, fcolor="$gv(c_dim)$", anchor="TOPLEFT",
                 title="Rács függőleges %d" % i,
                 extra_f=dict(vis("gv(open)=1"), position_offset_x="$si(rwidth)*(0.1+0.8/3*%d)$" % i,
                              position_offset_y="$si(rheight)*0.2$"))
        r["internal_animations"] = [anim("FORMULA", [kf(0, "SCALE_Y", 0), kf(100, "SCALE_Y", 1)], duration=3,
                                         delay=i, formula="$gv(open)$", anchor="MODULE_TOP")]
        out.append(r)
    return out


def cell(fidx, title, content):
    c = "((%d+gv(rot))%%9)" % fidx
    return overlap(
        [rect(CW, CH, fw=192, fh=320), content], title="Mező %d – %s" % (fidx, title), anchor="TOPLEFT",
        f=dict(vis("gv(open)=1&gv(grp)=0"),
               position_offset_x="$si(rwidth)*0.1+si(rwidth)*0.8/3*(%s%%3)$" % c,
               position_offset_y="$si(rheight)*0.2+si(rheight)*0.2*((%s-%s%%3)/3)$" % (c, c)),
        anims=[appear([("SCALE_XY", 0.8), ("OPACITY", 100)], [("SCALE_XY", 1), ("OPACITY", 0)], delay=fidx % 3)])


def label(t, color="$gv(c_txt)$", size=MID):
    return text(t, size=size, color=color, anchor="CENTER")


def controls():
    bw3, bh = "$si(rwidth)*0.8/9$", "$si(rheight)*0.1$"
    music = stack([
        stack([button(label("«"), bw3, bh, [{"type": "SINGLE_TAP", "action": "MUSIC", "music_action": "PREVIOUS"}]),
               button(label('$if(mi(state)=playing,"II","play")$'), bw3, bh,
                      [{"type": "SINGLE_TAP", "action": "MUSIC", "music_action": "PLAY_PAUSE"}]),
               button(label("»"), bw3, bh, [{"type": "SINGLE_TAP", "action": "MUSIC", "music_action": "NEXT"}])],
              "HORIZONTAL_CENTER"),
        text('$tc(cut,if(mi(title)="","csend",mi(title)),14)$', size=SMALL, color="$gv(c_dim)$")],
        "VERTICAL_CENTER", anchor="CENTER")

    bars = []
    for k, lvl in enumerate([20, 40, 60, 80, 100], start=1):
        bar = rect("$gv(lw)*2$", "$si(rheight)*0.02*%d$" % k, fw=4, fh=30, fcolor="$gv(c_txt)$", anchor="BOTTOM")
        bars.append(overlap([rect("$si(rwidth)*0.8/15$", "$si(rheight)*0.12$"), bar],
                            events=[{"type": "SINGLE_TAP", "action": "CHANGE_VOLUME", "volume_stream": "RINGER",
                                     "volume_action": "SET", "volume_level": float(lvl)}, EV_REFRESH]))
    volume = stack([stack(bars, "HORIZONTAL_BOTTOM"), text("hang", size=SMALL, color="$gv(c_dim)$")],
                   "VERTICAL_CENTER", anchor="CENTER")

    search = button(label("keresés"), CW, CH, [{"type": "SINGLE_TAP", "action": "LAUNCH_APP", "intent": GOOGLE}])

    bw2 = "$si(rwidth)*0.8/6$"
    net = stack([
        button(label("wifi", color="$if(nc(wifi)=connected,gv(c_acc),gv(c_dim))$"), bw2, bh,
               [{"type": "SINGLE_TAP", "action": "KUSTOM_ACTION", "kustom_action": "TOGGLE_WIFI"}]),
        button(label("bt", color="$if(nc(bt)=0,gv(c_dim),gv(c_acc))$"), bw2, bh,
               [{"type": "SINGLE_TAP", "action": "KUSTOM_ACTION", "kustom_action": "TOGGLE_BT"}])],
        "HORIZONTAL_CENTER", anchor="CENTER")

    ring = stack([
        stack([button(label("néma"), bw2, bh, [{"type": "SINGLE_TAP", "action": "CHANGE_VOLUME",
                                                 "volume_stream": "RINGER", "volume_action": "SET",
                                                 "volume_level": 0.0}]),
               button(label("hang"), bw2, bh, [{"type": "SINGLE_TAP", "action": "CHANGE_VOLUME",
                                                 "volume_stream": "RINGER", "volume_action": "SET",
                                                 "volume_level": 70.0}])], "HORIZONTAL_CENTER"),
        text("$si(ringer)$", size=SMALL, color="$gv(c_dim)$")], "VERTICAL_CENTER", anchor="CENTER")

    bw4 = "$si(rwidth)*0.8/12$"
    icons = []
    for n in range(3):
        bmp = node("BitmapModule", None, {"bitmap_width": 30.0},
                   {"bitmap_bitmap": "$ni(%d, icon)$" % n, "bitmap_width": "$si(rwidth)/24$"})
        icons.append(overlap([rect(bw4, bh), bmp], f=vis("ni(count)>%d" % n),
                             events=[{"type": "SINGLE_TAP", "action": "KUSTOM_ACTION",
                                      "kustom_action": "NOTIF_OPEN", "notification": str(n)}, EV_REFRESH]))
    icons.append(button(label("×", color="$gv(c_dim)$"), bw4, bh,
                        [{"type": "SINGLE_TAP", "action": "KUSTOM_ACTION", "kustom_action": "NOTIF_CLOSE_ALL"}],
                        f=vis("ni(count)>0")))
    notif = stack([stack(icons, "HORIZONTAL_CENTER"),
                   text('$if(ni(count)=0,"nincs értesítés",ni(count)+" értesítés")$', size=SMALL,
                        color="$gv(c_dim)$")], "VERTICAL_CENTER", anchor="CENTER")

    cells = [cell(0, "zene", music), cell(1, "hangerő", volume), cell(2, "kereső", search),
             cell(3, "wifi/bt", net), cell(4, "csengő", ring), cell(5, "értesítések", notif)]
    for i, (lbl, grp) in enumerate([("A–I", "1"), ("J–R", "2"), ("S–Z", "3")]):
        cells.append(cell(6 + i, "appok " + lbl,
                          button(label(lbl), CW, CH, [ev_switch("grp", grp)])))
    return cells


def app_lists():
    rw, rh = "$si(rwidth)*0.6$", "$si(rheight)*0.07$"
    lists = []
    for grp, lbl in [("1", "A–I"), ("2", "J–R"), ("3", "S–Z")]:
        rows = [text("[b]%s[/b]" % lbl, size=MID, color="$gv(c_dim)$")]
        for k in range(6):
            r = button(label("app %d" % (k + 1), size=MID), rw, rh, [{"type": "SINGLE_TAP", "action": "DISABLED"}],
                       title="App %s/%d – állítsd be: Launch App" % (lbl, k + 1))
            r["internal_animations"] = [appear([("X_OFFSET", 40), ("OPACITY", 100)],
                                               [("X_OFFSET", 0), ("OPACITY", 0)], delay=k)]
            rows.append(r)
        rows.append(button(label("összes", color="$gv(c_dim)$", size=SMALL), rw, rh,
                           [{"type": "SINGLE_TAP", "action": "LAUNCH_SHORTCUT", "intent": NOVA_DRAWER}]))
        rows.append(button(label("×", color="$gv(c_dim)$"), rw, rh, [ev_switch("grp", "0")]))
        lists.append(stack(rows, "VERTICAL_CENTER", title="App-lista " + lbl, anchor="CENTER",
                           f=vis('gv(open)=1&gv(grp)=%s' % grp)))
    return lists


def debug_line():
    return text("$gv(st)$ · age $gv(age)$ · open $gv(open)$ · z $gv(z)$ · rot $gv(rot)$",
                size="$(si(rwidth)+si(rheight))/140$", color="$gv(c_dim)$", anchor="BOTTOM", title="Debug",
                extra_f=dict(vis("gv(debug)=1"), position_padding_bottom="$si(rheight)*0.03$"))


# ---------------------------------------------------------------- összeállítás

def build_preset():
    # Teljes képernyős fekete alap (a mintákban nem szerepel SOLID háttértípus, így ez a biztos út).
    items = [rect("$si(rwidth)$", "$si(rheight)$", color="#FF000000", fw=W, fh=H, fcolor="$gv(c_bg)$",
                  anchor="CENTER", title="Fekete alap"), day_line()]
    items += [zone(l, i) for i, l in enumerate("abcdefghijkl")]
    items += grid_lines()
    items += controls()
    items += app_lists()
    items.append(debug_line())
    root = {"internal_type": "RootLayerModule", "globals_list": globals_list(),
            "background_color": "#FF000000",
            "internal_toggles": {"background_color": 10},
            "internal_formulas": {"background_color": "$gv(c_bg)$"},
            "viewgroup_items": items}
    info = {"archive": "", "author": "", "description": "Sötét mező – minimál, érintésre ébredő háttér",
            "email": "", "features": "LOCATION WEATHER FORECAST CALENDAR MUSIC NOTIFICATIONS NETWORK_INFO BLUETOOTH",
            "pflags": 0, "hash": None, "height": 1600, "id": str(uuid.uuid4()), "locked": False,
            "release": 382621115, "ts": int(time.time() * 1000), "title": "Sotet mezo", "version": 17,
            "width": 720, "xscreens": 1, "yscreens": 1}
    return {"preset_info": info, "preset_root": root}


def thumb(w, h):
    im = Image.new("RGB", (w, h), (0, 0, 0))
    d = ImageDraw.Draw(im)
    y = h // 2
    x0, x1 = int(w * 0.1), int(w * 0.9)
    d.line([(x0, y), (x1, y)], fill=(26, 26, 26), width=2)
    d.line([(x0, y), (x0 + int((x1 - x0) * 0.62), y)], fill=(70, 70, 70), width=2)
    cx = x0 + int((x1 - x0) * 0.8)
    d.ellipse([cx - 4, y - 4, cx + 4, y + 4], fill=(120, 120, 120))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=85)
    return buf.getvalue()


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                             "SotetMezo.klwp")
    preset = build_preset()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("preset.json", json.dumps(preset, ensure_ascii=False, indent=2))
        z.writestr("preset_thumb_portrait.jpg", thumb(360, 800))
        z.writestr("preset_thumb_landscape.jpg", thumb(800, 360))
    print("kész:", out)


if __name__ == "__main__":
    main()
