import unittest
import json
from flask import session
from v1.api import create_app
from v1.api import db
from v1.api.models import User, Meal, Menu, Order

class BaseCaseTest(unittest.TestCase):
    
	def setUp(self):
		#Set up the globally used variables for use
		app = create_app('testing')
		self.client = app.test_client()
		db.create_all()
		self.headers = {
			'Content-Type': 'application/json',
			'Authorization': 'Basic auth',
			'app-access-token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJhZG1pbiI6InRydWUifQ.W0EoWSsYbSlS8fSRWJsV77cBqbfNg8Iy2txp_9BdBzM'
		}

		self.meals_mock_data1 = {
			'meal': 'Luwombo with Matooke',
			'price': 25000
		}

		self.meals_mock_data2 = {
			'meal': 'Luwombo with Irish',
			'price': 25000
		}

		self.meal_mock_data3 = {
			'meal': 'Beef with Chicken',
			'price': 20000
		}


	def mock_signup(self):
		user_data = json.dumps({
			'username': 'derreckwasswa',
			'email': 'derrekwasswa256@gmail.com',
			'password': '12345',
			'admin': True
		})
		self.client.post('/api/v1/auth/signup', data = user_data)

	def mock_login(self):
		user_data = json.dumps({
			'email': 'derrekwasswa256@gmail.com',
			'password': '12345',
			'admin': True
		})
		self.client.post('/api/v1/auth/login', data = user_data)

	def add_mock_meals_to_menu(self):
		meals_mock_data = {
			'meal': 'Chips and Chicken',
			'price': 25000
		}
		self.client.post('/api/v1/meals/', data = meals_mock_data, headers = self.headers)
		app_menu = json.dumps({
			'menu_name': 'Jojo Restaurant Special Friday',
			'date': '2018-05-12',
			'description': 'For our special friday, enjoy the menu with a free dessert',
			'meal_id': 2
		})
		self.client.post('/api/v1/menu/', data = app_menu, headers = self.headers)

	def add_mock_menu(self):
		self.mock_signup()
		self.mock_login()

		#Testing setting the menu of the day with meals
		app_meal_one = json.dumps({
			'meal': 'Fish with All foods',
			'price': 25000
		})
		self.client.post('/api/v1/meals/', data = app_meal_one, headers = self.headers)

		app_menu = json.dumps({
			'menu_name': 'Jojo Restaurant Special Friday',
			'date': '2018-05-12',
			'description': 'For our special friday, enjoy the menu with a free dessert',
			'meal_id': 1
		})
		self.client.post('/api/v1/menu/', data = app_menu, headers = self.headers)

	def add_mock_meals(self):
		meal_object = Meal('Fish with Macs', 23000, 1)
		meal_object1 = Meal('Fish with Flies', 25000, 1)
		meal_object2 = Meal('Fish with Spags', 27000, 1)
		db.session.add(meal_object)
		db.session.commit()

	def tearDown(self):
		db.session.remove()
		db.drop_all()