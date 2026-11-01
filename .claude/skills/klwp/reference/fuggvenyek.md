# KLWP képletnyelv – függvények és szintaxis

Forrás: 3 KLWP preset (HackerTheme, NeuMorphicThemeVol2, Theme3), kb. 9000 képlet.
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

### Operátorok ✅

`=` `!=` `<` `>` `<=` `>=` · `&` (és, 1002×) · `|` (vagy, 261×) · `+` `-` `*` `/` `%` (maradék, 29×) · zárójelek.

Egy SWITCH (0/1) globális önmagában is feltétel: `if(gv(sunfirst), ..., ...)`, `gv(sunfirst)&gv(fdom)=7`. ✅

### Felsorolt értékek képletből ✅

Ha egy tulajdonság (láthatóság, alakzat, színátmenet stb.) értékét képlet adja, az értéket **kisbetűvel** kell visszaadni:

| Tulajdonság | Képletben látott értékek |
|---|---|
| láthatóság (`config_visible`) | `always`, `never`, `remove` |
| háttér típusa (`background_type`) | `solid`, `image` |
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
| `hh:mm:ss` | idő | ✅ |
| `a` | `am` / `pm` | ✅ (`df(a)=am`) |
| `d`, `dd` | a hónap napja | ✅ |
| `M`, `MMM`, `MMMM` | hónap: szám / rövid / hosszú név | ✅ |
| `y`, `yyyy` | év | ✅ |
| `EEE`, `EEEE` | a hét napja: rövid / hosszú | ✅ |
| `o` | **a hónap napjainak száma** | ✅ (a szerző leírása: „number of days in month”) |
| `f` | **a hét hányadik napja** (a megadott dátumé) | ✅ (a szerző leírása: „first day of the month”, `1d` dátummal) |

**Dátum megadása második paraméterként** ⚠️: a példák egy szöveget raknak össze számból és mértékegység-betűből: `gv(year)+y+gv(month)+M+gv(day)+d` → pl. `2026y11M1d`. Példák: `$df(o,gv(year)+y+gv(month)+M)$`, `$df(MMMM dd yyyy,gv(year)+y+gv(month)+M+gv(day)+d)$`. Azt nem tudni a fájlokból, hogy ez abszolút dátum vagy eltolás a mai naptól. A naptár viselkedéséből abszolút dátumra lehet következtetni.

A formátumkódok a Java dátumformázásához hasonlítanak, de csak a fenti táblázatban lévők igazoltak.

### `si(...)` – rendszerinformáció (5 124×)

| Hívás | Jelentés | |
|---|---|---|
| `si(rwidth)`, `si(rheight)` | a háttér szélessége és magassága; ehhez arányosan méreteznek | ✅ (3869×) |
| `si(mindex, szint)` | az elem sorszáma a szülő csoportjában; a `szint` (1, 2) azt adja meg, hány csoporttal feljebb. A naptárrácsban használják | ⚠️ |
| `si(screen)` | képernyő-/oldalindex; 1–4 értékekkel hasonlítják, animációk kapcsolására | ⚠️ (a presetek `xscreens=1` beállítással vannak mentve, így a pontos jelentés nem biztos) |
| `si(ringer)` | csengőmód: `normal`, `silent`, `vibrate` | ✅ |
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

### `wi(...)` – időjárás (27×) ✅

`temp`, `tempu` (mértékegység), `cond` (állapot szövegesen), `hum` (páratartalom %), `clouds`, `wspeed` (szélsebesség), `icon`.
A `wi(icon)` értékei a példákban: `TORNADO`, `TSTORM`, `TSHOWER`, `SHOWER`, `RAIN`, `SLEET`, `LSNOW`, `SNOW`. ✅ Ennél több érték is létezhet (például derült, felhős), de ezek nem szerepelnek a példákban. ❓

### `mi(...)` – zene (14×) ✅

`title`, `artist`, `album`, `cover` (borítókép, bitmap mezőbe), `len` (hossz), `pos` (pozíció), `state` (`playing`).
Ismeretlen előadó: `mi(artist)="<unknown>"` is előfordul. ✅

### `tf(időtartam, formátum)` – időtartam formázása ✅

`$tf(mi(pos), mm:ss)$`, `$tf(mi(len), hh)$`. ✅

### `bi(...)` – akkumulátor ✅

`bi(level)` (0–100). ✅ Töltés állapota, hőmérséklet stb. nem szerepel. ❓

### `ni(...)` – értesítések ✅

- `ni(count)` – az összes értesítés száma.
- `ni(pcount, csomagnév)` – egy alkalmazás értesítéseinek száma: `ni(pcount, com.facebook.katana)`.

### `uc(...)` – olvasatlan ✅

`uc(calls)` (nem fogadott hívások), `uc(sms)` (olvasatlan SMS). ✅

### `nc(...)` – hálózat ✅

- `nc(wifi)`: `connected`, `enabled`, `disabled`. ✅
- `nc(bt)`: számként hasonlítják, `2` és `1` = bekapcsolt állapotok. ⚠️ A pontos különbség (csatlakoztatva / bekapcsolva) következtetés.

### `ci(...)` – naptár ⚠️

- `ci(ecount, dátum)`, `ci(acount, dátum)` – események száma az adott napon (az `acount` valószínűleg az egész napos események száma). ⚠️
- `ci(title, index, dátum)` – egy esemény címe. ✅

### `tc(...)` – szövegműveletek ✅

- `tc(cut, szöveg, n)` – az első n karakter. ✅
- `tc(lpad, szöveg, hossz, karakter)` – balról kitöltés: `tc(lpad, gv(cpage), 2, 0)` → `05`. ✅
- `tc(up, ...)`, `tc(low, ...)` stb. nem szerepel képletben. ❓ Nagybetűsítésre a példák a Text elem `text_filter: ["UP"]` beállítását használják. ✅

### `mu(...)` – matematika ⚠️

`mu(ceil, x)` ✅. A példákban `mu(round(mu(ceil, x)))` alak szerepel (vessző nélkül). Ez lehet szerzői elírás is, a helyes alak valószínűleg `mu(round, x)`. ⚠️ A `mu(rnd, ...)`, `mu(sin, ...)` stb. nem szerepel. ❓

### `wg(url, rss, ...)` – webes tartalom (RSS) ✅

`wg(gv(nyt),rss,count)`, `wg(gv(nyt),rss,index,link)`, további mezők: `thumb`, `desc`. ✅

### `li(...)` – hely ✅

`li(lat)`, `li(lon)`, `li(spdu)` (sebesség mértékegysége). ✅

### `rm(...)` – erőforrások ✅

`rm(cused)` (CPU %), `rm(mfree)` (szabad memória MB), `rm(fsfree)`, `rm(fsused)`. ✅

### `tu(...)` – időzítő ⚠️

`tu(seq, 1/60, 1, 12)` – egyetlen előfordulás. Valószínűleg egy 1-től 12-ig lépkedő sorozat 1/60 másodperces ütemben, de ez következtetés. ⚠️

### Nem szerepel a példákban ❓

`ai()` (csillagászat, napkelte), `br()`, `fl()` (ciklus), `dp()`, `bp()`, `sh()`, `cm()` és mások. Ha ilyenre van szükség, jelezd, hogy nem igazolt, és kérd, hogy a felhasználó nézze meg az alkalmazás képletszerkesztőjében.
