"""
====================================== PROYECTO TDA ===============================
TECNOLOGÍA DE LA PROGRAMACIÓN UNIVERSIDAD DE MURCIA

2º DTIE MATEMÁTICAS Y FÍSICA CURSO 2025/6
"""
import csv


class InventarioError(Exception):
    def __init__(self, mensaje:str):
        super().__init__(mensaje)





class Inventario:


    class Nodo:
        def __init__(self, nombre: str, valor: float, siguiente=None:'Nodo'):
            self._nombre:str = nombre
            self._valor:float = valor
            self._siguiente:'Nodo' = siguiente

        def __str__(self) -> 'str':
            return f"[{self.get_nombre()} : {self.get_valor()}]"

        def get_nombre(self) -> 'str': 
            return self._nombre

        def get_valor(self) -> float:
            return self._valor

        def get_siguiente(self) -> 'Nodo':
            return self._siguiente

        def set_valor(self, nuevo_valor: float):
            self._valor = nuevo_valor

        def set_siguiente(self, siguiente:'Nodo'):
            self._siguiente = siguiente






    # ========================= CONSTRUCTOR =============================

    def __init__(self):
        """Constructor: Crea un nuevo inventario, inicialmente vacío."""
        self._primer_nodo = None 
        self._longitud = 0    






    # ========================= MÉTODOS MÁGICOS =============================

    def __len__(self) -> int:
        return self.total_items()

    def __iter__(self):
        # TODO
        self._iter_actual = self.get_primer_nodo()
        return self

    def __str__(self) -> str:
        msg:str = "################# INVENTARIO #################\n"
        
        pos = 0
        actual = self.get_primer_nodo()
        while actual is not None:
            msg += f"\t{pos} - {actual}\n"
            actual = actual.get_siguiente()
            pos += 1
            
        return msg
        





    # ========================= GETTERS Y SETTERS =============================

    def _get_primer_nodo(self) -> 'Nodo':
        return self._primer_nodo

    def _set_primer_nodo(self, nodo:'Nodo'):
        self._primer_nodo = nodo

    def _get_longitud(self) -> int:
        return self._longitud

    def _set_longitud(self, longitud:int):
        self._longitud = longitud

    def _buscar_nodo(self, nombre: str):
        """Dado el nombre de un nodo, lo busca y devuelve el nodo nombre:valor"""
        actual = self.get_primer_nodo()
        while actual is not None:
            if actual.get_nombre() == nombre:
                return actual
            actual = actual.get_siguiente()
        return actual







    # ========================= MÉTODOS MODIFICADORES =============================

    def agregar(self, nombre: str, valor: float = 1.0) -> None:
        """
        Modifica el inventario añadiendo el elemento nombre con el valor indicado.
        Si ya existe, su valor se incrementa.
        Excepciones: InventarioError si valor <= 0.
        """
        if valor <= 0:
            raise InventarioError("No se puede agregar un valor menor o igual a 0.")
        
        nodo = self._buscar_nodo(nombre)
        if nodo is not None:
            # El nodo ya existe, incremento el valor
            nodo.set_valor(nodo.get_valor() + valor)
        else:
            # El elemento no existe, añado un nuevo nodo al inicio
            nuevo_nodo = Nodo(nombre, valor, self.get_primer_nodo())
            self._set_primer_nodo(nuevo_nodo) 
            self.longitud += 1      

    def actualizar(self, nombre: str, nuevo_valor: float) -> None:
        """
        Sustituye el valor actual del elemento nombre por nuevo_valor.
        Excepciones: InventarioError si nombre no existe o nuevo_valor <= 0.
        """
        if nuevo_valor <= 0:
            raise InventarioError("No se puede agregar un valor menor o igual a 0.")
        
        nodo = self._buscar_nodo(nombre)
        if nodo is None:
            raise InventarioError(f"El elemento '{nombre}' no existe para actualizar.")
        
        nodo.set_valor(nuevo_valor)

    def eliminar(self, nombre: str, cantidad: float = 1.0) -> None:
        """
        Resta la cantidad indicada al elemento nombre. Si el valor resultante es <= 0, elimina el elemento.
        Excepciones: InventarioError si el elemento no existe.
        """
        nodo:'Nodo' = self._buscar_nodo(nombre) 
        
        if nodo_actual is None:
            raise InventarioError(f"El elemento '{nombre}' no existe para eliminar.")
        nuevo_valor = nodo.get_valor() - cantidad
    
        if nuevo_valor > 0:
            nodo.set_valor(nuevo_valor)
        else:
            if nodo is self.get_primer_nodo():
                self._set_primer_nodo(nodo.get_siguiente())         
            else:
                # Debo eliminar el nodo, y este no es el primero de la estructura
                nodo_anterior = self.get_primer_nodo()
                while nodo_anterior.get_siguiente() is nodo and nodo_anterior.get_siguiente() is not None:
                    nodo_anterior = nodo_anterior.siguiente()
                if nodo_anterior.get_siguiente() is nodo:
                    nodo_anterior.set_siguiente(nodo.get_siguiente())
            self.set_longitud(self.get_longitud()-1)

    def vaciar(self) -> None:
        """Elimina todos los elementos del inventario."""
        self._primer_nodo = None
        self.longitud = 0

    def fusionar(self, otro:'Inventario') -> None:
        """
        Modifica el inventario actual añadiendo los elementos del inventario 'otro'.
        Si hay elementos comunes, sus valores se suman.
        Excepciones: InventarioError si 'otro' no es de tipo Inventario
        """
        if not isinstance(otro, Inventario):
            raise InventarioError("El objeto a fusionar debe ser de tipo Inventario.")
            
        for nombre in otro:
            valor_otro:float = otro.consultar(nombre)
            self.agregar(nombre, valor_otro) # Inventario.agregar() ya maneja que esté repetido

    def diferencia(self, otro:'Inventario') -> None:
        """
        Resta al inventario actual los valores de los elementos contenidos en 'otro'.
        Si algún valor llega a 0 o menor, se elimina del inventario.
        Excepciones: InventarioError si 'otro' no es un objeto Inventario. [cite: 90, 91, 92, 93]
        """
        if not isinstance(otro, Inventario):
            raise InventarioError("El objeto para la diferencia debe ser de tipo Inventario.")
        
        for nombre in otro:
            valor_otro:float = otro.consultar(nombre)
            try:
                self.eliminar(nombre, valor_otro)
            except InventarioError:
                # Si el elemento nombre no existe en este inventario, eliminar() lanza InventarioError. Para esta implementación lo voy a obviar.
                pass
            






    # ========================= MÉTODOS DE PERSISTENCIA =============================
    def guardar(self, ruta: str) -> None:
        # TODO 
        pass



    def cargar(self, ruta: str) -> None:
        """
        Carga los elementos desde un archivo CSV y los fusiona con el inventario actual.
        Si hay elementos comunes, sus valores se suman a los ya existentes en el inventario actual.
        Excepciones: InventarioError si el archivo no existe o tiene formato incorrecto.
        """
        inventario_leido:'Inventario' = Inventario()

        try:
            with open(ruta, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) != 2:
                        raise InventarioError(f"La línea {row} de {ruta} no se puede cargar en el inventario.")
                    
                    nombre:str, valor_str:str = row
                    
                    try:
                        valor = float(valor_str)
                        if valor <= 0:
                             # Los valores en un inventario deben ser positivos. Lo ignoro si son <= 0.
                             pass 
                        else:
                            inventario_leido.agregar(nombre, valor)
                    except ValueError:
                        raise InventarioError(f"Valor no numérico en el archivo CSV: '{valor_str}'")
        
        except FileNotFoundError:
            raise InventarioError(f"El archivo CSV no existe en la ruta: {ruta}")
        except InventarioError as e:
            # Lanzo de nuevo los errores de inventario
            raise e
        except Exception as e:
            # Otros errores de lectura
            raise InventarioError(f"Error al cargar el archivo CSV en {ruta}: {e}")

        # Fusionar el inventario leído con el actual (self)
        # Esto suma los valores de los elementos comunes.
        self.fusionar(inventario_leido)




    # ========================= MÉTODOS DE CONSULTA =============================
    def consultar(self, nombre: str) -> float:
        """Devuelve el valor actual del elemento nombre o 0.0 si no existe."""
        nodo:'Nodo' = self._buscar_nodo(nombre)
        if nodo is not None:
            return nodo.get_valor()  
        return 0.0

    def existe(self, nombre: str) -> bool:
        """Indica si el elemento nombre está presente en el inventario."""
        nodo:'Nodo' = self._buscar_nodo(nombre)
        return nodo is not None

    def total_items(self) -> int:
        """Retorna el número total de elementos distintos en el inventario."""
        return self._get_longitud()

    def cantidad_total(self) -> float:
        """Retorna la suma de los valores de todos los elementos del inventario."""
        total_inventario:float = 0.0
        actual:'Nodo' = self.get_primer_nodo()
        while actual is not None:
            total_inventario += actual.get_valor()    # Usando el getter
            actual = actual.get_siguiente() # Usando el getter
        return total_inventario

    def maximo(self) -> str:
        """
        Devuelve el elemento con el valor más alto.
        Excepciones: InventarioError si el inventario está vacío.
        """
        if self.get_primer_nodo() is None:
            raise InventarioError("El inventario está vacío.")
        
        max_nombre:str = self.get_primer_nodo().get_nombre() 
        max_valor:float = self.get_primer_nodo().get_valor() 
        
        actual:'Nodo' = self.get_primer_nodo().get_siguiente()
        while actual is not None:
            if actual.get_valor() > max_valor:    
                max_valor = actual.get_valor()
                max_nombre = actual.get_nombre()
            actual = actual.get_siguiente()
    
        return max_nombre

    def minimo(self) -> str:
        """
        Devuelve el elemento con el valor más bajo.
        Excepciones: InventarioError si el inventario está vacío.
        """
        if self.get_primer_nodo() is None:
            raise InventarioError("El inventario está vacío.")
        
        min_nombre:str = self.get_primer_nodo().get_nombre() 
        min_valor:float = self.get_primer_nodo().get_valor() 
        
        actual:'Nodo' = self.get_primer_nodo().get_siguiente()
        while actual is not None:
            if actual.get_valor() < min_valor:    
                min_valor = actual.get_valor()
                min_nombre = actual.get_nombre()
            actual = actual.get_siguiente()
    
        return min_nombre

    def ordenar_por_valor(self, descendente: bool = False) -> list[str]:
        """
        Devuelve una lista con los nombres de los elementos, ordenados por su valor.
        """
        # TODO
        pass

    def copiar(self) -> Inventario:
        """
        Crea y retorna un nuevo inventario mediante copia profunda.
        """
        # TODO 
        pass