from werkzeug.security import check_password_hash
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

    #Check if the password the user is submitting matches the one they registered with
    def verify_user_password(self, user_password):
        return check_password_hash(self.password, user_password)     

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
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def delete_meal():
        db.session.commit()      

    def get_meal_as_dict(self):
        meal_as_dict = {}
        meal_as_dict['meal_id'] = self.meal_id
        meal_as_dict['meal'] = self.meal
        meal_as_dict['price'] = self.price
        return meal_as_dict




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
    def get_all_orders(orders_from_db):
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
        order_as_dict = {}
        order_as_dict['order_id'] = order.order_id
        order_as_dict['user'] = order.user
        order_as_dict['meal_id'] = order.meal_id
        order_as_dict['menu_id'] = order.menu_id
        order_as_dict['date'] = order.date
        return order_as_dict


         