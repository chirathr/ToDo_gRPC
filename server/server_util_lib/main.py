from protobuf.todo_pb2 import User, ToDo, SUCCESS, FAILED
from server.models.todo_db import ToDoDb


def add_user(user):
    if isinstance(user, User) and user.name:
        user.id = ToDoDb().add_user_if_not_exist(name=user.name)
        user.status = SUCCESS
        return user
    return User(status=FAILED)


def add_todo(todo):
    if isinstance(todo, ToDo) and todo.text and todo.user.id != 0:
        todo.id = ToDoDb().add_todo(todo.user.id, todo.text)
        todo.status = SUCCESS if todo.id else FAILED
        return todo
    return ToDo(status=FAILED)


def update_todo(todo):
    if isinstance(todo, ToDo) and todo.id != 0:
        status = ToDoDb().update_todo(
            todo_id=todo.id,
            user_id=todo.user.id if todo.user.id != 0 else None,
            is_done=todo.is_done)
        todo.status = SUCCESS if status else FAILED
        return todo
    return ToDo(status=FAILED)


def get_todo_list(user):
    if isinstance(user, User) and user.id != 0:
        todo_list = []
        todo_row_list = ToDoDb().get_todo_list(user.id)
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
