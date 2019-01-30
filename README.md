# Webik-sudoku
#### Projectvoorstel Webprogrammeren en databases IK
###### Groep: 08 Thom Buyck, Stijn Hering en Melvin Crombeen

### Samenvatting

Wij willen een website maken waarbij spelers sudoku’s voor zichtzelf kunnen spelen maar ook tegen elkaar.
Je verdient punten met het maken van sudokus. Zo krijg je punten per goed ingevulde vakje en krijg je extra punten
als je binnen de tijd klaar bent met een sudoku. Deze punten worden opgeslagen in een database.

In het begin was het een beetje zoeken wie wat zou gaan doen, maar gaandeweg ontstond er een globale taakverdeling. Melvin heeft de sudoku werkend gemaakt en de databases met de history en scores gedaan. Stijn heeft de opmaak gedaan en ook deels meegewerkt aan de databases. Thom heeft de pagina's en de timerfunctie gemaakt.

### Controllers

* Login/register (POST)
* Sudoku’s ophalen uit database (POST) (functie: get_sudoku)
... (We hebben zelf sudokus gegeneert omdat onze eerste database niet het sudoku niveau gaf, we hebben daarom het heft in eigen handen genomen en voor 4 verschillende niveaus sudokus gegenereert.
     voor nu hebben we 1000 sudokus per niveau gemaakt)
* Scores bijhouden/History (POST) (functie: score)
* Kijken of de sudoku af is en als niet af is kijken hoeveel goede cijfers ingevuld (functie: is_complete)
* Moeilijkheid sudokus (functie: sudoku_level)
* vriendenlijst (functie: friends_list)




### Features

* scorelijst van vrienden
* vriendenlijst
* Sudoku’s spelen (multiplayer en singleplayer)
* Inlog en registratiepagina
* Database gebruikers en scores.


### Model/helpers

* Sudoku invullen
* Login vereist
* Scores weergeven
* Timer



### MVP

* Sudokus spelen
* Vriendenlijst
* Inlog en registratiepagina
* Score
* Match history

### Plugins en frameworks

* Bootstrap (https://getbootstrap.com/docs/4.1/getting-started/introduction/)
* Numpy (https://docs.scipy.org/doc/)
* Elo (https://github.com/HankMD/EloPy)






