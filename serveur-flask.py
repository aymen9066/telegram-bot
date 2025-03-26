from flask import Flask, render_template, request, jsonify
from module1.storage import *

app = Flask("mini_app_serveur")

@app.route("/info-voiture")
def info_voiture():
    return render_template("info-voiture.html")

@app.route("/submit-car_info", methods=["POST"])
def sumbit_car_info():
    data = request.json
    car_brand, car_model,car_year,km_driven,chat_id,user_id = data.values()
    if chat_id is None:
        raise ValueError("chat_id is None can't insert car information!")
    if car_brand is not None and car_model is not None:
        km_driven = 0 if km_driven is None else km_driven
        brand_id = insert_car_brand(car_brand)
        model_id = insert_car_model(brand_id, car_model, None)
        car_id = insert_car(model_id, km_driven)
        insert_car_listing(car_id, user_id)
        print(f"Voiture d'utilisateur {chat_id} ajouter")
        return jsonify({"message": "Voiture ajoute!"})

app.run(debug=True)