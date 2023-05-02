from flask import Flask, request
import json

# now we wait for backend team to define requests
app = Flask(__name__)

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

@app.route('/api/user', methods=['GET'])
def user():
    name = request.args.get('name')
    if name:
        person = Person(name=name, age=30)
        return json.dumps(person.__dict__)
    else:
        return 'Please provide a name.'

if __name__ == '__main__':
    app.run(debug=True)
