from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import ast

def get_similar_books(user_scores):
    IDs = np.random.randint(0, 91, size=20)
    return IDs


def get_similar_musics(user_scores):
    IDs = np.random.randint(0, 91, size=20)
    return IDs


def get_similar_movies(user_scores):
    IDs = np.random.randint(0, 91, size=20)
    return IDs


def get_similar_podcasts(user_scores):
    IDs = np.random.randint(0, 91, size=20)
    return IDs


app = Flask(__name__)

DATASET_LINKS = []
books_data = pd.read_csv('datasets\collaborative_book_metadata.csv')
# Unique Book generes (10)
# 'young-adult'
# 'poetry'
# 'fantasy, paranormal'
# 'non-fiction'
# 'mystery, thriller, crime'
# 'children'
# 'romance'
# 'comics, graphic'
# 'history, historical fiction, biography'
# 'fiction'
# ------------------------------------------------------
# Code for extracting unique genres via set
# setofgenres = []
# for i in books_data.values:
#     my_list = ast.literal_eval(i[8])
#     print(my_list)
#     for gnr in my_list:
#         setofgenres.append(gnr)

# print(len(setofgenres))
# print(len(set(setofgenres)))
# print(set(setofgenres))
# ------------------------------------------------------

music_data = pd.read_csv('datasets\Spotify_Youtube.csv')
movies_data = pd.read_csv('datasets\imdb_top_1000.csv')
podcasts_data = pd.read_json('datasets/podcast.json')

categories = ['Book', 'Music', 'Movie', 'Podcast']

@app.route('/api/similar_items', methods=['POST'])
def get_similar_items():
    json_data = request.get_json()

    if not json_data or 'category' not in json_data:
        return jsonify({'Error': 'Please provide a category.'}), 400
    
    category = json_data['category']
    user_scores = json_data['user_scores']

    if category not in categories:
        return jsonify({'Error': 'Invalid category.'}), 400
    
    try:
        user_scores = [float(score) for score in user_scores]
        if not all(0 <= score <= 10 for score in user_scores):
            raise ValueError
    except ValueError:
        return jsonify({'Error': 'Invalid user scores.'}), 400

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

    return jsonify({'Recommendation': similar_items, 'Category': json_data['category']})

if __name__ == '__main__':
    app.run(debug=True)
