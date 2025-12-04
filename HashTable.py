from collections.abc import MutableMapping
from random import randrange

# ----------------------------
# Simple LinkedList 
# ----------------------------
class LinkedList:
    class Node:
        def __init__(self, key, value, nxt=None):
            self.key = key
            self.value = value
            self.next = nxt

    def __init__(self):
        self.head = None

    def append(self, key, value):
        new_node = self.Node(key, value, self.head)
        self.head = new_node

    def remove(self, key):
        """Remove a node by key.true ken tnaha false sinn"""
        prev = None
        cur = self.head

        while cur:
            if cur.key == key:
                if prev is None:
                    self.head = cur.next
                else:
                    prev.next = cur.next
                return True
            prev = cur
            cur = cur.next
        return False


# ----------------------------
# Base Map class
# ----------------------------
class MapBase(MutableMapping):
    """Abstract class mel cours."""

    class _Item:
        """key w value b fazt slots."""
        __slots__ = "_key", "_value"

        def __init__(self, key, value):
            self._key = key
            self._value = value

        def __eq__(self, other):
            return self._key == other._key

        def __lt__(self, other):
            return self._key < other._key


# ----------------------------
# Hash Map Base (MAD compression)
# ----------------------------
class HashMapBase(MapBase):
    """Base class for hash maps using MAD compression."""

    def __init__(self, capacity=11, prime=109345121):
        self._table = [None] * capacity
        self._n = 0
        self._prime = prime
        self._scale = 1 + randrange(prime - 1)
        self._shift = randrange(prime)

    def _hash_function(self, key):
        return (hash(key) * self._scale + self._shift) % self._prime % len(self._table)

    def __len__(self):
        return self._n

    def __getitem__(self, key):
        j = self._hash_function(key)
        return self._bucket_getitem(j, key)

    def __setitem__(self, key, value):
        j = self._hash_function(key)
        self._bucket_setitem(j, key, value)

        # resize if load factor > 0.5 aakthr m chtar
        if self._n > len(self._table) // 2:
            self._resize(2 * len(self._table) - 1)

    def __delitem__(self, key):
        j = self._hash_function(key)
        self._bucket_delitem(j, key)

    def _resize(self, new_cap):
        """Resize and rehash all items."""
        old_items = list(self.items())
        self._table = [None] * new_cap
        self._n = 0

        for (k, v) in old_items:
            self[k] = v


# ----------------------------
# Chained Hash Map
# ----------------------------
class ChainHashMap(HashMapBase):
    """Hash map using separate chaining with linked lists."""

    def _bucket_getitem(self, j, key):
        bucket = self._table[j]
        if bucket is None:
            raise KeyError(f"Key not found: {key}")

        cur = bucket.head
        while cur:
            if cur.key == key:
                return cur.value
            cur = cur.next

        raise KeyError(f"Key not found: {key}")

    def _bucket_setitem(self, j, key, value):
        if self._table[j] is None:
            self._table[j] = LinkedList()

        bucket = self._table[j]
        cur = bucket.head

        while cur:
            if cur.key == key:
                cur.value = value
                return
            cur = cur.next

        # not found -> insert new
        bucket.append(key, value)
        self._n += 1

    def _bucket_delitem(self, j, key):
        bucket = self._table[j]
        if bucket is None or not bucket.remove(key):
            raise KeyError(f"Key not found: {key}")
        self._n -= 1

    def __iter__(self):
        """Iterate through all keys in the table."""
        for bucket in self._table:
            if bucket is not None:
                cur = bucket.head
                while cur:
                    #yield cur.key
                    cur = cur.next


# ----------------------------
# Example 
# ----------------------------
if __name__ == "__main__":
    m = ChainHashMap()
    m["name"] = "hama"
    m["age"] = 25
    m["city"] = "souussa"

    print(m["name"])      # hama
    print(len(m))         # 3

    m["age"] = 26
    print("city" in m)    # True

    for key in m:
        print(f"{key}: {m[key]}")

    del m["city"]
    print(len(m))         # 2
