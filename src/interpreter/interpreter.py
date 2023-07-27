from src.scanner.scanner import Scanner
from src.scanner.token import *
from src.parser.symbol_table import *
from src.parser.ast import *
from src.parser.parser import *
from src.parser.node_type import *
from src.io.read_and_print import ReadAndPrint
       
class Interpreter():
    def __init__(self, parser):
        self.parser = parser
        self.errors_found = 0
    
    def interpret(self):
        ast = self.parser.parse_program()
        if self.parser.errors_found > 0:
          print("Since there are errors in the program, it is not executed.")
          return False # Errors.
        self.visit(ast)

    def raise_error(self, token: Token, msg: str):
        print(f"Error in line {token.line_start}: {msg}")
        self.errors_found += 1
        return False

    def to_int(self, value: str):
        try:
            return int(value)
        except ValueError:
            return False

    def visit(self, node: AST):      
        if node.node_type == NodeType.PROGRAM:
            for statement_node in node.statements:
                if statement_node.node_type == NodeType.READ:
                    self.visit_read(statement_node)
                    if self.errors_found > 0:
                        return


    def visit_read(self, node):
        if not node:
            print("AST Node was empty.")
            self.errors_found += 1
            return
        identifier_token = node.identifier_token
        identifier = identifier_token.lexeme
        symbol_table_entry = self.parser.symbol_table.exists_in_symbol_table(identifier_token)
        if not symbol_table_entry:
            self.raise_error(node.identifier_token, f"Identifier '{identifier}' is not declared.")
        read_value = ReadAndPrint.read()
        data_type = symbol_table_entry.variable_type
        if data_type == 'string':
            self.parser.symbol_table.set_new_value_to_variable_in_symbol_table_entry(identifier_token, read_value)
        elif data_type == 'int':
            int_value = self.to_int(read_value)
            while not int_value:
                print(f"The input '{read_value}' is not an integer. Please give an integer.")
                read_value = ReadAndPrint.read()
                int_value = self.to_int(read_value)
            self.parser.symbol_table.set_new_value_to_variable_in_symbol_table_entry(identifier_token, int_value)
            



