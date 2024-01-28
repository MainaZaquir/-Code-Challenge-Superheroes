from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

# The routes

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    heroes_data = [{"id": hero.id, "name": hero.name, "super_name": hero.super_name} for hero in heroes]
    return jsonify(heroes_data)

@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero_by_id(id):
    hero = Hero.query.get(id)
    if hero:
        hero_data = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
            "powers": [{"id": p.id, "name": p.name, "description": p.description} for p in hero.powers]
        }
        return jsonify(hero_data)
    else:
        return jsonify({"error": "Hero not found"}), 404

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    powers_data = [{"id": power.id, "name": power.name, "description": power.description} for power in powers]
    return jsonify(powers_data)

@app.route('/powers/<int:id>', methods=['GET'])
def get_power_by_id(id):
    power = Power.query.get(id)
    if power:
        power_data = {"id": power.id, "name": power.name, "description": power.description}
        return jsonify(power_data)
    else:
        return jsonify({"error": "Power not found"}), 404

@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if power:
        data = request.get_json()
        if 'description' in data:
            new_description = data['description']
            power.description = new_description

            try:
                db.session.commit()
                return jsonify({"id": power.id, "name": power.name, "description": power.description})
            except:
                return jsonify({"errors": ["validation errors"]}), 400
        else:
            return jsonify({"error": "Missing 'description' in request body"}), 400
    else:
        return jsonify({"error": "Power not found"}), 404

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    if all(key in data for key in ['strength', 'power_id', 'hero_id']):
        strength = data['strength']
        power_id = data['power_id']
        hero_id = data['hero_id']

        hero = Hero.query.get(hero_id)
        power = Power.query.get(power_id)

        if hero and power:
            hero_power = HeroPower(hero=hero, power=power, strength=strength)

            try:
                db.session.add(hero_power)
                db.session.commit()
                hero_data = {
                    "id": hero.id,
                    "name": hero.name,
                    "super_name": hero.super_name,
                    "powers": [{"id": p.id, "name": p.name, "description": p.description} for p in hero.powers]
                }
                return jsonify(hero_data), 201
            except:
                return jsonify({"errors": ["validation errors"]}), 400
        else:
            return jsonify({"error": "Hero or Power not found"}), 404
    else:
        return jsonify({"error": "Missing required fields in request body"}), 400

@app.route('/')
def home():
    return ''

if __name__ == '__main__':
    app.run(port=5555)


migrate = Migrate(app, db)