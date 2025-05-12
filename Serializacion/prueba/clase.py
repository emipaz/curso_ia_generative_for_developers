from dotenv import load_dotenv
import os
import openai    
import yaml
import pickle

if load_dotenv():
    print(os.environ.get("AUTOR"))
    cliente = openai.OpenAI(api_key=os.environ.get("API_KEY"))

with open("clase.yaml", "r", encoding="utf-8") as file:
    datos = yaml.safe_load_all(file)
    for dato in datos:
        print(dato)
        archivo = dato.pop("filename")
        print(archivo)
        result = cliente.images.generate(**dato)
        pickle.dump(result, open("datos.plk", "wb"))
        print(result)
        
            