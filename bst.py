class node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
class BST:
    def __init__(self):
        self.root = None
        self.hauteur=0
    def insertion(self,n):
        x=self.root
        if x is None:
            self.root=n
            return
        if n.value<x.value:
            insertion(x.left,n)
        else:
            insertion(x.right,n)
