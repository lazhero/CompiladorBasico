
from m_tree import *
from stack import Stack
def TS_FROM_m_tree(Node):
    stack=Stack()
    TS={}
    return TS_FROM_m_tree_aux(Node,stack,0,TS)


def TS_FROM_m_tree_aux(Node,Stack,ScopeCount,TS):
    for i in Node.getChildren():
        print("CACA")
        if(i.getData=="SCOPE"):
            print("EL MEXICANO CON EL PENE ESE")
            Stack.push("SCOPE"+str(ScopeCount))
            ScopeCount+=1
            TS_FROM_m_tree_aux(i,Stack,ScopeCount,TS)
            Stack.pop()
        if(i.getData=="IDENTIFIER"):
            print("PENE con tremendo culote")
            TS[(Stack.copy(),i.getChildren())]=[]
    return TS

            
