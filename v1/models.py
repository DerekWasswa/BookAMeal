#Users
#Meal
#Menu
#Order

class User(object):
    app_users = []
    def __init__(self, email, password, admin):
        self.email = email
        self.password = password
        self.admin = admin

class Meal(object):
    app_meals = []
    def __init__(self, meal, price):
        self.meal = meal
        self.price = price

class Menu(object):
    app_menu = []
    def __init__(self, Meal):
        self.meal = Meal

class Order(object):
    app_orders = []
    def __init__(self, User, Meal):
        self.user = User
        self.meal = Meal