from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class IngredientCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = IngredientCategory
        fields = "__all__"


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = "__all__"


class UnitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Unit
        fields = "__all__"


class MeasureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Measure
        fields = "__all__"


class MealSerializer(serializers.ModelSerializer):

    class Meta:
        model = Meal
        fields = "__all__"


class IngredientMeasureSerializer(serializers.ModelSerializer):

    class Meta:
        model = IngredientMeasure
        fields = "__all__"