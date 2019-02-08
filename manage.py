import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from tastee import app, db

app.config.from_object(os.environ['APP_SETTINGS'])
os.environ['DATABASE_URL'] = 'postgres://xoouzbxomnkewv:cda6adaed150127e02ff3fd307dbcbf26da99fc512809e0bc2ae5d8a63c8ec68@ec2-50-17-193-83.compute-1.amazonaws.com:5432/dfac869n1u1id'

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()