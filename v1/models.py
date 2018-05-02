from werkzeug.security import check_password_hash

app_users = []
app_meals = {}
app_menu = {}
app_orders = {}

class User(object):

    def __init__(self, user_name, email, password, admin):
        self.email = email
        self.password = password
        self.admin = admin
        self.user_name = user_name

    #Save a user object to the users as a dict 
    def save(self):
        app_users.append(self)

    def get_user_object_as_dict(self):
        user = {}
        user['user_name'] = self.user_name
        user['email'] = self.email
        user['password'] = self.password
        user['admin'] = self.admin
        return user

    #check if a certain user object exists in the app users
    def check_exists(self, user_email):
        for user in app_users:
            if user.email == user_email:
                return user.get_user_object_as_dict
        return None  

    #Check if the password the user is submitting matches the one they registered with
    def verify_user_password(self, user_password):
        return check_password_hash(self.password, user_password)    

    def get_user_by_email(self, user_email):
        for user in app_users:
            if user.email == user_email:
                return user
        return None  

class Caterer(object):

    def __init__(self, vendor_name, email, password):
        self.vendor_name = vendor_name
        self.email = email
        self.password = password
        self.meals = []
        self.menu = []
        self.orders = []

class Meal(object):

    def __init__(self, meal, price):
        self.meal = meal
        self.price = price

    def add_meal(self):
        app_meals[self.meal] = self.price

    def update_meal_by_id(self, mealId, meal_update):
        meal_price = app_meals[mealId]
        app_meals.pop(mealId, None) # REMOVE THE PREVIOUS ENTRY
        app_meals[meal_update] = meal_price # ADD THE NEW ENTRY

    def delete_meal_by_id(self, mealId):
        del app_meals[mealId]
    

class Menu(object):

    def __init__(self):
        self.menu_name = None
        self.menu_date = None
        self.caterer = None
        
    def add_meal_to_menu(self, meal, price):
        app_menu[meal] = price   

class Order(object):

    def __init__(self, user_id, meal_id):
        self.order_id = None
        self.user_id = user_id
        self.caterer_id = None
        self.meal_id = meal_id
        self.expiry_time = None

    def make_order(self):
        app_orders[self.user_id] = self.meal_id   

    def update_order_by_id(self, order_id, order_to_update):
        app_orders[order_id] = app_orders.pop(order_id)
        app_orders.pop(order_id, None) #REMOVE THE PREVIOUS ORDER ENTRY
        app_orders[order_id] = order_to_update #Add the New Entry