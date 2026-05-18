from collections import deque #  sirve para hacer una cola eficiente para BFS
from copy import deepcopy # para crear copias profundas del cubo sin referencias compartidas
import matplotlib.pyplot as plt # para visualización del cubo usando Matplotlib
import matplotlib.patches as patches # para dibujar rectángulos que representan las piezas del cubo
import matplotlib.animation as animation # para animar la solución paso a paso
COLOR_MAP = { # Mapa de colores para la visualización
    'B': 'white',      # Blanco (Arriba)
    'Y': 'yellow',     # Amarillo (Abajo)
    'R': 'red',        # Rojo (Derecha)
    'O': 'orange',     # Naranja (Izquierda)
    'G': 'green',      # Verde (Frente)
    'P': 'blue',       # Azul (Atrás)
    ' ': None
}
class CuboRubikHibrido: # Representación del cubo Rubik usando una estructura de datos híbrida    
    def __init__(self):
        # Cada cara se representa como una matriz 3x3, y el cubo completo es un diccionario de caras
        self.caras = {
            'U': [['B', 'B', 'B'], ['B', 'B', 'B'], ['B', 'B', 'B']],
            'D': [['Y', 'Y', 'Y'], ['Y', 'Y', 'Y'], ['Y', 'Y', 'Y']],
            'L': [['O', 'O', 'O'], ['O', 'O', 'O'], ['O', 'O', 'O']],
            'R': [['R', 'R', 'R'], ['R', 'R', 'R'], ['R', 'R', 'R']],
            'F': [['G', 'G', 'G'], ['G', 'G', 'G'], ['G', 'G', 'G']],
            'B': [['P', 'P', 'P'], ['P', 'P', 'P'], ['P', 'P', 'P']]
        }
    
    def obtener_plantilla_2d(self): # Crea una plantilla 2D para visualización
        plantilla = [
            [" ", " ", " ", "B", "B", "B", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", "B", "B", "B", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", "B", "B", "B", " ", " ", " ", " ", " ", " "],
            ["O", "O", "O", "G", "G", "G", "R", "R", "R", "P", "P", "P"],
            ["O", "O", "O", "G", "G", "G", "R", "R", "R", "P", "P", "P"],
            ["O", "O", "O", "G", "G", "G", "R", "R", "R", "P", "P", "P"],
            [" ", " ", " ", "Y", "Y", "Y", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", "Y", "Y", "Y", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", "Y", "Y", "Y", " ", " ", " ", " ", " ", " "],
        ]
        for i in range(3): # Cara U (Arriba)
            for j in range(3):
                plantilla[i][j+3] = self.caras['U'][i][j] # Coloca la cara U en la plantilla
                
        for i in range(3): # Caras L, F, R, B (Medio)
            plantilla[i+3][0:3] = self.caras['L'][i]
            plantilla[i+3][3:6] = self.caras['F'][i]
            plantilla[i+3][6:9] = self.caras['R'][i]
            plantilla[i+3][9:12] = self.caras['B'][i]
        
        for i in range(3): # Cara D (Abajo) 
            for j in range(3):
                plantilla[i+6][j+3] = self.caras['D'][i][j]  # Coloca la cara D en la plantilla
        
        return plantilla # Devuelve la plantilla 2D actualizada con el estado del cubo
    
    def obtener_estado(self): # Devuelve el estado actual del cubo como una tupla para uso en BFS
        estado = []
        for cara in ['U', 'D', 'L', 'R', 'F', 'B']: # Recorre las caras en un orden específico para mantener consistencia
            for fila in self.caras[cara]:
                estado.extend(fila) # Agrega cada fila de la cara al estado completo del cubo
        return tuple(estado)
    
    def rotacion_horaria(self, cara): # Rota una cara 90° horario
        self.caras[cara] = [
            [self.caras[cara][2][0], self.caras[cara][1][0], self.caras[cara][0][0]], # Rota la cara en sentido horario
            [self.caras[cara][2][1], self.caras[cara][1][1], self.caras[cara][0][1]],
            [self.caras[cara][2][2], self.caras[cara][1][2], self.caras[cara][0][2]]
        ]
    
    def mover_U(self): # Mueve la cara U (Arriba) en sentido horario y ajusta las piezas adyacentes
        self.rotacion_horaria('U')
        temp = [self.caras['F'][0][i] for i in range(3)] # Guarda la fila superior de la cara F antes de moverla
        for i in range(3):
            self.caras['F'][0][i] = self.caras['L'][0][i]
            self.caras['L'][0][i] = self.caras['B'][0][i]
            self.caras['B'][0][i] = self.caras['R'][0][i]
            self.caras['R'][0][i] = temp[i]
    
    def mover_U2(self): # Mueve la cara U dos veces (180°)
        self.mover_U()
        self.mover_U()
    
    def mover_U_(self): # Mueve la cara U en sentido antihorario (270° horario)
        for _ in range(3):
            self.mover_U()
    
    def mover_D(self): # Mueve la cara D (Abajo) en sentido horario y ajusta las piezas adyacentes
        self.rotacion_horaria('D')
        temp = [self.caras['F'][2][i] for i in range(3)]
        for i in range(3):
            self.caras['F'][2][i] = self.caras['R'][2][i]
            self.caras['R'][2][i] = self.caras['B'][2][i]
            self.caras['B'][2][i] = self.caras['L'][2][i]
            self.caras['L'][2][i] = temp[i] # Ajusta la fila inferior de las caras adyacentes después de mover la cara D
    
    def mover_D2(self):
        self.mover_D()
        self.mover_D()
    
    def mover_D_(self):
        for _ in range(3):
            self.mover_D()
    
    def mover_L(self): # Mueve la cara L (Izquierda) en sentido horario y ajusta las piezas adyacentes
        self.rotacion_horaria('L')
        temp = [self.caras['F'][i][0] for i in range(3)]
        for i in range(3):
            self.caras['F'][i][0] = self.caras['D'][i][0]
            self.caras['D'][i][0] = self.caras['B'][2-i][2]
            self.caras['B'][2-i][2] = self.caras['U'][i][0]
            self.caras['U'][i][0] = temp[i] # Ajusta la columna izquierda de las caras adyacentes después de mover la cara L
    
    def mover_L2(self): # Mueve la cara L dos veces (180°)
        self.mover_L()
        self.mover_L()
    
    def mover_L_(self): # Mueve la cara L en sentido antihorario (270° horario)
        for _ in range(3):
            self.mover_L()
    
    def mover_R(self): # Mueve la cara R (Derecha) en sentido horario y ajusta las piezas adyacentes
        self.rotacion_horaria('R')
        temp = [self.caras['F'][i][2] for i in range(3)]
        for i in range(3):
            self.caras['F'][i][2] = self.caras['U'][i][2] # Ajusta la columna derecha de las caras adyacentes después de mover la cara R
            self.caras['U'][i][2] = self.caras['B'][2-i][0]
            self.caras['B'][2-i][0] = self.caras['D'][i][2]
            self.caras['D'][i][2] = temp[i]
    
    def mover_R2(self): # Mueve la cara R dos veces (180°)
        self.mover_R()
        self.mover_R()
    
    def mover_R_(self): # Mueve la cara R en sentido antihorario (270° horario)
        for _ in range(3):
            self.mover_R()
    
    def mover_F(self): # Mueve la cara F (Frente) en sentido horario y ajusta las piezas adyacentes
        self.rotacion_horaria('F')
        temp = [self.caras['U'][2][i] for i in range(3)]
        for i in range(3):
            self.caras['U'][2][i] = self.caras['L'][2-i][2]
            self.caras['L'][2-i][2] = self.caras['D'][0][2-i]
            self.caras['D'][0][2-i] = self.caras['R'][i][0]
            self.caras['R'][i][0] = temp[i] # Ajusta la fila inferior de la cara U, la columna derecha de la cara L, la fila superior de la cara D y la columna izquierda de la cara R después de mover la cara F
    
    def mover_F2(self): # Mueve la cara F dos veces (180°)
        self.mover_F()
        self.mover_F()
    
    def mover_F_(self): # Mueve la cara F en sentido antihorario (270° horario)
        for _ in range(3):
            self.mover_F()
    
    def mover_B(self): # Mueve la cara B (Atrás) en sentido horario y ajusta las piezas adyacentes
        self.rotacion_horaria('B')
        temp = [self.caras['U'][0][i] for i in range(3)]
        for i in range(3):
            self.caras['U'][0][i] = self.caras['R'][i][2]
            self.caras['R'][i][2] = self.caras['D'][2][2-i]
            self.caras['D'][2][2-i] = self.caras['L'][2-i][0] 
            self.caras['L'][2-i][0] = temp[i] # Ajusta la fila superior de la cara U, la columna derecha de la cara R, la fila inferior de la cara D y la columna izquierda de la cara L después de mover la cara B
    
    def mover_B2(self): # Mueve la cara B dos veces (180°)
        self.mover_B()
        self.mover_B()
    
    def mover_B_(self): # Mueve la cara B en sentido antihorario (270° horario)
        for _ in range(3):
            self.mover_B()
    
    def aplicar_movimiento(self, movimiento): # Aplica un movimiento específico al cubo
        movimientos = {
            'U': self.mover_U,     'U2': self.mover_U2,     "U'": self.mover_U_, # Mueve la cara U en sentido horario, dos veces o en sentido antihorario
            'D': self.mover_D,     'D2': self.mover_D2,     "D'": self.mover_D_, # Mueve la cara D en sentido horario, dos veces o en sentido antihorario
            'L': self.mover_L,     'L2': self.mover_L2,     "L'": self.mover_L_, # Mueve la cara L en sentido horario, dos veces o en sentido antihorario
            'R': self.mover_R,     'R2': self.mover_R2,     "R'": self.mover_R_, # Mueve la cara R en sentido horario, dos veces o en sentido antihorario
            'F': self.mover_F,     'F2': self.mover_F2,     "F'": self.mover_F_, # Mueve la cara F en sentido horario, dos veces o en sentido antihorario
            'B': self.mover_B,     'B2': self.mover_B2,     "B'": self.mover_B_, # Mueve la cara B en sentido horario, dos veces o en sentido antihorario
        }
        if movimiento in movimientos:
            movimientos[movimiento]()  
    def es_resuelto(self): # Verifica si el cubo está resuelto comparando cada cara con su color de referencia
        for cara in self.caras.values():# Recorre cada cara del cubo
            color_ref = cara[0][0]
            for fila in cara:
                for celda in fila:
                    if celda != color_ref:
                        return False
        return True # Si todas las caras tienen el mismo color, el cubo está resuelto
    
    def copiar(self): # Crea una copia profunda del cubo para evitar referencias compartidas entre instancias
        nuevo = CuboRubikHibrido()
        nuevo.caras = deepcopy(self.caras)
        return nuevo
    
    def __str__(self): # Devuelve una representación en cadena del cubo para impresión en consola
        plantilla = self.obtener_plantilla_2d() # Obtiene la plantilla 2D actualizada con el estado del cubo
        resultado = "\n"
        for fila in plantilla:
            resultado += " ".join(fila) + "\n" 
        return resultado 
def dibujar_cubo_matplotlib(cubo, titulo="Cubo"): # Dibuja el cubo usando Matplotlib a partir de su plantilla 2D
    plantilla = cubo.obtener_plantilla_2d() # Obtiene la plantilla 2D del cubo para visualización
    fig, ax = plt.subplots(figsize=(10, 8)) # Crea una figura y un eje para dibujar el cubo
    filas = len(plantilla) # Obtiene el número de filas y columnas de la plantilla para iterar sobre ella
    columnas = len(plantilla[0]) # Itera sobre cada celda de la plantilla para dibujar un rectángulo con el color correspondiente al valor de la celda
    
    for r in range(filas): # Recorre cada fila de la plantilla
        for c in range(columnas):
            valor = plantilla[r][c]
            color = COLOR_MAP.get(valor)
            
            if color: # Si el valor de la celda corresponde a un color válido, dibuja un rectángulo en la posición correspondiente con el color asignado
                rect = patches.Rectangle(
                    (c, filas - r - 1),
                    1, 1,
                    linewidth=2,
                    edgecolor='black',
                    facecolor=color
                )
                ax.add_patch(rect)
    
    ax.set_xlim(0, columnas) # Ajusta los límites del eje para que se ajusten al tamaño de la plantilla
    ax.set_ylim(0, filas) # Ajusta los límites del eje para que se ajusten al tamaño de la plantilla
    ax.set_aspect('equal')
    ax.axis('off')
    plt.title(titulo, fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.show()
class ResolvadorBFSHibrido: # Clase que implementa un algoritmo de búsqueda BFS para resolver el cubo Rubik utilizando la representación híbrida del cubo
    
    MOVIMIENTOS = ['U', 'U2', "U'", 'D', 'D2', "D'",  # Lista de movimientos posibles para el cubo, incluyendo movimientos simples, dobles y en sentido antihorario para cada cara
                   'L', 'L2', "L'", 'R', 'R2', "R'",
                   'F', 'F2', "F'", 'B', 'B2', "B'"]
    
    def __init__(self, cubo_inicial): # Inicializa el resolvador con un cubo inicial y prepara las variables para almacenar la solución y contar los nodos visitados
        self.cubo_inicial = cubo_inicial.copiar()
        self.solucion = []
        self.nodos_visitados = 0
    
    def resolver(self, profundidad_maxima=5, verbose=True): # Resuelve el cubo utilizando BFS con una profundidad máxima para limitar la búsqueda y una opción de verbose para mostrar información durante el proceso
        if self.cubo_inicial.es_resuelto():
            if verbose: # Si el cubo ya está resuelto, muestra un mensaje indicando que no se necesitan movimientos y retorna True
                print("El cubo ya está resuelto. No se necesitan movimientos.")
            return True
        
        if verbose:# Si verbose es True, muestra un mensaje indicando que se está iniciando la búsqueda BFS con la profundidad máxima especificada
            print(f" Iniciando búsqueda BFS (máx {profundidad_maxima} movimientos)") 
        
        cola = deque([(self.cubo_inicial.copiar(), [])]) # Cola para BFS que almacena tuplas de (cubo_actual, movimientos_realizados)
        visitados = {self.cubo_inicial.obtener_estado()}
        self.nodos_visitados = 1
        
        while cola: # Mientras la cola no esté vacía, continúa explorando los nodos
            cubo_actual, movimientos = cola.popleft()
            
            if cubo_actual.es_resuelto(): # Si el cubo actual está resuelto, almacena la solución (movimientos realizados) y muestra un mensaje indicando que se encontró la solución junto con el número de movimientos y nodos visitados, luego retorna True
                self.solucion = movimientos
                if verbose: #|
                    print(f" Solución encontrada en {len(movimientos)} movimientos")
                    print(f" Nodos visitados: {self.nodos_visitados}")
                return True
            
            if len(movimientos) < profundidad_maxima: # Si la cantidad de movimientos realizados es menor que la profundidad máxima, continúa generando nuevos estados aplicando cada movimiento posible al cubo actual
                for movimiento in self.MOVIMIENTOS:
                    nuevo_cubo = cubo_actual.copiar()
                    nuevo_cubo.aplicar_movimiento(movimiento)
                    
                    estado = nuevo_cubo.obtener_estado() # Obtiene el estado del nuevo cubo después de aplicar el movimiento
                    if estado not in visitados:
                        visitados.add(estado)
                        cola.append((nuevo_cubo, movimientos + [movimiento]))
                        self.nodos_visitados += 1
        
        if verbose:
            print("No se encontró solución") # Si se agota la cola sin encontrar una solución, muestra un mensaje indicando que no se encontró solución y retorna False
        return False
    
    def animar_solucion(self): # Anima la solución paso a paso utilizando Matplotlib mostrando cada estado del cubo después de aplicar cada movimiento de la solución
        estados = [self.cubo_inicial.copiar()]
        cubo_actual = self.cubo_inicial.copiar()
        
        for mov in self.solucion: # Aplica cada movimiento de la solución al cubo actual y almacena el estado resultante en la lista de estados para animación
            cubo_actual.aplicar_movimiento(mov)
            estados.append(cubo_actual.copiar())
        
        for i, estado in enumerate(estados): # Itera sobre cada estado almacenado y dibuja el cubo utilizando Matplotlib con un título que indica el paso actual y el movimiento aplicado (si no es el estado inicial) para mostrar la animación de la solución paso a paso
            if i == 0:
                titulo = "Estado Inicial"
            else:
                titulo = f"Paso {i}: Movimiento {self.solucion[i-1]}" # Título que indica el paso actual y el movimiento aplicado
            dibujar_cubo_matplotlib(estado, titulo)
def ingresar_cubo(): # Función para ingresar un cubo personalizado desde la consola, solicitando al usuario que ingrese los colores de cada cara del cubo y almacenándolos en una instancia de CuboRubikHibrido
    print("\n" + "="*60)
    print("INGRESE EL CUBO DESARMADO")
    print("="*60)
    print("\nColores disponibles:")
    print("  W/B = Blanco (Arriba)")
    print("  Y = Amarillo (Abajo)")
    print("  G = Verde (Frente)")
    print("  R = Rojo (Derecha)")
    print("  O = Naranja (Izquierda)")
    print("  P/B = Azul (Atrás)")
    
    cubo = CuboRubikHibrido() # Crea una nueva instancia de CuboRubikHibrido para almacenar el cubo personalizado ingresado por el usuario
    
    caras = [
        ('U', 'Blanca (Arriba)'),
        ('D', 'Amarilla (Abajo)'),
        ('L', 'Naranja (Izquierda)'),
        ('R', 'Roja (Derecha)'),
        ('F', 'Verde (Frente)'),
        ('B', 'Azul (Atrás)')
    ]
    
    for key, nombre in caras: # Itera sobre cada cara del cubo, solicitando al usuario que ingrese los colores de cada fila de la cara correspondiente y almacenándolos en la estructura de datos del cubo
        print(f"\n Cara {nombre}") # Solicita al usuario que ingrese los colores de cada fila de la cara actual, asegurándose de que se ingresen exactamente 3 colores para cada fila y almacenándolos en la estructura de datos del cubo
        for i in range(3):
            fila = input(f"Fila {i+1} (3 colores): ").split() # Solicita al usuario que ingrese los colores de la fila actual, separándolos por espacios y almacenándolos en una lista
            if len(fila) == 3:
                cubo.caras[key][i] = fila
            else:
                print(" Debes ingresar exactamente 3 colores")
                i -= 1
    
    return cubo # Devuelve la instancia de CuboRubikHibrido con el cubo personalizado ingresado por el usuario
def main(): # Función principal que muestra un menú para que el usuario pueda elegir entre ingresar un cubo personalizado, usar un cubo con demostración o salir del programa, y luego procede a mostrar el estado inicial del cubo, resolverlo utilizando el resolvador BFS híbrido y mostrar la solución junto con la opción de animar la solución paso a paso utilizando Matplotlib
    print("\n" + "╔" + "="*58 + "╗")
    print("║" + " "*10 + "RESOLVEDOR DE CUBO RUBIK HÍBRIDO " + " "*12 + "   ║") 
    print("║" + " "*8 + "Combina potencia de BFS + visualización Matplotlib" + " "*0 + "║")
    print("╚" + "="*58 + "╝")
    
    print("\n¿Qué deseas hacer?") # Muestra un menú para que el usuario pueda elegir entre ingresar un cubo personalizado, usar un cubo con demostración o salir del programa
    print("1. Ingresar un cubo personalizado")
    print("2. Usar cubo con demostración")
    print("3. Salir")
    
    opcion = input("\nSelecciona (1-3): ").strip() # Solicita al usuario que seleccione una opción del menú y la almacena en la variable 'opcion' para determinar qué acción realizar a continuación (ingresar un cubo personalizado, usar un cubo con demostración o salir del programa) y luego procede a mostrar el estado inicial del cubo, resolverlo utilizando el resolvador BFS híbrido y mostrar la solución junto con la opción de animar la solución paso a paso utilizando Matplotlib
    
    if opcion == '1': # Si el usuario selecciona la opción 1, llama a la función ingresar_cubo() para permitir al usuario ingresar un cubo personalizado desde la consola y almacena el cubo ingresado en la variable 'cubo' para su posterior resolución y visualización
        cubo = ingresar_cubo()
    elif opcion == '2':
        cubo = CuboRubikHibrido()
        cubo.mover_R()
        cubo.mover_U()
        cubo.mover_R_()
        cubo.mover_U_()
        print(" Cubo desordenado con movimientos")
    else:
        print("Hasta luego")
        return
    print("\n Estado inicial:")
    print(cubo)
    dibujar_cubo_matplotlib(cubo, "Estado Inicial") # Dibuja el estado inicial del cubo utilizando Matplotlib para que el usuario pueda visualizarlo antes de resolverlo
    resolvador = ResolvadorBFSHibrido(cubo) # Crea una instancia del resolvador BFS híbrido con el cubo inicial para proceder a resolverlo utilizando el algoritmo de búsqueda BFS y luego mostrar la solución junto con la opción de animar la solución paso a paso utilizando Matplotlib
    if resolvador.resolver(profundidad_maxima=5): # Si el resolvador encuentra una solución dentro de la profundidad máxima especificada, muestra la solución (secuencia de movimientos) y luego pregunta al usuario si desea ver la animación de la solución paso a paso utilizando Matplotlib, mostrando cada estado del cubo después de aplicar cada movimiento de la solución para visualizar el proceso de resolución del cubo
        print(f"\n Solución: {' -> '.join(resolvador.solucion)}")
        
        ver_animacion = input("\n¿Ver animación de la solución? (s/n): ").strip().lower() # Pregunta al usuario si desea ver la animación de la solución paso a paso utilizando Matplotlib, y si el usuario responde afirmativamente, llama al método animar_solucion() del resolvador para mostrar cada estado del cubo después de aplicar cada movimiento de la solución para visualizar el proceso de resolución del cubo
        if ver_animacion == 's': # Si el usuario desea ver la animación de la solución, llama al método animar_solucion() del resolvador para mostrar cada estado del cubo después de aplicar cada movimiento de la solución para visualizar el proceso de resolución del cubo
            resolvador.animar_solucion()
            
            cubo_final = cubo.copiar() # Crea una copia del cubo inicial para aplicar la solución paso a paso y mostrar el estado final del cubo después de aplicar todos los movimientos de la solución para confirmar que el cubo se resuelve correctamente
            for mov in resolvador.solucion: # Aplica cada movimiento de la solución al cubo final para mostrar el estado final del cubo después de aplicar todos los movimientos de la solución para confirmar que el cubo se resuelve correctamente
                cubo_final.aplicar_movimiento(mov)
            
            print("\n ¡Cubo resuelto!") # Muestra un mensaje indicando que el cubo se ha resuelto correctamente después de aplicar todos los movimientos de la solución al cubo final para confirmar que el cubo se resuelve correctamente
            print(f" Total de movimientos: {len(resolvador.solucion)}")
            print(f" Nodos visitados: {resolvador.nodos_visitados}") # Muestra el total de movimientos de la solución y el número de nodos visitados durante la búsqueda BFS para resolver el cubo
    
    continuar = input("\n¿Deseas resolver otro cubo? (s/n): ").strip().lower() # Pregunta al usuario si desea resolver otro cubo después de completar la resolución del cubo actual, y si el usuario responde afirmativamente, llama a la función main() para reiniciar el proceso y permitir al usuario ingresar un nuevo cubo o usar un cubo con demostración para resolverlo utilizando el resolvador BFS híbrido y mostrar la solución junto con la opción de animar la solución paso a paso utilizando Matplotlib
    if continuar == 's':
        main() # Si el usuario desea resolver otro cubo, llama a la función main() para reiniciar el proceso y permitir al usuario ingresar un nuevo cubo o usar un cubo con demostración para resolverlo utilizando el resolvador BFS híbrido y mostrar la solución junto con la opción de animar la solución paso a paso utilizando Matplotlib

if __name__ == "__main__": # Punto de entrada del programa, llama a la función main() para iniciar el proceso de resolución del cubo Rubik utilizando el resolvador BFS híbrido y mostrar la solución junto con la opción de animar la solución paso a paso utilizando Matplotlib
    main()