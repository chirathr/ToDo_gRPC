from protobuf.todo_pb2 import User, ToDo, SUCCESS, FAILED
from server.models.todo_db import ToDoDb


def add_user(user):
    if isinstance(user, User) and user.name:
        user.id = ToDoDb().add_user_if_not_exist(name=user.name)
        user.status = SUCCESS
        return user
    return User(status=FAILED)


def add_todo(todo):
    if isinstance(todo, ToDo) and todo.id != 0 and todo.text and todo.user.id != 0:
        todo_id = ToDoDb().add_todo(todo.user.id, todo.text)
        if todo_id:
            todo.status = SUCCESS
            todo.id = todo_id
        else:
            todo.status = FAILED
        return todo
    return ToDo(status=FAILED)


def update_todo(todo):
    if isinstance(todo, ToDo) and todo.id != 0:
        todo_id = ToDoDb().update_todo(
            todo_id=todo.id, user_id=todo.user.id, is_done=todo.is_done)
        return todo_id
    return ToDo(status=FAILED)


def get_todo_list(user):
    if isinstance(user, User) and user.id != 0:
        todo_list = ToDoDb().get_todo_list(user)
        for todo in todo_list:
            yield todo
    yield ToDo(status=FAILED)
