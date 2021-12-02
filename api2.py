from flask import Flask
from flask_restful import Resource, Api, abort, reqparse

app = Flask(__name__)
api = Api(app)

# program data
todo = {
    1: {"task": "kill bill"},
    2: {"task": "save bill"},
}


task_post_args = reqparse.RequestParser()
# To get the mandatory argument 'task' of type string supplied with a POST request
# Input validation
task_post_args.add_argument("task", type=str, help="Task is required", required=True)


class ToDoList(Resource):
    @staticmethod
    def get():
        return todo


class ToDo(Resource):
    @staticmethod
    # ensure that the argument name 'id' is the same as in the endpoint '<int:id>'
    def get(id):
        return todo[id]

    @staticmethod
    def post(id):
        # get the parsed arguments as a dictionary
        args = task_post_args.parse_args()

        if id in todo:
            # return error, second argument's name is customizable
            abort(409, Error="ID already taken")
        todo[id] = {"task": args["task"]}
        return todo[id]


api.add_resource(ToDoList, "/todo")
api.add_resource(ToDo, "/todo/<int:id>")


if __name__ == '__main__':
    app.run(debug=True)