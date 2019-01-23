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
* Scores bijhouden/History (POST) (functie: score)
* Kijken of de sudoku af is en als niet af is kijken hoeveel goede cijfers ingevuld (functie: is_complete)
* ~~Moeilijkheid sudokus (functie: sudoku_level)~~
* vriendenlijst (functie: friends_list)




### Features

* scorelijst van vrienden
* vriendenlijst
* Sudoku’s spelen (multiplayer en ~~singleplayer~~)
* Vrienden uitnodigen
* ~~Inlog en registratiepagina~~
* Database ~~gebruikers~~ en scores.
* ~~ELO systeem~~

### Model/helpers

* ~~Sudoku invullen~~
* ~~Login vereist~~
* Scores weergeven
* ~~Elo systeem~~
* Timer
* Chat (optioneel)


### MVP

* ~~sudokus spelen~~
* `vrienden uitnodigen`
* `Vriendenlijst`
* ~~Inlog en registratiepagina~~
* score
* match history

### Plugins en frameworks

* Bootstrap (https://getbootstrap.com/docs/4.1/getting-started/introduction/)
* Numpy (https://docs.scipy.org/doc/)
* Elo (https://github.com/HankMD/EloPy)






