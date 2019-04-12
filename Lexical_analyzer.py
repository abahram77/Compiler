import string

code_string = "void main() {}"
code_pointer = 0
# States: state_
token = []
symbol = ['{', '}', ';', ':', ',', '(', ')', '&', '*', '=', '+', '%', '^', '!', '|', '/', '>', '<', '~', '[', '[', '"',
          0
          "'", '-', '?']
dict
symbol_permutations = {'&': ['&', '='], '=': ['='], '+': ['+', '='], '-': ['-', '='], '%': ['='], '*': ['*', '='],
                       '|': ['|', '='], '/': ['='], '>': ['>', '='], '<': ['<', '='], '~': ['='], '^': ['='],
                       '>>': ['='], '<<': ['=']}

letter = string.ascii_letters
digit = [str(i) for i in range(10)]
space = ['\n', '\t', ' ']


def SymNumIdKeySpace(not_used):
    global new_state
    char = code_string[code_pointer]
    if char in symbol:
        new_state = ['symbol', char]

        return

        # TODO: under construction


def symbol(char):
    char = code_string[code_pointer]
    if char in symbol_permutations.get(char):



def get_next_token():
    acceptable_state = [None, None]
    new_state = ['SymNumIdKeySpace', ' ']
    while new_state != 'error_state':
        acceptable_state = new_state
        eval(acceptable_state[0] + '(' + acceptable_state[1] + ')')


print(letter)
