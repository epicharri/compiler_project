from src.scanner.scanner import Scanner
from src.scanner.token import *
from src.parser.symbol_table import *
from src.parser.ast import *
from src.parser.parser import *

class Visitor(object):
    def visit(self, node: AST):
        pass
    
class Interpreter(Visitor):
    def __init__(self, parser):
        super().__init__()
        self.parser = parser
    
    def interpret(self):
        ast = self.parser.parse_program()
        if self.parser.errors_found > 0:
          print("Since there are errors in the program, it is not executed.")
          return False # Errors.
        self.visit(ast)


    
