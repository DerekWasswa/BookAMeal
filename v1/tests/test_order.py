import json
from v1.tests.base_case_test import BaseCaseTest

class MealTests(BaseCaseTest):

	""" ORDER OPERATION TESTS """
	def test_make_order(self):
		#Testing making an order from the menu
		response = self.client.post('/api/v1/orders/', data = self.order)
		self.assertEqual(response.status_code, 201)
		self.assertIn("Fish with All foods", str(response.data))

	def test_modifying_an_order(self):
		#Test that the API allows modification of an order
		self.mock_signup()
		login = self.mock_login()
		login_response = json.loads(login.get_data(as_text=True))

		response = self.client.post('/api/v1/orders/', data = self.order)
		posted_data = json.loads(response.get_data(as_text=True))

		response_edit_order = self.client.put(
			'/api/v1/orders/{}' . format(posted_data['order']['order_id']),
			data = self.order_update
		)
		self.assertEqual(response_edit_order.status_code, 202)

		results_get_order_by_id = self.client.get('/api/v1/orders/', headers = self.headers_with_token(login_response['token']))
		self.assertIn(str(posted_data['order']['order_id']), str(results_get_order_by_id.data))

	def test_getting_all_orders(self):
		#Testing for retrieving all the ORDERS
		self.mock_signup()
		login = self.mock_login()
		login_response = json.loads(login.get_data(as_text=True))

		app_orders = json.dumps({
			'user': 'test@example.com',
			'meal': "Kalo",
			"price": 4500
		})
		response_add = self.client.post('/api/v1/orders/', data = app_orders)

		response_get_orders = self.client.get('/api/v1/orders/', headers = self.headers_with_token(login_response['token']))
		self.assertEqual(response_get_orders.status_code, 200)
		self.assertIn('1', str(response_get_orders.data))

	def test_making_order_with_empty_fields(self):
		#Testing making an order from the menu with empty content
		response = self.client.post('/api/v1/orders/', data = self.empty_order)
		result = json.loads(response.data.decode())
		self.assertEqual(response.status_code, 400)
		self.assertEqual(result['message'], 'Can not order with empty content.')

	def test_modifying_order_with_empty_order_content(self):
		#Test modifying an order with empty order content
		response = self.client.post('/api/v1/orders/', data = self.order)

		posted_data = json.loads(response.get_data(as_text=True))

		response_edit_order = self.client.put(
			'/api/v1/orders/{}' . format(posted_data['order']['order_id']),
			data = self.order_update_empty
		)

		result = json.loads(response_edit_order.data.decode())
		self.assertEqual(response_edit_order.status_code, 400)
		self.assertEqual(result['message'], 'Can not modify an order with empty content.')

	def test_making_order_with_invalid_emails(self):
		#Testing making an order from the menu does not allow users with invalid emails

		response = self.client.post('/api/v1/orders/', data = self.order_invalid_email)
		result = json.loads(response.data.decode())
		self.assertEqual(response.status_code, 400)
		self.assertIn(result['message'], 'User Email not valid.')

	def test_making_orders_with_empty_request_parameters(self):
		#Making an order with Empty Request parameters should not go ahead to execute

		response = self.client.post('/api/v1/orders/', data = self.wrong_order_request_params)
		result = json.loads(response.data.decode())
		self.assertEqual(response.status_code, 400)
		self.assertEqual(result['message'], 'Making Order expects user email, meal id and either of them is not provided.')

	def test_order_modification_with_empty_request_parameters(self):
		#Order modification with Empty Request parameters should not go ahead to execute
		response = self.client.post('/api/v1/orders/', data = self.order)

		posted_data = json.loads(response.get_data(as_text=True))
		response_edit_order = self.client.put(
			'/api/v1/orders/{}' . format(posted_data['order']['order_id']),
			data = self.wrong_order_update_request_params
		)
		result = json.loads(response_edit_order.data.decode())
		self.assertEqual(response_edit_order.status_code, 400)
		self.assertEqual(result['message'], 'Modifying order expects the order id to edit with which is not provided.')
