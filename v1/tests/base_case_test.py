import unittest
import json
from flask import session
from v1.api import create_app
from v1.api import db
from v1.api.models.meals import Meal
from v1.api.models.users import User
from v1.api.models.menu import Menu
from v1.api.models.orders import Order


class BaseCaseTest(unittest.TestCase):

    def setUp(self):
        # Set up the globally used variables for use
        app = create_app('testing')
        self.client = app.test_client()
        db.create_all()

        self.no_token_headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic auth',
        }

        self.invalid_token_headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic auth',
            'app-access-token': 'eyJ1c2VyX2lkIjoxLCJhZG1pbiI6InRydWUifQ.W0EoWSsYbSlS8fSRWJsV77cBqbfNg8Iy2txp_9BdBzM'
        }

        self.user_data = json.dumps({
            'username': 'Wasswa Derick',
            'email': 'wasswadero@gmail.com',
            'password': '12345',
            'admin': False
        })

        self.invalid_email_user_data = json.dumps({
            'username': 'example',
            'email': 'test',
            'password': '12345',
            'admin': True
        })

        self.wrong_request_user_params = json.dumps({
            'us': 'example',
            'ma': 'tester@example.com',
            'asswo': '12345',
            'dmi': True
        })

        self.user_does_not_exists = json.dumps({
            'username': 'invasionworld',
            'email': 'invasionworlds@yahoo.com',
            'password': '12345',
            'admin': True
        })

        self.empty_user_data = json.dumps({
            'username': '',
            'email': '',
            'password': '',
            'admin': ''
        })

        self.empty_user_data_login = json.dumps({
            'email': '',
            'password': '',
            'admin': ''
        })

        self.all_food_meal = json.dumps({
            'meal': 'Fish with All foods',
            'price': 25000
        })

        self.matooke_meal = json.dumps({
            'meal': 'Luwombo with Matooke',
            'price': 25000
        })

        self.update_meal = json.dumps({
            'meal_update': 'Luwombo with All Local Foods',
            'price_update': 20000
        })

        self.empty_meal = json.dumps({
            'meal': '',
            'price': ''
        })

        self.meal_with_wrong_request = json.dumps({
            'mea': 'Fish with All foods',
            'pric': 25000
        })

        self.stringed_meal_price = json.dumps({
            'meal': 'Bananas',
            'price': '12asu'
        })

        self.stringed_meal_price_update = json.dumps({
            'meal_update': 'Bananas',
            'price_update': '12asu'
        })

        self.empty_meal_options = json.dumps({
            'meal_update': '',
            'price_update': ''
        })

        self.wrong_update_meal_request_params = json.dumps({
            'meal_upd': 'Luwombo with All Local Foods',
            'price_up': 20000
        })

        self.caterer_menu = json.dumps({
            'menu_name': 'Jojo Restaurant Special Friday',
            'date': '2018-05-12',
            'description': 'For our special friday, enjoy the menu with a free dessert',
            'meal_id': 1
        })

        self.caterer_menu_wrong_request_params = json.dumps({
            'menu_n': 'Jojo Restaurant Special Friday',
            'dae': '2018-05-12',
            'dcription': 'For our special friday, enjoy the menu with a free dessert',
            'ml_id': 1
        })

        self.menu_date = json.dumps({
            'date': '2018-05-12'
        })

        self.empty_menu = json.dumps({
            'menu_name': '',
            'date': '',
            'description': '',
            'meal_id': ''
        })

        self.app_order = json.dumps({
            'user': 'derrekwasswa256@gmail.com',
            'meal': 2,
            'date': '2018-05-12',
            'menu_id': 1
        })

    def mock_signup(self):
        user_data = json.dumps({
            'username': 'derreckwasswa',
            'email': 'derrekwasswa256@gmail.com',
            'password': '12345',
            'admin': True
        })
        self.client.post('/api/v1/auth/signup', data=user_data)

    def mock_login(self):
        user_data = json.dumps({
            'email': 'derrekwasswa256@gmail.com',
            'password': '12345',
            'admin': True
        })
        return self.client.post('/api/v1/auth/login', data=user_data)

    def unpriviledged_mock_login(self):
        user_data = json.dumps({
            'email': 'derrekwasswa256@gmail.com',
            'password': '12345',
            'admin': False
        })
        return self.client.post('/api/v1/auth/login', data=user_data)

    def headers_with_token(self, token):
        ''' Return Header with a token value '''
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic auth',
            'app-access-token': token
        }
        return headers

    def add_mock_meals_to_menu(self, header):
        meals_mock_data = {
            'meal': 'Chips and Chicken',
            'price': 25000
        }
        self.client.post(
            '/api/v1/meals/',
            data=meals_mock_data,
            headers=header)

        meal_object = Meal('Fish with Macs', 23000, 1)
        meal_object1 = Meal('Fish with Flies', 25000, 1)
        db.session.add(meal_object)
        db.session.commit()
        db.session.add(meal_object1)
        db.session.commit()

        app_menu = json.dumps({
            'menu_name': 'Jojo Restaurant Special Friday',
            'date': '2018-05-12',
            'description': 'For our special friday, enjoy the menu with a free dessert',
            'meal_id': 2
        })
        self.client.post('/api/v1/menu/', data=app_menu, headers=header)

        app_menu_two = json.dumps({
            'menu_name': 'Jojo Restaurant Special Friday',
            'date': '2018-05-12',
            'description': 'For our special friday, enjoy the menu with a free dessert',
            'meal_id': 3
        })
        self.client.post('/api/v1/menu/', data=app_menu_two, headers=header)

    def add_mock_meal_options(self):
        meal_object = Meal('Fish with Gnuts', 23000, 1)
        meal_object1 = Meal('Fish with Greens', 25000, 1)
        db.session.add(meal_object)
        db.session.commit()
        db.session.add(meal_object1)
        db.session.commit()

    def add_mock_menu(self, header):
        self.mock_signup()
        self.mock_login()

        # Testing setting the menu of the day with meals
        app_meal_one = json.dumps({
            'meal': 'Fish with All foods',
            'price': 25000
        })
        self.client.post('/api/v1/meals/', data=app_meal_one, headers=header)

        app_menu = json.dumps({
            'menu_name': 'Jojo Restaurant Special Friday',
            'date': '2018-05-12',
            'description': 'For our special friday, enjoy the menu with a free dessert',
            'meal_id': 1
        })
        self.client.post('/api/v1/menu/', data=app_menu, headers=header)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
