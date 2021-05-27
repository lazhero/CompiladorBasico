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
    'INSTANCE',
    'METHOD_CALL_POINT',
    'COMA',
    'RESERVED_FUNC',
    'MAIN_FUNC',
    'PROCEDURE'
   
]
reserved = {
    'if' : 'IF',
    'else' : 'ELSE',
    'for' : 'FOR',
    'in' : 'IN',
    'Step' : 'STEP',
 }
reserved_function_names={
    'blink' : 'BLINK',
    'delay': 'DELAY',
    'printLed' : "PRINT_LED" ,
    'printLedX' : 'PRINT_LED_X'
}
#.get = get()
reserved_methods_names={
    'F':'F_METHOD',
    'T': 'T_METHOD',
    'Neg' : 'NEG',
    'Pene' :'PENE',
    'shapeF' : 'SHAPE_F',
    'shapeC' : 'SHAPE_C',
    'insert' : 'INSERT',
    'delete': 'DELETE',
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
t_METHOD_CALL_POINT=r'\.'
t_COMA=r','

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
'''
@lex.Token(floatnumber)
def t_OPERATOR(t):
    return t
'''
def t_MAIN_FUNC(t):
    r'main'
    return t
def t_PROCEDURE(t):
    r'Procedure'
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
    Func = reserved_function_names.get(t.value,'IDENTIFIER') 
    if(Func!='IDENTIFIER'):
        t.type= 'RESERVED_FUNC'
    
    return t
def t_newline(t):
     r'\n+'
     t.lexer.lineno += len(t.value)


 
 # Error handling rule
def t_error(t):
     print("Illegal character '%s'" % t.value[0])
     t.lexer.skip(1)
 
 # Build the lexer


data = '''
main
'''
lexer = lex.lex()
lexer.input(data)



 
 # Tokenize

while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input 
    print(tok.type,tok.value)
#[[1,2,3],[4,5,6],[7,8,9]]
# 1,2,3#4,5,6#7,8,9
def p_func_custom(p):
    'func : PROCEDURE IDENTIFIER Parameters scope'
    p[0]=['Func',p[1],p[2],p[3]]
def p_func_main(p):
    'func : PROCEDURE MAIN_FUNC Parameters scope'
    p[0]=['Func',p[1],p[2],p[3]]
def p_Parameters(p):
    'Parameters : L_PAREN Params R_PAREN'
    p[0]=['Parameters',p[2]]
def p_Parameters_void(p):
    'Parameters : L_PAREN R_PAREN'
    p[0]=['Parameters',[]]

def p_Params_list(p):
    'Params : Params COMA final_param'
    p[0]=p[1]+[p[3]]
def p_Params_element(p):
    'Params : final_param'
    p[0]=[p[1]]
def p_final_param(p):
    'final_param : iterable'
    p[0]=p[1]


def p_statement_scope(p):
    'statement : scope'
    p[0]=p[1]

def p_statement_conditional(p):
    'statement : IF conditional scope'
    p[0]=[p[1],p[2],p[3]]

def p_statement_conditional_else(p):
    'statement : IF conditional scope ELSE scope'
    p[0]=["IF",p[2],p[3],p[4],p[5]]

def p_conditional(p):
    'conditional : IDENTIFIER COMPARATOR noiterable'
    p[0]= ["CONDITIONAL",p[2], p[1], p[3]]

def p_noiterable_integer(p):
    'noiterable : INTEGER'
    p[0]=p[1]

def p_noiterable_float(p):
    'noiterable : FLOAT'
    p[0]=p[1]

def p_noiterable_boolean(p):
    'noiterable : BOOLEAN'
    p[0]=p[1]

def p_statement_iteracionstep(p):
    'statement : FOR IDENTIFIER IN iterable STEP INTEGER scope'
    p[0]=["FOR",p[2],"IN",p[4],"STEP",p[6],p[7]]

def p_statement_iteracion(p):
    'statement : FOR IDENTIFIER IN iterable scope'
    p[0]=["FOR",p[2],"IN",p[4],"STEP",1,p[5]]


def p_iterable_integer(p):
    'iterable : INTEGER'
    p[0]=p[1]

def p_iterable_identifier(p):
    'iterable : IDENTIFIER'
    p[0]=p[1]

def p_statement_assign_math(p):
    'statement : IDENTIFIER INSTANCE expression EOL'
    p[0]=["ASSIGMENT",p[1],p[3]]
def p_statement_assign_boolean(p):
    'statement : IDENTIFIER INSTANCE BOOLEAN EOL'
    p[0]=["ASSIGMENT",p[1],p[3]]
def p_statement_expression(p):
    'statement : expression EOL'
    p[0]=p[1]
def p_scope(p):
    'scope : UP_SCOPE group DOWN_SCOPE'
    p[0]=["Scope",p[2]]
def p_group(p):
    'group : nombre'
    p[0]=p[1]
def p_nombre_final(p):
    'nombre : statement'
    p[0]=p[1]
def p_nombre_init(p):
    'nombre : statement nombre'
    p[0]=[p[1],p[2]]


def p_expression_plus(p):
     'expression : expression PLUS term'
     p[0] = p[1] + p[3]
 
def p_expression_minus(p):
    'expression : expression MINUS term'
    p[0] = p[1] - p[3]

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_times(p):
    'term : term MULTIPLICATION term2'
    p[0] = p[1] * p[3]
def p_term_leftover(p):
    'term : term LEFTOVER term2'
    p[0]=p[1]%p[3]
def p_term_div(p):
    'term : term DIVIDE term2'
    p[0] = p[1] / p[3]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_integer(p):
    'factor : INTEGER'
    p[0] = p[1]

def p_factor_float(p):
    'factor : FLOAT'
    p[0] = p[1]
def p_factor_expr(p):
    'factor : L_PAREN expression R_PAREN'
    p[0] = p[2]
def p_term_term2(p):
    'term : term2'
    p[0]=p[1]
def p_term2_pow(p):
    'term2 : term2 POW factor2'
    p[0]=p[1]**p[3]
def p_term2_integer_division(p):
    'term2 : term2 INT_DIVISION factor2'
    p[0]=p[1]//p[3]
def p_term2_factor2(p):
    'term2 : factor2'
    p[0] = p[1]
def p_factor2_integer(p):
    'factor2 : INTEGER'
    p[0] = p[1]

def p_factor2_float(p):
    'factor2 : FLOAT'
    p[0] = p[1]
def p_factor2_expr(p):
    'factor2 : L_PAREN expression R_PAREN'
    p[0] = p[2]

def p_term2_factor(p):
    'term2 : factor'
    p[0]=p[1]
# Error rule for syntax errors
def p_error(p):
    print(p)
    print("Syntax error in input!")

 
 # Build the parser

parser = yacc.yacc()
while True:
    try:
        #file=open("fuente.pn",'r')
        #s =file.read()
        #s="{var=12;var1=2**5;}"
        s=input('calc> ')
        print(s)
    except EOFError:
        break
    if not s: continue
    result = parser.parse(s,lexer=lexer)
    print(result)
