import pandas as pd
import numpy as np
from unittest import TestCase
from Recommender import Recommender

class TestRecommender(TestCase):

    def setUp(self):
        self.books_data = pd.read_csv('datasets/books_dataset.csv')
        self.musics_data = pd.read_csv('datasets\musics_dataset.csv')
        self.movies_data = pd.read_csv('datasets/movies_dataset.csv', encoding='ISO-8859-1')
        self.podcasts_data = pd.read_json('datasets/podcast.json')
        self.recommender = Recommender(self.podcasts_data, self.musics_data, self.movies_data, self.books_data)
