from flask import Flask, render_template, request, redirect, url_for
from models import db, User, Book, Wishlist
from recommend import recommend

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


# ---------------- HOME ---------------- #

@app.route("/")
def home():
    return render_template("index.htm")


# ---------------- LOGIN ---------------- #

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(
            email=email,
            password=password
        ).first()

        if user:
            return redirect(url_for("dashboard"))
        else:
            return "Invalid Email or Password"

    return render_template("login.htm")


# ---------------- SIGNUP ---------------- #

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        user = User(
            name=name,
            email=email,
            password=password
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("signup.htm")


# ---------------- DASHBOARD ---------------- #

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.htm")


# ---------------- SEARCH ---------------- #

@app.route("/search")
def search():

    query = request.args.get("query")

    if query:
        books = Book.query.filter(
            Book.title.ilike(f"%{query}%")
        ).all()
    else:
        books = Book.query.limit(20).all()

    return render_template(
        "search.htm",
        books=books,
        query=query
    )


# ---------------- BOOK DETAILS ---------------- #

@app.route("/book-details/<int:book_id>")
def book_details(book_id):

    book = Book.query.get_or_404(book_id)

    return render_template(
        "book-details.htm",
        book=book
    )


# ---------------- AI RECOMMENDATIONS ---------------- #

@app.route("/recommendation/<book_title>")
def recommendation(book_title):

    books = recommend(book_title)

    print("Book title:", book_title)
    print("Recommendations:", books)

    return render_template(
        "recommendation.htm",
        books=books,
        title=book_title
    )


# ---------------- ADD TO WISHLIST ---------------- #

@app.route("/add_wishlist/<int:book_id>")
def add_wishlist(book_id):

    book = Book.query.get_or_404(book_id)

    wishlist = Wishlist(
        title=book.title,
        author=book.author,
        genre=book.genre,
        image=book.image
    )

    db.session.add(wishlist)
    db.session.commit()

    return redirect(url_for("wishlist"))


# ---------------- WISHLIST ---------------- #

@app.route("/wishlist")
def wishlist():

    books = Wishlist.query.all()

    return render_template(
        "wishlist.htm",
        books=books
    )


# ---------------- PROFILE ---------------- #

@app.route("/profile")
def profile():
    return render_template("profile.htm")


# ---------------- RUN APP ---------------- #

if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)