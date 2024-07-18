# Bank_api
Banki számlakezelő rendszer api (flask-restx)

A mappa letöltése után létre kell hozni egy virtuális környezetet:
## Windows:

> python -m venv venv

> venv\Scripts\activate

### Majd le kell tölteni a requirements.txt-ből a szükséges csomagokat:

> pip install -r requirements.txt

## Linux:

> python3 -m venv venv

> source venv/bin/activate

### -||-

> pip install -r requirements.txt

## Esetlegesen ha bármi probléma merülne fel a db.sqlite3 adatbázissal:

> flask shell

### létre kell hozni az adatbázis a db_models.py-ban meghatározott séma szerint:

> from db_models import *
>db.create_all()

### Ezzel létre is lett hozva az adatbázis

## A unit teszt elindításu után az adatbázi törlődik újra létre kell hozni

# Swagger dokumentáció
Elérhető a localhost:5000 cím alatt a hozzá tartozó json fájlt is el lehet onnan érni

## Autorizáció
Ha nincs a felhasználónak profilja akkor létre tud hozni egyet majd azzal bejelentkezni
A sikeres bejelentkezéskor visszakapunk egy 'Kulcs'-nak keresztelt WebTokent amit az Authorize gombra kattintva meg lehet adni fontos, hogy előtte be kell írni a 'Bearer ' kifejezést majd beilletszteni a kulcsot.

## Admin ügyfél és sima ügyfél:
Az admin ügyfél mindenki adatát látja és módosíthatja, viszont a sima mazei ügyfél csak a saját adatait látja és módosíthatja és azt is csak korlátok között.

# Metódusok

Minden Class-nak van GET, POST, PUT, DELETE metódusa, tehát:

1. Ugyfelek
2. Szamlak
3. Utalasok
4. Befizetes
5. Penzfelvetel
   
ezek korlátozást kaptak az ügyfelek fajtái szerint.

## Példa:
Admin ügyfél:
Létre tud hozni a saját azonosítóján túl is számlákat más ügyfeleknek és bármennyi kezdő egyenleget el tud helyezni rajta.
Sima ügyfél:
Automatikusan magának generálja le a számlát 0 ft egyenleggel.

# Felhasznaloi felület
Ezen a linken érhető el: https://github.com/j6n0s/Bank-app.git
A program elindítása a readme-ben található
Egy teljes vizuális felület amely ellátja a fontosabb műveleteket (értelemszerűen erre is vonatkozik az admin privilégiuma - minden adat felett diszponál)

# Továbbfejlesztés (példák)
Nagyobb körü megszorítások bevezetése:
- email valódiságának megvizsgálása
- jelszó erősségénak vizsgálata
- dátum vizsgálat (18 év feletti az ügyfél?)
- befizetési kérelem összekötése a külső pézfeldolgozó rendszerekkel 
- pénzfelvétel hitelesítése, -||-
- külön admin felület létrehozása
