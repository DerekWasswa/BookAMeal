from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, jsonify, make_response
from v1.api.utils import UtilHelper
from v1.api import db
from v1.api.models.meals import Meal
from v1.api.models.users import User

associate_meals_to_menu = db.Table('menu_meals',
                                   db.Column(
                                       'menu_id',
                                       db.Integer,
                                       db.ForeignKey('menus.menu_id'),
                                       primary_key=True),
                                   db.Column('meal_id', db.Integer, db.ForeignKey('meals.meal_id', ondelete='CASCADE'), primary_key=True))


class Menu(db.Model):
    """ Menu object that defines the menu in the db """
    __tablename__ = 'menus'
    menu_id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    meals = db.relationship('Meal',
                            secondary=associate_meals_to_menu,
                            lazy='subquery',
                            backref=db.backref('menu', cascade='all,delete', passive_deletes=True, lazy=True)
                            )
    date = db.Column(db.Date, nullable=False)

    def __init__(self, name, date, description, vendor_id):
        self.name = name
        self.date = date
        self.meals = []
        self.description = description
        self.vendor_id = vendor_id

    @staticmethod
    def add_meals_to_menu():
        db.session.commit()

    def create_menu(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def commit_menu_changes():
        ''' Invoke when Deleting meal option off the menu '''
        db.session.commit()

    @staticmethod
    def get_menu_of_the_day(day):
        menudb = Menu.query.filter_by(date=day)
        menu_list = []
        for menu in menudb:
            menu_list.append(Menu.get_menu_as_dict(menu))
        return menu_list

    @staticmethod
    def get_vendor_menus(vendor_id):
        menudb = Menu.query.filter_by(vendor_id=vendor_id).order_by(Menu.date.desc())
        menu_list = []
        for menu in menudb:
            menu_list.append(Menu.get_menu_as_dict(menu))
        return menu_list

    @staticmethod
    def get_menu_vendor_name(menu_id):
        menudb = Menu.query.filter_by(menu_id=menu_id).first()
        vendor = Menu.get_menu_as_dict(menudb)
        return vendor

    @staticmethod
    def get_menu_as_dict(menudb):
        menu_dict = {}
        meals_list = []

        caterer = User.query.filter_by(user_id=menudb.vendor_id).first()

        menu_dict['menu_id'] = menudb.menu_id
        menu_dict['name'] = menudb.name
        menu_dict['description'] = menudb.description
        menu_dict['vendor_id'] = menudb.vendor_id
        menu_dict['vendor'] = caterer.username
        menu_dict['contact'] = caterer.email
        menu_dict['date'] = menudb.date

        for meal in menudb.meals:
            meals_dict = {}
            meals_dict['meal_id'] = meal.meal_id
            meals_dict['meal'] = meal.meal
            meals_dict['price'] = meal.price
            meals_list.append(meals_dict)

        menu_dict['meals'] = meals_list
        return menu_dict

    @staticmethod
    def check_menu_of_the_day_exists(date_selected):
        ''' check if a menu for a particular dates exists '''
        menudb = Menu.query.filter_by(date=date_selected).first()
        if menudb is not None:
            return True
        return False

    @staticmethod
    def check_caterer_menu_exists(vendor_id, date):
        ''' Check of a particular caterer has already set a menu for a particular date '''
        menudb = Menu.query.filter_by(vendor_id=vendor_id, date=date).first()
        if menudb is not None:
            return True
        return False

    @staticmethod
    def check_meal_exists_in_menu(menu_id, meal_id):
        menudb = Menu.query.filter_by(menu_id=menu_id).first()
        meal_available = False
        for meal in menudb.meals:
            if str(meal.meal_id) == str(meal_id):
                meal_available = True
                break
        return meal_available

    @staticmethod
    def validate_menu_data(menu_data):
        ''' validate the meal data '''
        response = None

        if UtilHelper.check_for_empty_variables(
                menu_data['menu_name'], menu_data['description'], menu_data['date'], menu_data['meal_id']):
            return make_response((jsonify({"message": 'Empty Menu Details.',
            'status_code': 400})), 400)
        elif UtilHelper.validate_exceeds_length(menu_data['menu_name'], 100):
            return make_response((jsonify({"message": 'Menu name should not exceed 100 characters.',
            'status_code': 400})), 400)
        elif not UtilHelper.check_row_id_exists_in_table(Meal, 'meal_id', menu_data['meal_id']):
            return make_response((jsonify({"message": 'Meal with provided ID does not exist.',
            'status_code': 200})), 200)
        return response
