from sklearn.cluster import KMeans
from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import ast
import random


book_genres = ['young-adult', 'poetry', 'fantasy, paranormal', 'non-fiction', 
               'mystery, thriller, crime', 'children', 'romance', 'comics, graphic', 
               'history, historical fiction, biography', 'fiction']

movie_genres = ['Animation', 'Sci-Fi', 'History', 'War', 'Family', 'Mystery', 
                'Action', 'Music', 'Musical', 'Crime', 'Sport', 'Romance', 
                'Adventure', 'Fantasy', 'Horror', 'Biography', 'Drama', 
                'Thriller', 'Comedy', 'Film-Noir', 'Western']

podcast_genres = ['Sports', 'Business', 'NA', 'Music', 'Government', 'Religion & Spirituality', 
                'Education', 'History', 'Science', 'Health & Fitness', 'News', 'Arts', 
                'Society & Culture', 'TV & Film', 'Comedy', 'True Crime', 
                'Fiction', 'Leisure', 'Kids & Family', 'Technology']


class Recommender:
    def __init__(self, podcasts_data, musics_data, movies_data, books_data) -> None:
        self.podcasts_data = podcasts_data
        self.musics_data =musics_data
        self.movies_data = movies_data
        self.books_data = books_data

    def get_book_vectors(self):
        book_vectors = []
        for i in self.books_data.values:
            genres = ast.literal_eval(i[7])
            vector = [10 if g in genres else 0 for g in book_genres]
            book_vectors.append(vector)
        return np.array(book_vectors)


    def get_similar_books(self, user_data:list):
        user_data = np.array(user_data)
        books = self.get_book_vectors()

        n_clusters = 8
        kmeans = KMeans(n_clusters=n_clusters)
        kmeans.fit(books)
        
        cluster_label = kmeans.predict(user_data.reshape(1, -1))[0]
        
        book_cluster_labels = kmeans.labels_
        book_ids_in_cluster = np.where(book_cluster_labels == cluster_label)[0]
        
        book_titles = self.books_data.iloc[book_ids_in_cluster, 0].tolist()

        if len(book_titles) < 5:
            remaining_count = 5 - len(book_titles)
            all_book_titles = self.books_data.iloc[:, 0].tolist()
            for i in range(remaining_count):
                random_title = random.choice(all_book_titles)
                while random_title in book_titles:
                    random_title = random.choice(all_book_titles)
                book_titles.append(random_title)

        return book_titles
    

    def get_movie_vectors(self, favorite_actors):
        movie_vectors = []
        for i, row in self.movies_data.iterrows():
            score = -10
            if any(actor in [row['Star1'], row['Star2'], row['Star3'], row['Star4']] for actor in favorite_actors):
                score = 10
            genres = row['Genre'].split(', ')
            vector = [10 if g in genres else 0 for g in movie_genres]
            movie_vectors.append([score] + vector)
        return np.array(movie_vectors)
    

    def get_similar_movies(self, user_fav_actors, user_genres):
        user_favorite_genres = np.array(user_genres)
        user_favorite_genres = np.insert(user_favorite_genres, 0, 10)
        movies = self.get_movie_vectors(user_fav_actors)

        n_clusters = 8
        kmeans = KMeans(n_clusters=n_clusters)
        kmeans.fit(movies)

        cluster_label = kmeans.predict(user_favorite_genres.reshape(1, -1))[0]

        movie_cluster_labels = kmeans.labels_
        movie_ids_in_cluster = np.where(movie_cluster_labels == cluster_label)[0]

        recommended_movies = self.movies_data.iloc[movie_ids_in_cluster, :]
        recommended_movies = recommended_movies.sort_values(by='IMDB_Rating', ascending=False)

        return recommended_movies.iloc[:20, 0].tolist()
    

    def get_podcast_vectors(self, user_data):
        podcast_vectors = []
        for i, row in self.podcasts_data.iterrows():
            score = -10
            if any(producer in row['producer'] for producer in user_data['favorite_producers']):
                score = 10
            genres = row['genre']
            vector = [10 if g == genres else 0 for g in podcast_genres]
            podcast_vectors.append([score] + vector)
        return np.array(podcast_vectors)


    def get_similar_podcasts(self, favorite_producers):
        podcasts = self.get_podcast_vectors(favorite_producers)
        user_favorite_genres = np.array(favorite_producers['genres'])
        user_favorite_genres = np.insert(user_favorite_genres, 0, 10)
        
        n_clusters = 20
        kmeans = KMeans(n_clusters=n_clusters)
        kmeans.fit(podcasts)

        cluster_label = kmeans.predict(user_favorite_genres.reshape(1, -1))[0]

        podcast_cluster_labels = kmeans.labels_
        podcast_ids_in_cluster = np.where(podcast_cluster_labels == cluster_label)[0]

        if len(podcast_ids_in_cluster) == 0:
            return []

        recommended_podcasts = self.podcasts_data.iloc[podcast_ids_in_cluster, :]
        recommended_podcasts = recommended_podcasts.sort_values(by='rating', ascending=False)

        return recommended_podcasts.iloc[:20, 8].tolist()
    

    def get_similar_musics(self, user_fav_artists):
        similar_musics = []
        for index, row in self.musics_data.iterrows():
            if row['Artist'] in user_fav_artists:
                similar_musics.append(row)

        sorted_musics = sorted(similar_musics, key=lambda x: x['Likes'], reverse=True)
        return [music['ID'] for music in sorted_musics[:20]]