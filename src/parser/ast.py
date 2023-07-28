from src.scanner.token import Token
import datetime;
from src.parser.node_type import NodeType



class AST(object):
    def __init__(self):
        self.id = self.get_id()
        self.parent_id = None
        self.node_type = None
        
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
        self.node_type = NodeType.PROGRAM
        

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
        self.node_type = NodeType.READ
    
    def __repr__(self):
        return f"READ NODE: id: {self.id}. parent_id: {self.parent_id}. KEYWORD: {self.read_keyword_token}, IDENTIFIER: {self.identifier_token}"
    

class IdentifierNode(AST):
    def __init__(self, identifier_token: Token):
        super().__init__()
        self.identifier_token = identifier_token
        self.node_type = NodeType.READ

    def __repr__(self):
        return f"IDENTIFIER NODE: id: {self.id}. parent_id: {self.parent_id}. {self.identifier_token}"


class VariableDeclarationNode(AST):
    def __init__(self, identifier_token: Token, variable_type_token: Token, variable_assignment_expression_root: AST = None):
        super().__init__()
        self.identifier_token = identifier_token
        self.variable_type_token = variable_type_token
        self.variable_assignment_expression_root = variable_assignment_expression_root
        self.node_type = NodeType.VARIABLE_DECLARATION

    def __repr__(self):
        return f"VARIABLE DECLARATION NODE: id: {self.id}. parent_id: {self.parent_id}. Identifier: {self.identifier_token}. Expression root node: {self.variable_assignment_expression_root}"


class VariableAssignNode(AST):
    def __init__(self, identifier_token: Token, expression_root: AST = None):
        super().__init__()
        self.identifier_token = identifier_token
        self.expression_root = expression_root
        self.node_type = NodeType.VARIABLE_ASSIGN

    def __repr__(self):
        return f"VARIABLE ASSIGN NODE: id: {self.id}. parent_id: {self.parent_id}. Identifier: {self.identifier_token}. Expression root node: {self.expression_root}"

    def add_expression_node(self, expression_root: AST):
        if isinstance(expression_root, AST):
            expression_root.set_parent_id(self.id)
        self.expression_root = expression_root

class PrintNode(AST):
    def __init__(self, print_keyword_token: Token, expression_root: AST = None):
        super().__init__()
        self.print_keyword_token = print_keyword_token
        self.expression_root = expression_root
        if isinstance(self.expression_root, AST):
            self.expression_root.set_parent_id(self.id)
        self.node_type = NodeType.PRINT
    
    def __repr__(self):
        return f"PRINT NODE: id: {self.id}. parent_id: {self.parent_id}. Print keyword: {self.print_keyword_token}. Expression root node: {self.expression_root}"    
 
class AssertNode(AST):
    def __init__(self, assert_keyword_token: Token, expression_root: AST = None):
        super().__init__()
        self.assert_keyword_token = assert_keyword_token
        self.expression_root = expression_root
        if isinstance(self.expression_root, AST):
            self.expression_root.set_parent_id(self.id)
        self.node_type = NodeType.ASSERT
    
    def __repr__(self):
        return f"ASSERT NODE: id: {self.id}. parent_id: {self.parent_id}. Assert keyword: {self.assert_keyword_token}. Expression root node: {self.expression_root}"    


class ForLoopNode(AST):
    def __init__(self, control_variable_token: Token, range_start_expression_node: AST, range_end_expression_node: AST, for_keyword_token: Token, end_keyword_token: Token = None): # end_token: end keyword token
        super().__init__()
        self.control_variable_token = control_variable_token
        self.for_keyword_token = for_keyword_token
        self.end_keyword_token = end_keyword_token
        self.range_start_expression_node = range_start_expression_node # AST
        self.range_end_expression_node = range_end_expression_node # AST
        self.statements = []
        self.node_type = NodeType.FOR_LOOP

    def __repr__(self):
        return f"FOR LOOP NODE: id: {self.id}. parent_id: {self.parent_id}. For keyword token: {self.for_keyword_token}. End keyword token: {self.end_keyword_token}. For loop variable token: {self.for_loop_variable_token}. Range start expression node: {self.range_start_expression_node}. Range end expression node: {self.range_end_expression_node}."

    def set_end_keyword_token(self, end_for_token: Token):
        self.end_for_token = end_for_token
    
    def add_statement(self, statement: AST):
        if isinstance(statement, AST):
            statement.set_parent_id(self.id)
        self.statements.append(statement)

class IfNode(AST):
    def __init__(self, if_token: Token, expression_token: Token, else_token: Token = None, end_token: Token = None, expression_node: AST = None):
        super().__init__()
        self.if_token = if_token
        self.else_token = else_token
        self.end_token = end_token # end_token, not if token after end token
        self.expression_token = expression_token
        self.expression_node = None # If expression is true, then statements, otherwise else_statements.
        self.add_expression_node(expression_node) 
        self.statements = []
        self.else_statements = []
        self.node_type = NodeType.IF

    def __repr__(self):
        else_keyword_printout = "No else block."
        else_statements_printout = ""
        if self.else_token:
            else_keyword_printout = f"Else keyword token: {self.else_token}"
            else_statements_printout = f"{self.else_statements}"
        return f"IF NODE: id: {self.id}. parent_id: {self.parent_id}. If keyword token: {self.if_token}. {else_keyword_printout}. End keyword token: {self.end_token}. If condition expression node: {self.expression_node}. Statements if condition is true: {self.statements}. {else_statements_printout}"

    def add_end_token(self, end_token: Token):
        self.end_token = end_token

    def add_else_token(self, else_token: Token):
        self.else_token = else_token

    def add_expression_node(self, expression_node: AST):
        self.expression_node = expression_node
        if isinstance(self.expression_node, AST):
            self.expression_node.set_parent_id(self.id)

    def add_statement(self, statement: AST):
        if isinstance(statement, AST):
            statement.set_parent_id(self.id)
        self.statements.append(statement)

    def add_else_statement(self, statement: AST):
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
        self.node_type = NodeType.BINARY_OPERATION

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
        self.node_type = NodeType.UNARY_OPERATION

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
        self.node_type = NodeType.INTEGER_LITERAL

    def __repr__(self):
        return f"INTEGER NODE: id: {self.id}. parent_id: {self.parent_id}. {self.literal_token}. VALUE: {self.value}."


class StringNode(AST):
    def __init__(self, literal_token: Token):      
        super().__init__()
        self.literal_token = literal_token
        self.value = literal_token.lexeme
        self.nodetype = NodeType.STRING_LITERAL

    def __repr__(self):
        return f"STRING NODE: id: {self.id}. parent_id: {self.parent_id}. {self.literal_token}. VALUE: {self.value}."


class BoolNode(AST):
    pass

