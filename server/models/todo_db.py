import sqlite3


class ToDoDb:
    db_path = 'todo.sqlite3'

    def __init__(self, conn=None):
        self.conn = conn or sqlite3.connect(self.db_path)
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

    @staticmethod
    def is_valid_id(int_id, name="id"):
        if not (isinstance(int_id, int) and int_id > 0):
            raise ValueError('{0} should be a valid int'.format(name))

    def get_user(self, name):
        get_user_sql = 'select * from user where name = "{name}";'.format(name=name)

        # Get user
        self.cursor.execute(get_user_sql)
        user_row = self.cursor.fetchone()

        # If no user is found return None
        if user_row is None:
            return None

        # Return the user id
        return int(user_row[0])

    def add_user_if_not_exist(self, name):
        # Check user exists, then return the existing user
        user_id = self.get_user(name)
        if user_id is not None:
            return user_id

        # Add user to db
        create_user_sql = 'insert into user (name) values("{name}");'.format(name=name)
        self.cursor.execute(create_user_sql)
        user_id = self.cursor.lastrowid
        self.conn.commit()

        # Get the new user
        return user_id

    def add_todo(self, user_id, text):
        self.is_valid_id(user_id, 'user_id')

        create_todo_sql = '''
                    insert into todo (user_id, todo_text, is_done) values ({user_id}, "{text}", {is_done})
                '''.format(user_id=user_id, text=text, is_done=0)

        self.cursor.execute(create_todo_sql)
        todo_id = self.cursor.lastrowid
        self.conn.commit()
        return todo_id

    def update_todo(self, todo_id, user_id=None, is_done=False):
        self.is_valid_id(todo_id, 'todo_id')

        # Delete todo
        if user_id is None:
            delete_todo_sql = '''delete from todo where id = {id};'''.format(id=todo_id)
            self.cursor.execute(delete_todo_sql)
            self.conn.commit()
            return True

        if is_done:
            self.is_valid_id(user_id)
            update_todo_is_done = '''
                update todo set is_done = {is_done} where id = {id};
                '''.format(id=todo_id, is_done=True)
            self.cursor.execute(update_todo_is_done)
            self.conn.commit()
            return True
        return False

    def get_todo_list(self, user_id):
        self.is_valid_id(user_id, 'user_id')

        select_todo_sql = '''
            select * from todo where user_id = {user_id};
        '''.format(user_id=user_id)
        self.cursor.execute(select_todo_sql)
        return self.cursor.fetchall()

    def __del__(self):
        self.conn.close()
