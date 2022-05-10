from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.String(80))
    id_favorite=db.relationship('Favorite',backref='user',)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "lastname": self.lastname,
            "password": self.password,
            "is_active": self.is_active,
            # do not serialize the password, its a security breach
        }

    @classmethod
    def create(cls, **data):
        #Crear Instancia
        instance=cls(**data)
        if (not isinstance(instance,cls)):
            print("FALLA EL CONSTRUCTOR")
            return None
        #guardar en bdd
        db.session.add(instance)
        try:
            db.session.commit()
            return instance
        except Exception as error:
            print('FALLA BDD')
            db.session.rollback()
            #return None
            raise Exception(error.args)

class item(db.Model):
    __abstract__ = True
    # Here we define db.Columns for the table person
    # Notice that each db.Column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    url= db.Column(db.String(250), nullable=True)
    uid=db.Column(db.Integer,nullable=True)
    description=db.Column(db.String,nullable=True)

class Character(item):
    # Here we define db.Columns for the table address.
    # Notice that each db.Column is also a normal Python instance attribute.
    birth_year = db.Column(db.String(250),nullable=True)
    eye_color = db.Column(db.String(250),nullable=True)
    gender = db.Column(db.String(250),nullable=True)
    height = db.Column(db.Numeric(precision=6, scale=2),nullable=True)
    mass = db.Column(db.Numeric(precision=6, scale=2),nullable=True)
    starship = db.Column(db.String(250),nullable=True)
    vehicles = db.Column(db.String(250),nullable=True)
    characters_favorites=db.relationship("Favorite",backref="character")

    def serialize(self):
        return {
            "id": self.id,
            "uid":self.uid,
            "name": self.name,
            "eye_color":self.eye_color,
            "birth_year":self.birth_year,
            "gender":self.gender,
            "heigth":self.height,
            "mass":self.mass,
            "description":self.description
            }

    def __init__(self,**kwargs):
        for (key, value) in kwargs.items():
            if hasattr(self, key):
                setattr(self, key,  value)
                

    @classmethod
    def create(cls, data):
        #Crear Instancia
        instance=cls(**data)
        if (not isinstance(instance,cls)):
            print("FALLA EL CONSTRUCTOR")
            return None
        #guardar en bdd
        db.session.add(instance)
        try:
            db.session.commit()
            return instance
        except Exception as error:
            print('FALLA BDD')
            db.session.rollback()
            #return None
            raise Exception(error.args)
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return True

class Planet(item):
    diameter=db.Column(db.String(250))
    rotation_period=db.Column(db.String(250))
    orbital_period=db.Column(db.String(250))
    gravity=db.Column(db.String(250))
    population=db.Column(db.String(250))
    climate=db.Column(db.String(250))
    residents=db.Column(db.String(250))
    terrain=db.Column(db.String(250))
    planets_favorites=db.relationship("Favorite",backref="planet")

    def serialize(self):
        return {
            "id": self.id,
            "uid":self.uid,
            "name": self.name,
            "diameter":self.diameter,
            "rotation_period":self.rotation_period,
            "orbital_period":self.orbital_period,
            "description":self.description
            }

    def __init__(self,**kwargs):
        for (key, value) in kwargs.items():
            if hasattr(self, key):
                setattr(self, key,  value)

    @classmethod
    def create(cls, data):
        #Crear Instancia
        instance=cls(**data)
        if (not isinstance(instance,cls)):
            print("FALLA EL CONSTRUCTOR")
            return None
        #guardar en bdd
        db.session.add(instance)
        try:
            db.session.commit()
            return instance
        except Exception as error:
            print('FALLA BDD')
            db.session.rollback()
            #return None
            raise Exception(error.args)
        
    

class Vehicle(item):
    vehicle_class=db.Column(db.String(250))
    manufacturer=db.Column(db.String(250))
    length=db.Column(db.String(250))
    cost_in_credits=db.Column(db.String(250))
    crew=db.Column(db.String(250))
    passengers=db.Column(db.String(250))
    cargo_capacity=db.Column(db.String(250))
    consumable=db.Column(db.String(250))
    pilots=db.Column(db.String(500))
    vehicles_favorites=db.relationship("Favorite",backref="vehicle")
    
    def serialize(self):
        return {
            "id": self.id,
            "uid":self.uid,
            "name": self.name,
            "manufacturer":self.manufacturer,
            "length":self.length,
            "passengers":self.passengers,
            "description":self.description
            }

    def __init__(self,**kwargs):
        for (key, value) in kwargs.items():
            if hasattr(self, key):
                setattr(self, key,  value)

    @classmethod
    def create(cls, data):
        #Crear Instancia
        instance=cls(**data)
        if (not isinstance(instance,cls)):
            print("FALLA EL CONSTRUCTOR")
            return None
        #guardar en bdd
        db.session.add(instance)
        try:
            db.session.commit()
            return instance
        except Exception as error:
            print('FALLA BDD: ', error.args)
            db.session.rollback()
            #return None
            raise Exception(error.args)
        
class Favorite(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    id_user=db.Column(db.Integer,db.ForeignKey('user.id'))
    character_fav=db.Column(db.Integer,db.ForeignKey('character.id'))
    planet_fav=db.Column(db.Integer,db.ForeignKey('planet.id'))
    vehicle_fav=db.Column(db.Integer,db.ForeignKey('vehicle.id'))
    
    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id_user": self.id_user,
            "character_fav": self.character_fav,
            "planet_fav": self.planet_fav,
            "vehicle_fav": self.vehicle_fav
        }  

    @classmethod
    def create(cls, data):
        #Crear Instancia
        instance=cls(**data)
        if (not isinstance(instance,cls)):
            print("FALLA EL CONSTRUCTOR")
            return None
        #guardar en bdd
        db.session.add(instance)
        try:
            db.session.commit()
            return instance
        except Exception as error:
            print('FALLA BDD: ', error.args)
            db.session.rollback()
            #return None
            raise Exception(error.args)