from src.scanner.token import Token
from src.parser.ast import *


class SymbolTableEntry():
    def __init__(self, identifier_token: Token, variable_type_token: Token, assigned_value_token = None):
        self.identifier_token = identifier_token
        self.variable_type_token = variable_type_token
        self.assigned_value_token = assigned_value_token
        self.identifier = identifier_token.lexeme # Variable IDENTIFIER
        self.variable_type = variable_type_token.lexeme # Types are: int, string, bool
        self.for_loop_node = None # If set, then self.value is a control variable. Control variables can not be assigned a new value. This is set in the beginning of for loop, and cleared in 'end for'.
        self.is_control_variable = False

        self.value = None # Value is: int, str, or bool. For example, 275, "something", False
        if self.identifier_token.is_identifier_token():
            if self.variable_type_token.is_int_token():
                self.value = 0
            elif self.variable_type_token.is_string_token():
                self.value = ""
            elif self.variable_type_token.is_bool_token():
                self.value = False 


    def __repr__(self):
        control_variable_printout = ""
        if self.is_control_variable:
            control_variable_printout = ", is control variable"
        if self.for_loop_node:
            control_variable_printout += " of for loop with AST id {self.for_loop_node.get_id()}"
        # control_variable_printout should not be visible after parsing, semantic analysis, or execution, provided all for loops have reached end for.
        return f"({self.identifier}, {self.variable_type}, '{self.value}'{control_variable_printout})"

    def set_as_control_variable(self, for_loop_node: AST):
        if self.is_control_variable:
            return False
        self.for_loop_node = for_loop_node # ForLoopNode owning the control variable.
        self.is_control_variable = True
        return True

    def unset_as_control_variable(self, for_loop_node: AST):
        if self.for_loop_node and (self.for_loop_node.get_id() == for_loop_node.get_id()):
            self.for_loop_node = None
            self.is_control_variable = False
        else:
            return False

    def set_value(self, new_value, for_loop_node: AST, in_execution: bool):
        if not self.is_correct_data_type(self.identifier_token, new_value):
            return False
        if (self.for_loop_node == None) or (for_loop_node == None) or (for_loop_node.get_id() == self.for_loop_node.get_id()):
            if in_execution: # Otherwise in semantical analysis phase.
                self.value = new_value
            return True # success
        else:
            control_variable_token = self.for_loop_node.control_variable_token
            print(f"Error: Trying to change the control variable '{control_variable_token.lexeme}' of the for loop which starts on line '{control_variable_token.line_start}'. The value of a for loop control variable is not allowed to be changed.")
            return False

    def increment_control_variable(self, for_loop_node: AST, in_execution: bool = None):
        if (self.for_loop_node == None) or (for_loop_node.get_id() == self.for_loop_node.get_id()):
            if in_execution:
                self.value += 1
            return True
        return False

    def is_correct_data_type(self, given_identifier_token: Token, value):
        types = {"<class 'int'>": 'int', "<class 'str'>": 'string', "<class 'bool'>": 'bool'}
        if types[str(type(value))] != self.variable_type:
            print(f"Error in line {given_identifier_token.line_start}. The identifier {self.identifier_token.lexeme} is of type {self.variable_type}, but the value assigned is of type {types[str(type(value))]}.")
            return False
        return True



class SymbolTable():
    def __init__(self):
        self.symbol_table = {} 
        # key: identifier, value: SymbolTableEntry object
        # types are INTEGER, STRING, and BOOL
        # values are stored as integers, strings and booleans (True or False).
        # Default integer value is 0, default string value is "", and default boolean value is False.

    def __repr__(self):
        output = ""
        for key, value in self.symbol_table.items():
            output += f"{key}: {value}\n"
        return output

    def exists_in_symbol_table(self, identifier_token: Token):
        symbol_table_entry = self.symbol_table.get(identifier_token.lexeme)
        if symbol_table_entry == None:
            print(f"Error in line {identifier_token.line_start}. There is not any variable '{identifier_token.lexeme}'.")
            return None
        return symbol_table_entry

    def get_value(self, identifier_token: Token):
        symbol_table_entry = self.exists_in_symbol_table(identifier_token)
        if symbol_table_entry == None:
            return None
        return symbol_table_entry.value # 


    def add_new_symbol_table_entry(self, identifier_token: Token, variable_type_token: Token) -> bool: # Returns True, if new symbol table entry, otherwise False.
        symbol_table_entry = SymbolTableEntry(identifier_token, variable_type_token)
        identifier = symbol_table_entry.identifier
        if self.symbol_table.get(identifier) == None: # None, if does not exists.
            self.symbol_table[identifier] = symbol_table_entry
            return True # Successfully added a new symbol table entry
        else:
            existing_symbol_table_entry = self.symbol_table[identifier]
            print(f"Error in line {symbol_table_entry.identifier_token.line_start}. The identifier {symbol_table_entry.identifier} of type {existing_symbol_table_entry.variable_type} is already declared in line {existing_symbol_table_entry.identifier_token.line_start}.")
            return False
        


    def set_new_value_to_variable_in_symbol_table_entry(self, identifier_token: Token, value, node: AST, in_execution: bool) -> bool:

        symbol_table_entry = self.symbol_table.get(identifier_token.lexeme)

        if symbol_table_entry is None:
            print(f"Error in line {identifier_token.line_start}. The identifier {identifier_token.lexeme} is not declared before the assignment.")
            return False
        return symbol_table_entry.set_value(value, node, in_execution)

    
        return True

