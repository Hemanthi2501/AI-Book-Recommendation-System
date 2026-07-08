import pandas as pd

from app import app
from models import db, Book

# Read CSV
books = pd.read_csv("data/books.csv")

with app.app_context():

    # Remove old books
    Book.query.delete()
    db.session.commit()

    for _, row in books.iterrows():

        book = Book(
            title=row["title"],
            author=row["authors"],
            image=row["image_url"],
            description="No description available.",
            genre="General"
        )

        db.session.add(book)

    db.session.commit()

    print("Books imported successfully!")
    print("Total books:", Book.query.count())