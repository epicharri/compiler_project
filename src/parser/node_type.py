from enum import Enum

class NodeType(Enum):
    PROGRAM = "program"
    READ = "read"
    IDENTIFIER = "identifier"
    VARIABLE_DECLARATION = "variable declaration"
    VARIABLE_ASSIGN = "variable assign"
    PRINT = "print"
    ASSERT = "assert"
    FOR_LOOP = "for loop"
    IF = "if"
    BINARY_OPERATION = "binary operation"
    UNARY_OPERATION = "unary operation"
    INTEGER_LITERAL = "integer literal"
    STRING_LITERAL = "string literal"

