from werkzeug.security import check_password_hash, generate_password_hash
from flask import jsonify, make_response
from validate_email import validate_email
from v1.api.utils import UtilHelper
from v1.api import db


class User(db.Model):
    """ User Object to define users """

    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(1000), nullable=False)
    admin = db.Column(db.Boolean, nullable=False)

    def __init__(self, username, email, password, admin):
        self.email = email
        self.password = password
        self.admin = admin
        self.username = username

    # Save a user object to the users as a dict

    def save(self):
        db.session.add(self)
        db.session.commit()

    def get_user_object_as_dict(self):
        user = {}
        user['username'] = self.username
        user['email'] = self.email
        user['admin'] = self.admin
        return user

    # Verify user registration data

    @staticmethod
    def validate_user_registration_data(user_data):
        message, status_code, validation_pass = '', 0, True

        user = User.instantiate_user(user_data)

        if UtilHelper.check_for_empty_variables(user_data['email'], user_data['password'], user_data['username'], user_data['admin']):
            message = 'Missing Credentials'
            status_code, validation_pass = 400, False
        elif not User.is_email_valid(user_data['email']):
            # CHECK IF EMAIL IS VALID
            message = 'Email is Invalid'
            status_code, validation_pass = 401, False
        elif user.check_if_user_exists():
            message = 'User already exists. Please login.'
            status_code, validation_pass = 200, False
        return {'message': message, 'status_code': status_code, 'validation_pass': validation_pass}

    # Verify user login data

    @staticmethod
    def validate_user_login_data(user_data, user_object):
        message, status_code, validation_pass = '', 0, True

        if UtilHelper.check_for_empty_variables(user_data['email'], user_data['password'], user_data['admin']):
            message = 'Could not verify. Login credentials required.'
            status_code, validation_pass = 401, False
        elif not User.is_email_valid(user_data['email']):
            # CHECK IF EMAIL IS VALID
            message = 'Email is Invalid'
            status_code, validation_pass = 401, False
        elif not user_object.check_if_user_exists():
            message = 'User email not found!!'
            status_code, validation_pass = 401, False
        elif not user_object.verify_user_password():
            message = 'Invalid/Wrong Password'
            status_code, validation_pass = 401, False
        return {'message': message, 'status_code': status_code, 'validation_pass': validation_pass}

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

    # Check if the password the user is submitting matches the one they
    # registered with

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

    @staticmethod
    def instantiate_user(data):
        return User(data['username'], data['email'], generate_password_hash(
            str(data['password'])), data['admin'])

    def __repr__(self):
        return "<User(user_id = '%s', username ='%s', password='%s', email='%s', admin='%s')>" % (
            self.user_id, self.username, self.password, self.email, self.admin)
