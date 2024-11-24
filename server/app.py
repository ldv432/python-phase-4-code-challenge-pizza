#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

class Pizzas(Resource):
    def get(self):
        try:
            return [pizza.to_dict() for pizza in Pizza.query], 200
        except Exception as e:
            return {'error': str(e)}, 400
        
api.add_resource(Pizzas, '/pizzas')



class Restaurants(Resource):
    def get(self):
        try:
            # import ipdb; ipdb.set_trace()
            return [restaurant.to_dict(only=('id','name', 'address')) for restaurant in Restaurant.query], 200
        except Exception as e:
            return {'error': str(e)}, 400
        
api.add_resource(Restaurants, '/restaurants')
        
class RestaurantById(Resource):
    def get(self, id):
        try:
            restaurant = db.session.get(Restaurant, id)
            if not restaurant:
                return make_response({'error': "Restaurant not found"}, 404)
            return make_response(restaurant.to_dict(), 200)
        except Exception as e:
            return {'error', str(e)}, 500
    
    def delete(self, id):
        try:
            restaurant = db.session.get(Restaurant, id)
            if not restaurant:
                return make_response({'error': 'Restaurant not found'}, 404)
            db.session.delete(restaurant)
            db.session.commit()
            return make_response({"message": "Restaurant deleted successfully"}, 204)
        except Exception as e:
            return {"error": str(e)}, 500
        
api.add_resource(RestaurantById, '/restaurants/<int:id>')

class RestaurantPizzas(Resource):
    def post(self):
        try:
            data = request.json
            restaurantpizza = RestaurantPizza(price=data.get("price"), pizza_id=data.get("pizza_id"), restaurant_id=data.get("restaurant_id"))
            db.session.add(restaurantpizza)
            db.session.commit()
            return make_response(restaurantpizza.to_dict(), 201)
        except Exception as e:
            return {'errors': ['validation errors']}, 400

api.add_resource(RestaurantPizzas, '/restaurant_pizzas')



if __name__ == "__main__":
    app.run(port=5555, debug=True)
