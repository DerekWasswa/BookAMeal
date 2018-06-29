# Book A Meal API
from flask import Flask, session, render_template, request, redirect, url_for, jsonify, make_response, current_app
from flask_api import FlaskAPI, status
import json
from werkzeug.security import generate_password_hash, check_password_hash
from v1.api.models import User, Meal, Menu, Order
from v1.api import models
from validate_email import validate_email
import jwt
from v1.api import auth_decorator
from flask.views import MethodView
from .import endpoints_blueprint
from v1.api import create_app


class SignUp(MethodView):

    def post(self):
        #Sign up a user either as a customer or vendor admin
        user_data = request.get_json(force=True)
        if not User.user_data_parameters_exist(user_data):
            return make_response(jsonify({'message': 'Signup expects username, email, password, admin values.'})), 400

        if User.user_data_is_empty(user_data):
            return make_response(jsonify({'message': 'Missing Credentials'})), 400

        user = User(user_data['username'], user_data['email'], generate_password_hash(str(user_data['password'])), user_data['admin'])

        #CHECK IF EMAIL IS VALID
        if not User.is_email_valid(user_data['email']):
            return make_response(jsonify({'message': 'Email is Invalid'})), 401

        if user.check_exists(user_data['email']):
            return make_response(jsonify({'message': 'User already exists. Please login.'})), 200
        else:
            user.save()
            return make_response(jsonify({
                'message': 'Successfully Registered. Please login',
                'status_code': 201,
                'data': user.get_user_object_as_dict()
                })), 201


class Login(MethodView):

    def post(self):
        #authenticate customers or admin
        user_data = request.get_json(force=True)
        if 'email' not in user_data or 'password' not in user_data or 'admin' not in user_data:
            return make_response(jsonify({'message': 'Logged requests expects email, password, and admin keys.'})), 400

        user_email = user_data['email']
        user_password = user_data['password']
        user_admin = user_data['admin']

        if len(str(user_email)) <= 0 or len(str(user_password)) <= 0 or len(str(user_admin)) <= 0:
            return make_response(jsonify({'message': 'Could not verify. Login credentials required.'})), 401

        #CHECK IF EMAIL IS VALID
        is_valid = validate_email(user_email)
        if not is_valid:
            return make_response(jsonify({'message': 'Email is Invalid'})), 401

        user = User('', user_email, user_password, user_admin)
        if not User.check_exists(user_email):
            return make_response(jsonify({'message': 'User email not found!!'})), 401

        app_user = user.get_user_by_email(user_email)
        if check_password_hash(app_user.password, user_password):
            #Create the app instance to use to generate the token
            app = create_app()
            # CREATE TOKEN: leverage isdangerous to create the token
            encoded_jwt_token = jwt.encode({
                'admin': user_admin,
                'email': user_email
                }, app.config['SECRET_KEY'], algorithm='HS256')
            return make_response(jsonify({
                'message': 'Logged in successfully',
                'status_code': 200,
                'token': encoded_jwt_token.decode('UTF-8')
                })), 200

        return make_response(jsonify({'message': 'Invalid Email or Password'})), 401






class MealsViews(MethodView):

    @auth_decorator.token_required_to_authenticate
    def get(current_user, self):
        #Verify If User is admin
        if not current_user:
            return jsonify({'message': 'You need to login as Admin to perform this operation.'})

        #Return all the available meals to the vendor admin
        return make_response(jsonify({
            'message': 'success',
            'status_code': 200,
            'data': models.app_meals
        })), 200

    @auth_decorator.token_required_to_authenticate
    def post(current_user, self):
        #Verify If User is admin
        if not current_user:
            return jsonify({'message': 'You need to login as Admin to perform this operation.'})

        #Allow the vendor admin to add another meal option
        meal_data = request.get_json(force=True)
        if 'meal' not in meal_data or 'price' not in meal_data:
            return make_response(jsonify({'message': 'Meal addition request expects a MEAL and its PRICE, either of them is not provided'})), 400

        meal = meal_data['meal']
        price = meal_data['price']

        if len(str(meal)) <= 0 or  len(str(price)) <= 0:
            return make_response(jsonify({'message': 'Meal Options Missing.'})), 400

        #Try parsing the Price, If doesnot pass the try then cast error
        if not isinstance(price, int):
            return make_response(jsonify({'message': 'Meal Price has to be an Integer.'})), 400


        meal_object = Meal(meal, price)
        meal_object.add_meal() #ADD MEAL HERE

        meal_as_dict = {}
        meal_as_dict['meal_id'] = meal_object.meal_id
        meal_as_dict['meal'] = meal_object.meal
        meal_as_dict['price'] = meal_object.price

        return make_response(jsonify({
            'message': 'Meal Added Successfully',
            'status_code': 201,
            'meal': meal_as_dict
        })), 201

    @auth_decorator.token_required_to_authenticate
    def put(current_user, self, mealId):
        #Verify If User is admin
        if not current_user:
            return jsonify({'message': 'You need to login as Admin to perform this operation.'})

        #Allow the ADMIN to edit a particular meal option
        meal_data = request.get_json(force=True)
        if 'meal_update' not in meal_data or 'price_update' not in meal_data:
            return make_response(jsonify({'message': 'Meal Update expects MEAL_UPDATE and PRICE_UPDATE, either of them is not provided.'})), 400

        meal_update = meal_data['meal_update']
        price_update = meal_data['price_update']

        if len(str(meal_update)) <= 0 or len(str(price_update)) <= 0:
            return make_response(jsonify({'message': 'Can not update meal with empty meal options'})), 400


        if not isinstance(price_update, int):
            return make_response(jsonify({'message': 'Can not update meal with non integer price'})), 400

        for i in range(len(models.app_meals)):
            if str(models.app_meals[i]['meal_id']) == str(mealId):
                models.app_meals[i]['meal'] = meal_update
                models.app_meals[i]['price'] = price_update
                break

        meal_as_dict = {}
        meal_as_dict['meal_id'] = mealId
        meal_as_dict['meal'] = meal_update

        return make_response(jsonify({
            'message': 'Meal Updated successfully',
            'status_code': 202,
            'data': meal_as_dict
        })), 202

    @auth_decorator.token_required_to_authenticate
    def delete(current_user, self, mealId):
        #Verify If User is admin
        if not current_user:
            return jsonify({'message': 'You need to login as Admin to perform this operation.'})

        #Allow the admin to delete a particular meal option
        if len(models.app_meals) > 0:
            delete_status = Meal.delete_meal_by_id(mealId)

            if delete_status:
                return make_response(jsonify({
                    'message': 'Meal Deleted successfully',
                    'status_code': 202
                })), 202
            else:
                return make_response(jsonify({
                    'message': 'Something went wrong!! Meal not deleted.',
                    'status_code': 404
                })), 404

        else:
            return make_response(jsonify({'message': 'Meals are Empty'})), 200

class GetMealById(MethodView):

    def get(self, mealId):
        # Return a meal for a particular ID
        if len(models.app_meals) > 0:

            for meal in models.app_meals:
                if mealId == meal['meal_id']:
                    return make_response(jsonify({ 'message': 'Meal Exists' })), 200

            return make_response(jsonify({ 'message': 'Meal not Found' })), 404

        else:
            return make_response(jsonify({'message': 'Meal are empty.'})), 404








class GetMenuOfTheDay(MethodView):

    def get(self):
        #Verify If User is admin

        appmenu = []
        for menus in models.app_menu:
            menu = {}
            menu['name'] = menus.name
            menu['date'] = menus.date
            menu['description'] = menus.description
            menu['meals'] = menus.meals
            appmenu.append(menu)

        #Allow the authenticated users to view menu of the day
        return make_response(jsonify({
            'message': 'success',
            'status_code': 200,
            'data': appmenu
        })), 200

class SetMenuOfTheDay(MethodView):

    @auth_decorator.token_required_to_authenticate
    def post(current_user, self):
        #Verify If User is admin
        if not current_user:
            return jsonify({'message': 'You need to login as Admin to perform this operation.'})

        #Allow the admin an operation to the set the menu of the day
        menu_data = request.get_json(force=True)
        if 'date' not in menu_data or 'description' not in menu_data or 'menu_name' not in menu_data or 'meal_id' not in menu_data:
            return make_response(jsonify({'message': 'Setting a Menu expects Menu name, date, description, and meal Id to add to the menu, either of them is not provided.'})), 400

        date = menu_data['date']
        description = menu_data['description']
        meal_id = menu_data['meal_id']
        menu_name = menu_data['menu_name']

        if len(str(menu_name)) <= 0 or len(str(description)) <= 0 or len(str(date)) <= 0 or len(str(meal_id)) <= 0:
            return make_response(jsonify({'message': 'Empty Menu Details.'})), 400


        meal = Meal.get_meal_by_id(meal_id)

        menu_exists = False
        for menu_object in models.app_menu:
            if date == menu_object.date:
                menu_object.meals.append(meal)
                menu_exists = True
            else:
                continue

        if not menu_exists:
            menu = Menu(menu_name, date, description)
            menu.meals.append(meal)
            menu.set_menu_of_the_day()

        return make_response(jsonify({'status_code': 201, 'data': 'success'})), 201







class MakeOrder(MethodView):

    def post(self):
        #Allow the authenticated users to make orders from the menu of the day
        order_data = request.get_json(force=True)
        if 'meal' not in order_data or 'user' not in order_data:
            return make_response(jsonify({'message': 'Making Order expects user email, meal id and either of them is not provided.'})), 400

        meal_id = order_data['meal']
        user_id = order_data['user']

        if len(str(meal_id)) <= 0 or len(str(user_id)) <= 0:
            return make_response(jsonify({'message': 'Can not order with empty content.'})), 400

        if not validate_email(user_id):
            return make_response(jsonify({'message': 'User Email not valid.'})), 400

        order = Order(user_id, meal_id)
        order.make_order()
        order_as_dict = {}
        order_as_dict['order_id'] = order.order_id
        order_as_dict['user_id'] = user_id
        order_as_dict['meal_id'] = meal_id

        order_id = order.order_id

        return make_response(jsonify({
            'message': 'Order Made successfully',
            'status_code': 201,
            'order': order_as_dict
            })), 201

class GetAllOrders(MethodView):

    @auth_decorator.token_required_to_authenticate
    def get(current_user, self):
        #Allow the Admin return all the Orders users have made
        orders_response = {
            'message': 'success',
            'status_code': 200,
            'orders': models.app_orders
        }
        return make_response(jsonify(orders_response)), 200

class ModifyOrder(MethodView):

    def put(self, orderId):
        #Allow the user to modify an order they've already made
        if len(models.app_orders) > 0:

            order_data = request.get_json(force=True)
            if 'order_to_update' not in order_data:
                return make_response(jsonify({'message': 'Modifying order expects the order id to edit with which is not provided.'})), 400

            order_update = order_data['order_to_update']

            if len(str(order_update)) <= 0:
                return make_response(jsonify({'message': 'Can not modify an order with empty content.'})), 400

            Order.update_order_by_id(orderId, order_update)
            return make_response(jsonify({'message': 'Order Updated successfully'})), 202
        else:
            return make_response(jsonify({'message': 'Orders are Empty', 'status_code': 200})), 200












#ADD THE VIEWS
signup = SignUp.as_view('signup_view')
login = Login.as_view('login_view')

meals_views = MealsViews.as_view('meals_views')
get_meal_by_id = GetMealById.as_view('get_meal_by_id')

get_menu_of_the_day = GetMenuOfTheDay.as_view('get_menu_of_the_day')
set_menu_the_day = SetMenuOfTheDay.as_view('set_menu_of_the_day')

make_order = MakeOrder.as_view('make_order')
get_all_orders = GetAllOrders.as_view('all_orders')
modify_order = ModifyOrder.as_view('modify_order')



endpoints_blueprint.add_url_rule('/auth/signup', view_func=signup, methods=['POST'])
endpoints_blueprint.add_url_rule('/auth/login', view_func=login, methods=['POST'])

endpoints_blueprint.add_url_rule('/meals/', view_func=meals_views, methods=['POST'])
endpoints_blueprint.add_url_rule('/meals/', view_func=meals_views, methods=['GET'])
endpoints_blueprint.add_url_rule('/meals/<mealId>', view_func=get_meal_by_id,methods=['GET'])
endpoints_blueprint.add_url_rule('/meals/<mealId>', view_func=meals_views,methods=['PUT', 'DELETE'])


endpoints_blueprint.add_url_rule('/menu/', view_func=get_menu_of_the_day, methods=['GET'])
endpoints_blueprint.add_url_rule('/menu/', view_func=set_menu_the_day, methods=['POST'])

endpoints_blueprint.add_url_rule('/orders/', view_func=make_order, methods=['POST'])
endpoints_blueprint.add_url_rule('/orders/', view_func=get_all_orders, methods=['GET'])
endpoints_blueprint.add_url_rule('/orders/<orderId>', view_func=modify_order,methods=['PUT'])
