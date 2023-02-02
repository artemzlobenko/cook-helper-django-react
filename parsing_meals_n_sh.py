import requests
import json
import re

alphabet = "abcdefghijklmnopqrstuvwxyz"
ingredients_set = set()
measurements_set = set()
categories_set = set()

with open("meals.txt","w") as f:
    for letter in alphabet:
        response = requests.get(f'https://www.themealdb.com/api/json/v1/1/search.php?f={letter}')
        if response.status_code == 200:
            data = response.content

        data = json.loads(data)
        meals = data['meals']
        if not meals:
            continue
        for meal in meals:
            selected_fields = {
                "strMeal": meal["strMeal"],
                "strCategory": meal["strCategory"],
                "strInstructions": meal["strInstructions"],
                "strMealThumb": meal["strMealThumb"],
                "strYoutube": meal["strYoutube"],
            }

            ingredients_count = 20 # number of ingredients and measures in the meal
            ingredients = {}
            for i in range(1, ingredients_count + 1):
                ingredient = meal.get(f"strIngredient{i}")
                measure = meal.get(f"strMeasure{i}")
                if ingredient and measure:
                    ingredients[ingredient] = measure
                    ingredients_set.add(ingredient)
                    measurements_set.add(measure)

            selected_fields["Ingredients"] = ingredients
            categories_set.add(selected_fields["strCategory"])
            
            f.write("Meal: " + selected_fields["strMeal"] + "\n")
            f.write("Category: "+ selected_fields["strCategory"] + "\n")
            f.write("Image: " + selected_fields["strMealThumb"] + "\n")
            f.write("Youtube video: " + selected_fields["strYoutube"]+ "\n")
            f.write("Instructions: " + selected_fields["strInstructions"] + "\n")

            f.write("Ingredients:\n")
            for ingredient, measure in selected_fields["Ingredients"].items():
                f.write(f"{ingredient}: {measure}\n")
            f.write("\n")

clean_measurements_set = set()
for measure in measurements_set:
    cleaned_measurement = re.sub(re.compile(r'\d+'), '', measure)
    clean_measurements_set.add(cleaned_measurement)
#print("Unique ingredients:", ingredients_set, "\n")
#print("Unique measurements:", measurements_set, "\n")
#print("Unique categories:", categories_set, "\n")
with open("ingr_img_links.txt","w") as f:
    for ingredient in ingredients_set:
        f.write(f"https://www.themealdb.com/images/ingredients/{ingredient}.png \n")
with open("unique_ingr.txt","w") as f:
    for ingredient in ingredients_set:
        f.write(f"{ingredient} \n")
with open("unique_clean_measurem.txt","w") as f:
    for measure in clean_measurements_set:
        f.write(f"{measure} \n")
with open("unique_cat.txt","w") as f:
    for category in categories_set:
        f.write(f"{category} \n")        