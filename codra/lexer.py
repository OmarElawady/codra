import ply.lex as lex
reserved = {
    'for'   : 'FOR',
    'if'    : 'IF',
    'in'    : 'IN',
    'endfor': 'ENDFOR',
    'endif' : 'ENDIF',
    'not'   : 'NOT',
    'or'    : 'OR',
    'and'   : 'AND'
}
tokens = [
'NUMBER',
'STRING',
'DATA',
'ID',
'EQ',
'NEQ',
'LT',
'LE',
'GT',
'GE'
] + list(reserved.values())

literals = '%,+-*/.()[]'
states = (
    ('code', 'exclusive'),
    ('string', 'exclusive')
)

stored_data = ""

def t_escaped(t):
    r'\\{{'
    t.lexer.stored_data += r'\{{'

def t_begin_code(t):
    r'{{'
    t.lexer.begin('code')
    t.type = 'DATA'
    t.value = t.lexer.stored_data
    t.lexer.stored_data = ""
    return t

def t_DATA(t):
    r'.|\n'
    if t.value == '\n':
        t.lexer.lineno += 1
    t.lexer.stored_data += t.value

def t_code_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_code_newlines(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_code_end(t):
    r'}}'
    t.lexer.begin('INITIAL')

def t_code_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')
    return t

def t_code_begin_string(t):
    r'"'
    t.lexer.begin('string')
    t.lexer.matched_string = ""

def t_code_error(t):
    t_error(t)

def t_string_escaped(t):
    r'\\.'
    if t.value[1] == 'n':
        t.lexer.matched_string += '\n'
    elif t.value[1] == 't':
        t.lexer.matched_string += '\t'
    else:
        if t.value[1] == '\n':
            t.lexer.lineno += 1
        t.lexer.matched_string += t.value[1]

def t_string_char(t):
    r'[^"]'
    t.lexer.matched_string += t.value

def t_string_end_string(t):
    r'"'
    t.lexer.begin('code')
    t.type = "STRING"
    t.value = t.lexer.matched_string
    t.lexer.matched_string = ""
    return t

def t_string_error(t):
    print("string error detected: This shouldn't be reached")
    t.lexer.skip(1)

def t_eof(t):
    if t.lexer.stored_data == "":
        return None
    t.type = 'DATA'
    t.value = t.lexer.stored_data
    t.lexer.stored_data = ""
    return t

t_code_ignore = ' \t'
t_code_EQ = r'=='
t_code_NEQ = r'!='
t_code_LE = r'<='
t_code_GT = r'>'
t_code_GE = r'>='
t_code_LT = r'<'

def t_error(t):
     print("Illegal character '%s'" % t.value[0])
     t.lexer.skip(1)

lexer = lex.lex()
lexer.stored_data = ""
if __name__ == '__main__':  
    lexer = lex.lex()
    lexer.stored_data = ""
    lexer.input(data)
    while True:
         tok = lexer.token()
         if not tok:
             break      # No more input
         print(tok)

