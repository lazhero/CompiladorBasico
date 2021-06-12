import sys
from Lex import lex_syntx 
from Semantic import SEMANTIC
def compile(filename):
    Tree=lex_syntx(filename)
    SEMANTIC(Tree)
    #aqui llamariamos a la funcion que genera codigo a partir del arbol 
    return "hola"
if __name__ == '__main__':
    globals()[sys.argv[1]](sys.argv[2])