#!/usr/bin/env python3.7.1
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, url_for, render_template, redirect


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurantmenu.db'
db = SQLAlchemy(app)


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
    
    
# Show all restaurants
@app.route('/')
@app.route('/restaurants/', methods=['GET', 'POST'])
def restaurants():
    restaurants = Restaurant.query.all()
    if request.method == 'POST':
        return redirect(url_for('newRestaurant'))
    return render_template('restaurants.html', restaurants=restaurants)


# Add new restaurant
@app.route('/restaurant/new', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name = request.form['newRestaurant'])
        db.session.add(newRestaurant)
        db.session.commit()
        return redirect(url_for('restaurants'))
    elif request.method == 'GET':
        return render_template('newRestaurant.html')


# Edit restaurant
@app.route('/restaurant/<int:restaurant_id>/edit')
def editRestaurant(restaurant_id):
    return 'edit rest'


# Delete restaurant
@app.route('/restaurant/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id):
    return 'delete rest'


# Show all menu items for a restaurant
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    return 'Menu here'


# Add new menu items to a restaurant
@app.route('/restaurant/<int:restaurant_id>/menu/new')
def newMenuItem(restaurant_id):
    return 'add new menu item'


# Edit menu items from a restaurant
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menuItem_id>/edit')
def editMenuItem(restaurant_id, menuItem_id):
    return 'Edit Menu Item here'


# Delete menu items from a restaurant
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menuItem_id>/delete')
def deleteMenuItem(restaurant_id, menuItem_id):
    return 'Delete Menu Item here'


if __name__ == '__main__':
    app.secret_key = 'key'
    app.debug = True
    app.run(host = '192.168.50.4', port = 8080)