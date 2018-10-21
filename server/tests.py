from unittest.mock import Mock, patch

import pytest

from server.models.todo_db import ToDoDb
from protobuf.todo_pb2 import User, ToDo, SUCCESS, FAILED
from server.server_util_lib.main import add_user, add_todo, update_todo, get_todo_list


# Server util functions test
def test_add_user():
    with patch('server.models.todo_db.ToDoDb', spec=True) as todo_db_stub:
        todo_db_stub.add_user_if_not_exist.return_value = 1
        print(todo_db_stub.add_user_if_not_exist())
        user = add_user(User(name="Test"))
        assert user.id == 1
        assert user.name == "Test"
