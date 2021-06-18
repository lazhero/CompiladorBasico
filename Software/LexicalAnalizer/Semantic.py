
from ast import Raise
from descriptors import function_descriptor
from const import reserved_function_names as prebuild
from const import reserved_function_params as reserved_params
from const import reserved_methods_names as prebuild_method
from const import method_valid_params_types as reserverd_method_params
from const import method_valid_caller as valid_caller_dic
from const import reserved_special_time as special_time
from const import reserved_special_object as special_object
from const import valid_insertion_type as special_insertion
from const import NoautoPercetivesMethods as DONT_ASSIGNT
from const import operators
from stack import Stack
#import Controller_Serial
global TS,MAIN_FLAG, GENERATED, TABCOUNTER
MAIN_FLAG=False


TS={} #Table Symbol
PATH="\Hardware"
HardWareFile="Controller_Serial"
ARGUMENTS="ARGUMENTS"
PARAMETERS="PARAMETERS"
ASSIGNMENT="ASSIGMENT"
METHODCALL="METHOD_CALL"
FUNCTIONCALL="CALL_FUNC"
LIST="LIST"
ACCESS="ACCESS"
SCOPE="SCOPE"
FOR="FOR"
IF="IF"

OUTPUTFILE="out.py"
def SEMANTIC(AST,outputPath,currentPath):
    global GENERATED, TABCOUNTER
    currentPath+=PATH
    currentPath=currentPath.replace('"\"','"/"')
    outputFile= outputPath+"/"+OUTPUTFILE
    GENERATED=open(outputFile,"w")
    GENERATED.write("import sys\n")
    GENERATED.write("sys.path.append(r")
    GENERATED.write('"')
    GENERATED.write(currentPath)
    GENERATED.write('"')
    GENERATED.write(")\n")
    GENERATED.write("from ")
    GENERATED.write(HardWareFile)
    GENERATED.write(" import *")
    GENERATED.write("\n")
    TABCOUNTER=0
    program(AST)
    return outputFile

def program(AST):
    MAIN_FLAG=True
    prebuild_setting()
    if not procedure_setting(AST):
        raise Exception("No main found")
    for i in AST.getChildren():
        procedure(i)
    GENERATED.write("main()")
    GENERATED.close()

def procedure(AST):
    global MAIN_FLAG
    Scope_Stack=Stack()
    proc_name=get_identifier(AST)
    Scope_Stack.push(proc_name)
    if(get_identifier(AST)=="main"):
        MAIN_FLAG=False
    Scope_Count=0
    GENERATED.write("def ")
    GENERATED.write(proc_name)
    params=getParamsNames(AST)
    writeParameters(params,"(",")")
    GENERATED.write(":\n")
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
    if(StatementName==ACCESS):
        return ACCESS_statement(statement,ScopeCount,ScopeStack)
    else:
        return ScopeCount

def scope(AST,ScopeCount,ScopeStack):
    global MAIN_FLAG, TABCOUNTER
    if(MAIN_FLAG):
        ScopeStack.push("SCOPE"+str(ScopeCount))
    else:
        MAIN_FLAG=True
    ScopeCount += 1
    TABCOUNTER += 1
    ScopeCount = process_children(AST,ScopeCount,ScopeStack)
    ScopeStack.pop()
    TABCOUNTER -= 1
    return ScopeCount

def function_call(AST,ScopeCount,ScopeStack):
    FunctionName=get_identifier(AST)
    if(FunctionName in prebuild):
        FunctionName=prebuild[FunctionName]
    Parameters_Node=AST.getChildren()[1]
    Parameters_given=parameters_type_func_call(Parameters_Node,ScopeStack)
    Parameters_requested=TS[FunctionName]
    Parameters_values=parameters_value_func_call(Parameters_Node,ScopeStack)
    valid_parameter_type(Parameters_requested,Parameters_given,FunctionName)
    evaluate_special_string(Parameters_requested,Parameters_values)

    writeFunctionCall(FunctionName,Parameters_values)
    GENERATED.write("\n")

    return ScopeCount

def method_call(AST,ScopeCount,ScopeStack):
    CallerClassifier=AST.getChildren()[0].getData()
    VarName=get_identifier(AST)
    MethodName=AST.getChildren()[1].getChildren()[0].getData()
    MethodName=prebuild_method[MethodName]
    AccessList=[]
    if(CallerClassifier=="ACCESS"):
        AccessNode=AST.getChildren()[0]
    
        VarName=get_identifier(AccessNode)
        AccessList=setting_access(AccessNode.getChildren(),ScopeStack)
       

    valid_caller(VarName,MethodName,ScopeStack)
    Parameters_Node=AST.getChildren()[2]
    Parameters_given=parameters_type_func_call(Parameters_Node,ScopeStack)
    Parameters_requested=TS[MethodName]
    Parameters_values=parameters_value_func_call(Parameters_Node,ScopeStack)
    valid_parameter_type(Parameters_requested,Parameters_given,MethodName)
    evaluate_special_string(Parameters_requested,Parameters_values)

    if(MethodName not in DONT_ASSIGNT):
        GENERATED.write("\t"*TABCOUNTER)
        GENERATED.write(VarName)
        GENERATED.write("=")
    writeMethodCall(MethodName,VarName,AccessList,Parameters_values)
    GENERATED.write("\n")

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
    elif(element_classifier==METHODCALL):
        assign_type=METHODCALL
    elif(element_classifier==FUNCTIONCALL):
        assign_type=FUNCTIONCALL
    elif(element_classifier==ACCESS):
        assign_type="ACCESS"
    else:
        assign_type="NOT_DEFINED"
    final_type=valid_change(current_type,assign_type)
    if(final_type!=None):
        var_to_TS(ScopeStack,varName,final_type)
    else:
        raise Exception("The "+varName+"'s type has changed")
    writeType=assign_type
    if(element_classifier in operators):
        writeType="MATH"
    if(writeType==METHODCALL):
        GENERATED.write((TABCOUNTER*"\t")+varName+"=")
        ScopeCount = method_call(AST.getChildren()[1],ScopeCount,ScopeStack)
    elif(writeType==FUNCTIONCALL):
        GENERATED.write((TABCOUNTER*"\t")+varName+"=")
        ScopeCount = function_call(AST.getChildren()[1],ScopeCount,ScopeStack)
    elif(writeType=="ACCESS"):
        GENERATED.write((TABCOUNTER*"\t")+varName+"=")
        ScopeCount = ACCESS_statement(AST.getChildren()[1],ScopeCount,ScopeStack)
    else:
        GENERATED.write((TABCOUNTER*"\t")+varName+"=")
        writeAssignment(AST,writeType,ScopeStack)
        GENERATED.write("\n")
    return ScopeCount

def FOR_STATEMENT(AST,ScopeCount,ScopeStack):
    iterable=get_identifier(AST)
    source=get_identifier(AST.getChildren()[1])
    try:
        find_var_type(iterable,ScopeStack)
    except:
        var_to_TS(ScopeStack,iterable,"bool")
    else:
        raise Exception("The variable "+iterable+ " has been defined previously")
    varType=find_var_type(source,ScopeStack)
    if(varType!="lista"):
        raise Exception("The "+source+" must be a list")
    for_scope = AST.getChildren()[3]
    step=AST.getChildren()[2].getChildren()[0].getChildren()[0].getData()
    GENERATED.write((TABCOUNTER*"\t")+"for ")
    GENERATED.write("uniquei in range(0,len("+source+"),"+str(step)+"):\n")
    GENERATED.write((TABCOUNTER+1)*"\t")
    GENERATED.write(iterable+"="+source+"[uniquei]\n")
    count=scope(for_scope,ScopeCount,ScopeStack)
    return count

def IF_statement(AST,ScopeCount,ScopeStack):
    iterable_name = AST.getChildren()[0].getChildren()[1].getChildren()[0].getData()
    iterable_type = find_var_type(iterable_name,ScopeStack)
    compared_value = AST.getChildren()[0].getChildren()[2].getChildren()[0].getData()
    compared_type=AST.getChildren()[0].getChildren()[2].getData()
    if_scope=AST.getChildren()[1]
    else_scope=AST.getChildren()[2].getChildren()[0]
    if (compared_type == 'IDENTIFIER'):
        compared_type=find_var_type(compared_value,ScopeStack)
    else:
        compared_type=transform_value(compared_type)
    if(compared_type!=iterable_type):
        raise Exception("Cant compare "+compared_type+" with "+iterable_type)
    operator=AST.getChildren()[0].getChildren()[0].getChildren()[0].getData()
    GENERATED.write((TABCOUNTER*"\t"))
    GENERATED.write("if("+iterable_name+str(operator)+str(compared_value)+"):\n")
    ScopeCount=scope(if_scope,ScopeCount,ScopeStack)
    GENERATED.write((TABCOUNTER*"\t"))
    GENERATED.write("else:\n")
    if(len(else_scope.getChildren())<=0):
        GENERATED.write(((TABCOUNTER+1)*"\t"))
        GENERATED.write("pass")

    return scope(else_scope,ScopeCount,ScopeStack)


def ACCESS_statement(AST,ScopeCount,ScopeStack):
    varName=get_identifier(AST)
    accessElements=setting_access(AST.getChildren()[1:],ScopeStack)
    GENERATED.write((TABCOUNTER*"\t"))
    writeAccess(varName,accessElements)
    GENERATED.write("\n")

    return ScopeCount

def just_math_expression(AST,ScopeStack):
    elements=get_operands(AST.getChildren()[1])
    return  validate_expression(elements,ScopeStack)

def get_operands(AST):
    if(AST.getData() not in operators):
        return [AST]
    else:
        left_operator=get_operands(AST.getChildren()[0])
        right_operator=get_operands(AST.getChildren()[1])
        return left_operator+right_operator

def get_operators(AST):
    if(AST.getData() not in operators):
        return []
    else:
        return [AST.getData()]+get_operators(AST.getChildren())

def validate_expression(operands_list,Scope_Stack):
    expression_type=None
    element_class=None
    for operand in operands_list:
        element_class=operand.getData()
        if(element_class=="IDENTIFIER"):
            element_class=just_identifier(operand,Scope_Stack)
            if(element_class=="NOT_DEFINED"):
                return element_class
            elif(element_class==METHODCALL):
                return element_class
            elif(element_class==FUNCTIONCALL):
                return element_class
        elif(element_class==FUNCTIONCALL):
            return  FUNCTIONCALL
        elif(element_class==METHODCALL):
            return METHODCALL
        
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
    if(type1==METHODCALL or type2==METHODCALL):
        return type1
    if(type1==FUNCTIONCALL or type2==FUNCTIONCALL):
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
        except_string='Variable: '+str(VarName)+" not defined previously"
        raise Exception(except_string)

def procedure_setting(AST):
    global GENERATED
    main_flag=False
    ScopeStack=None
    for i in AST.getChildren():
        proc_name= get_identifier(i)
        ScopeStack=Stack()
        ScopeStack.push(proc_name)
        parameters=getParamstypes(i,ScopeStack)
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
        value= Parameter.getData()
        
        if(value==FUNCTIONCALL):
            functionName=get_identifier(Parameter)
            functionName=prebuild[functionName]
            ParameterValue=parameters_value_func_call(Parameter.getChildren()[1],ScopeStack)
            ParameterValue=[functionName]+ParameterValue
        elif(value==LIST):
            ParameterValue= [listElements(Parameter)]
            
        else:
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
    if(isinstance(value,list)):
        return 
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

def getParamsNames(AST):
    nameslist=[]
    for i in AST.getChildren()[1].getChildren():
        varName=get_identifier(i)
        nameslist+=[varName]
    return nameslist

def valid_parameter_type(requested_param,given_param, name):
    if(len(requested_param)!=len(given_param)):
        raise Exception("The number of params in "+name+" doesnt match")
    for i in range(len(requested_param)):
        for j in range(len(given_param[i])):
            focus_type=transform_value(given_param[i][j])
            requested_params=requested_param[i]
            if(focus_type=="STRING"):
                continue
            if('valid_insertion'== requested_params[0] or 'ANY' == requested_params[0]):
                continue
            if(focus_type==METHODCALL):
                continue
            if(focus_type==FUNCTIONCALL):
                continue
            if(focus_type=="ACCESS"):
                continue
            if(focus_type=="NO_DEFINED"):
                continue
            print(focus_type)
            if(focus_type not in requested_params):
                raise Exception("The var params types in "+name+"  doesnt match")

def valid_caller(varName,MethodName,ScopeStack):
   
    varType=find_var_type(varName,ScopeStack)
    if(varType!="NOT_DEFINED" and varType!=FUNCTIONCALL and varType!=METHODCALL):
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

def setting_access(AST,ScopeStack):
    accessList=[]
    for i in AST:
        accessType=i.getData()
        if(accessType=="SINGLE"):
            firstAccess=i.getChildren()[0]
            access_verify(firstAccess,ScopeStack)
            accessList+=[str(firstAccess.getChildren()[0].getData())]
        elif(accessType=="RANGE"):
            firstAccess=i.getChildren()[0]
            secondAccess=i.getChildren()[1]
            access_verify(firstAccess,ScopeStack)
            access_verify(secondAccess,ScopeStack)
            accessList+=[str(firstAccess.getChildren()[0].getData())+":"+str(secondAccess.getChildren()[0].getData())]
        elif(accessType=="DOUBLESINGLE"):
            firstAccess=i.getChildren()[0]
            secondAccess=i.getChildren()[1]
            access_verify(firstAccess,ScopeStack)
            access_verify(secondAccess,ScopeStack)
            accessList+=[str(firstAccess.getChildren()[0].getData())]+[str(secondAccess.getChildren()[0].getData())]
        elif(accessType=="COLUMN"):
            firstAccess=i.getChildren()[0]
            access_verify(firstAccess,ScopeStack)
            function="columnAccess"
            accessList+=[[firstAccess.getChildren()[0].getData()]]
    return accessList

def access_verify(node,ScopeStack):
    nodeType=node.getData()
    if(nodeType=="IDENTIFIER"):
        nodeName=node.getChildren()[0].getData()
        find_var_type(nodeName,ScopeStack)

def get_identifier(AST):
    return AST.getChildren()[0].getChildren()[0].getData()

def var_to_TS(ScopeStack,varName,dataType):
    TS[tuple(ScopeStack.stack_to_list()),varName]=dataType


### GENERATOR FILE FUNCTIONS ###

def writeParameters(params,open,close):
    global GENERATED
    GENERATED.write(open)
    for parameter in params:
        if(isinstance(parameter,list)):
            firstElement=parameter[0]
            if(isinstance(firstElement,list)):
                #writeParameters(firstElement,"[","]")
                writeList(firstElement,"[","]")
                GENERATED.write(",")

            else:
                GENERATED.write(str(firstElement))
                writeParameters(parameter[1:],open,close)
                GENERATED.write(",")
        else:
            GENERATED.write(str(parameter))
            GENERATED.write(",")
    GENERATED.write(close)

def writeAssignment(AST,classifier,ScopeStack):
    assigned=AST.getChildren()[1]
    if(classifier=="MATH"):
        writeMath(assigned)
    elif(classifier=="lista"):
        writeListParams(assigned)
    
    else:
        GENERATED.write(str(assigned.getChildren()[0].getData()))


def writeList(elements,open,close):
    GENERATED.write(open)
    for element in elements:
        if(isinstance(element,list)):
            writeList(element,open,close)
            GENERATED.write(",")
        else:
            GENERATED.write(element)
            GENERATED.write(",")
    GENERATED.write(close)
    


def writeMath(AST):
    expression = AST.getData()
    if(expression in operators):
        GENERATED.write("(")
        writeMath(AST.getChildren()[0])
        GENERATED.write(expression)
        writeMath(AST.getChildren()[1])
        GENERATED.write(")")
    else:
        GENERATED.write(str(AST.getChildren()[0].getData()))

def writeFunctionCall(FunctionName,Parameters_values):
    GENERATED.write((TABCOUNTER*"\t")+FunctionName)
    writeParameters(Parameters_values,"(",")")
    
def writeMethodCall(MethodName,VarName,ACCESS,Parameters_values):
    GENERATED.write((TABCOUNTER*"\t")+MethodName)
    GENERATED.write("(")
    GENERATED.write(VarName)
    writeAccess("",ACCESS)
    params=Parameters_values
    writeParameters(params,"",")")

def writeAccess(varName,accessElements):
    if(not isinstance(accessElements,list)):
        return
    if(len(accessElements)<=0):
        return
    #GENERATED.write((TABCOUNTER*"\t"))
    element0=accessElements[0]
    if(isinstance(element0,list)):
            GENERATED.write("columnAccess(")
            GENERATED.write(varName)
            GENERATED.write(",")
            GENERATED.write(str(element0))
            GENERATED.write(")")
            GENERATED.write("\n")
            return
    GENERATED.write(varName)
    for element in accessElements:
        GENERATED.write("[")
        GENERATED.write(str(element))
        GENERATED.write("]")
    
    #GENERATED.write("\n")

def writeListParams(listNode):
    elements=listElements(listNode)
    writeList(elements,"[","]")

def listElements(AST):
    elements=[]
    for element in AST.getChildren():
        if(element.getData()=="LIST"):
            elements+=[listElements(element)]
        else:
            elements+=[element.getChildren()[0].getData()]
    return elements