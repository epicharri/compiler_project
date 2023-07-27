from src.io.file_handler import read_file_to_string
from src.scanner.scanner import Scanner
from src.parser.parser import Parser
from src.interpreter.interpreter import Interpreter
from src.parameters import Parameters
import sys

def compiler():
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
    
    scanner = Scanner(raw_data, parameters)
    parser = Parser(scanner)
    interpreter = Interpreter(parser)
    interpreter.interpret()

