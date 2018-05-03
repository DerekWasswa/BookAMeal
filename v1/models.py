from werkzeug.security import check_password_hash

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
    def delete_meal_by_id(mealId):
        for meal in app_meals:
            if meal['meal_id'] == mealId:
                app_meals.remove(meal)
    
    @staticmethod
    def get_meal_by_id(meal_id):
        for meal in app_meals:
            if meal_id == meal['meal_id']:
                return meal
        return None      





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
        
        for order in app_orders:
            if order_id == order['order_id']:
                order["meal_id"] = order_to_update
                break
         