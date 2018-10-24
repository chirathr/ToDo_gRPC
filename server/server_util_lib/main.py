from protobuf.todo_pb2 import User, ToDo, SUCCESS, FAILED
from server.models.todo_db import ToDoDb


class ServerUtils:

    def __init__(self, todo_db=None):
        self.todo_db = todo_db or ToDoDb()

    def add_user(self, user):
        print(isinstance(user, User))

        if isinstance(user, User) and user.name:
            print(user.name)
        if isinstance(user, User) and user.name:
            print(user)
            user.id = self.todo_db.add_user_if_not_exist(name=user.name)
            print("User id: " + str(user.id))
            if user.id > 0:
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
        if isinstance(todo, ToDo) and todo.id > 0:
            try:
                status = self.todo_db.update_todo(
                    todo_id=todo.id,
                    user_id=todo.user.id if todo.user.id != 0 else None,
                    is_done=todo.is_done)
            except ValueError:
                status = FAILED

            todo.status = status
            return todo
        return ToDo(status=FAILED)

    def get_todo_list(self, user):
        if isinstance(user, User) and user.id > 0:
            todo_list = []
            try:
                _todo_list = self.todo_db.get_todo_list(user.id)
            except ValueError:
                return [ToDo(status=FAILED), ]

            for current_todo in _todo_list:
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
