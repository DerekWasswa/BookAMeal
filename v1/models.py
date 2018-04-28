#Users
#Meal
#Menu
#Order

class User(object):
    
    def __init__(self, email, password):
        self.email = email
        self.password = password

class Meal(object):

    def __init__(self, meal, price):
        self.meal = meal
        self.price = price

class Menu(object):

    def __init__(self, meals, vendor):
        self.meals = meals
        self.vendor = vendor

class Orders(object):

    def __init__(self, user, meal):
        self.user = user
        self.meal = meal