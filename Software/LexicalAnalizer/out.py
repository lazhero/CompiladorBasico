import sys
sys.path.append(r"/home/lazh/TecnologicoCostaRica/QuintoSemestre/Compi/LedAnimator/LedAnimator\Hardware")
from Controller_Serial import *
def main():
	matrix=[[True,True,True,],[True,False,True,],[True,False,False,],]
	SHAPE_F(matrix,)
	var=[]
	pollo(var,)
def pollo(matrix,):
	mat=	matrix=	INSERT(matrix,[True,True,False,],0,1,)
	lenMat=	SHAPE_F(mat,)
	lenMatcol=	SHAPE_C(mat,)
	mat=	NEG(mat,)
	DELAY(5,"Seg",)
	mat[0:2]=	T_METHOD(mat[0:2])
	BLINK(mat,2,"Seg",True,)
	DELAY(10,"Seg",)
	BLINK(mat,2,"Seg",False,)
	listp=[True,]
	for uniquei in range(0,10,1):
		
		hola=2
		hola=3
main()