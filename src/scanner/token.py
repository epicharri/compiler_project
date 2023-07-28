from typing import TypeVar, Type
T = TypeVar('T', bound='Token')

class Token:
    def __init__(self, type, lexeme, start, end, error_message = None):
        self.type = type # e.g. add, mul
        self.lexeme = lexeme # lexeme
        self.start = start # [start, end)
        self.end = end # [start, end)
        self.line_start = 0
        self.error_message = error_message
        # self.line_end = 0 # In tokens, always line_start == line_end.
    
    def __eq__(self, other):
        return (self.type == other.type) and (self.lexeme == other.lexeme)

    def __repr__(self):
        error_message = ""
        if self.error_message:
            error_message = ", Error message: " + self.error_message
        return f"Token: Type = '{self.type}', Lexeme = '{self.lexeme}',  Start character index = '{self.start}', End character index = '{self.end}', Line = {self.line_start}{error_message}"
    
    @classmethod
    def create_assignment_token(cls: Type[T], start: int, end: int) -> T:
        return cls('ASSIGN', ':=', start, end)

    def is_assignment_token(self) -> bool:
        return self.type == 'ASSIGN'

    @classmethod
    def create_colon_token(cls: Type[T], start: int, end: int) -> T:
        return cls('COLON', ':', start, end)

    def is_colon_token(self) -> bool:
        return self.type == 'COLON'

    @classmethod
    def create_eos_token(cls: Type[T], start: int, end: int) -> T:
        return cls('EOS', ';', start, end)

    def is_eos_token(self) -> bool:
        return self.type == 'EOS'

    @classmethod
    def lexeme_is_eos(cls, lexeme: str) -> bool:
        return lexeme == ';'

    @classmethod
    def create_range_separator_token(cls: Type[T], start: int, end: int) -> T:
        return cls('RANGE SEPARATOR', '..', start, end)

    def is_range_separator_token(self) -> bool:
        return self.type == 'RANGE SEPARATOR'

    @classmethod
    def create_eof_token(cls: Type[T], start: int, end: int) -> T:
        return cls('EOF', 'EOF', start, end)

    def is_eof_token(self) -> bool:
        return self.type == 'EOF'

    @classmethod
    def create_error_token(cls: Type[T], lexeme: str, error_message: str, start: int, end: int) -> T:
        return cls('ERROR', lexeme, start, end, error_message)

    def is_error_token(self) -> bool:
        return self.type == 'ERROR'

    @classmethod
    def create_identifier_token(cls: Type[T], lexeme: str, start: int, end: int) -> T:
        return cls('IDENTIFIER', lexeme, start, end)

    def is_identifier_token(self) -> bool:
        return self.type == 'IDENTIFIER'

    @classmethod
    def lexeme_is_keyword(cls, identifier: str) -> bool:
        return identifier in ['var', 'for', 'end', 'in', 'do', 'read', 'print', 'int', 'string', 'bool', 'assert', 'if', 'else']

    @classmethod
    def create_keyword_token(cls: Type[T], lexeme: str, start: int, end: int) -> T:
        return cls('KEYWORD', lexeme, start, end)

    def is_keyword_token(self) -> bool:
        return self.type == 'KEYWORD'
    
    def is_var_token(self) -> bool:
        return self.type == 'KEYWORD' and self.lexeme == 'var'

    def is_for_token(self) -> bool:
        return self.type == 'KEYWORD' and self.lexeme == 'for'
    
    def is_end_token(self) -> bool:
        return self.type == 'KEYWORD' and self.lexeme == 'end'

    def is_in_token(self) -> bool:
        return self.type == 'KEYWORD' and self.lexeme == 'in'

    def is_do_token(self) -> bool:
        return self.type == 'KEYWORD' and self.lexeme == 'do'

    def is_read_token(self) -> bool:
        return self.type == 'KEYWORD' and self.lexeme == 'read'

    def is_print_token(self) -> bool:
        return self.type == 'KEYWORD' and self.lexeme == 'print'

    def is_assert_token(self) -> bool:
        return self.type == 'KEYWORD' and self.lexeme == 'assert'

    def is_if_token(self) -> bool:
        return self.type == 'KEYWORD' and self.lexeme == 'if'

    def is_else_token(self) -> bool:
        return self.type == 'KEYWORD' and self.lexeme == 'else'

    @classmethod
    def lexeme_is_variable_type(cls, identifier: str) -> bool:
        return identifier in ['int', 'string', 'bool']

    @classmethod
    def create_variable_type_token(cls: Type[T], lexeme: str, start: int, end: int) -> T:
        return cls('VARIABLE TYPE', lexeme, start, end)

    def is_variable_type_token(self) -> bool:
        return self.type == 'VARIABLE TYPE'
    
    def is_int_token(self) -> bool:
        return self.type == 'VARIABLE TYPE' and self.lexeme == 'int'

    def is_string_token(self) -> bool:
        return self.type == 'VARIABLE TYPE' and self.lexeme == 'string'
    
    def is_bool_token(self) -> bool:
        return self.type == 'VARIABLE TYPE' and self.lexeme == 'bool'
    
    @classmethod
    def lexeme_is_operator(cls, lexeme: str) -> bool:
        return lexeme in ['+', '-', '*', '/', '&', '!', '=', '<']

    @classmethod
    def create_operator_token(cls: Type[T], lexeme: str, start: int, end: int) -> T:
        operator_types = {'+': 'PLUS', '-': 'SUB', '*': 'MUL', '/': 'DIV', '&': 'AND', '!': 'NOT', '=': 'EQUAL', '<': 'SMALLER'}
        return cls(operator_types[lexeme], lexeme, start, end)
    
    def is_operator_token(self) -> bool:
        return self.type in {'PLUS': '+', 'SUB': '-', 'MUL': '*', 'DIV': '/', 'AND': '&', 'NOT': '!', 'EQUAL': "=", 'SMALLER': '<'}.keys()
    
    def is_multiplicative_operator(self) -> bool: # *, /, &
        return self.type in {'MUL': '*', 'DIV': '/', 'AND': '&'}.keys()

    def is_additive_operator(self) -> bool: # +, -, =, <
        return self.type in {'PLUS': '+', 'SUB': '-', 'EQUAL': "=", 'SMALLER': '<'}.keys()

    def is_binary_operator(self) -> bool:
        return self.is_operator_token() and self.type != 'NOT'

    def is_unary_operator(self) -> bool:
        return self.is_operator_token() and self.type == 'NOT'
    
    @classmethod
    def lexeme_is_parenthesis(cls, lexeme: str) -> bool:
        return lexeme in ['(', ')']
    
    @classmethod
    def create_parenthesis_token(cls: Type[T], lexeme: str, start: int, end: int) -> T:
        types = {'(': 'LEFT PARENTHESIS', ')': 'RIGHT PARENTHESIS'}
        return cls(types[lexeme], lexeme, start, end)
    
    def is_parenthesis(self) -> bool:
        return self.lexeme in ['(', ')']
    
    def is_left_parenthesis(self) -> bool:
        return self.type == 'LEFT PARENTHESIS'
    
    def is_right_parenthesis(self) -> bool:
        return self.type == 'RIGHT PARENTHESIS'

    @classmethod
    def create_string_literal_token(cls: Type[T], lexeme: str, start: int, end: int) -> T:
        return cls('STRING LITERAL', lexeme, start, end)

    def is_string_literal(self) -> bool:
        return self.type == 'STRING LITERAL'
    
    @classmethod
    def to_int(cls, literal: str): # Returns None, if not possible
        try:
            return int(literal)
        except ValueError:
            return None

    @classmethod
    def create_integer_literal_token(cls: Type[T], lexeme: str, start: int, end: int) -> T:
        return cls('INTEGER LITERAL', lexeme, start, end)

    def is_integer_literal(self) -> bool:
        return self.type == 'INTEGER LITERAL' and self.to_int(self.lexeme) != None
    