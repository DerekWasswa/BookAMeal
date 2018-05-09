from functools import wraps
from flask import request, jsonify, current_app
import jwt

def token_required_to_authenticate(admin_status):
    @wraps(admin_status)
    def authenticate_decorator(*args, **kwargs):
        token = None
        if 'app-access-token' in request.headers:
            token = request.headers['app-access-token']

        if not token:
            return jsonify({'message': 'No token in the headers'}), 401

        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'])   
            user_admin = payload['admin']
            print(user_admin)
        except:
            return jsonify({'message': 'Token is Invalid.'}), 401 

        return admin_status(user_admin, *args, **kwargs)
    return authenticate_decorator  
