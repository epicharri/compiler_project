from src.scanner.token import Token

class SymbolTableEntry():
    def __init__(self, identifier_token: Token, variable_type_token: Token, assigned_value_token = None):
        self.identifier_token = identifier_token
        self.variable_type_token = variable_type_token
        self.assigned_value_token = assigned_value_token
        self.identifier = identifier_token.lexeme # Variable IDENTIFIER
        self.variable_type = variable_type_token.lexeme # Types are: int, string, bool
        self.value = None # Value is: int, str, or bool. For example, 275, "something", False
        if self.identifier_token.is_identifier_token():
            if self.variable_type_token.is_int_token():
                self.value = 0
            elif self.variable_type_token.is_string_token():
                self.value = ""
            elif self.variable_type_token.is_bool_token():
                self.value = False 
    
    def __repr__(self):
        return f"({self.identifier}, {self.variable_type}, {self.value})"

class SymbolTable():
    def __init__(self):
        self.symbol_table = {} 
        # key: identifier, value: SymbolTableEntry object
        # types are INTEGER, STRING, and BOOL
        # values are stored as integers, strings and booleans (True or False).
        # Default integer value is 0, default string value is "", and default boolean value is False.

    def exists_in_symbol_table(self, identifier_token: Token):
        symbol_table_entry = self.symbol_table.get(identifier_token.lexeme)
        if symbol_table_entry == None:
            return False
        return True

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


    def set_new_value_to_variable_in_symbol_table_entry(self, identifier_token: Token, value) -> bool:
        symbol_table_entry = self.symbol_table.get(identifier_token.lexeme)
        types = {"<class 'int'>": 'int', "<class 'str'>": 'string', "<class 'bool'>": 'bool'}

        if symbol_table_entry == None:
            print(f"Error in line {identifier_token.line_start}. The identifier {identifier_token.lexeme} is not declared before the assignment.")
            return False
        if types[str(type(value))] != symbol_table_entry.variable_type:
            print(f"Error in line {identifier_token.line_start}. The identifier {identifier_token.lexeme} is of type {identifier_token.lexeme}, but the value assigned is of type {types[str(type(value))]}.")
            return False
        symbol_table_entry.value = value
        return True

