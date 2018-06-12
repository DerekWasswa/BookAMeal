from werkzeug.security import check_password_hash
from . import db

app_users = []
app_meals = []
app_menu = []
app_orders = []

class User(db.Model):
    """ User Object to define users """

    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)  
    password = db.Column(db.String(200), nullable=False)
    admin = db.Column(db.Boolean, nullable=False)

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
    def verify_user_password(self, user_password):
        return check_password_hash(self.password, user_password)    

    def get_user_by_email(self, user_email):
        for user in app_users:
            if user.email == user_email:
                return user
        return None  

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




class Menu(db.Model):
    """ Menu object that defines the menu in the db """
    __tablename__ = 'menus'
    menu_id = db.Column(db.Integer, primary_key = True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.Date, nullable=False)  
    

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


class Order(db.Model):
    """ Order Object to define the Order in the db """
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.meal_id'))

    def __init__(self, user_id, meal_id):
        self.order_id = len(app_orders) + 1
        self.user_id = user_id
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

         