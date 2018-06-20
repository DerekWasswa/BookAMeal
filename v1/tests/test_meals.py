import json
from v1.tests.base_case_test import BaseCaseTest

class MealTests(BaseCaseTest):

	""" MEALS OPERATIONS TESTS """
	def test_adding_a_meal_option(self):
		self.mock_signup()
		self.mock_login()
		
		#Testing addition of a meal option should add
		app_meal = json.dumps({
			'meal': 'Fish with All foods',
			'price': 25000
		})
		response = self.client.post('/api/v1/meals/', data = app_meal, headers = self.headers)
		self.assertEqual(response.status_code, 201)
		self.assertIn("Fish with All foods", str(response.data))
		self.assertIn('Meal Added Successfully', str(response.data))

	def test_modifying_a_meal_option(self):
		self.mock_signup()
		self.mock_login()
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
		self.assertEqual(response_edit_meal.status_code, 202)

		results_get_meals = self.client.get('/api/v1/meals/', headers = self.headers)
		self.assertIn('Luwombo with All', str(results_get_meals.data))		

	def test_deleting_a_meal_option(self):
		self.mock_signup()
		self.mock_login()

		#Test that the API allows for deletion of a meal option should delete a meal by the ID
		app_meal = json.dumps({
			'meal': 'Luwombo with Irish',
			'price': 25000
		})

		response = self.client.post('/api/v1/meals/', data = app_meal, headers = self.headers)
		self.assertEqual(response.status_code, 201)

		posted_data = json.loads(response.get_data(as_text=True))	

		response_delete_meal = self.client.delete('/api/v1/meals/{}' . format(posted_data['meal']['meal_id']), headers = self.headers)
		self.assertEqual(response_delete_meal.status_code, 202)

		#Now retrieve to see to it exists: Should Return Not Found - 404
		response_get = self.client.get('/api/v1/meals/{}' . format(posted_data['meal']['meal_id']), headers = self.headers)
		self.assertEqual(response_get.status_code, 404)

	def test_getting_all_meals(self):
		self.mock_signup()
		self.mock_login()

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

	def test_adding_empty_meal_options(self):
		self.mock_signup()
		self.mock_login()

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
		self.mock_signup()
		self.mock_login()

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
		self.mock_signup()
		self.mock_login()

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
		self.assertIn('Can not update meal with empty meal options', str(response_edit_meal.data))

	def test_adding_a_meal_with_empty_request_parameters(self):
		self.mock_signup()
		self.mock_login()

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
		self.mock_signup()
		self.mock_login()

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

	def test_meal_update_with_non_integer_price(self):
		self.mock_signup()
		self.mock_login()

		#Test that the API allows modification of a meal option by its ID should modify the meal by both the meal name and price
		app_meal = json.dumps({
			'meal': 'Luwombo with Matooke',
			'price': 25000
		})
		update_meal = json.dumps({
			'meal_update': 'Luwombo with Chips',
			'price_update': '20000'
		})
		response = self.client.post('/api/v1/meals/', data = app_meal, headers = self.headers)
		self.assertEqual(response.status_code, 201)

		posted_data = json.loads(response.get_data(as_text=True))
		
		response_edit_meal = self.client.put('/api/v1/meals/{}' . format(posted_data['meal']['meal_id']),
			data = update_meal,
			headers = self.headers
		)
		self.assertEqual(response_edit_meal.status_code, 400)
		result = json.loads(response_edit_meal.get_data(as_text=True))
		self.assertEqual(result['message'], 'Can not update meal with non integer price')

	def test_add_meal_with_unauthorized_access(self):
		#Testing addition of a meal option should add if user is unauthorized
		app_meal = json.dumps({
			'meal': 'Fish with All foods',
			'price': 25000
		})
		response = self.client.post('/api/v1/meals/', data = app_meal, headers = self.unauthorized_user_token_headers)
		self.assertEqual(response.status_code, 401)
		self.assertIn("You need to login as Admin to perform this operation.", str(response.data))

	def test_edit_meal_with_unauthorized_access(self):
		self.mock_signup()
		self.mock_login()
		#Test that the API does not allows modification of a meal option with unauthorized access
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
			headers = self.unauthorized_user_token_headers
		)
		self.assertEqual(response_edit_meal.status_code, 401)
		self.assertIn("You need to login as Admin to perform this operation.", str(response_edit_meal.data))

	def test_retrieving_meals_with_unauthorized_access(self):
		self.mock_signup()
		self.mock_login()

		#Testing for retrieving all the available meals should not return meals for unauthorized access
		app_meals = json.dumps({
			'meal': 'Beef with Chicken',
			'price': 20000
		})

		response_add = self.client.post('/api/v1/meals/', data = app_meals, headers = self.headers)
		self.assertEqual(response_add.status_code, 201)
		response_get = self.client.get('/api/v1/meals/', headers = self.unauthorized_user_token_headers)
		self.assertEqual(response_get.status_code, 401)
		self.assertIn("You need to login as Admin to perform this operation.", str(response_get.data))

	def test_deleting_meals_with_unauthorized_access(self):
		self.mock_signup()
		self.mock_login()

		#Test that the API allows for deletion of a meal option should delete a meal by the ID
		app_meal = json.dumps({
			'meal': 'Luwombo with Irish',
			'price': 25000
		})

		response = self.client.post('/api/v1/meals/', data = app_meal, headers = self.headers)
		self.assertEqual(response.status_code, 201)

		posted_data = json.loads(response.get_data(as_text=True))	

		response_delete_meal = self.client.delete(
			'/api/v1/meals/{}' . format(posted_data['meal']['meal_id']), 
			headers = self.unauthorized_user_token_headers
		)
		self.assertEqual(response_delete_meal.status_code, 401)
		self.assertIn("You need to login as Admin to perform this operation.", str(response_delete_meal.data))



	""" TOKEN TESTS """
	def test_add_meal_with_no_auth_token(self):
		''' Test that without a token, one cannot add a meal '''
		
		app_meal = json.dumps({
			'meal': 'Fish with All foods',
			'price': 25000
		})
		response = self.client.post('/api/v1/meals/', data = app_meal, headers = self.no_token_headers)
		self.assertEqual(response.status_code, 401)
		self.assertIn("No token in the headers", str(response.data))


	def test_add_meal_with_invalid_token(self):
		''' Test that an invalid token, one cannot add a meal '''
		
		app_meal = json.dumps({
			'meal': 'Fish with All foods',
			'price': 25000
		})
		response = self.client.post('/api/v1/meals/', data = app_meal, headers = self.invalid_token_headers)
		self.assertEqual(response.status_code, 401)
		self.assertIn("Token is Invalid.", str(response.data))