from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
import json
from random import randint
from pprint import pprint
from bs4 import BeautifulSoup
import pandas as pd
# import BeautifulSoup
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
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")
# @app.route("/levels", methods=["GET", "POST"])
# def level():
#     if request.method == "POST":

#         if request.form['level'] == "simple":
#             return("simple")
#         elif request.form.get["level"] == "Easy":
#             return ("easy")
#         elif request.form.get["level"] == "Intermediate":
#           return ("intermediate")
#         elif request.form.get["level"] == "Expert":
#             return ("expert")
#     else:
#         return render_template("levels.html")

@app.route("/looks", methods=["GET", "POST"])
def get_sudoku():

    # if request.method == "POST":
    #     lev = level()
    #     if lev in ["simple", "easy", "intermediate", "expert"]:
    random_sudoku = db.execute("SELECT sudoku FROM generated_sudokus WHERE id=:id", id=sudoku_id)

    for x in random_sudoku:
        for y in x.values():
            sudoku = y

    lst = [sud for sud in sudoku]
    repl = [w.replace('.', ' ') for w in lst]
    new_list = [repl[i:i+9] for i in range(0, len(repl), 9)]

    return render_template("looks.html", lst=lst, ran = range(9), cijfers = new_list)
    #     else:
    #         return render_template("looks.html")
    # else:
    #     return render_template("looks.html")

def solution():
    solution = db.execute("SELECT solution FROM generated_sudokus WHERE id=:id", id=sudoku_id)
    return solution


def get_sudoku_data():
    data = []
    for x in range(81):
        cijfers = request.form.get['cijfer']
        data.append(cijfers)
    return data

def check_complete(sudoku):
    get_sudoku()
    sol = solution()
    df = pd.read_html('looks.html')[0]
    df_list = df.values.tolist()

    if df_list == sol:
        return render_template("index.html")
    else:
        return ("You failed")


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
        elif len(db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))) == 1:
            return apology("confirmation password must match password")

        db.execute("INSERT INTO users (username, hashed, email) VALUES (:username, :hashed, :email)",
                username=request.form.get("username"), hashed =pwd_context.hash(request.form.get("password")), email=request.form.get("email"))

        #veranderen
        return redirect(url_for("register"))

    else:
        return render_template("register.html")


    return apology("TODO")