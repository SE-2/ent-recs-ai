import unittest
import requests

class TestGetSimilarItems(unittest.TestCase):
    def setUp(self):
        self.url = 'http://localhost:5000/api/similar_items'
        self.headers = {'Content-Type': 'application/json'}


    def test_invalid_category(self):
        data = {'category': 'Invalid', 'user_scores': [0.5, 0.3, 0.8]}
        response = requests.post(url=self.url, headers=self.headers, json=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid category.', response.json()['Error'])


    def test_missing_category(self):
        data = {'user_scores': [0.5, 0.3, 0.8]}
        response = requests.post(url=self.url, headers=self.headers, json=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Please provide a category.', response.json()['Error'])


if __name__ == '__main__':
    unittest.main()