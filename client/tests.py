from unittest.mock import Mock, MagicMock

import pytest

from client.text_format import TextFormat
from client.client import Client
from protobuf.todo_pb2 import User, ToDo


# Tests for TextFormat
class TestTextFormat:
    text_end = '\x1b[0m'

    def test_green_check(self):
        expected = '\x1b[1;32;m' + u'\u2713' + self.text_end
        assert expected == TextFormat.green_check()

    def test_todo_text(self):
        todo = ToDo(id=1, text="Test string")
        expected_string = " {0}. {1}".format(
            todo.id, '\x1b[1;37;m' + todo.text + self.text_end)
        assert expected_string == TextFormat.todo_text(todo)

    def test_todo_text_raises_value_error_on_wrong_type(self):
        with pytest.raises(ValueError):
            TextFormat.todo_text("")

    def test_done_text(self):
        todo = ToDo(id=1, text="Test string")
        actual_text = TextFormat.todo_done_text(todo)

        text = '\x1b[2;37;m' + todo.text + self.text_end
        expected_string = " {0}. {1:<63}".format(todo.id, text[:50]) + TextFormat.green_check()

        assert expected_string == actual_text

    def test_done_todo_text_raises_value_error_on_wrong_type(self):
        with pytest.raises(ValueError):
            TextFormat.todo_done_text(None)


# Tests for Client class
class TestClient:

    def test_load_user(self):
        stub = Mock()
        stub.add_user.return_value = User(id=1)
        client = Client(stub=stub)
        assert client.load_user('User')
        stub.add_user.assert_called_once()
        stub.add_user.assert_called_with(User(name='User'))

    def test_load_user_fails(self):
        stub = Mock()
        stub.add_user.return_value = User()
        client = Client(stub=stub)
        assert not client.load_user('User')
        stub.add_user.assert_called_with(User(name='User'))

    def test_add_todo(self):
        stub = Mock()
        user = User(id=1, name="Name")
        stub.add_todo.return_value = ToDo(id=1, user=user, text="Todo item")
        client = Client(stub=stub, user=user)
        assert client.add_todo('Todo item')
        stub.add_todo.assert_called_with(ToDo(user=user, text="Todo item"))

    def test_add_todo_fails(self):
        stub = Mock()
        user = User(id=1, name="Name")
        stub.add_todo.return_value = ToDo(id=0)
        client = Client(stub=stub, user=user)
        assert not client.add_todo('Todo item')
        stub.add_todo.assert_called_with(ToDo(user=user, text="Todo item"))

    def test_add_todo_without_user_calls_load_user(self):
        stub = Mock()
        user = User(id=1, name="Name")
        stub.add_todo.return_value = ToDo(id=1, user=user, text="Todo item")
        client = Client(stub=stub)
        client.load_user = MagicMock()
        client.add_todo(todo_text="Todo")
        client.load_user.assert_called()

    def _todo_list(self, user):
        todo_list = [
            ToDo(id=1, user=user, text="Todo 1"),
            ToDo(id=2, user=user, text="Todo 2"),
            ToDo(id=3, user=user, text="Todo 3"),
        ]

        for todo in todo_list:
            yield todo

    def test_load_todo_list(self):
        stub = Mock()
        user = User(id=1, name="Name")
        stub.get_todo_list.return_value = self._todo_list(user)
        client = Client(stub=stub, user=user)
        assert client.load_todo_list()
        stub.get_todo_list.assert_called_with(user)

    def test_load_todo_list_fails(self):
        stub = Mock()
        user = User(id=1, name="Name")
        stub.get_todo_list.return_value = []
        client = Client(stub=stub, user=user)
        assert not client.load_todo_list()
        stub.get_todo_list.assert_called_with(user)

    def test_load_todo_list(self):
        stub = Mock()
        user = User(id=1, name="Name")
        stub.get_todo_list.return_value = self._todo_list(user)
        client = Client(stub=stub)
        client.load_user = MagicMock()
        client.load_todo_list()
        client.load_user.assert_called()
