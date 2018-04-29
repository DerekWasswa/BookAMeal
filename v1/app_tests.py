import unittest
from app import app
import json

class AppTest(unittest.TestCase):
    
	def setUp(self):
		#Set up the globally used variables for use
		self.client = app.test_client()

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


if __name__ == '__main__':
	unittest.main()
		