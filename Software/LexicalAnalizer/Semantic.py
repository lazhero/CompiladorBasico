from ast import Raise
from descriptors import function_descriptor
from const import reserved_function_names as prebuild
from const import reserved_function_params as reserved_params
from const import operators
from stack import Stack

global TS,MAIN_FLAG
MAIN_FLAG=False

TS={} #Table Symbol
ARGUMENTS="ARGUMENTS"
PARAMETERS="PARAMETERS"
ASSIGNMENT="ASSIGMENT"
METHODCALL="METHOD_CALL"
FUNCTIONCALL="FUNC_CALL"
SCOPE="SCOPE"

def program(AST):
    MAIN_FLAG=True
    #prebuild_setting()
    if not procedure_setting(AST):
        raise Exception("No main found")
    for i in AST.getChildren():
        procedure(i)
    print(TS)

def procedure(AST):
    global MAIN_FLAG
    Scope_Stack=Stack()
    Scope_Stack.push(get_identifier(AST))
    if(get_identifier(AST)=="main"):
        MAIN_FLAG=False
    Scope_Count=0
    process_children(AST,Scope_Count,Scope_Stack)

def process_children(AST,Scope_Count,Scope_Stack):
    children=AST.getChildren()
    if(AST.getData()=="PROCEDURE"):
        print("EStoy en process")
        children=children[1:]
    for statement in children:
        print(statement.getData())
        Scope_Count=statement_classifier(statement,Scope_Count,Scope_Stack)
    return Scope_Count

def statement_classifier(statement,ScopeCount,ScopeStack):
    StatementName=statement.getData()
    print(StatementName)
    if (StatementName==SCOPE):
        return scope(statement,ScopeCount,ScopeStack)
    if(StatementName==ASSIGNMENT):
        return assignment(statement,ScopeCount,ScopeStack)
    if(StatementName==METHODCALL):
        return method_call(statement,ScopeCount,ScopeStack)
    if(StatementName==FUNCTIONCALL):
        return function_call(statement,ScopeCount,ScopeStack)
    else:
        return ScopeCount

def scope(AST,ScopeCount,ScopeStack):
    global MAIN_FLAG
    if(MAIN_FLAG):
        ScopeStack.push("SCOPE"+str(ScopeCount))
    else:
        MAIN_FLAG=True
    ScopeCount += 1
    ScopeCount = process_children(AST,ScopeCount,ScopeStack)
    ScopeStack.pop()
    return ScopeCount

def function_call(AST,ScopeCount,ScopeStack):
    FunctionName=get_identifier(AST)
    Parameters_Node=AST.getChildren()[1]
    Parameters=parameters_type_func_call(Parameters_Node,ScopeStack)

def method_call(AST,ScopeCount,ScopeStack):
    pass

def assignment(AST,ScopeCount,ScopeStack):
    print("el pene del wage es hermoso")
    element_classifier=AST.getChildren()[1].getData()
    varName=AST.getChildren()[0].getChildren()[0].getData()
    current_type=None
    try:
        current_type=find_var_type(varName,ScopeStack)
    except:
        pass
    assign_type=None
    if(element_classifier=='INTEGER'):
        assign_type='int'
    elif(element_classifier=="FLOAT"):
        assign_type="float"
    elif(element_classifier=="BOOLEAN"):
        assign_type="bool"
    elif(element_classifier in operators):
        assign_type=just_math_expression(AST,ScopeStack)
    elif(element_classifier=="LIST"):
        assign_type="lista"
    elif(element_classifier=="IDENTIFIER"):
        assign_type=just_identifier(AST,ScopeStack)
    else:
        assign_type="NOT_DEFINED"
    if(current_type==None or current_type==assign_type):
        TS[tuple(ScopeStack.stack_to_list()),varName]=assign_type
    else:
        raise Exception("The "+varName+"'s type has changed")
    return ScopeCount
  
def just_math_expression(AST,ScopeStack):
    elements=get_operands(AST.getChildren()[1])
    return  validate_expression(elements,ScopeStack)
    #raise Exception("The expression type doesnt match variable's type "+varName)

def get_operands(AST):
    if(AST.getData() not in operators):
        return [AST]
    else:
        left_operator=get_operands(AST.getChildren()[0])
        right_operator=get_operands(AST.getChildren()[1])
        return left_operator+right_operator

def validate_expression(operands_list,Scope_Stack):
    expression_type=None
    element_class=None
    for operand in operands_list:
        element_class=operand.getData()
        if(element_class=="IDENTIFIER"):
            element_class=just_identifier(operand,Scope_Stack)
            if(element_class=="NO_DEFINED"):
                return element_class
        elif(element_class=="FUNC_CALL"):
            return "NOT_DEFINED"
        elif(element_class=="METHOD_CALL"):
            return "NOT_DEFINED"
        
        expression_type=valid_change(expression_type,element_class)
        if(expression_type==None):
            raise Exception("Not valid operation between: "+expression_type+ " and "+element_class)
    return expression_type    
        
def valid_change(type1,type2):
    if(type1==None):
        return type2
    if(type2==None):
        return type1
    if(type1==type2):
        return type1
    if(type1=="INTEGER" and type2=="FLOAT"):
        return type2
    if(type2=="INTEGER" and type1=="FLOAT"):
        return type1
    return None

def just_identifier(AST,ScopeStack):
    prevVarName=AST.getChildren()[1].getChildren()[0].getData()
    new_type=find_var_type(prevVarName,ScopeStack)
    return new_type

def find_var_type(VarName,Scope):
    StackCopy=Scope.copy()
    while(not StackCopy.is_empty()):
        try: 
            return TS[tuple(StackCopy.stack_to_list()),VarName]
        except(KeyError):
            StackCopy.pop()
    try: 
        return TS[('main'),VarName]
    except(KeyError):
        except_string='Variable: '+VarName+" not defined previoustly"
        raise Exception(except_string)

def procedure_setting(AST):
    main_flag=False
    for i in AST.getChildren():
        proc_name= get_identifier(i)
        parameters=getParamstypes(i)
        param_numbers=len(i.getChildren()[1].getData()[1:])
        #procedure=function_descriptor(proc_name,parameters)
        TS[(proc_name)]=parameters
        if (proc_name=="main"):
            main_flag=True
    return main_flag

def parameters_type_func_call(AST,ScopeStack):
    Parameters=[]
    type=None
    for Parameter in AST.getChildren():
        ParameterType=Parameter.getData()
        ParameterValue=Parameter.getChildren()[0].getData()
        if(ParameterType=="IDENTIFIER"):
            type=find_var_type(ParameterValue,ScopeStack)
            Parameters+=[[type]]
        else:
            Parameters+=[[ParameterType]]
    return Parameters

def getParamstypes(AST):
    datatype=""
    typeslist=[]
    for i in AST.getChildren()[1].getChildren():
        try:
            datatype=i.getChildren()[1].getData()
            typeslist+=[[datatype]]
        except:
            return []
    return typeslist

def prebuild_setting():
    for value in prebuild.values():
        #procedure=function_descriptor(value,reserved_params[value])
        TS[(value)]=reserved_params 

def in_TS(id_tuple):
    return id_tuple in TS.keys()

def get_identifier(AST):
    return AST.getChildren()[0].getChildren()[0].getData()