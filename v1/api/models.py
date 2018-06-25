from werkzeug.security import check_password_hash
from flask import jsonify, make_response
from validate_email import validate_email
from . import db


class User(db.Model):
    """ User Object to define users """

    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(1000), nullable=False)
    admin = db.Column(db.Boolean, nullable=False)

    def __init__(self, username, email, password, admin):
        self.email = email
        self.password = password
        self.admin = admin
        self.username = username


    #Save a user object to the users as a dict
    def save(self):
        db.session.add(self)
        db.session.commit()


    def get_user_object_as_dict(self):
        user = {}
        user['username'] = self.username
        user['email'] = self.email
        user['admin'] = self.admin
        return user


    # verify if the user data requests exist
    @staticmethod
    def user_data_parameters_exist(user_data):
        if 'username' in user_data:
            if 'username' not in user_data or 'email' not in user_data or 'password' not in user_data or 'admin' not in user_data:
                return False
        else:
            if 'email' not in user_data or 'password' not in user_data or 'admin' not in user_data:
                return False
        return True

    @staticmethod
    def user_data_is_empty(user_data):
        if 'username' in user_data:
            if len(str(user_data['email'])) <= 0 or len(str(user_data['password'])) <= 0 or len(str(user_data['username'])) <= 0 or len(str(user_data['admin'])) <= 0:
                return True
        else:
            if len(str(user_data['email'])) <= 0 or len(str(user_data['password'])) <= 0 or len(str(user_data['admin'])) <= 0:
                return True
        return False


    #Check if the password the user is submitting matches the one they registered with
    def verify_user_password(self):
        userdb = User.query.filter_by(email=self.email).first()
        return check_password_hash(userdb.password, self.password)


    @staticmethod
    def is_email_valid(email):
        ''' check if an email address is valid '''
        is_valid = validate_email(email)
        return is_valid


    # Check if a user with a specified email exists or not
    def check_if_user_exists(self):
        userdb = User.query.filter_by(email=self.email).first()
        if userdb is not None:
            return True
        else:
            return False


    def __repr__(self):
        return "<User(user_id = '%s', username ='%s', password='%s', email='%s', admin='%s')>" % (self.user_id, self.username, self.password, self.email, self.admin)




class Meal(db.Model):
    """ Meal Object to define a meal in the database """

    __tablename__ = 'meals'
    meal_id = db.Column(db.Integer, primary_key = True)
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
    def retrieve_all_meals():
        '''' Return all meals from the db '''
        meals = Meal.query.all()
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
    def meals_empty():
        ''' return the count of the meals in the database '''
        meals = db.session.query(Meal).count()
        if meals > 0:
            return False
        return True

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

    @staticmethod
    def is_meal_available(meal_id):
        meal_obj = Meal.query.filter_by(meal_id=meal_id).first()
        if meal_obj is not None:
            return True
        return False

    @staticmethod
    def meal_request_data_keys_exist(meal_data=None, invoke_from=None):
        ''' Verify if the api ping has the request keys provided '''
        if invoke_from=='add_meal_option':
            if 'meal' not in meal_data or 'price' not in meal_data:
                return False
        else:
            if 'meal_update' not in meal_data or 'price_update' not in meal_data:
                return False
        return True

    @staticmethod
    def meal_request_data_empty(meal=None, price=None):
        ''' verify whether the request data parameters are not empty '''
        if len(str(meal)) <= 0 or len(str(price)) <= 0:
            return True
        return False




associate_meals_to_menu = db.Table('menu_meals',
    db.Column('menu_id', db.Integer, db.ForeignKey('menus.menu_id'), primary_key=True),
    db.Column('meal_id', db.Integer, db.ForeignKey('meals.meal_id'), primary_key=True))

class Menu(db.Model):
    """ Menu object that defines the menu in the db """
    __tablename__ = 'menus'
    menu_id = db.Column(db.Integer, primary_key = True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    meals = db.relationship('Meal',
    secondary= associate_meals_to_menu,
    lazy='subquery',
    backref=db.backref('menu', lazy=True)
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
    def get_menu_as_dict(menudb):
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
        return menu_dict

    @staticmethod
    def check_menu_of_the_day_exists(date_selected):
        ''' check if a menu for a particular dates exists '''
        menudb = Menu.query.filter_by(date=date_selected).first()
        if menudb is not None:
            return True
        return False

    @staticmethod
    def menu_request_data_keys_exist(menu_data=None):
        ''' Verify if the api ping has the request keys provided '''
        if 'date' not in menu_data or 'description' not in menu_data or 'menu_name' not in menu_data or 'meal_id' not in menu_data:
            return False
        return True

    @staticmethod
    def menu_request_data_empty(menu_name=None, description=None, date=None, meal_id=None):
        ''' verify whether the request data parameters are not empty '''
        if len(str(menu_name)) <= 0 or len(str(description)) <= 0 or len(str(date)) <= 0 or len(str(meal_id)) <= 0:
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
    def check_if_a_menu_exists(menu_id):
        menudb = Menu.query.filter_by(menu_id=menu_id).first()
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




class Order(db.Model):
    """ Order Object to define the Order in the db """
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key = True)
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
    def orders_empty():
        ''' return the count of the Orders in the database '''
        orders = db.session.query(Order).count()
        if orders > 0:
            return False
        return True

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

    @staticmethod
    def order_request_data_keys_exist(order_data=None):
        ''' Verify if the api ping has the order request keys provided '''
        if 'order_to_update' in order_data:
            if 'meal_id' not in order_data or 'user' not in order_data or 'order_to_update' not in order_data or 'menu_id' not in order_data:
                return False
        else:
            if 'meal' not in order_data or 'user' not in order_data or 'date' not in order_data or 'menu_id' not in order_data:
                return False
        return True

    @staticmethod
    def order_request_data_empty(meal=None, user=None, date=None, menu_id=None):
        ''' verify whether the request order data parameters are not empty '''
        if len(str(meal)) <= 0 or len(str(user)) <= 0 or len(str(date)) <= 0 or len(str(menu_id)) <= 0:
            return True
        return False
