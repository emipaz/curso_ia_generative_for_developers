from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

# Función para calcular los días hasta el próximo cumpleaños
def calcular_dias_faltantes(fecha_nac):
    hoy = datetime.today().date()
    nacimiento = datetime.strptime(fecha_nac, "%Y-%m-%d").date()
    proximo_cumple = nacimiento.replace(year=hoy.year)

    if proximo_cumple < hoy:
        proximo_cumple = proximo_cumple.replace(year=hoy.year + 1)

    dias_faltantes = (proximo_cumple - hoy).days
    return dias_faltantes

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

# Función para calcular la edad
def calcular_edad(fecha_nac):
    hoy = datetime.today().date()
    nacimiento = datetime.strptime(fecha_nac, "%Y-%m-%d").date()
    edad = hoy.year - nacimiento.year
    if (hoy.month, hoy.day) < (nacimiento.month, nacimiento.day):
        edad -= 1
    return edad

@app.route("/resultado", methods=["POST"])
def resultado():
    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    fecha_nac = request.form["fecha_nac"]

    dias_faltantes = calcular_dias_faltantes(fecha_nac)
    edad = calcular_edad(fecha_nac)  # Calculamos la edad

    # Definir el color dependiendo de los días que falten
    if dias_faltantes == 0:
        color = "rainbow"
    elif dias_faltantes <= 7:
        color = "red"
    elif dias_faltantes <= 30:
        color = "orange"
    else:
        color = "green"

    return render_template("resultado.html", 
                           nombre=nombre, 
                           apellido=apellido, 
                           color=color, 
                           dias_faltantes=dias_faltantes, 
                           edad=edad, 
                           es_cumple=(dias_faltantes == 0))


if __name__ == "__main__":
    app.run(debug=True)