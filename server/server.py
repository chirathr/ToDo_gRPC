from protobuf import todo_pb2_grpc
from server.server_util_lib.main import ServerUtils


class ToDoServicer(todo_pb2_grpc.TodoServiceServicer):
    """
    Methods that implement the functionality of the ToDo server
    """

    def AddUser(self, request, context):
        return ServerUtils().add_user(request)

    def AddToDo(self, request, context):
        return ServerUtils().add_todo(request)

    def UpdateToDo(self, request, context):
        return ServerUtils().update_todo(request)

    def GetToDoList(self, request, context):
        todo_list = ServerUtils().get_todo_list(request)
        for todo in todo_list:
            yield todo

    def delete_todo_list(self, user, context):
        # TODO: Complete delete_todo_list()
        pass
