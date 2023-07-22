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
  
    def is_eof(self):
        if self.current_token:
            return self.current_token.is_eof_token()
        return False # In the beginning, current_token == None. Thus, not EOF. 

    def parse_variable_declaration(self):
        self.new_current_token()

        if self.current_token.is_identifier_token():
            print("By method in Token, this is an identifier.")
        else:
            self.print_error_and_forward_to_next_statement("There should be a variable identifier after keyword var, but found '{token.type} {token.value}'.")
            return
        self.new_current_token()
        if not self.current_token.is_colon_token():
            self.print_error_and_forward_to_next_statement(f"There must be ':' after a variable identifier in declaration, but found '{self.current_token.lexeme}'.")
            return
        self.new_current_token()
        if not self.current_token.is_variable_type_token:
            self.print_error_and_forward_to_next_statement(f"Expected 'int', 'string', or 'bool', but got {self.current_token.lexeme}")
            return
        self.new_current_token()
        if self.current_token.is_eos_token():
            self.new_current_token()
        return

    def parse_read(self):
        self.new_current_token()
        if self.current_token.is_identifier_token():
            print(f"Found an identifier '{self.current_token.lexeme}'")
        else:
            self.print_error_and_forward_to_next_statement(f"Illegal variable name '{self.current_token.lexeme}'.")
        self.new_current_token()
        self.match_eos()

    def temporary_function_for_forward_to_next_statement(self):
        while not self.current_token.is_eof_token():
            if self.current_token.is_eos_token():
                self.new_current_token()
                break
            self.new_current_token()

    def parse_for(self):
        self.new_current_token()
        self.temporary_function_for_forward_to_next_statement()

    def parse_print(self):
        self.temporary_function_for_forward_to_next_statement()

    def parse_if(self):
        self.new_current_token()
        self.temporary_function_for_forward_to_next_statement()

    def parse_assert(self):
        self.new_current_token()
        self.temporary_function_for_forward_to_next_statement()

    def parse_variable_assignment(self):
        self.new_current_token()
        self.temporary_function_for_forward_to_next_statement()

    def parse_expression(self):
        self.parse_term()
        pass

    def parse_term(self):
        pass

    def parse_factor(self):
        pass

    def parse_add_op(self):
        pass

    def parse_mult_op(self):
        pass
    

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
        


    def parse_program(self):
        self.new_current_token()
        while True:
            self.parse_statement()
            if self.is_eof():
                break
        print(f"END OF PARSING. The last token is '{self.current_token.lexeme}'")


