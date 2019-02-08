from tastee import db


class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    name = db.Column(db.String(80), nullable = False)
    id = db.Column(db.Integer, primary_key = True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<id {}>'.format(self.id)


class MenuItem(db.Model):
    __tablename__ = 'menuItem'
    course = db.Column(db.String(250))
    description = db.Column(db.String(250))
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable = False)
    price = db.Column(db.String(8))
    restaurant = db.relationship(Restaurant)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))

    def __init__(self, course, description, price, restaurant, name, restaurant_id):
        self.name = name
        self.course = course
        self.description = description
        self.price = price
        self.restaurant = restaurant
        self.restaurant_id = restaurant_id

    def __repr__(self):
        return '<id {}>'.format(self.id)