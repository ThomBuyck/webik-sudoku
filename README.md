# Webik-sudoku
#### Projectvoorstel Webprogrammeren en databases IK
###### Groep: 08 Thom Buyck, Stijn Hering en Melvin Crombeen

### Samenvatting

Wij willen een website maken waarbij spelers sudoku’s voor zichtzelf kunnen spelen maar ook tegen elkaar.
Je verdient punten met het maken van sudokus. Zo krijg je punten per goed ingevulde vakje en krijg je punten
als je in een bepaalde tijd klaar bent met de sudoku. Deze punten worden opgeslagen in een database.
Als de gebruiker goed is in sudokus en hij/zij wilt een keer een potje spelen tegen iemand anders zal de gebruiker tegen een gelijkwaardig
tegenstanders spelen (elo rating).

### Controllers

* ~~Login/register (POST)~~
* ~~Sudoku’s ophalen uit database (POST) (functie: get_sudoku)~~
... (we hebben zelf sudokus gegeneert omdat onze eerste database niet het sudoku niveau gaf, we hebben daarom het heft in eigen handen genomen en voor 4 verschillende niveaus sudokus gegenereert.
     voor nu hebben we 1000 sudokus per niveau gemaakt)
* ~~Scores bijhouden/History (POST) (functie: score)~~
   Bij je profile heb je een scorebord met gespeeld games en hoeveel punten je hebt gehaald.
* ~~Kijken of de sudoku af is en als niet af is kijken hoeveel goede cijfers ingevuld (functie: checking)~~
   staat in application.py
* ~~Moeilijkheid sudokus~~

   alles staat op level in de database.
* ~~vriendenlijst (functie: friends)~~




### Features

* vriendenlijst

   staat in de multiplayer pagina, vrienden toevoegen en knop om tegen ze te spelen,
   daarnaast is er een check knop om te kijken of je nog moet spelen tegen andere.
* ~~Sudoku’s spelen (multiplayer en singleplayer)~~

   zowel singleplayer en multiplayer sudokus kan je nu spelen, voor singleplayer en multiplayer krijg je punten.
* Vrienden uitnodigen

   is net niet gelukt, heeft wellicht te maken dat we met ze 3en zijn.
* ~~Inlog en registratiepagina~~

   werkt helemaal
* ~~Database gebruikers en scores.~~
* ELO systeem

   Was wel een code voor geschreven maar sinds we niet toe kwamen aan random spelers uit te kunnen kiezen is de website nu gericht op..
   alleen maar vrienden.

### Model/helpers

* Sudoku invullen
* Login vereist
* Scores weergeven
* Timer



### MVP

* ~~sudokus spelen~~
* ~~vrienden uitnodigen~~
* ~~Vriendenlijst~~
* ~~Inlog en registratiepagina~~
* ~~score~~
* ~~match history~~

### Plugins en frameworks

* Bootstrap (https://getbootstrap.com/docs/4.1/getting-started/introduction/)
* Javascript
