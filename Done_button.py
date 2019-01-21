from application import *
import pandas as pd

def check_complete(sudoku):
    get_sudoku()
    sol = solution()
    df = pd.read_html('looks.html')[0]
    df_list = df.values.tolist()

    if df_list == sol:
        return render_template("index.html")
    else:
        return ("You failed")