from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from Recommender import Recommender
from Recommender import book_genres, movie_genres, podcast_genres


app = Flask(__name__)

categories = ['Book', 'Music', 'Movie', 'Podcast']
books_data = pd.read_csv('datasets/books_dataset.csv')
musics_data = pd.read_csv('datasets\musics_dataset.csv')
movies_data = pd.read_csv('datasets/movies_dataset.csv', encoding='ISO-8859-1')
podcasts_data = pd.read_json('datasets/podcast.json')


rec = Recommender(podcasts_data, musics_data, movies_data, books_data)


@app.route('/api/similar_items', methods=['POST'])
def get_similar_items():
    json_data = request.get_json()

    if not json_data or 'mediaType' not in json_data:
        return jsonify({'Error': 'Please provide a category.'}), 400
    
    category = json_data['mediaType']
    user_data = json_data['user_scores']

    if category not in categories:
        return jsonify({'Error': 'Invalid category.'}), 400
    

    if category == 'BOOK':
        favoriteBookGenres = np.zeros(len(book_genres))
        for i, genre in enumerate(book_genres):
            if genre in user_data['favoriteBookGenres']:
                favoriteBookGenres[i] = user_data['favoriteBookGenres'][genre]
        similar_items = rec.get_similar_books(favoriteBookGenres)
    elif category == 'MUSIC':
        favoriteMusicSingers = user_data['favoriteMusicSingers']
        similar_items = rec.get_similar_musics(list(favoriteMusicSingers.keys()))
    elif category == 'MOVIE':
        similar_items = rec.get_similar_movies(user_data)
    elif category == 'PODCAST':
        similar_items = rec.get_similar_podcasts(user_data)
    else:
        return jsonify({'Error': 'Invalid Category.'}), 400

    return jsonify({'Recommendation': similar_items, 'Category': category})

if __name__ == '__main__':
    print('Movies', rec.get_similar_movies({
        "favorite_actors": ["Leonardo DiCaprio", "Kate Winslet", "Tom Hanks"],
        "genres": np.random.uniform(0.0, 10.0, size=21)
        }))
    print('Podcasts', rec.get_similar_podcasts({
        "favorite_producers": ['RiotCast Network', 'BBC', 'VAULT Studios'],
        "genres": np.random.uniform(0.0, 10.0, size=20)
    }))
    app.run(debug=True)
