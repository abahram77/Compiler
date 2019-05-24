import string

file_name = 'testcase_3.txt'
input_file = open(file_name, mode='r')
code_string_all = input_file.read()

scanner_file_name = './scanner.txt'
scanner_file = open(scanner_file_name, mode='w')
lexical_file_name = './lexical_errors.txt'
error_file = open(lexical_file_name, mode='w')

code_pointer = 0

code_line = 1
symbols = ['{', '}', ';', ':', ',', '(', ')', '&', '*', '=', '+', '%', '^', '|', '/', '>', '<', '~', '[', '[', '"',
           "'", '-', '?']
dict
symbol_permutations = {'&': ['&', '='], '=': ['='], '+': ['+', '='], '-': ['-', '='], '%': ['='], '*': ['*', '='],
                       '|': ['|', '='], '/': ['=', '/', '*'], '>': ['>', '='], '<': ['<', '='], '~': ['='], '^': ['='],
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
    global new_state, code_pointer, valid_token, code_line
    char = code_string_all[code_pointer]
    code_pointer += 1
    if char in symbols:
        new_state = ['symbol', char]
        return char

    if char in space:
        if char == '\n':
            code_line += 1

        new_state = ['end_of_token', ' ']
        return ''

    if char in digit:
        new_state = ['number', ' ']
        return char

    if char in letter:
        new_state = ['IdKey', ' ']
        return char

    if char == '!' and code_pointer < len(code_string_all) and code_string_all[code_pointer] == '=':
        code_pointer += 1
        new_state = ['symbol', '!=']
        return '!='

    valid_token = False
    return char


def IdKey(not_used):
    global new_state, code_pointer, valid_token, code_line
    char = code_string_all[code_pointer]

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
    global new_state, code_pointer, valid_token, code_line
    char = code_string_all[code_pointer]

    if (char in space) or (char in symbols):
        new_state = ['end_of_token', ' ']
        return ''

    if char in digit or char == ".":
        code_pointer += 1
        return char

    valid_token = False
    code_pointer += 1
    return char


def symbol(pre_char):
    token = ''
    global code_pointer, new_state
    char = code_string_all[code_pointer]
    if char in symbol_permutations.get(pre_char):
        token += char
        code_pointer += 1

        if code_pointer < len(code_string_all) and (char == '>' or char == '<'):
            char = code_string_all[code_pointer]
            if char == '=':
                token += char
                code_pointer += 1

        if char == '/':
            new_state = ['one_line_comment', ' ']
            return ''

        if pre_char == '/' and char == '*':
            new_state = ['multi_line_comment', ' ']
            return ''

    new_state = ['end_of_token', ' ']
    return token


def one_line_comment(not_used):
    global code_string_all, code_pointer, new_state, code_line
    char = code_string_all[code_pointer]
    code_pointer += 1
    if char == '\n':
        code_line += 1
        new_state = ['end_of_token']
        return ''

    return ''


def multi_line_comment(not_used):
    global code_string_all, code_pointer, new_state, valid_token, code_line
    valid_token = False
    char = code_string_all[code_pointer]
    if char == '\n':
        code_line += 1
    code_pointer += 1
    if char == '*':
        if code_pointer < len(code_string_all):
            if code_string_all[code_pointer] == '/':
                valid_token = True
                code_pointer += 1
                new_state = ['end_of_token', ' ']
                return ''
    return ''


pre_line_state = 'SymNumIdKeySpace'


def make_next_token():
    global token_list, valid_token, error_list, new_state, pre_line_state
    if code_pointer < len(code_string_all):
        if pre_line_state == 'multi_line_comment':
            init_state = ['multi_line_comment', ' ']
        else:
            init_state = ['SymNumIdKeySpace', ' ']

        acceptable_state = [[None, ' ']]
        new_state = init_state
        valid_token = True
        token = ''

        while new_state[0] != 'end_of_token':
            if code_pointer < len(code_string_all):
                acceptable_state = new_state
                token += eval(acceptable_state[0] + "('" + acceptable_state[1] + "')")
            else:
                acceptable_state = new_state
                if new_state[0] == 'multi_line_comment':
                    return new_state[0]
                break

        if valid_token:
            if acceptable_state[0] == 'IdKey':
                acceptable_state[0] = 'ID'
                if token in key_words:
                    acceptable_state[0] = 'keyword'
            if token != '' and acceptable_state[0] != 'one_line_comment' and acceptable_state[0] \
                    != 'multi_line_comment':
                token_list += [(acceptable_state[0], token)]
                return [(acceptable_state[0], token)]

        else:
            if new_state[0] == 'multi_line_comment':
                error_list += [('/*', 'invalid input')]
                return [('/*', 'invalid input')]
            else:
                error_list += [(token, 'invalid input')]
                return [(token, 'invalid input')]
    else:
        return [('EOF', 'EOF')]


def get_next_token():
    res = None
    while res is None:
        res = make_next_token()
    return res


def output_form_converter(token):
    output = []
    for t in token:
        output += ['(' + t[0] + ', ' + t[1] + ')']
    return output


token = get_next_token()
while token != [('EOF', 'EOF')]:
    scanner_file.write(str(code_line) + str(token[0]) + '\n')
    token = get_next_token()
