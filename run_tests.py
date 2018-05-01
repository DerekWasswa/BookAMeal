import os
import unittest
from flask import Flask, current_app
from flask_api import FlaskAPI

# initialize the app with all its configurations
app = FlaskAPI(__name__, instance_relative_config=True)
app(config_name=os.getenv('APP_SETTINGS'))


@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('v1', pattern='test_app.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    
    return not result.wasSuccessful()

if __name__ == '__main__':
    app.run()
