import sys
sys.path.append(r"d:\Github Repositorios\LedAnimator\Hardware")
from Controller_Serial import *
def main():
	A=[[False,False,False,True,True,False,False,False,],[False,False,True,True,True,True,False,False,],[False,True,True,False,False,True,True,False,],[True,True,False,False,False,False,True,True,],[True,True,True,True,True,True,True,True,],[True,True,True,True,True,True,True,True,],[True,True,False,False,False,False,True,True,],[True,True,False,False,False,False,True,True,],]
	L=[[True,True,False,False,False,False,False,False,],[True,True,False,False,False,False,False,False,],[True,True,False,False,False,False,False,False,],[True,True,False,False,False,False,False,False,],[True,True,False,False,False,False,False,False,],[True,True,False,False,False,False,False,False,],[True,True,True,True,True,True,True,False,],[True,True,True,True,True,True,True,False,],]
	C=[[False,False,True,True,True,True,False,False,],[False,True,True,True,True,True,True,False,],[True,True,False,False,False,False,False,False,],[True,True,False,False,False,False,False,False,],[True,True,False,False,False,False,False,False,],[True,True,False,False,False,False,False,False,],[False,True,True,True,True,True,True,False,],[False,False,True,True,True,True,False,False,],]
	E=[[True,True,True,True,True,True,True,True,],[True,True,True,True,True,True,True,True,],[True,True,False,False,False,False,False,False,],[True,True,True,True,True,True,True,True,],[True,True,True,True,True,True,True,True,],[True,True,False,False,False,False,False,False,],[True,True,True,True,True,True,True,True,],[True,True,True,True,True,True,True,True,],]
	pass_word(A,)
	pass_word(L,)
	pass_word(C,)
	pass_word(E,)
def pass_word(matrix,):
	varFor=[True,True,True,True,True,True,True,True,]
	mat=