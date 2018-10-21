from protobuf.todo_pb2 import User, ToDo, SUCCESS, FAILED
from server.models.todo_db import ToDoDb


class ServerUtils:

    def __init__(self, todo_db=None):
        self.todo_db = todo_db or ToDoDb()

    def add_user(self, user):
        if isinstance(user, User) and user.name:
            user.id = self.todo_db.add_user_if_not_exist(name=user.name)
            if user.id != 0:
                user.status = SUCCESS
                return user
        return User(status=FAILED)

    def add_todo(self, todo):
        if isinstance(todo, ToDo) and todo.text and todo.user.id != 0:
            try:
                todo.id = self.todo_db.add_todo(todo.user.id, todo.text)
            except ValueError:
                return ToDo(status=FAILED)

            todo.status = SUCCESS if todo.id else FAILED
            return todo
        return ToDo(status=FAILED)

    def update_todo(self, todo):
        todo.status = FAILED
        if isinstance(todo, ToDo) and todo.id != 0:
            try:
                status = self.todo_db.update_todo(
                    todo_id=todo.id,
                    user_id=todo.user.id if todo.user.id != 0 else None,
                    is_done=todo.is_done)
            except ValueError:
                return todo

            todo.status = SUCCESS if status else FAILED
        return todo

    def get_todo_list(self, user):
        if isinstance(user, User) and user.id != 0:
            todo_list = []
            try:
                todo_row_list = self.todo_db.get_todo_list(user.id)
            except ValueError:
                return ToDo(status=FAILED)

            for todo_row in todo_row_list:
                todo = ToDo(
                    id=todo_row[0],
                    user=User(id=todo_row[1]),
                    text=todo_row[2],
                    is_done=True if todo_row[3] == 1 else False
                )
                todo_list.append(todo)
            return todo_list

        return ToDo(status=FAILED)
