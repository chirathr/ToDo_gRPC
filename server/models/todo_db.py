import sqlite3
from server.models.models import create_db_tables, get_session, User, ToDo
from sqlalchemy import select, insert
from sqlalchemy.orm import exc

class ToDoDb:

    def __init__(self, db_path='todo.sqlite3'):
        create_db_tables(db_path)
        self.session = get_session(db_path)

    @staticmethod
    def is_valid_id(int_id, name="id"):
        if not (isinstance(int_id, int) and int_id > 0):
            raise ValueError('{0} should be a valid int'.format(name))

    def get_user(self, name):
        if not name.strip():
            raise ValueError('Name cannot be empty')

        select_user = select([User.id]).where(User.name == name)
        try:
            user_id = self.session.query(select_user).one()[0]
        except exc.NoResultFound:
            return None

        # Return the user id
        return user_id

    def add_user_if_not_exist(self, name):
        if not name.strip():
            raise ValueError('Name cannot be empty')

        # Check user exists, then return the existing user
        user_id = self.get_user(name)
        if user_id is not None:
            return user_id

        # Add user to db
        user = User(name=name)
        self.session.add(user)
        self.session.commit()

        # Get the new user
        return user.id

    def add_todo(self, user_id, text):
        if not text.strip():
            raise ValueError('Todo text cannot be empty')

        # Get the user
        try:
            user = self.session.query(User).filter(User.id == user_id).one()
        except exc.NoResultFound:
            return None

        # Add the todo
        todo = ToDo(text=text, user=user)
        self.session.add(todo)
        self.session.commit()

        return todo.id

    def update_todo(self, todo_id, user_id=None, is_done=False):
        self.is_valid_id(todo_id, 'todo_id')
        if user_id is not None:
            self.is_valid_id(user_id, 'user_id')

        # Delete todo
        if user_id is None:
            try:
                todo = self.session.query(ToDo).filter(ToDo.id == todo_id).one()
            except exc.NoResultFound:
                return False
            
            self.session.delete(todo)
            self.session.commit()
            return True

        if is_done:
            try:
                todo = self.session.query(ToDo).filter(ToDo.id == todo_id).one()
            except exc.NoResultFound:
                return False
            todo.is_done = True
            self.session.commit()
            return True
        return False

    def get_todo_list(self, user_id):
        self.is_valid_id(user_id, 'user_id')

        # Get the user
        try:
            user = self.session.query(User).filter(User.id == user_id).one()
        except exc.NoResultFound:
            raise ValueError("User not found")

        return self.session.query(ToDo).filter(ToDo.user == user).all()

    def __del__(self):
        self.session.close()
