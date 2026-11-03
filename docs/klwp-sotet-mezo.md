# „Sötét mező” – minimál KLWP koncepció

Teljesen fekete AMOLED képernyő. Alapból csak egy hajszálvékony vonal látszik. Érintésre **csak az érintett zóna** ébred fel egy rövid időre. A vezérlőfunkciók egy **titkos kopogó kód** után jelennek meg, és ekkor a vonalak vezérlőráccsá rendeződnek át.

- Launcher: Nova, 1 oldal, kézi app-hozzárendelés.
- Jelölés: ✅ a 17 példapresetben igazolt · ⚠️ következtetés · 🔧 igazolt elemekből összerakva, nincs kipróbálva · ❓ nem igazolt.
- A méretek a képernyőhöz arányosak (`si(rwidth)`, `si(rheight)`).

> **Ez elrejtés, nem biztonság.** Aki a feloldott telefont a kezében tartja, a Nova gesztusaival (felhúzás → alkalmazásfiók) a háttér nélkül is mindent elér, és a KLWP szerkesztőjében a kód is látható. Az igazi védelem az Android képernyőzár. A koncepció célja, hogy egy kíváncsi kéz ne tudjon „csak úgy” zenét váltani, wifit kapcsolni vagy appot indítani a kezdőképernyőről.

---

## 1. Három állapot

| Állapot | Mi látszik | Mikor |
|---|---|---|
| **Nyugalom** | fekete képernyő + a „napvonal” (lassan lélegzik) | alapból |
| **Felfedés** | egyetlen zóna tartalma 6 mp-ig, vonalkerettel | koppintás egy zónára |
| **Vezérlés** | a vonalak 3×3-as ráccsá rendeződnek, bennük a funkciók | helyes kopogó kód után 45 mp-ig, illetve a képernyő lezárásáig |

```
 NYUGALOM                 FELFEDÉS (zóna 2)          VEZÉRLÉS
┌──────────────┐        ┌──────────────┐        ┌──────────────┐
│              │        │     ┌────┐   │        │  ⏮⏯⏭│ ▁▃▅▇ │ 🔍 │
│              │        │     │12° │   │        │ ─────┼──────┼─── │
│              │        │     │eső │   │        │  ≋ ᛒ │  🔕  │ •••│
│ ───────·──   │        │     └────┘   │        │ ─────┼──────┼─── │
│              │        │ ────·──      │        │  A–I │ J–R  │ S–Z│
│              │        │              │        │                  │
└──────────────┘        └──────────────┘        └──────────────┘
  vonal = a nap eltelt      a vonal keretet           a napvonal
  része, pont = akku        „rajzol” a tartalomnak    rácsvonalakká bomlik
```

---

## 2. Globális változók

### Megjelenés

| Név | Típus | Érték | |
|---|---|---|---|
| `c_bg` | COLOR | `#FF000000` | ✅ |
| `c_line` | COLOR | `#FF2A2A2A` | nyugalmi vonalak |
| `c_txt` | COLOR | `#FFE6E6E6` | |
| `c_dim` | COLOR | `$ce(gv(c_txt),alpha,50)$` | ✅ |
| `c_acc` | COLOR | `#FF7FDBFF` | egyetlen kiemelőszín, takarékosan |
| `fnt` | FONT | vékony betűtípus | ✅ |
| `lw` | NUMBER | `$si(rwidth)/360$` | vonalvastagság (~2 px) |

### Beállítások

| Név | Típus | Érték | |
|---|---|---|---|
| `kod` | TEXT (vagy SECRET) | `cjal` (hal) | a kopogó kód 4 zónabetűje (lásd 3.1). SECRET-ként tárolva védettebb, de hogy a `gv()` olvassa-e, az ❓; ha nem, TEXT |
| `nyitido` | NUMBER | `45` | ennyi mp-ig marad nyitva a vezérlés |
| `felfedido` | NUMBER | `6` | ennyi mp-ig látszik egy felfedett zóna |
| `forgat` | SWITCH | `1` | óránkénti átrendeződés be/ki |
| `debug` | SWITCH | `1` | hibakereső sor a képernyő alján (tesztelés idejére) |

### Állapot (a motor)

| Név | Típus | Érték / képlet | Leírás |
|---|---|---|---|
| `st` | TEXT | kezdőérték: `t100000cxxxx` | **az egész állapot egy szövegben** (lásd 3.2) |
| `now` | TEXT | `$df(H)*3600+df(mm)*60+df(ss)$` | a nap eltelt másodpercei 🔧 |
| `tt` | TEXT | `$tc(cut,gv(st),1,6)-100000$` | az utolsó koppintás ideje ⚠️ |
| `fl` | TEXT | `$tc(cut,gv(st),7,1)$` | `o` = nyitva, `c` = zárva ⚠️ |
| `sq` | TEXT | `$tc(cut,gv(st),8,4)$` | az utolsó 4 koppintott zóna ⚠️ |
| `z` | TEXT | `$tc(cut,gv(st),11,1)$` | a legutóbbi zóna ⚠️ |
| `age` | TEXT | `$if(gv(now)>=gv(tt),gv(now)-gv(tt),gv(now)+86400-gv(tt))$` | hány mp telt el azóta (éjfélen át is) 🔧 |
| `open` | TEXT | `$if(gv(fl)=o & gv(age)<gv(nyitido) & si(locked)=0,1,0)$` | **nyitva van-e a vezérlés** 🔧 |
| `rot` | TEXT | `$if(gv(forgat)=1,df(H)%9,0)$` | átrendeződési eltolás (0–8) 🔧 |
| `grp` | TEXT | `0` | megnyitott app-csoport (0 = nincs, 1–3) |

A `tc(cut, szöveg, kezdet, hossz)` 0-tól számoló kezdőpozícióját a példák alapján következtetem ki (`tc(cut, x, 1, tc(len, x))` = az első karakter utáni rész). ⚠️ Ez a teszt egyik első pontja.

---

## 3. A motor

### 3.1 Zónák

A képernyő **3 oszlop × 4 sor = 12 zóna**, betűjelük sorfolytonosan `a`…`l`:

```
 a | b | c
 d | e | f
 g | h | i
 j | k | l
```

Egy zóna = Overlap csoport:
- anchor `TOPLEFT`; X eltolás: `$si(rwidth)/3*OSZLOP$`; Y eltolás: `$si(rheight)/4*SOR$` (OSZLOP: 0–2, SOR: 0–3 számmal beírva) ✅;
- benne egy **átlátszó** Shape RECT: szélesség `$si(rwidth)/3$`, magasság `$si(rheight)/4$`, szín `#00000000`;
- az esemény a csoporton van (3.2).

Betűket használok számok helyett, mert a `+` csupa számjegyű szövegeket valószínűleg összeadna, nem összefűzne. A példákban az `uc(sms)+uc(calls)` összeadás, a `gv(year)+y+gv(month)+M` összefűzés. ⚠️

### 3.2 Az állapotszöveg és a koppintás képlete

```
 st  =  t  05000  o  cjal
        │  │      │  └─ az utolsó 4 zóna (pozíció 7–10)
        │  │      └──── o = nyitva / c = zárva (pozíció 6)
        │  └─────────── koppintás ideje, 5 jegy (pozíció 1–5)
        └────────────── kezdőbetű, hogy a szöveg biztosan ne legyen szám
```

**Minden zóna eseménye:** `SWITCH_GLOBAL`, switch: `st`, és a switch_text képlete az „a” zónánál (a többinél csak az utolsó `"a"` betű más):

```
$"t"+(gv(now)+100000)+if(gv(open)=1|tc(cut,gv(sq),1,3)+"a"=gv(kod),"o","c")+tc(cut,gv(sq),1,3)+"a"$
```

Jelentése: új idő + (ha eddig is nyitva volt, VAGY az utolsó 3 zóna + ez a mostani = a kód, akkor `o`, különben `c`) + az utolsó 4 zóna léptetve.

- ✅ A `switch_text` lehet képlet, ami a saját korábbi értékére hivatkozik (a példák hírléptetője így működik).
- 🔧 Az összetett képlet a teszt legfontosabb pontja.
- **Rossz kód esetén nincs semmilyen visszajelzés**: kívülről csak a zóna felfedése látszik.
- A nyitott állapot minden zónakoppintással megújul (újra 45 mp). A vezérlőgombok koppintása viszont nem frissíti, mert az más esemény. 45 mp elég egy-egy műveletre. Ha kevés, a `nyitido` növelhető.

### 3.3 Hibakereső sor (`debug`)

Text a képernyő alján, csak ha `debug=1`:

```
$gv(st)$ · age $gv(age)$ · open $gv(open)$ · z $gv(z)$ · sq $gv(sq)$
```

Ezzel tesztelés közben pontosan látod, mit csinál a motor. Utána kikapcsolod.

---

## 4. Nyugalom: a napvonal

| Elem | Mező | Képlet | |
|---|---|---|---|
| Vonal (Shape RECT) | anchor | CENTERLEFT, bal margó `$si(rwidth)*0.1$` | ✅ |
| | szélesség | `$si(rwidth)*0.8*(df(H)*60+df(mm))/1440$` | 🔧 a nap eltelt része |
| | magasság / szín | `$gv(lw)$` / `$gv(c_line)$` | ✅ |
| Halvány „hátralévő” vonal | szélesség | `$si(rwidth)*0.8$`, szín `$ce(gv(c_line),alpha,40)$` | 🔧 |
| Akkupont (Shape CIRCLE) | X eltolás | `$si(rwidth)*0.1+si(rwidth)*0.8*bi(level)/100$` | 🔧 |
| | méret / szín | `$gv(lw)*3$` / `$if(bi(level)<20,#FFFF5252,gv(c_dim))$` | 🔧 |
| | töltés közben pulzál | animáció type: `$if(bi(source)=Battery,disabled,loop_2w)$`, `SCALE_XY` 1 → 1.6 | 🔧 |
| Az egész csoport | lélegzés | `LOOP_2W`, `ADVANCED`, `Y_OFFSET` 0 → −6 → 0 → 6 → 0 (0/25/50/75/100%), duration 20 | ✅ minta |
| | elrejtés vezérléskor | `FORMULA` animáció, formula `$gv(open)$`, `SCALE_X` 1 → 0 | 🔧 a vonal „szétbomlik” |
| | beégésvédelem | Y eltolás: `$(df(mm)%5-2)*2$` | 🔧 |

Egy idegen ebből csak egy díszvonalat lát. Te tudod, hogy a hossza az idő, a pont pedig az akku.

---

## 5. Felfedés

Minden zónához tartozik egy tartalomcsoport (a zónacsoporton belül, a koppintási alakzat alatt):

- láthatóság: `$if(gv(z)=a & gv(age)<gv(felfedido) & gv(open)=0,always,remove)$` (zónánként a saját betűjével) 🔧
- **vonalkeret, ami „megrajzolódik”:** 4 hajszálvékony Shape (felső, alsó, bal, jobb). Mindegyik `VISIBILITY` animációval, `SCALE_X` (vízszintes) vagy `SCALE_Y` (függőleges) 0 → 1, anchor `MODULE_LEFT` / `MODULE_TOP`, egymás után 0 / 0,2 / 0,4 / 0,6 mp késleltetéssel. ✅ (`SCALE_X`/`SCALE_Y`, `MODULE_*` anchor, `delay` a példákban)
- a tartalom `VISIBILITY` animációval, `Y_OFFSET` 10 → 0. ✅ (Az `OPACITY` irányát tesztelni kell. ❓)

### Zónák tartalma (javaslat, átírható)

| Zóna | Tartalom | Képlet |
|---|---|---|
| a | idő + dátum | `[b]$df(HH:mm)$[/b]` / `[s=0.6]$df(EEEE)$, $df(MMMM d)$[/s]` ✅ |
| b | időjárás most | `[b]$wi(temp)$°[/b]` / `[s=0.6]$tc(cap,wi(cond))$ · hőérzet $wi(flik)$°[/s]` ✅ |
| c | következő esemény | `$if(ci(title, 0)="","nincs esemény",ci(title, 0))$` / `[s=0.6]$df("EEE HH:mm", ci(start, 0))$[/s]` 🔧 |
| d | zene | `$if(mi(title)="","csend",mi(title))$` / `[s=0.6]$mi(artist)$[/s]` ✅ |
| e | (üres – kódnak jó) | – |
| f | értesítések | `[b]$ni(count)$[/b]` / `[s=0.6]$ni(0, text)$[/s]` ✅ |
| g | akku | `[b]$bi(level)$%[/b]` / `[s=0.6]$if(bi(source)=Battery,merül,tölt)$[/s]` ✅ |
| h | ébresztés | `$df("EEE HH:mm", si(alarmd))$` ✅ (ébresztés nélküli viselkedése ❓) |
| i | holnap | `holnap ↓$wf(min, 1)$° ↑$wf(max, 1)$°` / `[s=0.6]$tc(cap,wf(cond, 1))$[/s]` 🔧 |
| j, k, l | (üres – kódnak jó) | – |

**A kód: „halacska”** – jobb fent (`c`) → bal lent (`j`) → bal fent (`a`) → jobb lent (`l`) = `cjal`. Nem rajzolni, hanem a négy sarokra egymás után koppintani kell (a KLWP a húzást nem érzékeli). A `kod` globálisban átírható.

**Generált preset:** `klwp/sotet-mezo/SotetMezo.klwp`, generátor: `klwp/sotet-mezo/build.py`.

---

## 6. Vezérlés: a vonalak ráccsá rendeződnek

### 6.1 Rácsvonalak

- 2 vízszintes és 2 függőleges hajszálvonal a képernyő középső 60%-án, plusz egy külső keret.
- Mindegyik: `FORMULA` animáció, formula `$gv(open)$`, `ADVANCED`.
  - vízszintes: `SCALE_X` 0 → 1 (anchor `MODULE_LEFT`, illetve a második `MODULE_RIGHT`, hogy két irányból „fussanak be”);
  - függőleges: `SCALE_Y` 0 → 1 (`MODULE_TOP`, illetve `MODULE_BOTTOM` ❓ – az utóbbi nem szerepelt a példákban);
  - duration 1–1,5 mp, kis eltolással. 🔧
- Láthatóság: `$if(gv(open)=1,always,remove)$` ✅

A `FORMULA` animáció 0/1 eredményét a példák pontosan így használják (`$if(gv(txta)=1,1,0)$` + `SCALE_XY` 0 → 1). ✅

### 6.2 A 9 funkciómező és az átrendeződés

Minden funkció egy Overlap csoport, a helyét **képlet** adja (F = a funkció sorszáma 0–8, beírva):

```
cella:    (F + gv(rot)) % 9
X eltolás: $si(rwidth)*0.1 + si(rwidth)*0.8/3 * ((F+gv(rot))%9 % 3)$
Y eltolás: $si(rheight)*0.2 + si(rheight)*0.6/3 * (((F+gv(rot))%9 - (F+gv(rot))%9%3)/3)$
```
🔧 (`%`, eltolás-képletek ✅; a sima átúszás az új helyre ❓, ha nincs, a mezők óraváltáskor „átpattannak”)

A mező tartalma a kereten belül, a koppintás a saját eseményein. Láthatóság: `$if(gv(open)=1 & gv(grp)=0,always,remove)$`. Megjelenés: `VISIBILITY` animáció, `SCALE_XY` 0,8 → 1, `ease: OVERSHOOT`. ✅

| F | Funkció | Belső felépítés | Események |
|---|---|---|---|
| 0 | **Zene** | Stack vízszintes: 3 alzóna ⏮ ⏯ ⏭ + alul apró cím | `MUSIC` `PREVIOUS` / `PLAY_PAUSE` / `NEXT` ✅; ikon: `$if(mi(state)!=playing,Play,Pause)$` (materialdesignicons) ✅ |
| 1 | **Hangerő** | 5 egyre magasabb függőleges vonal (mint egy hangszínszabályzó) | mindegyik `CHANGE_VOLUME` `SET` `20`/`40`/`60`/`80`/`100` ✅ (RINGER; média ❓) |
| 2 | **Kereső** | nagyító ikon | `LAUNCH_APP` → Google (`com.google.android.googlequicksearchbox/.SearchActivity`) ✅ |
| 3 | **Wifi / BT** | 2 alzóna | `KUSTOM_ACTION` `TOGGLE_WIFI` / `TOGGLE_BT` ✅; szín: `$if(nc(wifi)=connected,gv(c_acc),gv(c_dim))$` ✅ |
| 4 | **Csend / hang** | 2 alzóna | `CHANGE_VOLUME` RINGER `SET` `0` / `70` 🔧; ikon: `$if(si(ringer)=normal,Volume-low,if(si(ringer)=silent,Volume-variant-off,Volume-vibrate))$` ✅ |
| 5 | **Értesítések** | 3 ikon (`$ni(0, icon)$` … `$ni(2, icon)$`, BitmapModule) + „×” | `NOTIF_OPEN` 0/1/2 ✅⚠️ (0 vagy 1-től számol?), `NOTIF_CLOSE_ALL` ✅ |
| 6 | **Appok A–I** | felirat `A–I` | `SWITCH_GLOBAL` `grp` switch_text `1` ✅ |
| 7 | **Appok J–R** | `J–R` | `grp` = `2` |
| 8 | **Appok S–Z** | `S–Z` | `grp` = `3` |

### 6.3 App-listák

- 3 Stack (vertikális), láthatóság: `$if(gv(open)=1 & gv(grp)=1,always,remove)$` (illetve 2, 3).
- Soronként egy Text az app nevével + `LAUNCH_APP` (az alkalmazásban kiválasztva). Legfeljebb 8 sor.
- Megjelenés lépcsőzetesen: soronként `VISIBILITY` animáció, `X_OFFSET` 40 → 0, késleltetés 0 / 0,1 / 0,2 … ✅
- Utolsó sor `×`: `SWITCH_GLOBAL` `grp` = `0`. Legalul „összes”: `LAUNCH_SHORTCUT` → Nova `APP_DRAWER` ✅.
- Mivel a láthatóság az `open`-t is nézi, lezáráskor a lista is eltűnik. A `grp` viszont `1` marad, így a következő nyitáskor a lista nyílik meg. Ezt a „×” rendezi, vagy a `grp` képlete kiegészíthető. ⚠️

---

## 7. Nova beállítások

- Ikonok, dokk és keresősáv ki (üres oldal).
- **A gesztusok kikapcsolása vagy átállítása**, különösen a felhúzás → alkalmazásfiók. Különben bárki a háttér nélkül is mindenhez hozzáfér. ❓ (a menüpont pontos neve)
- A KLWP háttérként beállítva; a koppintás továbbítását a Nova tudomásom szerint támogatja. ❓

## 8. Akku

A másodpercre pontos időzítés (`df(ss)` a `now`-ban) másodpercenkénti újraszámolást jelent. A lélegzés pedig folyamatos animáció. Ha ez sokat merít:
- a felfedés és a nyitás percalapú is lehet (`now` = `df(H)*60+df(mm)`, `nyitido` = 1);
- a lélegzés kikapcsolható, vagy csak feloldott képernyőn futhat (`si(locked)` ✅).

---

## Tesztelt (Érintésteszt, a felhasználó telefonján)

- ✅ a koppintás átlátszó felületen és a motor képlete működik
- ✅ `tc(cut, s, kezdet, hossz)` 0-tól számol; ✅ `"x"+1+2` = `x12` (összefűz)
- ✅ a később felvett elem kerül felülre; ✅ `si(locked)`
- ❌ a `+` összefűzés elhagyja a vezető nullákat (`"t"+tc(lpad,5,5,0)` = `t5`) → **új állapotformátum: `t` + jelző (`o`/`c`) + utolsó 4 zóna + idő a végén**, pl. `tocjal83854`. Így nincs szükség kitöltésre; `tt` = `tc(cut,gv(st),6,tc(len,gv(st))-6)`, `fl` = 1. karakter, `sq` = 2–5., `z` = 5.
- A felfedésből kikerültek az animációk; tesztmódban (`debug=1`) a zónák kerete és betűje látszik, az utoljára érintett zöld
- Az animációkból kikerült az `OPACITY` (az iránya bizonytalan)

## 9. Tesztelési terv – 0. fázis (5–6 elem)

Mielőtt bármi más készül, ezeket kell kipróbálni a `debug` sorral:

| # | Teszt | Mit kell látni | Ha nem működik |
|---|---|---|---|
| 1 | 2 átlátszó zóna (`a`, `b`) eseménnyel | koppintásra változik a `st` a debug sorban | a zónába egy alig látható (`#01000000`) alakzat kell |
| 2 | `tc(cut, gv(st), 1, 5)` stb. | a `tt`, `fl`, `sq`, `z` helyes részeket ad | a kezdőpozíció 1-től számol → minden pozíció +1 |
| 3 | `"t"+tc(lpad,...)+...` | a `st` betűvel kezdődik, a vezető nullák megmaradnak | más elválasztó vagy formátum kell |
| 4 | `age` | másodpercenként nő, 6 után a felfedés eltűnik | a frissítés nem másodperces → percalapú változat |
| 5 | kód: 4 koppintás | `fl` → `o`, `open` → 1, 45 mp múlva → 0 | a koppintás-képlet hibáját a debug sor mutatja |
| 6 | `remove`-val rejtett réteg | a rejtett réteg nem fogadja a koppintást | a rétegek sorrendjét kell átrendezni |
| 7 | `si(locked)` | lezárás és feloldás után `open` = 0 | a lezárás nem bezár, csak az időkorlát |
| 8 | `FORMULA` animáció `$gv(open)$`-del | a vonal szétbomlik, a rács befut | `SWITCH` típusú segédváltozó kell |

## 10. Építési sorrend

1. **0. fázis** (fent) – a motor.
2. Napvonal + akkupont + lélegzés.
3. A 12 zóna felfedéssel (az első zónát kész állapotig, majd másolás).
4. Rácsvonalak + a 9 funkciómező fix helyen.
5. Átrendeződés (`rot`).
6. App-listák.
7. Finomhangolás: időzítések, színek, animációk; a `debug` ki.
