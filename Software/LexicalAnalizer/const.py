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
    'COLON',
    'pene',
    'STRING'
   
]
FunctionDataSetters={
    'int':'int',
    'float':'float',
    'bool':'bool',
    'lista' : 'lista',

}

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
    'BLINK'      : [['lista','int'],['int'],["RESERVED_SPECIAL_TIME"],['bool']],
    'DELAY'      : [['int'],["RESERVERD_SPECIAL_TIME"]],
    "PRINT_LED"  : [['int'],['int'],['bool']],
    'PRINT_LED_X': [["RESERVED_SPECIAL_OBJECT"],['int'],["lista"]],
    'RANGE'      : [["int"],["bool"]],
    'LIST'       : [['pene']],
    'TYPE'       : [['ANY']],
    'LEN'        : [["lista"]],
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

method_valid_caller={
    'F_METHOD': ['lista','bool'],
    'T_METHOD': ['lista','bool'],
    'NEG'     : ['lista','bool'],
    'SHAPE_F' : ['lista'],
    'SHAPE_C' : ['lista'],
    'INSERT'  : ['lista'],
    'DELETE'  : ['lista'],
}
method_valid_params_types={
    'INSERT':[['list'],['valid_insertion'],['int']],
    'DELETE':[['int'],['valid_insertion']],
    'F_METHOD':[],
    'T_METHOD':[],
    'NEG':[],
    'SHAPE_F':[],
    'SHAPE_C':[],

}
valid_insertion_type=[0,1]
reserved_special_time=[ "'seg'","'min'","'mil'"]
reserved_special_object=[ "'F'", "'C'","'M'",]

operators=['+','*','**','/','//','-']