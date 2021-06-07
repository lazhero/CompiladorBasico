from stack import Stack
global TS
ARGUMENTS="ARGUMENTS"
ASSIGNMENT="ASSIGNMENT"
METHODCALL="METHODCALL"
FUNCTIONCALL="FUNCTIONCALL"

def program(AST):
    for i in AST.getChildren():
        procedure(i)
def procedure(AST):
    Scope_Stack=Stack()
    Scope_Stack.push(AST.getChildren()[0][1])
    Scope_Count=0
    for statement in AST.getChildren()[1:]:
        Scope_Count=statement_classifier(AST,Scope_Count)

def arguments(AST,ScopeCount,ScopeStack):
    pass
    

def function_call(AST,ScopeCount,ScopeStack):
    pass
def assignment(AST,ScopeCount,ScopeStack):
    pass
def method_call(AST,ScopeCount,ScopeStack):
    pass
def statement_classifier(AST,ScopeCount,ScopeStack):
    StatementName=AST.getData()
    if(StatementName==ARGUMENTS):
        return arguments(AST,ScopeCount,ScopeStack)
    if(StatementName==ASSIGNMENT):
        return assignment(AST,ScopeCount,ScopeStack)
    if(StatementName==METHODCALL):
        return method_call(AST,ScopeCount,ScopeStack)
    if(StatementName==FUNCTIONCALL):
        return function_call(AST,ScopeCount,ScopeStack)
    else:
        return ScopeCount
