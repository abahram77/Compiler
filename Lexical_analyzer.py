import string
import grammer
import firstFollows
import sys

sys.setrecursionlimit(10000000)

file_name = './test_case/testcase_7.txt'
input_file = open(file_name, mode='r')
code_string_all = input_file.read()

parser_file_name = './res/parser.txt'
parser_file = open(parser_file_name, mode='w')
error_file_name = './res/error.txt'
error_file = open(error_file_name, mode='w')

code_pointer = 0

code_line = 1
symbols = ['{', '}', ';', ':', ',', '(', ')', '&', '*', '=', '+', '%', '^', '|', '/', '>', '<', '~', '[', '[', '"',
           "'", '-', '?']

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
        new_state = ['num', ' ']
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


def num(not_used):
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
                acceptable_state[0] = 'id'
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
    global code_line
    res = None
    while res is None:
        res = make_next_token()
    if res[0][1] == 'invalid input':
        error_file.write(str(code_line) + ' : Lexical Error! invalid input ' + res[0][0] + '\n')
    return res


def convert_token(token):
    if token[0] == 'symbol' or token[0] == 'keyword':
        return token[1]
    return token[0]


def print_tree(depth, state):
    for i in range(depth):
        parser_file.write('|')
    parser_file.write(state + '\n')


terminals = ['id', 'num'] + symbols + key_words
transition_diagram = grammer.get_grammer()
first = firstFollows.get_first()
follow = firstFollows.get_follow()
print("transition", transition_diagram)
print("first", first)
print("follow", follow)

for terminal in terminals:
    first[terminal] = [terminal]
    follow[terminal] = []

stack = ['Program']
depths = [0]



def parser(token):
    global stack, depths
    print("stack is !", stack[::-1])
    if token == 'EOF' and len(stack) > 1:
        error_file.write(str(code_line) + ' : Syntax Error! Malformed Input\n')
        return False

    if len(stack) == 1 and stack[0] == 'EOF':
        return True

    state = stack.pop()
    depth = depths.pop()
    print_tree(depth, state)

    if state in terminals:
        if state != token:
            error_file.write(str(code_line) + ' : Syntax Error! Missing ' + state + '\n')
            return parser(token)

        next_token_ = get_next_token()[0]
        next_token_ = convert_token(next_token_)
        return parser(next_token_)
    # print('error', state, first.get(state), follow.get(state))
    if token in first.get(state) or token in follow.get(state):
        for way in transition_diagram.get(state):
            # print("this", first.get(way[0]), way)
            if way == [] or token in first.get(way[0]) or ('ep' in first.get(way[0]) and token in follow.get(way[0])):
                stack += way[::-1]
                depths += [depth + 1 for i in range(len(way))]
                return parser(token)

        if token in follow.get(state):
            error_file.write(str(code_line) + ' : Syntax Error! Missing ' + state + '\n')
            return parser(token)

    error_file.write(str(code_line) + ' : Syntax Error! Unexpected ' + token + '\n')
    stack += [state]
    depths += [depth]
    next_token_ = get_next_token()[0]
    next_token_ = convert_token(next_token_)
    return parser(next_token_)


next_token = get_next_token()[0]
next_token = convert_token(next_token)
parser(next_token)
