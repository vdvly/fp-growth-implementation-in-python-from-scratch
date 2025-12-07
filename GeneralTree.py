"parent"
"children"
"nb children"
"find child (e)"
"attach child parent"
"ancestors"
"print textuel"
"visualize"

try:
    from graphviz import Digraph
    _GV_AVAILABLE = True
except Exception:
    _GV_AVAILABLE = False
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
        for key in self.children:
            self.children[key].print_textual(level + 1)

    # visualisation graphic avec graphviz Digraph
    def visualize(self, filename="tree", view=True):
        if not _GV_AVAILABLE:
            print("Graphviz not installed; skipping visualization.")
            return
        dot = Digraph(comment="General Tree", format='png')
        self._add_nodes(dot)
        dot.render(filename, view=view)

    def _add_nodes(self, dot):
        dot.node(str(id(self)), str(self.value))
        for child in self.children:
            dot.node(str(id(child)), str(child.value))
            dot.edge(str(id(self)), str(id(child)))
            child._add_nodes(dot)


