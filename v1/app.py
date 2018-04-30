# API ENDPOINTS
from flask import Flask, render_template, session, request, redirect, url_for, jsonify, make_response
from flask_socketio import SocketIO
from flask_api import FlaskAPI, status
import json
from validate_email import validate_email
from models import User, Meal, Menu, Order


 # Initialize the Flask application
app = FlaskAPI(__name__, instance_relative_config=True)
asyncMode = None
socketio  = SocketIO(app, async_mode=asyncMode)


#Initialise the Data structures to be used to Capture Data
app_users = []
app_vendor_admins = {}
app_meals = {}
app_menu = {}
app_orders = {}
# meal = Meal('Goat Luwombo with All Foods', '23000')
# menu = Menu(meal)
# order = Order(user, meal)



# API ENDPOINTS
#Sign up a user either as a customer or vendor admin
@app.route('/auth/signup', methods=['POST'])
def sign_up():
    user_email = request.get_json(force=True)['email']
    user_password = request.get_json(force=True)['password']
    user_admin = request.get_json(force=True)['admin']
    if len(user_email) > 0 and len(user_password) > 0:
        # for user in app_users:
        #     if user.email == user_email:
        #         return make_response(jsonify({'message': 'User already exists. Please login.'})), 200

        user = User(user_email, user_password, user_admin)
        app_users.append(user)
        return make_response(jsonify({'message': 'Successfully Registered. Please login'})), 201   
    else:
        return make_response(jsonify({'message': 'Missing Credentials'})), 400
 


#authenticate customers or admin
@app.route('/auth/login', methods=['POST'])
def login():
    user_email = request.get_json(force=True)['email']
    user_password = request.get_json(force=True)['password']
    #check if user data exists
    if len(user_email) > 0 and len(user_password) > 0:
        for user in app_users:
            if user.email == user_email:
                return make_response(jsonify({'message': 'Logged in succcessfully'})), 200
        return make_response(jsonify({'message': 'Invalid Email or Password'})), 200        
    else:
        return make_response(jsonify({'message': 'Missing Credentials'})), 200





#Return all the available meals to the vendor admin
@app.route('/meals/', methods=['GET'])
def get_all_meals():
    return make_response(jsonify({
        'data': app_meals
    })), 200

# Return a meal for a particular ID
@app.route('/meals/<mealId>', methods=['GET'])
def get_meal_by_id(mealId):
    if len(app_meals) > 0:
        if mealId in app_meals:
            return make_response(jsonify({
                'message': 'Meal Exists',
            })), 200
        else:
            return make_response(jsonify({
                'message': 'Meal not Found',
            })), 404
    else:
        return make_response(jsonify({'message': 'Meal are empty.'})), 200    

#Allow the vendor admin to add another meal option
@app.route('/meals/', methods=['POST'])
def add_meal():
    # retrieve the meal option submitted
    meal = request.get_json(force=True)['meal']
    mealPrice = request.get_json(force=True)['price']

    app_meals[str(meal)] = str(mealPrice)
    return make_response(jsonify({
        'message': 'Meal Added Successfully',
        'meal': meal
    })), 201

#Allow the ADMIN to edit a particular meal option
@app.route('/meals/<mealId>', methods=['PUT'])
def update_a_meal(mealId):
    if len(app_meals) > 0:
        mealUpdate = request.get_json(force=True)['meal_update']
        mealPrice = app_meals[mealId]
        app_meals.pop(mealId, None) #REMOVE THE PREVIOUS ENTRY
        app_meals[mealUpdate] = mealPrice #Add the New Entry
        return make_response(jsonify({
            'message': 'Meal Updated successfully',
            'data': app_meals
        })), 200
    else:
        return make_response(jsonify({'message': 'You can not modify empty meals'})), 200

#Allow the admin to delete a particular meal option
@app.route('/meals/<mealId>', methods=['DELETE'])
def delete_a_meal(mealId):
    if len(app_meals) > 0:
        del app_meals[mealId]
        return make_response(jsonify({
            'message': 'Meal Deleted successfully'
        })), 200
    else:
        return make_response(jsonify({'message': 'Meals are Empty'})), 200




#Allow the admin an operation to the set the menu of the day
@app.route('/menu/', methods=['POST'])
def set_menu_of_the_day():
    meal = request.get_json(force=True)['meal']
    price = request.get_json(force=True)['price']
    app_menu[meal] = price
    return make_response(jsonify({'data': app_menu})), 201

#Allow the authenticated users to view menu of the day
@app.route('/menu/', methods=['GET'])
def get_menu_of_the_day():
    return make_response(jsonify({
        'data': app_menu
    })), 200




#Allow the authenticated users to make orders from the menu of the day
@app.route('/orders/', methods=['POST'])
def make_order():
    meal = request.get_json(force=True)['meal']
    userId = request.get_json(force=True)['user']
    app_orders[userId] = meal
    return make_response(jsonify({
        'message': 'Order Made successfully',
        'orderId': userId,
        'data': app_orders
        })), 201

#Allow the user to modify an order they've already made
@app.route('/orders/<orderId>', methods=['PUT'])
def modify_order(orderId):
    if len(app_orders) > 0:
        order_update = request.get_json(force=True)['order_to_update']
        app_orders[orderId] = app_orders.pop(orderId)
        app_orders.pop(orderId, None) #REMOVE THE PREVIOUS ORDER ENTRY
        app_orders[orderId] = order_update #Add the New Entry
        return make_response(jsonify({'message': 'Order Updated successfully'})), 200
    else:
        return make_response(jsonify({'message': 'Orders are Empty'})), 200

#Allow the Admin return all the Orders users have made
@app.route('/orders/', methods=['GET'])
def  get_all_orders():
    return make_response(jsonify({'data': app_orders})), 200


# Run the app :)
if __name__ == '__main__':
    app.run(debug=True)
	# socketio.run(app, host="127.0.0.1", port=int("5556"), debug=True)
  
