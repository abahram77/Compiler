import string

code_string = "if (b == 3){" \
              "a= 3;" \
              "cd!e = -7;" \
              "else" \
              "return;"

# code_string = 'b != a'
code_pointer = 0
token = []
symbols = ['{', '}', ';', ':', ',', '(', ')', '&', '*', '=', '+', '%', '^', '|', '/', '>', '<', '~', '[', '[', '"',
           "'", '-', '?']
dict
symbol_permutations = {'&': ['&', '='], '=': ['='], '+': ['+', '='], '-': ['-', '='], '%': ['='], '*': ['*', '='],
                       '|': ['|', '='], '/': ['='], '>': ['>', '='], '<': ['<', '='], '~': ['='], '^': ['='],
                       '>>': ['='], '<<': ['='], '{': [], '}': [], ':': [], ';': [], ',': [], '(': [], ')': [],
                       '!=': [], '[': [], ']': [], '"': [], "'": [], '?': []}

key_words = ['auto', 'break', 'case', 'char',
             'const', 'continue', 'default', 'do',
             'double', 'else', 'enum', 'extern',
             'float', 'for', 'goto', 'if',
             'int', 'long', 'register', 'return',
             'short', 'signed', 'sizeof', 'static',
             'struct', 'switch', 'typedef', 'union',
             'unsigned', 'void', 'volatile', 'while']
letter = string.ascii_letters
digit = [str(i) for i in range(10)]
space = ['\n', '\t', ' ']
valid_token = True
token_list = []
error_list = []


def SymNumIdKeySpace(not_used):
    global new_state, code_pointer, valid_token
    char = code_string[code_pointer]
    code_pointer += 1
    if char in symbols:
        new_state = ['symbol', char]
        return char

    if char in space:
        new_state = ['end_of_token', ' ']
        return ''

    if char in digit:
        new_state = ['number', ' ']
        return char

    if char in letter:
        new_state = ['IdKey', ' ']
        return char

    if char == '!' and code_pointer < len(code_string) and code_string[code_pointer] == '=':
        code_pointer += 1
        new_state = ['symbol', '!=']
        return '!='

    valid_token = False
    return char


def IdKey(not_used):
    global new_state, code_pointer, valid_token
    char = code_string[code_pointer]

    if (char in space) or (char in symbols):
        new_state = ['end_of_token', ' ']
        return ''

    if (char in digit) or (char in letter):
        code_pointer += 1
        return char

    valid_token = False
    code_pointer += 1
    return char


def number(not_used):
    global new_state, code_pointer, valid_token
    char = code_string[code_pointer]

    if (char in space) or (char in symbols):
        new_state = ['end_of_token', ' ']
        return ''

    if char in digit:
        code_pointer += 1
        return char

    valid_token = False
    code_pointer += 1
    return char


def symbol(pre_char):
    token = ''
    global code_pointer, new_state
    char = code_string[code_pointer]
    if char in symbol_permutations.get(pre_char):
        token += char
        code_pointer += 1

        if code_pointer < len(code_string) and (char == '>' or char == '<'):
            char = code_string[code_pointer]
            if char == '=':
                token += char
                code_pointer += 1

    new_state = ['end_of_token', ' ']
    return token


def get_next_token():
    global token_list, valid_token, error_list, new_state
    acceptable_state = [None, ' ']
    new_state = ['SymNumIdKeySpace', ' ']
    token = ''

    while code_pointer < len(code_string):
        while new_state[0] != 'end_of_token':
            if code_pointer < len(code_string):
                acceptable_state = new_state
                # print(acceptable_state[0] + '(' + acceptable_state[1] + ')')
                token += eval(acceptable_state[0] + "('" + acceptable_state[1] + "')")
            else:
                acceptable_state = new_state
                break

        if valid_token:
            if acceptable_state[0] == 'IdKey':
                acceptable_state[0] = 'ID'
                if token in key_words:
                    acceptable_state[0] = 'keyword'
            if token != '':
                token_list += [(acceptable_state[0], token)]

        else:
            error_list += [('invalid input', token)]

        token = ''
        valid_token = True
        acceptable_state = [None, ' ']
        new_state = ['SymNumIdKeySpace', ' ']


get_next_token()
print(token_list, error_list)
