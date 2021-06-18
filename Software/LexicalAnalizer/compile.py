import sys
import subprocess
import os
from Lex import lex_syntx 
from Semantic import SEMANTIC
sys.tracebacklimit = 0
def compile(filename):
    print(filename)
    currentPath=os.path.abspath(__file__)
    currentPath=os.path.dirname(currentPath)
    currentPath=os.path.dirname(currentPath)
    currentPath=os.path.dirname(currentPath)
    print(currentPath)
    Tree=lex_syntx(filename)
    route=os.path.dirname(filename)
    returning = SEMANTIC(Tree,route,currentPath)
    print("File compiled successfully")
    
    return returning
    
def compile_and_run(filename):
    outputFile=compile(filename)

    command = command = ["python",outputFile,"main"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    print(output)
    print(error)
#if __name__ == '__main__':
 #   globals()[sys.argv[1]](sys.argv[2])
compile("/home/lazh/TecnologicoCostaRica/QuintoSemestre/Compi/LedAnimator/LedAnimator/Software/LexicalAnalizer/fuente.wage")