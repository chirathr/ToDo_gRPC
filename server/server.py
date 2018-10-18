from server.todo_db import ToDoDb
from protobuf.todo_pb2 import User, ToDo
from protobuf import todo_pb2_grpc


class ToDoServicer(todo_pb2_grpc.TodoServiceServicer):
    """
    Methods that implement the functionality of the ToDo server
    """
    def __init__(self):
        pass

    def add_user(self, user, context):
        if not user.name:
            return User()
        db = ToDoDb()
        return db.add_user_if_not_exist(user)

    def add_todo(self, todo, context):
        if not todo.text and not todo.user:
            return ToDo()
        db = ToDoDb()
        return db.add_todo(todo)

    def update_todo(self, todo, context):
        if not todo.text and not todo.user:
            return ToDo()
        db = ToDoDb()
        return db.update_todo(todo)

    def get_todo_list(self, user, context):
        if user.id == 0:
            return []
        db = ToDoDb()
        todo_list = db.get_todo_list(user)
        for todo in todo_list:
            yield todo

    def delete_todo_list(self, user, context):
        pass
