class LinkedList:
    
    # initial_elements: allow the collection to start with some elements
    def __init__(self, initial_elements=[]):
        self.elementos = [None] * 100  # Tamaño fijo de la colección
        for i, elemento in enumerate(initial_elements):
            if i < len(self.elementos):
                self.elementos[i] = elemento
            else:
                raise Exception("La colección no puede contener más de 100 elementos")
    
    # return an str of the collection
def __str__(self):
    elementos = [e for e in self.elementos if e is not None]
    return f"LinkedList con {len(self)} elementos: {elementos}"

    # return the length of the elements in the collection
def __len__(self):
        return len([elemento for elemento in self.elementos if elemento is not None])
    
    # return the element of the collection in the index possition
    # Error: the index dont exist
def __getitem__(self, index):
    elementos = [e for e in self.elementos if e is not None]
    if 0 <= index < len(elementos):
        return elementos[index]
    raise IndexError("Índice fuera de rango")

    # return a boolean that implies if the collection is empty or not
def isEmpty(self):
        return all(elemento is None for elemento in self.elementos)
    
    # allow the collection to be called in a for loop
def __iter__(self):
        for elemento in self.elementos:
            if elemento is not None:
                yield elemento
    
    # return a boolean value representing the existence of an element in the collection
def __contains__(self, element):
        return element in self.elementos
    
    # add the element to the end of the collection
def append(self, element):
        for i in range(len(self.elementos)):
            if self.elementos[i] is None:
                self.elementos[i] = element
                return
        raise Exception("La colección está llena")
    
    # add the element to the collection at the requested index
    # Error: non existing index in the collection
def insert(self, index, element):
    elementos = [e for e in self.elementos if e is not None]
    if index < 0 or index > len(elementos):
        raise IndexError("Índice fuera de rango")
    if len(elementos) >= 100:
        raise Exception("La colección está llena")
    elementos.insert(index, element)
    for i, e in enumerate(elementos):
        self.elementos[i] = e

    # remove an element in the collection by its value
    # Error: the element dont exist in the collection
def remove(self, element):
        for i in range(len(self.elementos)):
            if self.elementos[i] == element:
                self.elementos[i] = None
                return
        raise ValueError("El elemento no existe en la colección")
    
    # remove and return the element in the collection by its index
def pop(self, index):
    elementos = [e for e in self.elementos if e is not None]
    if 0 <= index < len(elementos):
        element = elementos[index]
        self.remove(element)
        return element
    raise IndexError("Índice fuera de rango")
    
    # remove all elements in the collection
def clear(self):
        self.elementos = [None] * len(self.elementos)