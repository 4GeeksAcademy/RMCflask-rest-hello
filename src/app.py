import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Usuario, Planeta, Vehiculo, Persona, Favorito

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([usuario.serialize() for usuario in usuarios]), 200

@app.route('/usuarios/<int:id>', methods=['GET'])
def get_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify(usuario.serialize()), 200

@app.route('/usuarios', methods=['POST'])
def create_usuario():
    data = request.json
    new_usuario = Usuario(
        username=data['username'],
        password=data['password'],
        full_name=data['full_name'],
        email=data['email']
    )
    db.session.add(new_usuario)
    db.session.commit()
    return jsonify(new_usuario.serialize()), 201

@app.route('/usuarios/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({"message": "Usuario eliminado"}), 200

@app.route('/planetas', methods=['GET'])
def get_planetas():
    planetas = Planeta.query.all()
    return jsonify([planeta.serialize() for planeta in planetas]), 200

@app.route('/planetas/<int:id>', methods=['GET'])
def get_planeta(id):
    planeta = Planeta.query.get(id)
    if not planeta:
        return jsonify({"error": "Planeta no encontrado"}), 404
    return jsonify(planeta.serialize()), 200

@app.route('/vehiculos', methods=['GET'])
def get_vehiculos():
    vehiculos = Vehiculo.query.all()
    return jsonify([vehiculo.serialize() for vehiculo in vehiculos]), 200

@app.route('/vehiculos/<int:id>', methods=['GET'])
def get_vehiculo(id):
    vehiculo = Vehiculo.query.get(id)
    if not vehiculo:
        return jsonify({"error": "Vehículo no encontrado"}), 404
    return jsonify(vehiculo.serialize()), 200

@app.route('/personas', methods=['GET'])
def get_personas():
    personas = Persona.query.all()
    return jsonify([persona.serialize() for persona in personas]), 200

@app.route('/personas/<int:id>', methods=['GET'])
def get_persona(id):
    persona = Persona.query.get(id)
    if not persona:
        return jsonify({"error": "Persona no encontrada"}), 404
    return jsonify(persona.serialize()), 200

@app.route('/favoritos', methods=['GET'])
def get_favoritos():
    favoritos = Favorito.query.all()
    return jsonify([favorito.serialize() for favorito in favoritos]), 200

@app.route('/favoritos', methods=['POST'])
def create_favorito():
    data = request.json
    new_favorito = Favorito(
        usuario_id=data['usuario_id'],
        persona_id=data.get('persona_id'),
        vehiculo_id=data.get('vehiculo_id'),
        planeta_id=data.get('planeta_id')
    )
    db.session.add(new_favorito)
    db.session.commit()
    return jsonify(new_favorito.serialize()), 201

@app.route('/favoritos/<int:id>', methods=['DELETE'])
def delete_favorito(id):
    favorito = Favorito.query.get(id)
    if not favorito:
        return jsonify({"error": "Favorito no encontrado"}), 404
    db.session.delete(favorito)
    db.session.commit()
    return jsonify({"message": "Favorito eliminado"}), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
