import unittest
import json
from flask import session
from v1.api import create_app
from v1.api import db

class BaseCaseTest(unittest.TestCase):
    
	def setUp(self):
		#Set up the globally used variables for use
		app = create_app('testing')
		self.client = app.test_client()
		self.headers = {
			'Content-Type': 'application/json',
			'Authorization': 'Basic auth',
			'app-access-token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJhZG1pbiI6InRydWUifQ.W0EoWSsYbSlS8fSRWJsV77cBqbfNg8Iy2txp_9BdBzM'
		}

	def tearDown(self):
		db.session.remove()
		db.drop_all()