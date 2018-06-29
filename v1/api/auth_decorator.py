from functools import wraps
from flask import Flask, request, g, jsonify, current_app
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
            user_id = payload['user_id']
            g.user_id = user_id
        except BaseException:
            return jsonify({'message': 'Token is Invalid.'}), 401

        return admin_status(user_admin, *args, **kwargs)
    return authenticate_decorator
