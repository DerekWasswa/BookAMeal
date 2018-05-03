# Book A Meal Application

An application that allows a user to make meal orders from various vendors


[![Build Status](https://travis-ci.org/DerekWasswa/BookAMeal.svg?branch=master)](https://travis-ci.org/DerekWasswa/BookAMeal)
[![Coverage Status](https://coveralls.io/repos/github/DerekWasswa/BookAMeal/badge.svg?branch=master)](https://coveralls.io/github/DerekWasswa/BookAMeal?branch=tests_amends)
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

##UI Pages hosted on GitHub Pages
* [Github-Pages](https://derekwasswa.github.io/BookAMeal/index.html)
* [Github-Pages](https://derekwasswa.github.io/BookAMeal/admin.html)
* [Github-Pages](https://derekwasswa.github.io/BookAMeal/customer.html)
* [Github-Pages](https://derekwasswa.github.io/BookAMeal/orderhistory.html)




## Application API endpoints ([Documentation](https://bookamealapi1.docs.apiary.io/#)

| EndPoint                | Method |
| ----------------------- | ------ |
| `/auth/signup`          | POST   |
| `/auth/login`           | POST   |
| `/meals/`               | GET    |
| `/meals/`               | POST   |
| `/meals/<mealId>`       | DELETE |
| `/meals/<mealId>`       | GET    |
| `/meals/<mealId>`       | PUT    |
| `/menu/`                | GET    |
| `/menu/`                | POST   |
| `/orders/`              | GET    |
| `/orders/`              | POST   |
| `/orders/<orderId>`     | GET    |
| `/orders/<orderId>`     | PUT    |

1.  Test the api endpoints using [Postman](https://www.getpostman.com/)
2.  To test the endpoints in Terminal shell (Use either pytest test_app.py, nosetests test_app.py, python test_app.py)


##Deploying the Application on your device
* First change to a directory you want to would like the application to be then clone the GitHub (https://github.com/DerekWasswa/BookAMeal.git) repository by the command: git clone https://github.com/DerekWasswa/BookAMeal.git
* Install a virtual environment on your device (run the command: pip install virtualenv)
* Change your current directory to the application you have just cloned.
* Start the virtual environment on to the application by running the command: source venv/bin/activate
* Run the following command to install the application modules and resources: pip install -r requirements.txt
* Run the application by hitting the command: python v1/app.py




## Production Application
The application api is deployed on Heroku [Link](https://bookamealapi1.docs.apiary.io/) 
