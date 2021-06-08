from descriptors import function_descriptor
from const import reserved_function_names as prebuild
from const import reserved_function_params as reserved_params
from stack import Stack

global TS
TS={} #Table Symbol
ARGUMENTS="ARGUMENTS"
PARAMETERS="PARAMETERS"
ASSIGNMENT="ASSIGNMENT"
METHODCALL="METHODCALL"
FUNCTIONCALL="FUNCTIONCALL"
SCOPE="SCOPE"

def program(AST):
    if not procedure_setting(AST):
        raise Exception("No main found")
    for i in AST.getChildren():
        procedure(i)

        
def procedure(AST):
    Scope_Stack=Stack()
    Scope_Stack.push(get_identifier(AST))
    Scope_Count=0
    process_children(AST,Scope_Count,Scope_Stack)

def scope(AST,ScopeCount,ScopeStack):
    ScopeStack.push("SCOPE"+str(ScopeCount))
    ScopeCount += 1
    ScopeCount = process_children(AST,ScopeCount,ScopeStack)
    ScopeStack.pop()
    return ScopeCount
    
def function_call(AST,ScopeCount,ScopeStack):
    pass

def method_call(AST,ScopeCount,ScopeStack):
    pass

def assignment(AST,ScopeCount,ScopeStack):
    # var1 = var2
    # var1 = 5
    # var1 = 2.3
    # var1 = [1,2,3]
    # var1 = True
    # var1 = 4+3*123-(12.2-3.14)+lista[0]
    # var1 = [True,True,True].Neg
    stack = ScopeStack.copy()
    identifier = get_identifier(AST) 

    pass

def statement_classifier(statement,ScopeCount,ScopeStack):
    print(statement.getData())
    StatementName=statement.getData()
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

def process_children(AST,Scope_Count,Scope_Stack):
    for statement in AST.getChildren()[1:]:
        Scope_Count=statement_classifier(statement,Scope_Count,Scope_Stack)
    return Scope_Count

def in_TS(id_tuple):
    return id_tuple in TS.keys()


def procedure_setting(AST):
    main_flag=False
    for i in AST.getChildren():
       
        proc_name= get_identifier(i)
        parameters=getParamstypes(i)
        print(parameters)
        param_numbers=len(i.getChildren()[1].getData()[1:])
        procedure=function_descriptor(proc_name,parameters)
        TS[((proc_name),())]=procedure
        if (proc_name=="main"):
            main_flag=True
    return main_flag

def getParamstypes(AST):
    datatype=""
    typeslist=[]
    for i in AST.getChildren()[1].getChildren():
        try:
            datatype=i.getChildren()[1].getData()
            typeslist+=[datatype]
        except:
            return []
    return typeslist



def prebuild_setting():
    for value in prebuild.values:
        procedure=function_descriptor(value,reserved_params[value])
        TS[((value),())]=procedure
    


def get_identifier(AST):
    return AST.getChildren()[0].getChildren()[0].getData()