from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import ast

book_genres = ['young-adult', 'poetry', 'fantasy, paranormal', 'non-fiction', 
               'mystery, thriller, crime', 'children', 'romance', 'comics, graphic', 
               'history, historical fiction, biography', 'fiction']


def get_book_vectors():
    book_vectors = []
    for i in books_data.values:
        genres = ast.literal_eval(i[8])
        vector = [10 if g in genres else 0 for g in book_genres]
        book_vectors.append(vector)
    return np.array(book_vectors)


def get_similar_books(user_data:list):
    user_data = np.array(user_data)
    books = get_book_vectors()

    n_clusters = 10
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(books)
    
    cluster_label = kmeans.predict(user_data.reshape(1, -1))[0]
    
    book_cluster_labels = kmeans.labels_
    book_ids_in_cluster = np.where(book_cluster_labels == cluster_label)[0][:5]

    return book_ids_in_cluster.tolist()


def get_similar_musics(user_data):
    IDs = np.random.randint(0, 91, size=20)
    return IDs


def get_similar_movies(user_prefs: dict):
    IDs = np.random.randint(0, 91, size=20)
    return IDs


def get_similar_podcasts(data):
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
# Unique Genres (21)
# {'Animation', 'Sci-Fi', 'History', 'War', 'Family', 'Mystery', 
# 'Action', 'Music', 'Musical', 'Crime', 'Sport', 'Romance', 
# 'Adventure', 'Fantasy', 'Horror', 'Biography', 'Drama', 
# 'Thriller', 'Comedy', 'Film-Noir', 'Western'}
podcasts_data = pd.read_json('datasets/podcast.json')

categories = ['Book', 'Music', 'Movie', 'Podcast']

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

        similar_items = get_similar_books(user_data)
    elif json_data['category'] == 'Music':
        similar_items = get_similar_musics(user_data)
    elif json_data['category'] == 'Movie':
        similar_items = get_similar_movies(user_data)
    elif json_data['category'] == 'Podcast':
        similar_items = get_similar_podcasts(user_data)
    else:
        return jsonify({'Error': 'Invalid Category.'}), 400

    return jsonify({'Recommendation': similar_items, 'Category': json_data['category']})

if __name__ == '__main__':
    print(get_similar_books([4.123,5.55,8.123,1,1,1,1.123,2.123, 7.7, 8.88]))
    # print(get_similar_movies({
    #     "favorite_actors": ["Leonardo DiCaprio", "Kate Winslet", "Tom Hanks"],
    #     "genres": ["Drama", "Action"]
    #     }))
    app.run(debug=True)
