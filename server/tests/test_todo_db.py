from server.models.todo_db import ToDoDb
from server.tests.conftest import ServerTestHelper


# Test models
class TestToDoDb:
    helper = ServerTestHelper()

    def test_get_user(self, db_session):
        todo_db = ToDoDb(db_session=db_session)
        expected_user = self.helper.mock_add_user(db_session, "Test user")

        user_dict = todo_db.get_user("Test user")
        actual_user = user_dict['user']

        assert user_dict['status'] == True
        assert actual_user.id == expected_user.id
        assert actual_user.name == expected_user.name

    def test_get_user_empty_db(self, db_session):
        todo_db = ToDoDb(db_session=db_session)

        assert todo_db.get_user("Test user")['status'] == False

    def test_get_user_empty_name_raises_value_error(self, db_session):
        todo_db = ToDoDb(db_session=db_session)

        assert todo_db.get_user("")['status'] == False

    def test_add_user(self, db_session):
        todo_db = ToDoDb(db_session=db_session)
        user_dict = todo_db.add_user("Test user")
        actual_user = user_dict['user']
        expected_user = self.helper.mock_get_user_list(db_session)[0]

        assert user_dict['status'] == True
        assert actual_user.id == expected_user.id
        assert actual_user.name == expected_user.name

    def test_add_user_if_exists(self, db_session):
        todo_db = ToDoDb(db_session=db_session)
        expected_user = self.helper.mock_add_user(db_session, "Test user")

        user_dict = todo_db.add_user("Test user")
        actual_user = user_dict['user']

        assert user_dict['status'] == True
        assert actual_user.id == expected_user.id
        assert actual_user.name == expected_user.name

    def test_add_user_empty_name_raises_value_error(self, db_session):
        todo_db = ToDoDb(db_session=db_session)

        assert todo_db.add_user("")['status'] == False

    def test_add_todo(self, db_session):
        todo_db = ToDoDb(db_session=db_session)
        user = self.helper.mock_add_user(db_session, "Test user")
        todo_dict = todo_db.add_todo(user.id, "Test todo")
        expected_todo = self.helper.mock_get_todo_list(db_session, user.id)[0]
        actual_todo = todo_dict['todo']

        assert todo_dict['status'] == True
        assert actual_todo.id == expected_todo.id
        assert actual_todo.text == expected_todo.text
        assert actual_todo.user.id == expected_todo.user.id

    def test_add_todo_empty_text_raises_error(self, db_session):
        todo_db = ToDoDb(db_session=db_session)

        assert todo_db.add_todo(1, "")['status'] == False

    def test_add_todo_invalid_user_id(self, db_session):
        todo_db = ToDoDb(db_session=db_session)
        assert todo_db.add_todo(None, "")['status'] == False
        assert todo_db.add_todo(-1, "")['status'] == False
        assert todo_db.add_todo(10, "Todo 1")['status'] == False

    def test_update_todo_is_done(self, db_session):
        todo_db = ToDoDb(db_session=db_session)
        user = self.helper.mock_add_user(db_session, "Test user")
        todo = self.helper.mock_add_todo(db_session, user.id, "Test Todo")

        assert todo_db.update_todo(todo.id, is_done=True) is True
        assert self.helper.mock_get_todo(db_session, todo.id).is_done is True

    def test_update_todo_fails_on_invalid_todo_id_input(self, db_session):
        todo_db = ToDoDb(db_session=db_session)

        # Mark todo as done
        assert todo_db.update_todo(-1, is_done=True) is False
        # Delete todo
        assert todo_db.update_todo(1) is False

    def test_update_todo_delete(self, db_session):
        todo_db = ToDoDb(db_session=db_session)
        user = self.helper.mock_add_user(db_session, "Test user")
        todo = self.helper.mock_add_todo(db_session, user.id, "Test Todo")

        assert todo_db.update_todo(todo.id) is True
        assert self.helper.mock_get_todo(db_session, todo.id) is None

    def test_get_todo_list(self, db_session):
        todo_db = ToDoDb(db_session=db_session)
        user = self.helper.mock_add_user(db_session, "Test user")
        self.helper.mock_add_todo(db_session, user.id, "Test Todo 1")
        self.helper.mock_add_todo(db_session, user.id, "Test Todo 2")

        expected_todo_list = self.helper.mock_get_todo_list(db_session, user.id)
        todo_list_dict = todo_db.get_todo_list(user.id)
        actual_todo_list = todo_list_dict['todo_list']

        assert todo_list_dict['status'] == True
        for i in range(len(expected_todo_list)):
            assert expected_todo_list[i].id == actual_todo_list[i].id
            assert expected_todo_list[i].text == actual_todo_list[i].text

    def test_get_todo_list_user_not_found_raises_exception(self, db_session):
        todo_db = ToDoDb(db_session=db_session)

        assert todo_db.get_todo_list(1)['status'] == False
