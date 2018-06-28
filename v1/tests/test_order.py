import json
from v1.tests.base_case_test import BaseCaseTest

class OrderTests(BaseCaseTest):

	""" ORDER OPERATION TESTS """
	def test_make_order(self):
		#Testing making an order from the menu
		self.mock_signup()
		login = self.mock_login()
		login_response = json.loads(login.get_data(as_text=True))
		self.add_mock_menu(self.headers_with_token(login_response['token']))
		self.add_mock_meals_to_menu(self.headers_with_token(login_response['token']))

		response = self.client.post('/api/v1/orders/', data = self.app_order)
		self.assertEqual(response.status_code, 201)

	def test_make_order_where_menu_id_not_existing(self):
		'''' verify that a user cannot order for a meal whose menu doesnot exist '''
		self.mock_signup()
		login = self.mock_login()
		login_response = json.loads(login.get_data(as_text=True))
		self.add_mock_menu(self.headers_with_token(login_response['token']))
		self.add_mock_meals_to_menu(self.headers_with_token(login_response['token']))

		app_order = json.dumps({
			'user': 'derrekwasswa256@gmail.com',
			'meal': 2,
			'date': '2018-05-12',
			'menu_id': 10
		})

		response = self.client.post('/api/v1/orders/', data = app_order)
		self.assertEqual(response.status_code, 400)
		self.assertIn('Menu ID does not exist.', str(response.data))

	def test_make_order_where_meal_id_is_not_in_the_menu(self):
		'''' verify that a user cannot order for a meal which is not on the menu '''
		self.mock_signup()
		login = self.mock_login()
		login_response = json.loads(login.get_data(as_text=True))
		self.add_mock_menu(self.headers_with_token(login_response['token']))
		self.add_mock_meals_to_menu(self.headers_with_token(login_response['token']))

		app_order = json.dumps({
			'user': 'derrekwasswa256@gmail.com',
			'meal': 25,
			'date': '2018-05-12',
			'menu_id': 1
		})

		response = self.client.post('/api/v1/orders/', data = app_order)
		self.assertEqual(response.status_code, 400)
		self.assertIn('Meal ID does not exist in the menu of the day', str(response.data))

	def test_modifying_an_order(self):
		#Test that the API allows modification of an order
		self.mock_signup()
		login = self.mock_login()
		login_response = json.loads(login.get_data(as_text=True))
		self.add_mock_menu(self.headers_with_token(login_response['token']))
		self.add_mock_meals_to_menu(self.headers_with_token(login_response['token']))

		order_update = json.dumps({
			'order_to_update': 3,
			'user': 'derrekwasswa256@gmail.com',
			'menu_id': 1,
			'meal_id': 2
		})
		response = self.client.post('/api/v1/orders/', data = self.app_order)
		posted_data = json.loads(response.get_data(as_text=True))

		response_edit_order = self.client.put(
			'/api/v1/orders/{}' . format(posted_data['order']['order_id']),
			data = order_update
		)

		self.assertEqual(response_edit_order.status_code, 202)
		results_get_order_by_id = self.client.get('/api/v1/orders/', headers = self.headers_with_token(login_response['token']))
		self.assertIn(str(posted_data['order']['order_id']), str(results_get_order_by_id.data))

	def test_modify_order_where_orders_are_empty(self):
		''' verify that attempts to update orders fail where there are no orders '''
		order_update = json.dumps({
			'order_to_update': 3,
			'user': 'derrekwasswa256@gmail.com',
			'menu_id': 1,
			'meal_id': 2
		})
		response_edit_order = self.client.put(
			'/api/v1/orders/{}' . format(1),
			data = order_update
		)

		self.assertEqual(response_edit_order.status_code, 200)
		self.assertIn('Orders are Empty', str(response_edit_order.data))

	def test_making_order_with_empty_fields(self):
		#Testing making an order from the menu with empty content
		self.mock_signup()
		self.mock_login()

		app_menu = json.dumps({
			'meal': '',
			'date': '',
			'user': '',
			'menu_id': ''
		})
		response = self.client.post('/api/v1/orders/', data = app_menu)

		result = json.loads(response.data.decode())
		self.assertEqual(response.status_code, 400)
		self.assertEqual(result['message'], 'Can not order with empty content.')

	def test_modifying_order_with_empty_order_content(self):
		#Test modifying an order with empty order content
		self.mock_signup()
		login = self.mock_login()
		login_response = json.loads(login.get_data(as_text=True))
		self.add_mock_menu(self.headers_with_token(login_response['token']))
		self.add_mock_meals_to_menu(self.headers_with_token(login_response['token']))

		app_order = json.dumps({
			'user': 'derrekwasswa256@gmail.com',
			'meal': 3,
			'date': '20180515',
			'menu_id': 1
		})

		order_update = json.dumps({
			'order_to_update': '',
			'user': '',
			'menu_id': '',
			'meal_id': ''
		})
		response = self.client.post('/api/v1/orders/', data = app_order)
		posted_data = json.loads(response.get_data(as_text=True))

		response_edit_order = self.client.put(
			'/api/v1/orders/{}' . format(posted_data['order']['order_id']),
			data = order_update
		)

		result = json.loads(response_edit_order.data.decode())
		self.assertEqual(response_edit_order.status_code, 400)
		self.assertEqual(result['message'], 'Can not modify an order with empty content.')

	def test_making_order_with_valid_email_and_order_id_of_type_int(self):
		#Testing making an order from the menu does not allow users with invalid emails
		self.mock_signup()
		self.mock_login()

		app_menu = json.dumps({
			'meal': 2,
			'user': 'wasswadero',
			'date': '2018-05-15',
			'menu_id': 1
		})
		response = self.client.post('/api/v1/orders/', data = app_menu)

		result = json.loads(response.data.decode())
		self.assertEqual(response.status_code, 400)
		self.assertIn(result['message'], 'User Email not valid.')

	def test_making_orders_with_empty_request_parameters(self):
		#Making an order with Empty Request parameters should not go ahead to execute
		self.mock_signup()
		self.mock_login()

		app_order = json.dumps({
			'us': 'derrekwasswa256@gmail',
			'me': 1,
			'da': '20180515',
			'menu_': 1
		})
		response = self.client.post('/api/v1/orders/', data = app_order)
		result = json.loads(response.data.decode())

		self.assertEqual(response.status_code, 400)
		self.assertEqual(result['message'], 'Making Order expects; user email, meal id, menu_id, and date keys.')

	def test_order_modification_with_empty_request_parameters(self):
		#Order modification with Empty Request parameters should not go ahead to execute
		self.mock_signup()
		login = self.mock_login()
		login_response = json.loads(login.get_data(as_text=True))
		self.add_mock_menu(self.headers_with_token(login_response['token']))
		self.add_mock_meals_to_menu(self.headers_with_token(login_response['token']))

		app_order = json.dumps({
			'user': 'derrekwasswa256@gmail.com',
			'meal': 3,
			'date': '2015-05-15',
			'menu_id': 1
		})

		order_update = json.dumps({
			'order_to': 2,
			'us': 'derrekwasswa256@gmail.com',
			'men': 1,
			'mea': 1
		})
		response = self.client.post('/api/v1/orders/', data = app_order)
		posted_data = json.loads(response.get_data(as_text=True))

		response_edit_order = self.client.put(
			'/api/v1/orders/{}' . format(posted_data['order']['order_id']),
			data = order_update
		)
		result = json.loads(response_edit_order.data.decode())
		self.assertEqual(response_edit_order.status_code, 400)
		self.assertEqual(result['message'], 'Modifying order expects the order id, user, menu id, meal id to edit with which is not provided.')

	def test_getting_all_orders(self):
		#Testing for retrieving all the ORDERS
		self.mock_signup()
		login = self.mock_login()
		login_response = json.loads(login.get_data(as_text=True))
		self.add_mock_menu(self.headers_with_token(login_response['token']))
		self.add_mock_meals_to_menu(self.headers_with_token(login_response['token']))

		response_add = self.client.post('/api/v1/orders/', data = self.app_order)

		response_get_orders = self.client.get('/api/v1/orders/', headers = self.headers_with_token(login_response['token']))
		self.assertEqual(response_get_orders.status_code, 200)
		self.assertIn('2', str(response_get_orders.data))

	def test_getting_all_orders_with_authorized_access(self):
		#Testing for retrieving all the ORDERS
		self.mock_signup()
		login = self.mock_login()
		login_response = json.loads(login.get_data(as_text=True))
		unpriviledged = self.unpriviledged_mock_login()
		unpriviledged_response = json.loads(unpriviledged.get_data(as_text=True))
		self.add_mock_menu(self.headers_with_token(login_response['token']))
		self.add_mock_meals_to_menu(self.headers_with_token(login_response['token']))

		response_add = self.client.post('/api/v1/orders/', data = self.app_order)

		response_get_orders = self.client.get('/api/v1/orders/', headers = self.headers_with_token(unpriviledged_response['token']))
		self.assertEqual(response_get_orders.status_code, 401)
		self.assertIn("You need to login as Admin to perform this operation.", str(response_get_orders.data))

	def test_making_order_with_unauthorized_user(self):
		#Testing making an order from the menu
		self.mock_signup()
		login = self.mock_login()
		login_response = json.loads(login.get_data(as_text=True))
		self.add_mock_menu(self.headers_with_token(login_response['token']))
		self.add_mock_meals_to_menu(self.headers_with_token(login_response['token']))

		app_order = json.dumps({
			'user': 'derrekwasswa@andela.com',
			'meal': 2,
			'date': '2018-05-12',
			'menu_id': 1
		})

		response = self.client.post('/api/v1/orders/', data = app_order)
		self.assertEqual(response.status_code, 401)
		self.assertIn("User doesnot exist or is not logged in.", str(response.data))
