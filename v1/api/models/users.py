from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, jsonify, make_response
from validate_email import validate_email
from v1.api.utils import UtilHelper
from v1.api import db


class User(db.Model):
    """ User Object to define users """

    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(1000), nullable=False, unique=True)
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
        response = None
        user = User.instantiate_user(user_data)
        message, status, validation = '', 0, True

        if UtilHelper.check_for_empty_variables(user_data['email'], user_data['password'],
            user_data['username'], user_data['admin']):
            message, status, validation = 'Missing Credentials', 400, False
        elif UtilHelper.validate_exceeds_length(user_data['username'], 100):
            message, status, validation = 'Username length should be less than 100 characters.', 400, False
        elif not User.is_email_valid(user_data['email']):
            message, status, validation = 'Email is Invalid', 401, False
        elif user.check_if_user_exists():
            message, status, validation = 'User already exists. Please login.', 200, False

        if not validation:
            return make_response((jsonify({"message": message, 'status_code': status})), status)
        return response


    # Verify user login data

    @staticmethod
    def validate_user_login_data(user_data, user_object):
        response = None
        message, status, validation = '', 0, True

        if UtilHelper.check_for_empty_variables(user_data['email'], user_data['password'], user_data['admin']):
            message, status, validation = 'Could not verify. Login credentials required.', 401, False
        elif not User.is_email_valid(user_data['email']):
            message, status, validation = 'Email is Invalid', 401, False
        elif not user_object.check_if_user_exists():
            message, status, validation = 'User email not found!!', 401, False
        elif not user_object.verify_user_password():
            message, status, validation = 'Invalid/Wrong Password', 401, False

        if not validation:
            return make_response((jsonify({"message": message, 'status_code': status})), status)
        return response


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

    def get_user_id(self):
        userdb = User.query.filter_by(email=self.email).first()
        return userdb.user_id


    @staticmethod
    def instantiate_user(data):
        return User(data['username'], data['email'], generate_password_hash(
            str(data['password'])), data['admin'])

    def __repr__(self):
        return "<User(user_id = '%s', username ='%s', password='%s', email='%s', admin='%s')>" % (
            self.user_id, self.username, self.password, self.email, self.admin)
