from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, jsonify, make_response
from validate_email import validate_email
from v1.api.utils import UtilHelper
from v1.api import db
from v1.api.models.users import User
from v1.api.models.menu import Menu

class Order(db.Model):
    """ Order Object to define the Order in the db """
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menus.menu_id'))
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.meal_id'))
    user = db.Column(db.String(100), db.ForeignKey('users.email'))
    date = db.Column(db.Date, nullable=False)

    def __init__(self, user, meal_id, menu_id, date):
        self.user = user
        self.meal_id = meal_id
        self.menu_id = menu_id
        self.expiry_time = None
        self.date = date

    def save_order(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def update_order():
        db.session.commit()

    @staticmethod
    def get_all_orders(orders_from_db):
        ''' return all orders as dict '''
        orders_list = []
        for order in orders_from_db:
            order_dict = {}
            order_dict['order_id'] = order.order_id
            order_dict['user'] = order.user
            order_dict['meal_id'] = order.meal_id
            order_dict['menu_id'] = order.menu_id
            order_dict['date'] = order.date
            orders_list.append(order_dict)
        return orders_list

    @staticmethod
    def order_as_dict(order):
        ''' a single order as a dict '''
        order_as_dict = {}
        order_as_dict['order_id'] = order.order_id
        order_as_dict['user'] = order.user
        order_as_dict['meal_id'] = order.meal_id
        order_as_dict['menu_id'] = order.menu_id
        order_as_dict['date'] = order.date
        return order_as_dict

    def validate_order_data(self):
        ''' validate the Order data '''
        response = None
        response_menu_eixstance = self.validate_order_user_meal_menu_exist()

        if UtilHelper.check_for_empty_variables(
                self.meal_id, self.user, self.date, self.menu_id):
            return make_response((jsonify({"message": 'Can not order with empty content.', 'status_code': 400})), 400)
        elif not UtilHelper.validate_email(self.user):
            return make_response((jsonify({"message": 'User Email not valid.', 'status_code': 400})), 400)
        elif not response_menu_eixstance['validation_pass']:
            return make_response((jsonify({"message": response_menu_eixstance['message'],
             'status_code': response_menu_eixstance['status_code']})), response_menu_eixstance['status_code'])
        return response

    def validate_order_update_data(self, order_data):
        ''' validate the Order data '''
        response = None
        response_menu_exists = self.validate_order_user_meal_menu_exist()

        if UtilHelper.check_for_empty_variables(
                order_data['order_to_update'], order_data['user'], order_data['meal_id'], order_data['menu_id']):
            return make_response((jsonify({"message":"Can not modify an order with empty content.",
            'status_code': 400})), 400)
        elif not response_menu_exists['validation_pass']:
            return make_response((jsonify({"message": response_menu_exists['message'],
             'status_code': response_menu_exists['status_code']})), response_menu_exists['status_code'])
        return response

    def validate_order_user_meal_menu_exist(self):
        user = User('', self.user, '', '')
        message, status_code, validation_pass = '', 0, True
        if not user.check_if_user_exists():
            # check if the user is a registered user and is logged
            message = 'User doesnot exist or is not logged in.'
            status_code, validation_pass = 401, False
        elif not UtilHelper.check_row_id_exists_in_table(Menu, 'menu_id' , self.menu_id):
            # verify if menu id exists and has the meal id specified
            message = 'Menu ID does not exist.'
            status_code, validation_pass = 400, False
        elif not Menu.check_meal_exists_in_menu(
                self.menu_id, self.meal_id):
                 # if false then meal does not exist
            message = 'Meal ID does not exist in the menu of the day'
            status_code, validation_pass = 400, False
        return {'message': message, 'status_code': status_code, 'validation_pass': validation_pass}
