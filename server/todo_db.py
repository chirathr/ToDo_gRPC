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
        new_user.id = self.cursor.lastrowid
        self.conn.commit()

        # Get the new user
        return new_user

    def add_todo(self, todo):
        if not isinstance(todo, ToDo):
            raise AttributeError('todo should be an instance of protobuf.todo_pb2.ToDo')

        create_todo_sql = '''
            insert into todo (user_id, todo_text, is_done) values ({user_id}, "{text}", {is_done})
        '''.format(user_id=todo.user.id, text=todo.text, is_done=1 if todo.is_done else 0)

        self.cursor.execute(create_todo_sql)
        todo.id = self.cursor.lastrowid
        self.conn.commit()
        return todo

    def update_todo(self, todo):
        if not isinstance(todo, ToDo):
            raise AttributeError('todo should be an instance of protobuf.todo_pb2.ToDo')

        print("User: " + str(todo.user))

        if not todo.user:
            delete_todo_sql = '''delete from todo where id = {id};'''.format(id=todo.id)
            self.cursor.execute(delete_todo_sql)
            todo.id = 0

        if todo.is_done:
            update_todo_is_done = '''
                update todo set is_done = {is_done} where id = {id}
            '''.format(id=todo.id, is_done=1 if todo.is_done else 0)
            self.cursor.execute(update_todo_is_done)

        self.conn.commit()
        return todo

    def get_todo_list(self, user):
        if not isinstance(user, User):
            raise AttributeError('user should be an instance of protobuf.todo_pb2.User')
        select_todo_sql = '''
            select * from todo where user_id = {user_id};
        '''.format(user_id=user.id)
        self.cursor.execute(select_todo_sql)
        rows = self.cursor.fetchall()

        todo_list = []
        for row in rows:
            todo = ToDo(id=row[0], user=user, text=row[2], is_done=True if row[3] == 1 else False)
            todo_list.append(todo)
        return todo_list

    def __del__(self):
        self.conn.close()
