# Working with GET, POST, PUT & DELETE methods

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
task_post_args.add_argument("task", type=str, help="Task is required", required=True)

# Another parser to handle put requests
task_put_args = reqparse.RequestParser()
task_put_args.add_argument("task", type=str)


class ToDoList(Resource):

    @staticmethod
    def get():
        return todo


class ToDo(Resource):

    @staticmethod
    # To read from todo
    def get(id):
        return {'task': '{}'.format(todo[id])}

    @staticmethod
    # To write into todo
    def post(id):
        args = task_post_args.parse_args()
        if id in todo:
            abort(409, message="ID already assigned to a task!")
        todo[id] = {"task": args["task"]}
        return todo[id]

    @staticmethod
    # To edit a task in todo
    def put(id):
        args = task_put_args.parse_args()
        if id not in todo:
            abort(409, message="Task not found")
        if args["task"]:
            todo[id] = {"task": args["task"]}
        return todo[id]

    @staticmethod
    # To delete a task in todo
    def delete(id):
        if id not in todo:
            abort(409, message="Task not found")
        del todo[id]
        return todo


api.add_resource(ToDo, '/todo/<int:id>')
api.add_resource(ToDoList, '/todo')

if __name__ == '__main__':
    app.run(debug=True)
