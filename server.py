from concurrent import futures

import grpc

import protobuf.todo_pb2
import protobuf.todo_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class ToDoServicer(todo_pb2_grpc.TodoServiceServicer):

    def AddUser(self, request, context):
        pass

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
    server = grpc.server(futures.ThreadPoolExecutor(max_servers=10))
    todo_pb2_grpc.add_TodoServiceServicer_to_server(TodoServicer(), server)
    server.add_insecure_port('[::]:50001')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
        except KeyboardInterrupt:
            server.stop()



if __name__ == '__main__':
    serve()
