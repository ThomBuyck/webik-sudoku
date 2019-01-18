from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

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
# def get_sudoku():
random_sudoku = db.execute("SELECT sudoku FROM generated_sudokus ORDER BY random() LIMIT 1")
# print(random_sudoku)
for sudoku_cijfers in random_sudoku:
    sudoku_cijfers = str(sudoku_cijfers).replace(".", " ")
    print(sudoku_cijfers)

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