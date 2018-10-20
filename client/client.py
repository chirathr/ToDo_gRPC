from protobuf.todo_pb2 import User
from client.text_format import TextFormat
from client.client_util_lib.client_stub import ClientStub
from client.client_util_lib import string_constants


class Client:

    def __init__(self, client_stub=None, user=None):
        self.todo_list = []
        self.client_stub = client_stub or ClientStub()
        if isinstance(user, User):
            self.user = user
        else:
            self.user = None

    def load_user(self, user_name=None):
        user_name = user_name or input(string_constants.ENTER_NAME)
        user = self.client_stub.add_user(user_name)
        if user:
            self.user = user
        else:
            print(string_constants.ERROR_FAIL)
            exit(0)

    def add_todo(self, todo_text=None):
        if not self.user:
            self.load_user()
        todo_text = todo_text or input(string_constants.ERROR_TODO)
        todo = self.client_stub.add_todo(self.user.id, todo_text)
        if todo:
            self.todo_list.append(todo)
        else:
            print(string_constants.ERROR_FAILED_ADD_TODO)

    def load_todo_list(self):
        if not self.user:
            self.load_user()
        self.todo_list = self.client_stub.get_todo_list(self.user.id)

    def mark_todo_as_done(self, todo_id=None):
        if not isinstance(todo_id, int):
            todo_id = None
        try:
            todo_id = todo_id or int(input(string_constants.ENTER_TODO_NO))
        except ValueError:
            print(string_constants.ERROR_WRONG_CHOICE)
            return self.mark_todo_as_done()

        if not self.client_stub.update_todo(todo_id, self.user.id, is_done=True):
            print(string_constants.ERROR_FAILED_TO_MARK_TODO.format(todo_id))

    def delete_todo(self, todo_id=None):
        if not isinstance(todo_id, int):
            todo_id = None

        try:
            todo_id = todo_id or int(input(string_constants.ENTER_TODO_NO))
        except ValueError:
            print(string_constants.ERROR_WRONG_CHOICE)
            return self.delete_todo()

        if not self.client_stub.update_todo(todo_id=todo_id, delete=True):
            print(string_constants.ERROR_FAILED_DELETE_TODO.format(todo_id))

    @staticmethod
    def count_generator(generator):
        return sum(1 for _ in generator)

    def delete_all_todo(self):
        if not self.user:
            self.load_user()
        deleted_todo_list = self.client_stub.delete_all_todo(self.user.id)
        if len(self.todo_list) == self.count_generator(deleted_todo_list):
            return True
        return False

    def print_to_do_list(self):

        print(string_constants.SEPARATOR)
        if not self.todo_list:
            print(string_constants.EMPTY_TODO_LIST)
        else:
            for todo in self.todo_list:
                if not todo.is_done:
                    print(TextFormat.todo_text(todo))
            print(string_constants.SEPARATOR_COMPLETED)
            for todo in self.todo_list:
                if todo.is_done:
                    print(TextFormat.todo_done_text(todo))
        print(string_constants.SEPARATOR)

    @staticmethod
    def get_user_selection(option=None):

        if not isinstance(option, int):
            option = None

        print(string_constants.CHOICES)
        print(string_constants.SEPARATOR)
        try:
            user_input = option or int(input(string_constants.ENTER_OPTION))
            if 1 > user_input > 4:
                raise ValueError
            return user_input
        except ValueError:
            return 0

    def run(self):
        print(string_constants.WELCOME_MESSAGE)

        while True:
            self.load_todo_list()
            self.print_to_do_list()

            user_input = self.get_user_selection()

            if user_input == 1:
                self.add_todo()

            if user_input == 2:
                self.mark_todo_as_done()

            if user_input == 3:
                self.delete_todo()

            if user_input == 4:
                exit(0)

            if user_input == 0:
                print(string_constants.ERROR_WRONG_CHOICE)
