#!/usr/bin/env python3
"""Érintésteszt KLWP preset – a Sötét mező hibakereséséhez.

Használat: python3 -I build_teszt.py [kimenet.klwp]

Négy nagy, LÁTHATÓ gomb, mindegyik egyre összetettebb koppintás-műveletet próbál ki,
és kiírja az eredményét. Mellette képlet- és rétegsorrend-tesztek.
"""
import json
import os
import sys
import time
import uuid
import zipfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sotet-mezo"))
import build as B  # noqa: E402  (a Sötét mező segédfüggvényei)

SIZE = "$(si(rwidth)+si(rheight))/42$"
SMALL = "$(si(rwidth)+si(rheight))/55$"


def box(n, title, result_expr, events, color="#FF303030"):
    """Látható, kitöltött gomb: szám + leírás + élő eredmény."""
    bw, bh = "$si(rwidth)*0.92$", "$si(rheight)*0.12$"
    content = B.stack([
        B.text("[b]%d. %s[/b]" % (n, title), size=SIZE, color="#FFFFFFFF"),
        B.text(result_expr, size=SMALL, color="#FFB0B0B0")], "VERTICAL_CENTER", anchor="CENTER")
    return B.overlap([B.rect(bw, bh, color=color, fw=576, fh=176), content],
                     title="Teszt %d" % n, events=events)


def globals_list():
    g = B.globals_list()          # a Sötét mező összes globálisa (st, now, age, open ...)
    for name, gtype, val in [("s1", "SWITCH", 0), ("t2", "TEXT", "nem"), ("t3", "TEXT", "0")]:
        g[name] = {"index": len(g) + 1, "type": gtype, "title": name, "description": "teszt", "value": val}
    return g


def build():
    tests = B.stack([
        box(1, "kapcsoló (SWITCH)", "s1 = $gv(s1)$  (koppintásra 0 ↔ 1)",
            [{"type": "SINGLE_TAP", "action": "SWITCH_GLOBAL", "switch": "s1"}]),
        box(2, "szöveg beállítása", "t2 = $gv(t2)$  (koppintásra: igen)",
            [B.ev_switch("t2", "igen")]),
        box(3, "képletes számláló", "t3 = $gv(t3)$  (koppintásonként +1)",
            [B.ev_switch("t3", "$gv(t3)+1$")]),
        box(4, "Sötét mező motor (zóna a)", "st = $gv(st)$  ·  age $gv(age)$  ·  open $gv(open)$",
            [B.ev_zone("a")]),
        B.stack([
            B.text("[b]Képletek[/b]", size=SIZE, color="#FFFFFFFF"),
            B.text("now = $gv(now)$   ·   mp = $df(ss)$  (másodpercenként nő?)", size=SMALL, color="#FFB0B0B0"),
            B.text('cut = $tc(cut,"abcdef",1,3)$   (bcd = 0-tól számol, abc = 1-től)', size=SMALL,
                   color="#FFB0B0B0"),
            B.text('lpad = $"t"+tc(lpad,5,5,0)$   (elvárt: t00005)', size=SMALL, color="#FFB0B0B0"),
            B.text('összefűzés = $"x"+1+2$   (x12 vagy x3?)', size=SMALL, color="#FFB0B0B0"),
            B.text("locked = $si(locked)$", size=SMALL, color="#FFB0B0B0"),
        ], "VERTICAL_CENTER"),
    ], "VERTICAL_CENTER", anchor="CENTER", title="Tesztek")

    # Rétegsorrend: két egymásra tett négyzet ugyanott. A látható szín mutatja, melyik van felül.
    order = [
        B.rect("$si(rwidth)*0.12$", "$si(rwidth)*0.12$", color="#FFE53935", fw=86, fh=86, anchor="TOPRIGHT",
               title="Első (piros)"),
        B.rect("$si(rwidth)*0.12$", "$si(rwidth)*0.12$", color="#FF43A047", fw=86, fh=86, anchor="TOPRIGHT",
               title="Második (zöld)"),
        B.text("felül lévő szín →", size=SMALL, color="#FFB0B0B0", anchor="TOPRIGHT",
               extra_f={"position_padding_right": "$si(rwidth)*0.14$"}),
    ]
    root = {"internal_type": "RootLayerModule", "globals_list": globals_list(),
            "background_color": "#FF000000", "viewgroup_items": order + [tests]}
    info = {"archive": "", "author": "", "description": "Érintésteszt a Sötét mezőhöz", "email": "",
            "features": "", "pflags": 0, "hash": None, "height": 1600, "id": str(uuid.uuid4()), "locked": False,
            "release": 382621115, "ts": int(time.time() * 1000), "title": "Erintesteszt", "version": 17,
            "width": 720, "xscreens": 1, "yscreens": 1}
    return {"preset_info": info, "preset_root": root}


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                             "Erintesteszt.klwp")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("preset.json", json.dumps(build(), ensure_ascii=False, indent=2))
        z.writestr("preset_thumb_portrait.jpg", B.thumb(360, 800))
        z.writestr("preset_thumb_landscape.jpg", B.thumb(800, 360))
    print("kész:", out)


if __name__ == "__main__":
    main()
