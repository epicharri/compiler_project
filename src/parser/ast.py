from src.scanner.token import Token

class AST(object):
    pass

class ProgramAST(AST):
    def __init__(self):
        self.statements = []

class VariableDeclaration(AST):
    def __init__(self, expression: AST, variable_symbol_token: Token):
        self.expression = expression
        self.variable_symbol_token = variable_symbol_token
        

class BinaryOperation(AST):
    def __init__(self, left: AST, right: AST, operation_token: Token):
        self.left = left
        self.right = right
        self.operation_token = operation_token

class UnaryOperation(AST):
    def __init__(self, left: AST, operation_token: Token):
        self.left = left
        self.token = operation_token

