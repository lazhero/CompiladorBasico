# ------------------------------------------------------------
 # calclex.py
 #
 # tokenizer for a simple expression evaluator for
 # numbers and +,-,*,/
 # ------------------------------------------------------------
from tokenize import Token
import ply.lex as lex
import ply.yacc as yacc
from ply.ctokens import tokens
 
 # List of token names.   This is always required
tokens = [
    'INTEGER',
    'FLOAT',
    'BOOLEAN',
    'PLUS',
    'MINUS',
    'MULTIPLICATION',
    'POW',
    'DIVIDE',
    'LEFTOVER',
    'INT_DIVISION',
    'OPERATOR',
    'COMPARATOR',
    'L_PAREN',
    'R_PAREN',
    'L_SQUARE_PAREN',
    'R_SQUARE_PAREN',
    'UP_SCOPE',
    'DOWN_SCOPE',
    'IDENTIFIER',
    'COMMENT',
    'EOL',
    'INSTANCE'
   
]
reserved = {
    'if' : 'IF',
    'else' : 'ELSE',
    'for' : 'FOR',
 }
tokens=list(reserved.values())+tokens

 # Regular expression rules for simple tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_MULTIPLICATION   = r'\*'
t_DIVIDE  = r'/'
t_INT_DIVISION = r'//'
t_LEFTOVER = r'%'
t_L_PAREN  = r'\('
t_R_PAREN  = r'\)'
t_L_SQUARE_PAREN = r'\['
t_R_SQUARE_PAREN = r'\]'
t_UP_SCOPE=r'{'
t_DOWN_SCOPE=r'}'
t_POW=r'\*\*'
t_ignore  = ' \t'
t_EOL=r';'
t_INSTANCE=r'='

#Some complex regex
digit            = r'([0-9])'
nonzerodigit =   r'([1-9])'
nondigit         = r'([_A-Za-z])'
floatnumber =r'(    '+r'(' +nonzerodigit+ r'\.'+r'(' +digit+r')+'+ r')' + r'|' r'(' + r'(' +digit+r')+'+r'\.'+r'(' +digit+r')+'+r')'  +r')'
identifier       = r'(' + nondigit + r'(' + digit + r'|' + nondigit + r')*)'
boolean=r'TRUE'+r'|'+r'FALSE'
multiplication=r'\*'
division=r'/'
plus=r'\+'
minus=r'-'
int_division=r'//'
leftover=r'%'
equals=r'=='
lower=r'<'
higher=r'>'
lower_or_equal=r'<='
higher_or_equal=r'>='
pow=r'\*\*'
operators=r'('+pow+r'|'+multiplication+r'|'+division+r'|'+int_division+r'|'+leftover+r'|'+plus+r'|'+minus+r')'
comparator=r'('+equals+r'|'+lower+r'|'+lower_or_equal+r'|'+higher+r'|'+higher_or_equal+r')'
@lex.Token(comparator)
def t_COMPARATOR(t):
    return t
@lex.Token(floatnumber)
def t_OPERATOR(t):
    return t
@lex.Token(boolean)
def t_BOOLEAN(t):
    return t
@lex.Token(floatnumber)
def t_FLOAT(t):
    t.value=float(t.value)
    return t
def t_INTEGER(t):
     r'\d+'
     t.value = int(t.value)    
     return t
def t_COMMENT(t):
    r'\#\#.*'
    pass

@lex.TOKEN(identifier)
def t_IDENTIFIER(t):
    t.type = reserved.get(t.value,'IDENTIFIER')    # Check for reserved words
    return t
def t_newline(t):
     r'\n+'
     t.lexer.lineno += len(t.value)
 

 
 # Error handling rule
def t_error(t):
     print("Illegal character '%s'" % t.value[0])
     t.lexer.skip(1)
 
 # Build the lexer
lexer = lex.lex()
data = '''
Var=2;
'''
lexer.input(data)



 
 # Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input 
    print(tok.type,tok.value)
def p_statement(p):
    'statement : expression EOL'
    p[0]=p[1]
def p_expression_operation(p):
    'expression : expression operations term'
    p[0]=["BinaryOperation",p[2],p[1],p[3]]
def p_expression_term(p):
    'expression : term'
    p[0]=p[1]
def p_term_float(p):
    'term : FLOAT'
    p[0]=p[1]
def p_term_integer(p):
    'term : INTEGER'
    p[0]=p[1]
def p_term_identificator(p):
    'term : IDENTIFIER'
    p[0]=p[1]
def p_term_expression(p):
    'term : L_PAREN expression R_PAREN'
    p[0]=p[2]

def p_operations_addition(p):
    'operations : PLUS'
    p[0]=p[1]
def p_operations_substraction(p):
    'operations : MINUS'
    p[0]=p[1]
def p_operations_leftover(p):
    'operations : LEFTOVER'
    p[0]=p[1]
def p_operations_division(p):
    'operations : DIVIDE'
    p[0]=p[1]
def p_operations_division_integer(p):
    'operations : INT_DIVISION'
    p[0]=p[1]
def p_operations_multiplication(p):
    'operations : MULTIPLICATION'
    p[0]=p[1]
def p_operations_pow(p):
    'operations : POW'
    p[0]=p[1]
def p_expresions_comparator(p):
    'expression : expression COMPARATOR term'
    p[0]=["BinaryComparator",p[2],p[1],p[3]]

def p_error(p):

    print(p)
    print("Syntax error in input!")
 
 # Build the parser
parser = yacc.yacc()


while True:
    try:
        s = input('calc > ')
    except EOFError:
        break
    if not s: continue
    result = parser.parse(s)
    print(result)
