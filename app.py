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

movie_genres = ['Animation', 'Sci-Fi', 'History', 'War', 'Family', 'Mystery', 
                'Action', 'Music', 'Musical', 'Crime', 'Sport', 'Romance', 
                'Adventure', 'Fantasy', 'Horror', 'Biography', 'Drama', 
                'Thriller', 'Comedy', 'Film-Noir', 'Western']

def get_book_vectors():
    book_vectors = []
    for i in books_data.values:
        genres = ast.literal_eval(i[7])
        vector = [10 if g in genres else 0 for g in book_genres]
        book_vectors.append(vector)
    return np.array(book_vectors)

def get_movie_containing_actors(actors):
    result = []
    for index, row in movies_data.iterrows():
        if any(actor in [row['Star1'], row['Star2'], row['Star3'], row['Star4']] for actor in actors):
            result.append(row)
    return pd.DataFrame(result)


def get_movie_vectors(selected_movies):
    movie_vectors = []
    for i in selected_movies:
        genres = i.split(', ')
        vector = [10 if g in genres else 0 for g in movie_genres]
        movie_vectors.append(vector)
    return np.array(movie_vectors)


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
    user_favorite_genres = np.array(user_prefs['genres'])
    selected_movies = get_movie_containing_actors(user_prefs['favorite_actors'])
    movies = get_movie_vectors(selected_movies['Genre'])

    n_clusters = 10
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(movies)

    cluster_label = kmeans.predict(user_favorite_genres.reshape(1, -1))[0]
    
    movie_cluster_labels = kmeans.labels_
    movie_ids_in_cluster = np.where(movie_cluster_labels == cluster_label)[0][:5]
    
    movie_ids = selected_movies.iloc[movie_ids_in_cluster, 0].tolist()

    return movie_ids


def get_similar_podcasts(data):
    IDs = np.random.randint(0, 91, size=20)
    return IDs


app = Flask(__name__)

DATASET_LINKS = []
books_data = pd.read_csv('datasets/books_dataset.csv')
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

music_data = pd.read_csv('datasets\musics_dataset.csv')
movies_data = pd.read_csv('datasets/movies_dataset.csv', encoding='ISO-8859-1')

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
    print('Books', get_similar_books(np.random.uniform(0.0, 10.0, size=10)))
    print('Movies', get_similar_movies({
        "favorite_actors": ["Leonardo DiCaprio", "Kate Winslet", "Tom Hanks"],
        "genres": np.random.uniform(0.0, 10.0, size=21)
        }))
    app.run(debug=True)
