# Book A Meal API
from flask import Flask, g, session, render_template, request, redirect, url_for, jsonify, make_response, current_app
from flask_api import FlaskAPI, status
import json
from werkzeug.security import generate_password_hash, check_password_hash
from v1.api.models.meals import Meal
from v1.api.models.users import User
from v1.api.models.menu import Menu
from v1.api.models.orders import Order
from v1.api.utils import UtilHelper
from v1.api import models
from validate_email import validate_email
import jwt
from v1.api import auth_decorator
from flask.views import MethodView
from .import endpoints_blueprint
from v1.api import create_app
from v1.api import db
from v1.api.utils import UtilHelper
import datetime


class SignUp(MethodView):

    def post(self):
        # Sign up a user either as a customer or vendor admin
        user_data = request.get_json(force=True)

        if not UtilHelper.check_for_request_params(user_data, 'email', 'password', 'admin', 'username'):
            return make_response(jsonify(
                {'message': 'Signup expects username, email, password, admin values.'})), 400

        response = User.validate_user_registration_data(user_data)
        if response:
            return response

        user = User.instantiate_user(user_data)

        # ADD THE USER TO THE DB SESSION
        user.save()
        return make_response(jsonify({
            'message': 'Successfully Registered. Please login', 'status_code': 201,
            'data': user.get_user_object_as_dict()})), 201


class Login(MethodView):

    def post(self):
        # authenticate customers or admin
        user_data = request.get_json(force=True)

        if not UtilHelper.check_for_request_params(user_data, 'email', 'password', 'admin'):
            return make_response(jsonify(
                {'message': 'Logged requests expects email, password, and admin values.'})), 400

        user = User('n/a', user_data['email'], user_data['password'], user_data['admin'])

        response = User.validate_user_login_data(user_data, user)
        if response:
            return response

        # Create the app instance to use to generate the token
        # CREATE TOKEN: leverage isdangerous to create the token
        encoded_jwt_token = jwt.encode({'admin': user_data['admin'], 'user_id': user.get_user_id(),
                                        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=35)},
                                       'boOk-a-MeAL', algorithm='HS256')

        return make_response(jsonify({
            'message': 'Logged in successfully',
            'status_code': 200,
            'token': encoded_jwt_token.decode('UTF-8')
        })), 200


class MealsViews(MethodView):

    @auth_decorator.token_required_to_authenticate
    def get(current_user, self):
        # Verify If User is admin
        if not current_user:
            return make_response(jsonify(
                {'message': 'You need to login as Admin to perform this operation.', 'status_code': 401})), 401

        return make_response(jsonify({
            'message': 'success',
            'status_code': 200,
            'data': Meal.retrieve_all_meals(g.user_id)
        })), 200

    @auth_decorator.token_required_to_authenticate
    def post(current_user, self):
        # Verify If User is admin
        if not current_user:
            return make_response(jsonify(
                {'message': 'You need to login as Admin to perform this operation.', 'status_code': 401})), 401

        # Allow the vendor admin to add another meal option
        meal_data = request.get_json(force=True)
        if not UtilHelper.check_for_request_params(meal_data, 'meal', 'price'):
            return make_response(jsonify(
                {'message': 'Meal addition request expects a MEAL and its PRICE keys.',
                'status_code': 400})), 400

        vendor_id = g.user_id

        meal_object = Meal(meal_data['meal'], meal_data['price'], vendor_id)

        response = Meal.validate_meal_data(meal_data, meal_object)
        if response:
            return response

        # ADD THE USER TO THE DB SESSION
        meal_object.save()

        return make_response(jsonify({
            'message': 'Meal Added Successfully',
            'status_code': 201,
            'meal': meal_object.get_meal_as_dict()
        })), 201

    @auth_decorator.token_required_to_authenticate
    def put(current_user, self, mealId):
        # Verify If User is admin
        if not current_user:
            return make_response(jsonify(
                {'message': 'You need to login as Admin to perform this operation.', 'status_code': 401})), 401

        # Allow the ADMIN to edit a particular meal option
        meal_data = request.get_json(force=True)
        if not UtilHelper.check_for_request_params(meal_data, 'meal_update', 'price_update'):
            return make_response(jsonify(
                {'message': 'Meal Update expects MEAL_UPDATE and PRICE_UPDATE keys.',
                'status_code': 400})), 400

        response = Meal.validate_meal_update_data(meal_data['meal_update'], meal_data['price_update'], mealId)
        if response:
            return response

        vendor_id = g.user_id
        update_status = Meal.query.filter_by(meal_id=mealId, vendor_id=vendor_id).update(
            dict(meal=meal_data['meal_update'], price=meal_data['price_update']))
        Meal.commit_meal_changes()

        message, status = '', 0
        if update_status == 1:
            message, status = 'Meal Updated successfully', 202
        else:
            message, status = 'Update Failed! Meal not in my meals.', 404
        return make_response((jsonify({"message": message, 'status_code': status})), status)


    @auth_decorator.token_required_to_authenticate
    def delete(current_user, self, mealId):
        # Verify If User is admin
        if not current_user:
            return make_response(jsonify(
                {'message': 'You need to login as Admin to perform this operation.', 'status_code': 401})), 401

        # Allow the admin to delete a particular meal option if it exists
        if UtilHelper.check_empty_database_table(Meal):
            return make_response(
                jsonify({'message': 'Meals are Empty', 'status_Code': 200})), 200

        if not UtilHelper.check_row_id_exists_in_table(Meal, 'meal_id', mealId):
            return make_response(jsonify(
                {'message': 'Deletion Incomplete! Meal Not Found.', 'status_code': 404})), 404

        vendor_id = g.user_id
        deletion_status = Meal.query.filter_by(meal_id=mealId, vendor_id=vendor_id).delete()
        Meal.commit_meal_changes()

        message, status = '', 0
        if deletion_status == 1:
            message, status = 'Meal Deleted successfully', 202
        else:
            message, status = 'Meal Deletion failed! Not found in my meals.', 404
        return make_response((jsonify({"message": message, 'status_code': status})), status)


class GetMealById(MethodView):

    def get(self, mealId):
        # Return a meal for a particular ID
        response = Meal.get_meal_by_id_validation(mealId)
        if not response['validation_pass']:
            return make_response(jsonify({'message': response['message'], 'status_code': response['status_code']
            })), response['status_code']

        return make_response(
            jsonify({'message': 'Meal not Found', 'status_code': 404})), 404


class MenusView(MethodView):
    """ Have customers retrieve the menu of the day """

    def get(self):

        # Allow the authenticated users to view menu of the day
        day_date = datetime.datetime.today().strftime('%Y-%m-%d')
        if not Menu.check_menu_of_the_day_exists(day_date):
            return make_response(
                jsonify({'message': 'No menu set for the day.', 'status_code': 200})), 200

        menu_list = Menu.get_menu_of_the_day(day_date)

        return make_response(
            jsonify({'message': 'success', 'status_code': 200, 'data': menu_list})), 200

    @auth_decorator.token_required_to_authenticate
    def post(current_user, self):
        # Verify If User is admin
        if not current_user:
            return make_response(jsonify(
                {'message': 'You need to login as Admin to perform this operation.', 'status_code': 401})), 401

        # Allow the admin an operation to the set the menu of the day
        menu_data = request.get_json(force=True)

        if not UtilHelper.check_for_request_params(menu_data, 'date', 'description', 'menu_name', 'meal_id'):
            return make_response(jsonify(
                {'message': 'Setting a Menu expects Menu name, date, description, and meal Id keys.'})), 400

        response = Menu.validate_menu_data(menu_data)
        if response:
            return response

        # CHECK IF THE MENU OF THE DAY ALREADY EXISTS
        vendor_id = g.user_id
        if Menu.check_caterer_menu_exists(vendor_id, menu_data['date']):
            mealdb = Meal.query.filter_by(meal_id=menu_data['meal_id']).first()
            menudb = Menu.query.filter_by(vendor_id=vendor_id, date=menu_data['date']).first()
            menudb.meals.append(mealdb)
            Menu.add_meals_to_menu()
        else:
            create_new_menu = Menu(menu_data['menu_name'], menu_data['date'], menu_data['description'], g.user_id)
            mealdb = Meal.query.filter_by(meal_id=menu_data['meal_id']).first()
            create_new_menu.meals.append(mealdb)
            create_new_menu.create_menu()


        return make_response(
            jsonify({'status_code': 201, 'message': 'success'})), 201


class OrdersView(MethodView):

    def post(self):
        # Allow the authenticated users to make orders from the menu of the day

        order_data = request.get_json(force=True)
        if not UtilHelper.check_for_request_params(order_data, 'meal_id', 'user', 'date', 'menu_id'):
            return make_response(jsonify(
                {'message': 'Making Order expects; user email, meal id, menu_id, and date keys.', 'status_code': 400})), 400

        response = Order.validate_order_data(order_data)
        if response:
            return response

        # MEAL EXISTS IN THE MENU -> Make the Order to the db
        order = Order(order_data['user'], order_data['meal_id'], order_data['menu_id'], order_data['date'])
        order.save_order()
        order_as_dict = Order.order_as_dict(order)

        return make_response(jsonify(
            {'message': 'Order Made successfully', 'status_code': 201, 'order': order_as_dict})), 201

    @auth_decorator.token_required_to_authenticate
    def get(current_user, self):
        # Allow the Authorized Admin return all the Orders users have made
        if not current_user:
            return make_response(jsonify(
                {'message': 'You need to login as Admin to perform this operation.', 'status_code': 401})), 401

        orderdb = Order.query.all()
        orders = Order.get_all_orders(orderdb)
        return make_response(jsonify({'message': 'success', 'status_code': 200, 'orders': orders })), 200

    def put(self, orderId):
        # Allow the user to modify an order they've already made
        if UtilHelper.check_empty_database_table(Order):
            return make_response(
                jsonify({'message': 'Orders are Empty', 'status_code': 200})), 200

        order_data = request.get_json(force=True)
        if not UtilHelper.check_for_request_params(order_data, 'meal_id', 'user', 'order_to_update', 'menu_id'):
            return make_response(jsonify(
                {'message': 'Modifying order expects the order id, user, menu id, meal id keys.'})), 400

        response = Order.validate_order_update_data(order_data)
        if response:
            return response

        Order.query.filter_by(order_id=orderId, menu_id=order_data['menu_id']).update(
            dict(meal_id=order_data['order_to_update']))
        Order.update_order()

        return make_response(
            jsonify({'message': 'Order Updated successfully', 'status_code': 202})), 202



# ADD THE VIEWS
signup = SignUp.as_view('signup_view')
login = Login.as_view('login_view')

meals_views = MealsViews.as_view('meals_views')
get_meal_by_id = GetMealById.as_view('get_meal_by_id')

get_menu_of_the_day = MenusView.as_view('get_menu_of_the_day')
set_menu_the_day = MenusView.as_view('set_menu_of_the_day')

make_order = OrdersView.as_view('make_order')
get_all_orders = OrdersView.as_view('all_orders')
modify_order = OrdersView.as_view('modify_order')


endpoints_blueprint.add_url_rule('/auth/signup', view_func=signup, methods=['POST'])
endpoints_blueprint.add_url_rule('/auth/login', view_func=login, methods=['POST'])

endpoints_blueprint.add_url_rule('/meals/', view_func=meals_views, methods=['POST'])
endpoints_blueprint.add_url_rule('/meals/', view_func=meals_views, methods=['GET'])
endpoints_blueprint.add_url_rule('/meals/<mealId>', view_func=get_meal_by_id, methods=['GET'])
endpoints_blueprint.add_url_rule('/meals/<mealId>', view_func=meals_views, methods=['PUT', 'DELETE'])


endpoints_blueprint.add_url_rule('/menu/', view_func=get_menu_of_the_day, methods=['GET'])
endpoints_blueprint.add_url_rule('/menu/', view_func=set_menu_the_day, methods=['POST'])

endpoints_blueprint.add_url_rule('/orders/', view_func=make_order, methods=['POST'])
endpoints_blueprint.add_url_rule('/orders/', view_func=get_all_orders, methods=['GET'])
endpoints_blueprint.add_url_rule('/orders/<orderId>', view_func=modify_order, methods=['PUT'])
