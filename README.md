# Ejercicios de Codigos del curso Introduction to Generative AI for Software Development

## Prompts de ejemplo (Generating code with chatbots)

- Escribe una función en Python que sume dos números llamados 'a' y 'b' y devuelva el resultado

- Crea una función en JavaScript que sume dos números

- Escribe un método en C# que sume dos números

- Escribe una función en Python que use NumPy para sumar dos arrays

- Escribe una función básica en JavaScript para verificar si un número es primo

- Actualiza la función para incluir manejo de errores para entradas que no sean enteros o que no sean positivas

- Haz una función

- Escribe una función en Python para calcular el cuadrado de un número

- Crea una aplicación simple en Flask con un endpoint de API en Python. Este endpoint debe manejar solicitudes GET en la URL /multiply, aceptar dos parámetros de consulta a y b, y devolver la multiplicación de estos dos parámetros como una respuesta en formato JSON. Asegúrate de incluir manejo de errores si los parámetros no se proporcionan o si no pueden convertirse a enteros


- Depuración de código con un LLM

Encuentra el error en este código

```python
def calcular_promedio(numeros):
    suma_total = sum(numeros)
    cantidad = len(numeros)
    promedio = suma_total / cantidad
    return promedio
```

- Escribe una función que calcule el área de un círculo dado el radio de ese círculo

### Ejemplo de un prompt efectivo

Prompt:

Escribe una función en Python llamada calculate_area que tome un argumento radius.

La función debe calcular el área de un círculo dado el radio.
Asegúrate de que la función maneje entradas no numéricas lanzando un ValueError con el mensaje "La entrada debe ser un valor numérico."

Incluye comentarios en el código explicando cada paso.

### En la carpeta prompt-Flask

Hay un ejemplo claro de como dando mas indicaciones de lo que realmente queremos obtenemos mejores resultado para comenzar un proecto

## Iterative prompting

- Escribe una función en Python para calcular la desviación estándar de una lista de números.

- Escribe una función en Python utilizando la biblioteca requests para descargar un archivo desde una URL y guardarlo en el disco, sin usar bibliotecas de terceros como wget

- Crea una API REST en Flask para devolver datos de usuario

- Agrega manejo de errores a la API para gestionar los códigos de estado 404 y 500

- Agrega comentarios detallados que expliquen este código. Resalta cualquier parte compleja que pueda requerir una explicación más profunda

## Giving the LLM feedback

- Escribe una función en Python para calcular el factorial de un número
  - Modifica la función para incluir una verificación que asegure que la entrada sea un número entero no negativo

- Crea una función en Python para verificar si una cadena es un palíndromo
  - Actualiza el código para asegurarte de que la cadena no esté vacía

- Escribe una función en Python para encontrar todos los caracteres únicos en una cadena
  - (Haz el codigo mucho mas simple teniendo en cuenta que un set solo almacena caracteres únicos)

- Explica cómo usar la función set de Python para calcular los caracteres únicos en una cadena

## * Assigning the LLM a role

Prompts con y sin roles

- Sin Rol
  - Escribe una función en Python para calcular un factorial
- Con Rol de Tutor o Mentor
  - Como mi mentor de Python, por favor escribe una función para calcular un factorial y explica cómo funciona

- Explica cómo crear una lista en Python y agregarle elementos

  - Como tutor de Python para principiantes, explica cómo crear una lista en Python y agregarle elementos

  - ALTERNATIVA
    - Eres un mentor de programación amigable. Explica cómo crear una lista en Python y agregarle elementos.
    - Como un guía de código amigable, explica cómo funcionan los bucles en Python

## Leveling up with multiple roles

- Como arquitecto de software y experto en seguridad, evalúa este script de Python para una aplicación web y sugiere mejoras arquitectónicas y de seguridad

```python
def storeuserdata(user_data):
    database = open('user_database.txt', 'a')
    database.write(str(user_data))
    database.close()

storeuserdata({'username': 'admin', 'password': '1234'})
```

## Expert roles for specialized knowledge

- Como colaborador de proyectos de código abierto en Python, critica esta biblioteca de Python para visualización de datos y sugiere mejoras para hacerla comparable a bibliotecas importantes como Matplotlib o Seaborn

```python
import matplotlib.pyplot as plt

class DataVisualizer:
    def __init__(self, data):
        self.data = data

    def plot(self, kind='line'):
        if kind == 'line':
            plt.plot(self.data)
        elif kind == 'bar':
            plt.bar(range(len(self.data)), self.data)
        plt.show()

# Example usage
visualizer = DataVisualizer([10, 20, 30, 40, 50])
visualizer.plot('bar')
```

- Como experto en NLP, sugiere mejoras para esta función de resumen de texto para mejorar su funcionalidad y precisión

```python
import nltk

class TextAnalyzer:
    def __init__(self, text):
        self.text = text

    def summarize(self):
        sentences = nltk.sent_tokenize(self.text)
        return ' '.join(sentences[:2])
```

- Como tester de software, analiza esta función en busca de casos extremos potenciales y sugiere estrategias de manejo más robustas

```python
def calculatediscount(price, discount):
    if discount > 100:
        raise ValueError('Discount cannot exceed 100%')

    return price * (100 - discount) / 100

# Test cases
print(calculatediscount(100, 105))  # Should raise an exception
```

