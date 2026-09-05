# Movie Recommendation System

A content-based movie recommendation engine built with Python, Pandas, and
Scikit-learn. It applies TF-IDF vectorization and cosine similarity to match
a movie you like with other titles that share similar genres, cast,
director, and themes — then serves the results through a small Flask web
interface.

## How it works

1. Each movie's metadata (genres, keywords, cast, director) is combined into
   a single text "feature soup."
2. Scikit-learn's `TfidfVectorizer` turns that text into a weighted vector
   space, so common/uninformative words matter less and distinctive terms
   (a specific actor, a niche keyword) matter more.
3. Cosine similarity is computed between every pair of movies in that
   vector space.
4. Given a title, the app looks up its similarity scores against every
   other movie and returns the top N closest matches.

## Project structure

```
movie-recommender/
├── app.py              # Flask app + API routes
├── recommender.py       # Core recommendation engine (TF-IDF + cosine similarity)
├── data/
│   └── movies.csv        # Movie metadata dataset
├── templates/
│   └── index.html        # Search page
├── static/
│   ├── style.css
│   └── app.js
└── requirements.txt
```

## Running it locally

```bash
# 1. Clone the repo and move into it
git clone https://github.com/gayathrijagadeesa/movie-recommender.git
cd movie-recommender

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py

# 4. Open in your browser
http://127.0.0.1:5000
```

## Using it without the web interface

The recommender can also be run directly from the command line:

```bash
python recommender.py "Inception"
```

This prints the top 5 movies most similar to the given title, along with
their similarity scores.

## Tech stack

- **Python** — core language
- **Pandas** — data loading and cleaning
- **Scikit-learn** — TF-IDF vectorization and cosine similarity
- **Flask** — web app and API layer
- **HTML/CSS/JS** — search interface

## Possible extensions

- Swap the sample dataset for a larger real-world one (e.g. TMDB 5000
  Movies).
- Add collaborative filtering using user ratings, and blend it with the
  content-based scores.
- Add poster images via a movie metadata API.
- Deploy the Flask app (Render, Railway, or PythonAnywhere) for a live demo
  link.
