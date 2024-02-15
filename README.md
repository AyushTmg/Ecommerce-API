#             Ecommerce-API 







Technologies used:Django, Django Rest Framework,Simple JWT ,Celery, Django Debug Toolbar, PostgreSQL, Redis,Faker,Django-Filter,Django-dotenv,pytest,pytest-django and more


    Please Use Better Comments Extension of VsCode for better 
    readability since i have used it in this project to highlight 
    my Comments 


## API documentation

The API documentation for the e-commerce Django project provides a straightforward and concise overview of the available endpoints and their functionalities, catering to developers of varying skill levels.This focuses on clarity and simplicity, providing developers with the necessary information to quickly and effectively integrate with the Django project


https://documenter.getpostman.com/view/30946823/2sA2r535Mj




## Installation


1-First of all clone this repo
--

        https://github.com/AyushTmg/Ecommerce-API.git


2-Setup a virtual enviroment 
--

        python -m venv venv


3-Install all dependencies from the requirements.txt in a virtual enviroment
--

        pip install -r requirements.txt


4- Configure database according to your reliability in this case postgres is used
--
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME':os.environ.get("DB_NAME"),
                'USER': 'postgres', 
                'PASSWORD':os.environ.get("DB_PASS"), 
                'HOST': 'localhost', 

            }
        }

- If you want to use default database you can also uncomment from the setting.py 

5-Add .env File and add these field or just configure example.env
--

        EMAIL="Add Your Email"
        EMAIL_PASSWORD="Add Your Email Password"

        SECRET_KEY = 'Your Project Secret Key'

        THE_SUPPLIER_EMAIL="Add Supplier Email here"


- You need to add this if you are also using postgres as your database 

        DB_NAME='Add Your Database Name'
        DB_PASS='Add Your Database Password'



6-Migrate the changes to your database
--
        python manage.py makemigrations 
        python manage.py migrate

7-Run Application with celery
--
        python manage.py runserver
        celery -A main worker -l info
## To Generate Dummy Data For Ecommerce-API

- In deveopment phase if you want to generate dummy data's for the application Use -->



        python manage.py generate_data


- To configure the process of generating dummy data you can configure the dummy.py file in ecommerce app which is only used for generating dummy data for development phase 






## For Running Test

### Running Tests

To run tests, use the following command in the terminal:

        pytest


### Continuous Testing

For continuous testing to update code and test simultaneously, use:



        ptw

## Contribution

Contributions are welcomed ! If you're interested in helping to improve this project, please feel free to fork the repository, make your changes, and submit a pull request. Any contributions, whether big or small, are greatly appreciated!