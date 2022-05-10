"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
import requests
import json
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Vehicle, Favorite
from sqlalchemy import select
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# @app.route('/user', methods=['GET'])
# def handle_hello():

#     response_body = {
#         "msg": "Hello, this is your GET /user response "
#     }

#     return jsonify(response_body), 200

BASE_URL="https://www.swapi.tech/api"

#POBLAR LISTA DE CHARACTERS

@app.route('/populate-characters',methods=["POST"])
def populate_characters():
    response=requests.get(
        f"{BASE_URL}{'/people'}"
    )
    #cuerpo con todos los personajes
    body=response.json()
    all_characters=[]

    #ciclo recorrer la respuesta y obtener detalles de cada uno    
    for result in body['results']:
        response=requests.get(result['url'])
        body=response.json()

    #se agregan las propiedades de cada character a la lista
        character_insert=body['result']['properties']
        character_insert['uid']=body['result']['uid']
        character_insert['description']=body['result']['description']
        all_characters.append(character_insert)
    instances=[]
    #recorremos la lista con todos los personajes y creamos la instancia
    for character in all_characters:
        instance=Character.create(character)
    #agregamos el OBJETO character a la lista instance
        instances.append(instance)

    return jsonify(list(map(
        lambda inst: inst.serialize(), 
        instances
    ))),200

#POBLAR LISTA DE PLANETS
@app.route('/populate-planets',methods=["POST"])
def populate_planets():
    response=requests.get( f"{BASE_URL}{'/planets'}")
    #cuerpo con todos los planets
    body=response.json()
    all_planets=[]

    #ciclo recorrer la respuesta y obtener detalles de cada uno    
    for result in body['results']:
        response=requests.get(result['url'])
        body=response.json()

    #se agregan las propiedades de cada planet a la lista
        planet_new=body['result']['properties']
        planet_new['uid']=body['result']['uid']
        planet_new['description']=body['result']['description']
        all_planets.append(planet_new)
    instances=[]
    #recorremos la lista con todos los planets y creamos la instancia
    for planet in all_planets:
        instance=Planet.create(planet)
    #agregamos el OBJETO character a la lista instance
        instances.append(instance)

    return jsonify(list(map(
        lambda inst: inst.serialize(), 
        instances
    ))),200


#POBLAR LISTA DE VEHICLES
@app.route('/populate-vehicles',methods=["POST"])
def populate_vehicles():
    response=requests.get( f"{BASE_URL}{'/vehicles'}" )
    #cuerpo con todos los vehicles
    body=response.json()
    all_vehicles=[]

    #ciclo recorrer la respuesta y obtener detalles de cada uno    
    for result in body['results']:
        response=requests.get(result['url'])
        body=response.json()

    #se agregan las propiedades de cada vehicle a la lista
        vehicle_new=body['result']['properties']
        vehicle_new['uid']=body['result']['uid']
        vehicle_new['description']=body['result']['description']        
        all_vehicles.append(vehicle_new)
    instances=[]
    #recorremos la lista con todos los personajes y creamos la instancia
    for vehicle in all_vehicles:
        instance=Vehicle.create(vehicle)
    #agregamos el OBJETO character a la lista instance
        instances.append(instance)

    return jsonify(list(map(
        lambda inst: inst.serialize(), 
        instances
    ))),200

#1. obtener people
@app.route('/characters', methods=['GET'])
def get_all_people():
    characters= Character.query.all()
    list_people= list(map(
        lambda persona: persona.serialize(), characters))
    return jsonify(list_people),200


#2. obtener people/especifica
@app.route('/characters/<int:id>', methods=['GET'])
def more_details_person(id):
    #buscar en base de datos al pesonaje cuya id corresponde a la suya
    character_esp = Character.query.get(id)
    if isinstance(character_esp,Character):
        #enviar vista detallada del personaje 
        dictionary = character_esp.serialize()
        return jsonify(dictionary),200
    return 404

#3. obtener planetas
@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets= Planet.query.all()
    list_planets= list(map(
        lambda planeta: planeta.serialize(), planets))
    return jsonify(list_planets),200


#4. obtener planetas/especificos
@app.route('/planets/<int:id>', methods=['GET'])
def more_details_planet(id):
    #buscar en base de datos del planeta cuya id corresponde a la suya
    planet = Planet.query.get(id)
    if isinstance(planet,Planet):
        #enviar vista detallada del planeta
        dictionary = planet.serialize()
        return jsonify(dictionary),200
    return 404

#5. obtener usuarios
@app.route('/user', methods=['GET'])
def get_all_user():
    users= User.query.all()
    list_users= list(map(
        lambda item: item.serialize(), users))
    return jsonify(list_users),200

#5.1. Postear usuarios
@app.route('/user', methods=['POST'])
def add_one_user():
    dictionary={}
    body = request.json
    decoded_object = json.loads(request.data)
    user = User.create(
        email=body["email"],
        name=body["name"],
        lastname=body["lastname"],
        password=body["password"],
        is_active= body["is_active"],
        )
    dictionary = user.serialize()
    return jsonify(dictionary), 201

#5.2. Delete usuarios
@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user= User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"msg": f"user id:{id} has been deleted succesfully"}),204

#6. obtener favoritos
@app.route('/favorite', methods=['GET'])
def get_favorite():
    favorites= Favorite.query.all()
    list_favorites= list(map(
        lambda item: item.serialize(), favorites))
    return jsonify(list_favorites),200

#6.1. Obtener favoritos/usuario
@app.route('/favorite/user/<int:id>', methods=['GET'])
def get_user_favorite(id):
    all_favorite_one_user= Favorite.query.filter(Favorite.id_user==id).all()
    dictionary_favorite_user=[]
    for general_fav in all_favorite_one_user:
        dictionary_favorite_user.append(general_fav.serialize())
    return jsonify(dictionary_favorite_user),200

#7. postear favorito, planeta por su id
@app.route('/favorite/planet/<int:planet_fav>', methods=['POST'])
def add_new_favorite_planet(planet_fav):
    dictionary={}
    request_body= request.json
    planet_favorite = Favorite.create(
        id_user= request_body['id_user'],
        planet_fav= request_body['planet_fav']
    )
    dictionary = Favorite.serialize()
    return jsonify(dictionary), 201

#8. postear favorito, people por su id
@app.route('/favorite/character/<int:character_fav>', methods=['POST'])
def add_new_favorite_character(character_fav):
    dictionary={}
    request_body= request.json
    planet_favorite = Favorite.create(
        id_user= request_body['id_user'],
        character_fav= request_body['character_fav']
    )
    dictionary = Favorite.serialize()
    return jsonify(dictionary), 201

#9. borrar favorito, planeta por su id
@app.route('/favorite/planet/', methods=['DELETE'])
def delete_fav_planet():
    stmt = select(Favorite).where(Favorite.id_user == "1" and Favorite.planet_fav =="2")
    favorite1= Favorite.query.get(stmt[id])
    db.session.delete(favorite1)
    db.session.commit()
    return jsonify({"msg": f"favorite id:{stmt[id]} has been deleted succesfully"}),204

# def delete_fav_planet(id):
    # id=request.args.get("id", default="", type=str)
    # id=request.args.get("id")
    # id_planet=request.args.get("planet_fav", default="", type=str)
    # print(id_user,id_planet)

    # query2= Favorite.query.filter(Favorite.planet_fav==id_planet).all()
    # stmt = select(Favorite).where(favorite.id_user == "1" and favorite.planet_fav =="2")
    # stmt = select(user_table).where(user_table.c.name == 'spongebob')

    # query = Favorite.query.get((id))
    # query1=db.session.query(Favorite).get((id))
    # if query1 is None:
    #     return jsonify({
    #         "msg": "not found"
    #         }), 404
    # db.session.delete(query1)
    # db.session.commit()
    # return print( { "msg": "favorite id{id_planet}was deleted "}), 204 

#10. borrar favorito, people por su id
@app.route('/favorite/character/<int:character_fav>', methods=['DELETE'])
def delete_fav_character(character_fav):
    id_user=request.args.get("id_user", default="", type=str)
    id_people=request.args.get("character_fav", default="", type=str)
    query = Favorite.query.get((id_user,id_people))
    query1=db.session.query(Favorite).get((id_user,id_people))
    if query is None:
        return jsonify({
            "msg": "not found"
            }), 404
    db.session.delete(query1)
    db.session.commit()
    return print( { "msg": "favorite id{id_people}was deleted "}), 204 
     

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
