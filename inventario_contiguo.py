from copy import deepcopy

class InventarioError(Exception):
    def __init__(self, msg = "%ERR%. Se ha producido un error en el inventario"):
        super().__init__(msg)
        self._msg = msg

    def __str__(self):
        return self._msg

class InventarioContiguo:
    """
    Parte Privada del Inventario Contiguo.
    """

    _CAPACIDAD_MINIMA : int = 2

    @classmethod
    def _get_capacidad_minima(cls):
        return cls._CAPACIDAD_MINIMA

    #Creación de un inventario, inicialmente vacío.
    def __init__(self):
        self._capacidad : int = InventarioContiguo._CAPACIDAD_MINIMA
        self._nombres : list[str | None] = [None] * self._capacidad
        self._valores : list[float | None]  = [None] * self._capacidad
        self._longitud : int = 0

    #Getters y setters
    def _get_capacidad(self) -> int:
        return self._capacidad

    def _get_nombres(self) -> list[str]:
        return self._nombres

    def _get_valores(self) -> list[float]:
        return self._valores

    def _get_longitud(self) -> int:
        return self._longitud

    def _set_capacidad(self, capacidad: int) -> None:
        self._capacidad = capacidad

    def _set_nombres(self, keys: list[str]) -> None:
        self._nombres = keys

    def _set_valores(self, values: list[float]) -> None:
        self._valores = values

    def _incrementar_longitud(self) -> None:
        self._longitud += 1

    def _decrementar_longitud(self) -> None:
        self._longitud -= 1

    #Consultas
    def consultar(self, nombre : str) -> float :
        i : int = 0
        while i < self._get_longitud():
            if self._get_nombres()[i] == nombre:
                return self._get_valores()[i]
            i += 1

        raise KeyError(f"Elemento '{nombre}' no encontrado")

    #Funcionalidad extra para facilitar la lógica.
    def inventario_lleno(self) -> bool:
        if self._get_capacidad() == self._get_longitud():
            return True

        return False

    def existe(self, nombre : str) -> bool:
        i : int = 0
        while i < self._get_longitud() and self._get_valores()[i] != nombre:
            i += 1

        return i < self._get_longitud()

    #Pendiente de revisión pq es lo mismo que self._get_longitud() ¿Lo quitamos y dejamos el de arriba? ¿Quitamos el de arriba y dejamos este?
    def total_items(self) -> int:
        return self._get_longitud()

    def cantidad_total(self) -> float:
        suma : float = 0
        for i in range(self._get_longitud()):
            suma += self._get_valores()[i]

        return suma

    def maximo(self) -> float:
        maximo : float = 0
        for i in range(1, self._get_longitud()):
            if self._get_valores()[i] > maximo:
                maximo = self._get_valores()[i]

        return maximo

    def minimo(self) -> float:
        minimo : float = 0
        for i in range(1, self._get_longitud()):
            if self._get_valores()[i] < minimo:
                minimo = self._get_valores()[i]

        return minimo

    #Usamos inserción
    def ordenar_por_valores(self, descendente: bool = False) -> list[str]:
        n = self._get_longitud()
        nombres = self._get_nombres()
        valores = self._get_valores()

        for i in range(1, n):
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

    def copiar(self) -> 'InventarioContiguo':
        copia_profunda = deepcopy(self)
        return copia_profunda

    # Modificadores
    def agregar(self, nombre: str, valor: float = 1.0) -> None:
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


