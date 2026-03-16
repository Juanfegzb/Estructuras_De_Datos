class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class Queue:

    def __init__(self, initial_elements=[]):
        self.head = None  # frente de la cola (primer elemento en salir)
        self.tail = None  # final de la cola (último en entrar)
        self.size = 0
        for element in initial_elements:
            self.push(element)

    def __str__(self):
        if self.head is None:
            return "[]"
        elements = []
        current = self.head
        while current:
            elements.append(str(current.data))
            current = current.next
        return "FRONT -> [" + " -> ".join(elements) + "] <- BACK"

    def __len__(self):
        return self.size

    def isEmpty(self):
        return self.size == 0

    def peek(self):
        if self.head is None:
            raise IndexError("peek from empty Queue")
        return self.head.data

    def __iter__(self):
        current = self.head
        while current:
            yield current.data
            current = current.next

    def __contains__(self, element):
        for item in self:
            if item == element:
                return True
        return False

    def push(self, element):
        new_node = Node(element)
        if self.tail is None:
            self.head = new_node   # si está vacía, head y tail apuntan al mismo nodo
            self.tail = new_node
        else:
            self.tail.next = new_node  # el tail actual apunta al nuevo nodo
            self.tail = new_node       # el nuevo nodo es el nuevo tail
        self.size += 1

    def pop(self):
        if self.head is None:
            raise IndexError("pop from empty Queue")
        value = self.head.data
        self.head = self.head.next    # el head pasa a ser el siguiente
        if self.head is None:
            self.tail = None          # si la cola quedó vacía, tail también es None
        self.size -= 1
        return value
    
    
    q = Queue([1, 2, 3])
print(q)            # FRONT -> [1 -> 2 -> 3] <- BACK
print(len(q))       # 3
print(q.peek())     # 1
print(2 in q)       # True
print(q.isEmpty())  # False

q.push(4)
print(q)            # FRONT -> [1 -> 2 -> 3 -> 4] <- BACK

print(q.pop())      # 1
print(q)            # FRONT -> [2 -> 3 -> 4] <- BACK

for item in q:
    print(item, end=" ")  # 2 3 4