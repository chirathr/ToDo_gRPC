import time
from concurrent import futures

import grpc

from protobuf import todo_pb2
from protobuf import todo_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class ToDoServicer(todo_pb2_grpc.TodoServiceServicer):
    """
    Methods that implement the functionality of the ToDo server
    """

    def AddUser(self, request, context):
        print(request.name)
        return todo_pb2.UserRequest(id=1)

    def DeleteUser(self, request, context):
        pass

    def AddToDo(self, request, context):
        pass

    def GetToDo(self, request, context):
        pass

    def SetDoneToDo(self, request, context):
        pass

    def DeleteToDo(self, request, context):
        pass

    def GetToDos(self, request, context):
        pass

    def DeleteToDo(self, request, context):
        pass


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    todo_pb2_grpc.add_TodoServiceServicer_to_server(ToDoServicer(), server)
    server.add_insecure_port('[::]:50001')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)



if __name__ == '__main__':
    serve()
