# Book A Meal API 
from flask import Flask, session, render_template, request, redirect, url_for, jsonify, make_response, current_app
from flask_api import FlaskAPI, status
import json


def create_app():
    # Initialize the Flask application
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = "boOk-a-MeAL"
    asyncMode = None

    from v1.api.endpoints import endpoints_blueprint
    app.register_blueprint(endpoints_blueprint, url_prefix='/api/v1')
    
    return app