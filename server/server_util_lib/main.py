from protobuf.todo_pb2 import User, ToDo, SUCCESS, FAILED
from server.models.todo_db import ToDoDb


class ServerUtils:

    def __init__(self, todo_db=None):
        self.todo_db = todo_db or ToDoDb()

    def add_user(self, user):
        if isinstance(user, User) and user.name:
            user_dict = self.todo_db.add_user(name=user.name)
            if user_dict['status']:
                user.id = user_dict['user'].id
                user.status = SUCCESS
                return user
        return User(status=FAILED)

    def add_todo(self, todo):
        if isinstance(todo, ToDo) and todo.text and todo.user.id != 0:
            todo_dict = self.todo_db.add_todo(todo.user.id, todo.text)
            if todo_dict['status']:
                todo.status = SUCCESS
                todo.id = todo_dict['todo'].id
                return todo
        return ToDo(status=FAILED)

    def update_todo(self, todo):
        if isinstance(todo, ToDo) and todo.id > 0:
            if self.todo_db.update_todo(todo.id, todo.is_done):
                todo.status = SUCCESS
                return todo
        return ToDo(status=FAILED)

    def get_todo_list(self, user):
        if isinstance(user, User) and user.id > 0:
            todo_list = []
            todo_list_dict = self.todo_db.get_todo_list(user.id)
            if todo_list_dict['status']:
                for current_todo in todo_list_dict['todo_list']:
                    todo = ToDo(
                        id=current_todo.id,
                        user=User(id=current_todo.user.id),
                        text=current_todo.text,
                        is_done=current_todo.is_done,
                        status=SUCCESS
                    )
                    todo_list.append(todo)
                return todo_list

        return [ToDo(status=FAILED), ]
