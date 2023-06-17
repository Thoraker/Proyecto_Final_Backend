"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, make_response, Blueprint
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Pet, Address
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import datetime
from functools import wraps
from routes.mascotas import mascotas

# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_key = os.getenv("SECRET_KEY")
db_url = os.getenv("DATABASE_URL")

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
CORS(app)
setup_admin(app)
app.register_blueprint(mascotas)


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        if "x-access-tokens" in request.headers:
            token = request.headers["x-access-tokens"]

        if not token:
            return jsonify({"message": "a valid token is missing"})

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"])
            current_user = User.query.filter_by(public_id=data["public_id"]).first()
        except:
            return jsonify({"message": "token is invalid"})

        return f(current_user, *args, **kwargs)

    return decorator


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# generate sitemap with all your endpoints
@app.route("/")
def sitemap():
    return generate_sitemap(app)


@app.route("/user", methods=["GET"])
def handle_hello():
    response_body = {"msg": "Hello, this is your GET /user response "}

    return jsonify(response_body), 200


@app.route("/register", methods=["GET", "POST"])
def signup_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data["password"], method="sha256")

    new_user = User(
        public_id=uuid.uuid4(),
        user_name=data["user_name"],
        email=data["email"],
        password=hashed_password,
        first_name=data["first_name"],
        last_name=data["last_name"],
        donor=data["donor"],
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "registered successfully"})


@app.route("/login", methods=["GET", "POST"])
def login_user():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response(
            "could not verify",
            401,
            {"WWW.Authentication": 'Basic realm: "login required"'},
        )

    user = User.query.filter_by(user_name=auth.username).first()

    if check_password_hash(user.password, auth.password):
        token = jwt.encode(
            {
                "public_id": user.public_id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            },
            app.config["SECRET_KEY"],
        )
        return jsonify({"token": token})

    return make_response(
        "could not verify", 401, {"WWW.Authentication": 'Basic realm: "login required"'}
    )


# this only runs if `$ python src/app.py` is executed
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=PORT, debug=False)
