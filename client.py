import grpc

from protobuf.todo_pb2 import User, ToDo
from protobuf import todo_pb2_grpc
from client.text_format import TextFormat


class Client:

    user = None

    def __init__(self):
        self.channel = grpc.insecure_channel('localhost:50001')
        self.stub = todo_pb2_grpc.TodoServiceStub(channel=self.channel)
        self.todo_list = []

    def __del__(self):
        self.channel.close()

    def load_user(self):
        name = input("Hi, Please enter name to continue: ")
        user = User(name=str(name))
        response_user = self.stub.add_user(user)
        if response_user.id != 0:
            self.user = response_user
            return True
        return False

    def add_todo(self):
        if not self.user:
            self.load_user()
        todo_text = input("Enter a todo: ")
        todo = ToDo(user=self.user, text=todo_text)
        response_todo = self.stub.add_todo(todo)
        if response_todo.id != 0:
            self.todo_list.append(response_todo)
            return True
        return False

    def load_todo_list(self):
        if not self.user:
            self.load_user()
        todo_list = self.stub.get_todo_list(self.user)
        self.todo_list = []
        for todo in todo_list:
            self.todo_list.append(todo)
        if len(self.todo_list) > 0:
            return True
        return False

    def mark_todo_as_done(self):
        try:
            todo_id = int(input('Enter todo number: '))
        except ValueError:
            print("Error: Wrong choice!")
            return self.mark_todo_as_done()

        todo = ToDo(id=todo_id, user=self.user, is_done=True)

        response_todo = self.stub.update_todo(todo)
        if response_todo.is_done:
            self.load_todo_list()
        return response_todo.is_done

    def delete_todo(self):
        try:
            todo_id = int(input('Enter todo number: '))
        except ValueError:
            print("Error: Wrong choice!")
            return self.delete_todo()

        todo = ToDo(id=todo_id)

        response_todo = self.stub.update_todo(todo)
        if response_todo.id == 0:
            return True
        return False

    @staticmethod
    def count_generator(generator):
        return sum(1 for _ in generator)

    def delete_all_todo(self):
        if not self.user:
            self.load_user()
        deleted_todo_list = self.stub.delete_todo_list(self.user)
        if len(self.todo_list) == self.count_generator(deleted_todo_list):
            return True
        return False

    def print_to_do_list(self):
        if not self.todo_list:
            return
        print('#-----------------------------------------------------------#')
        for todo in self.todo_list:
            if not todo.is_done:
                print(TextFormat.todo_text(todo))
        print('#---------------------- Completed --------------------------#')
        for todo in self.todo_list:
            if todo.is_done:
                print(TextFormat.todo_done_text(todo))
        print('#-----------------------------------------------------------#')


    @staticmethod
    def get_user_selection():
        print(' 1 -> Add    2 -> mark as done   3 -> delete todo    4-> Exit')
        print('#-----------------------------------------------------------#')
        try:
            user_input = int(input('Enter your option: '))
            if 1 > user_input > 4:
                raise ValueError
            return user_input
        except ValueError:
            return 0

    def run(self):
        print("Welcome to Todo application ")
        self.load_todo_list()

        while True:
            self.print_to_do_list()

            user_input = self.get_user_selection()
            print(user_input)

            if user_input == 1:
                self.add_todo()

            if user_input == 2:
                self.mark_todo_as_done()

            if user_input == 3:
                self.delete_todo()

            if user_input == 4:
                exit(0)

            if user_input == 0:
                print("Wrong option, Try again!")


if __name__ == '__main__':
    client = Client()
    client.run()
