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
    'RESERVED_METHOD',
    'MAIN_FUNC',
    'PROCEDURE',
    'COLON'
   
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
    'printLedX' : 'PRINT_LED_X',
    'range' : 'RANGE',
    'list'  : 'LIST',
    'type' : 'TYPE',
    'len': 'LEN',
}
#.get = get()
reserved_methods_names={
    'F':'F_METHOD',
    'T': 'T_METHOD',
    'Neg' : 'NEG',
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
t_COLON=r':'

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
    Method=reserved_methods_names.get(t.value,'IDENTIFIER')
    if(Func!='IDENTIFIER'):
        t.type= 'RESERVED_FUNC'
    if(Method!='IDENTIFIER'):
        t.type='RESERVED_METHOD'
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
mylexer = lex.lex()
mylexer.input(data)



 


while True:
    tok = mylexer.token()
    if not tok: 
        break 
    print(tok.type,tok.value)



def p_func_custom(p):
    'func : PROCEDURE IDENTIFIER Arguments scope'
    p[0]=["PROCEDURE",p[2],p[3],p[4]]
def p_func_main(p):
    'func : PROCEDURE MAIN_FUNC Arguments scope'
    p[0]=['MAIN_FUNC',p[1],p[2],p[3]]



def p_Arguments(p):
    'Arguments : L_PAREN args R_PAREN'
    p[0]=['ARGUMENTS',p[2]]
def p_Arguments_void(p):
    'Arguments : L_PAREN R_PAREN'
    p[0]=['ARGUMENTS',[]]
def p_args_list(p):
    'args : args COMA final_arg'
    p[0]=p[1]+[p[3]]
def p_args_element(p):
    'args : final_arg'
    p[0]=[p[1]]
def p_final_arg(p):
    'final_arg : iterable'
    p[0]=p[1]


def p_Parameters(p):
    'Parameters : L_PAREN params R_PAREN'
    p[0]=['PARAMETERS',p[2]]
def p_Parameters_void(p):
    'Parameters : L_PAREN R_PAREN'
    p[0]=['PARAMETERS',[]]
def p_params_list(p):
    'params : params COMA final_param'
    p[0]=p[1]+[p[3]]
def p_params_element(p):
    'params : final_param'
    p[0]=[p[1]]
def p_final_param_iterable(p):
    'final_param : iterable'
    p[0]=p[1]
def p_final_param_noiterable(p):
    'final_param : noiterable'
    p[0]=p[1]
def p_final_param_list(p):
    'final_param : list'
    p[0]=p[1]





def p_statement_scope(p):
    'statement : scope'
    p[0]=p[1]
def p_statement_conditional(p):
    'statement : IF conditional scope'
    p[0]=[p[1],p[2],p[3]]
def p_statement_functioncall(p):
    'statement : functioncall EOL'
    p[0]=p[1]
def p_statement_methodcall(p):
    'statement : methodcall EOL'

def p_functioncall(p):
    'functioncall : IDENTIFIER Parameters'
    p[0] = ["CALL_FUNC",p[1],p[2]]
def p_methodcall(p):
    'methodcall : IDENTIFIER METHOD_CALL_POINT IDENTIFIER Parameters'
    p[0] = ["METHOD_CALL",p[1],p[3],p[4]]
def p_methodcall_list(p):
    'methodcall : access_list METHOD_CALL_POINT IDENTIFIER Parameters'
    p[0] = ["METHOD_CALL",p[1],p[3],p[4]]
def p_statement_conditional_else(p):
    'statement : IF conditional scope ELSE scope'
    p[0]=["IF",p[2],p[3],p[4],p[5]]
def p_conditional(p):
    'conditional : IDENTIFIER COMPARATOR noiterable'
    p[0]= ["CONDITIONAL",p[2], p[1], p[3]]
def p_statement_iteracionstep(p):
    'statement : FOR IDENTIFIER IN iterable STEP INTEGER scope'
    p[0]=["FOR",p[2],"IN",p[4],"STEP",p[6],p[7]]
def p_statement_iteracion(p):
    'statement : FOR IDENTIFIER IN iterable scope'
    p[0]=["FOR",p[2],"IN",p[4],"STEP",1,p[5]]
def p_statement_assign_math(p):
    'statement : IDENTIFIER INSTANCE expression EOL'
    p[0]=["ASSIGMENT",p[1],p[3]]
def p_statement_assign_access_list(p):
    'statement : IDENTIFIER INSTANCE access_list EOL'
    p[0]=["ASSIGMENT",p[1],p[3]]
def p_statement_assign_boolean(p):
    'statement : IDENTIFIER INSTANCE BOOLEAN EOL'
    p[0]=["ASSIGMENT",p[1],p[3]]
def p_statement_assign_boolean(p):
    'statement : IDENTIFIER INSTANCE list EOL'
    p[0]=["ASSIGMENT",p[1],p[3]]
def p_statement_assing_method(p):
    'statement : IDENTIFIER INSTANCE methodcall EOL'
    p[0]=p[1]
def p_statement_expression(p):
    'statement : expression EOL'
    p[0]=p[1]
def p_statement_list_access(p):
    'statement : access_list EOL'
    p[0]=p[1]


def p_scope(p):
    'scope : UP_SCOPE group DOWN_SCOPE'
    p[0]=["SCOPE",p[2]]
def p_group(p):
    'group : Succesion_of_Statements'
    p[0]=p[1]
def p_Succesion_of_Statements_final(p):
    'Succesion_of_Statements : statement'
    p[0]=p[1]
def p_Succesion_of_Statements_init(p):
    'Succesion_of_Statements : statement Succesion_of_Statements'
    p[0]=[p[1],p[2]]


def p_list(p):
    'list : L_SQUARE_PAREN params R_SQUARE_PAREN'
    p[0]=["LIST",p[2]]
def p_list_void(p):
    'list : L_SQUARE_PAREN R_SQUARE_PAREN'
    p[0]=["LIST",[]]
def p_access_list(p):
    'access_list : IDENTIFIER index_list recursive_index'
    p[0]=["ACCESS",p[1]]+p[2]+p[3]

def p_index_list(p):
    'index_list : L_SQUARE_PAREN allowed_access_index R_SQUARE_PAREN'
    p[0]=["SINGLE",p[2]]
def p_index_list_range(p):
    'index_list : L_SQUARE_PAREN allowed_access_index COLON allowed_access_index R_SQUARE_PAREN'
    p[0]=["RANGE",p[2],p[4]]
def p_index_list_range_start_no_defined(p):
    'index_list : L_SQUARE_PAREN COLON COMA allowed_access_index R_SQUARE_PAREN'
    p[0]=["RANGE","NODEFINED",p[4]]
def p_index_list_range_end_no_defined(p):
    'index_list : L_SQUARE_PAREN allowed_access_index COMA COLON R_SQUARE_PAREN'
    p[0]=["RANGE",p[2],"NODEFINED"]
def p_allowed_access_index_integer(p):
    'allowed_access_index : INTEGER'
    p[0]=p[1]
def p_allowed_access_index_identifier(p):
    'allowed_access_index : IDENTIFIER'
    p[0]=p[1]
def p_recursive_index(p):
    'recursive_index : index_list recursive_index'
    p[0]=p[1]+p[2]
def p_recursive_index_void(p):
    'recursive_index : '
    p[0]=[]







#Math managing
def p_expression_plus(p):
     'expression : expression PLUS term'
     p[0]=[p[2],p[1],p[3]]
 
def p_expression_minus(p):
    'expression : expression MINUS term'
    p[0]=[p[2],p[1],p[3]]

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_times(p):
    'term : term MULTIPLICATION term2'
    p[0] = [p[2],p[1] , p[3]]
def p_term_leftover(p):
    'term : term LEFTOVER term2'
    p[0]=[p[2],p[1],p[3]]
def p_term_div(p):
    'term : term DIVIDE term2'
    p[0]=[p[2],p[1],p[3]]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_integer(p):
    'factor : INTEGER'
    p[0] = p[1]

def p_factor_float(p):
    'factor : FLOAT'
    p[0] = p[1]

def p_factor_function_call(p):
    'factor : functioncall'
    p[0]=p[1]
def p_factor_method_call(p):
    'factor : methodcall'
    p[0]=p[1]
def p_factor_list(p):
    'factor : access_list'
    p[0]=p[1]

def p_factor_id(p):
    'factor : IDENTIFIER'
    p[0] = p[1]
def p_factor_expr(p):
    'factor : L_PAREN expression R_PAREN'
    p[0] = p[2]
def p_term_term2(p):
    'term : term2'
    p[0]=p[1]
def p_term2_pow(p):
    'term2 : term2 POW factor2'
    p[0]=[p[2],p[1],p[3]]
def p_term2_integer_division(p):
    'term2 : term2 INT_DIVISION factor2'
    p[0]=[p[2],p[1],p[3]]
def p_term2_factor2(p):
    'term2 : factor2'
    p[0] = p[1]
def p_factor2_integer(p):
    'factor2 : INTEGER'
    p[0] = p[1]
def p_factor2_float(p):
    'factor2 : FLOAT'
    p[0] = p[1]

def p_factor2_function_call(p):
    'factor2 : functioncall'
    p[0]=p[1]
def p_factor2_method_call(p):
    'factor2 : methodcall'
    p[0]=p[1]
def p_factor2_list(p):
    'factor2 : access_list'
    p[0]=p[1]

def p_factor2_expr(p):
    'factor2 : L_PAREN expression R_PAREN'
    p[0] = p[2]
def p_factor2_id(p):
    'factor2 : IDENTIFIER'
    p[0] = p[1]

def p_term2_factor(p):
    'term2 : factor'
    p[0]=p[1]






#iterables and noiterables 
def p_iterable_identifier(p):
    'iterable : IDENTIFIER'
    p[0]=p[1]
def p_noiterable_integer(p):
    'noiterable : INTEGER'
    p[0]=p[1]

def p_noiterable_float(p):
    'noiterable : FLOAT'
    p[0]=p[1]

def p_noiterable_boolean(p):
    'noiterable : BOOLEAN'
    p[0]=p[1]
# Error rule for syntax errors
def p_error(p):
    print(p)
    print("Syntax error in input!")

 
 # Build the parser

parser = yacc.yacc()

   
file=open("fuente.pn",'r')
s =file.read()
#s="{var=12;var1=2**5;}"
#s=input('calc> ')
#print(s)
result = parser.parse(s,lexer=mylexer)
print(result)