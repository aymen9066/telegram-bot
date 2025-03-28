from flask import Flask, render_template, request, jsonify

from module1.join import Voiture
from module1.storage import *

app = Flask("mini_app_serveur")

@app.route("/info-voiture")
def info_voiture():
    return render_template("info-voiture.html")

@app.route("/submit-car-details", methods=["POST"])
def sumbit_car_info():
    data = request.json
    print(data)
    car_brand, car_model,car_year,km_driven,chat_id,user_id = data.values()
    if chat_id == '':
        raise ValueError("chat_id is None can't insert car information!")
    if car_brand != '' and car_model != '':
        if not Voiture.is_production_year_valid(int(car_year)):
            return jsonify({"message": "Anne de production invalide!"})
        km_driven = 0 if km_driven == '' else km_driven
        brand_id = insert_car_brand(car_brand)
        model_id = insert_car_model(brand_id, car_model, int(car_year))
        car_id = insert_car(model_id, km_driven)
        insert_car_listing(car_id, user_id)
        return jsonify({"message": "Voiture ajoute!"})
    return jsonify({"message": "peut pas ajouter une voiture vide..."})

app.run(debug=True)