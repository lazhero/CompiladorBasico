
from m_tree import *
from stack import Stack

global ScopeCount
ScopeCount=0

def TS_FROM_m_tree(Node):
    global ScopeCount
    ScopeCount=0
    stack=Stack()
    TS={}
    return TS_FROM_m_tree_aux(Node,stack,TS)

    
def TS_FROM_m_tree_aux(Node,Stack,TS):
    for i in Node.getChildren():
        if(i.getData()=="SCOPE"):
            global ScopeCount
            Stack.push("SCOPE"+str(ScopeCount))
            ScopeCount+=1
            TS_FROM_m_tree_aux(i,Stack,TS)
            Stack.pop()
        elif(i.getData()=="IDENTIFIER"):
            names = id_names(i.getChildren())
            TS[(tuple(Stack.stack_to_list()),tuple(names))]=[]
        
        else:
            TS_FROM_m_tree_aux(i,Stack,TS)
    #print(TS)
    return TS
    
def id_names(hijos):
    lista=[]
    for i in hijos:
        lista+=[i.getData()]
    return lista


'''
procedure 
'''