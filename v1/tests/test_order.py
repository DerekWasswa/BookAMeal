import json
from v1.tests.base_case_test import BaseCaseTest

class OrderTests(BaseCaseTest):

	""" ORDER OPERATION TESTS """
	def test_make_order(self):
		#Testing making an order from the menu
		app_order = json.dumps({
			'user': 'wasswadero@gmail',
			'meal': 1,
			'date': '20180515',
			'menu_id': 1
		})

		response = self.client.post('/api/v1/orders/', data = app_order)
		self.assertEqual(response.status_code, 201)

	def test_modifying_an_order(self):
		#Test that the API allows modification of an order
		app_order = json.dumps({
			'user': 'wasswadero@gmail',
			'meal': 1,
			'date': '20180515',
			'menu_id': 1
		})

		order_update = json.dumps({
			'order_to_update': 2
		})
		response = self.client.post('/api/v1/orders/', data = app_order)
		self.assertEqual(response.status_code, 201)

		posted_data = json.loads(response.get_data(as_text=True))

		response_edit_order = self.client.put(
			'/api/v1/orders/{}' . format(posted_data['order']['order_id']),
			data = order_update
		)
		self.assertEqual(response_edit_order.status_code, 202)

		results_get_order_by_id = self.client.get('/api/v1/orders/', headers = self.headers)
		self.assertIn(str(posted_data['order']['order_id']), str(results_get_order_by_id.data))

	def test_getting_all_orders(self):
		#Testing for retrieving all the ORDERS
		app_orders = json.dumps({
			'user': 'test@example.com',
			'meal': 1,
			'date': '20180515',
			'menu_id': 1
		})
		response_add = self.client.post('/api/v1/orders/', data = app_orders)
		self.assertEqual(response_add.status_code, 201)
		response_get_orders = self.client.get('/api/v1/orders/', headers = self.headers)
		self.assertEqual(response_get_orders.status_code, 200)
		self.assertIn('1', str(response_get_orders.data))

	def test_making_order_with_empty_fields(self):
		#Testing making an order from the menu with empty content
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
		app_order = json.dumps({
			'user': 'wasswadero@gmail',
			'meal': 1,
			'date': '20180515',
			'menu_id': 1
		})

		order_update = json.dumps({
			'order_to_update': ''
		})
		response = self.client.post('/api/v1/orders/', data = app_order)
		self.assertEqual(response.status_code, 201)

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
		app_menu = json.dumps({
			'meal': "Luwombo",
			'user': 'wasswadero',
			'date': '20180515',
			'menu_id': 1
		})

		response = self.client.post('/api/v1/orders/', data = app_menu)
		result = json.loads(response.data.decode())
		self.assertEqual(response.status_code, 400)
		self.assertIn(result['message'], 'User Email not valid.')

	def test_making_orders_with_empty_request_parameters(self):
		#Making an order with Empty Request parameters should not go ahead to execute
		app_order = json.dumps({
			'us': 'wasswadero@gmail',
			'me': 1,
			'da': '20180515',
			'menu_': 1
		})
		response = self.client.post('/api/v1/orders/', data = app_order)
		result = json.loads(response.data.decode())
		self.assertEqual(response.status_code, 400)
		self.assertEqual(result['message'], 'Making Order expects user email, meal id and either of them is not provided.')
		
	def test_order_modification_with_empty_request_parameters(self):
		#Order modification with Empty Request parameters should not go ahead to execute
		app_order = json.dumps({
			'user': 'wasswadero@gmail',
			'meal': 1,
			'date': '20150515',
			'menu_id': 1
		})

		order_update = json.dumps({
			'order_to': 'Luwombo with All foods'
		})
		response = self.client.post('/api/v1/orders/', data = app_order)
		self.assertEqual(response.status_code, 201)

		posted_data = json.loads(response.get_data(as_text=True))
		response_edit_order = self.client.put(
			'/api/v1/orders/{}' . format(posted_data['order']['order_id']),
			data = order_update
		)
		result = json.loads(response_edit_order.data.decode())
		self.assertEqual(response_edit_order.status_code, 400)
		self.assertEqual(result['message'], 'Modifying order expects the order id to edit with which is not provided.')