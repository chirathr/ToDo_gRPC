from server.models import models


class TestModels:
    def test_user_object_name_id_name(self, db_session):
        user = models.User(name="Test user")
        db_session.add(user)
        db_session.commit()

        assert str(user) == '{0}. {1}'.format(1, "Test user")

    def test_todo_object_name_is_id_todo_text(self, db_session):
        todo = models.ToDo(text="Todo Text")
        db_session.add(todo)
        db_session.commit()

        assert str(todo) == '{0}. {1}'.format(1, "Todo Text")
