import pytest

from client.text_format import TextFormat
from protobuf.todo_pb2 import ToDo


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
