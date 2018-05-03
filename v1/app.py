# Book A Meal API 
from flask import Flask, session, render_template, request, redirect, url_for, jsonify, make_response, current_app
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




#DOCUMENTATION ROUTE
@app.route('/')
def show_app_home():
    return render_template('app_home.html')


# API AUTHENTICATION ENDPOINTS
@app.route('/api/v1/auth/signup', methods=['POST'])
def sign_up():
    #Sign up a user either as a customer or vendor admin
    username = request.get_json(force=True)['username']
    user_email = request.get_json(force=True)['email']
    user_password = request.get_json(force=True)['password']
    user_admin = request.get_json(force=True)['admin']
    if len(user_email) > 0 and len(user_password) > 0:

        user = User(username, user_email, generate_password_hash(user_password), user_admin)
        check_user_exists = user.check_exists(user_email)
        
        if check_user_exists:
            return make_response(jsonify({'message': 'User already exists. Please login.'})), 200
        else:
            user.save()
            return make_response(jsonify({
                'message': 'Successfully Registered. Please login',
                'status_code': 201,
                'data': user.get_user_object_as_dict()
                })), 201 
    else:
        return make_response(jsonify({'message': 'Missing Credentials'})), 400
 

@app.route('/api/v1/auth/login', methods=['POST'])
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
            'message': 'Logged in successfully',
            'status_code': 200,
            'token': encoded_jwt_token.decode('UTF-8')
            })), 200
        
    return make_response(jsonify({'message': 'Invalid Email or Password'})), 401 




# API MEALS ENDPOINTS
@app.route('/api/v1/meals/', methods=['GET'])
@auth_decorator.token_required_to_authenticate
def get_all_meals(current_user):
    #Verify If User is admin
    if not current_user:
        return jsonify({'message': 'You need to login as Admin to perform this operation.'})

    #Return all the available meals to the vendor admin
    return make_response(jsonify({
        'message': 'success',
        'status_code': 200,
        'data': models.app_meals
    })), 200


@app.route('/api/v1/meals/<mealId>', methods=['GET'])
def get_meal_by_id(mealId):
    # Return a meal for a particular ID
    if len(models.app_meals) > 0:

        for meal in models.app_meals:
            if mealId == meal['meal_id']:
                return make_response(jsonify({ 'message': 'Meal Exists' })), 200

        return make_response(jsonify({ 'message': 'Meal not Found' })), 404

    else:
        return make_response(jsonify({'message': 'Meal are empty.'})), 404    


@app.route('/api/v1/meals/', methods=['POST'])
@auth_decorator.token_required_to_authenticate
def add_meal(current_user):
    #Verify If User is admin
    if not current_user:
        return jsonify({'message': 'You need to login as Admin to perform this operation.'})

    #Allow the vendor admin to add another meal option
    meal = request.get_json(force=True)['meal']
    price = request.get_json(force=True)['price']

    meal_object = Meal(meal, price)
    meal_object.add_meal() #ADD MEAL HERE

    meal_as_dict = {}
    meal_as_dict['meal_id'] = meal_object.meal_id
    meal_as_dict['meal'] = meal_object.meal
    meal_as_dict['price'] = meal_object.price

    meal_id = meal_object.meal_id
    return make_response(jsonify({
        'message': 'Meal Added Successfully',
        'status_code': 201,
        'meal_id': meal_id,
        'meal': meal_as_dict
    })), 201


@app.route('/api/v1/meals/<mealId>', methods=['PUT'])
@auth_decorator.token_required_to_authenticate
def update_a_meal(current_user, mealId):
    #Verify If User is admin
    if not current_user:
        return jsonify({'message': 'You need to login as Admin to perform this operation.'})

    #Allow the ADMIN to edit a particular meal option
    meal_update = request.get_json(force=True)['meal_update']
                    
    for i in range(len(models.app_meals)):
        if str(models.app_meals[i]['meal_id']) == str(mealId):
            models.app_meals[i]['meal_id'] = meal_update
            break     

    meal_as_dict = {}
    meal_as_dict['meal_id'] = mealId
    meal_as_dict['meal'] = meal_update

    return make_response(jsonify({
        'message': 'Meal Updated successfully',
        'status_code': 200,
        'data': meal_as_dict
    })), 200



@app.route('/api/v1/meals/<mealId>', methods=['DELETE'])
@auth_decorator.token_required_to_authenticate
def delete_a_meal(current_user, mealId):
    #Verify If User is admin
    if not current_user:
        return jsonify({'message': 'You need to login as Admin to perform this operation.'})

    #Allow the admin to delete a particular meal option
    if len(models.app_meals) > 0:
        
        Meal.delete_meal_by_id(mealId)

        return make_response(jsonify({
            'message': 'Meal Deleted successfully',
            'status_code': 200
        })), 200
    else:
        return make_response(jsonify({'message': 'Meals are Empty'})), 200





# API MENU ENDPOINTS
@app.route('/api/v1/menu/', methods=['POST'])
@auth_decorator.token_required_to_authenticate
def set_menu_of_the_day(current_user):
    #Verify If User is admin
    if not current_user:
        return jsonify({'message': 'You need to login as Admin to perform this operation.'})

    #Allow the admin an operation to the set the menu of the day
    
    date = request.get_json(force=True)['date']
    description = request.get_json(force=True)['description']
    meal_id = request.get_json(force=True)['meal_id']
    menu_name = request.get_json(force=True)['menu_name']

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


@app.route('/api/v1/menu/', methods=['GET'])
@auth_decorator.token_required_to_authenticate
def get_menu_of_the_day(current_user):
    #Verify If User is admin
    if not current_user:
        return jsonify({'message': 'You need to login as Admin to perform this operation.'})

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





# API ORDER ENDPOINTS
@app.route('/api/v1/orders/', methods=['POST'])
def make_order():
    #Allow the authenticated users to make orders from the menu of the day
    meal_id = request.get_json(force=True)['meal']
    user_id = request.get_json(force=True)['user']
    
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
        'orderId': order_id,
        'order': order_as_dict
        })), 201


@app.route('/api/v1/orders/<orderId>', methods=['PUT'])
def modify_order(orderId):
    #Allow the user to modify an order they've already made
    if len(models.app_orders) > 0:
        order_update = request.get_json(force=True)['order_to_update']
        Order.update_order_by_id(orderId, order_update)
        return make_response(jsonify({'message': 'Order Updated successfully'})), 200
    else:
        return make_response(jsonify({'message': 'Orders are Empty', 'status_code': 200})), 200


@app.route('/api/v1/orders/', methods=['GET'])
@auth_decorator.token_required_to_authenticate
def  get_all_orders(current_user):
    #Allow the Admin return all the Orders users have made
    orders_response = {
        'message': 'success',
        'status_code': 200,
        'orders': models.app_orders
    }
    return make_response(jsonify(orders_response)), 200





# Run the app :)
if __name__ == '__main__':
    app.run(debug=True)  