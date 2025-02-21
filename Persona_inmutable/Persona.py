import re
import datetime

class Persona:
    """
    Clase que representa a una persona con atributos inmutables y mutables.
    
    Los atributos inmutables son: nombre, fecha de nacimiento y DNI.
    El atributo 'profesion' es mutable y puede ser cambiado.
    Se Puede implentar mas Atributos agrgandolos a __dict__
    """
    
    __slots__ = ('_nombre', '_fecha_nacimiento', '_bloqueado', '_dni', '__dict__')

    # Diccionario de patrones para validación de fechas
    __patrones_fechas = {
        "AAAA-MM-DD": re.compile(r'(\d{4})[-:,.//](\d{2})[-:,.//](\d{2})'),
        "DD-MM-AAAA": re.compile(r'(\d{2})[-:,.//](\d{2})[-:,.//](\d{4})')
    }

    def __init__(self, nombre, fecha_nacimiento, dni=""):
        """
        Inicializa una nueva instancia de Persona.
        
        Args:
            nombre (str): El nombre de la persona.
            fecha_nacimiento (str o datetime.date): La fecha de nacimiento de la persona.
            dni (str): El DNI de la persona (opcional).
        """
        super().__setattr__('_nombre', nombre)
        super().__setattr__('_fecha_nacimiento', self.validar_fecha(fecha_nacimiento))
        super().__setattr__("_dni", dni)
        super().__setattr__('_bloqueado', bool(dni))
        super().__setattr__('__dict__', {})

    def validar_fecha(self, fecha):
        """
        Valida y convierte la fecha de nacimiento a un objeto datetime.date.
        
        Acepta diferentes formatos de fecha.
        
        Args:
            fecha (str o datetime.date): La fecha a validar.
            
        Returns:
            datetime.date: La fecha convertida a objeto datetime.date.
            
        Raises:
            ValueError: Si la fecha proporcionada no es válida.
        """
        if isinstance(fecha, datetime.date):
            return fecha
        
        # Itera sobre los patrones para encontrar coincidencias
        for formato, patron in self.__patrones_fechas.items():
            coincidencias = patron.match(fecha)
            if coincidencias:
                try:
                    if formato == "AAAA-MM-DD":
                        return datetime.date(int(coincidencias.group(1)), 
                                             int(coincidencias.group(2)), 
                                             int(coincidencias.group(3)))
                    elif formato == "DD-MM-AAAA":
                        return datetime.date(int(coincidencias.group(3)), 
                                             int(coincidencias.group(2)), 
                                             int(coincidencias.group(1)))
                except ValueError:
                    raise ValueError(f"Fecha no válida: {fecha}")

        raise ValueError(f"Formato de fecha no reconocido: {fecha}")
    def __setattr__(self, nombre, valor):
        """Controla la asignación de atributos a la instancia."""
        if nombre not in self.__slots__:
            if not hasattr(self.__class__, f"{nombre}setter"):
                raise AttributeError(f"No puedes agregar el atributo '{nombre}'")
            super().__setattr__(nombre, valor)  # Asigna el valor
        else:
            raise AttributeError(f"No puedes modificar '{nombre}'")

    def __eq__(self, otro):
        """Compara dos objetos Persona."""
        return isinstance(otro, Persona) and self.__hash__() == otro.__hash__()

    def __hash__(self):
        """Devuelve el hash de la instancia basada en los atributos inmutables."""
        return hash((self._nombre, self._fecha_nacimiento, self._dni))

    @property
    def dni(self):
        """Devuelve el DNI de la persona, o un mensaje si no está registrado."""
        return self._dni if self._dni else "DNI no registrado"

    def set_dni(self, valor):
        """Permite establecer el DNI si no está bloqueado."""
        if not self._bloqueado:
            super().__setattr__("_dni", valor)
            super().__setattr__("_bloqueado", True)
        else:
            raise AttributeError(f"No puedes modificar el 'dni', la persona tiene dni: {self._dni}.")

    @property
    def nombre(self):
        """Devuelve el nombre de la persona."""
        return self._nombre

    @property
    def fecha_nacimiento(self):
        """Devuelve la fecha de nacimiento de la persona."""
        return self._fecha_nacimiento

    @property
    def profesion(self):
        """Devuelve la profesión de la persona si está establecida."""
        return self.__dict__.get("profesion", None)

    def set_profesion(self, valor):
        """Establece la profesión de la persona."""
        self.__dict__["profesion"] = valor

    def obtener_atributos(self):
        """Devuelve un diccionario con los atributos inmutables y los mutables."""
        return {
            'nombre': self._nombre,
            'fecha_nacimiento': self._fecha_nacimiento,
            'dni': self._dni,
            **self.__dict__}