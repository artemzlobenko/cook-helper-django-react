from django.contrib import admin

from .models import *


class IngregientMeasureInline(admin.TabularInline):
    model = IngredientMeasure
    extra = 1


class IngredientAdmin(admin.ModelAdmin):
    inlines = (IngregientMeasureInline,)


class MealAdmin(admin.ModelAdmin):
    inlines = (IngregientMeasureInline,)

admin.site.register(Category)
admin.site.register(IngredientCategory)
admin.site.register(IngredientMeasure)
admin.site.register(Measure)
admin.site.register(Unit)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Meal, MealAdmin)
admin.site.register(UserStorage)


