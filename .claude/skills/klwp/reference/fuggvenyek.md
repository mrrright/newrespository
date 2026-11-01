# KLWP képletnyelv – függvények és szintaxis

Forrás: 17 KLWP preset, több különböző szerzőtől. A pontos szám nem állapítható meg, mert a fájlok szerzőmezője mentéskor felülíródik. 8 preset egy szerzőtől van (HackerTheme, NeuMorphicThemeVol2 ×2, Theme3 ×2, Theme4, Theme4a, Theme5). A többi: Kustom Punk, MTstyle03, MTstyle10, KoolKit Maps, Chameleon, Hooligans, WALKING, Prism Style, DeepOcean. Ami csak egy presetben látszik, az lehet az ottani szerző egyéni szokása is.
Jelölés: ✅ igazolt · ⚠️ megfigyelt, a jelentés következtetés · ❓ nem igazolt (nem szerepel a példákban).
A zárójelben lévő szám azt mutatja, hányszor fordult elő a példákban.

## 1. Szintaxis

| Szabály | Példa | |
|---|---|---|
| A képlet `$` jelek között van | `$df(HH:mm)$` | ✅ |
| Egy mezőben több képlet és sima szöveg keverhető | `$wi(temp)$°$wi(tempu)$`, `Free memory: $rm(mfree)$MB` | ✅ |
| A függvények egymásba ágyazhatók | `$ce(ce(gv(panelcl),contrast),lum,60)$` | ✅ |
| A képlet több sorba tördelhető (a sortörés megengedett az argumentumok között) | 48 többsoros képlet a naptárban | ✅ |
| Szöveg idézőjel nélkül is írható | `$if(mi(title)="",Refresh yourself with your favorites songs,mi(title))$` | ✅ |
| Idézőjeles szöveg is működik, szóköz/vessző esetén ez a biztos | `"Good Morning"` | ✅ |
| Üres szöveg vizsgálata | `mi(artist)=""` | ✅ |
| Szövegösszefűzés `+`-szal | `Page + " " + gv(cpevnt)` | ✅ |
| Megjegyzés (`//`) | egyik példában sincs | ❓ |
| A `$` jelek között egy sima szó is állhat (`$Sun$##Day`) | LIST `entries` mezőben | ⚠️ jelentése nem világos |

### Szövegformázás (BBCode-szerű) ✅

Text elem szövegében: `[b]félkövér[/b]`, `[i]dőlt[/i]`, `[s=0.8]kisebb[/s]` (relatív méret, `s=2` = kétszeres). Képletekkel keverhető: `[b]$wf(min, gv(wfcount))$°[/b][s=0.8] / $wf(max, gv(wfcount))$°[/s]`. Más címkék (szín, betűtípus) nem szerepelnek. ❓

### Operátorok ✅

`=` `!=` `<` `>` `<=` `>=` · `&` (és, 1002×) · `|` (vagy, 261×) · `+` `-` `*` `/` `%` (maradék, 29×) · `^` (hatvány: `si(rheight)^2`) · zárójelek.

Egy SWITCH (0/1) globális önmagában is feltétel: `if(gv(sunfirst), ..., ...)`, `gv(sunfirst)&gv(fdom)=7`. ✅

### Felsorolt értékek képletből ✅

Ha egy tulajdonság (láthatóság, alakzat, színátmenet stb.) értékét képlet adja, a példák szinte mindig **kisbetűvel** adják vissza. Egy aktív képletben nagybetűs is előfordul (`$if(ni(pcount, gv(emlpkg))>=1,loop_2w,FORMULA)$`), tehát a kis- és nagybetű valószínűleg mindegy. ⚠️ A kisbetű a biztos választás:

| Tulajdonság | Képletben látott értékek |
|---|---|
| láthatóság (`config_visible`) | `always`, `never`, `remove` |
| háttér típusa (`background_type`) | `solid`, `image` |
| kép/videó szűrő (`bitmap_filter`) | `hue`, `none` |
| színátmenet (`fx_gradient`) | `radial`, `none` |
| festés stílusa (`paint_style`) | `stroke`, `fill` |
| szűrő (`config_filter`) | `desaturate`, `none` |
| animáció típusa | `loop_2w`, `disabled` |

⚠️ A `never` és a `remove` a példákban felváltva szerepel. Az valószínű, hogy a `never` csak elrejti az elemet, a `remove` pedig a helyét is felszabadítja (például Stack csoportban), de ezt a fájlok nem bizonyítják.

## 2. Függvények

### `gv(név)` – globális változó (15 035×) ✅

- `$gv(txtcl)$` → a globális értéke.
- LIST globálisnál index is megadható: `gv(weekdays, 0)`. A `weekdays` = `SUN,MON,...` és a `gv(weekdays,si(mindex,1))` használatából következik, hogy **0-tól számoz**. ⚠️
- Háromargumentumos alak is előfordul: `gv(weekdays, gv(weekdays,0), si(mindex,1)+1)`. A jelentése nem egyértelmű. ⚠️
- **Mappában lévő globális** ✅: a név perjeles útvonal, idézőjelben: `gv("002/001/width")`, `gv("001/bg/color1")` (lásd `fajlformatum.md`, FOLDER).
- **Közvetett hivatkozás** ✅: `gv(gv(bg))` – a `bg` értéke egy másik globális neve, és annak az értékét adja. A háttérkép-választóban így használják: a `bg` LIST értékei `img1`…`img6`.
- **Komponensen belül** a `gv()` a komponens saját globálisaira hivatkozik. ✅ (A Chameleon „WEATHER NOW” komponense csak a saját 6 globálisát használja.)

### `if(f1, e1, [f2, e2, ...], [különben])` – feltétel (2 471×) ✅

```
$if(df(H)<12, "Jó reggelt", df(H)<18, "Szép napot", "Jó estét")$
$if(gv(dshal)="$gv(ca1)$",gv(dsha1),gv(dshal)="$gv(ca2)$",gv(dsha2))$
```
A többágú alak és az egymásba ágyazott `if(..., if(...))` is látható. A második példában egy idézőjeles szöveg belsejében egy `$...$` képlet van. Ezt a példák LIST globálisok kiválasztott elemének összehasonlítására használják. ✅

### `df(formátum[, dátum])` – dátum és idő (284×) ✅

| Kód | Jelentés | |
|---|---|---|
| `H` | óra, 0–23 | ✅ (üdvözlésben 0–23 tartománnyal) |
| `h`, `hh` | óra, 12 órás | ✅ |
| `mm` | perc | ✅ |
| `s`, `ss` | másodperc (`ss` két jeggyel, `00`–`59`) | ✅ |
| `MM/dd/yyyy` | teljes dátum, például összehasonlításhoz | ✅ |
| `hh:mm:ss` | idő | ✅ |
| `a` | `am` / `pm` | ✅ (`df(a)=am`) |
| `d`, `dd` | a hónap napja | ✅ |
| `M`, `MMM`, `MMMM` | hónap: szám / rövid / hosszú név | ✅ |
| `y`, `yyyy` | év | ✅ |
| `EE`, `EEE`, `EEEE` | a hét napja: rövid / hosszú | ✅ |
| `HH:mm`, `h:mm`, `h:mma` | idő 24/12 órás, `a` = am/pm | ✅ |
| `z` | időzóna | ⚠️ (csak `$df(z)$` önmagában) |
| `o` | **a hónap napjainak száma** | ✅ (a szerző leírása: „number of days in month”) |
| `f` | **a hét hányadik napja** (a megadott dátumé) | ✅ (a szerző leírása: „first day of the month”, `1d` dátummal) |

**Dátum megadása második paraméterként:**
- **Relatív dátum** ✅: `a1d` = mától +1 nap. `df(MM/dd/yyyy, a1d)` adja a holnapi dátumot, a Kustom Punk ezzel írja ki a „Tomorrow” feliratot. Más mértékegységek (`h`, `m` stb.) és a kivonás nem szerepelnek. ❓
- **Abszolút dátum** ⚠️: szám + mértékegység-betű, szövegként összefűzve: `gv(year)+y+gv(month)+M+gv(day)+d` → pl. `2026y11M1d`. Példák: `$df(o,gv(year)+y+gv(month)+M)$`, `$df(MMMM dd yyyy,gv(year)+y+gv(month)+M+gv(day)+d)$`. Hogy ez abszolút, azt az `a` előtag hiánya és a naptár működése mutatja.
- **Másik függvény eredménye** ✅: `df(EEEE, ci(start, 0))` – egy naptáresemény kezdetének a napja.
- A formátum lehet idézőjelben is (`df("h:mm a", ...)`, `df("EEE hh:mma", si(alarmd))`), szóközös formátumnál ez a biztos. ✅
- A formátum jöhet globálisból vagy képletből is: `df(gv(tmformat), ...)`, `df(tc(reg,gv(dtformat),"@","/"), a1d)`. ✅
- `a0d` = ma, `a1d`…`a5d` = 1–5 nap múlva (előrejelzéses napnevekhez). ✅

A formátumkódok a Java dátumformázásához hasonlítanak, de csak a fenti táblázatban lévők igazoltak.

### `si(...)` – rendszerinformáció (5 124×)

| Hívás | Jelentés | |
|---|---|---|
| `si(rwidth)`, `si(rheight)` | a háttér szélessége és magassága; ehhez arányosan méreteznek | ✅ (3869×) |
| `si(mindex, szint)` | az elem sorszáma a szülő csoportjában; a `szint` (1, 2) azt adja meg, hány csoporttal feljebb. A naptárrácsban használják | ⚠️ |
| `si(screen)` | az aktuális képernyő (oldal) sorszáma; 1–4 értékekkel hasonlítják, animációk és láthatóság kapcsolására: `$if(si(screen)=2,remove,always)$` | ⚠️ erős: a `SCROLL` animációk `center: SCREEN2` beállítása mellett ugyanaz az animáció `si(screen)=2`-t vizsgál. A presetek viszont `xscreens=1` beállítással vannak mentve, így nem teljesen biztos |
| `si(ringer)` | csengőmód: `normal`, `silent`, `vibrate` | ✅ |
| `si(locked)` | le van-e zárva a képernyő (feltételként: `if(si(locked),...)`) | ✅ |
| `si(alarmd)` | a következő ébresztés időpontja, `df()`-be adható | ✅ |
| `si(model)`, `si(aver)` | készülék típusa, Android-verzió (`Android $si(aver)$`) | ✅ |
| `si(sheight)` | képernyőmagasság | ⚠️ (a `rheight`-től való eltérése nem derül ki) |
| `si(sdensity)`, `si(skpi)` | képsűrűség-adatok, egy preset ezekből számol automatikus méretezési szorzót: `si(sdensity)/si(skpi)*100` | ⚠️ |
| `si(darkmode)` stb. | nem szerepel a példákban | ❓ |

### `ce(szín, művelet[, érték])` – színműveletek (865×) ✅

| Művelet | Példa | Jelentés |
|---|---|---|
| `alpha` | `ce(gv(ccl),alpha,50)` | átlátszóság (0–100) |
| `lum` | `ce(gv(ccl),lum,100)` | fényerő |
| `sat` | `ce(gv(cl),sat,30)` | telítettség |
| `contrast` | `ce(gv(cl),contrast)` | kontrasztos (olvasható) ellenszín |
| `comp` | `ce(gv(cl),comp)` | komplementer szín |

A `ce(ce(gv(panelcl),contrast),lum,60)` minta a háttérszínhez automatikusan olvasható szövegszínt ad. ✅

### `bp(mód, kép)` – szín kinyerése képből ✅

Módok: `vibrant`, `dominant`, `muted` ✅. A második paraméter kép: BITMAP globális (`gv(picl)`) vagy a zene borítója (`bp(muted, mi(cover))`). A mód is jöhet globálisból: `bp(gv(mode), gv(gv(bg)))`. A példák `ce()`-be csomagolják: `$ce(bp(vibrant, gv(picl)),alpha,50)$`, `$ce(bp(dominant, gv(picl)),contrast)$`. Így a téma színei a háttérképhez vagy a borítóhoz igazodnak. ✅ Egyéb módok (például „light”, „dark” változatok) nem szerepelnek. ❓

### `wi(...)` – időjárás (27×) ✅

`temp`, `tempu` (mértékegység), `flik` (hőérzet: „Feels like”), `cond` (állapot szövegesen), `hum` (páratartalom %), `clouds`, `wspeed` (szélsebesség), `lid` (⚠️ a helyszín neve, az időjárás-szolgáltatótól), `icon`.

A `wi(icon)` / `wf(icon, n)` értékei (15 különböző, összesen): `CLEAR`, `PCLOUDY`, `MCLOUDY`, `FOG`, `WINDY`, `RAIN`, `SHOWER`, `TSHOWER`, `TSTORM`, `TORNADO`, `SLEET`, `HAIL`, `LSNOW`, `SNOW`, `UNKNOWN`. ✅ Az, hogy ez a teljes lista, nem biztos. ❓

Nappali/éjszakai ikon: `ai(isday)`-jel kombinálják: `$if(wi(icon)=CLEAR & ai(isday)=1, A)$$if(wi(icon)=CLEAR & ai(isday)=0, a)$` (időjárás-betűtípus karakterei). ✅

### `wf(mező, nap)` – előrejelzés ✅

`wf(icon, 0)` = ma, `wf(icon, 1)` = holnap, … `wf(icon, 6)`. Mezők: `icon`, `cond`, `min`, `max`, `rain` (mm), `press` (mbar), `wspeedm` (m/s). A nap indexe globálisból is jöhet: `$wf(min, gv(wfcount))$°`. ✅ A preset `features` mezőjében ilyenkor `FORECAST` is szerepel. ✅

### `ai(...)` – csillagászat ✅

`ai(isday)` – nappal van-e (1/0): `$if(ai(isday)=1, Sun, Moon)$`. ✅ (151×) Napkelte, napnyugta, holdfázis stb. nem szerepel. ❓

### `mi(...)` – zene (14×) ✅

`title`, `artist`, `album`, `cover` (borítókép, bitmap mezőbe), `len` (hossz), `pos` (pozíció), `percent` (a lejátszás állása 0–100), `state` (`playing`), `vol` (hangerő, ⚠️ 0–100: `$mi(vol)*300/100$`), `package` (a lejátszó alkalmazás csomagneve).
Ismeretlen előadó: `mi(artist)="<unknown>"` is előfordul. ✅
A `mi(percent)` folyamatjelző szélességére: `$mi(percent)*480/100+50$`. ✅

### `tf(időtartam, formátum)` – időtartam formázása ✅

`$tf(mi(pos), mm:ss)$`, `$tf(mi(len), hh)$`. ✅

### `bi(...)` – akkumulátor ✅

- `bi(level)` (0–100). ✅
- `bi(source)` – áramforrás. `Battery` = akkumulátorról megy (nem tölt): `$if(bi(source)=Battery,discharged,charging)$`. ✅ A töltés közbeni értékek (például USB, AC) nem szerepelnek. ❓
- Hőmérséklet, feszültség stb. nem szerepel. ❓

### `ni(...)` – értesítések ✅

- `ni(count)` – az összes értesítés száma.
- `ni(pcount, csomagnév)` – egy alkalmazás értesítéseinek száma: `ni(pcount, com.facebook.katana)`. A csomagnév globálisból is jöhet: `ni(pcount, gv(emlpkg))`. ✅
- `ni(n, mező)` – az n-edik értesítés adatai (0-tól): `ni(0, text)`, `ni(0, icon)` (képként, BitmapModule-ba), `ni(0, time)` (`tf()`-be adható). ✅
- `ni(csomagnév, app)` – egy alkalmazás neve a csomagnévből: `"Playing by "+ni(mi(package),app)`. ✅

### `uc(...)` – olvasatlan ✅

`uc(calls)` (nem fogadott hívások), `uc(sms)` (olvasatlan SMS), `uc(gmail)` (olvasatlan Gmail). ✅

### `nc(...)` – hálózat ✅

- `nc(wifi)`: `connected`, `enabled`, `disabled`. ✅
- `nc(ssid)`: a wifi hálózat neve: `"Your current wifi connection is "+nc(ssid)+"."`. ✅
- `nc(operator)`: a mobilszolgáltató neve. ✅
- `nc(bt)`: számként hasonlítják, `2` és `1` = bekapcsolt állapotok. ⚠️ A pontos különbség (csatlakoztatva / bekapcsolva) következtetés.

### `ci(...)` – naptár ⚠️

- `ci(ecount, dátum)`, `ci(acount, dátum)` – események száma az adott napon (az `acount` valószínűleg az egész napos események száma). ⚠️
- `ci(title, index, dátum)` – egy esemény címe az adott napon. ✅
- `ci(title, index)` – a következő események közül az n-edik címe (0-tól). ✅
- `ci(start, index)` – az n-edik esemény kezdete. Dátumként `df()`-be adható: `df(MMMM, ci(start, 0))`. ✅
- `ci(end, ...)`, `ci(desc, ...)` (leírás), `ci(loc, ...)` (helyszín) – ugyanígy. ✅
- Harmadik paraméterként nap is megadható: `ci(title, 0, a0d)` = a mai nap 0. eseménye. ✅
- `e0` index: `ci(start, e0, a0d)`. ⚠️ Valószínűleg az „e” előtag a nem egész napos eseményekre szűr (vö. `ecount`), de ez nem biztos.

### `tc(...)` – szövegműveletek ✅

- `tc(up, szöveg)` – nagybetűsít: `$tc(up,gv(username))$`. ✅
- `tc(ord, szám)` – angol sorszámrag (`st`, `nd`, `rd`, `th`): `df(d, ...)+tc(ord, df(d, ...))` → `1st`. ⚠️ A pontos kimenet következtetés.
- `tc(cut, szöveg, n)` – az első n karakter. ✅
- `tc(lpad, szöveg, hossz, karakter)` – balról kitöltés: `tc(lpad, gv(cpage), 2, 0)` → `05`. ✅
- `tc(low, szöveg)` – kisbetűsít. ✅
- `tc(cap, szöveg)` – nagy kezdőbetű: `$tc(cap,wi(cond))$`. ✅
- `tc(len, szöveg)` – a szöveg hossza. ✅
- `tc(cut, szöveg, kezdet, hossz)` – részlet: `tc(cut, x, 1, tc(len, x))` = az első karakter utáni rész. ✅ (Együtt a `tc(cut, x, 1)`-gyel iniciálé-hatást ad.)
- `tc(reg, szöveg, minta, csere)` – csere reguláris kifejezéssel: `tc(reg,gv(dtformat),"@","/")`. ✅
- `tc(html, szöveg)` – HTML-kódok eltávolítása vagy átalakítása RSS-szövegből. ⚠️
- Nagybetűsítésre a Text elem `text_filter: ["UP"]` beállítása is használható. ✅

### `mu(...)` – matematika ⚠️

`mu(ceil, x)`, `mu(round, x)` (`$mu(round, df(s)*100/60)$`), `mu(round, x, tizedes)` (`mu(round,gv(...),0)`), `mu(min, a, b)`, `mu(max, a, b)`, `mu(sqrt, x)`, `mu(atan, x)` ✅. Több szerzőnél `mu(round(x))` alak is szerepel, vessző nélkül. Hogy ez működik-e, nem tudni, a `mu(round, x)` a biztos. ⚠️ A `mu(rnd, ...)`, `mu(sin, ...)` stb. nem szerepel. ❓

### `wg(url, rss, ...)` – webes tartalom (RSS) ✅

- RSS: `wg(gv(nyt),rss,count)`, `wg(gv(nyt),rss,index,link)`, további mezők: `title`, `thumb`, `desc`. A szöveget `tc(html, ...)`-lel tisztítják. ✅
- XML + XPath: `wg("api.theysaidso.com/qod.xml", xml, "//quote")`. ✅
- **Kép URL-ről, képlettel összerakva**: egy alakzat `fx_gradient_bitmap` mezőjébe statikus térkép-URL kerül, amibe a képlet beírja a helyet és a méretet: `...staticmap?center=lonlat:$li(lon)$,$li(lat)$&zoom=$gv("002/001/zoom")/1000$...`. ✅

### `li(...)` – hely ✅

`li(lat)`, `li(lon)`, `li(spdu)` (sebesség mértékegysége), `li(loc)` (település), `li(country)` (ország), `li(admin)` (⚠️ megye/régió). ✅

### `rm(...)` – erőforrások ✅

`rm(cused)` (CPU %), `rm(mfree)` (szabad memória MB), `rm(fsfree)`, `rm(fsused)`, `rm(fstot)` (teljes tárhely): `$mu(round, rm(fsused)/rm(fstot)*100)$%`. ✅

### `tu(...)` – időzítő ⚠️

`tu(seq, 1/60, 1, 12)`, `tu(seq, 0.01, 1, 3)`. Valószínűleg egy kezdő- és végérték között lépkedő sorozat a megadott ütemben, de ez következtetés. ⚠️

### `fl(kezdet, vég, lépés, kifejezés)` – ciklus ⚠️

Egyetlen előfordulás: `"Now playing."+fl(1, tu(seq, 0.01,1,3), "i + 1", ".")`. Ez a „Now playing...” után a pontokat 1–3 között animálja. Ebből látszik a szerkezet: kezdőérték, végérték, a léptetés kifejezése idézőjelben (`i` a ciklusváltozó), és a minden lépésben kiírt szöveg. ⚠️

### Nem szerepel a példákban ❓

`ai()` további paraméterei (napkelte, holdfázis), `br()`, `dp()`, `sh()`, `cm()` és mások. Ha ilyenre van szükség, jelezd, hogy nem igazolt, és kérd, hogy a felhasználó nézze meg az alkalmazás képletszerkesztőjében.
