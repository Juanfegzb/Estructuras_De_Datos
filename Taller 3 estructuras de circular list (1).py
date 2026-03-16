class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class CircularList:

    def __init__(self, initial_elements=[]):
        self.tail = None  # tail.next apunta al head (circular)
        self.size = 0
        for element in initial_elements:
            self.append(element)

    def __str__(self):
        if self.tail is None:
            return "[]"
        elements = []
        current = self.tail.next  # head
        for _ in range(self.size):
            elements.append(str(current.data))
            current = current.next
        return "[" + " -> ".join(elements) + " -> (head)]"

    def __len__(self):
        return self.size

    def __getitem__(self, index):
        if index < 0 or index >= self.size:
            raise IndexError(f"Index {index} out of range for CircularList of size {self.size}")
        current = self.tail.next  # head
        for _ in range(index):
            current = current.next
        return current.data

    def isEmpty(self):
        return self.size == 0

    def __iter__(self):
        if self.tail is None:
            return
        current = self.tail.next  # head
        for _ in range(self.size):
            yield current.data
            current = current.next

    def __contains__(self, element):
        for item in self:
            if item == element:
                return True
        return False

    def append(self, element):
        new_node = Node(element)
        if self.tail is None:
            new_node.next = new_node  # apunta a sí mismo
            self.tail = new_node
        else:
            new_node.next = self.tail.next  # new_node -> head
            self.tail.next = new_node       # tail -> new_node
            self.tail = new_node            # new_node es el nuevo tail
        self.size += 1

    def add(self, index, element):
        if index < 0 or index > self.size:
            raise IndexError(f"Index {index} out of range for CircularList of size {self.size}")
        new_node = Node(element)
        if self.tail is None or index == self.size:
            self.append(element)
            return
        if index == 0:
            new_node.next = self.tail.next  # new_node -> head
            self.tail.next = new_node       # tail -> new_node (nuevo head)
        else:
            current = self.tail.next        # head
            for _ in range(index - 1):
                current = current.next
            new_node.next = current.next
            current.next = new_node
        self.size += 1

    def remove(self, element):
        if self.tail is None:
            raise ValueError(f"Element '{element}' not found in CircularList")
        current = self.tail.next  # head
        prev = self.tail
        for _ in range(self.size):
            if current.data == element:
                if self.size == 1:
                    self.tail = None
                else:
                    prev.next = current.next
                    if current == self.tail:
                        self.tail = prev
                self.size -= 1
                return
            prev = current
            current = current.next
        raise ValueError(f"Element '{element}' not found in CircularList")

    def pop(self, index):
        if index < 0 or index >= self.size:
            raise IndexError(f"Index {index} out of range for CircularList of size {self.size}")
        current = self.tail.next  # head
        prev = self.tail
        for _ in range(index):
            prev = current
            current = current.next
        value = current.data
        if self.size == 1:
            self.tail = None
        else:
            prev.next = current.next
            if current == self.tail:
                self.tail = prev
        self.size -= 1
        return value

    def clear(self):
        self.tail = None
        self.size = 0
        
        
        cl = CircularList([1, 2, 3, 4])
print(cl)           # [1 -> 2 -> 3 -> 4 -> (head)]
print(len(cl))      # 4
print(cl[2])        # 3
print(3 in cl)      # True
print(cl.isEmpty()) # False

cl.append(5)
cl.add(0, 0)        # inserta al inicio
print(cl)           # [0 -> 1 -> 2 -> 3 -> 4 -> 5 -> (head)]

cl.remove(3)
print(cl)           # [0 -> 1 -> 2 -> 4 -> 5 -> (head)]

popped = cl.pop(1)
print(popped)       # 1

for item in cl:
    print(item, end=" ")  # 0 2 4 5