from graphviz import Digraph
from HashTable import HashTable
class Fp_node:
    def __init__(self, value, count=1, parent=None):
        self.value = value
        self.count = count
        self.children = HashTable()  
        self.parent = parent

    def increment_count(self):
        self.count += 1

    def add_child(self, child_node):
        """Ajoute un enfant dans la table de hachage"""
        self.children.put(child_node.value, child_node)

    def get_child(self, value):
        """Retourne l’enfant si existe"""
        return self.children.get(value)

    def display(self, level=0):
        print("* " * level + f"{self.value}: {self.count}")
        # afficher les enfants en parcourant la HashTable
        for i, node in enumerate(self.children.table):
            curr = node
            while curr:
                curr.value.display(level + 1)
                curr = curr.next


class FP_Tree:
    def __init__(self):
        self.root = Fp_node("Root", count=0)
        self.header_table = HashTable()  # {item: [count, [liste de nœuds]]}

    def update_header(self, item, node):
        """Met à jour la table d’en-tête"""
        entry = self.header_table.get(item)
        if entry:
            entry[0] += 1
            entry[1].append(node)
            self.header_table.put(item, entry)
        else:
            self.header_table.put(item, [1, [node]])
    def add_transactions(self, transactions):
        freq = HashTable()
        for tr in transactions:
            for item in tr:
                count = freq.get(item)
                if count:
                    freq.put(item, count + 1)
                else:
                    freq.put(item, 1)
        for tr in transactions:
            res =[]
            for item in tr:
                count = freq.get(item)
                res.append((count, item))
            res.sort(reverse=True)
            self.add_transaction(res[i][1] for i in range (len(res)))
    def add_transaction(self, tr):
        """Ajoute une transaction (liste ditems) dans le FP-Tree"""
        current_node = self.root
        for item in tr:
                child = current_node.get_child(item)
                if child:
                    child.increment_count()
                else:
                    new_node = Fp_node(item, parent=current_node)
                    current_node.add_child(new_node)
                    self.update_header(item, new_node)
                    child = new_node
                current_node = child

    def display(self):
        print("FP-Tree:")
        self.root.display()

    def display_header_table(self):
        print("\nHeader Table:")
        for i, node in enumerate(self.header_table.table):
            curr = node
            while curr:
                item, (count, nodes) = curr.key, curr.value
                print(f"{item}: count={count}, occurrences={len(nodes)}")
                curr = curr.next