from typing import Type

class Stack:
    def __init__(self):
        self.List=[]
    def push(self,Element):
        if(len(self.List)==0):
            self.List=[Element]
        else:
            First_Element=self.List[0]
            if(Type(First_Element)==Type(Element)):
                self.List+=[Element]
    def peek(self):
        if(self.List==[]):
            return None
        else:
            return self.List[0]
    def pop(self):
        Element=self.peek()
        if(Element!=None):
            self.List=self.List[1:]
    


