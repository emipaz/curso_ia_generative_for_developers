from persona import Persona

class Empleado:
    """
    Clase que representa a un empleado, usando composición con Persona.
    """

    def __init__(self, nombre, fecha_nacimiento, dni="", profesion=None, puesto=None):
        self.persona = Persona(nombre, fecha_nacimiento, dni, profesion=profesion)
        self._puesto = puesto

    @property
    def nombre(self):
        """Devuelve el nombre del empleado."""
        return self.persona.nombre

    @property
    def dni(self):
        """Devuelve el DNI del empleado."""
        return self.persona.dni

    @property
    def fecha_nacimiento(self):
        """Devuelve la fecha de nacimiento del empleado."""
        return self.persona.fecha_nacimiento

    @property
    def profesion(self):
        """Devuelve la profesión del empleado."""
        return self.persona.profesion
    
    def set_profesion(self, valor):
        self.persona.set_profesion(valor)
        
    @property
    def puesto(self):
        """Devuelve el puesto del empleado."""
        return self._puesto

    def set_puesto(self, valor):
        """Establece el puesto para el empleado."""
        self._puesto = valor

    def obtener_atributos(self):
        """Devuelve un diccionario con los atributos del empleado y los de Persona."""
        atributos = self.persona.obtener_atributos()
        atributos['puesto'] = self._puesto  # Añade el puesto
        return atributos

    @property
    def __dict__(self):
        return self.obtener_atributos()
    
    
if __name__ == "__main__":
    empleado = Empleado("Juan Pérez", "1990-01-01", "12345678A", "Desarrollador", "Ingeniero de Software")
    empleado.set_puesto("Senior Ingeniero de Software")

    print(empleado.obtener_atributos())

    empleado.set_profesion("jubilado")
    print(empleado.obtener_atributos())
    print(empleado.__dict__)