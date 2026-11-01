#!/usr/bin/env python3
"""KLWP preset elemző.

Használat:
    python3 -I analyze_klwp.py PRESET.klwp [MÁSIK.klwp ...] [--formulas KIMENET.json]

Mit csinál:
  - kicsomagolja a .klwp fájlt (zip) memóriában, és beolvassa a preset.json-t
  - összeszámolja az elemtípusokat, tulajdonságokat, eseményeket, animációkat,
    globális változókat és a képletekben használt függvényeket
  - a szerzői adatokat (név, e-mail, linkek) NEM írja ki

Csak a Python standard könyvtárát használja.
"""
import collections
import json
import re
import sys
import zipfile

FUNC_RE = re.compile(r"\b([a-z]{2})\(\s*([^,()$]*)")
SKIP_KEYS = {"internal_readonly"}  # zárolt komponensek titkosított tartalma


def nodes(o):
    if isinstance(o, dict):
        yield o
        for k, v in o.items():
            if k not in SKIP_KEYS:
                yield from nodes(v)
    elif isinstance(o, list):
        for x in o:
            yield from nodes(x)


def strings(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k not in SKIP_KEYS:
                yield from strings(v)
    elif isinstance(o, list):
        for x in o:
            yield from strings(x)
    elif isinstance(o, str):
        yield o


def load(path):
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        data = json.loads(z.read("preset.json").decode("utf-8"))
    return data, names


def main(argv):
    out_formulas = None
    if "--formulas" in argv:
        i = argv.index("--formulas")
        out_formulas = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    if not argv:
        print(__doc__)
        return 1

    types = collections.Counter()
    props = collections.defaultdict(collections.Counter)
    events = collections.Counter()
    anim = collections.Counter()
    anim_props = collections.Counter()
    glob = collections.Counter()
    toggles = collections.Counter()
    funcs = collections.defaultdict(collections.Counter)
    formulas = []

    for path in argv:
        data, names = load(path)
        info = data.get("preset_info", {})
        folders = collections.Counter(n.split("/")[0] for n in names if "/" in n)
        print(f"### {path}")
        print("  fájlok:", [n for n in names if "/" not in n], dict(folders))
        print("  méret: %sx%s, képernyők: %sx%s, features: %s" % (
            info.get("width"), info.get("height"), info.get("xscreens"),
            info.get("yscreens"), info.get("features")))
        locked = 0
        for n in nodes(data):
            t = n.get("internal_type")
            if t:
                types[t] += 1
                for k in n:
                    props[t][k] += 1
                if t == "KomponentModule" and n.get("internal_readonly"):
                    locked += 1
            for e in n.get("internal_events") or []:
                events[(e.get("type"), e.get("action"))] += 1
            for a in n.get("internal_animations") or []:
                anim[(a.get("type"), a.get("action"), a.get("ease"))] += 1
                for st in a.get("animator") or []:
                    anim_props[st.get("property")] += 1
            for g in (n.get("globals_list") or {}).values():
                glob[g.get("type")] += 1
            for v in (n.get("internal_toggles") or {}).values():
                toggles[v] += 1
        print("  zárolt komponensek:", locked)
        for s in strings(data):
            if "$" in s and len(s) < 5000:
                formulas.append(s)
                for m in FUNC_RE.finditer(s):
                    fn, arg = m.group(1), m.group(2).strip()[:25]
                    funcs[fn]["<változó>" if fn == "gv" else arg] += 1

    def show(title, counter, n=40):
        print(f"\n== {title}")
        for k, c in counter.most_common(n):
            print(f"  {c:6d}  {k}")

    show("Elemtípusok", types)
    print("\n== Tulajdonságok típusonként")
    for t, c in props.items():
        print(f"  {t}: {', '.join(k for k, _ in c.most_common())}")
    show("Események (type, action)", events)
    show("Animációk (type, action, ease)", anim)
    show("Animált tulajdonságok", anim_props)
    show("Globális változó típusok", glob)
    show("toggles értékek (10=képlet, 0=fix érték, 100=globális)", toggles)
    print("\n== Függvények és első paramétereik")
    for fn in sorted(funcs, key=lambda k: -sum(funcs[k].values())):
        top = ", ".join(f"{a or '∅'}×{c}" for a, c in funcs[fn].most_common(12))
        print(f"  {fn} ({sum(funcs[fn].values())}): {top}")
    print(f"\nÖsszes képlet: {len(formulas)}")
    if out_formulas:
        with open(out_formulas, "w", encoding="utf-8") as f:
            json.dump(sorted(set(formulas)), f, ensure_ascii=False, indent=1)
        print("Képletek mentve:", out_formulas)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
