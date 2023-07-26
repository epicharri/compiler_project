from src.scanner.scanner import Scanner
from src.scanner.token import *

class Parser:
    def __init__(self, scanner: Scanner):
        self.scanner = scanner
        self.current_token = None
        self.error_found = False
        self.error_in_last_token = False
        self.for_loop_depth = 0
        self.if_block_depth = 0

    
    def new_current_token(self):
        if not self.is_eof():
            self.current_token = self.scanner.get_next_token()
            print("In new_current_token():", self.current_token)
    
    def make_node(symbol: str, lexeme: str):
        print("IN MAKE_NODE: Current token = {self.current_token}, symbol = {symbol}, lexeme = {lexeme}")

    
    def is_literal_or_variable_identifier(self):
        return self.current_token.is_string_literal() or self.current_token.is_integer_literal() or self.current_token.is_variable_identifier()
    
  
    def print_error_and_forward_to_next_statement(self, error_message):
        self.error_found = True

        print(f"Error in line {self.current_token.line_start}.", error_message, "The parsing continues from the next statement, after the next semicolon.")

        while True:
            print("IN ERROR RECOVERY!!!!!!!!!!!!!!!!!!!!!!!1")
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
            print(f"MATCH SUCCESS in Token: {self.current_token}")
            self.new_current_token()
            return True
        else:
           self.print_error_and_forward_to_next_statement(f"Error in line {self.current_token.line_start}. Unexpected token '{self.current_token.lexeme}'.")
           return False


    def is_eof(self):
        if self.current_token:
            return self.current_token.is_eof_token()
        return False # In the beginning, current_token == None. Thus, not EOF. 

    def parse_variable_declaration(self):
        self.new_current_token()
        if self.current_token.is_identifier_token():
            self.match(True)
        else:
            self.print_error_and_forward_to_next_statement("There should be a variable identifier after keyword var, but found '{token.type} {token.value}'.")
            return False
        # self.new_current_token()
        if not self.current_token.is_colon_token():
            self.print_error_and_forward_to_next_statement(f"There must be ':' after a variable identifier in declaration, but found '{self.current_token.lexeme}'.")
            return False
        self.match(True)
        if not self.current_token.is_variable_type_token():
            self.print_error_and_forward_to_next_statement(f"Expected 'int', 'string', or 'bool', but got {self.current_token.lexeme}")
            return False
        self.match(True)
        if self.current_token.is_eos_token():
            self.match(True)
            return True
        if not self.current_token.is_assignment_token():
            return False
        self.match(True)
        if not self.parse_expression():
            return False
        if self.current_token.is_eos_token():
            self.match(True)
            return True
        else:
            self.print_error_and_forward_to_next_statement(f"Semicolon was expected but got '{self.current_token.lexeme}'")
        return False

    def parse_read(self):
        self.new_current_token()
        if self.current_token.is_identifier_token():
            self.match(True)
            return self.match_eos()
        else:
            self.print_error_and_forward_to_next_statement(f"Illegal variable name '{self.current_token.lexeme}'.")


    def parse_for(self):
        self.for_loop_depth += 1
        self.new_current_token()
        if not self.match(self.current_token.is_identifier_token()):
            return False
        if not self.match(self.current_token.is_in_token):
            return False
        if not self.parse_expression():
            return False
        if not self.match(self.current_token.is_range_separator_token()):
            return False
        if not self.parse_expression():
            return False
        if not self.match(self.current_token.is_do_token()):
            return False
        if self.is_proper_start_of_statement():
            if not self.parse_statement_list():
                return False
        if not self.match(self.current_token.is_end_token()):
            return False
        if not self.match(self.current_token.is_for_token()):
            return False
        self.for_loop_depth -= 1
        return self.match(self.current_token.is_eos_token())
        

    def parse_print(self):
        self.match(True)
        if not self.parse_expression():
            return False
        return self.match_eos()

    def parse_if(self):
        self.new_current_token()
        self.if_block_depth += 1
        if not self.parse_expression():
            return False
        if not self.match(self.current_token.is_do_token()):
            return False
        if self.is_proper_start_of_statement():
            if not self.parse_statement_list():
                return False
        if self.current_token.is_else_token():
            self.match(True)
            if self.is_proper_start_of_statement():
                if not self.parse_statement_list():
                    return False
        if not self.match(self.current_token.is_end_token()):
            return False
        if not self.match(self.current_token.is_if_token()):
            return False
        self.if_block_depth -= 1
        if not self.match(self.current_token.is_eos_token()):
            return False
        return True

    def parse_assert(self):
        self.new_current_token()
        if not self.match(self.current_token.is_left_parenthesis()):
            return False
        if not self.parse_expression():
            return False
        if not self.match(self.current_token.is_right_parenthesis()):
            return False
        if not self.match(self.current_token.is_eos_token()):
            return False
        return True

    def parse_variable_assignment(self):
        self.match(True)
        if not self.match(self.current_token.is_assignment_token()):
            return False
        if not self.parse_expression():
            return False
        if not self.match(self.current_token.is_eos_token()):
            return False
        return True


    def parse_expression(self) -> bool:
        if self.is_proper_start_of_operand():
            if not self.parse_operand():
                return False
            while self.current_token.is_binary_operator():
                self.new_current_token()
                if not self.match(self.parse_operand()):
                    return False
            return True
        elif self.current_token.is_unary_operator():
            self.new_current_token()
            if not self.parse_operand():
                return False
            return True
        else:
            self.print_error_and_forward_to_next_statement(f"The expression is invalid starting from '{self.current_token.lexeme}'.")
            return False

    def parse_operand(self): # term
        if not self.parse_factor():
            return False
        while self.current_token.is_binary_operator():
            self.new_current_token()
            if not self.parse_factor():
                return False
        return True

    def parse_factor(self):
        if self.current_token.is_identifier_token():
            self.match(True)
            return True
        if self.current_token.is_integer_literal() or self.current_token.is_string_literal():
            self.match(True)
            return True
        if self.current_token.is_left_parenthesis():
            self.new_current_token()
            if not self.parse_expression():
                return False
            if not self.match(self.current_token.is_right_parenthesis()):
                return False
            else:
                return True
        else:
            self.print_error_and_forward_to_next_statement(f"An identifier, integer literal, string literal, or left parenthesis was expected but got '{self.current_token.lexeme}'.")
            return False

    def parse_add_op(self):
        pass

    def parse_mult_op(self):
        pass

    def parse_not_op(self):
        pass

    def parse_and_op(self):
        pass

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
            return self.parse_read()
            
        elif self.current_token.is_for_token():
            return self.parse_for()
            
        elif self.current_token.is_print_token():
            return self.parse_print()
            
        elif self.current_token.is_if_token():
            return self.parse_if()
            
        elif self.current_token.is_assert_token():
            return self.parse_assert()
            
        elif self.current_token.is_identifier_token():
            return self.parse_variable_assignment()
        
        elif self.current_token.is_end_token() and (self.for_loop_depth > 0 or self.if_block_depth > 0):
            return True

        elif self.current_token.is_else_token() and self.if_block_depth > 0:
            return True

        elif self.current_token.is_error_token():
            print("ERROR TOKEN FOUND")
            self.print_error_and_forward_to_next_statement(f"An error: '{self.current_token.error_message}'.")
            return False
        else:
            self.print_error_and_forward_to_next_statement(f"A statement can not start with '{self.current_token.lexeme}'.")
            return False


    def parse_statement_list(self):
        if self.current_token.is_eof_token():
            return True
        while self.is_proper_start_of_statement():
            if self.current_token.is_eof_token():
                return True
            if not self.parse_statement():
                return False
            if self.current_token.is_end_token() and (self.for_loop_depth > 0 or self.if_block_depth > 0):
                return True
            if self.current_token.is_else_token() and self.if_block_depth > 0:
                return True            

    def parse_program(self):
        self.new_current_token()
        while self.is_proper_start_of_statement() or self.is_eof():
            self.parse_statement_list()
            if self.is_eof():
              error_info_text = "No errors found."
              if self.error_found:
                  error_info_text = "Error(s) found."
              print(f"END OF PARSING. {error_info_text} The last token is '{self.current_token.lexeme}'")
              return
        self.print_error_and_forward_to_next_statement(f"A statement can not start with '{self.current_token.lexeme}'")


