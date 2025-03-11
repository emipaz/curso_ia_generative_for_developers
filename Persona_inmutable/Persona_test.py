import unittest
from datetime import date
from persona import Persona

class TestPersona(unittest.TestCase):

    def test_instanciar_con_fecha_aaaammdd(self):
        persona = Persona("Carlos Ruiz", "1993-12-01")
        self.assertEqual(persona.fecha_nacimiento, date(1993, 12, 1))

    def test_instanciar_con_fecha_ddmmaaaa(self):
        persona = Persona("Lucía Fernández", "01-03-1995")
        self.assertEqual(persona.fecha_nacimiento, date(1995, 3, 1))

    def test_instanciar_con_fecha_con_separador_slash(self):
        persona = Persona("María López", "1998/09/15")
        self.assertEqual(persona.fecha_nacimiento, date(1998, 9, 15))

    def test_instanciar_con_fecha_con_separador_dos_puntos(self):
        persona = Persona("José Martínez", "1990:11:25")
        self.assertEqual(persona.fecha_nacimiento, date(1990, 11, 25))

    def test_instanciar_con_fecha_con_separador_punto(self):
        persona = Persona("Ana García", "1987.06.30")
        self.assertEqual(persona.fecha_nacimiento, date(1987, 6, 30))

    def test_fecha_invalida(self):
        with self.assertRaises(ValueError):
            Persona("Pedro Gutiérrez", "2023-02-30")  # Día no válido

    def test_inmutabilidad_nombre(self):
        persona = Persona("Sofía Castro", "1992-09-10")
        with self.assertRaises(AttributeError):
            persona._nombre = "Nuevo Nombre"  # Intentar cambiar un atributo inmutable

    def test_inmutabilidad_dni(self):
        persona = Persona("Fernando Gómez", "1985-04-25", "Z12345678")
        with self.assertRaises(AttributeError):
            persona.dni = "Nuevodni"  # Intentar cambiar un atributo inmutable

    def test_agregar_dni_persona_sin_dni(self):
        persona = Persona("Sofía Castro", "1992-09-10")
        persona.set_dni("888888")
        self.assertEqual(persona.dni, "888888")

    def test_agregar_dni_persona_con_dni(self):
        persona = Persona("Sofía Castro", "1992-09-10",  "888888")
        with self.assertRaises(AttributeError):
            persona.set_dni("888888")

    def test_igualdad_instancias(self):
        persona_1 = Persona("Laura Torres", "1995-07-15", "A12345678")
        persona_2 = Persona("Laura Torres", "1995-07-15", "A12345678")
        self.assertEqual(persona_1, persona_2)  # Deben ser iguales

    def test_no_igualdad_instancias_diferentes_dni(self):
        persona_1 = Persona("Javier Soto", "1988-01-12", "B23456789")
        persona_2 = Persona("Javier Soto", "1988-01-12", "C23456789")
        self.assertNotEqual(persona_1, persona_2)  # No deben ser iguales

    def test_atributo_dinamico(self):
        persona = Persona("Marta Silva", "1986-05-20")
        persona.set_profesion("Ingeniera")  # Se establece un atributo dinámico
        self.assertEqual(persona.profesion, "Ingeniera")

    def test_modificar_profesion(self):
        persona = Persona("Ernesto Ruiz", "1974-11-30")
        persona.set_profesion("Abogado")
        self.assertEqual(persona.profesion, "Abogado")

    def test_agregar_atributo_no_valido(self):
        persona = Persona("Ernesto Ruiz", "1974-11-30")
        with self.assertRaises(AttributeError):
            persona.nuevo_attr = "nuevo Atributo"

    def test_sgregar_attr_x_dict(self):
        persona = Persona("Ernesto Ruiz", "1974-11-30")
        with self.assertRaises(AttributeError):
            persona.__dict__["nuevo_atributo"] = "nuevo"
            

# Ejecutar las pruebas
if __name__ == '__main__':
    unittest.main()
