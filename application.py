import os
import json
import requests

from flask import Flask, session, redirect, render_template, request
from flask import flash, jsonify, url_for
from functools import wraps
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine('postgresql://localhost/postgres')
db = scoped_session(sessionmaker(bind=engine))


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


@app.route("/", methods=['POST', 'GET'])
@login_required
def index():
    """Homepage."""
    return render_template("index.html")


@app.route("/register", methods=['POST', 'GET'])
def register():
    """Registration page."""
    session.clear()

    if request.method == 'POST':
        # Ensure password confirmation matches submitted password
        if not request.form["password"] == request.form["confirmation"]:
            flash(u"Password and confirmation don't match!", "danger")
            return render_template("register.html")

        hashed = generate_password_hash(request.form.get("password"))

        # Check whether user exists
        user = get_user(request.form.get("username"))

        # Insert new user into database
        if user is None:
            db.execute("INSERT INTO users (username, hash) \
                        VALUES (:username, :password)",
                       {"username": request.form.get("username"),
                        "password": hashed})
            db.commit()

            flash("You have successfully registered!", "success")
            return render_template("login.html")

        else:
            flash("This username is already in use!", "danger")
            return render_template("register.html")

    else:
        return render_template("register.html")


@app.route("/login", methods=['POST', 'GET'])
def login():
    """ Log in."""
    session.clear()

    if request.method == 'POST':
        # Check whether user exists
        user = get_user(request.form.get("username"))
        if user is None:
            flash("No such username!", "danger")
            return render_template("login.html")

        # Check password
        if not check_password_hash(user["hash"], request.form.get("password")):
            flash("Password and username don't match!", "danger")
            return render_template("login.html")

        # Store current user in session
        session["user_id"] = user["id"]
        session["username"] = user["username"]

        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/query", methods=['POST'])
@login_required
def query():
    """Search books by ISBN, title or author, including partial match."""
    search = request.form["query"]

    # Database query for partial match across several columns
    results = db.execute("SELECT * FROM books WHERE \
                          isbn ILIKE :query OR \
                          title ILIKE :query OR \
                          author ILIKE :query",
                         {"query": '%' + search + '%'}).fetchall()

    if results:
        return render_template("query.html", results=results)

    else:
        flash("Your quest didn't yield any results!", "danger")
        return render_template("index.html")


@app.route("/book/<isbn>", methods=['POST', 'GET'])
@login_required
def book(isbn):
    """Book page."""
    key = os.getenv("GOODREADS_KEY")

    selected = get_book(isbn)
    reviews = get_reviews(selected["id"])

    # Fetch data via Goodreads API
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": key, "isbns": isbn})

    if res.status_code != 200:
        raise Exception("Error! Goodreads API Access Failed!")
    data = res.json()

    return render_template("bookpage.html", book=selected, reviews=reviews, data=data)


@app.route("/review", methods=['POST', 'GET'])
@login_required
def review():
    """Review submission."""
    if request.method == 'POST':
        # Data submitted via the html form fields
        isbn = request.form.get("isbn")
        rating = request.form.get("rating")
        title = request.form.get("title")
        text = request.form.get("text")
        user = get_user(session["username"])

        # Fetch book and available reviews from database
        selected = get_book(isbn)
        reviews = get_reviews(selected["id"])

        # Ensure that there is only one review per user
        for r in reviews:
            if r.by_user == user["username"]:
                # Update previously submitted review
                db.execute("UPDATE reviews SET book_id = :book_id, \
                            rating = :rating, \
                            review_title = :review_title, \
                            review_text = :review_text \
                            WHERE by_user = :by_user",
                           {"book_id": selected["id"],
                            "rating": rating,
                            "review_title": title,
                            "review_text": text,
                            "by_user": user["id"]})
                db.commit()

                flash("Your review for this book has been updated!", "success")
                return redirect(url_for("book", isbn=isbn))

        # Insert review into database
        db.execute("INSERT INTO reviews \
                    (book_id, by_user, rating, review_title, review_text) \
                    VALUES \
                    (:book_id, :by_user, :rating, :review_title, :review_text)",
                   {"book_id": selected["id"],
                    "by_user": user["id"],
                    "rating": rating,
                    "review_title": title,
                    "review_text": text})
        db.commit()

        flash("You have successfully submitted your review!", "success")
        return redirect(url_for("book", isbn=isbn))

    else:
        return redirect("/query")


@app.route("/api/<isbn>", methods=['GET'])
@login_required
def isbn_api(isbn):
    """Return details about a single book by isbn."""

    # Database query to check if book exists
    selected = db.execute("SELECT books.*, COUNT (reviews.id) AS review_count, \
                          AVG (rating) AS average_score \
                          FROM books \
                          LEFT OUTER JOIN reviews \
                          ON reviews.book_id=books.id \
                          WHERE isbn = :isbn\
                          GROUP BY books.id",
                          {"isbn": isbn}).fetchone()

    if selected is None:
        return page_not_found(404)

    return jsonify({
        "title": selected.title,
        "author": selected.author,
        "year": selected.year,
        "isbn": selected.isbn,
        "review_count": selected.review_count,
        "average_score": round(float(selected.average_score), 1)
    })


@app.route("/userpage", methods=['POST', 'GET'])
@login_required
def userpage():
    user = get_user(session["username"])
    """Query that contains all book reviews by the user."""
    results = db.execute("SELECT reviews.*, books.* \
                          FROM reviews \
                          LEFT JOIN books \
                          ON books.id = reviews.book_id \
                          WHERE reviews.by_user = :by_user\
                          GROUP BY reviews.id, books.id",
                         {"by_user": user["id"]}).fetchall()

    """Change password."""
    if request.method == 'POST':
        # Check in entered old password is correct
        if not check_password_hash(user["hash"], request.form.get("old_password")):
            flash(u"Wrong old password!", "danger")
            return render_template("userpage.html", results=results)

        # Ensure that new password and confirmation match
        if not request.form.get("new_password") == request.form.get("confirmation"):
            flash(u"Password and confirmation don't match!", "danger")
            return render_template("userpage.html", results=results)

        new_hash = generate_password_hash(request.form.get("new_password"))

        # Update database
        db.execute("UPDATE users SET hash = :hash WHERE id = :id",
                   {"hash": new_hash,
                    "id": user["id"]})
        db.commit()

        flash(u"You have successfully changed your password!", "success")
        return render_template("userpage.html", results=results)

    else:
        return render_template("userpage.html", results=results)


@app.route("/logout", methods=['POST', 'GET'])
@login_required
def logout():
    """Log out."""
    session.clear()
    return redirect("/")


@app.errorhandler(404)
def page_not_found(e):
    """Error handler."""
    return f"<h1>{e}</h1><p>The resource could not be found.</p>"


def get_book(isbn):
    """Query to fetch book from database by its isbn."""
    selected = db.execute("SELECT * FROM books WHERE isbn = :isbn",
                          {"isbn": isbn}).fetchone()
    return selected


def get_reviews(book_id):
    """Query to fetch saved reviews from the database."""
    reviews = db.execute("SELECT * FROM reviews WHERE book_id=:book_id \
                         ORDER BY id DESC",
                         {"book_id": book_id}).fetchall()
    return reviews


def get_user(username):
    """Query to check if user is stored in the database."""
    user = db.execute("SELECT * FROM users WHERE username = :username",
                      {"username": username}).fetchone()
    return user

if __name__ == "__main__":
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)