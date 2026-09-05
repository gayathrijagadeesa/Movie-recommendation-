"""
app.py
------
Flask web app exposing the movie recommender through a simple
search interface. Run with: python app.py
Then open http://127.0.0.1:5000
"""

from flask import Flask, render_template, request, jsonify
from recommender import MovieRecommender

app = Flask(__name__)
engine = MovieRecommender(data_path="data/movies.csv")


@app.route("/")
def home():
    return render_template("index.html", titles=sorted(engine.df["title"].tolist()))


@app.route("/recommend")
def recommend():
    title = request.args.get("title", "")
    results = engine.recommend(title, top_n=5)
    if results is None:
        return jsonify({"error": "Movie not found in dataset."}), 404
    return jsonify({"query": title, "results": results})


@app.route("/search")
def search():
    query = request.args.get("q", "")
    return jsonify(engine.search_titles(query))


if __name__ == "__main__":
    app.run(debug=True)
