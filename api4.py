from flask import Flask
from flask_restful import Resource, Api, abort, reqparse, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
db = SQLAlchemy(app)


# Schema for the db
class ToDoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200))


# creating the db - run only once
db.create_all()

task_post_args = reqparse.RequestParser()
task_post_args.add_argument("task", type=str, help="Task is required", required=True)

task_put_args = reqparse.RequestParser()
task_put_args.add_argument("task", type=str)

# Output format - serialised
resource_fields = {
    'id': fields.Integer,
    'task': fields.String,
}


class ToDoList(Resource):
    @staticmethod
    def get():
        tasks = ToDoModel.query.all()
        todos = {}
        for task in tasks:
            todos[task.id] = {"task": task.task}

        return todos


class ToDo(Resource):
    # 'marshal_with' annotation helps in mapping the returned value to the output format 'resource_fields'
    @marshal_with(resource_fields)
    def get(self, id):
        task = ToDoModel.query.filter_by(id=id).first()
        if not task:
            abort(409, message="Task does not exist")
        return task

    @marshal_with(resource_fields)
    def post(self, id):
        args = task_post_args.parse_args()
        task = ToDoModel.query.filter_by(id=id).first()
        if task:
            abort(409, message="Task ID is already taken")

        todo = ToDoModel(id=id, task = args['task'])
        db.session.add(todo)
        db.session.commit()
        return todo, 201

    @marshal_with(resource_fields)
    def put(self, id):
        args = task_put_args.parse_args()
        task = ToDoModel.query.filter_by(id=id).first()
        if not task:
            abort(409, message="Task does not exist")
        if args['task']:
            task.task = args['task']
        db.session.commit()
        return task

    @staticmethod
    def delete(id):
        task = ToDoModel.query.filter_by(id=id).first()
        if not task:
            abort(409, message="Task does not exist")
        db.session.delete(task)
        db.session.commit()
        return 'Todo deleted'


api.add_resource(ToDo, "/todo/<int:id>")
api.add_resource(ToDoList, "/todo")

if __name__ == '__main__':
    app.run(debug=True)