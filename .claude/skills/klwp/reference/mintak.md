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
  ⚠️ A példák beúszó animációiban az `OPACITY` mindig 100 → 0 irányú. Ebből arra lehet következtetni, hogy az animátorban az `OPACITY` az átlátszóság mértéke (100 = teljesen átlátszó), és nem az átlátszatlanságé. Kipróbálással ellenőrizd.
- **Megjelenés nagyítással kapcsolóra**: `formula: $if(gv(txta)=1,1,0)$`, `SCALE_XY` 0 → 1.
- **Folyamatos ingás**: `LOOP_2W` + `ADVANCED`, `ROTATE` 100% → 20, `ease: OVERSHOOT`, `duration: $gv(anispd)+5$`.
- **Folyamatos forgás**: `LOOP_FW` + `ROTATE`, `duration: 20`.
- **Lebegés**: `LOOP_2W`, `Y_OFFSET` 0 → -5 → 0 → 5 → 0 (0/25/50/75/100%).
- Az animáció sebességét egy NUMBER globális (`anispd`) adja, így egy helyen állítható. ✅
