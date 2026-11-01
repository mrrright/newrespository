# Bevált KLWP képletminták

Minden minta a 3 példapresetből származik, vagy azok szabályaiból van összerakva.
Jelölés: ✅ szó szerint a példákból · 🔧 a példák igazolt elemeiből összerakva (az összetétel nincs kipróbálva) · ❓ nem igazolt.

## Reszponzív méretezés ✅

A példák soha nem fix pixelt használnak, hanem a képernyőmérethez arányosítanak:

```
Szövegméret:      $(si(rwidth)+si(rheight))/116$
Kisebb szöveg:    $(si(rwidth)+si(rheight))/232$
Ikonméret:        $(si(rwidth)+si(rheight))/77.3/3$
Vízszintes margó: $si(rwidth)*1.4/100$
Függőleges érték: $si(rheight)*3.13/1000$
```

Tipp: a gyakori méretet tedd egy NUMBER globálisba (`global_formula`), és az elemek arra hivatkozzanak: `$gv(sdtxt)$`. ✅ (a `sdtxt` „size of date texts” így működik)

## Óra és dátum

```
$df(hh)$ és $df(mm)$       ✅ (az óra és a perc külön elemben a gyakori)
$df(hh:)$$df(mm)$          ✅ (egy mezőben, két képlettel)
$df(hh:mm:ss)$             ✅
$df(EEEE)$ - $df(dd)$      ✅
$df(MMMM dd yyyy)$         🔧
```

## Napszak szerinti üdvözlés ✅

```
$if((df(H)>=0&df(H)<=3)|(df(H)>=21&df(H)<=23),"Good Night",
 if(df(H)>=4&df(H)<=11,"Good Morning",
 if(df(H)>=12&df(H)<=17,"Good Afternoon",
 if(df(H)>=18&df(H)<=20,"Good Evening"))))$
```

Rövidebb, többágú változat magyarul 🔧:

```
$if(df(H)<4,"Jó éjszakát",df(H)<12,"Jó reggelt",df(H)<18,"Szép napot",df(H)<21,"Jó estét","Jó éjszakát")$
```

## Időjárás

```
$wi(temp)$°$wi(tempu)$     ✅
$wi(cond)$                 ✅
$wi(hum)$%                 ✅  (ProgressModule progress_level mezőjébe is: $wi(hum)$)
```

Ikon kiválasztása az időjárás szerint ✅ (rövidítve):

```
$if(wi(icon)=TORNADO|wi(icon)=TSTORM|wi(icon)=TSHOWER|wi(icon)=SHOWER|wi(icon)=RAIN,Rainy3,
 if(wi(icon)=SLEET|wi(icon)=LSNOW|wi(icon)=SNOW,Snowshower2, ...))$
```

A visszaadott érték (`Rainy3`) egy ikon- vagy képnév az adott presetben. Ezt a saját ikonjaidra kell cserélni.

## Zene ✅

```
$if(mi(title)="",Nincs zene,mi(title))$
$if(mi(artist)="<unknown>"|mi(artist)="",Ismeretlen előadó,mi(artist))$
$tf(mi(pos), mm:ss)$ / $tf(mi(len), mm:ss)$
Borító (Shape/háttér bitmap mezőbe): $mi(cover)$
Animáció csak lejátszás közben (az animáció type mezőjébe): $if(mi(state)=playing,loop_2w,disabled)$
```

Gombok: `MUSIC` esemény `music_action: PREVIOUS` / `NEXT`, illetve `music_action` nélkül (⚠️ valószínűleg lejátszás/szünet).

## Akkumulátor ✅

```
$bi(level)$%
Csak 75% felett látszik (config_visible): $if(bi(level)>=75,always,remove)$
```

Színváltás 🔧: `$if(bi(level)<20,#FFFF4444,gv(txtcl))$`

## Értesítések és olvasatlanok ✅

```
$ni(count)$
Jelvény csak, ha van értesítés (config_visible): $if(ni(count)=0,remove,always)$
Alkalmazásonként: $if(ni(pcount, com.instagram.android)=0,never,always)$
Nem fogadott hívás: $if(uc(calls)>=1,always,never)$
Olvasatlan SMS:     $if(uc(sms)>=1,always,never)$
```

## Wifi és Bluetooth ✅

```
Ikonnév (FontIcon icon_icon, entypo készlet): $if(nc(wifi)=disabled,Wifi-off,Wifi)$
                                               $if(nc(bt)=2,Bluetooth,if(nc(bt)=1,Bluetooth,Bluetooth-off))$
Koppintásra kapcsol: KUSTOM_ACTION → TOGGLE_WIFI / TOGGLE_BT
```

## Csengőmód ✅

```
$if(si(ringer)=silent,always,remove)$   (és normal / vibrate)
```

## Téma: színek és sötét/világos mód

1. Készíts COLOR globálisokat (`panelcl`, `apppcl`). ✅
2. A szövegszín számolja ki magát a panelszínből ✅:
   ```
   txtcl = $ce(ce(gv(panelcl),contrast),lum,60)$
   ```
3. Átlátszó változat ✅: `$ce(gv(ccl),alpha,50)$`
4. Témaváltó SWITCH (`swtheme`), és az elemek ehhez igazodnak ✅:
   ```
   config_visible: $if(gv(swtheme)=0,always,never)$
   fx_gradient:    $if(gv(swtheme)=1,radial,none)$
   ```
5. Fekete-fehér mód egy kapcsolóval ✅: `config_filter: $if(gv(swbt)=1,desaturate,none)$`

## Választható színpaletta LIST-tel ✅

```
ca1..ca4      COLOR globálisok
cal (LIST)    entries: $gv(ca1)$,$gv(ca2)$,$gv(ca3)$,$gv(ca4)$
              value:   $gv(ca3)$
Koppintásra léptet: SWITCH_GLOBAL, switch: cal  (visszafelé: switch_list: PREV)
Használat:    paint_color: $gv(cal)$
```

Ugyanez képekkel: `pic1..pic4` BITMAP globálisok + `pic` LIST, a háttér `background_bitmap` mezőjében `$gv(pic)$`. ✅

## Háttér képletből ✅

```
background_type:         $if(gv(txte5)=1,solid,image)$
background_bitmap:       $gv(pic)$
background_filter_color: $gv(cal)$   (background_filter: COLORIZE)
```

## Szám kitöltése két jegyre ✅

```
$if(gv(cpage)<10,tc(lpad, gv(cpage), 2, 0),gv(cpage))$
```

## Naptár-segédváltozók ✅

```
year  (TEXT): $df(yyyy)$
month (TEXT): $df(M)$
day   (TEXT): $df(d)$
ndim  (TEXT): $df(o,gv(year)+y+gv(month)+M)$          ← a hónap napjainak száma
fdom  (TEXT): $df(f,gv(year)+y+1+d+gv(month)+M)$      ← a hónap első napja a hét hányadik napja
Mai esemény van-e: $ci(ecount,gv(year)+y+gv(month)+M+gv(day)+d)+ci(acount,gv(year)+y+gv(month)+M+gv(day)+d)$
```

## Animációs minták ✅

- **Beúszás alulról**: `FORMULA` + `ADVANCED`, kulcskockák: 0% → `Y_OFFSET 30`, `OPACITY 100`; 100% → `Y_OFFSET 0`, `OPACITY 0`.
  ❓ Az `OPACITY` 100 → 0 irány a gyakoribb a példákban, de a fordítottja is előfordul, így nem tudni biztosan, hogy a 100 a látható vagy az átlátszó állapot. Kipróbálással ellenőrizd.
- **Megjelenés nagyítással kapcsolóra**: `formula: $if(gv(txta)=1,1,0)$`, `SCALE_XY` 0 → 1.
- **Folyamatos ingás**: `LOOP_2W` + `ADVANCED`, `ROTATE` 100% → 20, `ease: OVERSHOOT`, `duration: $gv(anispd)+5$`.
- **Folyamatos forgás**: `LOOP_FW` + `ROTATE`, `duration: 20`.
- **Lebegés**: `LOOP_2W`, `Y_OFFSET` 0 → -5 → 0 → 5 → 0 (0/25/50/75/100%).
- Az animáció sebességét egy NUMBER globális (`anispd`) adja, így egy helyen állítható. ✅

## Újabb minták (4–9. példafájl)

### Állapotmondat egy szövegben ✅ (rövidítve)

```
Your battery is $if(bi(source)=Battery,discharged,charging)$ at $bi(level)$%.
$if(nc(wifi)=disabled,"Your wifi connection is off now.",
 if(nc(wifi)=connected,"Your current wifi connection is "+nc(ssid)+".","You are not connected to any wifi network."))$
And you are on $nc(operator)$ operator now.
```

### Lejátszás/szünet gomb ✅

```
Ikon (entypo, icon_icon): $if(mi(state)!=playing,Triangle-right,Controller-paus)$
Esemény: MUSIC, music_action: PLAY_PAUSE
Zene folyamatjelző szélessége (Shape shape_width): $mi(percent)*480/100+50$
```

### Témaszín a háttérképből ✅

```
Kiemelő szín: $ce(bp(vibrant, gv(picl)),alpha,50)$
Olvasható szöveg: $ce(bp(dominant, gv(picl)),contrast)$
```

### Ma / holnap / dátum a következő naptáreseményhez ✅ (egyszerűsítve)

```
$if(df(MM/dd/yyyy, ci(start, 0))=df(MM/dd/yyyy),Today,
 df(MM/dd/yyyy, ci(start, 0))=df(MM/dd/yyyy, a1d),Tomorrow,
 df(EEEE, ci(start, 0))+", "+df(MMMM, ci(start, 0))+" "+df(d, ci(start, 0))+tc(ord, df(d, ci(start, 0))))$
Esemény címe: $tc(up,ci(title, 0))$
```

Magyar változat 🔧: `Today` → `Ma`, `Tomorrow` → `Holnap`. A `tc(ord, ...)` angol ragot ad, magyarhoz helyette `+"."` kell (`november 5.`).

### Váltakozó tartalom másodpercek szerint ✅

6 másodpercenként más eseményt mutat (0–4. esemény):

```
$if(df(ss)>=00 & df(ss)<=05,ci(title, 0), df(ss)>=06 & df(ss)<=11,ci(title, 1), ... )$
Animáció ugyanerre (FORMULA, formula mező): $if(df(ss)=00,f,df(ss)=06,f,df(ss)=12,f,...,r)$
```

### Értesítésjelző pulzálás csak új értesítésnél ✅

```
Animáció type mezője (képlet): $if(ni(pcount, gv(emlpkg))>=1,loop_2w,FORMULA)$
action: SCALE_INVERTED, amount: 0.5, duration: 3
A csomagnév globálisban (emlpkg, smspkg, phnpkg), így a felhasználó cserélheti.
```

### Lépcsőzetes beúszás kapcsolóra ✅

Több elem ugyanarra a SWITCH-re (`trigger: swapps`), `ADVANCED`, egyre nagyobb kezdő `Y_OFFSET`-tel (120 / 240 / 360) és `delay`-jel (0 / 1 / 2). A `duration`: `$gv(anispd)$`.

### Gombnyomás-visszajelzés ✅

`SWITCH` + `ADVANCED`, `SCALE_XY` 1 → 0.85 → 1 (0/50/100%), `duration: 1`.

### Betöltés-szimuláció ✅

```
LOADING  $mu(round, df(s)*100/60)+2$%
```

## Újabb minták (10–17. példafájl, több szerzőtől)

### Időjárás-előrejelzés napváltóval ✅

```
wfcount (TEXT globális): 0…6  — gombok: SWITCH_GLOBAL, switch: wfcount, switch_text: "4"
Nap neve:   $df(EEE, a4d)$   🔧 (a példában: $df(tc(reg,gv(dtformat),"@","/"), a4d)$, napokként a0d…a6d)
Min / max:  [b]$wf(min, gv(wfcount))$°[/b][s=0.8] / $wf(max, gv(wfcount))$°[/s]
Eső:        $wf(rain, gv(wfcount))$[s=0.8] mm[/s]
Légnyomás:  $wf(press, gv(wfcount))$[s=0.8] mbar[/s]
Szél:       $wf(wspeedm, gv(wfcount))$[s=0.8] mps[/s]
```

### Aktuális vagy előrejelzett ikon, nappal/éjszaka ✅

```
day (LIST, komponensben): entries "Current, 0, 1, 2, 3, 4, 5, 6, 7"
$if(if(gv(day)=current, wi(icon), wf(icon, gv(day)))=CLEAR & ai(isday)=1, A)$
$if(if(gv(day)=current, wi(icon), wf(icon, gv(day)))=CLEAR & ai(isday)=0, a)$
...  (a betűk egy időjárás-betűtípus karakterei)
Egyszerű nap/hold ikon: $if(ai(isday)=1, Sun, Moon)$
```

### Időjárás-mondat ✅

```
$tc(cap,wi(cond))$, $wi(temp)$°$wi(tempu)$ now. Feels like $wi(flik)$°$wi(tempu)$.
Hely: [b]$tc(up,li(loc)+", "+li(country))$[/b]
```

### Olvasatlanok összesítve ✅

```
$if(uc(sms)+uc(calls)+uc(gmail)=0,"you don't have misses.","you have "+(uc(sms)+uc(calls)+uc(gmail))+" miss"+if(uc(sms)+uc(calls)+uc(gmail)>1,"es",""))$
```
(a példában nincs szóköz a szavak körül, itt kiegészítve 🔧)

### Utolsó értesítés kártya ✅

```
Ikon (BitmapModule, bitmap_bitmap): $ni(0, icon)$
Szöveg: $ni(0, text)$
Idő:    $tf(ni(0, time))$
Bezárás gomb: KUSTOM_ACTION, kustom_action: NOTIF_CLOSE, notification: "0"
```

### Zene: lejátszó neve és animált pontok ✅

```
$if(ni(mi(package),app)="","- / -","Playing by "+ni(mi(package),app))$
[b]$tc(up,if(mi(state)!=playing,Pause,"Now playing."+fl(1, tu(seq, 0.01,1,3), "i + 1", ".")))$[/b]
Szín a borítóból: $bp(muted, mi(cover))$
```

### Háttérkép-választó + automatikus témaszín ✅

```
img1…img6 (BITMAP globálisok), bg (LIST: img1,…,img6), mode (LIST: vibrant, dominant, muted)
Háttér (background_bitmap): $gv(gv(bg))$
Gomb: SWITCH_GLOBAL, switch: bg, switch_list: img3
Témaszín: $bp(gv(mode), gv(gv(bg)))$
```

### Mai naptáresemény részletei ✅

```
Cím:      $ci(title, 0, a0d)$
Idő:      [b]$df(gv(tmformat),ci(start, e0, a0d))$ - $df(gv(tmformat),ci(end, e0, a0d))$[/b]
Helyszín: $if(ci(loc, 0 ,a0d)="","- / -",ci(loc, 0 ,a0d))$
Leírás:   $if(ci(desc, 0 ,a0d)="","- / -",ci(desc, 0 ,a0d))$
```

### Következő ébresztés, rendszeradatok ✅

```
$df("EEE hh:mma", si(alarmd))$
$si(model)$ · Android $si(aver)$
Tárhely: $mu(round, rm(fsused)/rm(fstot)*100)$%
```

### Napi idézet XML-ből ✅

```
$wg("api.theysaidso.com/qod.xml", xml, "//quote")$
[b]$wg("api.theysaidso.com/qod.xml", xml, "//author")$[/b]
```
(Hogy ez a szolgáltatás ma is működik-e, nem ellenőriztem. ❓)

### RSS hírolvasó léptetéssel ✅

```
Cím: [b]$tc(up,tc(html,wg(gv(rsslink), rss, gv(fdcount), title)))$[/b]
Iniciálé: [s=2]$tc(cut,tc(html,wg(gv(rsslink), rss, gv(fdcount), desc)),1)$[/s]
Következő hír gomb: SWITCH_GLOBAL, switch: fdcount,
  switch_text: $if(gv(fdcount)>=wg(gv(rsslink), rss, count)-1,0,gv(fdcount)+1)$
```

### Térkép háttér URL-ből ✅ (a KoolKit Maps elve)

Egy alakzat `fx_gradient: BITMAP` + `fx_gradient_bitmap` mezőjébe statikus térkép-URL kerül, amibe képletek írják be a helyet:
```
https://<térképszolgáltató>/staticmap?center=lonlat:$li(lon)$,$li(lat)$&zoom=$gv("002/001/zoom")/1000$&width=$mu(round,gv("002/001/width"),0)$...&apiKey=<SECRET globális>
```
A szolgáltatók API-ja és kulcsigénye változhat. ❓ Az API-kulcsot SECRET globálisban kell tárolni.

### Animációk zárolás/feloldás és kapcsoló szerint ✅

- Feloldáskor: `type: UNLOCK`, `action: SCALE_INVERTED`, `amount: 5`, `duration: $gv(speed)$`.
- Csak feloldott képernyőn gyorsabb: `duration: $gv(speed)*if(si(locked),1,0.5)$`.
- Csúszka-panel: `type: SWITCH`, `trigger: slider`, `action: FADE_INVERTED` / `SCALE`, `delay: $if(gv(slider)=0,1,0)$`.
- Kifelé nagyítás a képernyő sarkából: `action: SCALE`, `anchor: SCREEN_TOP_RIGHT`, `ease: INVERTED`.

### GIF animáció ✅

MovieModule, `bitmap_movie_uri`: GIF fájl. Kapcsolóval váltva: `$if(gv(switch)=1,gv(anim2),gv(anim1))$`, színezés: `bitmap_filter: $if(gv(switch)=1,hue,none)$`.
