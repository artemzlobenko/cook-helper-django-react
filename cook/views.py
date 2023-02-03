from rest_framework import viewsets
from .serializers import *
from .models import *

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
   # Category.create_from_list()


class IngredientCategorySet(viewsets.ModelViewSet):
    serializer_class = IngredientCategorySerializer
    queryset = IngredientCategory.objects.all()


class IngredientSet(viewsets.ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()


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





























#@api_view(["GET"])
#def apiOverview(request):
    #api_urls = {
        #'Category List': 'category-list',
        #'Detail View': '/meal-detail/<str:pk>/',
        #'Create': 'meal-create',
        #'Update': '/meal-update/<str:pk>/',
        #'Delete': '/meal-delete/<str:pk>/',
   # }
   # return Response(api_urls)
#@api_view(["GET"])
#def categoryList(request):
    #categorys = Category.objects.all()
    #serializer = CategorySerializer(categorys, many=True)
    #return Response(serializer.data)

