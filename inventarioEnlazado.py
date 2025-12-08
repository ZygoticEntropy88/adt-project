"""
====================================== PROYECTO TDA ===============================
TECNOLOGÍA DE LA PROGRAMACIÓN UNIVERSIDAD DE MURCIA

2º DTIE MATEMÁTICAS Y FÍSICA CURSO 2025/6
"""
import csv

class InventarioError(Exception):
    def __init__(self, mensaje: str):
        super().__init__(mensaje)


class Inventario:

    class Nodo:
        # CORRECCIÓN SINTAXIS: El valor por defecto va después del tipo (siguiente: Tipo = None)
        def __init__(self, nombre: str, valor: float, siguiente: 'Inventario.Nodo' = None):
            self._nombre: str = nombre
            self._valor: float = valor
            self._siguiente: 'Inventario.Nodo' = siguiente

        def __str__(self) -> str:
            return f"[{self.get_nombre()} : {self.get_valor()}]"

        # CORRECCIÓN LÓGICA: Se necesitan todos los operadores de comparación para ordenar
        def __gt__(self, otro: 'Inventario.Nodo') -> bool:
            return self.get_valor() > otro.get_valor()

        def __lt__(self, otro: 'Inventario.Nodo') -> bool:
            return self.get_valor() < otro.get_valor()

        def __le__(self, otro: 'Inventario.Nodo') -> bool:
            return self.get_valor() <= otro.get_valor()
            
        def __ge__(self, otro: 'Inventario.Nodo') -> bool:
            return self.get_valor() >= otro.get_valor()

        def get_nombre(self) -> str:
            return self._nombre

        def get_valor(self) -> float:
            return self._valor

        def get_siguiente(self) -> 'Inventario.Nodo':
            return self._siguiente

        def set_valor(self, nuevo_valor: float):
            self._valor = nuevo_valor

        def set_siguiente(self, siguiente: 'Inventario.Nodo'):
            self._siguiente = siguiente


    # ========================= CONSTRUCTOR =============================

    def __init__(self):
        """Constructor: Crea un nuevo inventario, inicialmente vacío."""
        self._primer_nodo: 'Inventario.Nodo' = None
        self._longitud: int = 0


    # ========================= MÉTODOS MÁGICOS =============================

    def __len__(self) -> int:
        return self.total_items()

    def __iter__(self):
        actual: 'Inventario.Nodo' = self._primer_nodo
        while actual is not None:
            yield actual.get_nombre()
            actual = actual.get_siguiente()

    def __str__(self) -> str:
        msg: str = "################# INVENTARIO #################\n"
        
        pos = 0
        actual = self._primer_nodo
        while actual is not None:
            msg += f"\t{pos} - {actual}\n"
            actual = actual.get_siguiente()
            pos += 1
            
        return msg
        

    # ========================= GETTERS Y SETTERS INTERNOS =============================

    def _get_primer_nodo(self) -> 'Inventario.Nodo':
        return self._primer_nodo

    def _set_primer_nodo(self, nodo: 'Inventario.Nodo'):
        self._primer_nodo = nodo

    def _get_longitud(self) -> int:
        return self._longitud

    def _set_longitud(self, longitud: int):
        self._longitud = longitud

    def _buscar_nodo(self, nombre: str) -> 'Inventario.Nodo':
        """Dado el nombre de un nodo, lo busca y devuelve el nodo nombre:valor"""
        actual = self._primer_nodo
        while actual is not None:
            if actual.get_nombre() == nombre:
                return actual
            actual = actual.get_siguiente()
        return None

    def _get_nodo_previo(self, nodo: 'Inventario.Nodo') -> 'Inventario.Nodo':
        """
        Busca y devuelve el nodo anterior al nodo proporcionado.
        Si el nodo proporcionado es el primero o None, devuelve None.
        """
        if nodo is None or nodo is self._primer_nodo:
            return None

        nodo_anterior: 'Inventario.Nodo' = self._primer_nodo
        
        while nodo_anterior is not None and nodo_anterior.get_siguiente() is not nodo:
            nodo_anterior = nodo_anterior.get_siguiente()
            
        return nodo_anterior


    # ========================= MÉTODOS MODIFICADORES =============================

    def agregar(self, nombre: str, valor: float = 1.0) -> None:
        """
        Modifica el inventario añadiendo el elemento nombre con el valor indicado.
        Si ya existe, su valor se incrementa.
        """
        if valor <= 0:
            raise InventarioError("No se puede agregar un valor menor o igual a 0.")
        
        nodo = self._buscar_nodo(nombre)
        if nodo is not None:
            nodo.set_valor(nodo.get_valor() + valor)
        else:
            # Inserta al principio de la lista
            nuevo_nodo = Inventario.Nodo(nombre, valor, self._primer_nodo)
            self._set_primer_nodo(nuevo_nodo)
            self._longitud += 1


    def actualizar(self, nombre: str, nuevo_valor: float) -> None:
        """
        Sustituye el valor actual del elemento nombre por nuevo_valor.
        """
        if nuevo_valor <= 0:
            raise InventarioError("El nuevo valor debe ser mayor que 0.")
        
        nodo = self._buscar_nodo(nombre)
        if nodo is None:
            raise InventarioError(f"El elemento '{nombre}' no existe para actualizar.")
        
        nodo.set_valor(nuevo_valor)

    def eliminar(self, nombre: str, cantidad: float = 1.0) -> None:
        """
        Resta la cantidad indicada al elemento nombre. Si el valor resultante es <= 0, elimina el elemento.
        """
        if cantidad <= 0:
             raise InventarioError("La cantidad a eliminar debe ser mayor que 0.")

        nodo_actual: 'Inventario.Nodo' = self._buscar_nodo(nombre)
        
        if nodo_actual is None:
            raise InventarioError(f"El elemento '{nombre}' no existe para eliminar.")
        
        nuevo_valor = nodo_actual.get_valor() - cantidad
    
        if nuevo_valor > 0:
            nodo_actual.set_valor(nuevo_valor)
        else:
            nodo_anterior: 'Inventario.Nodo' = self._get_nodo_previo(nodo_actual)
            
            if nodo_actual is self._primer_nodo:
                self._set_primer_nodo(nodo_actual.get_siguiente())         
            elif nodo_anterior is not None:
                nodo_anterior.set_siguiente(nodo_actual.get_siguiente())
            
            self._set_longitud(self._get_longitud() - 1)

    def vaciar(self) -> None:
        """Elimina todos los elementos del inventario."""
        self._primer_nodo = None
        self._longitud = 0

    def fusionar(self, otro: 'Inventario') -> None:
        """
        Modifica el inventario actual añadiendo los elementos del inventario 'otro'.
        """
        if not isinstance(otro, Inventario):
            raise InventarioError("El objeto a fusionar debe ser de tipo Inventario.")
            
        for nombre in otro:
            valor_otro: float = otro.consultar(nombre)
            self.agregar(nombre, valor_otro)

    def diferencia(self, otro: 'Inventario') -> None:
        """
        Resta al inventario actual los valores de los elementos contenidos en 'otro'.
        """
        if not isinstance(otro, Inventario):
            raise InventarioError("El objeto para la diferencia debe ser de tipo Inventario.")
        
        for nombre in list(otro): # Usamos list() para iterar sobre una copia de las claves
            valor_otro: float = otro.consultar(nombre)
            try:
                self.eliminar(nombre, valor_otro)
            except InventarioError as e:
                if "no existe" not in str(e):
                    raise e
                pass


    # ========================= MÉTODOS DE PERSISTENCIA =============================

    def cargar(self, ruta: str) -> None:
        """
        Carga los elementos desde un archivo CSV y los fusiona con el inventario actual.
        """
        inventario_leido: 'Inventario' = Inventario()

        try:
            with open(ruta, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if not row: continue # Saltar líneas vacías
                    if len(row) != 2:
                        continue # Saltar líneas mal formadas o headers si los hubiera
                    
                    nombre: str = row[0]
                    valor_str: str = row[1]
                    
                    try:
                        valor = float(valor_str)
                        if valor > 0:
                            inventario_leido.agregar(nombre, valor)
                    except ValueError:
                        # Ignorar valores no numéricos
                        continue
        
        except FileNotFoundError:
            raise InventarioError(f"El archivo CSV no existe en la ruta: {ruta}")
        except Exception as e:
            raise InventarioError(f"Error al cargar el archivo CSV en {ruta}: {e}")

        self.fusionar(inventario_leido)

    def guardar(self, ruta: str) -> None:
        """
        Guarda el inventario en un archivo CSV fusionando con el contenido existente.
        """
        inventario_a_guardar = self.copiar()

        try:
            inventario_a_guardar.cargar(ruta)
        except InventarioError as e:
            if "no existe" in str(e).lower():
                pass
            else:
                raise InventarioError(f"Error al intentar cargar datos existentes: {e}")
        
        try:
            with open(ruta, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                for nombre in inventario_a_guardar:
                    valor = inventario_a_guardar.consultar(nombre)
                    if valor > 0:
                        writer.writerow([nombre, valor])

        except Exception as e:
            raise InventarioError(f"Error al escribir en el archivo CSV en {ruta}: {e}")


    # ========================= MÉTODOS DE CONSULTA =============================
    
    def consultar(self, nombre: str) -> float:
        """Devuelve el valor actual del elemento nombre o 0.0 si no existe."""
        nodo: 'Inventario.Nodo' = self._buscar_nodo(nombre)
        if nodo is not None:
            return nodo.get_valor()
        return 0.0

    def existe(self, nombre: str) -> bool:
        """Indica si el elemento nombre está presente en el inventario."""
        nodo: 'Inventario.Nodo' = self._buscar_nodo(nombre)
        return nodo is not None

    def total_items(self) -> int:
        """Retorna el número total de elementos distintos en el inventario."""
        return self._get_longitud()

    def cantidad_total(self) -> float:
        """Retorna la suma de los valores de todos los elementos del inventario."""
        total_inventario: float = 0.0
        actual: 'Inventario.Nodo' = self._primer_nodo
        while actual is not None:
            total_inventario += actual.get_valor()
            actual = actual.get_siguiente()
        return total_inventario


    def _invertir(self) -> None:
        """Invierte el orden de la lista enlazada."""
        nodo_anterior: 'Inventario.Nodo' = None
        nodo_actual: 'Inventario.Nodo' = self._primer_nodo
        while nodo_actual is not None:
            nodo_siguiente: 'Inventario.Nodo' = nodo_actual.get_siguiente()
            nodo_actual.set_siguiente(nodo_anterior)
            nodo_anterior = nodo_actual
            nodo_actual = nodo_siguiente
        
        self._set_primer_nodo(nodo_anterior)


    def ordenar_por_valor(self, descendente=False):
        """
        Ordena la lista enlazada por el valor del elemento (Insertion Sort).
        """
        if self._get_longitud() <= 1:
            return

        lista_ordenada: 'Inventario.Nodo' = None
        nodo_actual = self._primer_nodo

        while nodo_actual is not None:
            nodo_siguiente = nodo_actual.get_siguiente()
            
            # Caso 1: Insertar en la lista ordenada vacía o al inicio
            # Nota: Requiere que Nodo implemente __le__ (<=)
            if lista_ordenada is None or nodo_actual <= lista_ordenada:
                nodo_actual.set_siguiente(lista_ordenada)
                lista_ordenada = nodo_actual
            else:
                # Caso 2: Buscar dónde insertar en la lista ordenada
                nodo_temp = lista_ordenada
                # Nota: Requiere que Nodo implemente __lt__ (<)
                while nodo_temp.get_siguiente() is not None and nodo_temp.get_siguiente() < nodo_actual:
                    nodo_temp = nodo_temp.get_siguiente()
                
                nodo_actual.set_siguiente(nodo_temp.get_siguiente())
                nodo_temp.set_siguiente(nodo_actual)
            
            nodo_actual = nodo_siguiente

        self._set_primer_nodo(lista_ordenada)
            
        if descendente:
            self._invertir()


    def maximo(self) -> str:
        """
        Devuelve el elemento con el valor más alto.
        """
        if self._primer_nodo is None:
            raise InventarioError("El inventario está vacío.")
        
        max_nombre: str = self._primer_nodo.get_nombre()
        max_valor: float = self._primer_nodo.get_valor()
        
        actual: 'Inventario.Nodo' = self._primer_nodo.get_siguiente()
        while actual is not None:
            if actual.get_valor() > max_valor:
                max_valor = actual.get_valor()
                max_nombre = actual.get_nombre()
            actual = actual.get_siguiente()
    
        return max_nombre

    def minimo(self) -> str:
        """
        Devuelve el elemento con el valor más bajo.
        """
        if self._primer_nodo is None:
            raise InventarioError("El inventario está vacío.")
        
        min_nombre: str = self._primer_nodo.get_nombre()
        min_valor: float = self._primer_nodo.get_valor()
        
        actual: 'Inventario.Nodo' = self._primer_nodo.get_siguiente()
        while actual is not None:
            if actual.get_valor() < min_valor:
                min_valor = actual.get_valor()
                min_nombre = actual.get_nombre()
            actual = actual.get_siguiente()
    
        return min_nombre


    def copiar(self) -> 'Inventario':
        """
        Crea y retorna un nuevo inventario mediante copia profunda.
        """
        nuevo_inventario = Inventario()
        actual = self._primer_nodo
        
        while actual is not None:
            # Al usar 'agregar', se inserta al principio (invirtiendo el orden)
            nuevo_inventario.agregar(actual.get_nombre(), actual.get_valor())
            actual = actual.get_siguiente()
        
        # Invertimos el nuevo inventario para restaurar el orden original
        nuevo_inventario._invertir()
        
        return nuevo_inventario