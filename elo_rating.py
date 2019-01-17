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


elo_rating_user = db.execute("SELECT elo_score FROM elo_score_history WHERE id = :user_id", user_id=session["user_id"])

elo_rating_opponent = db.execute("SELECT elo_score FROM elo_score_history WHERE id = :user_id", opponent_id=re)


def random_select():
    """
    selects a random user
    with a reasonable elo score to play against
    """
    elo_rating_user = db.execute("SELECT elo_score FROM elo_score_history WHERE id = :user_id", user_id=session["user_id"])

    min_elo_r_opp = elo_rating_user - 40
    max_elo_r_opp = elo_rating_user + 40

    # SELECT * FROM Products
    # WHERE Price NOT BETWEEN 10 AND 20;
    opponent_id = db.execute("SELECT user_id FROM elo_score_history WHERE elo_score BETWEEN min_elo_r_opp AND max_elo_r_opp")

    elo_rating_opponent = db.execute("SELECT elo_score FROM elo_score_history WHERE id = :opponent_id BETWEEN", opponent_id=opponent_id)
    return


def expected(elo_rating_user, B):
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