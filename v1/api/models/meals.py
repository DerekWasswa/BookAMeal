from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, jsonify, make_response
from v1.api.utils import UtilHelper
from v1.api import db


class Meal(db.Model):
    """ Meal Object to define a meal in the database """

    __tablename__ = 'meals'
    meal_id = db.Column(db.Integer, primary_key=True)
    meal = db.Column(db.Text, nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    def __init__(self, meal, price, vendor_id):
        self.meal = meal
        self.price = price
        self.vendor_id = vendor_id

    def save(self):
        ''' Save the Meal Option '''
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def commit_meal_changes():
        ''' Invoke when Deleting or Updating the meal option '''
        db.session.commit()

    @staticmethod
    def retrieve_all_meals(vendor_id):
        '''' Return all meals from the db '''
        meals = Meal.query.filter_by(vendor_id=vendor_id)
        meals_list = []
        for meal in meals:
            meal_dict = {}
            meal_dict['meal_id'] = meal.meal_id
            meal_dict['meal'] = meal.meal
            meal_dict['price'] = meal.price
            meal_dict['vendor_id'] = meal.vendor_id
            meals_list.append(meal_dict)
        return meals_list

    @staticmethod
    def validate_meal_data(meal_data, meal_object):
        ''' validate the meal data '''
        response = None

        if UtilHelper.check_for_empty_variables(meal_data['meal'], meal_data['price']):
            return make_response((jsonify({"message": 'Meal Options Missing.',
            'status_code': 400})), 400)
        elif not Meal.is_price_integer(meal_data['price']):
            # Try parsing the Price, If doesnot pass the try then cast error
            return make_response((jsonify({"message": 'Meal Price has to be an Integer.',
            'status_code': 400})), 400)
        elif meal_object.is_meal_already_existing():
            # check if the meal has already been entered
            return make_response((jsonify({"message": 'Meal already exists.',
            'status_code': 400})), 400)
        return response

    @staticmethod
    def validate_meal_update_data(meal, price, mealId):
        ''' validate the meal data '''
        response = None
        if not UtilHelper.check_row_id_exists_in_table(Meal, 'meal_id', mealId):
            return make_response((jsonify({"message": 'Update Incomplete! Meal does not exist.',
            'status_code': 404})), 404)
        elif UtilHelper.check_for_empty_variables(meal, price):
            return make_response((jsonify({"message": 'Can not update meal with empty meal options',
            'status_code': 400})), 400)
        elif not Meal.is_price_integer(price):
            return make_response((jsonify({"message": 'Can not update meal with non integer price',
            'status_code': 400})), 400)
        return response

    @staticmethod
    def validate_meal_deletion(mealId):
        ''' validate the meal deletion checks '''
        message, status_code, validation_pass = '', 0, True

        if check_empty_database_table(Meal):
            message = 'Meals are Empty'
            status_Code, validation_pass = 200, False
        elif not UtilHelper.check_row_id_exists_in_table(Meal, 'meal_id', mealId):
            message = 'Deletion Incomplete! Meal Not Found.'
            status_code, validation_pass = 404, False
        return {'message': message, 'status_code': status_code, 'validation_pass': validation_pass}

    @staticmethod
    def get_meal_by_id_validation(mealId):
        message, status_code, validation_pass = '', 0, True

        if db.session.query(Meal).count() < 1:
            message, status_code, validation_pass = 'Meal are empty.', 200, False

        if UtilHelper.check_row_id_exists_in_table(Meal, 'meal_id', mealId):
            message, status_code, validation_pass = 'Meal Exists', 200, False

        return {'message': message, 'status_code': status_code, 'validation_pass': validation_pass}

    @staticmethod
    def get_meal_by_id(meal_id):
        mealdb = Meal.query.filter_by(meal_id=meal_id).first()
        return mealdb.get_meal_as_dict()

    def get_meal_as_dict(self):
        ''' return a meal option as a dictionary '''
        meal_as_dict = {}
        meal_as_dict['meal_id'] = self.meal_id
        meal_as_dict['meal'] = self.meal
        meal_as_dict['price'] = self.price
        return meal_as_dict

    def is_meal_already_existing(self):
        ''' check if the meal is already in the db '''
        mealdb = Meal.query.filter_by(meal=self.meal).first()
        if mealdb is not None:
            return True
        else:
            return False

    @staticmethod
    def is_price_integer(price):
        ''' check if the price is of type integer '''
        if isinstance(price, int):
            return True
        return False
