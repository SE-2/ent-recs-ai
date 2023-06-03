from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from Recommender import Recommender
from Recommender import book_genres, movie_genres, podcast_genres


app = Flask(__name__)

categories = ['BOOK', 'MUSIC', 'MOVIE', 'PODCAST']
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

    if category not in categories:
        return jsonify({'Error': 'Invalid category.'}), 400
    

    if category == 'BOOK':
        favoriteBookGenres = np.zeros(len(book_genres))
        for i, genre in enumerate(book_genres):
            if genre in json_data['favoriteBookGenres']:
                favoriteBookGenres[i] = json_data['favoriteBookGenres'][genre]
        similar_items = rec.get_similar_books(favoriteBookGenres)

    elif category == 'MUSIC':
        favoriteMusicSingers = json_data['favoriteMusicSingers']
        similar_items = rec.get_similar_musics(list(favoriteMusicSingers.keys()))

    elif category == 'MOVIE':
        favoriteMovieActors = json_data['favoriteMovieActors']

        favoriteMovieGenres = np.zeros(len(movie_genres))
        for i, genre in enumerate(movie_genres):
            if genre in json_data['favoriteMovieGenres']:
                favoriteMovieGenres[i] = json_data['favoriteMovieGenres'][genre]

        similar_items = rec.get_similar_movies(list(favoriteMovieActors.keys()), favoriteMovieGenres)

    elif category == 'PODCAST':
        favoritePodcastProducers = json_data['favoritePodcastProducers']

        favoritePodcastGenres = np.zeros(len(podcast_genres))
        for i, genre in enumerate(podcast_genres):
            if genre in json_data['favoritePodcastGenres']:
                favoritePodcastGenres[i] = json_data['favoritePodcastGenres'][genre]

        similar_items = rec.get_similar_podcasts(list(favoritePodcastProducers.keys()), favoritePodcastGenres)
    else:
        return jsonify({'Error': 'Invalid Category.'}), 400

    print(similar_items)
    return similar_items

if __name__ == '__main__':
    app.run(debug=True)
