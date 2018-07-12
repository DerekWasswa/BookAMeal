import json
from v1.tests.base_case_test import BaseCaseTest


class Authentication(BaseCaseTest):

    """ USER REGISTRATION TESTS """

    def test_registration(self):
        # User registration should complete successfully
        response = self.client.post('/api/v1/auth/signup', data=self.user_data)
        result = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertIn(
            result['message'],
            'Successfully Registered. Please login')

    def test_registration_with_existing_user(self):
        # A user with the same email can not register more than once
        response_post = self.client.post('/api/v1/auth/signup', data=self.user_data)

        response_post_two = self.client.post(
            '/api/v1/auth/signup', data=self.user_data)
        self.assertEqual(response_post_two.status_code, 200)
        result = json.loads(response_post_two.data.decode())
        self.assertEqual(
            result['message'],
            "User already exists. Please login.")

    def test_user_registration_with_empty_credentials(self):
        # User should not register with missing credentials
        response = self.client.post('/api/v1/auth/signup', data=self.empty_user_data)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], "Missing Credentials")

    def test_registration_for_invalid_emails(self):
        # User registration with invalid emails should show invalid email
        response = self.client.post('/api/v1/auth/signup', data=self.invalid_email_user_data)
        result = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertIn(result['message'], 'Email is Invalid')

    def test_registration_with_empty_request_parameters(self):
        # User Registration with Empty Request parameters should not go ahead
        # to execute
        response = self.client.post('/api/v1/auth/signup', data=self.wrong_request_user_params)
        result = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            result['message'],
            'Signup expects username, email, password, admin values.')

    """ USER LOGIN TESTS """

    def test_user_login_with_empty_credentials(self):
        # User should not login with missing credentials
        response = self.client.post('/api/v1/auth/login', data=self.empty_user_data_login)
        self.assertEqual(response.status_code, 401)
        result = json.loads(response.data.decode())
        self.assertEqual(
            result['message'],
            "Could not verify. Login credentials required.")

    def test_user_login(self):
        # Test a registered user can be able to login
        response = self.client.post('/api/v1/auth/signup', data=self.user_data)

        user_login_response = self.client.post(
            '/api/v1/auth/login', data=self.user_data)
        result = json.loads(user_login_response.get_data(as_text=True))
        self.assertEqual(user_login_response.status_code, 200)
        self.assertEqual(result['message'], 'Logged in successfully')

    def test_user_login_with_user_who_does_not_exist(self):
        # Test a registered user can be able to login

        user_login_response = self.client.post(
            '/api/v1/auth/login', data=self.user_does_not_exists)
        result = json.loads(user_login_response.get_data(as_text=True))
        self.assertEqual(user_login_response.status_code, 401)
        self.assertEqual(result['message'], 'User email not found!!')

    def test_login_for_invalid_emails(self):
        # User login with invalid emails should show invalid email
        response = self.client.post('/api/v1/auth/login', data=self.invalid_email_user_data)
        result = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertIn(result['message'], 'Email is Invalid')

    def test_login_with_invalid_password(self):
        # User login with invalid password
        self.mock_signup()
        user_data = json.dumps({
            'email': 'derrekwasswa256@gmail.com',
            'password': '123456',
            'admin': True
        })
        response = self.client.post('/api/v1/auth/login', data=user_data)
        result = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertIn(result['message'], 'Invalid/Wrong Password')

    def test_login_with_empty_request_parameters(self):
        # User login with invalid emails should show invalid email
        response = self.client.post('/api/v1/auth/login', data=self.wrong_request_user_params)
        result = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            result['message'],
            'Logged requests expects email, password, and admin values.')

    def test_registration_username_should_not_exceed_chars_limit(self):
        response = self.client.post('/api/v1/auth/signup', data=self.username_too_long)
        result = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn(result['message'],
            'Username length should be less than 100 characters.')

    def test_registration_with_weak_password_should_fail(self):
        # User registration should not complete successfully if the password is weak
        response = self.client.post('/api/v1/auth/signup', data=self.weak_password)
        result = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertIn(
            result['message'],
            'Password is too weak.')
