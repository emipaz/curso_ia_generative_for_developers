from dotenv import load_dotenv
import os
import yaml
import base64
from PIL import Image
from io import BytesIO
import webbrowser
import sys

class Entorno:
    def __init__(self, archivo_env=".env"):
        self.archivo_env = archivo_env
        self.api_key = None
        self.autor = None

    def cargar(self):
        if load_dotenv(self.archivo_env):
            self.api_key = os.environ.get("API_KEY")
            self.autor = os.environ.get("AUTOR")
            if self.api_key:
                print("API_KEY cargada correctamente")
                return True
            else:
                print("No se pudo cargar la API_KEY")
        else:
            print("No se pudo cargar el archivo .env")
        return False

class GeneradorImagenes:
    def __init__(self, api_key):
        import openai
        self.cliente = openai.OpenAI(api_key=api_key)

    def generar(self, prompt):
        try:
            return self.cliente.images.generate(**prompt)
        except Exception as e:
            print("Error al generar la imagen:", e)
            return None

    @staticmethod
    def guardar_imagen(image_base64, nombre_archivo, formato="jpeg"):
        try:
            image_bytes = base64.b64decode(image_base64)
            image = Image.open(BytesIO(image_bytes))
            image.save(nombre_archivo, format=formato)
            print("Imagen guardada como:", nombre_archivo)
        except Exception as e:
            print("Error al guardar la imagen:", e)

class ScriptImagenes:
    def __init__(self, archivo_yaml="prompts_imagenes.yaml"):
        self.archivo_yaml = archivo_yaml
        self.entorno = Entorno()
        self.generador = None

    def ejecutar(self):
        print("Cargando script...")

        if not self.entorno.cargar():
            print("Error al cargar configuración.")
            return

        print("Creado por:", self.entorno.autor)
        self.generador = GeneradorImagenes(self.entorno.api_key)

        if not os.path.exists(self.archivo_yaml):
            print(f"No se encontró el archivo {self.archivo_yaml}")
            return

        with open(self.archivo_yaml, "r", encoding="utf-8") as file:
            imagenes = yaml.safe_load_all(file)
            print("Archivo de prompt cargado correctamente")

            for prompt in imagenes:
                self.procesar_prompt(prompt)

    def procesar_prompt(self, prompt):
        filename = prompt.pop("filename")
        formato = prompt.get("output_format", "jpeg")

        print(f"Creando: {filename}")
        print(f"Con el siguiente prompt: {prompt['prompt']}")

        resultado = self.generador.generar(prompt)
        if not resultado:
            return

        dato = resultado.data[0]

        if dato.b64_json:
            self.generador.guardar_imagen(dato.b64_json, filename, formato)
        else:
            print("No se generó la imagen.")
            print("Puede ver la imagen en el siguiente enlace:", dato.url)
            if input("¿Desea abrir la imagen en el navegador? (s/n): ").lower() == "s":
                webbrowser.open(dato.url)

if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) < 2:
        print("Uso: python generar_imagenes_poo.py <archivo_yaml>")
        archivo_yaml = None
    else:
        archivo_yaml = sys.argv[1] 
    # sys.argv[0] = "generar_imagenes_poo.py"
    script = ScriptImagenes(archivo_yaml=archivo_yaml)
    script.ejecutar()
