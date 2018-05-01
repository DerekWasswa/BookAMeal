import unittest
import json
from app import app

class AppTest(unittest.TestCase):
    
	def setUp(self):
		#Set up the globally used variables for use
		self.client = app.test_client()
		self.headers = {
			'Content-Type': 'application/json',
			'Authorization': 'Basic auth',
			'app-access-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhZG1pbiI6dHJ1ZSwiZW1haWwiOiJhbm5hYmVsbGFAZ21haWwuY29tIn0.23Dp0dP3TSYMCZIEfSEmKyD4kxSZU867cRXYDjzZ0AI'
		}

	""" USER REGISTRATION TESTS """
	def test_registration(self):
		#User registration should complete successfully
		user_data = json.dumps({
			'user_name': 'example',
			'email': 'test@example.com',
			'password': '12345',
			'admin': True
		})
		response = self.client.post('/auth/signup', data = user_data)
		result = json.loads(response.data.decode())
		self.assertEqual(response.status_code, 201)
		self.assertIn(result['message'], 'Successfully Registered. Please login')

	def test_registration_with_existing_user(self):
		#A user with the same email can not register more than once
		user_data = json.dumps({
			'user_name': 'Wasswa Derick',
			'email': 'wasswadero@gmail.com',
			'password': '12345',
			'admin': False
		})
		response_post = self.client.post('/auth/signup', data = user_data)
		self.assertEqual(response_post.status_code, 201)
		response_post_two = self.client.post('/auth/signup', data = user_data)
		self.assertEqual(response_post_two.status_code, 200)
		result = json.loads(response_post_two.data.decode())
		self.assertEqual(result['message'], "User already exists. Please login.")

	def test_user_registration_with_empty_credentials(self):
		#User should not register with missing credentials
		user_data = json.dumps({
			'user_name': '',
			'email': '',
			'password': '',
			'admin': ''
		})
		response = self.client.post('/auth/signup', data = user_data)
		self.assertEqual(response.status_code, 400)
		result = json.loads(response.data.decode())
		self.assertEqual(result['message'], "Missing Credentials")		




	""" USER LOGIN TESTS """
	def test_user_login_with_empty_credentials(self):
		#User should not login with missing credentials
		user_data = json.dumps({
			'user_name': '',
			'email': '',
			'password': '',
			'admin': ''
		})
		response = self.client.post('/auth/login', data = user_data)
		self.assertEqual(response.status_code, 401)
		result = json.loads(response.data.decode())
		self.assertEqual(result['message'], "Could not verify. Login credentials required.")		

	def test_user_login(self):
		#Test a registered user can be able to login
		user_data = json.dumps({
			'user_name': 'Derreck',
			'email': 'derrekwasswa@gmail.com',
			'password': '12345',
			'admin': True
		})
		response = self.client.post('/auth/signup', data = user_data)
		self.assertEqual(response.status_code, 201)

		user_login_response = self.client.post('/auth/login', data = user_data)
		result = json.loads(user_login_response.get_data(as_text=True))
		self.assertEqual(user_login_response.status_code, 200)		
		self.assertEqual(result['message'], 'Logged in successfully')





	""" MEALS OPERATIONS TESTS """
	def test_getting_all_meals(self):
		#Testing for retrieving all the available meals
		app_meals = json.dumps({
			'meal': 'Beef with Chicken',
			'price': '20000'
		})

		response_add = self.client.post('/meals/', data = app_meals, headers = self.headers)
		self.assertEqual(response_add.status_code, 201)
		response_get = self.client.get('/meals/', headers = self.headers)
		self.assertEqual(response_get.status_code, 200)
		self.assertIn('Beef with Chicken', str(response_get.data))

	def test_adding_a_meal_option(self):
		#Testing addition of a meal option
		app_meal = json.dumps({
			'meal': 'Fish with All foods',
			'price': '25000'
		})

		response = self.client.post('/meals/', data = app_meal, headers = self.headers)
		self.assertEqual(response.status_code, 201)
		self.assertIn("Fish with All foods", str(response.data))
		self.assertIn('Meal Added Successfully', str(response.data))		

	def test_modifying_a_meal_option(self):
		#Test that the API allows modification of a meal option by its ID
		app_meal = json.dumps({
			'meal': 'Luwombo with Matooke',
			'price': '25000'
		})
		update_meal = json.dumps({
			'meal_update': 'Luwombo with All Local Foods'
		})
		response = self.client.post('/meals/', data = app_meal, headers = self.headers)
		self.assertEqual(response.status_code, 201)

		posted_data = json.loads(response.get_data(as_text=True))

		response_edit_meal = self.client.put(
			'/meals/{}' . format(posted_data['meal']),
			data = update_meal, 
			headers = self.headers
			)
		self.assertEqual(response_edit_meal.status_code, 200)

		results_get_meals = self.client.get('/meals/', headers = self.headers)
		self.assertIn("Luwombo with All", str(results_get_meals.data))		

	def test_deleting_a_meal_option(self):
		#Test that the API allows for deletion of a meal option
		app_meal = json.dumps({
			'meal': 'Luwombo with Irish',
			'price': '25000'
		})

		response = self.client.post('/meals/', data = app_meal, headers = self.headers)
		self.assertEqual(response.status_code, 201)

		posted_data = json.loads(response.get_data(as_text=True))	

		response_delete_meal = self.client.delete('/meals/{}' . format(posted_data['meal']), headers = self.headers)
		self.assertEqual(response_delete_meal.status_code, 200)

		#Now retrieve to see to it exists: Should Return Not Found - 404
		response_get = self.client.get('/meals/{}' . format(posted_data['meal']), headers = self.headers)
		self.assertEqual(response_get.status_code, 404)





	""" MENU OPERATION TESTS """
	def test_set_menu_of_the_day(self):
		#Testing setting the menu of the day with meals
		app_meal = json.dumps({
			'meal': 'Fish with All foods',
			'price': '25000'
		})

		response = self.client.post('/menu/', data = app_meal, headers = self.headers)
		self.assertEqual(response.status_code, 201)
		self.assertIn("Fish with All foods", str(response.data))

	def test_get_menu_of_the_day(self):
		#Testing for retrieving the menu of the day
		app_menu = json.dumps({
			'meal': 'Beef with Gnuts',
			'price': '15000'
		})
		response_add = self.client.post('/menu/', data = app_menu, headers = self.headers)
		self.assertEqual(response_add.status_code, 201)
		response_get = self.client.get('/menu/', headers = self.headers)
		self.assertEqual(response_get.status_code, 200)
		self.assertIn('Beef with Gnuts', str(response_get.data))






	""" ORDER OPERATION TESTS """
	def test_make_order(self):
		#Testing making an order from the menu
		app_menu = json.dumps({
			'meal': 'Fish with All foods',
			'price': '25000',
			'user': 'wasswadero@gmail.com'
		})

		response = self.client.post('/orders/', data = app_menu)
		self.assertEqual(response.status_code, 201)
		self.assertIn("Fish with All foods", str(response.data))

	def test_modifying_an_order(self):
		#Test that the API allows modification of an order
		app_menu = json.dumps({
			'user': 'wasswadero@gmail',
			'meal': 'Luwombo with Matooke',
			'price': '25000'
		})

		order_update = json.dumps({
			'order_to_update': 'Luwombo with All foods'
		})
		response = self.client.post('/orders/', data = app_menu)
		self.assertEqual(response.status_code, 201)

		posted_data = json.loads(response.get_data(as_text=True))

		response_edit_order = self.client.put(
			'/orders/{}' . format(posted_data['orderId']),
			data = order_update
		)
		self.assertEqual(response_edit_order.status_code, 200)

		results_get_order_by_id = self.client.get('/orders/')
		self.assertIn("Luwombo with All", str(results_get_order_by_id.data))

	def test_getting_all_orders(self):
		#Testing for retrieving all the ORDERS
		app_orders = json.dumps({
			'user': 'test@example.com',
			'meal': 'Beef with Chicken',
			'price': '20000'
		})
		response_add = self.client.post('/orders/', data = app_orders)
		self.assertEqual(response_add.status_code, 201)
		response_get_orders = self.client.get('/orders/')
		self.assertEqual(response_get_orders.status_code, 200)
		self.assertIn('Beef with Chicken', str(response_get_orders.data))


if __name__ == '__main__':
	unittest.main()
		