from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from Recommender import Recommender

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

    if not json_data or 'category' not in json_data:
        return jsonify({'Error': 'Please provide a category.'}), 400
    
    category = json_data['category']
    user_data = json_data['user_scores']

    if category not in categories:
        return jsonify({'Error': 'Invalid category.'}), 400
    

    if json_data['category'] == 'Book':
        try:
            user_data = [float(score) for score in user_data]
            if not all(0 <= score <= 10 for score in user_data):
                raise ValueError
        except ValueError:
            return jsonify({'Error': 'Invalid user scores.'}), 400

        similar_items = rec.get_similar_books(user_data)
    elif json_data['category'] == 'Music':
        similar_items = rec.get_similar_musics(user_data)
    elif json_data['category'] == 'Movie':
        similar_items = rec.get_similar_movies(user_data)
    elif json_data['category'] == 'Podcast':
        similar_items = rec.get_similar_podcasts(user_data)
    else:
        return jsonify({'Error': 'Invalid Category.'}), 400

    return jsonify({'Recommendation': similar_items, 'Category': json_data['category']})

if __name__ == '__main__':
    print('Books', rec.get_similar_books(np.random.uniform(0.0, 10.0, size=10)))
    print('Movies', rec.get_similar_movies({
        "favorite_actors": ["Leonardo DiCaprio", "Kate Winslet", "Tom Hanks"],
        "genres": np.random.uniform(0.0, 10.0, size=21)
        }))
    print('Songs',rec. get_similar_musics({
        "favorite_artists": ['Gorillaz', '50 Cent', 'Snoop Dogg', 'João Gomes'],
    }))

    print('Podcasts', rec.get_similar_podcasts({
        "favorite_producers": ['RiotCast Network', 'BBC', 'VAULT Studios'],
        "genres": np.random.uniform(0.0, 10.0, size=20)
    }))
    app.run(debug=True)
