data = r"""
Hello, My name is {{ omar }}
my parent name is {{ parent.name }}
I want to condition on something
{{ if count == 1 }}
this is data
{{ omar.parent[name] }}
this is another data
{{ endif }}


and finally this is for loops:
{{ for var in range(1, 5) }}
data inside the loop
{{ var + 1 }}

{{ endfor }}

conditioning on string
{{ if name == "o\"omar'\qmar" }}
yay!
{{ endif }}
"""
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
    t.lexer.stored_data += t.value

def t_code_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

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

t_code_ignore = ' \n\t'
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

