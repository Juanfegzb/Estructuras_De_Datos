class ArrayList:
    
    # tamaño: capacidad inicial de la colección
    # elementos_iniciales: permite que la colección inicie con algunos elementos
     # retorna una representación en cadena (str) de la colección
def __init__(self, tamaño=100, elementos_iniciales=None):
        self.tamaño = tamaño
        self.elementos = [None] * tamaño
        if elementos_iniciales is not None:
            for i, elemento in enumerate(elementos_iniciales):
                if i < tamaño:
                    self.elementos[i] = elemento
                else:
                    break
        
     # retorna la cantidad de elementos en la colección
def __str__(self):
        elementos_str = len ([elemento for elemento in self.elementos if elemento is not None])
        return f"ArrayList con {elementos_str} elementos: {[elemento for elemento in self.elementos if elemento is not None]}"
  
    # retorna un valor booleano que indica si la colección está vacía o no
def __len__(self): 
        valor = len ([elemento for elemento in self.elementos if elemento is not None])
        return valor
def estaVacia(self):
        return len(self) == 0
    
    
    # retorna el elemento de la colección en la posición índice
    # Error: el índice no existe
def __getitem__(self, index):
    elementos = [e for e in self.elementos if e is not None]
    if 0 <= index < len(elementos):
        return elementos[index]
    raise IndexError("Índice fuera de rango")
    
    # permite que la colección pueda usarse en un ciclo for
 def __iter__(self):
        for elemento in self.elementos:
            if elemento is not None:
                yield elemento
    
    # retorna un valor booleano que indica si un elemento existe en la colección
def __contains__(self, elemento):
        return elemento in [e for e in self.elementos if e is not None]
    
    # agrega un elemento al final de la colección
def agregar(self, elemento):
        for i in range(len(self.elementos)):
            if self.elementos[i] is None:
                self.elementos[i] = elemento
                return
        raise Exception("La colección está llena")
    
    # agrega un elemento en la posición índice solicitada
    # Error: índice inexistente en la colección
def insert(self, index, element):
    elementos = [e for e in self.elementos if e is not None]
    if index < 0 or index > len(elementos):
        raise IndexError("Índice fuera de rango")
    if len(elementos) >= self.tamaño:
        raise Exception("La colección está llena")
    elementos.insert(index, element)
    for i, e in enumerate(elementos):
        self.elementos[i] = e
    # elimina un elemento de la colección por su valor
    # Error: el elemento no existe en la colección
def eliminar(self, elemento):
        for i in range(len(self.elementos)):
            if self.elementos[i] == elemento:
                self.elementos[i] = None
                return
        raise ValueError("El elemento no existe en la colección")
    
    # elimina y retorna el elemento de la colección por su índice
def extraer(self, indice):
        if 0 <= indice < len(self.elementos) and self.elementos[indice] is not None:
            elemento = self.elementos[indice]
            self.elementos[indice] = None
            return elemento
        else:
            raise IndexError("Índice fuera de rango o elemento no existe")
    # elimina todos los elementos de la colección
def limpiar(self):
        self.elementos = [None] * len(self.elementos)