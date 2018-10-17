import grpc

from protobuf import todo_pb2
from protobuf import todo_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50001') as channel:
        stub = todo_pb2_grpc.TodoServiceStub(channel)
        user = todo_pb2.User(name="Chirath")
        print(user)
        user_request = stub.AddUser(user)
        print(user_request.id)


if __name__ == '__main__':
    run()
