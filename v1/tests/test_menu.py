import json
from v1.tests.base_case_test import BaseCaseTest

class MenuTests(BaseCaseTest):

	""" MENU OPERATION TESTS """
	def test_set_menu_of_the_day(self):
		#Testing setting the menu of the day with meals
		self.mock_signup()
		login = self.mock_login()
		login_response = json.loads(login.get_data(as_text=True))

		response_one = self.client.post('/api/v1/meals/', data = self.fish_meal, headers = self.headers_with_token(login_response['token']))

		response = self.client.post('/api/v1/menu/', data = self.app_menu, headers = self.headers_with_token(login_response['token']))
		self.assertEqual(response.status_code, 201)
		self.assertIn("success", str(response.data))

	def test_get_menu_of_the_day(self):
		#Testing for retrieving the menu of the day
		self.mock_signup()
		login = self.mock_login()
		login_response = json.loads(login.get_data(as_text=True))

		response_add = self.client.post('/api/v1/menu/', data = self.app_menu, headers = self.headers_with_token(login_response['token']))

		response_get = self.client.get('/api/v1/menu/', headers = self.headers_with_token(login_response['token']))
		self.assertEqual(response_get.status_code, 200)
		self.assertIn('"Fish with All foods', str(response_get.data))

	def test_setting_empty_menu(self):
		#Testing setting the menu of the day with meals
		self.mock_signup()
		login = self.mock_login()
		login_response = json.loads(login.get_data(as_text=True))

		response = self.client.post('/api/v1/menu/', data = self.empty_app_menu, headers = self.headers_with_token(login_response['token']))
		self.assertEqual(response.status_code, 400)
		self.assertIn("Empty Menu Details.", str(response.data))

	def test_setting_menu_of_the_day_with_empty_request_parameters(self):
		#Creating a menu with Empty Request parameters should not go ahead to execute
		self.mock_signup()
		login = self.mock_login()
		login_response = json.loads(login.get_data(as_text=True))

		response = self.client.post('/api/v1/menu/', data = self.wrong_menu_request_params, headers = self.headers_with_token(login_response['token']))
		result = json.loads(response.data.decode())
		self.assertEqual(response.status_code, 400)
		self.assertEqual(result['message'], 'Setting a Menu expects Menu name, date, description, and meal Id to add to the menu, either of them is not provided.')
