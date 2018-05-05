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
			'username': 'example',
			'email': 'tests@example.com',
			'password': '12345',
			'admin': True
		})
		response = self.client.post('/api/v1/auth/signup', data = user_data)
		result = json.loads(response.data.decode())
		self.assertEqual(response.status_code, 201)
		self.assertIn(result['message'], 'Successfully Registered. Please login')

	def test_registration_with_existing_user(self):
		#A user with the same email can not register more than once
		user_data = json.dumps({
			'username': 'Wasswa Derick',
			'email': 'wasswadero@gmail.com',
			'password': '12345',
			'admin': False
		})
		response_post = self.client.post('/api/v1/auth/signup', data = user_data)
		self.assertEqual(response_post.status_code, 201)
		response_post_two = self.client.post('/api/v1/auth/signup', data = user_data)
		self.assertEqual(response_post_two.status_code, 200)
		result = json.loads(response_post_two.data.decode())
		self.assertEqual(result['message'], "User already exists. Please login.")

	def test_user_registration_with_empty_credentials(self):
		#User should not register with missing credentials
		user_data = json.dumps({
			'username': '',
			'email': '',
			'password': '',
			'admin': ''
		})
		response = self.client.post('/api/v1/auth/signup', data = user_data)
		self.assertEqual(response.status_code, 400)
		result = json.loads(response.data.decode())
		self.assertEqual(result['message'], "Missing Credentials")		

	def test_registration_for_invalid_emails(self):
		#User registration with invalid emails should show invalid email
		user_data = json.dumps({
			'username': 'example',
			'email': 'test',
			'password': '12345',
			'admin': True
		})
		response = self.client.post('/api/v1/auth/signup', data = user_data)
		result = json.loads(response.data.decode())
		self.assertEqual(response.status_code, 401)
		self.assertIn(result['message'], 'Email is Invalid')

	def test_registration_with_empty_request_parameters(self):
		#User Registration with Empty Request parameters should not go ahead to execute
		user_data = json.dumps({
			'user': 'example',
			'ema': 'test@example.com',
			'passwo': '12345',
			'admi': True
		})
		response = self.client.post('/api/v1/auth/signup', data = user_data)
		result = json.loads(response.data.decode())
		self.assertEqual(response.status_code, 400)
		self.assertIn(result['message'], 'Signup expects username, email, password, admin value, either of them is not provided.')






	""" USER LOGIN TESTS """
	def test_user_login_with_empty_credentials(self):
		#User should not login with missing credentials
		user_data = json.dumps({
			'username': '',
			'email': '',
			'password': '',
			'admin': ''
		})
		response = self.client.post('/api/v1/auth/login', data = user_data)
		self.assertEqual(response.status_code, 401)
		result = json.loads(response.data.decode())
		self.assertEqual(result['message'], "Could not verify. Login credentials required.")		

	def test_user_login(self):
		#Test a registered user can be able to login
		user_data = json.dumps({
			'username': 'derreckwasswa',
			'email': 'derrekwasswa@gmail.com',
			'password': '12345',
			'admin': True
		})
		response = self.client.post('/api/v1/auth/signup', data = user_data)
		self.assertEqual(response.status_code, 201)

		user_login_response = self.client.post('/api/v1/auth/login', data = user_data)
		result = json.loads(user_login_response.get_data(as_text=True))
		self.assertEqual(user_login_response.status_code, 200)		
		self.assertEqual(result['message'], 'Logged in successfully')

	def test_user_login_with_user_who_does_not_exist(self):
		#Test a registered user can be able to login
		user_data = json.dumps({
			'username': 'invasionworld',
			'email': 'invasionworld@gmail.com',
			'password': '12345',
			'admin': True
		})

		user_login_response = self.client.post('/api/v1/auth/login', data = user_data)
		result = json.loads(user_login_response.get_data(as_text=True))
		self.assertEqual(user_login_response.status_code, 401)		
		self.assertEqual(result['message'], 'User email not found!!')

	def test_login_for_invalid_emails(self):
		#User login with invalid emails should show invalid email
		user_data = json.dumps({
			'username': 'example',
			'email': 'tests',
			'password': '12345',
			'admin': True
		})
		response = self.client.post('/api/v1/auth/login', data = user_data)
		result = json.loads(response.data.decode())
		self.assertEqual(response.status_code, 401)
		self.assertIn(result['message'], 'Email is Invalid')

	def test_login_with_empty_request_parameters(self):
		#User Login with Empty Request parameters should not go ahead to execute
		user_data = json.dumps({
			'username': 'example',
			'email': 'test@example.com',
			'password': '12345',
			'admin': True
		})

		login_data = json.dumps({
			'use': 'example',
			'em': 'test@example.com',
			'passd': '12345',
			'ain': True
		})		
		response = self.client.post('/api/v1/auth/signup', data = user_data)
		self.assertEqual(response.status_code, 201)

		user_login_response = self.client.post('/api/v1/auth/login', data = login_data)
		result = json.loads(user_login_response.get_data(as_text=True))
		self.assertEqual(user_login_response.status_code, 400)		
		self.assertEqual(result['message'], 'Logged requests expects email, password, and admin value. Either of them id not provided.')





	""" MEALS OPERATIONS TESTS """
	def test_modifying_a_meal_option(self):
		#Test that the API allows modification of a meal option by its ID should modify the meal by both the meal name and price
		app_meal = json.dumps({
			'meal': 'Luwombo with Matooke',
			'price': 25000
		})
		update_meal = json.dumps({
			'meal_update': 'Luwombo with All Local Foods',
			'price_update': 20000
		})
		response = self.client.post('/api/v1/meals/', data = app_meal, headers = self.headers)
		self.assertEqual(response.status_code, 201)

		posted_data = json.loads(response.get_data(as_text=True))
		
		response_edit_meal = self.client.put('/api/v1/meals/{}' . format(posted_data['meal']['meal_id']),
			data = update_meal,
			headers = self.headers
		)
		self.assertEqual(response_edit_meal.status_code, 200)

		results_get_meals = self.client.get('/api/v1/meals/', headers = self.headers)
		self.assertIn('Luwombo with All', str(results_get_meals.data))		

	def test_deleting_a_meal_option(self):
		#Test that the API allows for deletion of a meal option should delete a meal by the ID
		app_meal = json.dumps({
			'meal': 'Luwombo with Irish',
			'price': 25000
		})

		response = self.client.post('/api/v1/meals/', data = app_meal, headers = self.headers)
		self.assertEqual(response.status_code, 201)

		posted_data = json.loads(response.get_data(as_text=True))	

		response_delete_meal = self.client.delete('/api/v1/meals/{}' . format(posted_data['meal']['meal_id']), headers = self.headers)
		self.assertEqual(response_delete_meal.status_code, 200)

		#Now retrieve to see to it exists: Should Return Not Found - 404
		response_get = self.client.get('/api/v1/meals/{}' . format(posted_data['meal']['meal_id']), headers = self.headers)
		self.assertEqual(response_get.status_code, 404)

	def test_getting_all_meals(self):
		#Testing for retrieving all the available meals should return all meals
		app_meals = json.dumps({
			'meal': 'Beef with Chicken',
			'price': 20000
		})

		response_add = self.client.post('/api/v1/meals/', data = app_meals, headers = self.headers)
		self.assertEqual(response_add.status_code, 201)
		response_get = self.client.get('/api/v1/meals/', headers = self.headers)
		self.assertEqual(response_get.status_code, 200)
		self.assertIn('Beef with Chicken', str(response_get.data))

	def test_adding_a_meal_option(self):
		#Testing addition of a meal option should add
		app_meal = json.dumps({
			'meal': 'Fish with All foods',
			'price': 25000
		})

		response = self.client.post('/api/v1/meals/', data = app_meal, headers = self.headers)
		self.assertEqual(response.status_code, 201)
		self.assertIn("Fish with All foods", str(response.data))
		self.assertIn('Meal Added Successfully', str(response.data))		

	def test_adding_empty_meal_options(self):
		#Testing addition of a meal option with missing content should not pass
		app_meal = json.dumps({
			'meal': '',
			'price': ''
		})

		response = self.client.post('/api/v1/meals/', data = app_meal, headers = self.headers)
		result = json.loads(response.data.decode())
		self.assertEqual(response.status_code, 400)	
		self.assertIn(result['message'], 'Meal Options Missing.')	

	def test_adding_meal_price_that_is_not_an_int(self):
		#Testing addition of a meal option with a price that is not empty should not pass
		app_meal = json.dumps({
			'meal': 'Bananas',
			'price': '12asu'
		})

		response = self.client.post('/api/v1/meals/', data = app_meal, headers = self.headers)
		result = json.loads(response.data.decode())
		self.assertEqual(response.status_code, 400)		
		self.assertIn(result['message'], 'Meal Price has to be an Integer.')	

	def test_modifying_a_meal_with_empty_meal_options(self):
		#MODIFYING A MEAL OPTIONS WITH EMPTY DATA SHOULD NOT ACCEPT
		app_meal = json.dumps({
			'meal': 'Luwombo with Matooke',
			'price': 25000
		})
		update_meal = json.dumps({
			'meal_update': '',
			'price_update': ''
		})
		response = self.client.post('/api/v1/meals/', data = app_meal, headers = self.headers)
		self.assertEqual(response.status_code, 201)

		posted_data = json.loads(response.get_data(as_text=True))
		
		response_edit_meal = self.client.put('/api/v1/meals/{}' . format(posted_data['meal']['meal_id']),
			data = update_meal,
			headers = self.headers
		)
		self.assertEqual(response_edit_meal.status_code, 400)
		self.assertIn('Can not update meal with empty meal options.', str(response_edit_meal.data))

	def test_adding_a_meal_with_empty_request_parameters(self):
		#Meal Addition with Empty Request parameters should not go ahead to execute
		app_meal = json.dumps({
			'mea': 'Fish with All foods',
			'pric': 25000
		})

		response = self.client.post('/api/v1/meals/', data = app_meal, headers = self.headers)
		result = json.loads(response.data.decode())
		self.assertEqual(response.status_code, 400)
		self.assertEqual(result['message'], 'Meal addition request expects a MEAL and its PRICE, either of them is not provided')
		
	def test_meal_update_with_empty_request_parameters(self):
		#Meal modification with Empty Request parameters should not go ahead to execute
		app_meal = json.dumps({
			'meal': 'Luwombo with Matooke',
			'price': 25000
		})
		update_meal = json.dumps({
			'meal_upd': 'Luwombo with All Local Foods',
			'price_up': 20000
		})
		response = self.client.post('/api/v1/meals/', data = app_meal, headers = self.headers)
		self.assertEqual(response.status_code, 201)

		posted_data = json.loads(response.get_data(as_text=True))
		
		response_edit_meal = self.client.put('/api/v1/meals/{}' . format(posted_data['meal']['meal_id']),
			data = update_meal,
			headers = self.headers
		)
		result = json.loads(response_edit_meal.data.decode())
		self.assertEqual(response_edit_meal.status_code, 400)
		self.assertEqual(result['message'], 'Meal Update expects MEAL_UPDATE and PRICE_UPDATE, either of them is not provided.')




	""" MENU OPERATION TESTS """
	def test_set_menu_of_the_day(self):
		#Testing setting the menu of the day with meals
		app_meal_one = json.dumps({
			'meal': 'Fish with All foods',
			'price': 25000
		})

		response_one = self.client.post('/api/v1/meals/', data = app_meal_one, headers = self.headers)
		self.assertEqual(response_one.status_code, 201)


		app_menu = json.dumps({
			'menu_name': 'Jojo Restaurant Special Friday',
			'date': 'Monday',
			'description': 'For our special friday, enjoy the menu with a free dessert',
			'meal_id': 1
		})

		response = self.client.post('/api/v1/menu/', data = app_menu, headers = self.headers)
		self.assertEqual(response.status_code, 201)
		self.assertIn("success", str(response.data))

	def test_get_menu_of_the_day(self):
		#Testing for retrieving the menu of the day
		app_menu = json.dumps({
			'menu_name': 'Jojo Restaurant Special Friday',
			'date': 'Monday',
			'description': 'For our special friday, enjoy the menu with a free dessert',
			'meal_id': 1
		})
		response_add = self.client.post('/api/v1/menu/', data = app_menu, headers = self.headers)
		self.assertEqual(response_add.status_code, 201)
		response_get = self.client.get('/api/v1/menu/', headers = self.headers)
		self.assertEqual(response_get.status_code, 200)
		self.assertIn('"Fish with All foods', str(response_get.data))

	def test_setting_empty_menu(self):
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





	""" ORDER OPERATION TESTS """
	def test_make_order(self):
		#Testing making an order from the menu
		app_order = json.dumps({
			'user': 'wasswadero@gmail',
			'meal': 'Fish with All foods',
			'price': 24000
		})

		response = self.client.post('/api/v1/orders/', data = app_order)
		self.assertEqual(response.status_code, 201)
		self.assertIn("Fish with All foods", str(response.data))

	def test_modifying_an_order(self):
		#Test that the API allows modification of an order
		app_order = json.dumps({
			'user': 'wasswadero@gmail',
			'meal': 'Luwombo with Matooke',
			'price': 25000
		})

		order_update = json.dumps({
			'order_to_update': 'Luwombo with All foods'
		})
		response = self.client.post('/api/v1/orders/', data = app_order)
		self.assertEqual(response.status_code, 201)

		posted_data = json.loads(response.get_data(as_text=True))

		response_edit_order = self.client.put(
			'/api/v1/orders/{}' . format(posted_data['order']['order_id']),
			data = order_update
		)
		self.assertEqual(response_edit_order.status_code, 200)

		results_get_order_by_id = self.client.get('/api/v1/orders/', headers = self.headers)
		self.assertIn(str(posted_data['order']['order_id']), str(results_get_order_by_id.data))

	def test_getting_all_orders(self):
		#Testing for retrieving all the ORDERS
		app_orders = json.dumps({
			'user': 'test@example.com',
			'meal': "Kalo",
			"price": 4500
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
			'price': '',
			'user': ''
		})

		response = self.client.post('/api/v1/orders/', data = app_menu)
		result = json.loads(response.data.decode())
		self.assertEqual(response.status_code, 400)
		self.assertEqual(result['message'], 'Can not order with empty content.')

	def test_modifying_order_with_empty_order_content(self):
		#Test modifying an order with empty order content
		app_order = json.dumps({
			'user': 'wasswadero@gmail',
			'meal': 'Luwombo with Matooke',
			'price': 25000
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
			"price": 5600
		})

		response = self.client.post('/api/v1/orders/', data = app_menu)
		result = json.loads(response.data.decode())
		self.assertEqual(response.status_code, 400)
		self.assertIn(result['message'], 'User Email not valid.')

	def test_making_orders_with_empty_request_parameters(self):
		#Making an order with Empty Request parameters should not go ahead to execute
		app_order = json.dumps({
			'us': 'wasswadero@gmail',
			'me': 'Fish with All foods',
			'pri': 24000
		})
		response = self.client.post('/api/v1/orders/', data = app_order)
		result = json.loads(response.data.decode())
		self.assertEqual(response.status_code, 400)
		self.assertEqual(result['message'], 'Making Order expects user email, meal id and either of them is not provided.')
		
	def test_order_modification_with_empty_request_parameters(self):
		#Order modification with Empty Request parameters should not go ahead to execute
		app_order = json.dumps({
			'user': 'wasswadero@gmail',
			'meal': 'Luwombo with Matooke',
			'price': 25000
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



if __name__ == '__main__':
	unittest.main()
		