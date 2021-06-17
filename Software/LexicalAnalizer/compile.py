import sys
import os
from Lex import lex_syntx 
from Semantic import SEMANTIC
def compile(filename):
    currentPath=os.path.abspath(__file__)
    currentPath=os.path.dirname(currentPath)
    currentPath=os.path.dirname(currentPath)
    currentPath=os.path.dirname(currentPath)
    print(currentPath)
    Tree=lex_syntx(filename)
    route=os.path.dirname(filename)
    SEMANTIC(Tree,route,currentPath)
    return "hola"
    
#if __name__ == '__main__':
 #   globals()[sys.argv[1]](sys.argv[2])
compile("C:/Users/allva/Desktop/LedAnimator/Software/LexicalAnalizer/fuente.wage")