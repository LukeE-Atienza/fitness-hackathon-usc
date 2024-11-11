import pandas as pd
import requests 
from flask import Flask


app = Flask(__name__)

@app.route('/')
def food_Call(food_query, grams):
    # Step 1: Search for a product by name and retrieve the first matching product's code
    search_url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={food_query}&search_simple=1&action=process&json=1"

    # Make the search request
    search_response = requests.get(search_url)
    search_data = search_response.json()

    # Check if any products are found
    if search_data['count'] > 0:
        # Get the product code of the first result
        product_code = search_data['products'][0]['code']
        print(f"Found product code for {food_query}: {product_code}")

        # Step 2: Use the product code to retrieve detailed information about the product
        product_url = f"https://world.openfoodfacts.org/api/v0/product/{product_code}.json"
        product_response = requests.get(product_url)
        product_data = product_response.json()

        # Extract nutrient values, initializing missing values with 0
        nutrients = product_data.get('product', {}).get('nutriments', {})

        # Nutrients per 100g
        nutrient_values = {
            "Calories": nutrients.get("energy-kcal_100g", 0),
            "Fats": nutrients.get("fat_100g", 0),
            "Sodium": nutrients.get("sodium_100g", 0),
            "Carbohydrates": nutrients.get("carbohydrates_100g", 0),
            "Protein": nutrients.get("proteins_100g", 0),
        }

        # Adjust nutrients based on the portion size
        portion_values = {k: (v * grams / 100) for k, v in nutrient_values.items()}

        # Display the nutrient information for this portion
        print(pd.DataFrame([portion_values], index=[f"{grams}g of {food_query}"]))

        return portion_values  # Return adjusted nutrient values for this portion
    else:
        print(f"No products found for the food: {food_query}")
        # Return zero values if no product was found
        return {"Calories": 0, "Fats": 0, "Sodium": 0, "Carbohydrates": 0, "Protein": 0}

def food_Eaten():
    eaten_food = []
    print("Enter food items you've eaten. Type 'done' when finished.")
    while True:
        food = input("Food item: ")
        if food.lower() == "done":
            break
        grams = float(input(f"How many grams of {food} did you eat? "))
        eaten_food.append((food, grams))
    return eaten_food

def getData():
    eaten_food = food_Eaten()
    totals = {"Calories": 0, "Fats": 0, "Sodium": 0, "Carbohydrates": 0, "Protein": 0}

    for food_item, grams in eaten_food:
        nutrient_values = food_Call(food_item, grams)

        # Add the nutrient values to the totals
        totals["Calories"] += nutrient_values.get("Calories", 0)
        totals["Fats"] += nutrient_values.get("Fats", 0)
        totals["Sodium"] += nutrient_values.get("Sodium", 0)
        totals["Carbohydrates"] += nutrient_values.get("Carbohydrates", 0)
        totals["Protein"] += nutrient_values.get("Protein", 0)

    # Display the total nutritional information
    print("\nTotal Nutritional Information for All Eaten Food:")
    total_df = pd.DataFrame([totals], index=["Total"])
    print(total_df)

    return totals  # Make sure to return the totals dictionary


 
def calculate_calories_burned(age, height, weight, gender, distance_miles, terrain_difficulty):
    # Estimate calories burned per mile based on gender and weight
    if gender.lower() == 'm':
        calories_per_mile = 0.75 * weight  # For males
    else:
        calories_per_mile = 0.65 * weight  # For females

    # Calculate total calories burned
    calories_burned = calories_per_mile * distance_miles
    if terrain_difficulty >= 1 and terrain_difficulty <= 4:
        calories_burned = calories_burned*1
    elif terrain_difficulty >= 5 and terrain_difficulty <= 7:
        calories_burned = calories_burned*1.4
    else:
        calories_burned = calories_burned*1.6
    return calories_burned

def cal_calc(BMR, total_calories):
    delta_cal = BMR - total_calories
    print(f"Delta Calories: {delta_cal:.2f}")
    
def BMR(age, height, weight, gender):
    weight = weight/2.2
    height = height*2.54
    
    if gender == 'm':
        BMR = (10*weight ) + (6.5*height) - (5*age) +5
    else:
        BMR = (10 * weight) + (6.5 * height) - (5 * age) + 161

    return BMR

def main():
    age = int(input("Enter your age: "))
    height = float(input("Enter your height in inches: "))
    weight = float(input("Enter your weight in pounds: "))
    gender = input("Enter your gender (M/F): ")
    distance_miles = float(input("Enter the distance in miles: "))
    terrain_difficulty = int(input("Enter the terrain difficulty(1-10): "))
    cups_of_water = int(input("Enter the number of cups of water consumed: "))

    # Get total calories from eaten food
    total_calories = getData()  # Now this will return the totals dictionary

    if total_calories:  # Check if total_calories is not None
        # Calculate BMR
        BMR_value = BMR(age, height, weight, gender)  
        print(f"BMR: {BMR_value:.2f}")

        # Calculate calories burned from exercise
        calories_burned = calculate_calories_burned(age, height, weight, gender, distance_miles, terrain_difficulty)
        print(f"Calories burned: {calories_burned:.2f}")

        # Calculate the delta calories (BMR - total calories eaten)
        cal_calc(BMR_value, total_calories["Calories"])  # Pass the total calories to cal_calc
    else:
        print("No calories data found.")


main()

