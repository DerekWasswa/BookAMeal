# Book A Meal API
from flask import Flask, session, render_template, request, redirect, url_for, jsonify, make_response, current_app
from flask_api import FlaskAPI, status
import json
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app(configuration):
    # Initialize the Flask application
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = "boOk-a-MeAL"

    asyncMode = None

    if configuration == 'production':
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', 'postgresql://localhost/book_a_meal_db')#pragma:no cover
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False#pragma:no cover
        db.init_app(app)#pragma:no cover

    if configuration == 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/book_a_meal_test_db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)

    from v1.api.endpoints import endpoints_blueprint
    app.register_blueprint(endpoints_blueprint, url_prefix='/api/v1')

    return app
