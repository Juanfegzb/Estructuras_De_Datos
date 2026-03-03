class OrderList:
    
    # initial_elements: allow the collection to start with some elements
    def __init__(self, initial_elements=[]):
        self .elements = initial_elements
    
    # return an str of the collection
    def __str__(self):
        return str(self.elements)
    
    # return the length of the elements in the collection
    def __len__(self):
        return  len(self.elements)
    
    # return the element of the collection in the index possition
    # Error: the index dont exist
    def __getitem__(self, index):
        if index < 0 or index >= len(self.elements):
            raise IndexError("Index out of bounds")
        return self.elements[index]

    # return a boolean that implies if the collection is empty or not
    def isEmpty(self):
        return len(self.elements) == 0
    
    # allow the collection to be called in a for loop
    def __iter__(self):
        return iter(self.elements)
    
    # return a boolean value representing the existence of an element in the collection
    def __contains__(self, element):
        return element in self.elements
    
    # add the element to the end of the collection
    def add(self, element):
        self.elements.append(element)
    
    # remove an element in the collection by its value
    # Error: the element dont exist in the collection
    def remove(self, element):
        if element not in self.elements:
            raise ValueError("Element not found in the collection")
        self.elements.remove(element)
    
    # remove and return the element in the collection by its index
    def pop(self, index):
        if index < 0 or index >= len(self.elements):
            raise IndexError("Index out of bounds")
        return self.elements.pop(index)
    
    # remove all elements in the collection
    def clear(self):
        self.elements.clear()