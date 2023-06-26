from flask import request, Blueprint, jsonify
from models import Pet, db


mascotas = Blueprint("mascotas", __name__, url_prefix="/mascotas")
# Ruta para procesar los datos del formulario reg de mascotas


@mascotas.route("/")
def prueba():
    return {"mensaje": "prueba"}


@mascotas.route("/mascotas", methods=["GET", "POST"])
def form_pets():
    if request.method == "POST":
        data = request.get_json()
        new_pet = Pet(
            name=data["nombre"],
            specie=data["especie"],
            age=data["edad"],
            size=data["tamano"],

        )
        db.session.add(new_pet)
        db.session.commit()

        return jsonify({"mensaje": "Registro de mascota exitoso"}), 201

    if request.method == "GET":
        return {"mensaje": "Form Data Example"}


# @mascotas.route("/registro", methods=["POST"])
# def procesar_registro():
#     data = request.get_jason()

#
#     #    Guardar la imagen en el servidor
#     # filename = secure_filename(image.filename)
#     # image.save(filename)

#     new_register = Pet_Register(
#         name=name,
#         age=age,
#         specie=especie,
#         description=description

#   


# # Ejemplo: enviar los datos a la API
# url = "http://localhost:8000/animalitos/registrar"  # Reemplaza con la URL de tu API
# data = {
#     "nombre": nombre,
#     "edad": edad,
#     "especie": especie,
#     "raza": raza,
#     "descripcion": descripcion,
#     # Procesa el archivo de imagen aquí según los requerimientos de tu API
# }
# response = requests.post(url, json=data)

# # Realiza cualquier manejo de la respuesta de la API según tus necesidades

# return "Registro exitoso"  # Puedes redirigir a otra página o mostrar un mensaje de éxito
