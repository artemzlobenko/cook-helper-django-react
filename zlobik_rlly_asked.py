import requests
import json
import re
from enum import Enum
from typing import Optional

class Units(Enum):
    PIECE = 0
    MILLILITERS = 1
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

alphabet = "abcdefghijklmnopqrstuvwxyz"

def abbreviation_checker(*abbreviations: str):
    not_letters_of_word = lambda measure: fr'\d{measure}| {measure} | {measure}$'
    return r'|'.join((not_letters_of_word(abbreviation) for abbreviation in abbreviations))

#def number_to_left(s: str, word: str) -> Optional[int]:
#    """
#    Returns the first number to the left side of given word
#    """
#    
#    match = re.search(fr'\d+\s*{word}', s)
#    return int(match.group()[:-1].strip()) if match else None

def number_to_left(s: str, word: str) -> Optional[int]:
    """
    Returns the first number to the left side of given word
    """
    
    units = [
        'g', 'gr', 'gram', 'kilogram', 'kg', 'ml', 'l', 'litre', 'teaspoon', 'tsp', 'tbsp', 'tbs', 'tbls', 'tblsp', 'tablespoon', 'cups', 'oz', 'oz.', 'ounce', 'lb', 'lbs', 'pound', 'scoop', 'parts', 'inch', 'cm', 'drd', 'dnd', 'dth', 'whole pieces'
    ]

    pattern = fr'\d+\s*({"|".join(units)})'
    match = re.search(pattern, s)
    return int(match.group()[:-1].strip().split(" ")[0]) if match else None

def get_value_of_units(s: str, abbreviations): 
    value = None
    for unit in abbreviations:
        if (number := number_to_left(s, unit)) is not None:
            value = number
            break   
    return value

in_grams = lambda string: bool(re.compile(abbreviation_checker('g', 'gr') + r'|gram').search(string))
in_kilograms = lambda string: bool(re.compile(abbreviation_checker('kg') + r'|kilogram').search(string))
in_ml = lambda string: bool(re.compile(abbreviation_checker('ml')).search(string))
in_l = lambda string: bool(re.compile(abbreviation_checker('l') + r'|litre').search(string))
in_table_spoons = lambda string: bool(re.compile(abbreviation_checker('tbsp', 'tbs', 'tbls', 'tblsp') + r'|tablespoon').search(string))
in_tea_spoons = lambda string: bool(re.compile(abbreviation_checker('tsp') + r'|teaspoon').search(string))
in_cups = lambda string: bool(re.compile(r'cup').search(string))
in_oz = lambda string: bool(re.compile(abbreviation_checker('oz', 'oz.') + r'|ounce|oz.\)').search(string))
in_lb = lambda string: bool(re.compile(abbreviation_checker('lb', 'lbs')).search(string))
in_pounds = lambda string: bool(re.compile(r'pound').search(string))
in_scoops = lambda string: bool(re.compile(r'scoop').search(string))
in_parts = lambda string: bool(re.compile(r'|'.join(PARTS) + r'inch|cm' + r'|\drd|\dnd|\dth').search(string))
in_whole_pieces = lambda string: bool(re.compile(r'|'.join(WHOLE_PIECES) + r'|^[\d .\-/]*$|^½ $').search(string))
in_none = lambda string: bool(re.compile(r'|'.join(NON_MEASURABLE)).search(string))


def get_unit(measure):
    if in_grams(measure):
        abbreviations = ['g', 'gr', 'gram']
        amount = get_value_of_units(measure, abbreviations)
        return amount, Units.GRAMS, abbreviations
    elif in_kilograms(measure):
        abbreviations = ['kg', 'kilogram']
        amount = get_value_of_units(measure, abbreviations)
        return amount * 1000, Units.GRAMS, abbreviations
    elif in_ml(measure):
        abbreviations = ['ml']
        amount = get_value_of_units(measure, abbreviations)
        return amount, Units.MILLILITERS, abbreviations
    elif in_l(measure):
        abbreviations = ['l', 'litre']
        amount = get_value_of_units(measure, abbreviations)
        return amount * 1000, Units.MILLILITERS, abbreviations
    elif in_table_spoons(measure):
        abbreviations = ['tbsp', 'tbs', 'tbls', 'tblsp', 'tablespoon']
        amount = get_value_of_units(measure, abbreviations)
        return amount * 21.25, Units.GRAMS, abbreviations
    elif in_tea_spoons(measure):
        abbreviations = ['tsp', 'teaspoon']
        amount = get_value_of_units(measure, abbreviations)
        return amount * 4.2, Units.GRAMS, abbreviations
    elif in_cups(measure):
        abbreviations = ['cup']
        amount = get_value_of_units(measure, abbreviations)
        return amount * 250, Units.GRAMS, abbreviations
    elif in_oz(measure):
        abbreviations = ['oz', 'oz.', 'ounce', 'oz']
        amount = get_value_of_units(measure, abbreviations)
        return amount * 28.3495, Units.GRAMS, abbreviations
    elif in_lb(measure):
        abbreviations = ['lb', 'lbs']
        amount = get_value_of_units(measure, abbreviations)
        return amount * 453.592, Units.GRAMS, abbreviations
    elif in_pounds(measure):
        abbreviations = ['pound']
        amount = get_value_of_units(measure, abbreviations)
        return amount * 453.592, Units.GRAMS, abbreviations
    elif in_scoops(measure):
        abbreviations = ['scoop'].PIECE
        amount = get_value_of_units(measure, abbreviations)
        return amount, Units, abbreviations
    elif in_parts(measure):
        abbreviations = PARTS
        amount = get_value_of_units(measure, abbreviations)
        abbreviations.append(['inch','cm', 'rd', 'th', 'nd'])
        return amount, Units.PIECE, abbreviations
    elif in_whole_pieces(measure):
        abbreviations = WHOLE_PIECES
        amount = get_value_of_units(measure, abbreviations)
        return amount, Units.PIECE, abbreviations
    elif in_none(measure):
        amount = get_value_of_units(measure, abbreviations)
        return amount, None
    else:
        amount = get_value_of_units(measure, abbreviations)
        return amount,None

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
            "strInstructions": meal["strInstructions"],
        }

        ingredients_count = 20 # number of ingredients and measures in the meal
        ingredients_list = []
    
        for i in range(1, ingredients_count + 1):
            ingredient = meal.get(f"strIngredient{i}")
            measure = meal.get(f"strMeasure{i}")
            if ingredient and measure:
                amount, enum_units, abbreviations = get_unit(measure)
               
                
              #  amount = int(measure.split(" ")[0])
               # text, enum_units, abbreviations = get_unit(measure)
                
                ingredients_list.append({
                    'ingredient': ingredient,
                    'amount': amount,
                    'measure': enum_units,
                    'text': measure
                })

        selected_fields["Ingredients"] = ingredients_list

        print("Meal:", selected_fields["strMeal"])
        #print("Instructions:", selected_fields["strInstructions"])

        print("Ingredients:")
        for ingredient_dict in selected_fields["Ingredients"]:
            print(f"{ingredient_dict['ingredient']}: {ingredient_dict['amount']} {ingredient_dict['measure']}")
        print("\n")
