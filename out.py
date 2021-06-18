import sys
sys.path.append(r"d:\Github Repositorios\LedAnimator\Hardware")
from Controller_Serial import *
def main():
	A=[[False,False,False,True,True,False,False,False,],[False,False,True,True,True,True,False,False,],[False,True,True,False,False,True,True,False,],[True,True,False,False,False,False,True,True,],[True,True,True,True,True,True,True,True,],[True,True,True,True,True,True,True,True,],[True,True,False,False,False,False,True,True,],[True,True,False,False,False,False,True,True,],]
	L=[[True,True,False,False,False,False,False,False,],[True,True,False,False,False,False,False,False,],[True,True,False,False,False,False,False,False,],[True,True,False,False,False,False,False,False,],[True,True,False,False,False,False,False,False,],[True,True,False,False,False,False,False,False,],[True,True,True,True,True,True,True,False,],[True,True,True,True,True,True,True,False,],]
	C=[[False,False,True,True,True,True,False,False,],[False,True,True,True,True,True,True,False,],[True,True,False,False,False,False,False,False,],[True,True,False,False,False,False,False,False,],[True,True,False,False,False,False,False,False,],[True,True,False,False,False,False,False,False,],[False,True,True,True,True,True,True,False,],[False,False,True,True,True,True,False,False,],]
	E=[[True,True,True,True,True,True,True,True,],[True,True,True,True,True,True,True,True,],[True,True,False,False,False,False,False,False,],[True,True,True,True,True,True,True,True,],[True,True,True,True,True,True,True,True,],[True,True,False,False,False,False,False,False,],[True,True,True,True,True,True,True,True,],[True,True,True,True,True,True,True,True,],]
	SMILE()
def pass_word(matrix,):
	mat=[[False,False,False,False,False,False,False,False,],[False,False,False,False,False,False,False,False,],[False,False,False,False,False,False,False,False,],[False,False,False,False,False,False,False,False,],[False,False,False,False,False,False,False,False,],[False,False,False,False,False,False,False,False,],[False,False,False,False,False,False,False,False,],[False,False,False,False,False,False,False,False,],]
	for var in range(0,8,1):
		
		PRINT_LED_X("M",0,mat,)
		mat=		DELETE(mat,0,0,)
		lis=		matrix[var]
		mat=		INSERT(mat,lis,0,7,)
main()