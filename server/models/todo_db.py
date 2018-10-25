from server.models.models import User, ToDo, dal
from sqlalchemy.orm import exc


class ToDoDb:

    def __init__(self, db_session=None):
        if db_session:
            self.session = db_session
        else:
            dal.connect()
            dal.session = dal.Session()
            self.session = dal.session

    @staticmethod
    def is_valid_id(int_id):
        """Checks if id is a valid int

        Args:
            int_id(int): id that is to be validated

        Returns:
            bool: True if id is valid else false
        """
        return isinstance(int_id, int) and int_id > 0

    def get_user(self, name):
        """Gets a user from the database

        Args:
            name(str): The Name of the user

        Returns:
            return_value(dict): A dictionery with status and user(models.User)
        """
        return_value = {'status': False}
        if not name.strip():
            return return_value

        try:
            return_value["user"] = self.session.query(User).filter(User.id).one()
            return_value["status"] = True
        except exc.NoResultFound:
            return return_value

        # Return the user
        return return_value

    def add_user(self, name):
        """Adds and returns the user.

        Args:
            name(str): The Name of the user
        Returns:
            return_value(dict): A dictionery with status and user(models.User)
        """
        return_value = {'status': False}
        if not name.strip():
            return return_value

        # Check user exists, then return the existing user
        user_dict = self.get_user(name)
        if user_dict['status']:
            return user_dict

        # Add user to db
        user = User(name=name)
        self.session.add(user)
        self.session.commit()
        return_value['user'] = user
        return_value['status'] = True

        # Get the new user
        return return_value

    def add_todo(self, user_id, text):
        """Adds a user to the database if the user with `name` does not exist

        Args:
            user_id(int): user id of the user who added the ToDo
            text(str): The ToDo text
        Returns:
            return_value(dict): A dictionery with status and todo(models.ToDo)
        """
        return_value = {'status': False}
        if not text.strip():
            return return_value

        # Get the user
        try:
            user = self.session.query(User).filter(User.id == user_id).one()
        except exc.NoResultFound:
            return return_value

        # Add the todo
        todo = ToDo(text=text, user=user)
        self.session.add(todo)
        self.session.commit()

        return_value['todo'] = todo
        return_value['status'] = True

        return return_value

    def update_todo(self, todo_id, is_done=False):
        """Marks a todo as done, or deletes a todo

        Args:
            todo_id(int): Id of a todo
            is_done(bool): True marks the todo as done, False deletes the todo
        Returns:
            bool: True if todo is deleted or mark todo as done is successful.
        """
        if not self.is_valid_id(todo_id):
            return False

        if is_done:
            try:
                todo = self.session.query(ToDo).filter(ToDo.id == todo_id).one()
            except exc.NoResultFound:
                return False
            todo.is_done = True
            self.session.commit()
        else:
            # Delete todo
            try:
                todo = self.session.query(ToDo).filter(ToDo.id == todo_id).one()
            except exc.NoResultFound:
                return False

            self.session.delete(todo)
            self.session.commit()
        return True

    def get_todo_list(self, user_id):
        """Returns a list of todo objects

        Args:
            user_id(int): id of the user whose todo list is to be fetched from the db
        Returns:
            return_value(dict): A dictionery with status and a list of todo(models.ToDo)
        """
        return_value = {'status': False}
        if not self.is_valid_id(user_id):
            return return_value

        # Get the user
        try:
            user = self.session.query(User).filter(User.id == user_id).one()
        except exc.NoResultFound:
            return return_value

        return_value['todo_list'] = self.session.query(ToDo).filter(ToDo.user == user).all()
        return_value['status'] = True
        return return_value

    def __del__(self):
        self.session.close()
