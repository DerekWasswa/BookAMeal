import unittest
import json
from v1.api import create_app

class BaseCaseTest(unittest.TestCase):
    
	def setUp(self):
		#Set up the globally used variables for use
		app = create_app()
		self.client = app.test_client()

		self.headers = {
			'Content-Type': 'application/json',
			'Authorization': 'Basic auth',
			'app-access-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhZG1pbiI6dHJ1ZSwiZW1haWwiOiJhbm5hYmVsbGFAZ21haWwuY29tIn0.23Dp0dP3TSYMCZIEfSEmKyD4kxSZU867cRXYDjzZ0AI'
		}