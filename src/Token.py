from enum import Enum, auto

class TokenType(Enum):
    NUMBER = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULUS = auto()
    POWER = auto()
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    COMMA = auto()
    COLON = auto()
    ASSIGN = auto()
    SEMICOLON = auto()
    AT = auto()
    ARROW = auto()
    EQUALS = auto()
    NOT_EQUALS = auto()
    KEYWORD = auto()
    IDENTIFIER = auto()
    EOF = auto()

class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __repr__(self):
        if self.value:
            return f'Token({self.type}, {repr(self.value)})'
        return f'Token({self.type})'