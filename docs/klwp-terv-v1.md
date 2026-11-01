# „Okos sáv” KLWP háttér – terv v1

Fekete AMOLED háttér, középen digitális óra időjárással, alatta keresősáv, a jobb szélen egy több funkciót ellátó „okos sáv”, amelynek a módját egy karika választja ki.

- Launcher: **Nova**, **1 kezdőképernyő-oldal**, alkalmazások **kézi hozzárendeléssel**.
- Jelölés: ✅ a 17 példapresetben igazolt · ⚠️ következtetés · 🔧 igazolt elemekből összerakva, nincs kipróbálva · ❓ nem igazolt, tesztelni kell.
- A méretek mindenhol a képernyőhöz arányosak (`si(rwidth)`, `si(rheight)`), így a telefon típusa nem számít.

---

## 1. Elrendezés

```
┌───────────────────────────────────┐
│                               ┌─┐ │
│                               │◉│ │ ← MÓDKARIKA (akkuív körülötte)
│                               ├─┤ │
│          Jó estét             │ │ │
│                               │ │ │
│           21:47               │ │ │ ← OKOS SÁV
│    12° · Felhős               │ │ │   (N db érintési zóna,
│    ↓8° ↑15° · holnap: eső     │ │ │    a módtól függően)
│                               │ │ │
│  ┌──────────────────────┐     │ │ │
│  │ 🔍  Keresés           │     │ │ │
│  └──────────────────────┘     └─┘ │
│    ⏰ H 6:30 · Fogorvos 10:00      │
└───────────────────────────────────┘
```

| Rész | Hely | Méret (a képernyőhöz képest) |
|---|---|---|
| Óra-blokk | középen, a magasság 35%-ánál | szélesség 70% |
| Keresősáv | az óra alatt | szélesség 70%, magasság 6% |
| Infósor | a keresősáv alatt | 1 sor |
| Módkarika | jobb szél, a magasság 15%-ánál | átmérő a szélesség 11%-a |
| Okos sáv | jobb szél, a karika alatt | szélesség 11% (érinthető), magasság 60% |

**Android-gesztus figyelmeztetés:** gesztusnavigációnál a jobb szélről befelé húzás a „vissza” mozdulat. Ez a sávot nem zavarja, mert **koppintással** használjuk, nem húzással. A látható csík legyen a szélen, de az érintési zóna kicsit befelé is nyúljon.

---

## 2. Globális változók

Egyszerű, mappák nélküli nevek, hogy kézzel könnyű legyen felvenni őket.

### Megjelenés

| Név | Típus | Érték | Leírás |
|---|---|---|---|
| `bg` | COLOR | `#FF000000` | háttér (tiszta fekete, AMOLED) |
| `txt` | COLOR | `#FFE6E6E6` | fő szövegszín (nem teljesen fehér) |
| `txt2` | COLOR | képlet: `$ce(gv(txt),alpha,55)$` | halvány szöveg ✅ |
| `acc` | COLOR | `#FF4FC3F7` | kiemelő szín |
| `fnt` | FONT | tetszőleges vékony betűtípus | az óra betűtípusa |
| `animspd` | NUMBER | `3` | animációsebesség |

### Működés

| Név | Típus | Érték | Leírás |
|---|---|---|---|
| `mod` | LIST | entries: `zene,hang,abc,kapcs,ertes` · value: `zene` | a sáv kiválasztott módja |
| `automusic` | SWITCH | `1` | lejátszáskor a sáv magától zene módra vált |
| `aktmod` | TEXT | képlet: `$if(gv(automusic)=1&mi(state)=playing,zene,gv(mod))$` | **a ténylegesen aktív mód**; a láthatóság mindenhol ezt nézi ✅ (TEXT globális képlettel) |
| `abc` | TEXT | `0` | az ABC módban kiválasztott betűcsoport (0 = nincs) |
| `fc` | SWITCH | `0` | előrejelzés panel nyitva/zárva |

Fontos: a mód **váltása** a `mod`-ot lépteti, a **megjelenítés** viszont mindenhol az `aktmod`-ot figyeli.

---

## 3. Elemfa

```
Root (háttér: szín, gv(bg))
├── [Overlap] Óra-blokk                         (anchor: CENTER)
│   ├── Text  üdvözlés
│   ├── Text  óra
│   ├── Text  időjárás most
│   ├── Text  mai/holnapi előrejelzés
│   └── esemény: koppintás → fc kapcsolása
├── [Overlap] Előrejelzés panel                 (csak ha fc=1)
│   └── [Stack vertikális] 5 sor: nap · állapot · min/max
├── [Overlap] Keresősáv
│   ├── Shape  lekerekített téglalap (körvonal)
│   ├── FontIcon  nagyító
│   ├── Text   "Keresés"
│   └── esemény: LAUNCH_APP → Google keresés
├── Text  infósor (ébresztés · következő esemény)
├── [Overlap] Módkarika                          (anchor: TOPRIGHT)
│   ├── Progress  akkuív (kör)
│   ├── Shape  kör
│   ├── FontIcon / Text  mód ikon
│   └── esemény: SWITCH_GLOBAL mod NEXT
└── [Overlap] Okos sáv                           (anchor: CENTERRIGHT)
    ├── Shape  vékony vezetőcsík (mindig látszik)
    ├── [Stack vertikális] ZENE     (látható: aktmod=zene)
    ├── [Stack vertikális] HANG     (látható: aktmod=hang)
    ├── [Stack vertikális] ABC      (látható: aktmod=abc)
    ├── [Overlap] ABC app-lista     (látható: aktmod=abc & abc!=0)
    ├── [Stack vertikális] KAPCS    (látható: aktmod=kapcs)
    └── [Stack vertikális] ERTES    (látható: aktmod=ertes)
```

---

## 4. Elemek és képletek

### 4.1 Óra-blokk

| Elem | Mező | Érték / képlet | |
|---|---|---|---|
| Üdvözlés | szöveg | `$if(df(H)<4,"Jó éjszakát",df(H)<10,"Jó reggelt",df(H)<18,"Szép napot",df(H)<22,"Jó estét","Jó éjszakát")$` | 🔧 |
| | szín | `$gv(txt2)$` | ✅ |
| | méret | `$(si(rwidth)+si(rheight))/120$` | ✅ minta |
| Óra | szöveg | `$df(HH:mm)$` | ✅ |
| | betűtípus | globális: `fnt` | ✅ |
| | méret | `$(si(rwidth)+si(rheight))/14$` | 🔧 |
| | szín | `$gv(txt)$` | ✅ |
| Időjárás most | szöveg | `$wi(temp)$°  ·  $tc(cap,wi(cond))$` | ✅ |
| Előrejelzés sor | szöveg | `↓$wf(min, 0)$°  ↑$wf(max, 0)$°  ·  holnap: $tc(low,wf(cond, 1))$` | 🔧 (a `wf(min, n)`, `wf(cond, n)`, `tc(low)` külön-külön ✅) |
| | szín | `$gv(txt2)$` | ✅ |
| Csoport | esemény | koppintás → `SWITCH_GLOBAL`, switch: `fc` | ✅ |
| Csoport | X eltolás (**beégésvédelem**) | `$(df(mm)%3-1)*2$` | 🔧 percenként −2 / 0 / +2 px |

Az állapotszöveg (`wi(cond)`) nyelve a telefon/időjárás-szolgáltató beállításától függ. ❓

### 4.2 Előrejelzés panel

- Csoport láthatósága: `$if(gv(fc)=1,always,remove)$` ✅
- Megjelenés: `SWITCH` animáció, trigger: `fc`, `ADVANCED`, `Y_OFFSET` 40 → 0 és `OPACITY` (az irányát tesztelni kell ❓).
- 5 sor (n = 1…5), soronként:

| Mező | Képlet | |
|---|---|---|
| Nap | `$df(EEE, a1d)$` … `$df(EEE, a5d)$` | 🔧 (`df(EEE)` és `a1d` külön ✅) |
| Állapot | `$tc(cap,wf(cond, 1))$` … `wf(cond, 5)` | ✅ |
| Min/max | `$wf(min, 1)$° / $wf(max, 1)$°` | ✅ |

### 4.3 Keresősáv

| Elem | Mező | Érték | |
|---|---|---|---|
| Shape | típus / sarok | RECT, sarok: magasság fele | ✅ |
| | festés | STROKE, szín `$ce(gv(txt),alpha,30)$` | ✅ |
| FontIcon | ikon | nagyító (a listából kiválasztva) | ❓ ikonnév |
| Text | szöveg | `Keresés` · szín `$gv(txt2)$` | ✅ |
| Csoport | esemény | `LAUNCH_APP` → **Google** (component: `com.google.android.googlequicksearchbox/.SearchActivity`) | ✅ a példákban így szerepel |

Alternatíva: `LAUNCH_SHORTCUT` → Nova művelet `TEXT_SEARCH` (a Nova saját keresője, ami appokat is talál). ✅

### 4.4 Infósor

```
$if(ci(title, 0)="","",ci(title, 0)+"  "+df(HH:mm, ci(start, 0)))$
```
🔧 (a `ci(title, n)`, `ci(start, n)` és a `df(formátum, ci(start, n))` külön-külön ✅)

Ébresztés eléje: `⏰ $df("EEE HH:mm", si(alarmd))$  ·  ` ✅. Hogy ébresztés nélkül mit ad a `si(alarmd)`, az ❓, ezért első körben teszteld.

### 4.5 Módkarika

| Elem | Mező | Érték / képlet | |
|---|---|---|---|
| Progress (akkuív) | stílus | CIRCLE | ✅ |
| | szint | `$bi(level)$` | ✅ |
| | szín | `$if(bi(level)<20,#FFFF5252,gv(acc))$` | 🔧 |
| Shape | típus | CIRCLE, szín `#FF111111` | ✅ |
| Mód ikon (FontIcon, materialdesignicons) | ikon | `$if(gv(aktmod)=zene,Play,gv(aktmod)=hang,Volume-low,gv(aktmod)=kapcs,Wifi,gv(aktmod)=ertes,Bell,Play)$` | ✅ ikonnevek a példákból |
| ABC jelzés (Text, az ikon helyett) | szöveg | `A` · láthatóság: `$if(gv(aktmod)=abc,always,remove)$` | ✅ |
| Csoport | esemény | `SWITCH_GLOBAL`, switch: `mod`, switch_list: `NEXT` | ✅ |
| Értesítéspötty (kis Shape kör) | láthatóság | `$if(ni(count)>0,always,remove)$` | ✅ |
| Töltés-pulzálás | animáció type | `$if(bi(source)=Battery,disabled,loop_2w)$`, `SCALE_XY` 1 → 1.08 | 🔧 |

A `NEXT` a lista végén valószínűleg az elejére ugrik. ⚠️ Teszteld.

### 4.6 Okos sáv – közös felépítés

- Mód-csoport: **Stack, VERTICAL_CENTER**, láthatóság: `$if(gv(aktmod)=zene,always,remove)$` (és így tovább módonként). ✅
- Egy zóna = Overlap csoport:
  - egy **átlátszó** Shape RECT (szélesség `$si(rwidth)*0.11$`, magasság `$si(rheight)*0.6/N$`), ez az érintési felület;
  - jobb szélén egy vékony látható csík vagy ikon;
  - az esemény a csoporton van.
- Mód-váltáskor beúszás: `VISIBILITY` animáció, `X_OFFSET` 40 → 0. ✅

⚠️ **1. teszt (a legfontosabb):** a `remove`-val elrejtett réteg tényleg nem fogadja-e a koppintást, és az átlátszó alakzat érzékeli-e a koppintást. A példákban 316 elem használja így, ami erősen erre utal, de a tervet erre építjük, ezért ezt kell először kipróbálni.

### 4.7 ZENE mód (N = 3 zóna + kijelzés)

| Zóna | Ikon (materialdesignicons) | Esemény | |
|---|---|---|---|
| 1 | `Skip-previous` ❓ (vagy entypo `Controller-jump-to-start` ❓) | `MUSIC`, music_action: `PREVIOUS` | ✅ esemény |
| 2 | `$if(mi(state)!=playing,Play,Pause)$` | `MUSIC`, music_action: `PLAY_PAUSE` | ✅ |
| 3 | `Skip-next` ❓ | `MUSIC`, music_action: `NEXT` | ✅ esemény |

- A vezetőcsíkon a lejátszás állása: egy Progress vagy Shape, magasság `$si(rheight)*0.6*mi(percent)/100$`, szín `$gv(acc)$`. 🔧
- A sáv mellett balra elforgatott szöveg: `$mi(title)$ · $mi(artist)$` (Text, `text_rotate_mode` ⚠️ az értéke kipróbálandó).
- Lejátszás nélkül: `$if(mi(title)="","Nincs zene",mi(title))$` ✅

Az előző/következő ikonok pontos nevét a KLWP ikonválasztójában kell kikeresni. ❓

### 4.8 HANG mód (N = 6 zóna)

| Zóna (fentről) | Esemény | |
|---|---|---|
| 100% | `CHANGE_VOLUME`, volume_action: `SET`, volume_level: `100` | ✅ |
| 80% … 0% | ugyanígy `80`, `60`, `40`, `20`, `0` | 🔧 |

- Melyik hangerő: a példákban csak a `RINGER` (csengő) szerepel ✅. A zene hangereje (média) a KLWP listájában valószínűleg külön választható ❓. Javaslat: a zóna-csoport fölé egy kis kapcsoló, ami a csengő és a média között vált (két külön zónasor, láthatóság szerint).
- Kijelzés: a média hangerejéhez `mi(vol)` ✅. A csengő aktuális szintje a példákban nem szerepel. ❓
- Csengőmód ikon a karika alatt: `$if(si(ringer)=normal,Volume-low,if(si(ringer)=silent,Volume-variant-off,Volume-vibrate))$` ✅

### 4.9 ABC mód (N = 9 zóna) + app-lista

**Zónák:** `ABC`, `DEF`, `GHI`, `JKL`, `MNO`, `PQR`, `STU`, `VWX`, `YZ`

| Mező | Érték | |
|---|---|---|
| Zóna szöveg | `A·B·C` (függőlegesen, kicsi) | ✅ |
| Zóna szín | `$if(gv(abc)=1,gv(acc),gv(txt2))$` (a zóna saját sorszámával) | ✅ |
| Esemény | `SWITCH_GLOBAL`, switch: `abc`, switch_text: `1` … `9` | ✅ |

**App-lista panel:** a sávtól balra nyílik. Overlap, láthatóság: `$if(gv(aktmod)=abc&gv(abc)!=0,always,remove)$`.

- Belül **9 Stack csoport** (egy minden betűcsoportnak), mindegyik láthatósága: `$if(gv(abc)=1,always,remove)$` … `=9`.
- Minden Stack-ben **legfeljebb 6 sor**. Egy sor egy Overlap:
  - Text: az app neve (`txt`, jobbra igazítva);
  - esemény: `LAUNCH_APP` → az adott app (az alkalmazásban kiválasztva).
- Legalul egy „Összes app” sor: `LAUNCH_SHORTCUT` → Nova `APP_DRAWER` ✅.
- Bezárás: egy „×” sor, ami az `abc`-t `0`-ra állítja ✅, vagy újra az aktív zónára koppintás.
- Megjelenés: `VISIBILITY` animáció, `X_OFFSET` 60 → 0. ✅

**Kézi munka csökkentése:** készítsd el az első sort, másold le hatszor, aztán az egész Stack-et kilencszer, és csak a neveket és az indított appokat kell átírni. Ahol nincs app, a sort töröld.

### 4.10 KAPCS mód (N = 4 zóna)

| Zóna | Ikon (materialdesignicons) | Esemény | |
|---|---|---|---|
| Wifi | `$if(nc(wifi)=disabled,Wifi-off,Wifi)$` | `KUSTOM_ACTION` `TOGGLE_WIFI` | ✅ |
| Bluetooth | `$if(nc(bt)=0,Bluetooth-off,Bluetooth)$` | `KUSTOM_ACTION` `TOGGLE_BT` | ✅ / ⚠️ (`nc(bt)=0` = ki) |
| Csengőmód | lásd 4.8 | `CHANGE_VOLUME` RINGER `SET` 0 / 100 felváltva | 🔧 |
| Képernyő ki | (ikon a listából) | `LAUNCH_SHORTCUT` → Nova `SCREEN_OFF` | ✅ |

Az ikon színe az állapottól függ: `$if(nc(wifi)=connected,gv(acc),gv(txt2))$` ✅

A wifi kapcsolása újabb Android-verziókon korlátozott lehet (az alkalmazás nem kapcsolhatja közvetlenül). ❓

### 4.11 ÉRTES mód (N = 5 zóna)

| Mező | Képlet | |
|---|---|---|
| Ikon (BitmapModule) | `$ni(0, icon)$` … `$ni(4, icon)$` | ✅ |
| Láthatóság | `$if(ni(count)>0,always,remove)$` (a 2. zónától `>1`, `>2` …) | 🔧 |
| Esemény | `KUSTOM_ACTION` `NOTIF_OPEN`, notification: `0` … `4` | ✅ ⚠️ (a példákban `1`, `2` szerepel; hogy 0-tól vagy 1-től számol, tesztelendő) |
| Előnézet a sáv mellett (Text) | `$ni(0, text)$` | ✅ |
| Legalsó zóna | `KUSTOM_ACTION` `NOTIF_CLOSE_ALL` | ✅ |
| Üres állapot | Text „Nincs értesítés”: `$if(ni(count)=0,always,remove)$` | ✅ |

---

## 5. Építési sorrend (a kockázatos részek előre)

| Fázis | Mit | Miért |
|---|---|---|
| **0. Teszt** | 2 egymásra tett zóna, az egyik `remove`-val rejtve, mindkettőn más koppintás-esemény; egy átlátszó alakzat eseménnyel; `NOTIF_OPEN` 0 és 1; `si(alarmd)` ébresztés nélkül; `NEXT` a lista végén; animáció `OPACITY` iránya | ezekre épül a terv; ha valami nem úgy működik, az elején kell tudni |
| **1. Alap** | háttér, globálisok, óra-blokk, keresősáv, infósor | önmagában is használható |
| **2. Karika + ZENE + HANG** | a sáv vázával | a sáv mechanikájának kipróbálása |
| **3. KAPCS + ÉRTES** | | egyszerű, az 1. fázisra épül |
| **4. ABC** | a 9 csoport app-listákkal | a legtöbb kézi munka |
| **5. Finomhangolás** | animációk, előrejelzés panel, beégésvédelem, színek | |

## 6. Nova beállítások

- Dokk, keresősáv és ikonok kikapcsolása, vagy egy üres oldal (így a háttér szabad).
- Nova gesztus (például dupla koppintás) → képernyő kikapcsolása.
- A KLWP-ben a háttér beállítása Nova alá. A koppintás továbbításához a Nova támogatása kell, tudomásom szerint ezt a Nova tudja. ❓

## 7. Nyitott kérdések / későbbi ötletek

- Óránkénti előrejelzés nem érhető el (csak napi). ❓
- Időjárás-ikon: egy időjárás-betűtípussal (a példák így csinálják) vagy egy kész komponenssel később hozzáadható.
- Lehetséges további sávmódok: naptár (következő 5 esemény), kedvencek (5 app egyenesen), média-hangerő külön.
- Kísérleti lehetőség: a terv alapján generált `.klwp` fájl, ami **nincs tesztelve**.
