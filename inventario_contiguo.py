from copy import deepcopy
import csv

class InventarioError(Exception):
    def __init__(self, msg = "%ERR%. Se ha producido un error en el inventario"):
        super().__init__(msg)
        self._msg = msg

    def __str__(self):
        return self._msg

class Inventario:
    """
    Parte Privada del Inventario Contiguo.
    """

    _CAPACIDAD_MINIMA : int = 2

    @classmethod
    def _get_capacidad_minima(cls):
        return cls._CAPACIDAD_MINIMA

    #Creación de un inventario, inicialmente vacío.
    def __init__(self):
        self._capacidad : int = Inventario._CAPACIDAD_MINIMA
        self._nombres : list[str | None] = [None] * self._capacidad
        self._valores : list[float | None]  = [None] * self._capacidad
        self._longitud : int = 0

    #Getters y setters
    def _get_capacidad(self) -> int:
        return self._capacidad

    def _get_nombres(self) -> list[str | None]:
        return self._nombres

    def _get_valores(self) -> list[float | None]:
        return self._valores

    def _get_longitud(self) -> int:
        return self._longitud

    def _set_capacidad(self, capacidad: int) -> None:
        self._capacidad = capacidad

    def _set_nombres(self, keys: list[str]) -> None:
        self._nombres = keys

    def _set_valores(self, values: list[float]) -> None:
        self._valores = values

    def _set_longitud(self, nueva_longitud: int) -> None:
        self._longitud = nueva_longitud

    def _incrementar_longitud(self) -> None:
        self._longitud += 1

    def _decrementar_longitud(self) -> None:
        self._longitud -= 1

    # ============================= CONSULTAS =============================

    def consultar(self, nombre: str) -> float:
        """
        Devuelve el valor actual del elemento nombre, o 0.0 si no existe.

        Parámetros -> nombre: str

        Return -> valor: float

        Exception -> None
        """

        for i in range(self._get_longitud()):
            if self._get_nombres()[i] == nombre:
                return self._get_valores()[i]

        return 0.0

    #Funcionalidad extra para facilitar la lógica.
    def inventario_lleno(self) -> bool:
        """
        Indica si el inventario ha alcanzado su capacidad máxima.

        Parámetros -> self: Inventario

        Return -> True/False: bool

        Exception -> None
        """

        if self._get_capacidad() == self._get_longitud():
            return True

        return False

    def existe(self, nombre: str) -> bool:
        """
        Indica si el elemento nombre está presente en el inventario.

        Parámetros -> nombre: str

        Return -> True/False: bool

        Exception -> None
        """

        for i in range(self._get_longitud()):
            if self._get_nombres()[i] == nombre:
                return True
        return False

    def total_items(self) -> int:
        """
        Retorna el número total de elementos distintos en el inventario.

        Parámetros -> self: Inventario

        Return -> num_total_items_distintos: int

        Exception -> None
        """

        return self._get_longitud()

    def cantidad_total(self) -> float:
        """
        Retorna la suma de los valores de todos los elementos del inventario.

        Parámetros -> self: Inventario

        Return -> suma_total_items: float

        Exception -> None
        """

        suma : float = 0
        for i in range(self._get_longitud()):
            suma += self._get_valores()[i]

        return suma

    def maximo(self) -> str:
        """
        Devuelve el elemento con el valor más alto.
        En caso de coincidencia, se devuelve uno de los coincidentes.

        Parámetros -> self: Inventario

        Return -> nombre_max: str

        Exception -> InventarioError si el inventario está vacío.
        """

        if self._get_longitud() == 0:
            raise InventarioError("Imposible encontrar al máximo, el inventario está vacío.")

        nombre_max : str = self._get_nombres()[0]
        maximo : float = self._get_valores()[0]

        for i in range(1, self._get_longitud()):
            if self._get_valores()[i] > maximo:
                maximo = self._get_valores()[i]
                nombre_max = self._get_nombres()[i]

        return nombre_max

    def minimo(self) -> str:
        """
        Devuelve el elemento con el valor más bajo.
        En caso de coincidencia, se devuelve uno de los coincidentes.

        Parámetros -> self: Inventario

        Return -> nombre_min: float

        Exception -> InventarioError si el inventario está vacío.
        """

        if self._get_longitud() == 0:
            raise InventarioError("Imposible encontrar al mínimo, el inventario está vacío.")

        nombre_min : str = self._get_nombres()[0]
        minimo : float = self._get_valores()[0]

        for i in range(1, self._get_longitud()):
            if self._get_valores()[i] < minimo:
                minimo = self._get_valores()[i]
                nombre_min= self._get_nombres()[i]

        return nombre_min

    #Usamos inserción
    def ordenar_por_valor(self, descendente: bool = False) -> list[str]:
        """
        Devuelve la lista de nombres ordenada según su valor usando inserción.

        Parámetros -> descendente: bool (False por defecto)

        Return -> lista_ordenada: list[str]

        Exception -> None
        """

        #Creamos dos listas de nombres y valores vacías que son copias de los del inventario.
        #Lo hacemos para no modificar el propio inventario cuando lo ordenamos.
        l = self._get_longitud()
        nombres : list[str | None] = [None] * l
        valores : list[float | None] = [None] * l

        for i in range(l):
            nombres[i] = self._get_nombres()[i]
            valores[i] = self._get_valores()[i]

        # Ordenación por inserción
        for i in range(1, l):
            key_nombre = nombres[i]
            key_valor = valores[i]
            j = i - 1

            while j >= 0 and ((not descendente and valores[j] > key_valor) or
                              (descendente and valores[j] < key_valor)):
                valores[j + 1] = valores[j]
                nombres[j + 1] = nombres[j]
                j -= 1

            valores[j + 1] = key_valor
            nombres[j + 1] = key_nombre

        return nombres

    def copiar(self) -> 'Inventario':
        """
        Crea y retorna una copia profunda del inventario.

        Parámetros -> self: Inventario

        Return -> copia_profunda: Inventario

        Exception -> None
        """

        copia_profunda = deepcopy(self)
        return copia_profunda

    # ============================= MODIFICADORES =============================

    def agregar(self, nombre: str, valor: float = 1.0) -> None:
        """
        Modifica el inventario añadiendo el elemento nombre con el valor indicado.
        Si el elemento ya existe, se incrementa su valor.

        Parámetros ->
            nombre: str
            valor: float (por defecto 1.0)

        Return -> None

        Excepciones ->
            InventarioError si valor ≤ 0.
        """

        if valor <= 0:
            raise InventarioError(f"Valor debe ser mayor a 0.")

        nombres = self._get_nombres()
        valores = self._get_valores()
        l = self._get_longitud()

        if self.existe(nombre):

            i: int = 0
            while i < l:
                if nombres[i] == nombre:
                    valores[i] += valor
                    return
                i += 1
        else:
            if self.inventario_lleno():
                nueva_capacidad = self._get_capacidad() * 2
                nuevos_nombres : list[str | None] = [None] * nueva_capacidad
                nuevos_valores : list[float | None] = [None] * nueva_capacidad

                for i in range(l):
                    nuevos_nombres[i] = nombres[i]
                    nuevos_valores[i] = valores[i]

                nuevos_nombres[l] = nombre
                nuevos_valores[l] = valor

                self._set_capacidad(nueva_capacidad)
                self._set_nombres(nuevos_nombres)
                self._set_valores(nuevos_valores)
                self._incrementar_longitud()

            else:
                nombres[l] = nombre
                valores[l] = valor

                self._incrementar_longitud()

    def actualizar(self, nombre: str, nuevo_valor: float) -> None:
        """
        Sustituye el valor actual del elemento nombre por nuevo_valor.

        Parámetros ->
            nombre: str
            nuevo_valor: float

        Return -> None

        Excepciones ->
            InventarioError si nombre no existe.
            InventarioError si nuevo_valor ≤ 0.
        """

        if nuevo_valor <= 0:
            raise InventarioError(f"Valor debe ser mayor a 0.")
        elif not self.existe(nombre):
            raise InventarioError(f"Nombre '{nombre}' no encontrado en el inventario.")
        else:
            i: int = 0
            while i < self._get_longitud():
                if self._get_nombres()[i] == nombre:
                    self._get_valores()[i] = nuevo_valor
                    return
                i += 1

    #Aquí hay que comprobar que la cantidad a eliminar sea <= 0, ¿no? En el enunciado se les ha olvidado.
    def eliminar(self, nombre: str, cantidad : float = 1.0) -> None:
        """
        Resta la cantidad indicada al elemento nombre.
        Si el valor resultante es ≤ 0, el elemento se elimina.

        Parámetros ->
            nombre: str
            cantidad: float (por defecto 1.0)

        Return -> None

        Excepciones ->
            InventarioError si el elemento no existe.
            InventarioError si cantidad < 0.
        """

        if not self.existe(nombre):
            raise InventarioError("El elemento que se quiere eliminar no está en el inventario.")
        elif cantidad < 0:
            raise InventarioError(f"Valor a eliminar ha de ser mayor o igual a 0.")

        nombres = self._get_nombres()
        valores = self._get_valores()
        l = self._get_longitud()

        for i in range(l):
            if nombres[i] == nombre:
                if cantidad >= valores[i]:
                    for j in range(i, l-1):
                        nombres[j] = nombres[j+1]
                        valores[j] = valores[j+1]

                    nombres[l-1] = None
                    valores[l-1] = None
                    self._decrementar_longitud()
                else:
                    valores[i] -= cantidad
                return

    def fusionar(self, otro_inventario : 'Inventario') -> None:
        """
        Modifica el inventario actual añadiendo los elementos del inventario otro.
        Si un elemento existe en ambos, sus valores se suman.

        Parámetros -> otro_inventario: Inventario

        Return -> None

        Exception -> InventarioError si otro_inventario no es un Inventario.
        """

        if not isinstance(otro_inventario, Inventario):
            raise InventarioError("El inventario proporcionado no es de tipo Inventario")

        for nombre in otro_inventario:
            valor_otro: float = otro_inventario.consultar(nombre)
            self.agregar(nombre, valor_otro)

    def diferencia(self, otro_inventario: 'Inventario') -> None:
        """
        Resta al inventario actual los valores del inventario proporcionado.
        Elementos que lleguen a valor ≤ 0 se eliminan.

        Parámetros -> otro_inventario: Inventario

        Return -> None

        Exception -> InventarioError si otro_inventario no es Inventario.
        """

        if not isinstance(otro_inventario, Inventario):
            raise InventarioError("El inventario proporcionado no es de tipo Inventario")

        otros_nombres = otro_inventario._get_nombres()
        otros_valores = otro_inventario._get_valores()

        for i in range(otro_inventario._get_longitud()):
            if self.existe(otros_nombres[i]):
                self.eliminar(otros_nombres[i], otros_valores[i])

    def vaciar(self) -> None:
        """
        Elimina todos los elementos del inventario, dejándolo vacío.

        Parámetros -> self: Inventario

        Return -> None

        Exception -> None
        """

        for i in range(self._get_longitud()):
            self._get_nombres()[i] = None
            self._get_valores()[i] = None

        self._set_longitud(0)

    # ============================= PERSISTENCIA =============================
    def cargar(self, ruta : str = "inventario.csv") -> None:
        """
        Carga los elementos desde un archivo CSV y los fusiona con el inventario actual.

        Parámetros -> ruta: str (ruta al archivo CSV)

        Return -> None

        Exception -> InventarioError si el archivo no existe o su formato es incorrecto.
        """

        inventario_en_archivo : 'Inventario' = Inventario()

        try:
            with open(ruta, "r", newline="", encoding="utf-8") as archivo:
                reader = csv.reader(archivo, delimiter=",")

                for row in reader:
                    if len(row) != 2:
                        raise InventarioError(f"La línea {row} de {ruta} no se puede cargar en el inventario.")

                    nombre, valor_str = row
                    try:
                        valor = float(valor_str)
                        if valor > 0:
                            inventario_en_archivo.agregar(nombre, valor)

                    except ValueError:
                        raise InventarioError(f"Valor no numérico en el archivo CSV: '{valor_str}'")

        except FileNotFoundError:
            raise InventarioError(f"El archivo '{ruta}' no existe.")
        except InventarioError as e:
            raise e
        except Exception as e:
            raise InventarioError(f"Error al cargar el archivo CSV en {ruta}: {e}")

        self.fusionar(inventario_en_archivo)

    def guardar(self, ruta : str = "inventario.csv") -> None:
        """
        Guarda el inventario en un archivo CSV. Si el archivo existe,
        primero fusiona los datos actuales con los del archivo.

        Parámetros -> ruta: str

        Return -> None

        Exception -> InventarioError si no se puede escribir en el archivo.
        """

        #Intentamos cargar el archivo existente.
        try:
            self.cargar(ruta)
        except InventarioError:
            #Si no existe, hacemos pass y guardamos el inventario actual tal cual.
            pass

        try:
            with open(ruta, "w", newline="" ,encoding="utf-8") as archivo:
                writer = csv.writer(archivo)

                for i in range(self._get_longitud()):
                    writer.writerow([self._get_nombres()[i], self._get_valores()[i]])

        except FileNotFoundError:
            raise InventarioError(f"El archivo '{ruta}' no existe.")
        except Exception as e:
            raise InventarioError(f"Error al guardar el archivo CSV en {ruta}: {e}")

    # ============================= MÉTODOS MÁGICOS =============================
    def __len__(self) -> int:
        """
        Retorna el número de elementos del inventario (equivalente a total_items()).

        Parámetros -> self: Inventario

        Return -> total: int

        Exception -> None
        """

        return self.total_items()

    def __iter__(self):
        """
        Permite recorrer secuencialmente los nombres de los elementos del inventario.

        Parámetros -> self: Inventario

        Return -> iterador: Iterator[str]

        Exception -> None
        """

        for i in range(self._get_longitud()):
            yield self._get_nombres()[i]

    def __str__(self) -> str:
        """
        Devuelve una representación legible del inventario en formato texto.

        Parámetros -> self: Inventario

        Return -> representación: str

        Exception -> None
        """

        if self._get_longitud() == 0:
            return "Inventario vacío"

        resultado = "\nInventario:"
        for nombre in self:
            valor = self.consultar(nombre)
            resultado += f"\n  {nombre}: {valor}"
        return resultado
