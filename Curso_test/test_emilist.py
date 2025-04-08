import pytest
from emilist import Emilist  # Asegúrate de que la clase Emilist esté en el archivo emilist.py

def test_initialization():
    emilist = Emilist("tareas", size=5, max_element_length=10)
    assert emilist.nombre == "tareas"
    assert emilist.MAX_LEN == 5
    assert emilist.MAX_ELEMENT_LENGTH == 10
    assert len(emilist) == 0

def test_append_valid_string():
    emilist = Emilist("tareas")
    assert len(emilist) == 0
    emilist.append("tarea 1")
    assert len(emilist) == 1
    assert "tarea 1" in emilist

def test_append_full_list():
    emilist = Emilist("tareas", size=2)
    emilist.append("tarea 1")
    emilist.append("tarea 2")
    with pytest.raises(OverflowError):
        emilist.append("tarea 3")

def test_append_empty_value():
    emilist = Emilist("tareas")
    with pytest.raises(ValueError, match="No se puede agregar un valor vacío."):
        emilist.append("")

def test_append_non_string_value():
    emilist = Emilist("tareas")
    with pytest.raises(TypeError, match="Emilist solo acepta strings y recibió un objeto tipo: <class 'int'>"):
        emilist.append(123)

def test_append_string_too_long():
    emilist = Emilist("tareas", max_element_length=5)
    with pytest.raises(ValueError, match="Emilist solo acepta strings de menos de 5 caracteres y recibió un str de 21 caracteres."):
        emilist.append("tarea demasiado larga")

def test_remove_existing_element():
    emilist = Emilist("tareas")
    emilist.append("tarea 1")
    emilist.remove("tarea 1")
    assert len(emilist) == 0

def test_remove_non_existing_element():
    emilist = Emilist("tareas")
    emilist.append("tarea 1")
    with pytest.raises(ValueError, match="Elemento cafe no encontrado en la lista."):
        emilist.remove("cafe")

def test_extend_with_valid_elements():
    emilist = Emilist("tareas", size=5)
    emilist.extend(["tarea 1", "tarea 2"])
    assert len(emilist) == 2
    assert "tarea 1" in emilist
    assert "tarea 2" in emilist

def test_extend_with_oversized_elements():
    emilist = Emilist("tareas", size=2)
    emilist.append("tarea 1")
    emilist.extend(["tarea 2", "tarea 3"])
    assert len(emilist) == 2  # No debe permitir agregar "tarea 3"

def test_extend_with_non_string_elements():
    emilist = Emilist("tareas")
    emilist.extend([1, 2, "tarea válida"])
    assert len(emilist) == 1  # Solo debe agregar "tarea válida"

def test_repr_method():
    emilist = Emilist("tareas")
    emilist.append("tarea 1")
    assert repr(emilist) == "<Emilist tareas> 1 elementos: ['tarea 1']"

def test_str_method():
    emilist = Emilist("tareas")
    emilist.append("tarea 1")
    expected_str = "tareas:\n\ttarea 1\n"
    assert str(emilist) == expected_str

if __name__ == "__main__":
    pytest.main()
