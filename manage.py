# manage.py

import os
import unittest
import coverage

from flask_script import Manager
from flask_migrate import Migrate

COV = coverage.coverage(
    branch=True,
    include='api/*',
    omit=['api/tests/*', 'api/server/config.py', 'api/server/*/__init__.py'],
)

COV.start()

from api.server import app, db, models

migrate= Migrate(app, db)
manager = Manager(app)

# migrations
manager.add_command('db')

@manager.command
def hello():
    print('test')

@manager.command
def test():
    tests = unittest.TestLoader().discover('api/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()