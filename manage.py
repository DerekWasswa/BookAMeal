import os
import unittest
from flask_script import Manager, Shell
from flask import Flask
from v1.api import create_app, db
from v1.api.models.users import User
from v1.api.models.meals import Meal
from v1.api.models.menu import Menu
from v1.api.models.orders import Order
from flask_migrate import Migrate, MigrateCommand


# initialize the app with all its configurations
app = create_app('production')
manager = Manager(app)
migrate = Migrate(app, db)

def shell_context():
    return dict(app=app, User=User, Meal=Meal, Menu=Menu, db=db, Order=Order)

manager.add_command("shell", Shell(make_context=shell_context))
manager.add_command("db", MigrateCommand)

@manager.command
def upgrade_changes():
    """ Upgrade application to reflect the changes in the db """
    from flask_migrate import upgrade
    upgrade()

# Usage: python test_app.py test
@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('./v1/tests', pattern='*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    return not result.wasSuccessful()


if __name__ == '__main__':
    manager.run()
