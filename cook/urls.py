from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'categorys', views.CategoryViewSet, basename='category')
router.register(r'ingredient_categorys', views.IngredientCategorySet, basename='ingredient_category')
router.register(r'ingredients', views.IngredientSet, basename='ingredient')
router.register(r'units', views.UnitSet, basename='unit')
router.register(r'measures', views.MeasureSet, basename='measure')
router.register(r'meals', views.MealSet, basename='meal')
router.register(r'ingredient_measures', views.IngredientMeasureSet, basename='ingredient_measure')

urlpatterns = router.urls