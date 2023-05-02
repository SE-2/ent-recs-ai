from flask import Flask, request, jsonify
import pandas as pd
from sklearn.neighbors import NearestNeighbors

# now we wait for backend team to define requests
app = Flask(__name__)

DATASET_LINKS = []
books_data = pd.read_csv('books.csv')
music_data = pd.read_csv('music.csv')
movies_data = pd.read_csv('movies.csv')
podcasts_data = pd.read_csv('podcasts.csv')


categories = ['Book', 'Music', 'Movie', 'podcast']
data = []
X = data
knn = NearestNeighbors(n_neighbors=5)
knn.fit(X)

@app.route('/api/similar_users', methods=['GET'])
def get_similar_users():
    user_id = int(request.args.get('user_id'))
    if not user_id:
        return jsonify({'error': 'Please provide a user ID.'}), 400
    
    user_index = data[data['id'] == user_id].index[0]
    distances, indices = knn.kneighbors(X.iloc[user_index].values.reshape(1, -1))
    
    neighbor_user_ids = [data.iloc[index]['id'] for index in indices.squeeze()]

    return jsonify({'Similar users': neighbor_user_ids})


if __name__ == '__main__':
    app.run(debug=True)
