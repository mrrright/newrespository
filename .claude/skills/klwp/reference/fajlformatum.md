# A .klwp fájl szerkezete

Forrás: 9 preset. 8 preset `preset_info.version = 17` (720×1600, `xscreens`/`yscreens` = 1), egy (Kustom Punk) `version = 11` (540×1200, `xscreens`/`yscreens` mező nélkül). A régebbi verzióból néhány mező hiányozhat, de a szerkezet ugyanaz. ✅
Jelölés: ✅ igazolt · ⚠️ következtetés · ❓ nem igazolt.

## 1. A csomag ✅

A `.klwp` egy **zip**-archívum:

```
preset.json                  ← a teljes háttér leírása
preset_thumb_portrait.jpg    ← előnézeti kép
preset_thumb_landscape.jpg
bitmaps/IMG<hash>            ← képek (kiterjesztés nélkül)
fonts/*.ttf, *.otf           ← betűtípusok
icons/<készlet>.ttf + .json  ← ikonkészletek (material, materialdesignicons, entypo, fontawesome, meteo)
```

A fájlokra a JSON így hivatkozik: `kfile://org.kustom.provider/bitmaps/IMG...`, `kfile://org.kustom.provider/fonts/Roboto-Bold.ttf`. ✅

## 2. preset.json felső szint ✅

```json
{
  "preset_info": {
    "title": "...", "description": "...", "author": "...", "email": "...",
    "features": "WEATHER NOTIFICATIONS UNREAD",
    "width": 720, "height": 1600, "xscreens": 1, "yscreens": 1,
    "version": 17, "id": "<uuid>", "release": ..., "ts": ..., "locked": false, "hash": null, "pflags": 0, "archive": ""
  },
  "preset_root": {
    "internal_type": "RootLayerModule",
    "globals_list": { ... },
    "viewgroup_items": [ ... ]
  }
}
```

- A `features` a használt adatforrásokat sorolja fel. Látott értékek: `LOCATION WEATHER CALENDAR MUSIC DOWNLOAD NOTIFICATIONS UNREAD NETWORK_INFO BLUETOOTH GYRO SIGNAL`. ⚠️ Valószínűleg ebből tudja az alkalmazás, milyen engedélyeket kell kérnie.
- A `width`/`height` mindhárom fájlban 720×1600. ⚠️ Valószínűleg a szerkesztő eszközének mérete, ezért kell a méreteket `si(rwidth)`/`si(rheight)` arányában megadni.

## 3. A tulajdonságok tárolása – a legfontosabb szabály ✅

Minden elem három helyen tárolhat egy tulajdonságot:

```json
{
  "paint_color": "#35000000",                       ← fix érték
  "internal_toggles":  { "paint_color": 10, "text_family": 100 },
  "internal_formulas": { "paint_color": "$gv(txticl)$" },
  "internal_globals":  { "text_family": "txtifnt2" }
}
```

| `internal_toggles` érték | Jelentés | Előfordulás |
|---|---|---|
| `10` | **a képlet aktív** (`internal_formulas`) | 5498 |
| `0` | a fix érték érvényes; a képlet lehet, hogy el van mentve, de ki van kapcsolva | 2132 |
| `100` | **globális változóhoz kötve** (`internal_globals`, a globális nevével) | 64 |

A szabály mindhárom fájlban kivétel nélkül teljesül: 10 → van formula, 100 → van globális kötés. ✅

A globálisoknál ugyanígy: `"toggles": 10` + `"global_formula"`, illetve `"toggles": 100` + `"global": "<másik globális>"`. ✅

## 4. Elemtípusok (`internal_type`) ✅

| Típus | Mire való | Fő tulajdonságok |
|---|---|---|
| `RootLayerModule` | a háttér gyökere | `background_type`, `background_color`, `background_bitmap`, `background_blur`, `background_dim`, `background_filter` (`COLORIZE`), `background_filter_color`, `background_scroll` (`NONE`) |
| `OverlapLayerModule` | csoport, az elemek egymásra kerülnek | `viewgroup_items`, `internal_title`, `config_visible`, `config_filter`, `config_rotate_mode`, `config_tiling` |
| `StackLayerModule` | csoport, az elemek egymás mellé/alá kerülnek | `config_stacking`: `HORIZONTAL_CENTER`, `VERTICAL_CENTER`, `VERTICAL_RIGHT` |
| `TextModule` | szöveg | `text_expression` (a szöveg/képlet), `text_family`, `text_size`, `text_size_type` (`FIXED_WIDTH`), `text_width`, `text_lines`, `text_align` (`CENTER`, `RIGHT`), `text_filter` (`["UP"]`, `["CAP"]`) |
| `CurvedTextModule` | ívelt szöveg | `text_expression`, `text_spacing`, `text_mode` (`JUSTIFY`) |
| `ShapeModule` | alakzat | `shape_type`: `RECT`, `CIRCLE`, `OVAL`, `EXAGON`, `SLICE`, `ARC`, `TRIANGLE`, `RTRIANGLE`; `shape_width`, `shape_height`, `shape_corners`, `shape_angle`, `shape_rotate_mode` |
| `FontIconModule` | ikon ikonkészletből | `icon_set` (kfile ttf), `icon_icon` (ikonnév, pl. `center_focus_weak`), `icon_size` |
| `ProgressModule` | folyamatjelző | `progress_progress` (`CUSTOM`), `progress_level`, `progress_mode` (`SPLIT`, `SHAPES`), `style_style` (`CIRCLE`), `style_shape`, `style_size`, `style_height`, `color_fgcolor`, `color_bgcolor` |
| `KomponentModule` | komponens (beágyazott, saját globálisokkal) | `globals_list`, `internal_title`, `internal_readonly` |

**Zárolt komponensek**: a példák mind a 67 komponense zárolt, a tartalmuk az `internal_readonly` mezőben titkosított/kódolt szövegként van. Ebből nem lehet tanulni. ✅

### Közös tulajdonságok ✅

- Pozíció: `position_anchor` (`CENTER`, `TOP`, `BOTTOM`, `CENTERLEFT`, `CENTERRIGHT`, `TOPLEFT`, `TOPRIGHT`, `BOTTOMLEFT`, `BOTTOMRIGHT`), `position_offset_x/y`, `position_padding_left/right/top/bottom`.
- Festés: `paint_color` (`#AARRGGBB`), `paint_style` (`STROKE`), `paint_stroke`, `paint_mode` (`CLEAR`, `SRC`).
- Érintési esemény (`internal_events`) csoporton kívül közvetlenül alakzaton (ShapeModule) is lehet. ✅
- Szövegen (TextModule) is lehet `paint_style`, `paint_stroke`, `fx_gradient` és `text_rotate_mode`. A ProgressModule-nak `color_color` mezője is van. ✅
- Effektek: `fx_shadow` (`OUTER`), `fx_shadow_color/blur/distance/direction`; `fx_gradient` (`RADIAL`, `SWEEP`, `VERTICAL`, `HORIZONTAL`, `BITMAP`), `fx_gradient_color`, `fx_gradient_offset(_x/_y)`, `fx_gradient_width`, `fx_gradient_bitmap`; `fx_mask` (`CLIP_NEXT`, `CLIP_ALL`); `fx_bitmap_filter/_color/_amount`, `fx_bitmap_dim`, `fx_bitmap_blur`.
- A neumorfikus stílus (NeuMorphicThemeVol2) kulcsa: két `OUTER` árnyék ellentétes irányban, világos és sötét színnel. ⚠️ A sok `fx_shadow_direction`/`fx_shadow_color` párosból következtetve.

## 5. Globális változók (`globals_list`) ✅

Kulcs = a változó neve, érték:

```json
"panelcl": { "index": 1, "type": "COLOR", "title": "panelcl", "description": "panel's color", "value": "#FF181818" }
"txtcl":   { "index": 7, "type": "COLOR", "title": "txtcl", "toggles": 10, "global_formula": "$ce(ce(gv(panelcl),contrast),lum,60)$" }
"pic":     { "type": "LIST", "entries": "$gv(pic1)$,$gv(pic2)$,$gv(pic3)$,$gv(pic4)$", "value": "$gv(pic1)$" }
"anispd":  { "type": "NUMBER", "min": 0, "max": 720, "value": 2.0 }
"swbt":    { "type": "SWITCH", "on_mode": "MANUAL_FORMULA", "on_formula": "$gv(txte5)=1$", "off_mode": "MANUAL_FORMULA", "off_formula": "$gv(txte5)!=1$" }
"txtdfnt": { "type": "FONT", "value": "kfile://org.kustom.provider/fonts/DS-Digib.TTF" }
```

Típusok: `COLOR`, `TEXT`, `NUMBER`, `SWITCH`, `LIST`, `FONT`, `BITMAP`. ✅
- A LIST `entries` mezője vesszővel elválasztott lista, az elemek lehetnek képletek is. ✅
- A TEXT globális `value` mezője is lehet képlet (`"$df(yyyy)$"`). ✅
- A SWITCH automatikusan is kapcsolhat képlet alapján (`on_formula` / `off_formula`). ⚠️ A pontos működés következtetés.

## 6. Érintési események (`internal_events`) ✅

Mindegyik `"type": "SINGLE_TAP"` (9 presetben). A dupla koppintás és a hosszú nyomás nem szerepel. ❓

```json
{ "type": "SINGLE_TAP", "action": "SWITCH_GLOBAL", "switch": "txtd", "switch_text": "1" }     ← szöveges globális beállítása
{ "type": "SINGLE_TAP", "action": "SWITCH_GLOBAL", "switch": "pic" }                          ← SWITCH átkapcsolása / LIST léptetése
{ "type": "SINGLE_TAP", "action": "SWITCH_GLOBAL", "switch": "nyt", "switch_list": "PREV" }   ← LIST visszaléptetése
{ "type": "SINGLE_TAP", "action": "LAUNCH_APP", "intent": "intent:#Intent;action=android.intent.action.MAIN;category=android.intent.category.LAUNCHER;component=<csomag>/<activity>;S.org.kustom.intent.label=<név>;end" }
{ "type": "SINGLE_TAP", "action": "OPEN_LINK", "url": "$wg(gv(nyt),rss,gv(item),link)$" }    ← az URL is lehet képlet
{ "type": "SINGLE_TAP", "action": "MUSIC", "music_action": "NEXT" }                           ← PREVIOUS, PLAY_PAUSE; music_action nélkül ⚠️ valószínűleg az alapértelmezett lejátszás/szünet
{ "type": "SINGLE_TAP", "action": "KUSTOM_ACTION", "kustom_action": "TOGGLE_WIFI" }          ← TOGGLE_BT, NOTIF_CLOSE_ALL
{ "type": "SINGLE_TAP", "action": "KUSTOM_ACTION", "kustom_action": "NOTIF_OPEN", "notification": "1" }   ← az n-edik értesítés megnyitása
{ "type": "SINGLE_TAP", "action": "LAUNCH_ACTIVITY", "intent": "intent:#Intent;component=com.android.settings/.Settings%24HighPowerApplicationsActivity;S.org.kustom.intent.label=Settings;end" }   ← egy alkalmazás adott képernyője (itt: akkumulátor-optimalizálás)
{ "type": "SINGLE_TAP", "action": "CHANGE_VOLUME", "volume_stream": "RINGER", "volume_action": "SET" }
{ "type": "SINGLE_TAP", "action": "LAUNCH_SHORTCUT", "intent": "intent:#Intent;action=...;component=<launcher>/...;end" }   ← indító (pl. Nova) parancsikonja
{ "type": "SINGLE_TAP", "action": "DISABLED" }                                            ← kikapcsolt esemény
```

⚠️ Egy eseményben néhol a `kustom_action` mező is ott van egy másik `action` mellett. Ez valószínűleg egy korábbi beállítás maradványa, nem második művelet.

## 7. Animációk (`internal_animations`) ✅

```json
{ "type": "FORMULA", "formula": "$if(gv(txta)=1,1,0)$", "action": "ADVANCED", "ease": "STRAIGHT",
  "duration": 4.0, "delay": 10.0,
  "animator": [
    { "position": 0,   "property": "SCALE_XY", "value": 0.0, "ease": "STRAIGHT" },
    { "position": 100, "property": "SCALE_XY", "value": 1.0, "ease": "STRAIGHT" } ] }
```

| Mező | Látott értékek |
|---|---|
| `type` (kiváltó) | `FORMULA` (212), `SWITCH` (126, `trigger`: SWITCH globális neve), `LOOP_2W` (47, oda-vissza), `VISIBILITY` (33, amikor az elem láthatóvá válik ⚠️), `LOOP_FW` (32, csak előre), `GYRO` (5, a telefon döntésére, `axis`: `Y`, `Z`), `SCROLL` (4, képernyőváltáskor, `center`: `SCREEN1`, `SCREEN2`), `DISABLED` (1) |
| `action` | `ADVANCED` (378, kulcskockás), `FADE_INVERTED` (22), `ROTATE`, `ROTATE_INVERTED`, `SCROLL`, `SCROLL_INVERTED`, `COLOR`, `FADE`, `SCALE_X`, `SCALE_Y`, `SCALE_INVERTED`; néha hiányzik |
| `ease` | `STRAIGHT`, `INVERTED`, `OVERSHOOT`, `BOUNCE`, `STRAIGHT_2W` |
| `animator[].property` | `OPACITY`, `Y_OFFSET`, `X_OFFSET`, `SCALE_XY`, `SCALE_X`, `SCALE_Y`, `ROTATE`, `DESATURATE` |
| `animator[].position` | 0–100, az animáció százalékában |
| egyéb | `anchor` (`MODULE_TOP`, `MODULE_LEFT`, `MODULE_RIGHT`), `axis`, `speed`, `angle` (pl. 180, 270), `amount`, `limit`, `center`, `trigger` |

- A `duration`/`delay` is lehet képlet (`internal_toggles`/`internal_formulas`, mint az elemeknél): `"duration": "$gv(anispd)+10$"`. ✅
- **Lépcsőzetes megjelenés**: egy SWITCH-re (`trigger: swapps`) kötött `ADVANCED` animáció több elemen, különböző kezdő `Y_OFFSET`-tel (120, 240, 360) és késleltetéssel (`delay: $if(gv(swapps)=1,2,0)$`, illetve `delay: 1.0`). Így az alkalmazásikonok egymás után úsznak be. ✅
- `SCROLL` animációnál a `center` adja meg, melyik képernyőn van a 0% állapot, és mellette `formula` is lehet (`$if(si(screen)=2,1,0)$`). ✅ A `center` pontos jelentése ⚠️.
- Az animáció típusa képlettel ki-be kapcsolható: `"type": "$if(mi(state)=playing,loop_2w,disabled)$"`. ✅
- ❓ `OPACITY` irány: a példákban mindkét irány előfordul. Kb. 130 animációban a 0% kockán 100 és a 100% kockán 0 van, kb. 40-ben fordítva. Ebből nem dönthető el, hogy az animátorban a 100 teljesen látható vagy teljesen átlátszó állapotot jelent. Kipróbálással kell ellenőrizni.
- ⚠️ `FORMULA` típusnál a képlet eredménye (0 vagy 1) a példák alapján azt mondja meg, az animáció a kezdő (0) vagy a végállapotban (1) legyen. Előfordulnak 4-es, 5-ös, 6-os értékek is (`$if(si(screen)=3,6,0)$`), ezek jelentése nem világos.
- ⚠️ `FORMULA` típusnál a képlet gyakran `f` vagy `r` betűt ad vissza (`$if(gv(hack)=0,r,f)$`, `$if(gv(phnbtn)=1,f,r)$`), egy helyen `b`-t is (`$if(gv(hack)=0,f,b)$`). Nagyon valószínű, hogy `f` = előre (forward), `r` = visszafelé (reverse). A `b` jelentése ismeretlen.
- A Kustom Punk presetben a másodpercek (`df(ss)`) szerint 6 másodpercenként előre lejátszott animáció is van: `$if(df(ss)=00,f,df(ss)=06,f,...,r)$`. ✅

## 8. Furcsaságok a példákban ⚠️

- A szerzők a saját elérhetőségüket egy kikapcsolt (`toggles: 0`) `config_visible` képletmezőbe írják, aláírásként. Ez nem működési szabály.
- Egy `config_filter` mező képlete az összes globális `$gv(...)$` hivatkozását egymás után tartalmazza. Valószínűleg arra szolgál, hogy bármelyik globális változásakor frissüljön a csoport, de ez nem bizonyított.
