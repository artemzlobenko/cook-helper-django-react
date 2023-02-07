Cook Helper Django REST framework-React

1. Description

Our web application is a recipe storage platform, where users can store, manage, and organize their favorite recipes in one place. It allows users to create an online recipe book with detailed instructions, ingredient lists, and photos for each recipe. The application is user-friendly, easy to navigate and provides a way to categorize recipes based on different criteria such as meal type and ingredient type. With this web application, users can keep track of their favorite meals, experiment with new recipes, and save time and effort in the kitchen. They can also share their recipes with friends and family, making meal planning and preparation a breeze.


2. Prerequisites

asgiref 3.6.0
Django 4.1.6
django-cors-headers 3.13.0
djangorestframework 3.14.0
djangorestframework-simplejwt 5.2.2
Python 3.10+
Pillow 9.4.0
PyJWT 2.6.0
pytz 2022.7.1
sqlparse 0.4.3
tzdata 2022.7

    - ASGI is a standard for Python asynchronous web apps and servers to communicate with each other, and positioned as an asynchronous successor to WSGI.
    - Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of web development, so you can focus on writing your app without needing to reinvent the wheel. It's free and open source.
    - Django REST framework is a powerful and flexible toolkit for building Web APIs. 
    - Simple JWT is a JSON Web Token authentication plugin for the Django REST Framework. 
    - A Django App that adds Cross-Origin Resource Sharing (CORS) headers to responses. This allows in-browser requests to your Django application from other origins.
    - PyJWT is a Python library which allows you to encode and decode JSON Web Tokens (JWT). JWT is an open, industry-standard (RFC 7519) for representing claims securely between two parties.
    - The Python Imaging Library adds image processing capabilities to your Python interpreter.
    - pytz brings the Olson tz database into Python. This library allows accurate and cross platform timezone calculations using Python 2.4 or higher.
    - tzdata is a Python package containing zic-compiled binaries for the IANA time zone database.
    - sqlparse is a non-validating SQL parser for Python. It provides support for parsing, splitting and formatting SQL statements


3. Installation 

To work with project you must create python virtual enviroment by using command:
    py -m venv env
Before you can start installing or using packages in your virtual environment you'll need to activate it. Activating a virtual environment will put the virtual environment-specific python and pip executables into your shel's PATH.
    .\env\Scripts\activate
Then you must download all the packages in requierements.txt. Command:
    pip install -r requierements.txt
Then in terminal set your SecretKey:
$env:SECRET_KEY='django-insecure-1lt(e!7+ukhyskgqccw4+vhor4p-u$khry-vlh*=b_61_x5$#m'
Then make migrations. Command:
    python manage.py makemigrations 
Then migrate:
python manage.py migrate
Create superuser(admin):
    python manage.py createsuperuser
username - your superuser name
email - enter your email(used for superuser recovery)
password - must be 8 characters long
password2 - confirm password

Superuser usage is needed for storing main data, which can't be seen by non-superusers. 
Then you can have all of the functionality of Django REST framework.


4. Code

When project started with, app cook was created.
In INSTALLED-APPS(settings.py) was added a new value cook.apps.CookConfig.
Than models were created and initial migration was made.

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('img', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='IngredientMeasure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('description', models.CharField(max_length=60)),
                ('ingredient_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cook.ingredient')),
            ],
        ),
        migrations.CreateModel(
            name='Measure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('value', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='UserStorage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('ingredient_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cook.ingredient')),
                ('measure_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cook.measure')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='measure',
            name='unit_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cook.unit'),
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('recipe', models.CharField(max_length=5000)),
                ('img', models.URLField(blank=True, null=True)),
                ('video', models.URLField(blank=True, null=True)),
                ('category_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cook.category')),
                ('ingredients', models.ManyToManyField(through='cook.IngredientMeasure', to='cook.ingredient')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='ingredientmeasure',
            name='meal_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cook.meal'),
        ),
        migrations.AddField(
            model_name='ingredientmeasure',
            name='measure_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cook.measure'),
        ),
        migrations.CreateModel(
            name='IngredientCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='ingredient',
            name='ingredient_category_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cook.ingredientcategory'),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]


Serializers allow complex data such as querysets and model instances to be converted to native Python datatypes that can then be easily rendered into JSON, XML or other content types. Serializers also provide deserialization, allowing parsed data to be converted back into complex types, after first validating the incoming data. Serializers were made for created models and User.

    from rest_framework import serializers
    from .models import *
    from django.contrib.auth.models import User
    from django.contrib.auth.password_validation import validate_password
    from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


    class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
        @classmethod
        def get_token(cls, user):
            token = super().get_token(user)
            token['username'] = user.username
            token['email'] = user.email
            return token


    class RegisterSerializer(serializers.ModelSerializer):
        email = serializers.CharField(write_only=True, required=True)
        password = serializers.CharField(
            write_only=True, required=True, validators=[validate_password])
        password2 = serializers.CharField(write_only=True, required=True)

        class Meta:
            model = User
            fields = ('username', 'email', 'password', 'password2')

        def validate(self, attrs):
            if attrs['password'] != attrs['password2']:
                raise serializers.ValidationError(
                    {"password": "Password fields didn't match."})

            return attrs

        def create(self, validated_data):
            user = User.objects.create(
                username=validated_data['username'], email = validated_data['email']
            )

            user.set_password(validated_data['password'])
            user.save()

            return user


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


    class UserStorageSerializer(serializers.ModelSerializer):

        class Meta:
            model = UserStorage
            fields = "__all__"

To use Django REST framework features in INSTALLED_APPS were added new values, so INSTALLED looked this:

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'rest_framework',
        'rest_framework_simplejwt.token_blacklist',
        'cook.apps.CookConfig',
        'corsheaders',
    ]
SIMPLE_JWT were added with installing djangorestframework-simplejwt. REST_FRAMEWORK should be made manually.

    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework_simplejwt.authentication.JWTAuthentication',
        )
    }
views.py

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


    class UserStorageSet(viewsets.ModelViewSet):
        serializer_class = UserStorageSerializer
        queryset = UserStorage.objects.all()


REST framework adds support for automatic URL routing to Django, and provides you with a simple, quick and consistent way of wiring your view logic to a set of URLs.
DefaultRouter includes a root API view that returns a response containing hyperlinks to all list views. It also generates routers for the optional style in .json format. This router includes routes for the standard set of actions list, create, retrieve, update, partial_update and destroy.

In urls.py we made router for API and made connection for our token user registration.

    from django.urls import path, include
    from . import views
    from rest_framework.routers import DefaultRouter

    from rest_framework_simplejwt.views import (
        TokenRefreshView,
    )
        

    router = DefaultRouter()
    router.register(r'categories', views.CategoryViewSet, basename='category')
    router.register(r'ingredient_categories', views.IngredientCategorySet, basename='ingredient_category')
    router.register(r'ingredients', views.IngredientSet, basename='ingredient')
    router.register(r'units', views.UnitSet, basename='unit')
    router.register(r'measures', views.MeasureSet, basename='measure')
    router.register(r'meals', views.MealSet, basename='meal')
    router.register(r'ingredient_measures', views.IngredientMeasureSet, basename='ingredient_measure')
    router.register(r'user_storages', views.UserStorageSet, basename='user_storage')

    urlpatterns = [
        path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('register/', views.RegisterView.as_view(), name='auth_register'),
        path('test/', views.testEndPoint, name = 'test')
    ]

    urlpatterns += router.urls

In admin.py all models were registered to do CRUD operation in localhost/admin. Developer can access this admin panel via superuser created earlier.

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
