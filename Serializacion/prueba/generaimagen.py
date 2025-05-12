from dotenv import load_dotenv
import os
import yaml
import base64
from PIL import Image
from io import BytesIO

def guardar_imagen(image_base64, nombre_archivo, formato):
   
    try:
        image_bytes = base64.b64decode(image_base64)
        image = Image.open(BytesIO(image_bytes))
        image.save(nombre_archivo, format=formato)
        print("Imagen guardada como:", nombre_archivo)
    except Exception as e:
        print("Error al guardar la imagen:", e)
        exit()
    finally:
        return        

if __name__ == "__main__":
    
    if load_dotenv():
        print("cargando script")
        print("creado por:",os.environ.get("AUTOR"))
        try:
            print("cargando API_KEY")
            import openai
            if api_key := os.environ.get("API_KEY", False):
                cliente = openai.OpenAI(api_key=api_key)
                print("API_KEY cargada correctamente")
            else:
                print("No se pudo cargar la API_KEY")
                exit()
        except Exception as e:
            print("Error al cargar la API_KEY:", e)
            exit()
    else:
        print("No se pudo cargar el archivo .env")
        print("Asegúrate de que el archivo .env esté en la misma carpeta que este script.")
        exit()
    # Cargar el archivo de configuración
    if os.path.exists("prompts_imagenes.yaml"):
        with open("prompts_imagenes.yaml", "r", encoding="utf-8") as file:
            imagenes = yaml.safe_load_all(file)
            print("Archivo de prompt cargado correctamente")
            for prompt in imagenes:
                filename = prompt.pop("filename")
                print("Creando :", filename)
                print("con el siguente prompt :", prompt["prompt"])
                formato = prompt.get("output_format", "jpeg")
                # print(formato) 
                try:
                    result = cliente.images.generate(**prompt)
                except Exception as e:
                    print("Error al generar la imagen:", e)
                    continue
                else:
                    if result.data[0].b64_json is None:
                        print("No se generó la imagen")
                        print("Puede ver la imagen en el siguiente enlace:", result.data[0].url)
                        if input("¿Desea abrir la imagen en el navegador? (s/n): ").lower() == "s":
                            import webbrowser
                            webbrowser.open(result.data[0].url)
                        else:
                            continue
                    else:
                        guardar_imagen(result.data[0].b64_json, filename, formato)
    else:
        print("No se encontró el archivo prompts_imagenes.yaml")
        exit()

    
    
    
 