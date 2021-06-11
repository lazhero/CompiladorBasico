from typing import Type

class Stack:
    def __init__(self):
        self.List=[]
    def push(self,Element):
        if(len(self.List)==0):
            self.List=[Element]
        else:
            First_Element=self.List[0]
            if(type(First_Element)==type(Element)):
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
    def copy(self):
        return list_to_stack(self.List.copy())
        
    def stack_to_list(self):
        return self.List
    def is_empty(self):
        return self.List==[]



def list_to_stack(stack_list):
    stack=Stack()
    for i in range(-1,-len(stack_list)-1,-1):
        stack.push(stack_list[i])
    return stack
