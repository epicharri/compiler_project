

class Parameters:
    def __init__(self):
        self.print_debug_info = False
        self.print_tokens = False
        self.print_ast = False
        self.print_symbol_table = False
    
    def set_print_debug_info(self):
        self.print_debug_info = True
    
    def set_print_tokens(self):
        self.print_tokens = True
    
    def set_print_ast(self):
        self.print_ast = True

    def set_print_symbol_table(self):
        self.print_symbol_table = True
    
    def print_debug_info(self, msg: str):
        if self.print_debug_info:
            print(msg)
  
    def print_token(self, token: str):
        if self.print_tokens:
            print(token)