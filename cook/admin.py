from django.contrib import admin

from .models import *


class IngredientMeasureInline(admin.TabularInline):
    model = IngredientMeasure
    extra = 1


class IngredientAdmin(admin.ModelAdmin):
    inlines = (IngredientMeasureInline,)


class MealAdmin(admin.ModelAdmin):
    inlines = (IngredientMeasureInline,)

admin.site.register(Category)
admin.site.register(IngredientCategory)
admin.site.register(IngredientMeasure)
admin.site.register(Measure)
admin.site.register(UserStorage)
admin.site.register(Unit)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Meal, MealAdmin)


