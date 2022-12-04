import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///amenities.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def map():
    """Show map of Yale"""
    if request.method == "GET":
        return render_template("map.html")
    else:
        render_template("map.html")
# Check that this keeps users logged in

@app.route("/sciencehill")
def sciencehill():
    if request.method == "GET":
        return render_template("sciencehill.html")

@app.route("/kroonhall")
def kroonhall():
    if request.method == "GET":
        return render_template("kroonhall.html")

@app.route("/kroonvend")
def kroonvend():
    if request.method == "GET":
        return render_template("kroonvend.html")

@app.route("/kroonrest")
def kroonrest():
    kroonrestrooms = db.execute("SELECT floor, gender, rating FROM restrooms WHERE building_id = 14")
    return render_template("kroonrest.html", kroonrestrooms=kroonrestrooms)


@app.route("/kroonwater")
def kroonwater():
    if request.method == "GET":
        return render_template("/areas/sciencehill/kroonhall/kroonwater.html")

# @app.route("/review", methods=["GET", "POST"])
# @login_required
# def review():
#     """review shares of stock"""
#     # Check is method is post
#     if request.method == "POST":

#         # Check whether inputted a symbol
#         if not request.form.get("symbol"):
#             return apology("Must input a symbol")

#         # Check if input shares
#         if not request.form.get("shares"):
#             return apology("Must input amount of shares")

#         # Check if integer
#         if not (request.form.get("shares").isdigit()):
#             return apology("Input an integer")

#         else:
#             shares = int(request.form.get("shares"))

#         # make sure handles fractional, negative, and non-numeric shares
#         if shares < 1:
#             return apology("Shares must be positive")

#             # Check if valid share inputted
#             if not stock:
#                 return apology("Invalid stock symbol")

#             cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
#             price = stock["price"]
#             total = price * shares

#             if int(cash) < int(total):
#                 return apology("You do not have enough money")

#             updated = cash - total
#             db.execute("UPDATE users SET cash = ? WHERE id = ?", updated, session["user_id"])
#             db.execute("INSERT INTO transactions (symbol, name, shares, price, total, user_id) VALUES (?, ?, ?, ?, ?, ?)",
#                        symbol, stock["name"], shares, price, total, session["user_id"])
#             return redirect("/")

#         return apology("Invalid symbol")

#     else:
#         return render_template("review.html")


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     """Log user in"""

#     # Forget any user_id
#     session.clear()

#     # User reached route via POST (as by submitting a form via POST)
#     if request.method == "POST":

#         # Ensure username was submitted
#         if not request.form.get("username"):
#             return apology("must provide username", 403)

#         # Ensure password was submitted
#         elif not request.form.get("password"):
#             return apology("must provide password", 403)

#         # Query database for username
#         rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

#         # Ensure username exists and password is correct
#         if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
#             return apology("invalid username and/or password", 403)

#         # Remember which user has logged in
#         session["user_id"] = rows[0]["id"]

#         # Redirect user to home page
#         return redirect("/")

#     # User reached route via GET (as by clicking a link or via redirect)
#     else:
#         return render_template("login.html")


# @app.route("/logout")
# def logout():
#     """Log user out"""

#     # Forget any user_id
#     session.clear()

#     # Redirect user to login form
#     return redirect("/")


# @app.route("/search", methods=["GET", "POST"])
# def search():
#     """Get stock search."""
#     # Check is method is post
#     if request.method == "POST":

#         # check if user gives symbol
#         if not request.form.get("symbol"):
#             return apology("No symbol provided")

#         # return stock price
#         symbol = request.form.get("symbol")

#         # if not stock then return apology
#         if not stock:
#             return apology("Stock does not exist")

#         company = stock["name"]
#         price = stock["price"]

#         # render the searchd.html template and list variables
#         return render_template("show.html", company=company, price=price, symbol=symbol)

#     # return the user to search page
#     else:
#         return render_template("search.html")


# @app.route("/register", methods=["GET", "POST"])
# def register():
#     """Register user"""
#     if request.method == "POST":

#         # Ensure username was submitted
#         if not request.form.get("username"):
#             return apology("must provide username")

#         # Ensure password was submitted
#         if not request.form.get("password"):
#             return apology("must provide password")

#         # Ensure password confirmation was submitted
#         if not request.form.get("confirmation"):
#             return apology("must provide password confirmation")

#         # Query database checking for whether username is already taken
#         if db.execute("SELECT username FROM users WHERE username =?", request.form.get("username")):
#             return apology("Username already taken")

#         # Check if password and confirmation match
#         password = request.form.get("password")
#         confirmation = request.form.get("confirmation")
#         if password != confirmation:
#             return apology("Passwords do not match")

#         hash = generate_password_hash(password)

#         # Insert information into the database
#         username = request.form.get("username")
#         db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)

#         # Set session to be id of user
#         id = db.execute("SELECT id FROM users WHERE username IS ?", request.form.get("username"))
#         session["user_id"] = id[0]["id"]

#         return redirect("/")

#     else:
#         return render_template("register.html")


