from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
import json

from helpers import *

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

@app.route("/looks", methods=["GET", "POST"])
def get_sudoku():

    random_sudoku = db.execute("SELECT sudoku FROM generated_sudokus ORDER BY random() LIMIT 1")

    for x in random_sudoku:
        for y in x.values():
            sudoku = y

    lst = [sud for sud in sudoku]
    repl = [w.replace('.', ' ') for w in lst]
    new_list = [repl[i:i+9] for i in range(0, len(repl), 9)]

    return render_template("looks.html", lst=lst, ran = range(9), cijfers = new_list)


def is_complete(sudoku):





