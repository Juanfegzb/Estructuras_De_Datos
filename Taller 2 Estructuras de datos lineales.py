class OrderList:

    # initial_elements: allow the collection to start with some elements
    def __init__(self, initial_elements=[]):
        self.elements = []
        for element in initial_elements:
            self.add(element)

    # return an str of the collection
    def __str__(self):
        return str(self.elements)

    # return the length of the elements in the collection
    def __len__(self):
        return len(self.elements)

    # return the element of the collection in the index possition
    # Error: the index dont exist
    def __getitem__(self, index):
        if index < 0 or index >= len(self.elements):
            raise IndexError("The index does not exist")
        return self.elements[index]

    # return a boolean that implies if the collection is empty or not
    def isEmpty(self):
        return len(self.elements) == 0

    # allow the collection to be called in a for loop
    def __iter__(self):
        for element in self.elements:
            yield element

    # return a boolean value representing the existence of an element in the collection
    def __contains__(self, element):
        for e in self.elements:
            if e == element:
                return True
        return False

    # add the element to the end of the collection
    def add(self, element):
        i = 0
        while i < len(self.elements) and self.elements[i] < element:
            i += 1
        self.elements.insert(i, element)

    # remove an element in the collection by its value
    # Error: the element dont exist in the collection
    def remove(self, element):
        if element not in self.elements:
            raise ValueError("The element does not exist in the collection")
        self.elements.remove(element)

    # remove and return the element in the collection by its index
    def pop(self, index):
        if index < 0 or index >= len(self.elements):
            raise IndexError("The index does not exist")
        return self.elements.pop(index)

    # remove all elements in the collection
    def clear(self):
        self.elements = []

lista = OrderList([5,1,7,3])

print(lista)      # [1,3,5,7]

lista.add(4)
print(lista)      # [1,3,4,5,7]

print(len(lista)) # 5

print(lista[2])   # 4

lista.remove(3)
print(lista)      # [1,4,5,7]

print(4 in lista) # True