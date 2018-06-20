import json
from v1.tests.base_case_test import BaseCaseTest

class MenuTests(BaseCaseTest):

	""" MENU OPERATION TESTS """
	def test_set_menu_of_the_day(self):
		self.mock_signup()
		self.mock_login()

		#Testing setting the menu of the day with meals
		app_meal_one = json.dumps({
			'meal': 'Fish with All foods',
			'price': 25000
		})

		response_one = self.client.post('/api/v1/meals/', data = app_meal_one, headers = self.headers)
		self.assertEqual(response_one.status_code, 201)

		app_menu = json.dumps({
			'menu_name': 'Jojo Restaurant Special Friday',
			'date': '2018-05-12',
			'description': 'For our special friday, enjoy the menu with a free dessert',
			'meal_id': 1
		})

		response = self.client.post('/api/v1/menu/', data = app_menu, headers = self.headers)
		self.assertEqual(response.status_code, 201)
		self.assertIn("success", str(response.data))

	def test_setting_empty_menu(self):
		self.mock_signup()
		self.mock_login()

		#Testing setting the menu of the day with meals
		app_meal_one = json.dumps({
			'meal': 'Fish with All foods',
			'price': 25000
		})

		response_one = self.client.post('/api/v1/meals/', data = app_meal_one, headers = self.headers)
		self.assertEqual(response_one.status_code, 201)


		app_menu = json.dumps({
			'menu_name': '',
			'date': '',
			'description': '',
			'meal_id': ''
		})

		response = self.client.post('/api/v1/menu/', data = app_menu, headers = self.headers)
		self.assertEqual(response.status_code, 400)
		self.assertIn("Empty Menu Details.", str(response.data))

	def test_setting_menu_of_the_day_with_empty_request_parameters(self):
		self.mock_signup()
		self.mock_login()

		#Creating a menu with Empty Request parameters should not go ahead to execute
		app_meal_one = json.dumps({
			'meal': 'Fish with All foods',
			'price': 25000
		})

		response_one = self.client.post('/api/v1/meals/', data = app_meal_one, headers = self.headers)
		self.assertEqual(response_one.status_code, 201)


		app_menu = json.dumps({
			'menu_na': 'Jojo Restaurant Special Friday',
			'da': 'Monday',
			'dription': 'For our special friday, enjoy the menu with a free dessert',
			'meal': 1
		})
		response = self.client.post('/api/v1/menu/', data = app_menu, headers = self.headers)
		result = json.loads(response.data.decode())
		self.assertEqual(response.status_code, 400)
		self.assertEqual(result['message'], 'Setting a Menu expects Menu name, date, description, and meal Id to add to the menu, either of them is not provided.')

	def test_get_menu_of_the_day(self):
		self.add_mock_menu()
		
		#Testing for retrieving the menu of the day
		menu_date = json.dumps({
			'date': '2018-05-12'
		})
		response_get = self.client.get('/api/v1/menu/', data = menu_date, headers = self.headers)
		self.assertEqual(response_get.status_code, 200)
		self.assertIn('1', str(response_get.data))

	def test_setting_menu_with_unauthorized_access(self):
		self.mock_signup()
		self.mock_login()

		#Testing setting the menu of the day with meals should not allow unauthorized access
		app_meal_one = json.dumps({
			'meal': 'Fish with All foods',
			'price': 25000
		})

		response_one = self.client.post('/api/v1/meals/', data = app_meal_one, headers = self.headers)
		self.assertEqual(response_one.status_code, 201)

		app_menu = json.dumps({
			'menu_name': 'Jojo Restaurant Special Friday',
			'date': '2018-05-12',
			'description': 'For our special friday, enjoy the menu with a free dessert',
			'meal_id': 1
		})

		response = self.client.post('/api/v1/menu/', data = app_menu, headers = self.unauthorized_user_token_headers)
		self.assertEqual(response.status_code, 401)
		self.assertIn("You need to login as Admin to perform this operation.", str(response.data))