# Book A Meal API 
from flask import Flask, session, render_template, request, redirect, url_for, jsonify, make_response, current_app
from flask_api import FlaskAPI, status
import json
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def create_app(configuration):
    # Initialize the Flask application
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = "boOk-a-MeAL"
    
    if configuration == 'development':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/book_a_meal_db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    if configuration == 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/book_a_meal_test_db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    asyncMode = None

    db.init_app(app)
    with app.test_request_context():
        db.create_all()

    from v1.api.endpoints import endpoints_blueprint
    app.register_blueprint(endpoints_blueprint, url_prefix='/api/v1')
    
    return app