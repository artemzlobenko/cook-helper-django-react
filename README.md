Cook Helper Django REST framework-React
1. Description
Our project is made for people, who enjoy cooking. We have provided recipe meals and functionality for adding user own meals and recipes. Enjoy!
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
3. Installation
To install Python visit https://www.python.org/ and download last version of it for your OS. Follow the installation.
To install Django create your python project in any IDE(PyCharm, Visual Studio Code) and run this command in terminal.
python -m pip install Django
- Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of web development, so you can focus on writing your app without needing to reinvent the wheel. It's free and open source.

To install djangorestframework. markdown, django-filter, cors-headers and simplejwt run commands:
pip install djangorestframework
pip install markdown      
pip install django-filter  
pip install djangorestframework-simplejwt
pip install django-cors-headers
- Django REST framework is a powerful and flexible toolkit for building Web APIs. 
- Markdown is a popular text-to-HTML conversion tool for web writers. It is far easier to use than plain old HTML. 
- Django-filter is a reusable Django application allowing users to declaratively add dynamic QuerySet filtering from URL parameters. 
- Simple JWT is a JSON Web Token authentication plugin for the Django REST Framework. 
- A Django App that adds Cross-Origin Resource Sharing (CORS) headers to responses. This allows in-browser requests to your Django application from other origins.

To install PyJWT run:
pip install pyjwt
- PyJWT is a Python library which allows you to encode and decode JSON Web Tokens (JWT). JWT is an open, industry-standard (RFC 7519) for representing claims securely between two parties.

To install Pillow run:
pip install Pillow
- The Python Imaging Library adds image processing capabilities to your Python interpreter.

To install pytz and tzdata run:
pip install pytz
pip install tzdata
- pytz brings the Olson tz database into Python. This library allows accurate and cross platform timezone calculations using Python 2.4 or higher.
- tzdata is a Python package containing zic-compiled binaries for the IANA time zone database.

To install sqlparse run:
pip install sqlparse
- sqlparse is a non-validating SQL parser for Python. It provides support for parsing, splitting and formatting SQL statements.

4. Backend

5. Installation 2
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
Then you can have all of the functionality of Django REST framework.

