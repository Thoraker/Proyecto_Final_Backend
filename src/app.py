import os
from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Pet, Address, Photo, Post
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from flask_cors import CORS
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
CORS(app)
app.url_map.strict_slashes = False

db_key = os.getenv("SECRET_KEY")
db_url = os.getenv("DATABASE_URL")
db_imageshack_key = os.getenv("IMAGESHACK_KEY")

app.config["SECRET_KEY"] = db_key

if db_url is not None:
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url.replace(
        "postgres://", "postgresql://"
    )
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
setup_admin(app)

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return jsonify({"message": "a valid token is missing"})
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            active_user = User.query.filter_by(public_id=data["public_id"]).first()
        except Exception as e:  # Capture the exception
            return jsonify({"message": "token is invalid", "error": str(e)})
        return f(active_user, *args, **kwargs)
    return decorator

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route("/")
def sitemap():
    return generate_sitemap(app)

@app.route("/users", methods=["GET"])
def handle_hello():
    users = User.query.all()
    response_body = jsonify([user.serialize_extended() for user in users])
    return (response_body), 200

@app.route("/pets", methods=["GET"])
def get_available_pets():
    pets = Pet.query.filter(Pet.for_adoption == True).all()
    return jsonify([pet.serialize() for pet in pets])

@app.route("/register", methods=["GET", "POST"])
def register_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data["password"], method="sha256")
    new_user = User(
        public_id=uuid.uuid4(),
        user_name=data["user_name"],
        email=data["email"],
        password=hashed_password,
        first_name=data["first_name"],
        last_name=data["last_name"],
        avatar=data["avatar"],
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"Response": "Registro exitoso", "User": new_user.serialize_extended()})

@app.route("/register", methods=["PUT"])
@token_required
def modify_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data["password"], method="sha256")
    new_user = User(
        public_id=uuid.uuid4(),
        user_name=data["user_name"],
        email=data["email"],
        password=hashed_password,
        first_name=data["first_name"],
        last_name=data["last_name"],
        avatar=data["avatar"],
        donor=data["donor"],
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"Response": "Registro exitoso", "User": new_user.serialize_extended()})

@app.route("/login", methods=["GET", "POST"])
def login_user():
    auth = request.get_json()
    if not auth["user_name"] or not auth["password"]:
        return make_response(
            "could not verify",
            401,
            {"WWW.Authentication": 'Basic realm: "login required"'},
        )
    user = User.query.filter_by(user_name=auth["user_name"]).first()
    if check_password_hash(user.password, auth["password"]):
        token = jwt.encode(
            {
                "public_id": user.public_id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            },
            app.config["SECRET_KEY"],
        )
        print(User.serialize_extended)
        return jsonify(
            {
                "User": user.serialize_extended(),
                "Token": token,
            }
        )
    return make_response(
        "could not verify", 401, {"WWW.Authentication": 'Basic realm: "login required"'}
    )

@app.route("/address", methods=["GET", "POST"])
@token_required
def manage_address(active_user):
    data = request.get_json()
    new_house = Address(
        street=data["street"],
        building_number=data["building_number"],
        department_number=data["department_number"],
        commune=data["commune"],
        region=data["region"],
        has_backyard=data["has_backyard"],
        habitant=active_user.id,
    )
    db.session.add(new_house)
    db.session.commit()
    return jsonify({"Response": "Registro exitoso", "Address": new_house.serialize(), "User": active_user.serialize_address()})

@app.route("/pet", methods=["GET", "POST"])
@token_required
def manage_pet(active_user):
    data = request.get_json()
    new_pet = Pet(
        name=data["name"],
        specie=data["specie"],
        age=data["age"],
        size=data["size"],
        need_backyard=data["need_backyard"],
        for_adoption=data["for_adoption"],
    )
    new_pet.add_owner(active_user)
    db.session.add(new_pet)
    db.session.commit()
    return jsonify({"Response": "Registro exitoso", "Pet": new_pet.serialize(), "User": active_user.serialize_pet()})

@app.route("/photo", methods=["GET", "POST"])
@token_required
def manage_pictures(active_user):
    data = request.get_json()
    new_photo = Photo(url=data["url"], pet_id=data["pet_id"])
    db.session.add(new_photo)
    db.session.commit()
    return jsonify({"Response": "Registro exitoso", "Photo": new_photo.serialize(), "User": active_user.serialize_pet()})

@app.route("/post", methods=["GET", "POST"])
@token_required
def manage_post(active_user):
    if request.method == "POST":
        data = request.get_json()
        new_post = Post(
            reference_post_id=data["reference_post_id"],
            title=data["title"],
            message=data["message"],
            pet_id=data["pet_id"],
            user_id=active_user.id,
        )
        db.session.add(new_post)
        db.session.commit()
        return jsonify({"Response": "Registro exitoso", "Post": new_post.serialize()})

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=PORT, debug=False)
