import sys
import os
from Lex import lex_syntx 
from Semantic import SEMANTIC
def compile(filename):
    #print(filename)
    Tree=lex_syntx(filename)
    #print(Tree.inorder())
    route=os.path.dirname(filename)
    #print(route)
    SEMANTIC(Tree)
    #aqui llamariamos a la funcion que genera codigo a partir del arbol 
    return "hola"
#if __name__ == '__main__':
 #   globals()[sys.argv[1]](sys.argv[2])
compile("C:/Users/allva/Desktop/LedAnimator/Software/LexicalAnalizer/fuente.wage")