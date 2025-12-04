class LinkedList:
    class Node:
        def __init__(self, data):
            self.data = data
            self.next = None
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
    def append(self, data):
        new_node = self.Node(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1
    def display(self):
        current = self.head
        while current:
            print(current.data, end=" ")
            current = current.next
    def __iter__(self):
        current = self.head
        while current:
            yield current.data
            current = current.next