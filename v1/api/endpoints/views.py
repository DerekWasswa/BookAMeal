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
from v1.api import db
import datetime


class SignUp(MethodView):

    def post(self):
        #Sign up a user either as a customer or vendor admin
        user_data = request.get_json(force=True)
        if 'username' not in user_data or 'email' not in user_data or 'password' not in user_data or 'admin' not in user_data:
            return make_response(jsonify({'message': 'Signup expects username, email, password, admin value, either of them is not provided.'})), 400

        username = user_data['username']
        user_email = user_data['email']
        user_password = user_data['password']
        user_admin = user_data['admin']

        if len(str(user_email)) > 0 or len(str(user_password)) > 0 or len(str(username)) > 0 or len(str(user_admin)) > 0:

            user = User(username, user_email, generate_password_hash(user_password), user_admin)

            #CHECK IF EMAIL IS VALID
            is_valid = validate_email(user_email)
            if not is_valid:
                return make_response(jsonify({'message': 'Email is Invalid'})), 401

            # CHECK IF USER ALREADY EXISTS
            userdb = User.query.filter_by(email=user_email).first()
            if userdb is not None:    
                return make_response(jsonify({'message': 'User already exists. Please login.'})), 200
            else:

                #ADD THE USER TO THE DB SESSION
                db.session.add(user)
                db.session.commit()

                return make_response(jsonify({
                    'message': 'Successfully Registered. Please login',
                    'status_code': 201,
                    'data': user.get_user_object_as_dict()
                    })), 201 
        else:
            return make_response(jsonify({'message': 'Missing Credentials'})), 400

class Login(MethodView):

    def post(self):
        #authenticate customers or admin
        user_data = request.get_json(force=True)
        if 'email' not in user_data or 'password' not in user_data or 'admin' not in user_data:
            return make_response(jsonify({'message': 'Logged requests expects email, password, and admin value. Either of them id not provided.'})), 400

        user_email = user_data['email']
        user_password = user_data['password']
        user_admin = user_data['admin']
        
        if len(str(user_email)) <= 0 or len(str(user_password)) <= 0 or len(str(user_admin)) <= 0:
            return make_response(jsonify({'message': 'Could not verify. Login credentials required.'})), 401

        #CHECK IF EMAIL IS VALID
        is_valid = validate_email(user_email)
        if not is_valid:
            return make_response(jsonify({'message': 'Email is Invalid'})), 401

        user = User.query.filter_by(email=user_email).first()
        if user is None:
            return make_response(jsonify({'message': 'User email not found!!'})), 401 

        if user.verify_user_password(user_password):
            #Create the app instance to use to generate the token
            app = create_app()

            # CREATE TOKEN: leverage isdangerous to create the token
            encoded_jwt_token = jwt.encode({
                'admin': user_admin, 
                'email': user_email
                }, app.config['SECRET_KEY'], algorithm='HS256')

            #ADD USER ID TO THE CURRENT USER DATA
            print(user.user_id)
            session['user_id'] = user.user_id

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

        # Return all meals from the db
        meals = Meal.query.all()
        meals_list = []
        for meal in meals:
            meal_dict = {}
            meal_dict['meal_id'] = meal.meal_id
            meal_dict['meal'] = meal.meal
            meal_dict['price'] = meal.price
            meal_dict['vendor_id'] = meal.vendor_id
            meals_list.append(meal_dict)

        return make_response(jsonify({
            'message': 'success',
            'status_code': 200,
            'data': meals_list
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
        vendor_id = session['user_id']

        if len(str(meal)) <= 0 or  len(str(price)) <= 0:
            return make_response(jsonify({'message': 'Meal Options Missing.'})), 400

        #Try parsing the Price, If doesnot pass the try then cast error
        if not isinstance(price, int):
            return make_response(jsonify({'message': 'Meal Price has to be an Integer.'})), 400
        
        # check if the meal has already been entered
        mealdb = Meal.query.filter_by(meal=meal).first()
        if mealdb is not None:    
            return jsonify({'message': 'Meal already exists.'}), 400

        meal_object = Meal(meal, price, vendor_id)
        
        #ADD THE USER TO THE DB SESSION
        db.session.add(meal_object)
        db.session.commit()

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
            

        meal_update = Meal.query.filter_by(meal_id=mealId, vendor_id=session['user_id']).update(dict(meal=meal_update, price=price_update))
        db.session.commit()

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
        meals = db.session.query(Meal).count()
        if meals > 0:

            delete_status = Meal.query.filter_by(meal_id=mealId, vendor_id=session['user_id']).delete()
            db.session.commit() 

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
        meals = db.session.query(Meal).count()
        if meals > 0:      

            mealdb = Meal.query.filter_by(meal_id=mealId).first()
            if mealdb is not None:    
                return make_response(jsonify({ 'message': 'Meal Exists' })), 200

            return make_response(jsonify({ 'message': 'Meal not Found' })), 404

        else:
            return make_response(jsonify({'message': 'Meal are empty.'})), 404            








class GetMenuOfTheDay(MethodView):
    """ Have customers retrieve the menu of the day """
    def get(self):   

        #Allow the authenticated users to view menu of the day
        today = datetime.date.today()
        menudb = Menu.query.filter_by(date=today).first()

        if menudb is not None:  
            menu_dict = {}
            meals_list = []

            menu_dict['menu_id'] = menudb.menu_id 
            menu_dict['name'] = menudb.name
            menu_dict['description'] = menudb.description
            menu_dict['vendor_id'] = menudb.vendor_id

            for meal in menudb.meals:
                meals_dict = {}
                meals_dict['meal_id'] = meal.meal_id
                meals_dict['meal'] = meal.meal
                meals_dict['price'] = meal.price
                meals_list.append(meals_dict)
            
            menu_dict['meals'] = meals_list
            
            return make_response(jsonify({
                'message': 'success',
                'status_code': 200,
                'data': menu_dict
            })), 200  

        else:
            return make_response(jsonify({'message': 'No menu set for the day ' + today, 'status_code': 200})), 200
      

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
    
        #CHECK IF THE MEAL ID EXISTS
        mealdb = Meal.query.filter_by(meal_id=meal_id).first()
        if mealdb is None:    
            return make_response(jsonify({ 'message': 'Meal with id ' + meal_id + ' does not exist.' })), 400

        #CHECK IF THE MENU OF THE DAY ALREADY EXISTS
        menudb = Menu.query.filter_by(vendor_id=session['user_id'], date=date).first()
        if menudb is not None:
            menudb.meals.append(mealdb)
            db.session.commit()
        else:
            create_new_menu = Menu(menu_name, date, description, session['user_id'])
            create_new_menu.meals.append(mealdb)
            db.session.add(create_new_menu)
            db.session.commit()

        return make_response(jsonify({'status_code': 201, 'message': 'success'})), 201        







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