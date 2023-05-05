from flask import Flask, request, jsonify
import pandas as pd
from sklearn.neighbors import NearestNeighbors


def get_similar_books(user_scores):
    pass


def get_similar_musics(user_scores):
    pass


def get_similar_movies(user_scores):
    pass


def get_similar_podcasts(user_scores):
    pass


app = Flask(__name__)

DATASET_LINKS = []
books_data = pd.read_csv('books.csv')
music_data = pd.read_csv('music.csv')
movies_data = pd.read_csv('movies.csv')
podcasts_data = pd.read_csv('podcasts.csv')


categories = ['Book', 'Music', 'Movie', 'podcast']

@app.route('/api/similar_items', methods=['POST'])
def get_similar_items():
    json_data = request.get_json()

    if not json_data or 'category' not in json_data:
        return jsonify({'Error': 'Please provide a category.'}), 400
    
    category = json_data['category']
    user_scores = json_data['user_scores']

    if category not in categories:
        return jsonify({'Error': 'Invalid category.'}), 400

    if json_data['category'] == 'Book':
        similar_items = get_similar_books(user_scores)
    elif json_data['category'] == 'Music':
        similar_items = get_similar_musics(user_scores)
    elif json_data['category'] == 'Movie':
        similar_items = get_similar_movies(user_scores)
    elif json_data['category'] == 'Podcast':
        similar_items = get_similar_podcasts(user_scores)
    else:
        return jsonify({'Error': 'Invalid Category.'}), 400

    return jsonify({'Recommendation': similar_items})

if __name__ == '__main__':
    app.run(debug=True)
