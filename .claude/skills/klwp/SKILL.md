---
name: klwp
description: KLWP (Kustom Live Wallpaper, Android) élő háttérképek tervezése és kódolása — képletek ($...$ formula language: gv, df, wi, mi, bi, si, if, ce, ni, nc, uc, tc, mu, tf, wg, ci, rm, li, tu), globális változók, elemek, érintési események, animációk, és .klwp preset fájlok (zip + preset.json) elemzése. Használd, ha a felhasználó KLWP/Kustom háttérképet, KWGT widgetet, Kustom képletet vagy .klwp/.komp fájlt említ, vagy élő Android háttérképet szeretne funkciókkal (óra, időjárás, zene, akkumulátor, értesítések, naptár).
---

# KLWP skill

Ez a skill három valódi KLWP preset (összesen kb. 9000 képlet, 2400 elem) elemzéséből készült. A szabályok forrását mindenhol jelöljük:

- ✅ **Igazolt**: a példafájlokban szerepel, a jelentése egyértelmű.
- ⚠️ **Megfigyelt**: a példafájlokban szerepel, de a pontos jelentése következtetés.
- ❓ **Nem igazolt**: a példákban nem szerepel, csak általános tudás. Mindig mondd meg a felhasználónak, hogy ellenőrizze az alkalmazás képletszerkesztőjében.

**Soha ne találj ki függvényt vagy paramétert.** Ha valami nincs a `reference/fuggvenyek.md`-ben ✅ vagy ⚠️ jelöléssel, akkor ❓-ként jelöld, vagy kérdezz.

## Referenciák (olvasd be, amikor kell)

- `reference/fuggvenyek.md` — a képletnyelv szintaxisa, operátorok, minden függvény a látott paraméterekkel. **Képletírás előtt mindig olvasd be.**
- `reference/mintak.md` — kész, bevált képletminták (óra, üdvözlés, időjárás, zene, akksi, értesítések, wifi/bt, témaváltás, reszponzív méretezés).
- `reference/fajlformatum.md` — a `.klwp` fájl belső szerkezete: elemtípusok, tulajdonságnevek, `toggles` kódok, globális változók, események, animációk JSON-formája. Akkor kell, ha fájlt elemzel, vagy a felhasználó azt kérdezi, mi hol van.
- `scripts/analyze_klwp.py` — új preset elemzése: `python3 -I .claude/skills/klwp/scripts/analyze_klwp.py FÁJL.klwp [--formulas ki.json]`. A szerzői adatokat nem írja ki.

## Alapszabályok röviden

1. A képlet `$` jelek között van: `$df(HH:mm)$`. Egy szövegben több is lehet, és keverhető sima szöveggel: `$wi(temp)$°$wi(tempu)$`. ✅
2. Feltétel: `if(feltétel, igaz, hamis)`, és **több ág egy if-ben**: `if(f1, e1, f2, e2, ..., különben)`. ✅
3. Operátorok: `=`, `!=`, `<`, `>`, `<=`, `>=`, `&` (és), `|` (vagy), `+ - * / %`, zárójelezés. ✅
4. Szöveg idézőjel nélkül is működik (`never`, `Unknown Artist`), de szóközös/vesszős szöveget tegyél `"..."` közé. ✅
5. **Felsorolt értékek képletből kisbetűvel**: `always`, `never`, `remove`, `radial`, `none`, `stroke`, `fill`, `solid`, `image`, `desaturate`, `loop_2w`, `disabled`. A JSON-ban tárolt fix értékek nagybetűsek (`ALWAYS`, `RADIAL`). ✅
6. Színek `#AARRGGBB` formában (`#FF181818`), színműveletek `ce()`-vel. ✅
7. Méretezz a képernyőhöz, ne fix pixelre: `$(si(rwidth)+si(rheight))/116$`, `$si(rwidth)*3.475/100$`. Mindhárom preset így csinálja. ✅
8. Egy témát globális változókra építs (szín, betűtípus, kapcsolók), és az elemek ezekre hivatkozzanak `gv()`-vel. Ez a példák legfontosabb mintája (a képletek ~65%-a `gv()`). ✅

## Munkamenet

1. **Tisztázd a célt**: milyen funkciók kellenek (óra, időjárás, zene, akksi, értesítések, naptár, alkalmazásindítók, oldalak), milyen stílus, hány képernyő.
2. **Tervezd meg a globálisokat** (színek, betűk, kapcsolók). Adj nekik rövid, beszédes nevet és leírást.
3. **Írd le az elemfát**: mely csoportban (Overlap/Stack) milyen elem (Text, Shape, FontIcon, Progress) legyen. Az összerakást a felhasználó végzi az alkalmazásban, ezért a lépéseket a KLWP felületének fogalmaival írd le (például „Items → + → Text”). A menüpontok pontos nevét ❓-ként kezeld.
4. **Add meg a képleteket tulajdonságonként** (melyik mezőbe mi kerül). Használd a `reference/mintak.md` mintáit.
5. **Jelezd a tesztelés szükségességét**: a képleteket csak az alkalmazás tudja kiértékelni, itt nem lehet futtatni.

## Amit NE csinálj

- Ne generálj `.klwp` fájlt úgy, mintha biztosan működne. A szerkezet ismert (lásd `fajlformatum.md`), de hogy a KLWP elfogad-e egy generált fájlt, az **nincs tesztelve**. Ha a felhasználó mégis kéri, kísérletiként add át, és kérd, hogy próbálja ki.
- A zárolt komponensek (`KomponentModule` + `internal_readonly`) tartalma titkosított, abból nem lehet tanulni.
- Ne másold a példapresetek szerzői adatait (név, e-mail, linkek) semmilyen kimenetbe.
