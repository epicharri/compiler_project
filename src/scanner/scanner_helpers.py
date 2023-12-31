from src.scanner.token import Token

letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
digits = "0123456789"
identifier_chars = letters + digits + "_"



def is_digit(data: str, i: int):
    if i < len(data) - 1:
        return data[i] in digits

def is_minus_sign(data: str, i: int):
    if i < len(data) - 1:
        return data[i] == '-'

def give_escaped_character(data: str, i: int):
    escaped_characters = {'\\a': '\a', '\\b': '\b', '\\f': '\f', '\\n': '\n', '\\r': '\r', '\\t': '\t', '\\v': '\v', '\\\\': "\\", '\\"': '\"'}
    if i < len(data) - 1:
        if data[i : i + 2] in escaped_characters.keys():
            return escaped_characters[data[i : i + 2]]
    return False

def is_start_of_multiline_comment(data: str, i: int):
    if i < len(data) - 1:
        if data[i] == '/' and data[i+1] == '*':
            return True
    return False

def is_end_of_multiline_comment(data: str, i: int):
    if i < len(data) - 2:
        if data[i] == '*' and data[i+1] == '/':
            return True
    return False

def is_start_of_oneline_comment(data: str, i: int):
    if i < len(data) - 2:
        if data[i] == '/' and data[i+1] == '/':
            return True
    return False

def is_newline(data: str, i: int):
    if i < len(data):
        if data[i] == '\n':
            return True
    return False

def is_quote(data: str, i: int):
    if i < len(data):
        if data[i] == '"':
            return True
    return False

def is_semicolon(data: str, i: int):
    if i < len(data):
        if data[i] == ';':
            return True
    return False

def is_space_or_tab(data: str, i: int):
    if i < len(data):
        if data[i] in [' ', '\t']:
            return True
    return False

def is_letter(data: str, i: int):
    if i < len(data):
        if data[i] in letters:
            return True
    return False

def is_valid_identifier_char(data: str, i: int):
    if i < len(data):
        if data[i] in identifier_chars:
            return True
    return False

# Called after checking the substring starts with a letter.
# Returns range (start, end) of the identifier, i.e. a substring 
# starting with a letter, and including only letters, digits and
# underscores.
def give_range_of_identifier(data: str, i: int):
    start = i
    end = i
    i += 1
    while i < len(data):
        if is_valid_identifier_char(data, i):
            end = i
            i += 1
        else:
            break
    return (start, end)

def is_EOF(data: str, i: int):
    return i >= len(data)

def is_operator(data: str, i: int):
    if i < len(data) - 1:
        return Token.lexeme_is_operator(data[i])
    return None

def is_paren(data: str, i: int):
    if i < len(data) - 1:
        return Token.lexeme_is_parenthesis(data[i])
    return None
    
def is_eos(data: str, i: int):
    if i < len(data):
        if Token.lexeme_is_eos(data[i]):
            return True
    return False
    
def give_separator_token(data: str, i: int):
    if i < len(data):
        if data[i] == ":":
            if i < len(data) - 2 and data[i + 1] == '=':
                return Token.create_assignment_token(i, i + 2) 
            else:
                return Token.create_colon_token(i, i + 1) 
        elif is_eos(data, i):
            return Token.create_eos_token(i, i + 1) 
        elif data[i] == '.':
            if i < len(data) - 2 and data[i + 1] == '.':
                return Token.create_range_separator_token(i, i + 2) 
            else:
                return Token.create_error_token('.', "Illegal token '.'", i, i + 1)  
        else:
            return None
    return None

def give_operator_token(data: str, i: int):
    if is_operator(data, i):
        return Token.create_operator_token(data[i], i, i + 1)
    else:
        return None

def give_eof_token(data: str, i: int):
    if is_EOF(data, i):
        return Token.create_eof_token(i, i + 1) 
    else:
        return None

def give_parens_token(data: str, i: int):
    if is_paren(data, i):
        return Token.create_parenthesis_token(data[i], i, i + 1)
    else:
        return None

def give_identifier_or_keyword_token(data: str, i: int):
    if is_letter(data, i):
        range_of_identifier = give_range_of_identifier(data, i)
        the_identifier = data[range_of_identifier[0]: range_of_identifier[1] + 1]
        if Token.lexeme_is_variable_type(the_identifier):
            return Token.create_variable_type_token(the_identifier, i, i + len(the_identifier))
        elif Token.lexeme_is_keyword(the_identifier):
            return Token.create_keyword_token(the_identifier, i, i + len(the_identifier)) 
        else:
            return Token.create_identifier_token(the_identifier, i, i + len(the_identifier)) 
    else:
        return None

def give_string_literal_token(data: str, i: int):
    if is_quote(data, i):
        the_string_literal = ""
        k = i
        literal_start = k + 1
        literal_end = k
        k += 1
        while k < len(data):
            escaped_char = give_escaped_character(data, k)
            if escaped_char:
                    the_string_literal += escaped_char
                    k += 2
            elif is_newline(data, k):
                the_start = literal_start
                the_end = k + 1
                return (Token.create_error_token("", "A newline inside a string literal.", the_start, the_end), True)

            elif data[k] == '"':
                return (Token.create_string_literal_token(the_string_literal, i, k + 1), False)
            else:
                the_string_literal += data[k]
                k += 1
        return None
    return None

def give_integer_token(data: str, i: int):
    if is_digit(data, i): # In MiniPL, an integer literal is a sequence of decimal digits. Thus, negative integer literals are not supported.
        k = i
        literal_start = k
        literal_end = k + 1
        k += 1
        while k < len(data):
            if not is_digit(data, k):
                literal_end = k
                the_integer_literal = data[literal_start:literal_end]
                return Token.create_integer_literal_token(the_integer_literal, i, literal_end) 
            k += 1
        return None           
    return None

