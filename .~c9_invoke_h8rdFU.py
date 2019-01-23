from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
import json
from random import randint
from pprint import pprint
from bs4 import BeautifulSoup
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


ran = randint(2,1000)
sudoku_id = ran

@app.route("/levels", methods=["GET", "POST"])
def levels():
    if request.method == "POST":
        return render_template("levels.html")
    else:
        return render_template("levels.html")

@app.route("/looks", methods=["GET", "POST"])
def get_sudoku():
    if request.method == "POST":
        if request.form['level'] == "Simple":
            lev = "simple"
        elif request.form['level'] == "Easy":
            lev = "easy"
        elif request.form['level'] == "Intermediate":
            lev = "intermediate"
        elif request.form['level'] == "Expert":
            lev ="expert"


        random_sudoku = db.execute("SELECT sudoku FROM generated_sudokus WHERE id=:id AND level=:level", id=sudoku_id, level=lev)

        for x in random_sudoku:
            for y in x.values():
                sudoku = y

        lst = [sud for sud in sudoku]
        repl = [w.replace('.', ' ') for w in lst]
        new_list = [repl[i:i+9] for i in range(0, len(repl), 9)]

        return render_template("looks.html", lst=lst, ran = range(9), cijfers = new_list)
    else:
        return render_template("looks.html")

def solution():
    solution = db.execute("SELECT solution FROM generated_sudokus WHERE id=:id", id=sudoku_id)
    for x in solution:
        for y in x.values():
            sol = y

    lst = [s for s in sol]
    repl = [w.replace('.', ' ') for w in lst]
    new_list = [repl[i:i+9] for i in range(0, len(repl), 9)]
    return new_list

@app.route("/checking", methods=["GET", "POST"])
def checking():

    sol = solution()

    new_list = [[0 for x in range(9)] for y in range(9)]
    for x in range(9):
        for y in range(9):
            get_data = request.form.get(str(x) + " - " + str(y))
            new_list[x][y] = get_data

    if new_list == sol:
        return render_template("index.html")
    else:
        return render_template("Lost.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hashed"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    # clear user_id
    session.clear()
    # wanneer gebruiker via Post
    if request.method == "POST":
        # check username
        if not request.form.get("username"):
            return apology("Vul een gebruikersnaam in")
        # check wachtwoord
        elif not request.form.get("password"):
            return apology("Vul een wachtwoord in ")
        # Check of 2x zelfde wachtwoord is ingevuld
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("wachtwoorden komen niet overeen!")


        data = db.execute("INSERT INTO users (username, hashed, email) VALUES (:username, :hashed, :email)",
                username=request.form.get("username"), hashed =pwd_context.hash(request.form.get("password")), email=request.form.get("email"))
        if not data:
            return apology("Username is already taken!!!")
        else:
            session["user_id"] = data
        #veranderen
        return redirect(url_for("index"))

    else:
        return render_template("register.html")

    return apology("TODO")

@app.route("/", methods=["GET", "POST"])
@login_required
def index():

    return render_template("index.html")

@app.route("/multiplayer", endpoint = 'multiplayer', methods=["GET", "POST"])
@login_required
def multiplayer():

    return apology("SORRY! WORK IN PROGRESS")


@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/profile", methods=["GET", "POST"])
def profile():
    # Get user col
    user = db.execute("SELECT * FROM users WHERE id=:id", id = session["user_id"])
    # Get singleplayer score col
    points = db.execute("SELECT points FROM singleplayer_score WHERE id=:id", id = session["user_id"])
    # Get username
    username = user[0]["username"]
<<<<<<< HEAD
    return render_template("profile.html",username=username)

@app.route("/lost")
def lost():
    return render_template("Lost.html")
=======
    e_mail = user[0]["email"]


    return render_template("profile.html", username=username, e_mail=e_mail, points=points)
>>>>>>> fd912d5335543253292626c6ab22aeb2a2461721
