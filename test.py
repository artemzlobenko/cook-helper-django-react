import json
from django.shortcuts import render
from django.views import View
import requests
from rest_framework import viewsets
from .serializers import *
from .models import *

from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

from cook.serializers import MyTokenObtainPairSerializer, RegisterSerializer

from django.contrib.auth.models import User




import requests
import json
import re
from typing import Optional


Unit(name='Piece').save()
Unit(name='Milliliter').save()
Unit(name='Grams').save()



class Units():
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

    pattern = fr'\d+\s*({word})'
    match = re.search(pattern, s)
    if word == 'g':
        return int(match.group()[:-1].strip()) if match else 0
    if (result := ''.join(filter(str.isdigit, s))):
        return int(result)
    else:
        return 0


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
        abbreviations = ['gram', 'gr', 'g']
        unicode_fractions = {'¼': 0.25}
        for fract, val in unicode_fractions.items():
            if fract in measure:
                return val, Units.GRAMS, abbreviations
        amount = get_value_of_units(measure, abbreviations)
        return amount, Units.GRAMS, abbreviations
    elif in_kilograms(measure):
        abbreviations = ['kilogram', 'kg']
        amount = get_value_of_units(measure, abbreviations)
        return amount * 1000, Units.GRAMS, abbreviations
    elif in_ml(measure):
        abbreviations = ['ml']
        amount = get_value_of_units(measure, abbreviations)
        return amount, Units.MILLILITERS, abbreviations
    elif in_l(measure):
        abbreviations = ['litre', 'l']
        amount = get_value_of_units(measure, abbreviations)
        return amount * 1000, Units.MILLILITERS, abbreviations
    elif in_table_spoons(measure):
        abbreviations = ['tablespoon', 'tbsp', 'tblsp', 'tbls', 'tbs', ]
        amount = get_value_of_units(measure, abbreviations)
        return round(amount * 21.25), Units.GRAMS, abbreviations
    elif in_tea_spoons(measure):
        abbreviations = ['teaspoon', 'tsp']
        unicode_fractions = {'¼': 0.25, '½': 0.5}
        for fract, val in unicode_fractions.items():
            if fract in measure:
                return val, Units.GRAMS, abbreviations
        amount = get_value_of_units(measure, abbreviations)
        return round(amount * 4.2), Units.GRAMS, abbreviations
    elif in_cups(measure):
        abbreviations = ['cup']
        amount = get_value_of_units(measure, abbreviations)
        return amount * 250, Units.GRAMS, abbreviations
    elif in_oz(measure):
        abbreviations = ['ounce', 'oz.', 'oz']
        amount = get_value_of_units(measure, abbreviations)
        return round(amount * 28.3495), Units.GRAMS, abbreviations
    elif in_lb(measure):
        abbreviations = ['lbs', 'lb']
        amount = get_value_of_units(measure, abbreviations)
        return round(amount * 453.592), Units.GRAMS, abbreviations
    elif in_pounds(measure):
        abbreviations = ['pound']
        amount = get_value_of_units(measure, abbreviations)
        return round(amount * 453.592), Units.GRAMS, abbreviations
    elif in_scoops(measure):
        abbreviations = ['scoop']
        amount = get_value_of_units(measure, abbreviations)
        return round(amount * 70.87), Units.MILLILITERS, abbreviations
    elif in_parts(measure):
        abbreviations = PARTS
        amount = get_value_of_units(measure, abbreviations)
        abbreviations.extend(['inch','cm', 'rd', 'th', 'nd'])
        for abb in abbreviations:
            if abb in measure:
                return amount, Units.PIECE, [abb]
        return amount, Units.PIECE, abbreviations
    elif in_whole_pieces(measure):
        abbreviations = WHOLE_PIECES
        unicode_fractions = {'1 1/2': 0.5}
        for fract, val in unicode_fractions.items():
            if fract in measure:
                return val, Units.GRAMS, ['half']
        amount = get_value_of_units(measure, abbreviations)
        for abb in abbreviations:
            if abb in measure:
                return amount, Units.PIECE, [abb]
        return amount, Units.PIECE, abbreviations
    elif in_none(measure):
        amount = None
        abbreviations = NON_MEASURABLE
        for abb in abbreviations:
            if abb in measure:
                return amount, Units.PIECE, [abb]
        return amount, None, abbreviations
    else:
        amount = None
        return amount, None, [None]
result = []
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
        ingredients_list = []
    
        for i in range(1, ingredients_count + 1):
            ingredient = meal.get(f"strIngredient{i}")
            measure_obj = meal.get(f"strMeasure{i}")
            if ingredient and measure_obj:
                amount, enum_units, abbreviations = get_unit(measure_obj)
               
                
              #  amount = int(measure.split(" ")[0])
               # text, enum_units, abbreviations = get_unit(measure)
                
                ingredients_list.append({
                    'ingredient': ingredient,
                    'amount': 1,
                    'measure': {
                            'abbreviation': abbreviations[0],
                            'units': enum_units,
                            'value': amount,
                        },
                    'text': measure_obj
                })

        selected_fields["Ingredients"] = ingredients_list
        for i in range(len(ingredients_list)):
            if ingredients_list[i]["amount"] is None:
                ingredients_list[i]["amount"] = ingredients_list[i]["text"]
        result.append(selected_fields)
        #####print("Meal:", selected_fields["strMeal"])
        #print("Instructions:", selected_fields["strInstructions"])

        print("Ingredients:")
        for ingredient_dict in selected_fields["Ingredients"]:
            print(f"{ingredient_dict['ingredient']}: {ingredient_dict['amount']} {ingredient_dict['measure']} {ingredient_dict['text']}")
        #####print("\n")
print(result[0])

   
   
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def testEndPoint(request):
    if request.method == 'GET':
        data = f"Congratulation {request.user}, your API just responded to GET request"
        return Response({'response': data}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        text = request.POST.get('text')
        data = f'Congratulation your API just responded to POST request with text: {text}'
        return Response({'response': data}, status=status.HTTP_200_OK)
    return Response({}, status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/cook/token/',
        '/cook/register/',
        '/cook/token/refresh/'
    ]
    return Response(routes)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    
    categories = [
            'Beef',
            'Breakfast',
            'Miscellaneous',
            'Pork',
            'Vegan',
            'Starter',
            'Dessert',
            'Seafood',
            'Pasta',
            'Lamb',
            'Side',
            'Chicken',
            'Goat',
            'Vegetarian',
        ]

    for category in categories:
        owner = User.objects.get(id=1)
        Category(name=category, user_id=owner).save()


class IngredientCategorySet(viewsets.ModelViewSet):
    serializer_class = IngredientCategorySerializer
    queryset = IngredientCategory.objects.all()


class IngredientSet(viewsets.ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    response = requests.get('https://www.themealdb.com/api/json/v1/1/list.php?i=list')
    data = response.content
    
    data = json.loads(data)
    ingredients = data['meals']
    ingredient_names = [ingredient['strIngredient'] for ingredient in ingredients]
    
    owner = User.objects.get(id=1)
    
    for i_name in ingredient_names:
        image = fr'https://www.themealdb.com/images/ingredients/{i_name}.png'
        Ingredient(name=i_name, user_id=owner, image=image).save()


class UnitSet(viewsets.ModelViewSet):
    serializer_class = UnitSerializer
    queryset = Unit.objects.all()


class MeasureSet(viewsets.ModelViewSet):
    serializer_class = MeasureSerializer
    queryset = Measure.objects.all()


class MealSet(viewsets.ModelViewSet):
    serializer_class = MealSerializer
    queryset  = Meal.objects.all()


class IngredientMeasureSet(viewsets.ModelViewSet):
    serializer_class = IngredientMeasureSerializer
    queryset = IngredientMeasure.objects.all()


class UserStorageSet(viewsets.ModelViewSet):
    serializer_class = UserStorageSerializer
    queryset = UserStorage.objects.all()








owner = User.objects.get(id=1)
for meal in result:
    meal_name = meal['strMeal']
    meal_category = meal['strCategory']
    meal_text = meal['strInstructions']
    meal_yt = meal['strYoutube']
    meal_obj = Meal(
            name=meal_name,
            category_id=Category.objects.filter(name=meal_name).first(),
            recipe=meal_text,
            video=meal_yt,
            user_id=owner,
        )
    meal_obj.save()
    print(meal_category + '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    for ingredient in meal['Ingredients']:
        ingredient_name = ingredient['ingredient']
        ingredient_amount = 1
        ingredient_text = ingredient['text']
        
        measure_name = ingredient['measure']['abbreviation']
        measure_units = ingredient['measure']['units']
        measure_value = ingredient['measure']['value']
        
        if measure_units is None:
            measure_units = 0
            
        if measure_value is None:
            measure_value = 0
            
        if measure_name is None:
            measure_name = 0
            
        
        measure_obj = Measure(
            name=measure_name,
            value=measure_value,
            unit_id=Unit.objects.get(id=measure_units + 1)
            )
        measure_obj.save()
        
        
        if 'softe' in ingredient_name and 'butter' in ingredient_name:
            ingredient_name = 'butter'             
        
        ingredient_obj = Ingredient.objects.filter(name__contains=ingredient_name).first()
        
        if ingredient_obj is None:
            ingredient_obj = Ingredient(
                name=ingredient_name,
                user_id=owner
            )
            ingredient_obj.save()
            
        print(ingredient_name + '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print(ingredient_name.title() + '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        
        IngredientMeasure(
            ingredient_id=ingredient_obj,
            measure_id=measure_obj,
            meal_id=meal_obj,
            description=ingredient_text,
            amount=ingredient_amount,
        ).save()
       