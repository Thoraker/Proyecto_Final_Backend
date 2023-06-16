from flask import request, Blueprint

app = Blueprint("mascotas", __name__, url_prefix="/mascotas")
# Ruta para procesar los datos del formulario reg de mascotas


@app.route("/")
def prueba():
    return {"mensaje": "prueba"}


@app.route("/registro", methods=["POST"])
def procesar_registro():
    data
    nombre = request.form.get("nombre")
    edad = request.form.get("edad")
    especie = request.form.get("especie")
    raza = request.form.get("raza")
    descripcion = request.form.get("descripcion")
    imagen = request.files["imagen"]

    # Aquí puedes realizar cualquier validación o procesamiento adicional de los datos

    # Ejemplo: enviar los datos a la API
    url = "http://localhost:8000/animalitos/registrar"  # Reemplaza con la URL de tu API
    data = {
        "nombre": nombre,
        "edad": edad,
        "especie": especie,
        "raza": raza,
        "descripcion": descripcion,
        # Procesa el archivo de imagen aquí según los requerimientos de tu API
    }
    response = requests.post(url, json=data)

    # Realiza cualquier manejo de la respuesta de la API según tus necesidades

    return "Registro exitoso"  # Puedes redirigir a otra página o mostrar un mensaje de éxito
