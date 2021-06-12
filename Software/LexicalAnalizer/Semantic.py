from ast import Raise
import re
from descriptors import function_descriptor
from const import reserved_function_names as prebuild
from const import reserved_function_params as reserved_params
from const import reserved_methods_names as prebuild_method
from const import method_valid_params_types as reserverd_method_params
from const import method_valid_caller as valid_caller_dic
from const import reserved_special_time as special_time
from const import reserved_special_object as special_object
from const import valid_insertion_type as special_insertion
from const import operators
from stack import Stack

global TS,MAIN_FLAG
MAIN_FLAG=False

TS={} #Table Symbol
ARGUMENTS="ARGUMENTS"
PARAMETERS="PARAMETERS"
ASSIGNMENT="ASSIGMENT"
METHODCALL="METHOD_CALL"
FUNCTIONCALL="CALL_FUNC"
SCOPE="SCOPE"
FOR="FOR"
IF="IF"

def program(AST):
    MAIN_FLAG=True
    prebuild_setting()
    if not procedure_setting(AST):
        raise Exception("No main found")
    for i in AST.getChildren():
        procedure(i)
    #print(TS)

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
        children=children[1:]
    for statement in children:
        Scope_Count=statement_classifier(statement,Scope_Count,Scope_Stack)
    return Scope_Count

def statement_classifier(statement,ScopeCount,ScopeStack):
    StatementName=statement.getData()
    if (StatementName==SCOPE):
        return scope(statement,ScopeCount,ScopeStack)
    if(StatementName==ASSIGNMENT):
        return assignment(statement,ScopeCount,ScopeStack)
    if(StatementName==METHODCALL):
        return method_call(statement,ScopeCount,ScopeStack)
    if(StatementName==FUNCTIONCALL):
        return function_call(statement,ScopeCount,ScopeStack)
    if(StatementName==FOR):
        return FOR_STATEMENT(statement,ScopeCount,ScopeStack)
    if(StatementName==IF):
        return IF_statement(statement,ScopeCount,ScopeStack)
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
    if(FunctionName in prebuild):
        FunctionName=prebuild[FunctionName]
    Parameters_Node=AST.getChildren()[1]
    Parameters_given=parameters_type_func_call(Parameters_Node,ScopeStack)
    Parameters_requested=TS[FunctionName]
    Parameters_values=parameters_value_func_call(Parameters_Node,ScopeStack)
    valid_parameter_type(Parameters_requested,Parameters_given)
    evaluate_special_string(Parameters_requested,Parameters_values)
    return ScopeCount

def method_call(AST,ScopeCount,ScopeStack):
    VarName=get_identifier(AST)
    MethodName=AST.getChildren()[1].getChildren()[0].getData()
    MethodName=prebuild_method[MethodName]
    valid_caller(VarName,MethodName,ScopeStack)
    Parameters_Node=AST.getChildren()[2]
    Parameters_given=parameters_type_func_call(Parameters_Node,ScopeStack)
    Parameters_requested=TS[MethodName]
    Parameters_values=parameters_value_func_call(Parameters_Node,ScopeStack)
    valid_parameter_type(Parameters_requested,Parameters_given)
    evaluate_special_string(Parameters_requested,Parameters_values)
    return ScopeCount

def assignment(AST,ScopeCount,ScopeStack):
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
    final_type=valid_change(current_type,assign_type)
    if(final_type!=None):
        var_to_TS(ScopeStack,varName,final_type)
    else:
        raise Exception("The "+varName+"'s type has changed")
    return ScopeCount

def FOR_STATEMENT(AST,ScopeCount,ScopeStack):
    iterable=get_identifier(AST)
    source=get_identifier(AST.getChildren()[1])
    print("soy el scope")
    print(ScopeStack.stack_to_list())
    try:
        find_var_type(iterable,ScopeStack)
    except:
        var_to_TS(ScopeStack,iterable,"bool")
    else:
        #print("llegue aqui")
        raise Exception("The "+iterable+ " has been defined previously")
    varType=find_var_type(source,ScopeStack)
    if(varType!="lista"):
        raise Exception("The "+source+" must be a list")
    for_scope = AST.getChildren()[3]
    count=scope(for_scope,ScopeCount,ScopeStack)
    print("el scope al final del for es ")
    print(ScopeStack.stack_to_list())
    return count

def IF_statement(AST,ScopeCount,ScopeStack):
    print(TS)
    print(ScopeStack.stack_to_list())
    iterable_name = AST.getChildren()[0].getChildren()[1].getChildren()[0].getData()
    print(iterable_name)
    iterable_type = find_var_type(iterable_name,ScopeStack)

    compared_type = AST.getChildren()[0].getChildren()[2].getChildren()[0].getData()
    print(compared_type)
    '''
    if (compared_type == 'IDENTIFIER'):
        compared_type=
        pass
    pass
    '''
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
            if(element_class=="NOT_DEFINED"):
                return element_class
        elif(element_class==FUNCTIONCALL):
            return "NOT_DEFINED"
        elif(element_class==METHODCALL):
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
    if(type1=="NOT_DEFINED" or type2=="NOT_DEFINED"):
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
    ScopeStack=None
    for i in AST.getChildren():
        proc_name= get_identifier(i)
        ScopeStack=Stack()
        ScopeStack.push(proc_name)
        parameters=getParamstypes(i,ScopeStack)
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
def parameters_value_func_call(AST,ScopeStack):
    Parameters=[]
    for Parameter in AST.getChildren():
        ParameterValue=Parameter.getChildren()[0].getData()
        Parameters+=[ParameterValue]
    return Parameters
def evaluate_special_string(requestedParameters,givenValues):
    current_types=None
    current_value=None
    current_type=None
    for i in range(len(requestedParameters)):
        current_types=requestedParameters[i]
        current_value=givenValues[i]
        if(len(current_types)==1):
            current_type=current_types[0]
            match_special_types(current_type,current_value)
            
    

def match_special_types(varType,value):
    if(varType=="RESERVERD_SPECIAL_TIME"):
        if(value not in special_time):
            special_type_exception(value,varType)
    if(varType=="RESERVED_SPECIAL_OBJECT"):
        if(value not in special_object):
            special_type_exception(value,varType)
    if(varType=='valid_insertion'):
        if(value not in special_insertion):
            special_type_exception(value,varType)
    




def special_type_exception(value,varType):
    raise Exception("The "+str(value)+" doesnt match with the "+varType+" requested")
        
def getParamstypes(AST,ScopeStack):
    datatype=""
    typeslist=[]
    for i in AST.getChildren()[1].getChildren():
        try:
            varName=get_identifier(i)
            datatype=i.getChildren()[1].getData()
            typeslist+=[[datatype]]
            var_to_TS(ScopeStack,varName,datatype)
        except:
            return []
    return typeslist


def valid_parameter_type(requested_param,given_param):
    #print("given param")
    #print(given_param)
    if(len(requested_param)!=len(given_param)):
        raise Exception("The number of params doesnt match")
    for i in range(len(requested_param)):
        for j in range(len(given_param[i])):
            focus_type=transform_value(given_param[i][j])
            requested_params=requested_param[i]
            #print(requested_params)
            if(focus_type=="STRING"):
                continue
            if('valid_insertion'== requested_params[0]):
                continue
            if(focus_type not in requested_params):
                raise Exception("The var params types doesnt match")
def valid_caller(varName,MethodName,ScopeStack):
    varType=find_var_type(varName,ScopeStack)
    if(varType!="NOT_DEFINED"):
        if(varType not in valid_caller_dic[MethodName]):
            raise Exception("No valid caller "+varName+" to method "+ MethodName)

def transform_value(varType):
    if(varType=="INTEGER"):
        return 'int'
    if(varType=="BOOLEAN"):
        return 'bool'
    if(varType=='LIST'):
        return 'lista'
    if(varType=="FLOAT"):
        return 'float'
    else:
        return varType
    

def prebuild_setting():
    for value in prebuild.values():
        TS[(value)]=reserved_params[value]
    for value in prebuild_method.values():
        TS[(value)]=reserverd_method_params[value]

def in_TS(id_tuple):
    return id_tuple in TS.keys()

def get_identifier(AST):
    return AST.getChildren()[0].getChildren()[0].getData()
def var_to_TS(ScopeStack,varName,dataType):
    TS[tuple(ScopeStack.stack_to_list()),varName]=dataType
