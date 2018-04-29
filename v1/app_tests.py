import unittest
from app import app
import json

class AppTest(unittest.TestCase):
    
	def setUp(self):
		#Set up the globally used variables for use
		self.client = app.test_client()

	""" USER REGISTRATION TESTS """
	def test_registration(self):
		#User registration should complete successfully
		user_data = json.dumps({
			'email': 'test@example.com',
			'password': '12345'
		})
		response = self.client.post('/auth/signup', data = user_data)
		result = json.loads(response.data.decode())
		self.assertEqual(response.status_code, 201)
		self.assertEqual(result['message'], 'Successfully Registered. Please login')

	def test_existing_user(self):
		#A user with the same email can not register more than once
		user_data = json.dumps({
			'email': 'test@example.com',
			'password': '12345'
		})
		response1 = self.client.post('/auth/register', data = user_data)
		self.assertEqual(response1.status_code, 201)
		response2 = self.client.post('/auth/register', data = user_data)
		self.assertEqual(response2.status_code, 202)
		result = json.loads(response2.data.decode())
		self.assertEqual(result['message'], "User already exists. Please login.")

	def test_user_registration_with_invalid_email(self):
		#User should register with the correct format of an email
		user_data = json.dumps({
			'email': 'test',
			'password': '12345'
		})
		response = self.client.post('/auth/register', data = user_data)
		self.assertEqual(response.status_code, 200)
		result = json.loads(response.data.decode())
		self.assertEqual(result['message'], "Invalid Email")

	def test_user_with_empty_credentials(self):
		#User should not register with missing credentials
		user_data = json.dumps({
			'email': '',
			'password': ''
		})
		response = self.client.post('/auth/register', data = user_data)
		self.assertEqual(response.status_code, 200)
		result = json.loads(response.data.decode())
		self.assertEqual(result['message'], "Missing Credentials")		



	""" USER LOGIN TESTS """
	def test_user_login_with_invalid_email(self):
		#User should login with the correct format of an email
		user_data = json.dumps({
			'email': 'test',
			'password': '12345'
		})
		response = self.client.post('/auth/login', data = user_data)
		self.assertEqual(response.status_code, 200)
		result = json.loads(response.data.decode())
		self.assertEqual(result['message'], "Invalid Email")

	def test_user_login_with_empty_credentials(self):
		#User should not login with missing credentials
		user_data = json.dumps({
			'email': '',
			'password': ''
		})
		response = self.client.post('/auth/login', data = user_data)
		self.assertEqual(response.status_code, 200)
		result = json.loads(response.data.decode())
		self.assertEqual(result['message'], "Missing Credentials")		

	def test_user_login(self):
		#Test a registered user can be able to login
		user_data = json.dumps({
			'email': 'test@example.com',
			'password': '12345'
		})
		response = self.client.post('/auth/signup', data = user_data)
		self.assertEqual(response.status_code, 201)

		user_login_response = self.client.post('/auth/login', data = user_data)
		result = json.loads(user_login_response.data.decode())
		self.assertEqual(result['message'], 'Logged in succcessfully')
		self.assertEqual(user_login_response.status_code, 200)


	""" MEALS OPERATIONS TESTS """
	def test_getting_all_meals(self):
		#Testing for retrieving all the available meals
		appMeals = json.dumps({
			'mealName': 'Beek with Chicken',
			'price': '20000'
		})
		responseAdd = self.client.post('/meals/', data = appMeals)
		self.assertEqual(responseAdd.status_code, 201)
		responseGet = self.client.get('/meals/')
		self.assertEqual(responseGet.status_code, 200)
		self.assertIn('Beek with Chicken', str(responseGet.data))

	def test_adding_a_meal_option(self):
		#Testing addition of a meal option
		appMeal = json.dumps({
			'mealName': 'Fish with All foods',
			'price': '25000'
		})

		response = self.client.post('/meals/', data = appMeal)
		self.assertEqual(response.status_code, 201)
		self.assertIn("Fish with All foods", str(response.data))

	def test_adding_a_meal_option_with_empty_meal_option(self):
		#Test admin can not add an empty meal option
		appMeal = json.dumps({
			'mealName': '',
			'price': ''
		})

		response = self.client.post('/meals/', data = appMeal)
		self.assertEqual(response.status_code, 200)
		result = json.loads(response.data.decode())
		self.assertEqual(result['message'], "Empty Meal Option")

	def test_modifying_a_meal_option(self):
		#Test that the API allows modification of a meal option by its ID
		appMeal = json.dumps({
			'mealName': 'Luwombo with Matooke',
			'price': '25000'
		})

		response = self.client.post('/meals/', data = appMeal)
		self.assertEqual(response.status_code, 201)

		postedData = json.loads(response.data.decode())

		responseEditMeal = self.client.put(
			'/meals/{}' . format(postedData['mealID']),
			data = {'name': 'Luwombo with All Local Foods'}
			)
		self.assertEqual(responseEditMeal.status_code, 200)

		resultsGetMeals = self.client.get('/meals/{}' . format(postedData['mealID']))
		self.assertIn("Luwombo with All", str(resultsGetMeals.data))
		pass 		

	def test_deleting_a_meal_option(self):
		#Test that the API allows for deletion of a meal option
		appMeal = json.dumps({
			'mealName': 'Luwombo with Irish',
			'price': '25000'
		})

		response = self.client.post('/meals/', data = appMeal)
		self.assertEqual(response.status_code, 201)

		postedData = json.loads(response.data.decode())	

		responseDeleteMeal = self.client.delete('/meals/{}' . format(postedData['mealID']))
		self.assertEqual(responseDeleteMeal.status_code, 200)

		#Now retrieve to see to it exists: Should Return Not Found - 404

		responseGet = self.client.get('/meals/{}' . format(postedData['mealID']))
		self.assertEqual(responseGet.status_code, 404)


	""" MENU OPERATION TESTS """

	""" ORDER OPERATION TESTS """

if __name__ == '__main__':
	unittest.main()
		