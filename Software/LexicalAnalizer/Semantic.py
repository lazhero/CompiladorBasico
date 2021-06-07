from stack import Stack
global TS
TS={}
ARGUMENTS="ARGUMENTS"
PARAMETERS="PARAMETERS"
ASSIGNMENT="ASSIGNMENT"
METHODCALL="METHODCALL"
FUNCTIONCALL="FUNCTIONCALL"
SCOPE="SCOPE"

def program(AST):
    for i in AST.getChildren():
        procedure(i)
def procedure(AST):
    Scope_Stack=Stack()
    Scope_Stack.push(AST.getChildren()[0][1])
    Scope_Count=0
    process_children(AST,Scope_Count,Scope_Stack)

def scope(AST,ScopeCount,ScopeStack):
    ScopeStack.push("SCOPE"+str(ScopeCount))
    ScopeCount += 1
    ScopeCount = process_children(AST,ScopeCount,ScopeStack)
    ScopeStack.pop()
    return ScopeCount
    
def parameters(AST,ScopeCount,ScopeStack,funcName):
    parameters=AST[1]
    return ScopeCount
    
def function_call(AST,ScopeCount,ScopeStack):
    pass

def method_call(AST,ScopeCount,ScopeStack):
    pass

def assignment(AST,ScopeCount,ScopeStack):
    pass

def statement_classifier(statement,ScopeCount,ScopeStack):
    StatementName=statement.getData()
    if (StatementName==SCOPE):
        return scope(statement,ScopeCount,ScopeStack)
    if(StatementName==PARAMETERS):
        return parameters(statement,ScopeCount,ScopeStack,0)
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