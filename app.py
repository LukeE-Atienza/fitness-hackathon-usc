from flask import Flask, render_template, request, jsonify
from utils import food_Call, calculate_calories_burned, BMR  # Import functions

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_food_data", methods=["POST"])
def get_food_data():
    # Retrieve JSON data from the request
    data = request.get_json()
    food_query = data.get("food_query")
    grams = data.get("grams")

    # Call the food_Call function with the received data
    nutrient_values = food_Call(food_query, grams)

    # Return the nutrient values as a JSON response
    return jsonify(nutrient_values)

@app.route("/calculate_burned_calories", methods=["POST"])
def calculate_burned_calories():
    # Retrieve JSON data from the request
    data = request.get_json()
    age = data.get("age")
    height = data.get("height")
    weight = data.get("weight")
    gender = data.get("gender")
    distance = data.get("distance")
    difficulty = data.get("difficulty")

    # Call the calculate_calories_burned function with the received data
    calories_burned = calculate_calories_burned(age, height, weight, gender, distance, difficulty)

    # Return the calculated calories burned as a JSON response
    return jsonify({"calories_burned": calories_burned})


if __name__ == "__main__":
    app.run(debug=True)
