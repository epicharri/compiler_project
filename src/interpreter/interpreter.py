from src.scanner.scanner import Scanner
from src.scanner.token import *
from src.parser.symbol_table import *
from src.parser.ast import *
from src.parser.parser import *
from src.parser.node_type import *
from src.io.read_and_print import ReadAndPrint

class Visitor:
    def __init__(self):
        self.errors_found = 0

    def if_errors_found(self):
        return self.errors_found > 0

    def visit(self, node):
        if self.if_errors_found():
            return
        if node == None:
            return
        class_name = node.__class__.__name__
        return getattr(self, 'visit_' + class_name)(node)

class Interpreter(Visitor):
    def __init__(self, parser):
        super().__init__()
        self.parser = parser
        self.symbol_table = parser.symbol_table
        self.running_after_semantic_analysis = False
    
    def in_semantic_analysis(self):
        return not self.running_after_semantic_analysis
    
    def in_execution(self):
        return self.running_after_semantic_analysis

    def interpret(self):
        ast = self.parser.parse_program()
        if self.parser.errors_found > 0:
          print("Since the program is not error free, it is not interpreted.")
          return False # Errors.
        if self.parser.scanner.parameters.print_ast:
            ast.pretty_print()
        if self.parser.scanner.parameters.print_symbol_table:
            print(f"\nSymbol table created by parser\n{self.parser.symbol_table.symbol_table}")

        self.visit(ast)
        if self.parser.scanner.parameters.print_symbol_table:
            print(f"Symbol table after semantic analysis\n{self.parser.symbol_table.symbol_table}")
        if self.errors_found > 0:
            print("The semantic analysis showed errors. The program is not executed.")
            return False
        
        self.running_after_semantic_analysis = True
        self.visit(ast)

        if self.errors_found > 0:
            print("The execution of the program is stopped.")
        if self.parser.scanner.parameters.print_symbol_table:
            print(f"Symbol table after execution\n{self.parser.symbol_table.symbol_table}")

    def raise_error(self, token: Token, msg: str):
        if token is not None:
            print(f"Error in line {token.line_start}: {msg}")
        else:
            print(f"Error: {msg}")
        self.errors_found += 1
        return None

    def value_is_correct(self, token: Token = None, value = None, msg: str = None):
        if value == None:
            return self.raise_error(token, msg)
        return True

    def to_mini_pl_type(self, value):
        if isinstance(value, int):
            return 'int'
        if isinstance(value, str):
            return 'string'
        if isinstance(value, bool):
            return 'bool'
        return None

    def to_int(self, value: str):
        try:
            int_value = int(value)
            return int_value
        except ValueError:
            return None

    def read_input(self, data_type: str):
        if self.in_semantic_analysis():
            if data_type == 'string':
                return ""
            if data_type == 'int':
                return 0;
            return None
        # In execution:
        read_value = ReadAndPrint.read()
        if data_type == 'string':
            return read_value
        elif data_type == 'int':
            int_value = self.to_int(read_value)
            while int_value == None:
                print(f"The input '{read_value}' is not an integer. Please try again.")
                read_value = self.read_input()
                int_value = self.to_int(read_value)
            return int_value

    def print_output(self, value):
        if self.in_execution():
            ReadAndPrint.print(value)


    def visit_ProgramNode(self, node: AST):      
        for statement_node in node.statements:
            self.visit(statement_node)


    def visit_ReadNode(self, node: AST):
        if node == None:
            self.raise_error("AST Node was empty.")
            return
        identifier_token = node.identifier_token
        identifier = identifier_token.lexeme
        symbol_table_entry = self.parser.symbol_table.exists_in_symbol_table(identifier_token)
        if symbol_table_entry == None:
            return self.raise_error(node.identifier_token, f"Identifier '{identifier}' is not declared.")
        data_type = symbol_table_entry.variable_type
        if data_type == 'bool': 
            return self.raise_error(node.read_keyword_token, f"Trying to read an input into a bool variable '{identifier}'. It is not allowed.")

        read_value = self.read_input(data_type)
        if self.in_execution():
            self.parser.symbol_table.set_new_value_to_variable_in_symbol_table_entry(identifier_token, read_value, node, self.in_execution())

    def visit_IdentifierNode(self, node: AST):
        value = self.symbol_table.get_value(node.identifier_token)
        if self.value_is_correct(node.identifier_token, value, "Incorrect value."):
            return value
        else:
            return

    def visit_PrintNode(self, node: AST):
        # visit the expression and print the value
        value = self.visit(node.expression_root)
        if self.value_is_correct(node.expression_root.the_token(), value, "Incorrect expression."):
            self.print_output(value)
        return


    def visit_VariableDeclarationNode(self, node: AST):
        # Variable is already declared by parser. If node has assignment expression, visit it.
        if node.variable_assignment_expression_root == None:
            return
        identifier_token = node.identifier_token
        value = self.visit(node.variable_assignment_expression_root)
        if self.value_is_correct(identifier_token, value, "Incorrect expression."):
            if self.in_execution():
                if self.symbol_table.set_new_value_to_variable_in_symbol_table_entry(identifier_token, value, node, self.in_execution()) == False:
                    self.raise_error(identifier_token, "")
                
        return

    def visit_VariableAssignNode(self, node: AST):
        # Visit the assignment.
        identifier_token = node.identifier_token
        value = self.visit(node.expression_root)
        if self.value_is_correct(node.expression_root.the_token(), value, "Incorrect expression."):
            if self.symbol_table.set_new_value_to_variable_in_symbol_table_entry(identifier_token, value, node, self.in_execution()) == False:
                self.raise_error(identifier_token, f"Error occured while trying to set new value to variable {identifier_token.lexeme}.")
        return

    def raise_assertion_error(self, token: Token):
        if self.in_execution():
            print(f"Assertion error in line {token.line_start}. The execution of the program is ended.")
            self.errors_found += 1
        return

    def visit_AssertNode(self, node: AST):
        # visit the expression and compare if true. If not, show Assertion error and stop interpreting.
        value = self.visit(node.expression_root)
        if self.value_is_correct(node.expression_root.the_token(), value, "Incorrect expression."):
            if (type(value) == type(True)) and (value == True):
                return
            else:
                self.raise_assertion_error(node.the_token())
        return
        

    def visit_ForLoopNode(self, node: AST):
        for_keyword_token = node.for_keyword_token
        end_keyword_token = node.end_keyword_token
        control_variable_token = node.control_variable_token
        symbol_table_entry = self.symbol_table.exists_in_symbol_table(control_variable_token)
        if symbol_table_entry == None:
            self.raise_error(control_variable_token, f"The control variable {control_variable_token.lexeme} in for loop starting from line {for_keyword_token.line_start} is not declared.")
            return None
        range_start_value = self.visit(node.range_start_expression_node)
        range_end_value = self.visit(node.range_end_expression_node)
        if not self.value_is_correct(node.range_start_expression_node, range_start_value, "Incorrect expression."):
            return False
        if not self.value_is_correct(node.range_end_expression_node, range_end_value, "Incorrect expression."):
            return False
        if not isinstance(range_start_value, int):
            self.raise_error(for_keyword_token, "In for loop, the range start value is not of type 'int'.")
            return False
        if not isinstance(range_end_value, int):
            self.raise_error(for_keyword_token, "In for loop, the range end value is not of type 'int'.")
            return False
        if not symbol_table_entry.set_as_control_variable(node):
            self.raise_error(control_variable_token, f"The variable {control_variable_token.lexeme} is a control variable of another for loop.")
            return False

        if not self.symbol_table.set_new_value_to_variable_in_symbol_table_entry(control_variable_token, range_start_value, node, self.in_execution()):
            return False
        if self.in_semantic_analysis():
            for statement_node in node.statements:
                self.visit(statement_node)
            if not symbol_table_entry.increment_control_variable(node, self.in_execution()):
                self.raise_error(control_variable_token, f"Error: It is forbidden to change the value of a for loop control variable.")
                return False
            symbol_table_entry.unset_as_control_variable(node)
        else: # If in execution
            while symbol_table_entry.value <= range_end_value:
                for statement_node in node.statements:
                    self.visit(statement_node)
                if not symbol_table_entry.increment_control_variable(node, self.in_execution()):
                    self.raise_error(control_variable_token, f"Error: It is forbidden to change the value of a for loop control variable.")
                    return False
            symbol_table_entry.unset_as_control_variable(node)

    def visit_IfNode(self, node: AST):
        if_token = node.if_token
        expression_node = node.expression_node
        condition_value = self.visit(expression_node)
        if not self.value_is_correct(expression_node, condition_value, "Incorrect expression."):
            return False
        if not isinstance(condition_value, bool):
            self.raise_error(if_token, "Type error in the condition expression of the if statement.")
            return False
        if self.in_execution():
            if condition_value:
                for statement_node in node.statements:
                    self.visit(statement_node)
            else:
                for statement_node in node.else_statements:
                    self.visit(statement_node)
        else: # In semantical analysis
            for statement_node in node.statements:
                self.visit(statement_node)            
            for statement_node in node.else_statements:
                self.visit(statement_node)


    def visit_BinaryOperationNode(self, node: AST):
        left_value = self.visit(node.left)
        right_value = self.visit(node.right)
        operation_token = node.operation_token
        operation = operation_token.type
        if type(left_value) != type(right_value):
            self.raise_error(operation_token, f"The expression has incompatible types. All types must be the same.")
            return
        if type(left_value) != type(True): # int and string are ok.
            if operation == 'PLUS':
                return left_value + right_value
        if type(left_value) == type(1):
            if operation == 'SUB':
                return left_value - right_value
            if operation == 'MUL':
                return left_value * right_value
            if operation == 'DIV':
                if self.in_semantic_analysis():
                    return left_value # Do not check dividing by zero, because right value may be dependent on runtime execution.
                if right_value == 0:
                    return self.raise_error(operation_token, "Divide by zero.")
                return left_value // right_value
        if (type(left_value) == type(True)) and (operation == 'AND'):
            return left_value and right_value
        if operation == 'EQUAL':
            return left_value == right_value
        if operation == 'SMALLER':
            return left_value < right_value
        left_type = self.to_mini_pl_type(left_value)
        right_type = self.to_mini_pl_type(right_value)
        return self.raise_error(operation_token, f"Incompatible operand types for binary operation.")
        

    def visit_UnaryOperationNode(self, node: AST):
        value = self.visit(node.left)
        if type(value) != type(True):
            self.raise_error(node.the_token(), "The operation !:(bool) -> bool can be used only if the value is of type 'bool', not with type '{self.to_mini_pl_type(value)}'.")
            return
        if node.operation_token.type == 'NOT':
            return not value

    def visit_IntegerNode(self, node: AST) -> int:
        return node.value

    def visit_StringNode(self, node: AST) -> str:
        return node.value

        
