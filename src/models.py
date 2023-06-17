from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


owners_pets = db.Table(
    "owners_pets",
    db.Column("user_id", db.ForeignKey("users.id")),
    db.Column("pet_id", db.ForeignKey("pets.id")),
)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True, nullable=False)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=False, nullable=False)
    first_name = db.Column(db.String(50), unique=False, nullable=False)
    last_name = db.Column(db.String(50), unique=False, nullable=False)
    donor = db.Column(db.Boolean(), unique=False, nullable=False)

    owner = db.relationship("Pet", secondary=owners_pets, back_populates="pet")
    house = db.relationship("Address", back_populates="home_owner")

    def __init__(
        self, public_id, user_name, email, password, first_name, last_name, donor
    ):
        self.public_id = public_id
        self.user_name = user_name
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.donor = donor

    def __repr__(self):
        return f'User("{self.user_name}")'

    def serialize(self):
        return {
            "Usuario": self.user_name,
            "Email": self.email,
            "Dador": self.giver,
        }


class Pet(db.Model):
    __tablename__ = "pets"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=True)
    specie = db.Column(db.Integer, unique=False, nullable=True)
    age = db.Column(db.Integer, unique=False, nullable=True)
    size = db.Column(db.Integer, unique=False, nullable=True)
    need_backyard = db.Column(db.Boolean, unique=False, nullable=True)
    id_origin = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    id_owner = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    pet = db.relationship("User", secondary=owners_pets, back_populates="owner")

    def __init__(self, name, specie, age, size, need_backyard= True, id_origin=None, id_actual=None):
        self.name = name
        self.age = age
        self.specie = specie
        self.size = size
        self.need_backyard = need_backyard
        self.id_origin = id_origin
        self.id_actual = id_actual

    def __repr__(self):
        return f'Pet("{self.name}","{self.specie})'

    def serialize(self):
        return {
            "Nombre": self.name,
            "Especie": self.specie,
            "Tamaño": self.size,
            "Necesita Patio": self.need_backyard,
            "Entregado por": self.id_origin,
        }


class Address(db.Model):
    __tablename__ = "addresses"
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(30), unique=False, nullable=False)
    building_number = db.Column(db.Integer, unique=False, nullable=False)
    department_number = db.Column(db.Integer, unique=False, nullable=False)
    commune = db.Column(db.Integer, unique=False, nullable=False)
    region = db.Column(db.Integer, unique=False, nullable=True)
    has_backyard = db.Column(db.Boolean, unique=False, nullable=True)
    habitant = db.Column(
        db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False
    )

    home_owner = db.relationship("User", back_populates="house")

    def __init__(
        self, street, building_number, department_number, commune, region, has_backyard
    ):
        self.street = street
        self.building_number = building_number
        self.department_number = department_number
        self.commune = commune
        self.region = region
        self.has_backyard = has_backyard

    def __rep__(self):
        return f'Address("{self.street}","{self.building_number}","{self.commune}")'

    def serialize(self):
        return {
            "Calle": self.street,
            "Numero": self.building_number,
            "Departamento": self.department_number,
            "Comuna": self.commune,
            "Región": self.region,
            "Tiene Patio": self.has_backyard,
        }
