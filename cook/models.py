from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class IngredientCategory(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    ingredient_category_id = models.ForeignKey(IngredientCategory, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to='cook/files/images/ingredient_images', blank=True, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Measure(models.Model):
    name = models.CharField(max_length=20)
    value = models.FloatField()
    unit_id = models.ForeignKey(Unit, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Meal(models.Model):
    name = models.CharField(max_length=200)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    recipe = models.CharField(max_length=5000)
    ingredients = models.ManyToManyField(Ingredient, through='IngredientMeasure')
    img = models.ImageField(upload_to='cook/files/images/meal_images', blank=True, null=True)
    video = models.CharField(max_length=200, blank=True, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class IngredientMeasure(models.Model):
    measure_id = models.ForeignKey(Measure, on_delete=models.CASCADE)
    amount = models.FloatField()
    description = models.CharField(max_length=60)
    meal_id = models.ForeignKey(Meal, on_delete=models.CASCADE)
    ingredient_id = models.ForeignKey(Ingredient, on_delete=models.CASCADE)


    def __str__(self):
        return self.measure_id.name


class UserStorage(models.Model):
    measure_id = models.ForeignKey(Measure, on_delete=models.CASCADE)
    amount = models.FloatField()
    ingredient_id = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.measure_id.name
