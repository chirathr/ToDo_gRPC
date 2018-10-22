# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: todo.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='todo.proto',
  package='protobuf',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\ntodo.proto\x12\x08protobuf\"F\n\x04User\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\x12$\n\x06status\x18\x03 \x01(\x0e\x32\x14.protobuf.StatusType\"u\n\x04ToDo\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x1c\n\x04user\x18\x02 \x01(\x0b\x32\x0e.protobuf.User\x12\x0c\n\x04text\x18\x03 \x01(\t\x12\x0f\n\x07is_done\x18\x04 \x01(\x08\x12$\n\x06status\x18\x05 \x01(\x0e\x32\x14.protobuf.StatusType*%\n\nStatusType\x12\n\n\x06\x46\x41ILED\x10\x00\x12\x0b\n\x07SUCCESS\x10\x01\x32\xca\x01\n\x0bTodoService\x12+\n\x07\x41\x64\x64User\x12\x0e.protobuf.User\x1a\x0e.protobuf.User\"\x00\x12+\n\x07\x41\x64\x64ToDo\x12\x0e.protobuf.ToDo\x1a\x0e.protobuf.ToDo\"\x00\x12.\n\nUpdateToDo\x12\x0e.protobuf.ToDo\x1a\x0e.protobuf.ToDo\"\x00\x12\x31\n\x0bGetToDoList\x12\x0e.protobuf.User\x1a\x0e.protobuf.ToDo\"\x00\x30\x01\x62\x06proto3')
)

_STATUSTYPE = _descriptor.EnumDescriptor(
  name='StatusType',
  full_name='protobuf.StatusType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='FAILED', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SUCCESS', index=1, number=1,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=215,
  serialized_end=252,
)
_sym_db.RegisterEnumDescriptor(_STATUSTYPE)

StatusType = enum_type_wrapper.EnumTypeWrapper(_STATUSTYPE)
FAILED = 0
SUCCESS = 1



_USER = _descriptor.Descriptor(
  name='User',
  full_name='protobuf.User',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='protobuf.User.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='protobuf.User.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='status', full_name='protobuf.User.status', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=24,
  serialized_end=94,
)


_TODO = _descriptor.Descriptor(
  name='ToDo',
  full_name='protobuf.ToDo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='protobuf.ToDo.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='user', full_name='protobuf.ToDo.user', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='text', full_name='protobuf.ToDo.text', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='is_done', full_name='protobuf.ToDo.is_done', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='status', full_name='protobuf.ToDo.status', index=4,
      number=5, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=96,
  serialized_end=213,
)

_USER.fields_by_name['status'].enum_type = _STATUSTYPE
_TODO.fields_by_name['user'].message_type = _USER
_TODO.fields_by_name['status'].enum_type = _STATUSTYPE
DESCRIPTOR.message_types_by_name['User'] = _USER
DESCRIPTOR.message_types_by_name['ToDo'] = _TODO
DESCRIPTOR.enum_types_by_name['StatusType'] = _STATUSTYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

User = _reflection.GeneratedProtocolMessageType('User', (_message.Message,), dict(
  DESCRIPTOR = _USER,
  __module__ = 'todo_pb2'
  # @@protoc_insertion_point(class_scope:protobuf.User)
  ))
_sym_db.RegisterMessage(User)

ToDo = _reflection.GeneratedProtocolMessageType('ToDo', (_message.Message,), dict(
  DESCRIPTOR = _TODO,
  __module__ = 'todo_pb2'
  # @@protoc_insertion_point(class_scope:protobuf.ToDo)
  ))
_sym_db.RegisterMessage(ToDo)



_TODOSERVICE = _descriptor.ServiceDescriptor(
  name='TodoService',
  full_name='protobuf.TodoService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=255,
  serialized_end=457,
  methods=[
  _descriptor.MethodDescriptor(
    name='AddUser',
    full_name='protobuf.TodoService.AddUser',
    index=0,
    containing_service=None,
    input_type=_USER,
    output_type=_USER,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='AddToDo',
    full_name='protobuf.TodoService.AddToDo',
    index=1,
    containing_service=None,
    input_type=_TODO,
    output_type=_TODO,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='UpdateToDo',
    full_name='protobuf.TodoService.UpdateToDo',
    index=2,
    containing_service=None,
    input_type=_TODO,
    output_type=_TODO,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='GetToDoList',
    full_name='protobuf.TodoService.GetToDoList',
    index=3,
    containing_service=None,
    input_type=_USER,
    output_type=_TODO,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_TODOSERVICE)

DESCRIPTOR.services_by_name['TodoService'] = _TODOSERVICE

# @@protoc_insertion_point(module_scope)
