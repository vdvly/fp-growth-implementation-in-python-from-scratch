class HashNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashTable:
    """HashTable générique fonctionnant avec tout type de clé et de valeur."""
    def __init__(self, size=16):
        self.size = size
        self.table = [None] * size

    def hash_function(self, key):
        """Fonction de hachage par défaut."""
        return hash(key) % self.size

    def put(self, key, value):
        index = self.hash_function(key)
        node = self.table[index]

        if not node:
            self.table[index] = HashNode(key, value)
            return

        prev = None
        while node:
            if node.key == key:
                node.value = value  # met à jour si existe
                return
            prev = node
            node = node.next

        prev.next = HashNode(key, value)

    def get(self, key):
        index = self.hash_function(key)
        node = self.table[index]
        while node:
            if node.key == key:
                return node.value
            node = node.next
        return None

    def delete(self, key):
        index = self.hash_function(key)
        node = self.table[index]
        prev = None
        while node:
            if node.key == key:
                if prev:
                    prev.next = node.next
                else:
                    self.table[index] = node.next
                return True
            prev = node
            node = node.next
        return False

    def items(self):
        """Itérateur sur toutes les paires (clé, valeur)."""
        for bucket in self.table:
            node = bucket
            while node:
                yield (node.key, node.value)
                node = node.next

    def display(self):
        for i, node in enumerate(self.table):
            print(f"{i}:", end=" ")
            curr = node
            while curr:
                print(f"({curr.key}: {curr.value}) ->", end=" ")
                curr = curr.next
            print("None")