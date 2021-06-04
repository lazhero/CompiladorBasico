class m_node:
    def __init__(self,Name,Children):
        self.Name=Name
        self.Children=Children
    def inorder(self):
        List=[self.Name]
        if(self.Children==[]):
            return self.Name
        for i in self.Children:

            List+=[i.inorder()]
        return List   
    def getChildren(self):
        return self.Children
    def getData(self):
        return self.Name
    def isLeaf(self):
        return self.Children==[]
def create_tree_from_list(lista):
    if(not isinstance(lista,list)):
        return m_node(lista,[])
    if(len(lista)<=0):
        return None
    if(len(lista)==1):
        return m_node(lista[0],[])
    else:
        Sons=[]
        for i in lista[1:]:
            Sons+=[create_tree_from_list(i)]
        Tree=m_node(lista[0],Sons)
        return Tree




    