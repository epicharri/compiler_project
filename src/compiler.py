from src.io.file_handler import read_file_to_string
from src.scanner.scanner import Scanner
from src.parser.parser import Parser
from src.interpreter.interpreter import Interpreter
from src.parameters import Parameters
import sys

def compiler():
    if len(sys.argv) == 1 or (len(sys.argv) >= 2 and sys.argv[1] == '--help'):
        print("Mini-PL interpreter. Copyright Harri Kähkönen 2023.\nTo interpret a program, give the file path of the source code file as the first parameter.\nIn addition, you can use the following parameters:\n --print-tokens\t\tTo print tokens during parsing.\n --print-ast\t\tTo print AST.\n --print-debug-info\tTo print information during debugging.\n --print-symbol-table\tTo print symbol table after parsing, semantic analysis, and execution.")
        return True
    raw_data = read_file_to_string()
    if not raw_data:
        return False
    parameters = Parameters()

    for i in range(2, len(sys.argv)):
        parameter = sys.argv[i]
        if parameter == "--print-tokens":
            parameters.set_print_tokens()
        if parameter == "--print-ast":
            parameters.set_print_ast()
        if parameter == '--print-debug-info':
            parameters.set_print_debug_info()
        if parameter == '--print-symbol-table':
            parameters.set_print_symbol_table()
    
    scanner = Scanner(raw_data, parameters)
    parser = Parser(scanner)
    interpreter = Interpreter(parser)
    interpreter.interpret()

