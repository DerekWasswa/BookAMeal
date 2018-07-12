import json
from v1.tests.base_case_test import BaseCaseTest


class MealTests(BaseCaseTest):

    """ MEALS OPERATIONS TESTS """

    def test_adding_a_meal_option(self):
        self.mock_signup()
        login = self.mock_login()
        login_response = json.loads(login.get_data(as_text=True))

        # Testing addition of a meal option should add
        response = self.client.post(
            '/api/v1/meals/',
            data=self.all_food_meal,
            headers=self.headers_with_token(
                login_response['token']))

        self.assertEqual(response.status_code, 201)
        self.assertIn("Fish with All foods", str(response.data))
        self.assertIn('Meal Added Successfully', str(response.data))

    def test_adding_existing_meal_option(self):
        self.mock_signup()
        login = self.mock_login()
        login_response = json.loads(login.get_data(as_text=True))

        # Testing addition of a meal option should add
        response_first = self.client.post(
            '/api/v1/meals/',
            data=self.all_food_meal,
            headers=self.headers_with_token(
                login_response['token']))

        response_existing = self.client.post(
            '/api/v1/meals/',
            data=self.all_food_meal,
            headers=self.headers_with_token(
                login_response['token']))
        self.assertEqual(response_existing.status_code, 400)
        self.assertIn("Meal already exists.", str(response_existing.data))

    def test_modifying_a_meal_option(self):
        self.mock_signup()
        login = self.mock_login()
        login_response = json.loads(login.get_data(as_text=True))

        # Test that the API allows modification of a meal option by its ID
        # should modify the meal by both the meal name and price
        response = self.client.post(
            '/api/v1/meals/',
            data=self.matooke_meal,
            headers=self.headers_with_token(
                login_response['token']))
        posted_data = json.loads(response.get_data(as_text=True))

        response_edit_meal = self.client.put('/api/v1/meals/{}' . format(posted_data['meal']['meal_id']),
                                             data=self.update_meal,
                                             headers=self.headers_with_token(
                                                 login_response['token'])
                                             )
        self.assertEqual(response_edit_meal.status_code, 202)
        results_get_meals = self.client.get(
            '/api/v1/meals/',
            headers=self.headers_with_token(
                login_response['token']))
        self.assertIn('Luwombo with All', str(results_get_meals.data))

    def test_deleting_a_meal_option(self):
        self.mock_signup()
        login = self.mock_login()
        login_response = json.loads(login.get_data(as_text=True))
        self.add_mock_meal_options()

        # Test that the API allows for deletion of a meal option should delete
        # a meal by the ID
        response = self.client.post(
            '/api/v1/meals/',
            data=self.all_food_meal,
            headers=self.headers_with_token(
                login_response['token']))
        posted_data = json.loads(response.get_data(as_text=True))

        response_delete_meal = self.client.delete(
            '/api/v1/meals/{}' . format(
                posted_data['meal']['meal_id']), headers=self.headers_with_token(
                login_response['token']))

        # Now retrieve to see to it exists: Should Return Not Found - 404
        response_get = self.client.get(
            '/api/v1/meals/{}' . format(
                posted_data['meal']['meal_id']),
            headers=self.headers_with_token(
                login_response['token']))
        self.assertEqual(response_get.status_code, 404)

    def test_getting_all_meals(self):
        self.mock_signup()
        login = self.mock_login()
        login_response = json.loads(login.get_data(as_text=True))

        # Testing for retrieving all the available meals should return all
        # meals
        response_add = self.client.post(
            '/api/v1/meals/',
            data=self.all_food_meal,
            headers=self.headers_with_token(
                login_response['token']))

        response_get = self.client.get(
            '/api/v1/meals/',
            headers=self.headers_with_token(
                login_response['token']))
        self.assertEqual(response_get.status_code, 200)
        self.assertIn('Fish with All foods', str(response_get.data))

    def test_adding_empty_meal_options(self):
        self.mock_signup()
        login = self.mock_login()
        login_response = json.loads(login.get_data(as_text=True))

        # Testing addition of a meal option with missing content should not
        # pass
        response = self.client.post(
            '/api/v1/meals/',
            data=self.empty_meal,
            headers=self.headers_with_token(
                login_response['token']))
        result = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn(result['message'], 'Meal Options Missing.')

    def test_adding_meal_price_that_is_not_an_int(self):
        self.mock_signup()
        login = self.mock_login()
        login_response = json.loads(login.get_data(as_text=True))

        # Testing addition of a meal option with a price that is not empty
        # should not pass
        response = self.client.post(
            '/api/v1/meals/',
            data=self.stringed_meal_price,
            headers=self.headers_with_token(
                login_response['token']))
        result = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn(result['message'], 'Meal Price has to be an Integer.')

    def test_modifying_a_meal_with_empty_meal_options(self):
        self.mock_signup()
        login = self.mock_login()
        login_response = json.loads(login.get_data(as_text=True))

        # MODIFYING A MEAL OPTIONS WITH EMPTY DATA SHOULD NOT ACCEPT
        response = self.client.post(
            '/api/v1/meals/',
            data=self.matooke_meal,
            headers=self.headers_with_token(
                login_response['token']))
        posted_data = json.loads(response.get_data(as_text=True))

        response_edit_meal = self.client.put('/api/v1/meals/{}' . format(posted_data['meal']['meal_id']),
                                             data=self.empty_meal_options,
                                             headers=self.headers_with_token(
                                                 login_response['token'])
                                             )
        self.assertEqual(response_edit_meal.status_code, 400)
        self.assertIn(
            'Can not update meal with empty meal options', str(
                response_edit_meal.data))

    def test_adding_a_meal_with_empty_request_parameters(self):
        self.mock_signup()
        login = self.mock_login()
        login_response = json.loads(login.get_data(as_text=True))

        # Meal Addition with Empty Request parameters should not go ahead to
        # execute

        response = self.client.post(
            '/api/v1/meals/',
            data=self.meal_with_wrong_request,
            headers=self.headers_with_token(
                login_response['token']))
        result = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            result['message'],
            'Meal addition request expects a MEAL and its PRICE keys.')

    def test_meal_update_with_empty_request_parameters(self):
        self.mock_signup()
        login = self.mock_login()
        login_response = json.loads(login.get_data(as_text=True))

        # Meal modification with Empty Request parameters should not go ahead
        # to execute
        response = self.client.post(
            '/api/v1/meals/',
            data=self.matooke_meal,
            headers=self.headers_with_token(
                login_response['token']))
        posted_data = json.loads(response.get_data(as_text=True))

        response_edit_meal = self.client.put('/api/v1/meals/{}' . format(posted_data['meal']['meal_id']),
                                             data=self.wrong_update_meal_request_params,
                                             headers=self.headers_with_token(
                                                 login_response['token'])
                                             )
        result = json.loads(response_edit_meal.data.decode())
        self.assertEqual(response_edit_meal.status_code, 400)
        self.assertEqual(
            result['message'],
            'Meal Update expects MEAL_UPDATE and PRICE_UPDATE keys.')

    def test_meal_update_with_non_integer_price(self):
        self.mock_signup()
        login = self.mock_login()
        login_response = json.loads(login.get_data(as_text=True))

        # Test that the API allows modification of a meal option by its ID
        # should modify the meal by both the meal name and price
        response = self.client.post(
            '/api/v1/meals/',
            data=self.matooke_meal,
            headers=self.headers_with_token(
                login_response['token']))
        posted_data = json.loads(response.get_data(as_text=True))

        response_edit_meal = self.client.put('/api/v1/meals/{}' . format(posted_data['meal']['meal_id']),
                                             data=self.stringed_meal_price_update,
                                             headers=self.headers_with_token(
                                                 login_response['token'])
                                             )
        self.assertEqual(response_edit_meal.status_code, 400)
        result = json.loads(response_edit_meal.get_data(as_text=True))
        self.assertEqual(
            result['message'],
            'Can not update meal with non integer price')

    def test_meal_update_not_found(self):
        # verify that updating does not happen if the meal does not exist
        self.mock_signup()
        login = self.mock_login()
        login_response = json.loads(login.get_data(as_text=True))

        update_meal = json.dumps({
            'meal_update': 'Luwombo with All Local Foods',
            'price_update': 20000
        })

        response_edit_meal = self.client.put('/api/v1/meals/{}' . format(20),
                                             data=update_meal,
                                             headers=self.headers_with_token(
                                                 login_response['token'])
                                             )
        self.assertEqual(response_edit_meal.status_code, 404)
        self.assertIn(
            'Update Incomplete! Meal does not exist.', str(
                response_edit_meal.data))

    def test_add_meal_with_unauthorized_access(self):
        # Testing addition of a meal option should add if user is unauthorized
        self.mock_signup()
        unpriviledged = self.unpriviledged_mock_login()
        unpriviledged_response = json.loads(
            unpriviledged.get_data(as_text=True))

        response = self.client.post(
            '/api/v1/meals/',
            data=self.all_food_meal,
            headers=self.headers_with_token(
                unpriviledged_response['token']))
        self.assertEqual(response.status_code, 401)
        self.assertIn(
            "You need to login as Admin to perform this operation.", str(
                response.data))

    def test_edit_meal_with_unauthorized_access(self):
        self.mock_signup()
        login = self.mock_login()
        unpriviledged = self.unpriviledged_mock_login()
        login_response = json.loads(login.get_data(as_text=True))
        unpriviledged_response = json.loads(
            unpriviledged.get_data(as_text=True))

        # Test that the API does not allows modification of a meal option with
        # unauthorized access
        response = self.client.post(
            '/api/v1/meals/',
            data=self.matooke_meal,
            headers=self.headers_with_token(
                login_response['token']))
        posted_data = json.loads(response.get_data(as_text=True))

        response_edit_meal = self.client.put('/api/v1/meals/{}' . format(posted_data['meal']['meal_id']),
                                             data=self.update_meal,
                                             headers=self.headers_with_token(
                                                 unpriviledged_response['token'])
                                             )
        self.assertEqual(response_edit_meal.status_code, 401)
        self.assertIn(
            "You need to login as Admin to perform this operation.", str(
                response_edit_meal.data))

    def test_retrieving_meals_with_unauthorized_access(self):
        self.mock_signup()
        login = self.mock_login()
        unpriviledged = self.unpriviledged_mock_login()
        login_response = json.loads(login.get_data(as_text=True))
        unpriviledged_response = json.loads(
            unpriviledged.get_data(as_text=True))

        # Testing for retrieving all the available meals should not return
        # meals for unauthorized access

        response_get = self.client.get(
            '/api/v1/meals/',
            headers=self.headers_with_token(
                unpriviledged_response['token']))
        self.assertEqual(response_get.status_code, 401)
        self.assertIn(
            "You need to login as Admin to perform this operation.", str(
                response_get.data))

    def test_deleting_meals_with_unauthorized_access(self):
        self.mock_signup()
        login = self.mock_login()
        unpriviledged = self.unpriviledged_mock_login()
        login_response = json.loads(login.get_data(as_text=True))
        unpriviledged_response = json.loads(
            unpriviledged.get_data(as_text=True))

        # Test that the API allows for deletion of a meal option should delete
        # a meal by the ID
        response = self.client.post(
            '/api/v1/meals/',
            data=self.matooke_meal,
            headers=self.headers_with_token(
                login_response['token']))
        posted_data = json.loads(response.get_data(as_text=True))

        response_delete_meal = self.client.delete(
            '/api/v1/meals/{}' . format(posted_data['meal']['meal_id']),
            headers=self.headers_with_token(unpriviledged_response['token'])
        )
        self.assertEqual(response_delete_meal.status_code, 401)
        self.assertIn(
            "You need to login as Admin to perform this operation.", str(
                response_delete_meal.data))

    def test_deleting_a_meal_with_empty_meals(self):
        self.mock_signup()
        login = self.mock_login()
        login_response = json.loads(login.get_data(as_text=True))

        # Test that the API does not allow for deletion with empty meals
        response_delete_meal = self.client.delete(
            '/api/v1/meals/{}' . format(15),
            headers=self.headers_with_token(
                login_response['token']))

        self.assertEqual(200, response_delete_meal.status_code)
        self.assertIn("Meals are Empty", str(response_delete_meal.data))

    def test_deleting_meal_not_found(self):
        self.mock_signup()
        login = self.mock_login()
        login_response = json.loads(login.get_data(as_text=True))

        response = self.client.post(
            '/api/v1/meals/',
            data=self.all_food_meal,
            headers=self.headers_with_token(
                login_response['token']))

        # Test that the API does not allow for deletion of a meal option which
        # does not exist
        response_delete_meal = self.client.delete(
            '/api/v1/meals/{}' . format(20),
            headers=self.headers_with_token(
                login_response['token']))
        self.assertEqual(response_delete_meal.status_code, 404)
        self.assertIn(
            "Deletion Incomplete! Meal Not Found.", str(
                response_delete_meal.data))

    """ TOKEN TESTS """

    def test_add_meal_with_no_auth_token(self):
        # Test that without a token, one cannot add a meal

        response = self.client.post(
            '/api/v1/meals/',
            data=self.all_food_meal,
            headers=self.no_token_headers)
        self.assertEqual(response.status_code, 401)
        self.assertIn("No token in the headers", str(response.data))

    def test_add_meal_with_invalid_token(self):
        # Test that an invalid token, one cannot add a meal

        response = self.client.post(
            '/api/v1/meals/',
            data=self.all_food_meal,
            headers=self.invalid_token_headers)
        self.assertEqual(response.status_code, 401)
        self.assertIn("Token is Invalid.", str(response.data))
