import grpc

from protobuf.todo_pb2_grpc import TodoServiceStub
from protobuf.todo_pb2 import User, ToDo, FAILED, SUCCESS


class ClientStub:
    def __init__(self, stub=None):
        self.channel = grpc.insecure_channel('localhost:50001')
        self.stub = stub or TodoServiceStub(channel=self.channel)
        self.todo_list = []

    @staticmethod
    def _is_valid_id(int_id, name="id"):
        if not (isinstance(int_id, int) and int_id > 0):
            raise ValueError('{0} should be a valid int'.format(name))
        return True

    def add_user(self, user_name):
        user = User(name=str(user_name))
        user_response = self.stub.AddUser(user)
        if user_response.status == SUCCESS:
            return user_response
        return None

    def add_todo(self, user_id, todo_text):
        self._is_valid_id(user_id, 'user_id')

        todo = ToDo(user=User(id=user_id), text=str(todo_text))
        todo_response = self.stub.AddToDo(todo)
        if todo_response.status == SUCCESS:
            return todo_response
        return None

    def get_todo_list(self, user_id):
        self._is_valid_id(user_id, 'user_id')

        user = User(id=user_id)
        todo_list = self.stub.GetToDoList(user)
        todo_item_list = []
        for todo in todo_list:
            if todo.status != FAILED:
                todo_item_list.append(todo)
        return todo_item_list

    def update_todo(self, todo_id, is_done=False, delete=False):
        self._is_valid_id(todo_id, 'todo_id')

        if is_done and delete:
            raise ValueError('Both is_done and delete cannot be true together')

        if delete:
            todo_response = self.stub.UpdateToDo(ToDo(id=todo_id))
        if is_done:
            todo = ToDo(id=todo_id, is_done=is_done)
            todo_response = self.stub.UpdateToDo(todo)
        return todo_response.status == SUCCESS

    def __del__(self):
        self.channel.close()
