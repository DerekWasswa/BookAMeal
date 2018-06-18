# Book A Meal Application

An application that allows a user to make meal orders from various vendors


[![Build Status](https://travis-ci.org/DerekWasswa/BookAMeal.svg?branch=develop)](https://travis-ci.org/DerekWasswa/BookAMeal)
[![Coverage Status](https://coveralls.io/repos/github/DerekWasswa/BookAMeal/badge.svg?branch=develop)](https://coveralls.io/github/DerekWasswa/BookAMeal?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/2877ce828afcde45fe6a/maintainability)](https://codeclimate.com/github/DerekWasswa/BookAMeal/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/2877ce828afcde45fe6a/test_coverage)](https://codeclimate.com/github/DerekWasswa/BookAMeal/test_coverage)



## UI Designs

The user interfaces for Book A Meal application were developed with the following:
* HTML
* CSS
* Javascript

Under the UI directory on the feature branch, there are various various HTML pages as described below
* An HTML page to all users to signup and sign to the application
* An HTML page that shows the customers' (user) home page where they can perform their operations (i.e. get the menu of the day, make order)
* An HTML page that allows admins (caterers) a home to perform their operations (i.e. add meal, edit meal, delete meal, set up a menu for the day)
* An HTML page that allows the admins and users to view their order history

## UI Pages hosted on GitHub Pages
* [Github-Pages](https://derekwasswa.github.io/BookAMeal/index.html)
* [Github-Pages](https://derekwasswa.github.io/BookAMeal/admin.html)
* [Github-Pages](https://derekwasswa.github.io/BookAMeal/customer.html)
* [Github-Pages](https://derekwasswa.github.io/BookAMeal/orderhistory.html)


## Technologies used.

* [Flask API](https://www.flaskapi.org/)
* [python 3.6](https://www.python.org/downloads/release/python-360/)
* [flask](flask.pocoo.org/)
* [virtualenv](https://virtualenv.pypa.io/en/stable/)
* [PyJWT](https://pypi.org/project/PyJWT/)


## Application API endpoints [Documentation](https://bookamealapi1.docs.apiary.io/#)

| EndPoint                       | Method |
| ------------------------------ | ------ |
| `/api/v1/auth/signup`          | POST   |
| `/api/v1/auth/login`           | POST   |
| `/api/v1/meals/`               | GET    |
| `/api/v1/meals/`               | POST   |
| `/api/v1/meals/<mealId>`       | DELETE |
| `/api/v1/meals/<mealId>`       | GET    |
| `/api/v1/meals/<mealId>`       | PUT    |
| `/api/v1/menu/`                | GET    |
| `/api/v1/menu/`                | POST   |
| `/api/v1/orders/`              | GET    |
| `/api/v1/orders/`              | POST   |
| `/api/v1/orders/<orderId>`     | GET    |
| `/api/v1/orders/<orderId>`     | PUT    |

* Test the api endpoints using [Postman](https://www.getpostman.com/)
* To test the endpoints in Terminal shell (Use either pytest test_app.py, nosetests test_app.py, python test_app.py)
* Test the AI endpoints using [Heroku](https://bookamealapi1.docs.apiary.io/) 


## Running the Application on your device
1. First change to a directory you want to would like the application to be then clone the GitHub repository.
    * Run the command.
    > `$ git clone https://github.com/DerekWasswa/BookAMeal.git`
2. Install a virtual environment on your device.
> `$ pip install virtualenv`
3. Change your current directory to the application you have just cloned.
6. Start the virtual environment on to the application by running the command.
> `source venv/bin/activate*`
4. Run the following command to install the application modules and resources.
> `pip install -r requirements.txt`
5. Run the application by hitting the command.
> `python run.py`



## Production Application
The application api is deployed on Heroku [Link](https://bookamealapi1.docs.apiary.io/) 
