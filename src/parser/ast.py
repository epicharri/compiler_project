from src.scanner.token import Token

class AST(object):
    pass

class ProgramAST(AST):
    def __init__(self):
        self.statements = []

class VariableDeclaration(AST):
    def __init__(self, left: AST, right: AST):
        
        pass

class BinaryOperation(AST):
    def __init__(self, left: AST, right: AST, operation_token: Token):
        self.left = left
        self.right = right
        self.operation = operation_token.type

class UnaryOperation(AST):
    def __init__(self, left: AST, operation_token: Token):
        self.left = left
        self.operation = operation_token.type

