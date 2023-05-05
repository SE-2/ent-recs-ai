from flask import Flask, request

app = Flask(__name__)
categories = ['Book', 'Music', 'Movie', 'podcast']

@app.route('/api/similar_items', methods=['POST'])
def get_similar_items():
    pass

if __name__ == '__main__':
    app.run(debug=True)
