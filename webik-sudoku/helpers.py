import csv
import urllib.request
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
import json
from random import randint
from flask import redirect, render_template, request, session
from functools import wraps


db = SQL("sqlite:///sudokus.db")


def apology(message, code=400):
    """Renders message as an apology to user."""
    def escape(s):
        # Escape special characters
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def friendadded(message, code=200):
    """Renders message when friend is added succesfully."""
    def escape(s):
        # Escape special characters
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("friendadded.html", top=code, bottom=escape(message)), code


def login_required(f):
    """Decorate routes to require login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def random_number():
    """Generates random number between 2 and 1000 for the sudoku database."""
    ran = randint(2, 1000)
    return ran


def solution(ran, lev):
    """Generates the solutions for sudokus."""
    # Select solution from database
    solution = db.execute("SELECT solution FROM generated_sudokus WHERE id=:id AND level=:level", id=ran, level=lev)
    # Convert solution to a 2d list to work with
    for x in solution:
        for y in x.values():
            sol = y

    lst = [s for s in sol]
    repl = [w.replace('.', ' ') for w in lst]
    answer = [repl[i:i+9] for i in range(0, len(repl), 9)]

    return answer


def get_data():
    """Get the filled in data from user that filled in sudoku in singleplayer."""

    sol = solution(session["random_number"], session["level"])

    # Generates a 2d list of the filled in data
    new_list = [[0 for x in range(9)] for y in range(9)]
    for x in range(9):
        for y in range(9):
            get_data = request.form.get(str(x) + " - " + str(y))
            new_list[x][y] = get_data

            if new_list[x][y] == None:
                new_list[x][y] = sol[x][y]
    return new_list


def mp_get_data():
    """Returns the filled in data from user that filled in sudoku in multiplayer."""

    sol = solution(session["random_number"], session["level_mul"])

    # Generates a 2d list of the filled in data
    new_list = [[0 for x in range(9)] for y in range(9)]
    for x in range(9):
        for y in range(9):
            get_data = request.form.get(str(x) + " - " + str(y))
            new_list[x][y] = get_data

            if new_list[x][y] == None:
                new_list[x][y] = sol[x][y]
    return new_list


def points(sudoku_list):
    """Returns the points earned by the user in singleplayer."""
    sol = solution(session["random_number"], session["level"])
    data = get_data()
    # Standard score is 81, due to negative scores retrieved when score would start at 0
    score = 81
    # Check if filled in data from user is correct
    if data == sol:
        score += 100
        for x in data:
            if " " in x:
                break
            else:
                score += (sec_left//10)
    # Else if user solution is not correct, calculate points based on filled in cells
    else:
        index = -1
        index2 = -1
        for lst in data:
            index += 1
            index2 += 1
            for number in lst:
                # print(number)
                if number == '':
                    score -= 1
                elif number in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                    if sudoku_list[index][index2] != data[index][index2] and data[index][index2] != " ":
                        if data[index][index2] == sol[index][index2]:
                            score += 1
                        else:
                            score -= 1
                    else:
                        score += 0
    return score


def mp_points(sudoku_list):
    """Returns the points earned by the user in multiplayer."""
    sol = solution(session["random_number"], session["level_mul"])
    data = mp_get_data()
    # Standard score is 81, due to negative scores retrieved when score would start at 0
    score = 81
    # Check if filled in data from user is correct
    if data == sol:
        score += 100
        for x in data:
            if " " in x:
                break
            else:
                score += (sec_left//10)
    # Else if user solution is not correct, calculate points based on filled in cells
    else:
        index = -1
        index2 = -1
        for lst in data:
            index += 1
            index2 += 1
            for number in lst:
                # print(number)
                if number == '':
                    score -= 1
                elif number in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                    if sudoku_list[index][index2] != data[index][index2] and data[index][index2] != '':
                        if data[index][index2] == sol[index][index2]:
                            score += 1
                        else:
                            score -= 1
                    else:
                        score += 0
    return score
