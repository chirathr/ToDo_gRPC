### ToDo

A ToDo CLI program that uses gRPC to communicate between client and server.

To generate the protocol buffer and gRPC client classes execute the command from inside the `protobuf/` directory:

```bash
python -m grpc_tools.protoc -I./  --python_out=. --grpc_python_out=. todo.proto
```

To run the program, execute the server script.

```bash
python server.py
```

Then run the client script in a new terminal.

```bash
python client.py
```
