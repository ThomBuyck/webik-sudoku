from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from __future__ import division
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




def random_select():
    """
    selects a 'random' opponent
    with the right elo rating.
    """

    # Get elo rating from user.
    elo_rating_user = db.execute("SELECT elo_rating FROM users WHERE id = :user_id", user_id=session["user_id"])

    # Calculate interval to search for the right opponent.
    min_elo_r_opp = elo_rating_user - 40
    max_elo_r_opp = elo_rating_user + 40

    # Selects the opponent, remember opponent ID.
    opponent_id = db.execute("SELECT id FROM users ORDER BY random() LIMIT 1 WHERE elo_rating BETWEEN min_elo_r_opp AND max_elo_r_opp", min_elo_r_opp, max_elo_r_opp)

    # Get his elo rating.
    elo_opponent = db.execute("SELECT elo FROM elo_rating WHERE id = :opponent_id BETWEEN", opponent_id=opponent_id)

    # Return his elo_rating.
    return  elo_opponent

elo_user = db.execute("SELECT elo FROM elo_rating WHERE id = :user_id", user_id=session["id"])

def elo_calculate(elo_user,elo_opponent, score, k=32):
    """
    P1 = elo_rating_user
    P2 = elo_rating_opponent
    k = 32 constant variable
    score, 0 for loser, 0.5 for draw(both players), 1 for winner.

    E1 = 10^(elo_rating_user/400)
    E2 = 10^(elo_rating_opponent/400)

    R1 = new rating user
    R2 = new rating opponent

    R1 = P1 + k(score - E1/(E1 - E2))
    R2 = P2 + k(score - E2/(E1 - E2))

    rounding the new elo ratings would be nice.
    """
    E1 = 10**(elo_rating_user/400)
    E2 = 10**(elor_ratin_opponent/400)

    new_elo_user = round(elo_user + k * (score - E1/(E1-E2)))

    db.execute("UPDATE users SET elo_rating = :new_elo_user WHERE id = :user_id", new_elo_user=new_elo_user, user_id=session["id"])
    return  redirect(url_for("index"))

