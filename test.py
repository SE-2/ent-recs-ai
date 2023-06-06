import pandas as pd
import numpy as np
import unittest
from Recommender import Recommender

book_genres = ['young-adult', 'poetry', 'fantasy, paranormal', 'non-fiction', 
               'mystery, thriller, crime', 'children', 'romance', 'comics, graphic', 
               'history, historical fiction, biography', 'fiction']

movie_genres = ['Animation', 'Sci-Fi', 'History', 'War', 'Family', 'Mystery', 
                'Action', 'Music', 'Musical', 'Crime', 'Sport', 'Romance', 
                'Adventure', 'Fantasy', 'Horror', 'Biography', 'Drama', 
                'Thriller', 'Comedy', 'Film-Noir', 'Western']

class TestRecommender(unittest.TestCase):

    def setUp(self):
        self.books_data = pd.read_csv('datasets/books_dataset.csv')
        self.musics_data = pd.read_csv('datasets\musics_dataset.csv')
        self.movies_data = pd.read_csv('datasets/movies_dataset.csv', encoding='ISO-8859-1')
        self.podcasts_data = pd.read_json('datasets/podcast.json')
        self.recommender = Recommender(self.podcasts_data, self.musics_data, self.movies_data, self.books_data)

    def test_get_book_vectors(self):
        book_vectors = self.recommender.get_book_vectors()
        self.assertIsInstance(book_vectors, np.ndarray)
        self.assertEqual(book_vectors.shape, (self.books_data.shape[0], len(book_genres)))

        # Test if the function returns a numpy array with only 0 and 10 values
        self.assertTrue(np.isin(book_vectors, [0, 10]).all())


    def test_get_similar_books(self):
        user_data = [0, 10, 0, 0, 0, 0, 0, 0, 0, 0]
        book_titles = self.recommender.get_similar_books(user_data)
        self.assertIsInstance(book_titles, list)
        self.assertTrue(all(isinstance(title, str) for title in book_titles))

        # Test if the function returns at least 5 book titles
        self.assertGreaterEqual(len(book_titles), 5)


    def test_get_movie_vectors(self):
        favorite_actors = ['Tom Hanks', 'Julia Roberts', 'Brad Pitt']
        movie_vectors = self.recommender.get_movie_vectors(favorite_actors)
    
        # Verify that the output has the correct shape
        self.assertEqual(movie_vectors.shape, (self.movies_data.shape[0], len(movie_genres) + 1))

        # Verify that the first element of each row is either 10 or -10
        self.assertTrue(np.isin(movie_vectors[:, 0], [-10, 10]).all())

        # Verify that the remaining elements of each row are either 0 or 10
        self.assertTrue(np.isin(movie_vectors[:, 1:], [0, 10]).all())

    

if __name__ == '__main__':
    unittest.main()