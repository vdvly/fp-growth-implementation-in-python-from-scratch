
from HashTable import ChainHashMap
class Fp_node:
    def __init__(self, value, count=1, parent=None):
        self.value = value
        self.count = count
        self.children = ChainHashMap()  
        self.parent = parent

    def increment_count(self):
        self.count += 1

    def add_child(self, child_node):
        """Ajoute un enfant dans la table de hachage"""
        self.children[child_node.value] = child_node

    def get_child(self, value):
        """Retourne l’enfant si existe"""
        try:
            return self.children[value]
        except KeyError:
            return None

    def display(self, level=0):
        print("* " * level + f"{self.value}: {self.count}")
        # afficher les enfants en parcourant la ChainHashMap
        for key in self.children:
            self.children[key].display(level + 1)


class FP_Tree:
    def __init__(self):
        self.root = Fp_node("Root", count=0)
        self.header_table = ChainHashMap()  # {item: [count, [liste de nœuds]]}

    def update_header(self, item, node):
        """Met à jour la table d’en-tête"""
        try:
            entry = self.header_table[item]
            entry[0] += node.count
            entry[1].append(node)
            self.header_table[item] = entry
        except KeyError:
            self.header_table[item] = [node.count, [node]]
    def add_transactions(self, transactions):
        freq = ChainHashMap()
        for tr in transactions:
            for item in tr:
                try:
                    count = freq[item]
                    freq[item] = count + 1
                except KeyError:
                    freq[item] = 1
        for tr in transactions:
            res =[]
            for item in tr:
                try:
                    count = freq[item]
                except KeyError:
                    count = 0
                res.append((count, item))
            res.sort(reverse=True)
            self.add_transaction(res[i][1] for i in range (len(res)))
    def add_transaction(self, tr):
        """Ajoute une transaction (liste d’items) dans le FP-Tree"""
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
        for item in self.header_table:
            count, nodes = self.header_table[item]
            print(f"{item}: count={count}, occurrences={len(nodes)}")

