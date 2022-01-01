import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    user_id = session["user_id"]
    stocks = db.execute("SELECT symbol, name, price, SUM(shares) as totalShares FROM buy WHERE user_id = ? GROUP BY symbol", user_id)
    cash = db.execute("SELECT cash FROM users WHERE id =  ?", user_id)[0]["cash"]

    total = cash

    for stock in stocks:
        total += stock["price"] * stock["totalShares"]

    return render_template("index.html", stock=stocks, cash=cash, usd=usd, total=total)



@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():

    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        item = lookup(symbol)



        if not symbol:
            return apology("Please insert stock name")

        elif item is None:
            return apology("symbol does not exist")

        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("shares must be an integer")

        if shares <= 0:
            return apology("please enter a postive value")



        user_id = session["user_id"]
        cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

        item_name = item["name"]
        item_price = item["price"]
        total_price = item_price * shares

        if cash < total_price:
            return apology("not enough cash")

        else:
            db.execute("UPDATE users SET cash = ? WHERE id = ?", cash - total_price, user_id)
            db.execute("INSERT INTO buy(user_id, name, shares, price, type, symbol) VALUES (?, ?, ?, ?, ?, ?)", user_id, item_name, shares, item_price, 'buy', symbol)

        return redirect("/")

    else:
        return render_template("buy.html")




    """Buy shares of stock"""
    #return apology("TODO")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    transactions = db.execute("SELECT type, symbol, price, shares, time FROM buy WHERE user_id = ? ", user_id)
    
    return render_template("history.html", transactions=transactions)
    
    return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""


    if request.method =="POST":
        name = request.form.get("symbol")
        if not name:
            return apology ("please enter a valid symbol")

        symbol  =  request.form.get("symbol")
        item = lookup(symbol)

        if not symbol:
            return apology ("please enter a valid symbol")
            
        if not item:
            return apology ("please enter a valid symbol")

        return render_template("quoted.html", symbol=item, usd=usd)
        
        
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        row = db.execute("SELECT * FROM users")
        name = request.form.get("username")


        if not name:
            return apology("Please input a username")


        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        
        if not password:
            return apology("Please input a password")
        if password != confirmation:
            return apology("password do not match")

        else:

            password = generate_password_hash(password)

        try:
            db.execute("INSERT INTO users (username, hash) VALUES(?,?)", name, password)
            return redirect("/")

        except:
            return apology("Username has already been registered")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":
        user_id = session["user_id"]
        shares = request.form.get("shares")
        symbol = request.form.get("symbol")
        non = request.form.get("non")


        if symbol == non:
            return apology ("input a valid symbol")

        if not shares:
            return apology ("input some shares")
        
        shares = int(request.form.get("shares"))
        
        if shares <= 0:
            return apology ("shares must be positive")

        item_price = lookup(symbol)["price"]
        item_name = lookup(symbol)["name"]
        price = shares * item_price

        shares_owned = db.execute("SELECT shares FROM buy WHERE user_id = ? AND symbol = ? GROUP BY symbol", user_id, symbol)[0]["shares"]

        if shares_owned < shares:
            return apology ("you dont have enough shares")

        current_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
        db.execute("UPDATE users SET cash = ? WHERE id = ?", current_cash + price, user_id)
        db.execute("INSERT INTO buy (user_id, name, shares, price, type, symbol) VALUES (?, ?, ?, ?, ?, ?)", user_id, item_name, -shares, item_price, "sell", symbol)


        return redirect('/')

    else:
        user_id = session["user_id"]
        symbols = db.execute("SELECT symbol FROM buy WHERE user_id = ? GROUP BY symbol", user_id)
        return render_template("sell.html", symbols=symbols)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

