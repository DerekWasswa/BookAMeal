from flask import Flask, session, request, url_for, jsonify, make_response, current_app
from flask_api import FlaskAPI, status

app = FlaskAPI(__name__, instance_relative_config=True)

def __init__(self):
    import unittest
    tests = unittest.TestLoader().discover('v1', pattern='test_app.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    return not result.wasSuccessful()


if __name__ == '__main__':
    app.run()