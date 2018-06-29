from werkzeug.security import check_password_hash
from validate_email import validate_email

app_users = []
app_meals = []
app_menu = []
app_orders = []

class User(object):

    def __init__(self, username, email, password, admin):
        self.email = email
        self.password = password
        self.admin = admin
        self.username = username

    #Save a user object to the users as a dict
    def save(self):
        app_users.append(self)

    def get_user_object_as_dict(self):
        user = {}
        user['username'] = self.username
        user['email'] = self.email
        user['admin'] = self.admin
        return user

    #check if a certain user object exists in the app users
    @staticmethod
    def check_exists(user_email):
        for user in app_users:
            if user.email == user_email:
                return True
        return False

    #Check if the password the user is submitting matches the one they registered with
    def verify_user_password(self):
        userdb = User.query.filter_by(email=self.email).first()
        return check_password_hash(userdb.password, self.password)

    def get_user_by_email(self, user_email):
        for user in app_users:
            if user.email == user_email:
                return user
        return None

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


class Meal(object):

    def __init__(self, meal, price):
        self.meal_id = len(app_meals) + 1
        self.meal = meal
        self.price = price

    def add_meal(self):
        meal = {}
        meal['meal_id'] = self.meal_id
        meal['meal'] = self.meal
        meal['price'] = self.price
        app_meals.append(meal)

    @staticmethod
    def update_meal_by_id(mealId, meal_update):
        for meal in app_meals:
            if meal['meal_id'] == mealId:
                price = meal['price']
                app_meals.remove(meal)
                new_meal = {}
                new_meal['meal_id'] = mealId
                new_meal['meal'] = meal_update
                new_meal['price'] = price
                app_meals.append(new_meal)
                break

    @staticmethod
    def check_if_meal_exists(meal):
        for i in range(len(app_meals)):
            if str(app_meals[i]['meal']) == str(meal):
                return True
        return False

    @staticmethod
    def delete_meal_by_id(mealId):
        for i in range(len(app_meals)):
            if str(app_meals[i]['meal_id']) == str(mealId):
                del app_meals[i]
                return True
        return False

    @staticmethod
    def get_meal_by_id(meal_id):
        for meal in app_meals:
            if meal_id == meal['meal_id']:
                return meal
        return None

    @staticmethod
    def is_price_integer(price):
        ''' check if the price is of type integer '''
        if isinstance(price, int):
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



class Menu(object):

    def __init__(self, name, date, description):
        self.name = name
        self.date = date
        self.meals = []
        self.description = description
        self.caterer = None

    @staticmethod
    def add_meal_to_menu(meal_object, date, menu_object):
        meal = {}
        meal['meal_id'] = meal_object['meal_id']
        meal['meal'] = meal_object['meal']
        meal['price'] = meal_object['price']

        #Add Meal to the date's menu
        for menu in app_menu:
            if date == menu['date']:
                menu_object.meals.append(meal)
                break

    def set_menu_of_the_day(self):
        app_menu.append(self)

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


class Order(object):

    def __init__(self, user_id, meal_id):
        self.order_id = len(app_orders) + 1
        self.user_id = user_id
        self.caterer_id = None
        self.meal_id = meal_id
        self.expiry_time = None

    def make_order(self):
        order = {}
        order['order_id'] = self.order_id
        order['user_id'] = self.user_id
        order['meal_id'] = self.order_id
        app_orders.append(order)

    @staticmethod
    def update_order_by_id(order_id, order_to_update):
        for i in range(len(app_orders)):
            if str(app_orders[i]['order_id']) == str(order_id):
                app_orders[i]["meal_id"] = order_to_update
                return True
        return False

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
