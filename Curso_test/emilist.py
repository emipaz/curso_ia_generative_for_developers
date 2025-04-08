class Emilist(list):
    def __init__(self, nombre, size=20, max_element_length=20):
        super().__init__()  # Inicializar la lista base
        self.nombre = nombre
        self.MAX_LEN = size  # Tamaño máximo de la lista
        self.MAX_ELEMENT_LENGTH = max_element_length  # Tamaño máximo de cada elemento

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.nombre}> {len(self)} elementos: {super().__repr__()}"

    def __str__(self):
        st = self.nombre + ":\n"
        for elemento in self:
            st += "\t" + elemento + "\n"
        return st

    def append(self, valor):
        if len(self) >= self.MAX_LEN:
            raise OverflowError("La lista está llena, no se puede agregar más elementos.")
        
        if not valor:
            raise ValueError("No se puede agregar un valor vacío.")
        
        long=""
        if isinstance(valor, str) and 0 < ( long := len(valor) ) < self.MAX_ELEMENT_LENGTH:
            super().append(valor);
            return True
        elif long:
            raise ValueError(f"Emilist solo acepta strings de menos de {self.MAX_ELEMENT_LENGTH} caracteres y recibió un str de {long} caracteres.")
        else:
            raise TypeError(f"Emilist solo acepta strings y recibió un objeto tipo: {type(valor)}")

    def remove(self, elemento):
        if elemento not in self:
            raise ValueError(f"Elemento {elemento} no encontrado en la lista.")
        else:
            super().remove(elemento)

    def extend(self, otra_lista):
        for elemento in otra_lista:
            try:
                self.append(elemento)
            except OverflowError:
                return 
            except ValueError:
                pass
            except TypeError:
                pass

if __name__== "__main__":
    lista = Emilist("tareas", size=3,max_element_length=10)
    try:
        lista.append(1)
    except Exception as e:
        print (type(e),e)
    try:
        lista.append("Agregando una tarea")
    except Exception as e:
        print (type(e),e)
    lista.append("desayuno")
    lista.append("almuerzo")
    lista.append("cena")
    print(lista)
    try:
        lista.remove("cafe")
    except Exception as e:
        print (type(e),e)

    lista_numeros = Emilist("numeros", size=10)
    lista_numeros.append("diez")
    lista_numeros.extend(["uno","dos",1,0,"15","tres mil ochocientos cuarenta y cuatro"])
    print(lista_numeros)