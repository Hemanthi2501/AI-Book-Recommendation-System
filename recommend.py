import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the dataset
books = pd.read_csv("data/books.csv").head(3000)

# Fill missing values
books["authors"] = books["authors"].fillna("")
books["title"] = books["title"].fillna("")
books["image_url"] = books["image_url"].fillna("")

# Create a combined feature
books["features"] = books["title"] + " " + books["authors"]

# Convert text into vectors
vectorizer = TfidfVectorizer(stop_words="english")
matrix = vectorizer.fit_transform(books["features"])

# Calculate similarity
similarity = cosine_similarity(matrix)


def recommend(book_title):

    # Try exact match (case-insensitive)
    matches = books[
        books["title"].str.lower() == book_title.lower()
    ]

    # If no exact match, try partial match
    if matches.empty:
        matches = books[
            books["title"].str.contains(book_title, case=False, na=False)
        ]

    # No book found
    if matches.empty:
        print("No match found for:", book_title)
        return []

    index = matches.index[0]

    # Find most similar books
    scores = list(enumerate(similarity[index]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    recommendations = []

    for i, score in scores[1:7]:

        recommendations.append({
            "title": books.iloc[i]["title"],
            "author": books.iloc[i]["authors"],
            "image": books.iloc[i]["image_url"]
        })

    print("Recommendations:", recommendations)

    return recommendations


if __name__ == "__main__":

    recs = recommend("Harry Potter")

    for book in recs:
        print(book)