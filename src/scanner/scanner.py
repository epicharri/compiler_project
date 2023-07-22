from src.scanner.scanner_helpers import * # is_end_of_multiline_comment, is_escaped_quote, is_newline, is_start_of_multiline_comment, is_end_of_multiline_comment, is_start_of_oneline_comment, is_quote, is_semicolon, is_space_or_tab
from src.parameters import Parameters
from src.scanner.token import Token
# from src.scanner.token import STRING

class Scanner:
    def __init__(self, raw_data: str, parameters):
        self.raw_data = raw_data
        self.i = 0
        self.data = ""
        self.string_literals = []
        self.tokens = []
        # self.last_token_is_consumed = True
        self.current_raw_data_line = 1 # Numbering of lines starts from 1.
        self.current_raw_data_line_start_index = 0
        self.errors_found = False
        self.parameters = parameters
        self.last_error_printed_in_tokens_index = -2

    def skip_spaces_and_tabs(self):
        self.i += 1
        while is_space_or_tab(self.raw_data, self.i):
            self.i += 1
        

    def skip_multiline_comment(self):
        count_multiline_comment_blocks = 1
        self.i += 2
        while self.i < len(self.raw_data):
            if is_newline(self.raw_data, self.i):
                self.i += 1
                self.current_raw_data_line += 1
                self.current_raw_data_line_start_index = self.i
            elif is_start_of_multiline_comment(self.raw_data, self.i):
                self.i += 2 #
                count_multiline_comment_blocks += 1
            elif is_end_of_multiline_comment(self.raw_data, self.i):
                self.i += 2
                count_multiline_comment_blocks -= 1
                if count_multiline_comment_blocks == 0:
                    break
            else:
                self.i += 1


    def skip_oneline_comment(self):
        self.i += 2
        while self.i < len(self.raw_data):
            if is_newline(self.raw_data, self.i):
                self.current_raw_data_line += 1
                self.i += 1
                break
            self.i += 1

    def print_error_if_any(self):
        if self.last_error_printed_in_tokens_index == len(self.tokens) - 1:
            return
        if len(self.tokens) > 0:
            error_token = self.tokens[-1]
            if error_token.is_error_token():
                print(f"Error found during tokenization in line {self.current_raw_data_line}:", error_token.lexeme)
                self.errors_found = True
                self.last_error_printed_in_tokens_index = len(self.tokens) - 1


    def append_token(self, token: Token):
        self.i = token.end
        self.tokens.append(token)
        self.parameters.print_token(token)
        self.print_error_if_any()



    def get_next_token(self):
        return self.scan_next_token()

    def scan_next_token(self):
        start_of_code_line = 0
        if type(self.i) == str:
            print(f"PANIC!!! self.i = {self.i}")
        while self.i < len(self.raw_data):
            if is_newline(self.raw_data, self.i):
                self.current_raw_data_line += 1
                self.i += 1
                self.current_raw_data_line_start_index = self.i
                continue
                
            if is_space_or_tab(self.raw_data, self.i):
                self.skip_spaces_and_tabs()
                continue
            if is_start_of_multiline_comment(self.raw_data, self.i):
                self.skip_multiline_comment()
                continue
            if is_start_of_oneline_comment(self.raw_data, self.i):
                self.skip_oneline_comment()
                continue
            token_and_error_code = give_string_literal_token(self.raw_data, self.i)
            if (token_and_error_code):
                (token, error) = token_and_error_code
                if (error): # Newline inside the string literal
                    token.line_start = self.current_raw_data_line
                    self.current_raw_data_line += 1
                    self.current_raw_data_line_start_index = self.i
                    self.append_token(token)
                    return token
                elif (token):
                    token.line_start = self.current_raw_data_line
                    self.append_token(token)
                    return token
                
            token = give_identifier_or_keyword_token(self.raw_data, self.i)
            if (token):
                token.line_start = self.current_raw_data_line
                self.append_token(token)
                return token
            token = give_operator_token(self.raw_data, self.i)
            if (token):
                token.line_start = self.current_raw_data_line
                self.append_token(token)
                return token
            token = give_parens_token(self.raw_data, self.i)
            if (token):
                token.line_start = self.current_raw_data_line
                self.append_token(token)
                return token
            token = give_separator_token(self.raw_data, self.i)
            if (token):
                token.line_start = self.current_raw_data_line
                self.append_token(token)
                return token
            token = give_integer_token(self.raw_data, self.i)
            if (token):
                token.line_start = self.current_raw_data_line
                self.append_token(token)
                return token              
            else:
                token = Token.create_error_token(self.raw_data[self.current_raw_data_line_start_index:self.i + 1], f"Error in line {self.current_raw_data_line}, found in the end of this: {self.raw_data[self.current_raw_data_line_start_index:self.i + 1]}", self.i, self.i + 1)
                # token = Token(ERROR, f"Error in line {self.current_raw_data_line}, found in the end of this: {self.raw_data[self.current_raw_data_line_start_index:self.i + 1]}", self.i, self.i + 1)
                token.line_start = self.current_raw_data_line
                self.append_token(token)
                self.i += 1
                self.errors_found = True
                return token
        if len(self.tokens) > 0 and (not self.tokens[-1].is_eof_token()):
            token = give_eof_token(self.raw_data, self.i)
            if (token):
                token.line_start = self.current_raw_data_line
                self.append_token(token)
                return token
        return None
                

 

