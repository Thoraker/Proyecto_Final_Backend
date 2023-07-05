from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

owners_pets = db.Table(
    "owners_pets",
    db.Column("user_id", db.ForeignKey("users.id")),
    db.Column("pet_id", db.ForeignKey("pets.id")),
    db.Column("time_stamp", db.DateTime(timezone=True), default=db.func.now()),
)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True, nullable=False)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(150), unique=False, nullable=False)
    first_name = db.Column(db.String(50), unique=False, nullable=False)
    last_name = db.Column(db.String(50), unique=False, nullable=False)
    avatar = db.Column(db.String(100), unique=False, nullable=True)
    pets = db.relationship("Pet", secondary=owners_pets, back_populates="owners")
    houses = db.relationship("Address", back_populates="home_owner")
    posted = db.relationship("Post", back_populates="poster")

    def __init__(
        self,
        public_id,
        user_name,
        email,
        password,
        first_name,
        last_name,
        avatar,
    ):
        self.public_id = public_id
        self.user_name = user_name
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.avatar = avatar

    def __repr__(self):
        return f'User("{self.id}")'

    def serialize(self):
        return {
            "Usuario": self.user_name,
            "Email": self.email,
            "Avatar": self.avatar,
        }
    
    def serialize_address(self):
        return {
            "id": self.id,
            "Usuario": self.user_name,
            "Email": self.email,
            "Nombre": self.first_name,
            "Apellido": self.last_name,
            "Avatar": self.avatar,

            "Direcciones": [house.serialize() for house in self.houses],
        }
    
    def serialize_pet(self):
        return {
            "id": self.id,
            "Usuario": self.user_name,
            "Email": self.email,
            "Nombre": self.first_name,
            "Apellido": self.last_name,
            "Avatar": self.avatar,
            "Mascotas": [pet.serialize() for pet in self.pets],
        }
    
    def serialize_post(self):
        return {
            "id": self.id,
            "Usuario": self.user_name,
            "Email": self.email,
            "Nombre": self.first_name,
            "Apellido": self.last_name,
            "Avatar": self.avatar,
            "Mensajes": [post.serialize for post in self.posted]
        }

    def serialize_extended(self):
        return {
            "id": self.id,
            "Usuario": self.user_name,
            "Email": self.email,
            "Nombre": self.first_name,
            "Apellido": self.last_name,
            "Avatar": self.avatar,
            "Mascotas": [pet.serialize() for pet in self.pets],
            "Direcciones": [house.serialize() for house in self.houses],
            "Mensajes": [post.serialize() for post in self.posted]
        }

class Pet(db.Model):
    __tablename__ = "pets"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=True)
    specie = db.Column(db.Integer, unique=False, nullable=True)
    age = db.Column(db.String(100), unique=False, nullable=True)
    size = db.Column(db.Integer, unique=False, nullable=True)
    need_backyard = db.Column(db.Boolean, unique=False, nullable=True)
    for_adoption = db.Column(db.Boolean, unique=False, nullable=True)
    owners = db.relationship("User", secondary=owners_pets, back_populates="pets")
    photos = db.relationship("Photo", back_populates="pets")
    posts = db.relationship("Post", back_populates="anser")

    def __init__(self, name, specie, age, size, need_backyard, for_adoption):
        self.name = name
        self.specie = specie
        self.age = age
        self.size = size
        self.need_backyard = need_backyard
        self.for_adoption = for_adoption

    def __repr__(self):
        return f'Pet("{self.name}","{self.specie})'

    def serialize(self):
        return {
            "id": self.id,
            "Nombre": self.name,
            "Especie": self.specie,
            "Tamano": self.size,
            "Edad": self.age,
            "Necesita_Patio": self.need_backyard,
            "En_Adopcion": self.for_adoption,
            "Fotos": [photo.serialize() for photo in self.photos],
            "Dueño": [owner.serialize() for owner in self.owners],
            "Mensajes": [post.serialize() for post in self.posts],
        }
    
    def add_owner(self, user):
        self.owners.append(user)

class Address(db.Model):
    __tablename__ = "addresses"
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(100), unique=False, nullable=False)
    building_number = db.Column(db.Integer, unique=False, nullable=False)
    department_number = db.Column(db.Integer, unique=False, nullable=True)
    commune = db.Column(db.String(100), unique=False, nullable=False)
    region = db.Column(db.Integer, unique=False, nullable=True)
    has_backyard = db.Column(db.Boolean, unique=False, nullable=True)
    habitant = db.Column(db.Integer, db.ForeignKey("users.id"), unique=False, nullable=True)
    home_owner = db.relationship("User", back_populates="houses")

    def __init__(
        self,
        street,
        building_number,
        department_number,
        commune,
        region,
        has_backyard,
        habitant,
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
            "id": self.id,
            "Calle": self.street,
            "Numero": self.building_number,
            "Departamento": self.department_number,
            "Comuna": self.commune,
            "Region": self.region,
            "Tiene_Patio": self.has_backyard,
        }

class Photo(db.Model):
    __tablename__ = "photos"
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200), unique=True, nullable=False)
    pet_id = db.Column(db.Integer, db.ForeignKey("pets.id"), unique=False, nullable=True)
    pets = db.relationship("Pet", back_populates="photos")

    def __init__(self, url, pet_id):
        self.url = url
        self.pet_id = pet_id

    def __repr__(self):
        return f'Photo("{self.url}")'

    def serialize(self):
        return {"id": self.id, "url": self.url}

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    reference_post_id = db.Column(db.Integer, unique=False, nullable=True)
    title = db.Column(db.String(100), unique=False, nullable=False)
    message = db.Column(db.String(500), unique=False, nullable=False)
    pet_id = db.Column(db.Integer, db.ForeignKey("pets.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    anser = db.relationship("Pet", back_populates="posts")
    poster = db.relationship("User", back_populates="posted")

    def __init__(self, reference_post_id, title, message, pet_id, user_id):
        self.reference_post_id = reference_post_id
        self.title = title
        self.message = message
        self.pet_id = pet_id
        self.user_id = user_id

    def __repr__(self):
        return f'Post("{self.title}","{self.pet_id}, "{self.user_id}")'

    def serialize(self):
        return {
            "id": self.id,
            "Mensaje_Origen": self.reference_post_id,
            "Titulo": self.title,
            "Mensaje": self.message,
            "Id_Mascota": self.pet_id,
            "Id_Usuario": self.user_id,
        }