from flask import Flask, request, jsonify
import pandas as pd
from sklearn.neighbors import NearestNeighbors

app = Flask(__name__)

# DATASET_LINKS = []
# books_data = pd.read_csv('books.csv')
# music_data = pd.read_csv('music.csv')
# movies_data = pd.read_csv('movies.csv')
# podcasts_data = pd.read_csv('podcasts.csv')


categories = ['Book', 'Music', 'Movie', 'podcast']

@app.route('/api/similar_items', methods=['POST'])
def get_similar_items():
    json_data = request.get_json()

    if not json_data or 'category' not in json_data:
        return jsonify({'Error': 'Please provide a category.'}), 400
    
    category = json_data['category']
    user_scores = json_data['user_scores']
    
    if category not in categories:
        return jsonify({'Error': 'Invalid category.'}), 400
    


    # TODO: build similar_items to return
    return jsonify({'Recommendation': similar_items})

if __name__ == '__main__':
    app.run(debug=True)
