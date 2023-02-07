from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class IngredientCategory(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    ingredient_category = models.ForeignKey(IngredientCategory, on_delete=models.CASCADE, blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Measure(models.Model):
    name = models.CharField(max_length=20)
    value = models.FloatField()
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Meal(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    recipe = models.CharField(max_length=5000)
    ingredients = models.ManyToManyField(Ingredient, through='IngredientMeasure')
    image_url = models.URLField(max_length=500, blank=True, null=True)
    video_url = models.URLField(max_length=500, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class IngredientMeasure(models.Model):
    measure = models.ForeignKey(Measure, on_delete=models.CASCADE)
    amount = models.FloatField()
    description = models.CharField(max_length=60)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)


    def __str__(self):
        return self.measure.name


class UserStorage(models.Model):
    measure = models.ForeignKey(Measure, on_delete=models.CASCADE)
    amount = models.FloatField()
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.measure.name
