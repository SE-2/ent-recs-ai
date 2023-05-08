import unittest
import requests

class TestGetSimilarItems(unittest.TestCase):
    def setUp(self):
        self.url = 'http://localhost:5000/api/similar_items'
        self.headers = {'Content-Type': 'application/json'}


if __name__ == '__main__':
    unittest.main()