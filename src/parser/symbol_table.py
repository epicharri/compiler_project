from src.scanner.token import Token

VAR_INTEGER, VAR_STRING, VAR_BOOL = "VAR_INTEGER", "VAR_STRING", "VAR_BOOL"

class SymbolTableEntry():
    def __init__(self, token: Token):
        self.symbol = "" # Variable IDENTIFIER
        self.type = None # Types are: VAR_INTEGER, VAR_STRING, VAR_BOOL 
        self.value = None # Value is: int, str, or bool. For example, 275, "something", False
        self.token = token # Here is also the information of the line the token has been declared.

    def set_symbol_and_type(self, symbol: str, type: str, token: Token):
        if symbol == VAR_INTEGER:
            self.symbol = symbol
            self.type = VAR_INTEGER
            self.value = 0 # Default value for integers
            self.token = token
        elif symbol == VAR_STRING:
            self.symbol = symbol
            self.type = VAR_STRING
            self.value = "" # Default value for strings
            self.token = token
        elif symbol == VAR_BOOL:
            self.symbol = symbol
            self.type = VAR_BOOL
            self.value = False # Default value for booleans is False
            self.token = token
        else:
            print(f"ERROR: Wrong type {type}")

    def set_value(self, symbol: str, value):
        if symbol == VAR_INTEGER:
            if type(value) == str:
                self.value = int(value)
            elif type(value) == int:
                self.value = value
        elif symbol == VAR_STRING:
            self.value = value
        elif symbol == VAR_BOOL:
            if type(value) == bool:
                self.value = value
            else:
                print("Value for boolean must be True of False.")
        else:
            print(f"ERROR: Wrong type {type}")

class SymbolTable():
    def __init__(self):
        self.symbol_table = {} 
        # key: identifier, value: SymbolTableEntry object
        # types are INTEGER, STRING, and BOOL
        # values are stored as integers, strings and booleans (True or False).
        # Default integer value is 0, default string value is "", and default boolean value is false.
    
    def get_type_and_value(self, symbol) -> tuple:
        type_and_value = self.symbol_table.get(symbol)
        return type_and_value # Returns None, if the key does not exist, otherwise returns (type, value)
    
    def add_new_symbol_and_type(self, symbol, type):
        type_and_value = self.type_and_value(symbol)
        if (type_and_value):
            print(f"Error: symbol {symbol} already exists with type {type_and_value[0]} and value {type_and_value[1]}")
            return None
        self.symbol_table[symbol] = ()