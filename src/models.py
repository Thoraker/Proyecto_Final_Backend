from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


owners_pets = db.Table(
    "owners_pets",
    db.Column("user_id", db.ForeignKey("users.id")),
    db.Column("pet_id", db.ForeignKey("pets.id")),
    db.Column("time_stamp", db.DateTime(timezone=True), default=db.func.now())
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
    avatar = db.Column(db.String(100), unique=False, nullable=True)
    donor = db.Column(db.Boolean(), unique=False, nullable=False)

    pets = db.relationship("Pet", secondary=owners_pets, back_populates="owners")
    houses = db.relationship("Address", back_populates="home_owner")
    posted = db.relationship("Post", back_populates="poster")

    def __init__(self, public_id, user_name, email, password, first_name, last_name, avatar, donor):
        self.public_id = public_id
        self.user_name = user_name
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.avatar = avatar
        self.donor = donor

    def __repr__(self):
        return f'User("{self.id}")'
    
    def serialize(self):
        return {
            "Usuario": self.user_name,
            "Email": self.email,
            "Avatar": self.avatar,
        }

    def serialize_extended(self):
        return {
            "Usuario": self.user_name,
            "Email": self.email,
            "Avatar": self.avatar,
            "Dador": self.donor,
            "Mascotas": [pet.serialize() for pet in self.pets],
            "Direcciones": [house.serialize() for house in self.houses],
        }
    
    def get_all_users(self):
        return self._users


class Pet(db.Model):
    __tablename__ = "pets"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=True)
    specie = db.Column(db.Integer, unique=False, nullable=True)
    age = db.Column(db.String(20), unique=False, nullable=True)
    size = db.Column(db.Integer, unique=False, nullable=True)
    photo_url = db.Column(db.String(100), unique=False, nullable=True)
    need_backyard = db.Column(db.Boolean, unique=False, nullable=True)

    owners = db.relationship("User", secondary=owners_pets, back_populates="pets")
    photos = db.relationship("Portfolio", back_populates="pets")
    posts = db.relationship("Post", back_populates="anser")

    def __init__(self, name, specie, age, size, photo_url, need_backyard):
        self.name = name
        self.specie = specie
        self.age = age
        self.size = size
        self.photo_url = photo_url
        self.need_backyard = need_backyard

    def __repr__(self):
        return f'Pet("{self.name}","{self.specie})'

    def serialize(self):
        return {
            "Nombre": self.name,
            "Especie": self.specie,
            "Tamano": self.size,
            "Necesita Patio": self.need_backyard,
        }
    
    def add_owner(self, user):
        self.owners.append(user)


class Address(db.Model):
    __tablename__ = "addresses"
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(30), unique=False, nullable=False)
    building_number = db.Column(db.Integer, unique=False, nullable=False)
    department_number = db.Column(db.Integer, unique=False, nullable=True)
    commune = db.Column(db.Integer, unique=False, nullable=False)
    region = db.Column(db.Integer, unique=False, nullable=True)
    has_backyard = db.Column(db.Boolean, unique=False, nullable=True)
    habitant = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=True)

    home_owner = db.relationship("User", back_populates="houses")

    def __init__(
        self, street, building_number, department_number, commune, region, has_backyard, habitant
    ):
        self.street = street
        self.building_number = building_number
        self.department_number = department_number
        self.commune = commune
        self.region = region
        self.has_backyard = has_backyard
        self.habitant = habitant

    def __rep__(self):
        return f'Address("{self.street}","{self.building_number}","{self.commune}")'

    def serialize(self):
        return {
            "Calle": self.street,
            "Numero": self.building_number,
            "Departamento": self.department_number,
            "Comuna": self.commune,
            "Region": self.region,
            "Tiene Patio": self.has_backyard,
        }
    
    
class Portfolio(db.Model):
    __tablename__ = "portfolios"
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(100), unique=True, nullable=False)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'))

    pets = db.relationship("Pet", back_populates="photos")

    def __init__(self, url, pet_id):
        self.url = url
        self.pet_id = pet_id

    def __repr__(self):
        return f'Portfolio("{self.url}","{self.pet_id}")'
    

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    reference_post_id = db.Column(db.Integer, unique=False, nullable=True)
    header = db.Column(db.String(50), unique=False, nullable=False)
    body = db.Column(db.String(500), unique=False, nullable=False)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    anser = db.relationship("Pet", back_populates="posts")
    poster = db.relationship("User", back_populates="posted")
    
    def __init__(self, reference_post_id, header, body, pet_id, user_id):
        self.reference_post_id = reference_post_id
        self.header = header
        self.body = body
        self.pet_id = pet_id
        self.user_id = user_id

    def __repr__(self):
        return f'Post("{self.header}","{self.pet_id}, "{self.user_id}")'
    
    def serialize(self):
        return {
            "reference_post_id": self.reference_post_id,
            "header": self.header,
            "body": self.body,
            "pet_id": self.pet_id,
            "user_id": self.user_id,
        }