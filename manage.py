from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    name = db.Column(db.String(80), nullable = False)
    id = db.Column(db.Integer, primary_key = True)


class MenuItem(db.Model):
    __tablename__ = 'menuItem'
    course = db.Column(db.String(250))
    description = db.Column(db.String(250))
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable = False)
    price = db.Column(db.String(8))
    restaurant = db.relationship(Restaurant)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))

if __name__ == '__main__':
    manager.run()