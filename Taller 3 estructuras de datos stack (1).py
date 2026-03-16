class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class Stack:

    def __init__(self, initial_elements=[]):
        self.top = None  
        self.size = 0
        for element in initial_elements:
            self.push(element)

    def __str__(self):
        if self.top is None:
            return "[]"
        elements = []
        current = self.top
        while current:
            elements.append(str(current.data))
            current = current.next
        return "TOP -> [" + " -> ".join(elements) + "]"

    def __len__(self):
        return self.size

    def isEmpty(self):
        return self.size == 0

    def peek(self):
        if self.top is None:
            raise IndexError("peek from empty Stack")
        return self.top.data

    def __iter__(self):
        current = self.top
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
        new_node.next = self.top  
        self.top = new_node       
        self.size += 1

    def pop(self):
        if self.top is None:
            raise IndexError("pop from empty Stack")
        value = self.top.data
        self.top = self.top.next  
        self.size -= 1
        return value
    
    
    s = Stack([1, 2, 3])
print(s)            
print(len(s))       
print(s.peek())     
print(2 in s)       
print(s.isEmpty())  

s.push(4)
print(s)            

print(s.pop())      
print(s)            

for item in s:
    print(item, end=" ") 