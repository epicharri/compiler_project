from src.scanner.scanner import Scanner
from src.scanner.token import *

class Parser:
    def __init__(self, scanner: Scanner):
        self.scanner = scanner
        self.current_token = None
        self.error_found = False
        self.error_in_last_token = False
    
    def new_current_token(self):
        if not self.is_eof():
            self.current_token = self.scanner.get_next_token()
            print("In new_current_token():", self.current_token)
    
    def make_node(symbol: str, lexeme: str):
        print("IN MAKE_NODE: Current token = {self.current_token}, symbol = {symbol}, lexeme = {lexeme}")

    
    def is_literal_or_variable_identifier(self):
        return self.current_token.is_string_literal() or self.current_token.is_integer_literal() or self.current_token.is_variable_identifier()
    
    def is_expression_operand(self):
        pass

  
    def print_error_and_forward_to_next_statement(self, error_message):
        self.error_found = True

        print(f"Error in line {self.current_token.line_start}.", error_message, "The parsing continues from the next statement, after the next semicolon.")

        while True:
            self.new_current_token()
            if self.current_token.is_eos_token():
                print(f"The parsing starts again from line {self.current_token.line_start + 1}.")
                self.new_current_token()
                break
            if self.current_token.is_eof_token():
                print("The end of file reached without any semicolon after the error.")
                break


    def operand(self):
        if not self.is_literal_or_variable_identifier():
            return False
        pass # To do: handle the operand
        
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
            print("By method in Token, this is an identifier.")
            self.match(True)
        else:
            self.print_error_and_forward_to_next_statement("There should be a variable identifier after keyword var, but found '{token.type} {token.value}'.")
            return
        # self.new_current_token()
        if not self.current_token.is_colon_token():
            self.print_error_and_forward_to_next_statement(f"There must be ':' after a variable identifier in declaration, but found '{self.current_token.lexeme}'.")
            return
        self.match(True)
        if not self.current_token.is_variable_type_token:
            self.print_error_and_forward_to_next_statement(f"Expected 'int', 'string', or 'bool', but got {self.current_token.lexeme}")
            return
        self.match(True)
        if self.current_token.is_eos_token():
            self.match(True)
            return
        if self.current_token.is_assignment_token():
            self.match(True)
            self.parse_expression()
        if self.current_token.is_eos_token():
            self.match(True)
            return
        else:
            self.print_error_and_forward_to_next_statement(f"Semicolon was expected but got '{self.current_token.lexeme}'")
        return

    def parse_read(self):
        self.new_current_token()
        if self.current_token.is_identifier_token():
            print(f"Found an identifier '{self.current_token.lexeme}'")
            self.match(True)
            self.match_eos()
        else:
            self.print_error_and_forward_to_next_statement(f"Illegal variable name '{self.current_token.lexeme}'.")


    def temporary_function_for_forward_to_next_statement(self):
        while not self.current_token.is_eof_token():
            if self.current_token.is_eos_token():
                self.match(True)
                break
            self.new_current_token()

    def parse_for(self):
        self.new_current_token()
        if not self.match(self.current_token.is_identifier_token()):
            return
        if not self.match(self.current_token.is_in_token):
            return
        self.parse_expression()
        if not self.match(self.current_token.is_range_separator_token()):
            return
        self.parse_expression()
        if not self.match(self.current_token.is_do_token()):
            return
        if self.is_proper_start_of_statement():
            self.parse_statement_list()
        elif not self.match(self.current_token.is_end_token()):
            return
        if not self.match(self.current_token.is_for_token()):
            return
        self.match(self.current_token.is_eos_token())
        

    def parse_print(self):
        self.match(True)
        self.parse_expression()
        self.match_eos()

    def parse_if(self):
        self.new_current_token()
        self.parse_expression()
        if self.match(self.current_token.is_do_token()):
            return
        if self.is_proper_start_of_statement():
            self.parse_statement_list()
        if self.current_token.is_else_token():
            if self.is_proper_start_of_statement():
                self.parse_statement_list()
        if not self.match(self.current_token.is_end_token()):
            return
        if not self.match(self.current_token.is_if_token()):
            return
        self.match(self.current_token.is_eos_token())

    def parse_assert(self):
        self.new_current_token()
        if not self.match(self.current_token.is_left_parenthesis()):
            return
        self.parse_expression()
        if not self.match(self.current_token.is_right_parenthesis()):
            return
        self.match(self.current_token.is_eos_token())

    def parse_variable_assignment(self):
        self.match(True)
        if not self.match(self.current_token.is_assignment_token()):
            return
        self.parse_expression()
        print(f"IN PARSE_VARIABLE_ASSIGNMENT: current token is '{self.current_token}'")
        self.match(self.current_token.is_eos_token())


    def parse_expression(self):
        if self.is_proper_start_of_operand():
            self.parse_operand()
            while self.current_token.is_additive_operator():
                self.new_current_token()
                self.parse_operand()
        elif self.current_token.is_unary_operator():
            self.parse_unary_operator()
            self.parse_operand()
        else:
            self.print_error_and_forward_to_next_statement(f"The expression is invalid starting from '{self.current_token.lexeme}'.")

    def parse_operand(self): # term
        self.parse_factor()
        while self.current_token.is_multiplicative_operator():
            self.new_current_token()
            self.parse_factor()

    def parse_factor(self):
        if self.current_token.is_identifier_token():
            self.match(True)
        elif self.current_token.is_integer_literal() or self.current_token.is_string_literal:
            print(f"In parse_factor, is_integer_literal or string_literal, token = {self.current_token}")
            self.match(True)
        elif self.current_token.is_left_parenthesis():
            self.new_current_token()
            self.parse_expression()
            self.match(self.current_token.is_right_parenthesis())
        else:
            self.print_error_and_forward_to_next_statement(f"An identifier, integer literal, string literal, or left parenthesis was expected but got '{self.current_token.lexeme}'.")

    def parse_add_op(self):
        pass

    def parse_mult_op(self):
        pass

    def parse_not_op(self):
        pass

    def parse_and_op(self):
        pass

    # def parse_expression_tail(self):
    #    pass
            

    def is_proper_start_of_operand(self):
        return self.current_token.is_integer_literal() or self.current_token.is_string_literal() or self.current_token.is_identifier_token() or self.current_token.is_left_parenthesis()

    def is_proper_start_of_statement(self) -> bool:
        return self.current_token.is_var_token() or self.current_token.is_read_token() or self.current_token.is_for_token() or self.current_token.is_print_token() or self.current_token.is_if_token() or self.current_token.is_assert_token() or self.current_token.is_identifier_token() or self.current_token.is_eof_token()

    def parse_statement(self):
        if self.is_eof():
            return
        if self.current_token.is_var_token():
            self.parse_variable_declaration()
            return
        elif self.current_token.is_read_token():
            self.parse_read()
            return
        elif self.current_token.is_for_token():
            self.parse_for()
            return
        elif self.current_token.is_print_token():
            self.parse_print()
            return
        elif self.current_token.is_if_token():
            self.parse_if()
            return
        elif self.current_token.is_assert_token():
            self.parse_assert()
            return
        elif self.current_token.is_identifier_token():
            self.parse_variable_assignment()
            return
        elif self.current_token.is_error_token():
            print("ERROR TOKEN FOUND")
            self.print_error_and_forward_to_next_statement(f"An error: '{self.current_token.error_message}'.")
        else:
            self.print_error_and_forward_to_next_statement(f"A statement can not start with '{self.current_token.lexeme}'.")


    def parse_statement_list(self):
        if self.current_token.is_eof_token():
            return
        if self.is_proper_start_of_statement():
            self.parse_statement()
            self.parse_statement_list()         
        else:
          self.print_error_and_forward_to_next_statement(f"An error while parsing the statements list.") 

    def parse_program(self):
        self.new_current_token()
        if self.is_proper_start_of_statement():
            self.parse_statement_list()
            if self.is_eof():
              print(f"END OF PARSING. The last token is '{self.current_token.lexeme}'")
              return
        else:
            self.print_error_and_forward_to_next_statement(f"A statement can not start with '{self.current_token.lexeme}'")


