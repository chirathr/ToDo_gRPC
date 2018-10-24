from unittest.mock import Mock

import pytest
import grpc

from client.text_format import TextFormat
from client.client_util_lib.client_stub import ClientStub
from protobuf.todo_pb2_grpc import TodoServiceStub
from protobuf.todo_pb2 import User, ToDo, FAILED, SUCCESS


# Tests for client_stub util class
class TestClientStub:
    stub = Mock(spec=TodoServiceStub(channel=grpc.insecure_channel('')))
    user = Mock(spec=User())
    todo = Mock(spec=ToDo())
    id_test_arguments = [0, -20, "test", 15.5]

    def test_add_user(self):
        self.user.status = SUCCESS
        self.stub.AddUser.return_value = self.user

        client_stub = ClientStub(stub=self.stub)
        assert client_stub.add_user("Test") == self.user

    def test_add_user_returns_none_on_failure(self):
        self.user.status = FAILED
        self.stub.AddUser.return_value = self.user

        client_stub = ClientStub(stub=self.stub)
        assert client_stub.add_user("Test") is None

    def test_add_todo(self):
        self.todo.status = SUCCESS
        self.stub.AddToDo.return_value = self.todo

        client_stub = ClientStub(stub=self.stub)
        assert client_stub.add_todo(1, "Test todo") == self.todo

    def test_add_todo_returns_none_on_failure(self):
        self.todo.status = FAILED
        self.stub.AddToDo.return_value = self.todo

        client_stub = ClientStub(stub=self.stub)
        assert client_stub.add_todo(1, "Test todo") is None

    def add_todo_raises_value_error(self):
        client_stub = ClientStub(stub=self.stub)

        for user_id in self.id_test_arguments:
            with pytest.raises(ValueError):
                client_stub.add_todo(user_id, "Todo test")

    def test_get_todo_list(self):
        self.todo.status = SUCCESS
        todo_list = [self.todo, self.todo, self.todo]
        self.stub.GetToDoList.return_value = todo_list

        client_stub = ClientStub(stub=self.stub)
        assert client_stub.get_todo_list(1) == todo_list

    def test_get_todo_list_raise_value_error_for_todo_id(self):
        client_stub = ClientStub(stub=self.stub)
        for todo_id in self.id_test_arguments:
            with pytest.raises(ValueError):
                client_stub.get_todo_list(todo_id)

    def test_update_todo_with_delete(self):
        self.todo.status = SUCCESS
        self.stub.UpdateToDo.return_value = self.todo

        client_stub = ClientStub(stub=self.stub)
        assert client_stub.update_todo(1, delete=True)

    def test_update_todo_with_delete_raise_value_error(self):
        client_stub = ClientStub(stub=self.stub)
        for todo_id in self.id_test_arguments:
            with pytest.raises(ValueError):
                client_stub.update_todo(todo_id, delete=True)

    def test_update_todo_with_delete_is_done_raises_value_error(self):
        client_stub = ClientStub(stub=self.stub)
        with pytest.raises(ValueError):
            client_stub.update_todo(1, delete=True, is_done=True)

    def test_update_todo_with_is_done(self):
        self.todo.status = SUCCESS
        self.stub.UpdateToDo.return_value = self.todo

        client_stub = ClientStub(stub=self.stub)
        assert client_stub.update_todo(1, is_done=True)

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
