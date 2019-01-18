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

    # Calculate interval for to search for the right opponent.
    min_elo_r_opp = elo_rating_user - 40
    max_elo_r_opp = elo_rating_user + 40


    opponent_id = db.execute("SELECT id FROM users ORDER BY random() LIMIT 1 WHERE elo_rating BETWEEN min_elo_r_opp AND max_elo_r_opp", min_elo_r_opp, max_elo_r_opp)


    return


elo_rating_user = db.execute("SELECT elo FROM elo_rating WHERE id = :user_id", user_id=session["id"])

elo_rating_opponent = db.execute("SELECT elo FROM elo_rating WHERE id = :opponent_id BETWEEN", opponent_id=opponent_id)


def expected(elo_rating_user, elo_rating_opponent):
    """
    Calculate expected score of A in a match against B
    :param A: Elo rating for player A
    :param B: Elo rating for player B
    """
    exp_score = 1 / (1 + 10 ** ((B - elo_rating_user) / 400))

    return exp_score


def elo(elo_rating_user, exp_score, score, k=32):
    """
    Calculate the new Elo rating for a player
    :param old: The previous Elo rating
    :param exp: The expected score for this match
    :param score: The actual score for this match
    :param k: The k-factor for Elo (default: 32)
    """
    new_elo_rating = elo_rating_user + k * (score - exp_score)

    return new_elo_rating

db.execute("UPDATE users SET elo_rating = new_elo_rating WHERE id = user_id", new_elo_rating, user_id=session["id"])