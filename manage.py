# manage.py
from dotenv import load_dotenv
load_dotenv()



# import unittest
# import coverage


from src import create_app, db
from src.models import *
import os
os.getenv("SQLALCHEMY_DATABASE_URI")

app = create_app(test_config=None)
app.app_context().push()

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import logging

migrate = Migrate()
migrate.init_app(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

# COV = coverage.coverage(
#     branch=True,
#     include='api/*',
#     omit=['api/tests/*', 'api/server/config.py', 'api/server/*/__init__.py'],
# )

# COV.start()
# migrations
@manager.command
def run():
    app.run(host='localhost', port='5000')
    logging.info('Flask app run')

@manager.command
def recreate_db():
    # Recreate a local db
    db.drop_all()
    db.create_all()
    db.session.commit()
    logging.warning("DB was recreated.")

# @manager.command
# def test():
#     tests = unittest.TestLoader().discover('api/tests', pattern='test*.py')
#     result = unittest.TextTestRunner(verbosity=2).run(tests)
#     if result.wasSuccessful():
#         return 0
#     return 1
if __name__ == '__main__':
    manager.run()
