"""
recommender.py
----------------
Core content-based movie recommendation engine.

Builds a TF-IDF vector space over each movie's combined metadata
(genres, keywords, cast, director) and ranks other movies by
cosine similarity to a given title.
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class MovieRecommender:
    def __init__(self, data_path: str = "data/movies.csv"):
        self.data_path = data_path
        self.df = None
        self.tfidf_matrix = None
        self.similarity_matrix = None
        self.title_to_index = {}
        self._load_and_build()

    def _load_and_build(self):
        """Load the dataset, clean it, and build the TF-IDF + similarity matrix."""
        df = pd.read_csv(self.data_path)

        # Basic cleaning: fill missing metadata so vectorization doesn't break
        for col in ["genres", "keywords", "cast", "director", "overview"]:
            df[col] = df[col].fillna("")

        # Feature engineering: combine genre, cast, keywords, director into
        # a single "soup" of text per movie. This is what TF-IDF vectorizes.
        df["combined_features"] = (
            df["genres"] + " " +
            df["keywords"] + " " +
            df["cast"] + " " +
            df["director"] + " " +
            df["director"]  # weight director a bit more, it's a strong signal
        )

        self.df = df.reset_index(drop=True)
        self.title_to_index = {
            title.lower(): idx for idx, title in enumerate(self.df["title"])
        }

        vectorizer = TfidfVectorizer(stop_words="english")
        self.tfidf_matrix = vectorizer.fit_transform(self.df["combined_features"])
        self.similarity_matrix = cosine_similarity(self.tfidf_matrix)

    def search_titles(self, query: str, limit: int = 8):
        """Return titles that contain the query string (for autocomplete/search)."""
        query = query.lower().strip()
        if not query:
            return []
        matches = self.df[self.df["title"].str.lower().str.contains(query)]
        return matches["title"].tolist()[:limit]

    def recommend(self, title: str, top_n: int = 5):
        """
        Return the top_n movies most similar to `title`, based on
        cosine similarity over the TF-IDF feature space.
        """
        key = title.lower().strip()
        if key not in self.title_to_index:
            return None  # caller should handle "movie not found"

        idx = self.title_to_index[key]
        scores = list(enumerate(self.similarity_matrix[idx]))

        # Sort by similarity score, descending, excluding the movie itself
        scores = sorted(scores, key=lambda x: x[1], reverse=True)
        scores = [s for s in scores if s[0] != idx][:top_n]

        results = []
        for movie_idx, score in scores:
            row = self.df.iloc[movie_idx]
            results.append({
                "title": row["title"],
                "genres": row["genres"],
                "overview": row["overview"],
                "score": round(float(score), 3),
            })
        return results


if __name__ == "__main__":
    # Quick manual test from the command line:
    # python recommender.py "Inception"
    import sys

    engine = MovieRecommender()
    query = sys.argv[1] if len(sys.argv) > 1 else "Inception"

    print(f"\nTop recommendations for '{query}':\n")
    recs = engine.recommend(query, top_n=5)
    if recs is None:
        print("Movie not found in dataset.")
    else:
        for i, r in enumerate(recs, 1):
            print(f"{i}. {r['title']}  (similarity: {r['score']})")
            print(f"   Genres: {r['genres']}")
            print(f"   {r['overview']}\n")
