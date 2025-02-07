def calculate_area(radio):
    """
    Calcula el área de un círculo dado su radio.
    
    Parámetros:
        radio (float): El radio del círculo.
    
    Retorna:
        float: El área del círculo si la entrada es válida.
    Execciones:
        ValueError: Si la entrada no es numérica.
        ValueError: Si el valor es menor que 0
    """
    from math import pi
    try:
        # Intentar convertir la entrada a un número flotante
        radio = float(radio)
    except ValueError:
        # Lanzar un error si la entrada no es numérica
        raise ValueError("La entrada debe ser un valor numérico.")
    else:
        if radio < 0:
            # lanzar un error si el radio es menor que 0
            raise ValueError("El radio no puede ser negativo.")
        # Calcular el área usando la fórmula del círculo
        return pi * radio ** 2

# Ejemplo de uso
if __name__ == "__main__":
    entrada = input("Ingrese el radio del círculo: ")
    try:
        area = calculate_area(entrada)
        print(f"El área del círculo es: {area:.2f}")
    except ValueError as e:
        print(f"Error: {e}")
    finally :
        print("Gracias por uasr mi Script")