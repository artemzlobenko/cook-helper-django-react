import json
import re
from enum import Enum
from typing import Optional

import requests


class Units(Enum):
    PIECE = 0,
    MILLILITERS = 1,
    GRAMS = 2

PARTS = [
        'pinch',
        'slice',
        'handful',
        'drizzle',
        'inch',
        'part',
        'sprinking',
        'pod',
        'zest',
        'knob',
        'thumb',
        'strip',
        'drop',
        'drops',
        'halved',
        'splash',
        'splash', # don't delete
    ]

WHOLE_PIECES = [
                    'small',
                    'medium',
                    'large',
                    'bulb',
                    'whole',
                    'sliced',
                    'chopped',
                    'piece',
                    'can',
                    'fry',
                    'crush',
                    'dash',
                    'leave',
                    'cut',
                    'glaze',
                    'bone',
                    'florets',
                    'clove',
                    'bottle',
                    'bunch',
                    'juice',
                    'white',
                    'jar',
                    'qt',
                    'skinned',
                    'dried',
                    'tin',
                    'tail',
                    'head',
                    'mashed',
                    'packet',
                    'ground',
                    'boiled',
                    'bag',
                    'red',
                    'yolk',
                    'stick',
                    'tub',
                    'pot',
                    'beat',
                    'sprig',
                    'skin',
                    'diced',
                    'rinsed',
                    'shank',
                    'package',
                    'marble',
                    'fillets',
                    'shaved',
                    'minced',
                    'bashed',
                    'steamed',
                    'seperated',
                    'grated',
                    'top',
                    'ancho',
    ]

NON_MEASURABLE = [
        'to taste',
        'garnish',
        'topping',
        'free-range',
        'to serve',
        'spinkling',
        'greasing',
        'brushing',
    ]

ALPHABET = "abcdefghijklmnopqrstuvwxyz"


ingredients_set = set()
measurements_set = set()
categories_set = set()

with open("meals.txt","w") as f:
    for letter in ALPHABET:
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
            
            #f.write("Meal: " + selected_fields["strMeal"] + "\n")
            #f.write("Category: "+ selected_fields["strCategory"] + "\n")
            #f.write("Image: " + selected_fields["strMealThumb"] + "\n")
            #f.write("Youtube video: " + selected_fields["strYoutube"]+ "\n")
            #f.write("Instructions: " + selected_fields["strInstructions"] + "\n")
#
            #f.write("Ingredients:\n")
            #for ingredient, measure in selected_fields["Ingredients"].items():
            #    f.write(f"{ingredient}: {measure}\n")
            #f.write("\n")



def abbreviation_checker(*abbreviations: str):
    not_letters_of_word = lambda measure: fr'\d{measure}| {measure} | {measure}$'
    return r'|'.join((not_letters_of_word(abbreviation) for abbreviation in abbreviations))

def number_to_left(s: str, word: str) -> Optional[int]:
    """
    Returns the first number to the left side of given word
    """
    
    match = re.search(fr'\d+\s*{word}', s)
    return int(match.group()[:-1].strip()) if match else None


counter = 0


in_grams = lambda string: bool(re.compile(abbreviation_checker('g', 'gr') + r'|gram').search(string))
in_kilograms = lambda string: bool(re.compile(abbreviation_checker('kg') + r'|kilogram').search(string))
in_ml = lambda string: bool(re.compile(abbreviation_checker('ml')).search(string))
in_l = lambda string: bool(re.compile(abbreviation_checker('l') + r'|litre').search(string))
n_table_spoons = lambda string: bool(re.compile(abbreviation_checker('tbsp', 'tbs', 'tbls', 'tblsp') + r'|tablespoon').search(string))
in_tea_spoons = lambda string: bool(re.compile(abbreviation_checker('tsp') + r'|teaspoon').search(string))
in_cups = lambda string: bool(re.compile(r'cup').search(string))
in_oz = lambda string: bool(re.compile(abbreviation_checker('oz', 'oz.') + r'|ounce|oz.\)').search(string))
in_lb = lambda string: bool(re.compile(abbreviation_checker('lb', 'lbs')).search(string))
in_pounds = lambda string: bool(re.compile(r'pound').search(string))
in_scoops = lambda string: bool(re.compile(r'scoop').search(string))
in_parts = lambda string: bool(re.compile(r'|'.join(PARTS) + r'inch|cm' + r'|\drd|\dnd|\dth').search(string))
in_whole_pieces = lambda string: bool(re.compile(r'|'.join(WHOLE_PIECES) + r'|^[\d .\-/]*$|^½ $').search(string))
in_none = lambda string: bool(re.compile(r'|'.join(NON_MEASURABLE)).search(string))

for measure in measurements_set:
    measure = measure.lower()



    #if (not in_ml(measure)
    #    and not in_l(measure)
    #    and not in_grams(measure)
    #    and not in_kilograms(measure)
    #    and not n_table_spoons(measure)
    #    and not in_tea_spoons(measure)
    #    and not in_cups(measure)
    #    and not in_oz(measure)
    #    and not in_lb(measure)
    #    and not in_pounds(measure)
    #    and not in_scoops(measure)
    #    and not in_whole_pieces(measure)
    #    and not in_parts(measure)
    #    and not in_none(measure)
    #    and not '½' in measure):
    #    counter += 1
    #    print(measure)
    
    if in_grams(measure):
        grams = None
        counter += 1
        for gram in ('g', 'gr', 'gram'):
            if (number := number_to_left(measure, gram)) is not None:
                grams = number
                break
        if grams is not None:    
            print(measure + ': ' + str(grams))
        else:
            print(measure + ': !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            
 
    #if 'g' in measure and not 'for' in measure and not 'large' in measure and not 'spr' in measure:
    #    print(measure)
print(counter)
#print("Unique ingredients:", ingredients_set, "\n")
#print("Unique measurements:", measurements_set, "\n")
#print("Unique categories:", categories_set, "\n")
#with open("ingr_img_links.txt","w") as f:
#    for ingredient in ingredients_set:
#        f.write(f"https://www.themealdb.com/images/ingredients/{ingredient}.png \n")
#with open("unique_ingr.txt","w") as f:
#    for ingredient in ingredients_set:
#        f.write(f"{ingredient} \n")
#with open("unique_clean_measurem.txt","w") as f:
#    for measure in clean_measurements_set:
#        f.write(f"{measure} \n")
#with open("unique_cat.txt","w") as f:
#    for category in categories_set:
#        f.write(f"{category} \n")        