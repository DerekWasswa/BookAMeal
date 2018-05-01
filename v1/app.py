# Book A Meal API 
from flask import Flask, session, request, redirect, url_for, jsonify, make_response, current_app
from flask_api import FlaskAPI, status
import json
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Meal, Menu, Order
import models
import datetime
import jwt
import auth_decorator


 # Initialize the Flask application
app = FlaskAPI(__name__, instance_relative_config=True)
app.config['SECRET_KEY'] = "boOk-a-MeAL"
asyncMode = None





# API AUTHENTICATION ENDPOINTS
@app.route('/auth/signup', methods=['POST'])
def sign_up():
    #Sign up a user either as a customer or vendor admin
    user_name = request.get_json(force=True)['user_name']
    user_email = request.get_json(force=True)['email']
    user_password = request.get_json(force=True)['password']
    user_admin = request.get_json(force=True)['admin']
    if len(user_email) > 0 and len(user_password) > 0:

        user = User(user_name, user_email, generate_password_hash(user_password), user_admin)
        check_user_exists = user.check_exists(user_email)
        
        if check_user_exists:
            return make_response(jsonify({'message': 'User already exists. Please login.'})), 200
        else:
            user.save()
            return make_response(jsonify({
                'message': 'Successfully Registered. Please login',
                'data': user.get_user_object_as_dict()
                })), 201 
    else:
        return make_response(jsonify({'message': 'Missing Credentials'})), 400
 

@app.route('/auth/login', methods=['POST'])
def login():
    #authenticate customers or admin
    user_email = request.get_json(force=True)['email']
    user_password = request.get_json(force=True)['password']
    user_admin = request.get_json(force=True)['admin']
    
    if len(user_email) <= 0 and len(user_password) <= 0:
        return make_response(jsonify({'message': 'Could not verify. Login credentials required.'})), 401

    user = User('', user_email, user_password, user_admin)
    if not user.check_exists(user_email):
        make_response(jsonify({'message': 'Invalid Email or Password'})), 401 

    app_user = user.get_user_by_email(user_email)
    if check_password_hash(app_user.password, user_password):
        # CREATE TOKEN: leverage isdangerous to create the token
        encoded_jwt_token = jwt.encode({
            'admin': user_admin, 
            'email': user_email
            }, app.config['SECRET_KEY'], algorithm='HS256')
        return make_response(jsonify({
            'token': encoded_jwt_token.decode('UTF-8'),
            'message': 'Logged in successfully'})), 200
        
    return make_response(jsonify({'message': 'Invalid Email or Password'})), 401 




# API MEALS ENDPOINTS
@app.route('/meals/', methods=['GET'])
@auth_decorator.token_required_to_authenticate
def get_all_meals(current_user):
    #Verify If User is admin
    if not current_user:
        return jsonify({'message': 'You need to login as Admin to perform this operation.'})

    #Return all the available meals to the vendor admin
    return make_response(jsonify({
        'data': models.app_meals
    })), 200


@app.route('/meals/<mealId>', methods=['GET'])
def get_meal_by_id(mealId):
    # Return a meal for a particular ID
    if len(models.app_meals) > 0:
        if mealId in models.app_meals:
            return make_response(jsonify({
                'message': 'Meal Exists',
            })), 200
        else:
            return make_response(jsonify({
                'message': 'Meal not Found',
            })), 404
    else:
        return make_response(jsonify({'message': 'Meal are empty.'})), 404    


@app.route('/meals/', methods=['POST'])
@auth_decorator.token_required_to_authenticate
def add_meal(current_user):
    #Verify If User is admin
    if not current_user:
        return jsonify({'message': 'You need to login as Admin to perform this operation.'})

    #Allow the vendor admin to add another meal option
    meal = request.get_json(force=True)['meal']
    meal_price = request.get_json(force=True)['price']

    models.app_meals[meal] = meal_price
    return make_response(jsonify({
        'message': 'Meal Added Successfully',
        'meal': meal,
        'meals': models.app_meals
    })), 201


@app.route('/meals/<mealId>', methods=['PUT'])
@auth_decorator.token_required_to_authenticate
def update_a_meal(current_user, mealId):
    #Verify If User is admin
    if not current_user:
        return jsonify({'message': 'You need to login as Admin to perform this operation.'})

    #Allow the ADMIN to edit a particular meal option
    if len(models.app_meals) > 0:
        meal_update = request.get_json(force=True)['meal_update']
        meal_price = models.app_meals[mealId]
        models.app_meals.pop(mealId, None) # REMOVE THE PREVIOUS ENTRY
        models.app_meals[meal_update] = meal_price # ADD THE NEW ENTRY
        return make_response(jsonify({
            'message': 'Meal Updated successfully',
            'data': models.app_meals
        })), 200
    else:
        return make_response(jsonify({'message': 'You can not modify empty meals'})), 200


@app.route('/meals/<mealId>', methods=['DELETE'])
@auth_decorator.token_required_to_authenticate
def delete_a_meal(current_user, mealId):
    #Verify If User is admin
    if not current_user:
        return jsonify({'message': 'You need to login as Admin to perform this operation.'})

    #Allow the admin to delete a particular meal option
    if len(models.app_meals) > 0:
        del models.app_meals[mealId]
        return make_response(jsonify({
            'message': 'Meal Deleted successfully'
        })), 200
    else:
        return make_response(jsonify({'message': 'Meals are Empty'})), 200





# API MENU ENDPOINTS
@app.route('/menu/', methods=['POST'])
@auth_decorator.token_required_to_authenticate
def set_menu_of_the_day(current_user):
    #Verify If User is admin
    if not current_user:
        return jsonify({'message': 'You need to login as Admin to perform this operation.'})

    #Allow the admin an operation to the set the menu of the day
    meal = request.get_json(force=True)['meal']
    price = request.get_json(force=True)['price']
    
    menu = Menu()
    menu.add_meal_to_menu(meal, price)
    return make_response(jsonify({'data': models.app_menu})), 201


@app.route('/menu/', methods=['GET'])
@auth_decorator.token_required_to_authenticate
def get_menu_of_the_day(current_user):
    #Verify If User is admin
    if not current_user:
        return jsonify({'message': 'You need to login as Admin to perform this operation.'})

    #Allow the authenticated users to view menu of the day
    return make_response(jsonify({
        'data': models.app_menu
    })), 200





# API ORDER ENDPOINTS
@app.route('/orders/', methods=['POST'])
def make_order():
    #Allow the authenticated users to make orders from the menu of the day
    meal_id = request.get_json(force=True)['meal']
    user_id = request.get_json(force=True)['user']

    order = Order(user_id, meal_id)
    order.make_order()
    return make_response(jsonify({
        'message': 'Order Made successfully',
        'orderId': user_id,
        'data': models.app_orders
        })), 201


@app.route('/orders/<orderId>', methods=['PUT'])
def modify_order(orderId):
    #Allow the user to modify an order they've already made
    if len(models.app_orders) > 0:
        order_update = request.get_json(force=True)['order_to_update']
        order = Order('', '')
        order.update_order_by_id(orderId, order_update)
        return make_response(jsonify({'message': 'Order Updated successfully'})), 200
    else:
        return make_response(jsonify({'message': 'Orders are Empty'})), 200


@app.route('/orders/', methods=['GET'])
def  get_all_orders():
    #Allow the Admin return all the Orders users have made
    return make_response(jsonify({'data': models.app_orders})), 200





# Run the app :)
if __name__ == '__main__':
    app.run(debug=True)  
