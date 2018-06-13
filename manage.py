import os
import unittest
from flask_script import Manager, Shell
from flask import Flask
from v1.api import create_app, db
from flask_migrate import Migrate, MigrateCommand


# initialize the app with all its configurations
app = create_app('testing')
manager = Manager(app)
migrate = Migrate(app, db)

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