from protobuf.todo_pb2 import ToDo


class TextFormat:
    _escape_code_format_str = '\x1b[{text_format};{text_color};{background_color}m'
    _escape_code_end = '\x1b[0m'
    _string_format = '{escape_code_style}{text:50s}{escape_code_end}'

    # Text formating
    _BOLD = 1
    _FAINT = 2
    _UNDERLINE = 4

    # Text color
    _TC_BLACK = 30
    _TC_RED = 31
    _TC_GREEN = 32
    _TC_YELLOW = 33
    _TC_WHITE = 37

    # Background color
    _BC_BLACK = 40
    _BC_GREEN = 42
    _BC_BLUE = 44
    _BC_YELLOW = 43
    _BC_WHITE = 47

    @classmethod
    def green_check(cls):
        check = u'\u2713'
        return '\x1b[1;32;m' + check + cls._escape_code_end

    @classmethod
    def format_text(cls, text, text_format=0, text_color=37, background_color=""):

        escape_code_style = cls._escape_code_format_str.format(
            text_format=text_format,
            text_color=text_color,
            background_color=background_color
        )
        return cls._string_format.format(
            escape_code_style=escape_code_style,
            text=text,
            escape_code_end=cls._escape_code_end
        )

    @classmethod
    def todo_text(cls, todo):
        if not isinstance(todo, ToDo):
            raise ValueError("todo should be an instance of ToDo")
        return " {0}. {1}".format(todo.id, cls.format_text(todo.text, text_format=cls._BOLD))

    @classmethod
    def todo_done_text(cls, todo):
        if not isinstance(todo, ToDo):
            raise ValueError("todo should be an instance of ToDo")
        text = cls.format_text(todo.text, text_format=cls._FAINT)
        return " {0}. {1:<63}".format(todo.id, text[:50]) + cls.green_check()
