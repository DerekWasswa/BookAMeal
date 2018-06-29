import unittest
import json
from v1.api import create_app

class BaseCaseTest(unittest.TestCase):

	def setUp(self):
		#Set up the globally used variables for use
		app = create_app()
		self.client = app.test_client()

		self.example_user_data = json.dumps({
			'username': 'example',
			'email': 'tests23@example.com',
			'password': '12345',
			'admin': True
		})

		self.user = json.dumps({
			'username': 'Wasswa',
			'email': 'wasswadero@gmail.com',
			'password': '12345678',
			'admin': True
		})

		self.empty_user_data = json.dumps({
			'username': '',
			'email': '',
			'password': '',
			'admin': ''
		})

		self.invalid_email_user_data = json.dumps({
			'username': 'example',
			'email': 'test',
			'password': '12345',
			'admin': True
		})

		self.wrong_request_params_user_data = json.dumps({
			'user': 'example',
			'ema': 'tester@example.com',
			'passwo': '12345',
			'admi': True
		})

		self.user_data_not_in_db = json.dumps({
			'username': 'invasionworld',
			'email': 'invasionworlds@gmail.com',
			'password': '12345',
			'admin': True
		})

		self.luwombo_meal = json.dumps({
			'meal': 'Luwombo with Matooke',
			'price': 25000
		})

		self.fish_meal = json.dumps({
			'meal': 'Fish with All foods',
			'price': 25000
		})

		self.empty_meal = json.dumps({
			'meal': '',
			'price': ''
		})

		self.beef_meals = json.dumps({
			'meal': 'Beef with Chicken',
			'price': 20000
		})

		self.update_meal = json.dumps({
			'meal_update': 'Luwombo with All Local Foods',
			'price_update': 20000
		})

		self.update_empty_meal = json.dumps({
			'meal_update': '',
			'price_update': ''
		})

		self.wrong_meal_request_params = json.dumps({
			'mea': 'Fish with All foods',
			'pric': 25000
		})

		self.update_meal_price_not_int = json.dumps({
			'meal_update': 'Luwombo with Chips',
			'price_update': "20000"
		})

		self.meal_addition_price_not_int = json.dumps({
			'meal': 'Bananas',
			'price': '12asu'
		})

		self.app_menu = json.dumps({
			'menu_name': 'Jojo Restaurant Special Friday',
			'date': 'Monday',
			'description': 'For our special friday, enjoy the menu with a free dessert',
			'meal_id': 1
		})

		self.empty_app_menu = json.dumps({
			'menu_name': '',
			'date': '',
			'description': '',
			'meal_id': ''
		})

		self.wrong_menu_request_params = json.dumps({
			'menu_na': 'Jojo Restaurant Special Friday',
			'da': 'Monday',
			'dription': 'For our special friday, enjoy the menu with a free dessert',
			'meal': 1
		})

		self.empty_order = json.dumps({
			'meal': '',
			'price': '',
			'user': ''
		})

		self.order = json.dumps({
			'user': 'wasswadero@gmail',
			'meal': 'Fish with All foods',
			'price': 25000
		})

		self.order_update = json.dumps({
			'order_to_update': 'Luwombo with All foods'
		})

		self.order_update_empty = json.dumps({
			'order_to_update': ''
		})

		self.wrong_order_request_params = json.dumps({
			'us': 'wasswadero@gmail',
			'me': 'Fish with All foods',
			'pri': 24000
		})

		self.wrong_order_update_request_params = json.dumps({
			'order_to': 'Luwombo with All foods'
		})

		self.order_invalid_email = json.dumps({
			'meal': "Luwombo",
			'user': 'wasswadero',
			"price": 5600
		})


	def mock_signup(self):
		user_data = json.dumps({
			'username': 'derreckwasswa',
			'email': 'derrekwasswa256@gmail.com',
			'password': '12345678',
			'admin': True
		})
		self.client.post('/api/v1/auth/signup', data = user_data)

	def mock_login(self):
		user_data = json.dumps({
			'email': 'derrekwasswa256@gmail.com',
			'password': '12345678',
			'admin': True
		})
		return self.client.post('/api/v1/auth/login', data = user_data)

	def headers_with_token(self, token):
		''' Return Header with a token value '''
		headers = {
			'Content-Type': 'application/json',
			'Authorization': 'Basic auth',
			'app-access-token': token
		}
		return headers
