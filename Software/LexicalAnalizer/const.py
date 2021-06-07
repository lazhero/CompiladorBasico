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
    'if'    : 'IF',
    'else'  : 'ELSE',
    'for'   : 'FOR',
    'in'    : 'IN',
    'Step'  : 'STEP',
 }
reserved_function_names={
    'blink'      : 'BLINK',
    'delay'      : 'DELAY',
    'printLed'   : "PRINT_LED" ,
    'printLedX'  : 'PRINT_LED_X',
    'range'      : 'RANGE',
    'list'       : 'LIST',
    'type'       : 'TYPE',
    'len'        : 'LEN',
}

reserved_function_params={
    'BLINK'      : 4,
    'DELAY'      : 2,
    "PRINT_LED"  : 3,
    'PRINT_LED_X': 3,
    'RANGE'      : 2,
    'LIST'       : 1,
    'TYPE'       : 1,
    'LEN'        : 1,
}

reserved_methods_names={
    'F'      :'F_METHOD',
    'T'      : 'T_METHOD',
    'Neg'    : 'NEG',
    'shapeF' : 'SHAPE_F',
    'shapeC' : 'SHAPE_C',
    'insert' : 'INSERT',
    'delete' : 'DELETE',
}