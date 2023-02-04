from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


router = DefaultRouter()
router.register(r'categorys', views.CategoryViewSet, basename='category')
router.register(r'ingredient_categorys', views.IngredientCategorySet, basename='ingredient_category')
router.register(r'ingredients', views.IngredientSet, basename='ingredient')
router.register(r'units', views.UnitSet, basename='unit')
router.register(r'measures', views.MeasureSet, basename='measure')
router.register(r'meals', views.MealSet, basename='meal')
router.register(r'ingredient_measures', views.IngredientMeasureSet, basename='ingredient_measure')

urlpatterns = [
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterView.as_view(), name='auth_register'),
    path('test/', views.testEndPoint, name = 'test')
]

urlpatterns += router.urls