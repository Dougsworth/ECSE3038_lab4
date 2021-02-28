from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from datetime import datetime

 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://ismkifgu:iVg9eF_UVTI2_azZoxpFVvqshpfs4prs@ziggy.db.elephantsql.com:5432/ismkifgu"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

Profile_DB = {
    "success": True,
    "data": {
        "last_updated": "",
        "username": "Douglas",
        "role": "Engineer",
        "color": "#977FD7"
    }
}

class Tank(db.Model):
  __tablename__ = 'tanks'

  id = db.Column(db.Integer, primary_key = True)
  location = db.Column(db.String(), unique=True, nullable=False)
  lat = db.Column(db.Boolean(), nullable=False)
  long = db.Column(db.Float(), nullable=False)
  percentage_full = db.Column(db.String(), nullable=False)

class TankSchema(ma.SQLAlchemySchema):
  class Meta:
    model = Tank
    fields = ("id", "location", "lat", "long", "percentage_full")

db.init_app(app) 
migrate = Migrate(app, db) 


@app.route("/")
def home():
    return "ECSE3038_LAB4"

##_____________________________________________________________________________________

#GET / Profile


@app.route("/profile", methods=["GET", "POST", "Patch"])
def get_profile():
    if request.method == "GET":
        return jsonify(Profile_DB)

        if request.method == "POST":
            Profile_DB["data"]["username"] = (request.json["username"])
            Profile_DB["data"]["role"] = (request.json["role"])
            Profile_DB["data"]["color"] = (request.json["color"])
            Profile_DB["data"]["last_updated"] = datetime.now()

            return jsonify(Profile_DB)

            if request.method == "PATCH":

                tempDict = request.json
                tempDict["last_updated"] = datetime.now()
                attributes = tempDict.keys()

            for attribute in attributes:
                Profile_DB["data"][attribute] = tempDict[attribute]

    return jsonify(Profile_DB)

##_____________________________________________________________________________________


@app.route("/data")
def get_tanks():
    tanks = Tank.query.all()
    tanks_json = TankSchema(many=True).dump(tanks)
    return jsonify(tanks_json)

@app.route("/data", methods=["POST"])
def add_Tank():
        newTank = Tank(
            location = request.json["location"],
            lat = request.json["lat"],
            long = request.json["long"],
            percentage_full = request.json["percentage_full"]
        )

        db.session.add(newTank)
        db.session.commit()
        return TankSchema().dump(newTank)


@app.route("/data/<int:id>", methods=["PATCH"])
def upd_tank(id):
    tanks = Tank.query.get(id)
    update = request.json
    if "location" in update:
        tanks.location = update["location"]
    if "lat" in update:
        tanks.lat = update["lat"]
    if "long" in update:
        tanks.long = update["long"]
    if "percentage_full" in update:
        tanks.percentage_full = update["percentage_full"]
    
    db.session.commit()
    return TankSchema().dump(tanks)


@app.route("/data/<int:id>", methods=["DELETE"])
def delete_tank(id):
    tanks = Tank.query.get(id)
    db.session.delete(tanks)
    db.session.commit()
    return{"success": True}
    


if __name__ == '__main__':
    app.run(debug=True)