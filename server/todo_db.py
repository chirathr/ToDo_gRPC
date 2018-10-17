import sqlite3
from protobuf.todo_pb2 import User, ToDo

class ToDoDb:

    def __init__(self):
        self.conn = sqlite3.connect('todo.sqlite3')
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute(
            '''create table if not exists user(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT
               );'''
        )
        self.cursor.execute(
            '''create table if not exists todo(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    todo_text TEXT,
                    is_done BOOL,
                    FOREIGN KEY(user_id) REFERENCES user(id)
                );'''
        )

    def get_user(self, user):
        if not isinstance(user, User):
            raise AttributeError('user should be an instance of protobuf.todo_pb2.User')

        get_user_sql = 'select * from user where name = "{name}";'.format(name=user.name)

        # Get user
        self.cursor.execute(get_user_sql)
        user_row = self.cursor.fetchone()

        # If no user is found return None
        if user_row is None:
            return None

        # Return the user
        return User(id=int(user_row[0]), name=str(user_row[1]))



    def add_user_if_not_exist(self, new_user):
        if not isinstance(new_user, User):
            raise AttributeError('user should be an instance of protobuf.todo_pb2.User')

        # Check user exists, then return the existing user
        user = self.get_user(new_user)
        if user is not None:
            return user

        # Add user to db
        create_user_sql = 'insert into user (name) values("{name}");'.format(name=new_user.name)
        self.cursor.execute(create_user_sql)
        self.conn.commit()

        # Get the new user
        return self.get_user(new_user)



    def __del__(self):
        self.conn.close()
