from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import requests
import random

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}



@app.route("/")
def home():
    return render_template("index.html")
    

## HTTP GET - Read Record
@app.route("/random")
def get_random_cafe():
    cafes = db.session.query(Cafe).all()
    random_cafe = random.choice(cafes)
    # return jsonify(cafe={
    #     id=random_cafe.id, 
    #     name=random_cafe.name, 
    #     map_url=random_cafe.map_url, 
    #     img_url=random_cafe.img_url, 
    #     location=random_cafe.location,
    #     seats=random_cafe.seats, 
    #     has_toilet=random_cafe.has_toilet, 
    #     has_wifi=random_cafe.has_wifi, 
    #     has_sockets=random_cafe.has_sockets, 
    #     can_take_calls=random_cafe.can_take_calls,
    #     coffee_price=random_cafe.coffee_price})

    #Simply convert the random_cafe data record to a dictionary of key-value pairs. 
    return jsonify(cafe=random_cafe.to_dict())


@app.route("/all")
def all():
    cafes = db.session.query(Cafe).all()
    data = []
    for cafe in cafes:
        cafe_dict = cafe.to_dict()
        data.append(cafe_dict)

    return jsonify(cafes=data)

@app.route("/search")
def get_cafe_at_location():
    query_location = request.args.get("loc")
    cafe = db.session.query(Cafe).filter_by(location=query_location).first()
    if cafe:
        return jsonify(cafe=cafe.to_dict())
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."})


## HTTP POST - Create Record
@app.route("/add", methods=["POST"])
def add():
        name = request.form.get("name")
        map_url = request.form.get("map_url")
        img_url = request.form.get("img_url")
        location = request.form.get("location")
        seats = request.form.get("seats")
        has_toilet =  bool(request.form.get("has_toilet"))
        has_wifi = bool(request.form.get("has_wifi"))
        has_sockets = bool(request.form.get("has_sockets"))
        can_take_calls = bool(request.form.get("can_take_calls"))
        coffee_price = request.form.get("coffee_price")
        data = Cafe(name=name, map_url=map_url, img_url=img_url, location=location, seats=seats, has_toilet=has_toilet, has_wifi=has_wifi, has_sockets=has_sockets, can_take_calls=can_take_calls, coffee_price=coffee_price)   
        db.session.add(data) 
        db.session.commit()
        return jsonify(response={"success": "Successfully added the new cafe."})


## HTTP PUT/PATCH - Update Record
@app.route("/update-price/<cafe_id>", methods=["GET","PATCH"])
def patch(cafe_id):
    cafe_to_update = Cafe.query.get(cafe_id)
    coffee_price = request.args.get("new_price")
    if cafe_to_update:
        cafe_to_update.coffee_price = coffee_price
        db.session.commit()  
        return jsonify(response={"success": "Successfully updated the coffee price."}), 200
    else:
         return jsonify(error={"Not Found": "Sorry, we don't have a cafe with that id."}), 404
## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
