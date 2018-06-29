import json
from v1.tests.base_case_test import BaseCaseTest


class MenuTests(BaseCaseTest):

    """ MENU OPERATION TESTS """

    def test_set_menu_of_the_day(self):
        self.mock_signup()
        login = self.mock_login()
        login_response = json.loads(login.get_data(as_text=True))

        # Testing setting the menu of the day with meals
        response_one = self.client.post(
            '/api/v1/meals/',
            data=self.all_food_meal,
            headers=self.headers_with_token(
                login_response['token']))

        response = self.client.post(
            '/api/v1/menu/',
            data=self.caterer_menu,
            headers=self.headers_with_token(
                login_response['token']))
        self.assertEqual(response.status_code, 201)
        self.assertIn("success", str(response.data))

    def test_setting_empty_menu(self):
        self.mock_signup()
        login = self.mock_login()
        login_response = json.loads(login.get_data(as_text=True))

        # Testing setting the menu of the day with meals
        response_one = self.client.post(
            '/api/v1/meals/',
            data=self.all_food_meal,
            headers=self.headers_with_token(
                login_response['token']))

        response = self.client.post(
            '/api/v1/menu/',
            data=self.empty_menu,
            headers=self.headers_with_token(
                login_response['token']))
        self.assertEqual(response.status_code, 400)
        self.assertIn("Empty Menu Details.", str(response.data))

    def test_setting_menu_of_the_day_with_empty_request_parameters(self):
        self.mock_signup()
        login = self.mock_login()
        login_response = json.loads(login.get_data(as_text=True))

        # Creating a menu with Empty Request parameters should not go ahead to
        # execute
        response_one = self.client.post(
            '/api/v1/meals/',
            data=self.all_food_meal,
            headers=self.headers_with_token(
                login_response['token']))

        response = self.client.post(
            '/api/v1/menu/',
            data=self.caterer_menu_wrong_request_params,
            headers=self.headers_with_token(
                login_response['token']))
        result = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            result['message'],
            'Setting a Menu expects Menu name, date, description, and meal Id keys.')

    def test_get_menu_of_the_day(self):
        self.mock_signup()
        login = self.mock_login()
        login_response = json.loads(login.get_data(as_text=True))
        self.add_mock_menu(self.headers_with_token(login_response['token']))

        # Testing for retrieving the menu of the day
        response_get = self.client.get('/api/v1/menu/', data=self.menu_date)
        self.assertEqual(response_get.status_code, 200)
        self.assertIn('1', str(response_get.data))

    def test_setting_menu_with_unauthorized_access(self):
        self.mock_signup()
        login = self.mock_login()
        unpriviledged = self.unpriviledged_mock_login()
        login_response = json.loads(login.get_data(as_text=True))
        unpriviledged_response = json.loads(
            unpriviledged.get_data(as_text=True))

        # Testing setting the menu of the day with meals should not allow
        # unauthorized access
        response_one = self.client.post(
            '/api/v1/meals/',
            data=self.all_food_meal,
            headers=self.headers_with_token(
                login_response['token']))

        response = self.client.post(
            '/api/v1/menu/',
            data=self.caterer_menu,
            headers=self.headers_with_token(
                unpriviledged_response['token']))
        self.assertEqual(response.status_code, 401)
        self.assertIn(
            "You need to login as Admin to perform this operation.", str(
                response.data))

    def test_get_menu_of_the_day_not_set(self):
        # Testing for retrieving the menu of the day which does not exist
        response_get = self.client.get('/api/v1/menu/', data=self.menu_date)
        self.assertEqual(200, response_get.status_code)
        self.assertIn('No menu set for the day.', str(response_get.data))

    def test_setting_menu_of_the_day_meal_option_does_not_exist(self):
        ''' verify that setting a menu with a meal not in meals should not complete '''
        self.mock_signup()
        login = self.mock_login()
        login_response = json.loads(login.get_data(as_text=True))

        response = self.client.post(
            '/api/v1/menu/',
            data=self.caterer_menu,
            headers=self.headers_with_token(
                login_response['token']))
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Meal with provided ID does not exist.", str(
                response.data))
