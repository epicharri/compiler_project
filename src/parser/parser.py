from src.scanner.scanner import Scanner
from src.scanner.token import *
from src.parser.symbol_table import *
from src.parser.ast import *

class Parser:
    def __init__(self, scanner: Scanner):
        self.scanner = scanner
        self.current_token = None
        self.errors_found = 0
        self.error_in_last_token = False
        self.for_loop_depth = 0
        self.if_block_depth = 0
        self.current_data_type_in_expression = None
        self.symbol_table = SymbolTable()
        self.program_node = ProgramNode()

    
    def new_current_token(self):
        if not self.is_eof():
            self.current_token = self.scanner.get_next_token()
            if self.scanner.parameters.print_tokens:
                print("New token found:", self.current_token)
    
    
    def is_literal_or_variable_identifier(self):
        return self.current_token.is_string_literal() or self.current_token.is_integer_literal() or self.current_token.is_variable_identifier()
    
  
    def print_error_and_forward_to_next_statement(self, error_message):
        self.errors_found += 1

        print(f"Error in line {self.current_token.line_start}: '{self.current_token.lexeme}'", error_message, "The parsing continues from the next statement, after the next semicolon.")

        while True:
            self.new_current_token()
            if self.current_token.is_eos_token():
                print(f"The parsing starts again from line {self.current_token.line_start + 1}.")
                self.new_current_token()
                break
            if self.current_token.is_eof_token():
                print("The end of file reached without any semicolon after the error.")
                break


    def match_eos(self):
        if self.current_token.is_eos_token():
            self.new_current_token()
            return True
        else:
            self.print_error_and_forward_to_next_statement(f"The end of the statement symbol ';' expected, but got '{self.current_token.lexeme}'.")   
            return False     
  
    def match(self, expected: bool) -> bool: # The parameter is boolean in the form self.current_token.is_something(), where is_something is a method in Token class. Returns True, if successfully matched.
        if expected:
            self.new_current_token()
            return True
        else:
           self.print_error_and_forward_to_next_statement(f"Unexpected token '{self.current_token.lexeme}'.")
           return False


    def is_eof(self):
        if self.current_token:
            return self.current_token.is_eof_token()
        return False # In the beginning, current_token == None. Thus, not EOF. 

    def parse_variable_declaration(self):
        self.new_current_token()
        identifier_token = self.current_token
        variable_type_token = None
        variable_assignment_expression_root = None # AST

        if self.current_token.is_identifier_token():
            self.match(True)
        else:
            self.print_error_and_forward_to_next_statement("There should be a variable identifier after keyword var, but found '{token.type} {token.value}'.")
            return None
        if not self.current_token.is_colon_token():
            self.print_error_and_forward_to_next_statement(f"There must be ':' after a variable identifier in declaration, but found '{self.current_token.lexeme}'.")
            return None
        self.match(True)
        if not self.current_token.is_variable_type_token():
            self.print_error_and_forward_to_next_statement(f"Expected 'int', 'string', or 'bool', but got {self.current_token.lexeme}")
            return None
        variable_type_token = self.current_token
        if not self.symbol_table.add_new_symbol_table_entry(identifier_token, variable_type_token):
            self.errors_found += 1
        self.match(True)
        if self.current_token.is_eos_token():
            node = VariableDeclarationNode(identifier_token, variable_type_token, None)
            self.match(True)
            return node
        if not self.current_token.is_assignment_token():
            return None
        self.match(True)
        variable_assignment_expression_root = self.parse_expression()
        if not variable_assignment_expression_root:
            return None
        if self.current_token.is_eos_token():
            node = VariableDeclarationNode(identifier_token, variable_type_token, variable_assignment_expression_root)
            self.match(True)
            return node
        else:
            self.print_error_and_forward_to_next_statement(f"Semicolon was expected but got '{self.current_token.lexeme}'")
        return None

    def parse_read(self):
        read_keyword_token = self.current_token
        identifier_token = None
        self.new_current_token()
        if self.current_token.is_identifier_token():
            identifier_token = self.current_token
            self.match(True)
            read_node = ReadNode(read_keyword_token, identifier_token)
            if not self.match_eos():
                return None
            return read_node
        else:
            self.print_error_and_forward_to_next_statement(f"Illegal variable name '{self.current_token.lexeme}'.")


    def parse_for(self):
        self.for_loop_depth += 1
        for_keyword_token = self.current_token
        self.match(True)
        for_loop_variable_token = self.current_token
        if not self.match(for_loop_variable_token.is_identifier_token()):
            return None
        if not self.match(self.current_token.is_in_token):
            return None
        range_start_expression_node = self.parse_expression()
        if not range_start_expression_node:
            return None
        if not self.match(self.current_token.is_range_separator_token()):
            return None
        range_end_expression_node = self.parse_expression()
        if not range_end_expression_node:
            return None
        node = ForLoopNode(for_loop_variable_token, range_start_expression_node, range_end_expression_node, for_keyword_token, None)
        if not self.match(self.current_token.is_do_token()):
            return False

        while not(self.current_token.is_end_token() or self.current_token.is_eof_token()):
            statement_node = self.parse_statement()
            if not statement_node:
                return None
            node.add_statement(statement_node)

        end_keyword_token = self.current_token
        if not self.match(end_keyword_token.is_end_token()):
            return None
        if not self.match(self.current_token.is_for_token()):
            return None
        node.set_end_keyword_token(end_keyword_token)
        self.for_loop_depth -= 1
        if not self.match(self.current_token.is_eos_token()):
            return None
        return node
        

    def parse_if(self):
        if_token = self.current_token
        self.new_current_token()
        self.if_block_depth += 1
        expression_token = self.current_token
        expression_node = self.parse_expression()
        if not expression_node:
            return None
        node = IfNode(if_token, expression_token, None, None, expression_node)

        if not self.match(self.current_token.is_do_token()):
            return None
                
        while not(self.current_token.is_end_token() or self.current_token.is_else_token() or self.current_token.is_eof_token()):
            statement_node = self.parse_statement()
            if not statement_node:
                return None
            node.add_statement(statement_node)

        if self.current_token.is_else_token():
            else_token = self.current_token
            node.add_else_token(else_token)
            self.match(True)
            while not(self.current_token.is_end_token() or self.current_token.is_eof_token()):
                statement_node = self.parse_statement()
                if not statement_node:
                    return None
                node.add_else_statement(statement_node)

        end_token = self.current_token    

        if not self.match(end_token.is_end_token()):
            return None
        node.add_end_token(end_token)
        if not self.match(self.current_token.is_if_token()):
            return None
        self.if_block_depth -= 1
        if not self.match(self.current_token.is_eos_token()):
            return None
        return node

    def parse_assert(self):
        assert_token = self.current_token
        self.new_current_token()
        if not self.match(self.current_token.is_left_parenthesis()):
            return None
        expression_node = self.parse_expression()
        if not expression_node:
            return None
        if not self.match(self.current_token.is_right_parenthesis()):
            return None
        if not self.match(self.current_token.is_eos_token()):
            return None
        assert_node = AssertNode(assert_token, expression_node)
        return assert_node

    def undeclared_variable_error(self):
        if self.symbol_table.exists_in_symbol_table(self.current_token):
            return False
        else:
            self.print_error_and_forward_to_next_statement(f"Error in line {self.current_token.line_start}. The variable {self.current_token.lexeme} is not yet declared.")
            return True       

    def parse_variable_assignment(self):
        if self.undeclared_variable_error():
            return False
        node = VariableAssignNode(self.current_token)
        self.match(True)
        if not self.match(self.current_token.is_assignment_token()):
            return False
        expression_root = self.parse_expression()
        if not expression_root:
            return None
        node.add_expression_node(expression_root)
        if not self.match(self.current_token.is_eos_token()):
            return None
        return node

    def parse_print(self):
        print_keyword_token = self.current_token
        self.match(True)
        expression_root = self.parse_expression()
        if not expression_root:
            return None
        if not self.match_eos():
            return None
        node = PrintNode(print_keyword_token, expression_root)
        return node

    def parse_expression(self) -> bool:
        if self.is_proper_start_of_operand():
            node = self.parse_term()
            if not node:
                return None
            while self.current_token.is_binary_operator():
                token = self.new_current_token()
                rhs = self.parse_term()
                if not self.match(rhs):
                    return None
                node = BinaryOperationNode(token, node, rhs)
            return node
        elif self.current_token.is_unary_operator():
            token = self.current_token
            self.new_current_token()
            lhs = self.parse_term()
            if not lhs:
                return None
            node = UnaryOperationNode(token, lhs)
            return node
        else:
            self.print_error_and_forward_to_next_statement(f"The expression is invalid starting from '{self.current_token.lexeme}'.")
            return False

    def parse_term(self): 
        lhs = self.parse_factor()
        if not lhs:
            return None
        while self.current_token.is_binary_operator():
            bin_op_node = BinaryOperationNode(self.current_token)
            self.new_current_token()
            rhs = self.parse_factor()
            if not rhs:
                return None
            bin_op_node.add_left_and_right_child(lhs, rhs)
            lhs = bin_op_node
        return lhs

    def parse_factor(self):
        if self.current_token.is_identifier_token():
            e = IdentifierNode(self.current_token)
            self.match(True)
            return e
        if self.current_token.is_integer_literal(): 
            e = IntegerNode(self.current_token)
            self.match(True)
            return e
        if self.current_token.is_string_literal(): 
            e = StringNode(self.current_token)
            self.match(True)
            return e
        if self.current_token.is_left_parenthesis():
            self.new_current_token()
            e = self.parse_expression()
            if not e:
                return None
            if not self.match(self.current_token.is_right_parenthesis()):
                return None
            else:
                return e
        else:
            self.print_error_and_forward_to_next_statement(f"An identifier, integer literal, string literal, or left parenthesis was expected but got '{self.current_token.lexeme}'.")
            return False

    def is_proper_start_of_operand(self):
        return self.current_token.is_integer_literal() or self.current_token.is_string_literal() or self.current_token.is_identifier_token() or self.current_token.is_left_parenthesis()

    def is_proper_start_of_statement(self) -> bool:
        return self.current_token.is_var_token() or self.current_token.is_read_token() or self.current_token.is_for_token() or self.current_token.is_print_token() or self.current_token.is_if_token() or self.current_token.is_assert_token() or self.current_token.is_identifier_token() or self.current_token.is_eof_token()

    def parse_statement(self):
        if self.is_eof():
            return True

        if self.current_token.is_var_token():
            return self.parse_variable_declaration()
            
        elif self.current_token.is_read_token():
            node = self.parse_read()
            return node
            
        elif self.current_token.is_for_token():
            return self.parse_for()
            
        elif self.current_token.is_print_token():
            return self.parse_print()
            
        elif self.current_token.is_if_token():
            return self.parse_if()
            
        elif self.current_token.is_assert_token():
            return self.parse_assert()
            
        elif self.current_token.is_identifier_token():
            node = self.parse_variable_assignment()
            return node

        elif self.current_token.is_error_token():
            self.print_error_and_forward_to_next_statement(f"Incorrect token. '{self.current_token.error_message}'.")
            return False
        else:
            self.print_error_and_forward_to_next_statement(f"A statement can not start with '{self.current_token.lexeme}'.")
            return False
       

    def parse_program(self):
        self.new_current_token()
        while not self.is_eof():
            node = self.parse_statement()
            self.program_node.append_statement(node)
        if self.is_eof():
            print("SYMBOL TABLE")
            print(f"{self.symbol_table.symbol_table}")
            print()
            for st in self.program_node.statements:
                print(st)
                print()
            
            error_info_text = "No errors found."
            if self.errors_found > 0:
                error_info_text = f"Number of errors is {self.errors_found}."
            print(f"END OF PARSING. {error_info_text} The last token is '{self.current_token.lexeme}'")

            return
        self.print_error_and_forward_to_next_statement(f"A statement can not start with '{self.current_token.lexeme}'")


