"parent"
"children"
"nb children"
"find child (e)"
"attach child parent"
"ancestors"
"print textuel"
"visualize"

from graphviz import Digraph
from HashTable import ChainHashMap

class TreeNode:

    __slots__ = "value", "parent", "children"
    def __init__(self, value):
        self.value = value
        self.parent = None
        #self.children = []#hash
        self.children = ChainHashMap()
    def get_parent(self):
        return self.parent

    def get_children(self):
        #return self.children
        return [self.children[k] for k in self.children]
    def nb_children(self):
        return len(self.children)

    def find_child(self, value):
        """Find and return the first direct child with the given value(valeur li yhezha)"""
        #for child in self.children:
        #    if child.value == value:
        #        return child
        #return None
        try:
            return self.children[value]
        except KeyError:
            return None

    def attach_child(self, child):
        #child.parent = self
        #self.children.append(child)
        if child.value not in self.children:
            child.parent = self
            self.children[child.value] = child

    def ancestors(self):
        """lest des ancestors jusqu'a root"""
        current = self.parent
        ancestors = []
        while current:
            ancestors.append(current)
            current = current.parent
        return ancestors

    # visualisation adcii
    def print_textual(self, level=0):
        print("  " * level + f"- {self.value}")
        for child in self.children:
            child.print_textual(level + 1)

    # visualisation graphic avec graphviz Digraph
    def visualize(self, filename="tree", view=True):
        dot = Digraph(comment="General Tree", format='png')
        self._add_nodes(dot)
        dot.render(filename, view=view)

    def _add_nodes(self, dot):
        dot.node(str(id(self)), str(self.value))
        for child in self.children:
            dot.node(str(id(child)), str(child.value))
            dot.edge(str(id(self)), str(id(child)))
            child._add_nodes(dot)


#EXEMPLE
if __name__ == "__main__":
    root = TreeNode("A")
    b = TreeNode("B")
    c = TreeNode("C")
    d = TreeNode("D")
    e = TreeNode("E")
    f = TreeNode("F")
    x  = TreeNode("X")

    root.attach_child(b)
    root.attach_child(c)
    b.attach_child(d)
    b.attach_child(e)
    c.attach_child(f)
    f.attach_child(x)

    print("Textual Tree:")
    root.print_textual()

    print("\nAncestors of x:", [a.value for a in x.ancestors()])
    print("Number of children of B:", b.nb_children())

    
    root.visualize("tree_example")
