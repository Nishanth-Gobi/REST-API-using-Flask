# Hello world program

from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class Hello(Resource):
    # Class corresponding to the '/hello/<string:name>' API endpoint

    # Static as we are not instantiating the class
    # We can use a not-static function as well (ensure to add the "self" argument)
    @staticmethod
    def get(name):
        # Returning JSON as it's serializable
        return {'data': 'Hello, {}!'.format(name)}
        # You can return just a string as well (as below)
        # return "Hello!"


# We can add an API endpoint using the 'add_resource' method
# '<string:name>' indicates an argument 'name' of type string
api.add_resource(Hello, '/hello/<string:name>')

if __name__ == '__main__':
    app.run(debug=True)
