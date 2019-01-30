from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
import json
from random import randint

from helpers import *

# import MySQLdb
# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///sudokus.db")


@app.route("/levels", methods=["GET", "POST"])
@login_required
def levels():
    """Generates the level template."""
    return render_template("levels.html")


@app.route("/looks", methods=["GET", "POST"])
@login_required
def get_sudoku():
    """Retrieves a random sudoku from the database based on the level for singleplayer mode."""

    if request.method == "POST":
        # Determines the level based on a button click
        if request.form['level'] == "Simple":
            lev = "simple"
            session["level"] = "simple"
        elif request.form['level'] == "Easy":
            lev = "easy"
            session["level"] = "easy"
        elif request.form['level'] == "Intermediate":
            lev = "intermediate"
            session["level"] = "intermediate"
        elif request.form['level'] == "Expert":
            lev = "expert"
            session["level"] = "expert"

        # Retrieves a random_sudoku from the database based on the level selected by the user
        session["level"] = lev
        ran = random_number()
        session["random_number"] = ran

        random_sudoku = db.execute("SELECT sudoku FROM generated_sudokus WHERE id=:id AND level=:level", id=ran, level=lev)

        # Converts the sudoku to a 2d list to work with and stores it in a session
        for x in random_sudoku:
            for y in x.values():
                sudoku = y

        lst = [sud for sud in sudoku]
        repl = [w.replace('.', ' ') for w in lst]

        sudoku_list = [repl[i:i+9] for i in range(0, len(repl), 9)]
        session["sudoku"] = sudoku_list
        return render_template("looks.html", ran=range(9), cijfers=sudoku_list)
    else:
        # If request method is GET:
        return render_template("index.html")


@app.route("/multiplayer_levels", methods=["GET", "POST"])
@login_required
def multiplayer_levels():
    """Renders the levelselect page for multiplayer."""
    # Store the friend retrieved from the play with friend button in a session
    if request.method == "POST":

        multiplayer_friend = request.form['friend']
        session['mpfriend'] = multiplayer_friend
        print("mp", session['mpfriend'])
        return render_template("multiplayer_levels.html")
    else:
        return render_template("multiplayer_levels.html")


@app.route("/multiplayer_looks", methods=["GET", "POST"])
@login_required
def multiplayer_looks():
    """Retrieves a random sudoku from the database for multiplayer mode."""
    if request.method == "POST":
        # Determines the level based on a button click
        if request.form['level'] == "Simple":
            lev = "simple"
            session["level_mul"] = "simple"
        elif request.form['level'] == "Easy":
            lev = "easy"
            session["level_mul"] = "easy"
        elif request.form['level'] == "Intermediate":
            lev = "intermediate"
            session["level_mul"] = "intermediate"
        elif request.form['level'] == "Expert":
            lev = "expert"
            session["level_mul"] = "expert"
        session["level_mul"] = lev

        # Retrieves a random_sudoku from the database based on the level selected by the user
        random = random_number()
        session["random_number"] = random
        random_sudoku = db.execute("SELECT sudoku FROM generated_sudokus WHERE id=:id AND level=:level", id=random, level=lev)

        # Convert sudoku to a 2d list to work with
        for x in random_sudoku:
            for y in x.values():

                sudoku = y

        lst = [sud for sud in sudoku]
        repl = [w.replace('.', ' ') for w in lst]

        sudoku_list = [repl[i:i+9] for i in range(0, len(repl), 9)]
        session["sudoku_lst"] = sudoku_list

        return render_template("multiplayer_looks.html", ran=range(9), cijfers=sudoku_list)
    else:
        # If request method is GET:
        return render_template("index.html")


# Set the variable seconds left to 0 to work with later
sec_left = 0


@app.route("/checking", methods=["GET", "POST"])
@login_required
def checking():
    """Checks the sudoku for correctness in singleplayer mode."""
    if request.method == 'POST':
        # Retrieves the seconds left from timer to work with in points function(helpers)
        time_left = str(request.form['timeleft'])
        # convert to seconds
        global sec_left
        sec_left = sum(x * int(t) for x, t in zip([60, 1], time_left.split(":")))

    sol = solution(session["random_number"], session["level"])

    data = get_data()
    score = points(session["sudoku"])
    user = db.execute("SELECT username FROM users WHERE id=:id", id=session["user_id"])
    # Put the played sudokus in the history database
    db.execute("INSERT INTO history (user,opponent,sudoku_id,level,gamemode,player_score,friend_score) VALUES(:user, :opponent, :sudoku_id, :level, :gamemode, :player_score, :friend_score)",
               user=user[0]["username"], opponent="/", sudoku_id=session["random_number"], level=session["level"], gamemode="Singleplayer", player_score=score, friend_score="/")

    # Check if answer is correct
    if data == sol:
        return render_template("wonlost.html", score=score, solved="solved", time=sec_left)
    else:
        return render_template("wonlost.html", score=score, solved="not solved", time=sec_left)


@app.route("/multiplayer_checking", methods=["GET", "POST"])
@login_required
def multiplayer_checking():
    """Checks the sudoku for who won in multiplayer mode."""
    if request.method == 'POST':
        # Retrieves the time left to work with in multiplayer_points(helpers)
        time_left = str(request.form['timeleft'])
        # convert to seconds
        sec_left = sum(x * int(t) for x, t in zip([60, 1], time_left.split(":")))

    score = mp_points(session["sudoku_lst"])

    sudoku_id = session["random_number"]

    user = db.execute("SELECT username FROM users WHERE id=:id", id=session["user_id"])

    dbrow = db.execute("SELECT * FROM played_games WHERE (user=:user AND opponent=:opponent AND level=:level AND gamemode=:gamemode)  ORDER BY id DESC LIMIT 1",
                       user=session["mpfriend"], opponent=user[0]["username"], level=session["level_mul"], gamemode="Multiplayer")

    # Check if friend already played, if not:
    if not dbrow:

        dbex = db.execute("INSERT INTO played_games (user, opponent, sudoku_id, level, gamemode, player_score, friend_score) VALUES(:user, :opponent, :sudoku_id, :level, :gamemode, :player_score, :friend_score)",
                          user=user[0]["username"], opponent=session["mpfriend"], sudoku_id=sudoku_id, level=session["level_mul"], gamemode="Multiplayer", player_score=score, friend_score=0)

        db.execute("INSERT INTO history (user, opponent, sudoku_id, level, gamemode, player_score, friend_score) VALUES(:user, :opponent, :sudoku_id, :level, :gamemode, :player_score, :friend_score)",
                   user=user[0]["username"], opponent=session["mpfriend"], sudoku_id=sudoku_id, level=session["level_mul"], gamemode="Multiplayer", player_score=score, friend_score=0)
        db.execute("INSERT INTO history (user, opponent, sudoku_id, level, gamemode, player_score, friend_score) VALUES(:user, :opponent, :sudoku_id, :level, :gamemode, :player_score, :friend_score)",
                   user=session["mpfriend"], opponent=user[0]["username"], sudoku_id=sudoku_id, level=session["level_mul"], gamemode="Multiplayer", player_score=score, friend_score=0)

        scorepoints = db.execute("SELECT player_score FROM played_games WHERE (user=:user AND opponent=:opponent AND sudoku_id=:sudoku_id)",
                                 user=user[0]["username"], opponent=session["mpfriend"], sudoku_id=session["random_number"])
        if scorepoints:
            return render_template("multiplayer_msg.html", dbrow=dbrow, friend=session["mpfriend"], score=scorepoints[0]['player_score'])
        else:
            return render_template("multiplayer_msg.html", dbrow=dbrow, friend=session["mpfriend"], score=score)
    # Else, update the databases and check who has won the game
    else:
        update_score = db.execute("UPDATE played_games SET friend_score=:friend_score WHERE (user=:user AND opponent=:opponent AND level=:level AND gamemode=:gamemode) ORDER BY id DESC LIMIT 1",
                                  friend_score=score, user=session["mpfriend"], opponent=user[0]["username"], level=session["level_mul"], gamemode="Multiplayer")
        update_his = db.execute("UPDATE history SET friend_score=:friend_score WHERE (user=:user AND opponent=:opponent AND level=:level AND gamemode=:gamemode)",
                                friend_score=score, user=session["mpfriend"], opponent=user[0]["username"], level=session["level_mul"], gamemode="Multiplayer")
        update_his = db.execute("UPDATE history SET friend_score=:friend_score WHERE (user=:user AND opponent=:opponent AND level=:level AND gamemode=:gamemode)",
                                friend_score=score, user=user[0]["username"], opponent=session["mpfriend"], level=session["level_mul"], gamemode="Multiplayer")
        scores = db.execute("SELECT player_score, friend_score FROM played_games WHERE (user=:user AND opponent=:opponent) ORDER BY id DESC LIMIT 1",
                            user=session["mpfriend"], opponent=user[0]["username"])

        delete_played = db.execute("DELETE FROM played_games WHERE user=:user and opponent=:opponent",
                                   user=session["mpfriend"], opponent=user[0]["username"])
        if scores[0]['player_score'] > scores[0]['friend_score']:
            return render_template("multiplayer_msg.html", dbrow=dbrow, friend=session["mpfriend"], played="played", friendscore=scores[0]['friend_score'], wonlost="won", score=scores[0]['player_score'])
        elif scores[0]['player_score'] == scores[0]['friend_score']:
            return render_template("multiplayer_msg.html", dbrow=dbrow, friend=session["mpfriend"], played="played", friendscore=scores[0]['friend_score'], wonlost="played a tie", score=scores[0]['player_score'])
        else:
            return render_template("multiplayer_msg.html", dbrow=dbrow, friend=session["mpfriend"], played="played", friendscore=scores[0]['friend_score'], wonlost="lost", score=scores[0]['player_score'])


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    if request.method == "POST":
        # ensure form was enterily filled
        if not request.form.get("username"):
            return apology("must provide username")
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hashed"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        return redirect(url_for("index"))
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    # Remove user_id
    session.clear()

    if request.method == "POST":
        # Check if form is filled in correctly
        if not request.form.get("username"):
            return apology("Vul een gebruikersnaam in")
        elif not request.form.get("password"):
            return apology("Vul een wachtwoord in ")
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("wachtwoorden komen niet overeen!")

        # Insert user data into database
        data = db.execute("INSERT INTO users (username, hashed, email) VALUES (:username, :hashed, :email)",
                          username=request.form.get("username"), hashed=pwd_context.hash(request.form.get("password")), email=request.form.get("email"))

        if not data:
            return apology("Username is already taken!!!")
        else:
            session["user_id"] = data

        return redirect(url_for("index"))

    else:
        return render_template("register.html")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Loads index page"""
    return render_template("index.html")


@app.route("/multiplayer", methods=["GET", "POST"])
@login_required
def multiplayer():
    """Display multiplayer page with friends list on it"""
    user = db.execute("SELECT username FROM users WHERE id=:id", id=session["user_id"])
    friends = db.execute("SELECT friend FROM friends WHERE user=:user", user=user[0]["username"])
    friend_set = set()
    for f in friends:
        for friend in f.values():
            friend_set.add(friend)
    print(friend_set)

    return render_template("multiplayer.html", friends=friend_set)


@app.route("/friend_check", methods=["GET", "POST"])
@login_required
def friend_check():
    """Checks if friends form is filled in correctly"""
    if request.method == "POST":
        # Selecting rows from database to check if friend form is filled in correctly
        user = db.execute("SELECT username FROM users WHERE id=:id", id=session["user_id"])
        select_user = db.execute("SELECT username FROM users WHERE (username=:username)", username=request.form.get("search"))
        select_friends = db.execute("SELECT * FROM friends WHERE (user=:user AND friend=:friend)",
                                    user=user[0]["username"], friend=request.form.get("search"))

        select = [user[0][k] for k in user[0]]

        friend = db.execute("INSERT INTO friends (user, friend) VALUES(:user,:friend)",
                            user=user[0]["username"], friend=request.form.get("search"))
        friend2 = db.execute("INSERT INTO friends (user, friend) VALUES(:user, :friend)",
                             user=request.form.get("search"), friend=user[0]["username"])

        # Return apology for different reasons why friend can't be added
        if request.form["search"]:
            if request.form.get("search") == select[0]:
                db.execute("DELETE FROM friends WHERE (user=:user AND friend=:friend) LIMIT 1",
                           user=user[0]["username"], friend=request.form.get("search"))
                db.execute("DELETE FROM friends WHERE (user=:user AND friend=:friend) LIMIT 1",
                           user=request.form.get("search"), friend=user[0]["username"])
                return apology("You can't add yourself as a friend")
            elif not select_user:
                db.execute("DELETE FROM friends WHERE (user=:user AND friend=:friend) LIMIT 1",
                           user=user[0]["username"], friend=request.form.get("search"))
                db.execute("DELETE FROM friends WHERE (user=:user AND friend=:friend) LIMIT 1",
                           user=request.form.get("search"), friend=user[0]["username"])
                return apology("That user doesn't exist")
            elif select_friends:
                db.execute("DELETE FROM friends WHERE (user=:user AND friend=:friend) LIMIT 1",
                           user=user[0]["username"], friend=request.form.get("search"))
                db.execute("DELETE FROM friends WHERE (user=:user AND friend=:friend) LIMIT 1",
                           user=request.form.get("search"), friend=user[0]["username"])
                return apology("You already have that user as a friend")
            elif friend:
                return friendadded("Friend succesfully added!")
        elif request.form["friend"]:
            db.execute("DELETE FROM friends WHERE (user=:user AND friend=:friend)",
                       user=user[0]["username"], friend=request.form.get("search"))
            db.execute("DELETE FROM friends WHERE (user=:user AND friend=:friend)",
                       user=request.form.get("search"), friend=user[0]["username"])
            return render_template("multiplayer_levels.html")
        else:
            return apology("Please provide valid input")
    else:
        return render_template("multiplayer.html")


@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    return redirect(url_for("login"))


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """Generates profile page"""
    # Get user column
    user = db.execute("SELECT username FROM users WHERE id=:id", id=session["user_id"])

    # Get columns from played_games
    played = db.execute(
        "SELECT user, opponent, level, gamemode, player_score, friend_score FROM history WHERE user=:user ORDER BY id DESC", user=user[0]["username"])

    return render_template("profile.html", played=played, username=user[0]["username"])


@app.route("/wonlost")
@login_required
def wonlost():
    """Generates page for won or lost with points"""
    return render_template("wonlost.html")

