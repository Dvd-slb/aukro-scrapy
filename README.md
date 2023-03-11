# aukro-scrapy
Script za použití knihovny Scrapy prohledá nabídky aukcí uživatele Paleto, který poskytuje aukce celých palet s různě namíchaným zbožím.
Důležité údaje o aukcích, včetně nejdražšího zboží z palety, se ukládají do databáze.
Se spuštěným scriptem app.py každý večer proběhne aktualizace databáze (bez nutnosti spouštět scrapy přes příkazový řádek) a zároveň pošle notifikaci (na pc/telefon), pokud se během nastávajícího večera bude dražit paleta, u které zatím nejvyšší nabídka nedosáhla ani 10% ceny z celkové hodnoty zboží.
K odesílání notifikací je potřeba zadat vlastní Access-Token získaný po registraci na pushbullet.com.
