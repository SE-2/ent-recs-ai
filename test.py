import pandas as pd
import numpy as np
import unittest
from Recommender import Recommender

book_genres = ['young-adult', 'poetry', 'fantasy, paranormal', 'non-fiction', 
               'mystery, thriller, crime', 'children', 'romance', 'comics, graphic', 
               'history, historical fiction, biography', 'fiction']


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

    

if __name__ == '__main__':
    unittest.main()