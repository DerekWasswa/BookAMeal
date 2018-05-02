import os
import unittest
from flask_script import Manager
from flask import Flask

# initialize the app with all its configurations
app = Flask(__name__)
app(config_name=os.getenv('APP_SETTINGS'))
manager = Manager(app)

# Usage: python test_app.py test
@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('/v1', pattern='test*.py'
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    return not result.wasSuccessful()



if __name__ == '__main__':
    manager.run()