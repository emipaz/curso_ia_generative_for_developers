class Emilist(list):
    """Una lista personalizada con restricciones de tamaño y longitud de elementos.

    Emilist es una subclase de `list` que impone un límite en la cantidad de elementos
    y en la longitud de cada uno. Solo acepta strings y genera errores si se intenta
    agregar elementos que no cumplan con las restricciones.

    Attributes:
        nombre (str): Nombre de la lista.
        MAX_LEN (int): Número máximo de elementos permitidos en la lista.
        MAX_ELEMENT_LENGTH (int): Longitud máxima permitida para cada elemento.
    """

    def __init__(self, nombre, size=20, max_element_length=20):
        """Inicializa la lista con nombre y restricciones de tamaño.

        Args:
            nombre (str): Nombre de la lista.
            size (int, optional): Tamaño máximo de la lista. Por defecto es 20.
            max_element_length (int, optional): Longitud máxima de cada elemento. Por defecto es 20.
        """
        super().__init__()
        self.nombre = nombre
        self.MAX_LEN = size
        self.MAX_ELEMENT_LENGTH = max_element_length

    def __repr__(self):
        """Devuelve una representación en cadena de la lista.

        Returns:
            str: Representación de la lista con su nombre y número de elementos.
        """
        return f"<{self.__class__.__name__} {self.nombre}> {len(self)} elementos: {super().__repr__()}"

    def __str__(self):
        """Devuelve una cadena con el contenido de la lista.

        Returns:
            str: Nombre de la lista y sus elementos formateados.
        """
        st = self.nombre + ":\n"
        for elemento in self:
            st += f"\t{elemento}\n"
        return st

    def append(self, valor):
        """Agrega un elemento a la lista si cumple con las restricciones.

        Args:
            valor (str): Elemento a agregar.

        Raises:
            OverflowError: Si la lista ya alcanzó el tamaño máximo.
            ValueError: Si el elemento es una cadena vacía o excede la longitud permitida.
            TypeError: Si el elemento no es una cadena.

        Returns:
            bool: True si el elemento se agrega con éxito.
        """
        if len(self) >= self.MAX_LEN:
            raise OverflowError("La lista está llena, no se puede agregar más elementos.")
        
        if not valor:
            raise ValueError("No se puede agregar un valor vacío.")
        
        if isinstance(valor, str):
            long = len(valor)
            if 0 < long <= self.MAX_ELEMENT_LENGTH:
                super().append(valor)
                return True
            raise ValueError(f"Emilist solo acepta strings de hasta {self.MAX_ELEMENT_LENGTH} caracteres y recibió un str de {long} caracteres.")
        
        raise TypeError(f"Emilist solo acepta strings y recibió un objeto tipo: {type(valor)}")

    def remove(self, elemento):
        """Elimina un elemento de la lista.

        Args:
            elemento (str): Elemento a eliminar.

        Raises:
            ValueError: Si el elemento no está en la lista.
        """
        if elemento not in self:
            raise ValueError(f"Elemento {elemento} no encontrado en la lista.")
        super().remove(elemento)

    def extend(self, otra_lista):
        """Extiende la lista con elementos de otra lista.

        Solo se agregan los elementos válidos que cumplen con las restricciones.
        Si la lista alcanza su tamaño máximo, la operación se detiene.

        Args:
            otra_lista (iterable): Lista de elementos a agregar.

        Warnings:
            Se omitirán silenciosamente los elementos inválidos.
        """
        for elemento in otra_lista:
            try:
                self.append(elemento)
            except OverflowError:
                print("Extensión detenida: La lista ha alcanzado su límite.")
                break
            except (ValueError, TypeError) as e:
                print(f"Advertencia: {e}")
