from src.scanner.token import Token
import datetime;
  

class AST(object):
    def __init__(self):
        self.id = self.get_id()
        self.parent_id = None

    def set_parent_id(self, parent_id):
        self.parent_id = parent_id

    def get_id(self):
        current_time = datetime.datetime.now()
        time_stamp = current_time.timestamp()
        return time_stamp

class ProgramNode(AST):
    def __init__(self):
        super().__init__()
        self.statements = []

    def append_statement(self, statement: AST):
        if isinstance(statement, AST):
            statement.set_parent_id(self.id)
        self.statements.append(statement)

    def __repr__(self):
        return str(self.statements)

class ReadNode(AST):
    def __init__(self, read_keyword_token: Token, identifier_token: Token):
        super().__init__()
        self.read_keyword_token = read_keyword_token
        self.identifier_token = identifier_token
    
    def __repr__(self):
        return f"READ NODE: id: {self.id}. parent_id: {self.parent_id}. KEYWORD: {self.read_keyword_token}, IDENTIFIER: {self.identifier_token}"
    
    def is_read_node(self):
        return True

class IdentifierNode(AST):
    def __init__(self, identifier_token: Token):
        super().__init__()
        self.identifier_token = identifier_token

    def __repr__(self):
        return f"IDENTIFIER NODE: id: {self.id}. parent_id: {self.parent_id}. {self.identifier_token}"

    def is_identifier_node(self):
        return True

class VariableDeclarationNode(AST):
    def __init__(self, identifier_token: Token, variable_type_token: Token, variable_assignment_expression_root: AST = None):
        super().__init__()
        self.identifier_token = identifier_token
        self.variable_type_token = variable_type_token
        self.variable_assignment_expression_root = variable_assignment_expression_root

    def __repr__(self):
        return f"VARIABLE DECLARATION NODE: id: {self.id}. parent_id: {self.parent_id}. Identifier: {self.identifier_token}. Expression root node: {self.variable_assignment_expression_root}"


class VariableAssignNode(AST):
    def __init__(self, identifier_token: Token, expression_root: AST = None):
        super().__init__()
        self.identifier_token = identifier_token
        self.expression_root = expression_root

    def __repr__(self):
        return f"VARIABLE ASSIGN NODE: id: {self.id}. parent_id: {self.parent_id}. Identifier: {self.identifier_token}. Expression root node: {self.expression_root}"

    def add_expression_node(self, expression_root: AST):
        if isinstance(expression_root, AST):
            expression_root.set_parent_id(self.id)
        self.expression_root = expression_root
        
class ForLoopNode(AST):
    def __init__(self, variable_declaration: AST, for_constant_start_expression: AST, for_constant_end_expression: AST, for_token: Token, end_for_token: Token = None):
        super().__init__()
        self.for_token = for_token
        self.end_for_token = end_for_token
        self.for_constant = variable_declaration # AST
        self.for_constant_start_expression = for_constant_start_expression # AST
        self.for_constant_end_expression = for_constant_end_expression # AST
        self.statements = []
    
    def set_end_for_token(self, end_for_token: Token):
        self.end_for_token = end_for_token
    
    def add_statement(self, statement: AST):
        if isinstance(statement, AST):
            statement.set_parent_id(self.id)
        self.statements.append(statement)



class BinaryOperationNode(AST):
    def __init__(self, operation_token: Token, left: Token = None, right: Token = None):
        super().__init__()
        self.left = left
        self.right = right
        if isinstance(left, AST):
            self.left.set_parent_id(self.id)
        if isinstance(right, AST):
            self.right.set_parent_id(self.id)
        self.operation_token = operation_token

    def __repr__(self):
        left = self.left
        right = self.right
        if not left:
            left = "None"
        if not right:
            right = "None"
        return f"BINARY OPERATION NODE: id: {self.id}. parent_id: {self.parent_id}. Operation: {self.operation_token}. LEFT: {left}. RIGHT: {right}"

    def add_left_and_right_child(self, left: AST, right: AST):
        if isinstance(left, AST):
            left.set_parent_id(self.id)
        if isinstance(right, AST):
            right.set_parent_id(self.id)
        self.left = left
        self.right = right

class UnaryOperationNode(AST):
    def __init__(self, operation_token: Token, left: AST):
        super().__init__()
        self.left = left
        if isinstance(self.left, AST):
            self.left.set_parent_id(self.id)
        self.operation_token = operation_token

    def __repr__(self):
        return f"UNARY OPERATION NODE: id: {self.id}. parent_id: {self.parent_id}. {self.operation_token}. Left: {self.left}."



class IntegerNode(AST):
    def __init__(self, literal_token: Token):
        super().__init__()
        self.literal_token = literal_token
        self.value = 0
        if Token.to_int(literal_token.lexeme):
            self.value = Token.to_int(literal_token.lexeme)
        else:
            print("The literal token '{literal_token.lexeme}' in line {literal_token.line_start} should be integer but is not.")

    def __repr__(self):
        return f"INTEGER NODE: id: {self.id}. parent_id: {self.parent_id}. {self.literal_token}. VALUE: {self.value}."


class StringNode(AST):
    def __init__(self, literal_token: Token):      
        super().__init__()
        self.literal_token = literal_token
        self.value = literal_token.lexeme

    def __repr__(self):
        return f"STRING NODE: id: {self.id}. parent_id: {self.parent_id}. {self.literal_token}. VALUE: {self.value}."


class BoolNode(AST):
    pass

