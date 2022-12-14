import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required
from helpers import apology

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

# Homepage displaying an interactive map of the Yale campus
@app.route("/")
def map():
    if request.method == "GET":
        return render_template("map.html")
    else:
        render_template("map.html")

# App routes to the six areas of campus
@app.route("/area-sh")
def sh():
    if request.method == "GET":
        place="Science Hill"
        buildings=db.execute("SELECT * FROM building WHERE location_id = 0")
        return render_template("area.html", place=place, buildings=buildings)

@app.route("/area-gym")
def gym():
    if request.method == "GET":
        place="Payne Whitney Area"
        buildings=db.execute("SELECT * FROM building WHERE location_id = 3")
        return render_template("area.html", place=place, buildings=buildings)

@app.route("/area-arts")
def arts():
    if request.method == "GET":
        place="Arts Area"
        buildings=db.execute("SELECT * FROM building WHERE location_id = 2")
        return render_template("area.html", place=place, buildings=buildings)

@app.route("/area-cc")
def cc():
    if request.method == "GET":
        place="Cross Campus"
        buildings=db.execute("SELECT * FROM building WHERE location_id = 4")
        return render_template("area.html", place=place, buildings=buildings)

@app.route("/area-oc")
def oc():
    if request.method == "GET":
        place="Old Campus"
        buildings=db.execute("SELECT * FROM building WHERE location_id = 6")
        return render_template("area.html", place=place, buildings=buildings)

@app.route("/area-hh")
def hh():
    if request.method == "GET":
        place="Hillhouse"
        buildings=db.execute("SELECT * FROM building WHERE location_id = 1")
        return render_template("area.html", place=place, buildings=buildings)

# App route to building page
@app.route("/building", methods = ["GET"])
def building():
    if request.method == "GET":
        buildings=db.execute("SELECT * FROM building WHERE abbreviation = ?", request.args.get("abbreviation"))
        return render_template("building.html", buildings=buildings)

# App route to page displaying all vending machines in a building
@app.route("/vend", methods = ["GET"])
def vend():
    if request.method == "GET":
        buildings=db.execute("SELECT * FROM building WHERE abbreviation = ?", request.args.get("abbreviation"))
        vendmachines=db.execute("SELECT * from amenities WHERE type = 'vending' AND building_id = ?", buildings[0]['id'])
        if len(vendmachines) == 0:
            return render_template("comingsoon.html", buildings=buildings)
        return render_template("vend.html", vendmachines=vendmachines, buildings=buildings)

# App route to page displaying all restrooms in a building
@app.route("/rest", methods = ["GET"])
def rest():
    if request.method == "GET":
        buildings=db.execute("SELECT * FROM building WHERE abbreviation = ?", request.args.get("abbreviation"))
        restrooms=db.execute("SELECT * from amenities WHERE type = 'bathroom' AND building_id = ?", buildings[0]['id'])
        if len(restrooms) == 0:
            return render_template("comingsoon.html", buildings=buildings)
        return render_template("rest.html", restrooms=restrooms, buildings=buildings)

# App route to page displaying all fountains in a building
@app.route("/fount", methods = ["GET"])
def fount():
    coldlist=[]
    if request.method == "GET":
        buildings=db.execute("SELECT * FROM building WHERE abbreviation = ?", request.args.get("abbreviation"))
        fountains=db.execute("SELECT * FROM amenities WHERE type = 'fountain' AND building_id = ?", buildings[0]['id'])
        for fountain in fountains:
            # Checks whether a review contains the word "cold" so that a snowflake icon will be displayed beside it in the table
            cold=db.execute("SELECT amenity_id FROM reviews WHERE text LIKE '%cold%' AND amenity_id = ?", fountain['id'])
            if len(cold) != 0:
                coldlist.append(cold[0]['amenity_id'])
        if len(fountains) == 0:
            return render_template("comingsoon.html", buildings=buildings)
        return render_template("fount.html", fountains=fountains, buildings=buildings, coldlist=coldlist)

# App route allowing the user to submit new amenities if they are logged in
@app.route("/submit", methods=["GET", "POST"])
@login_required
def submit():
    if request.method == "POST":
        build = request.form.get("building")
        type = request.form.get("type")
        floor = request.form.get("floor")
        gend = request.form.get("gender")
        bottle = request.form.get("bottle_refiller")
        name = request.form.get("name")
        build_id=db.execute("SELECT id FROM building WHERE name=?", build)[0]["id"]
        db.execute("INSERT INTO amenities (type, building_id, gender, floor, bottle_filler, name) VALUES (?, ?, ?, ?, ?, ?)", type, build_id, gend, floor, bottle, name)
        id=db.execute("SELECT id FROM amenities WHERE name=? AND building_id=? AND type=?", name, build_id, type)[0]["id"]
        reviews=db.execute("SELECT * FROM reviews WHERE amenity_id = ?", id)
        amenity=db.execute("SELECT * FROM amenities WHERE id=?", id)[0]
        return render_template("amenities.html", amenity=amenity, building=build, reviews=reviews)
    else:
        buildings = db.execute("SELECT * FROM building")
        return render_template("submit.html", buildings=buildings)

# App route allowing the user to search through a table displaying all the amenities
@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        if request.form.get("amen"):
            id=request.form.get("amen")
            amenity=db.execute("SELECT * FROM amenities WHERE id=?", id)
            build_id=db.execute("SELECT * FROM amenities WHERE id=?", id)[0]["building_id"]
            building=db.execute("SELECT name FROM building WHERE id=?", build_id)[0]["name"]
            reviews=db.execute("SELECT * FROM reviews WHERE amenity_id=?", id)
            amenity=db.execute("SELECT * FROM amenities WHERE id=?", id)[0]
            return render_template("amenities.html", amenity=amenity, building=building, reviews=reviews)
        else:
            type=request.form.get("type")
            floor=request.form.get("floor")
            rating=request.form.get("rating")
            gender=request.form.get("gender")
            bottle_filler=request.form.get("bottle_filler")
            vend_type=request.form.get("vend_type")
            building_id=request.form.get("building")
            
            counter=0
            for i in range(0,7):
                categories=["type", "floor", "rating", "gender", "bottle_filler", "vend_type", "building_id"]
                values=[type, floor, rating, gender, bottle_filler, vend_type, building_id]
                if values[i] == 'any':
                    counter=counter+1
            if counter == 7:
                amenities=db.execute("SELECT * FROM amenities")
                buildings=db.execute("SELECT * FROM building")
                return render_template("search.html", amenities=amenities, buildings=buildings)
            
            check="SELECT * FROM amenities WHERE"
            greaterorequals=">="
            for i in range(0,7):
                equals="="
                categories=["type", "floor", "avg_rev", "gender", "bottle_filler", "vend_type", "building_id"]
                values=[type, floor, rating, gender, bottle_filler, vend_type, building_id]
                if values[i] != 'any':
                    check=check+" "
                    check=check+categories[i]
                    if categories[i] == "avg_rev":
                        check=check+greaterorequals
                    else:
                        check=check+equals
                    if categories[i] == "avg_rev" or categories[i] == "floor" or categories[i] == "building_id":
                        check=check+values[i]
                    else:
                        check=check+"'"
                        check=check+values[i]
                        check=check+"'"
                    if i!=6:
                        if values[i+1] != 'any':
                            check=check+" "
                            check=check+"AND"
                            check=check+" "
            amenities=db.execute(check)
            buildings=db.execute("SELECT * FROM building")
            return render_template("search.html", amenities=amenities, buildings=buildings)
    else:
        amenities=db.execute("SELECT * FROM amenities")
        buildings=db.execute("SELECT * FROM building")
        return render_template("search.html", amenities=amenities, buildings=buildings)

# App route allowing the user to write reviews about amenities if they are logged in
@app.route("/review", methods=["GET", "POST"])
@login_required
def review():
    if request.method == "POST":
        review=request.form.get("review")
        rating=request.form.get("rating")
        id=request.form.get("amen")
        db.execute("INSERT INTO reviews (amenity_id, text, rating) VALUES (?, ?, ?)", id, review, rating)
        amenity=db.execute("SELECT * FROM amenities WHERE id=?", id)
        build_id=db.execute("SELECT * FROM amenities WHERE id=?", id)[0]["building_id"]
        building=db.execute("SELECT name FROM building WHERE id=?", build_id)[0]["name"]
        reviews=db.execute("SELECT * FROM reviews WHERE amenity_id = ?", id)
        c = 0
        s = 0
        for review in reviews:
            c = c + 1
            s = s + review["rating"]
        if c > 0:
            avg=(s/c)
        else:
            avg="N/A"
        db.execute("UPDATE amenities SET avg_rev=? WHERE id=?", avg, id)
        amenity=db.execute("SELECT * FROM amenities WHERE id=?", id)[0]
        return render_template("amenities.html", building=building, amenity=amenity, reviews=reviews)
    else:
        amenities=db.execute("SELECT * FROM amenities")
        buildings=db.execute("SELECT * FROM building")
        return render_template("review.html", amenities=amenities, buildings=buildings)


@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 403)

        # Ensure password confirmation was submitted
        if not request.form.get("confirmation"):
            return apology("must provide password confirmation", 403)

        # Query database checking for whether username is already taken
        if db.execute("SELECT username FROM users WHERE username =?", request.form.get("username")):
            return apology("Username already taken", 403)

        # Check if password and confirmation match
        password = request.form.get("password")
        confirmation = request.form.get("confirmation", 403)
        if password != confirmation:
            return apology("Passwords do not match", 403)

        hash = generate_password_hash(password)

        # Insert information into the database
        username = request.form.get("username")
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)

        # Set session to be id of user
        id = db.execute("SELECT id FROM users WHERE username IS ?", request.form.get("username"))
        session["user_id"] = id[0]["id"]

        return redirect("/")

    else:
        return render_template("register.html")

# SOURCES: https://www.w3schools.com/python/python_lists_add.asp, https://www.w3schools.com/sql/sql_insert.asp
# We used code from finance for Log In, Register, Logout, and Apology.