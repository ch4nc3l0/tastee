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
@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    restaurant = Restaurant.query.filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        restaurant.name = request.form['editedRestaurantName']
        db.session.add(restaurant)
        db.session.commit()
        return redirect(url_for('restaurants'))
    elif request.method == 'GET':
        return render_template('editRestaurant.html', restaurant_id='restaurant_id', restaurant=restaurant)


# Delete restaurant
@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    restaurant = Restaurant.query.filter_by(id = restaurant_id).one() 
    if request.method == 'POST':
        if 'redirect' in request.form:
            return redirect(url_for('restaurants'))
        elif 'delete' in request.form:
            db.session.delete(restaurant)
            db.session.commit()
            return redirect(url_for('restaurants'))
    elif request.method == 'GET':
        return render_template('deleteRestaurant.html', restaurant_id='restaurant_id', restaurant=restaurant)    


# Show all menu items for a restaurant
@app.route('/restaurant/<int:restaurant_id>/menu', methods=['GET', 'POST'])
def showMenu(restaurant_id):
    restaurant = Restaurant.query.filter_by(id = restaurant_id).one()
    menu = MenuItem.query.filter_by(restaurant_id=restaurant_id)
    if request.method == 'POST':
        return redirect(url_for('newMenuItem', restaurant_id=restaurant_id))
    elif request.method == 'GET':
        return render_template('restaurantMenu.html', restaurant_id='restaurant_id', restaurant=restaurant, menu=menu)


# Add new menu items to a restaurant
@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    restaurant = Restaurant.query.filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        newMenu = MenuItem(
            course = request.form['menuCourse'],
            description = request.form['menuDescription'],
            name = request.form['menuName'],
            price = request.form['menuPrice'],
            restaurant_id = restaurant_id
        )
        db.session.add(newMenu)
        db.session.commit()
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    elif request.method == 'GET':
        return render_template('newRestaurantMenuItem.html', restaurant_id='restaurant_id', restaurant=restaurant)


# Edit menu items from a restaurant
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menuItem_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menuItem_id):
    restaurant = Restaurant.query.filter_by(id = restaurant_id).one()
    menu = MenuItem.query.filter_by(id = menuItem_id).one()
    if request.method == 'POST':
        menu.course = request.form['editedMenuCourse']
        menu.description = request.form['editedMenuDescription']
        menu.name = request.form['editedMenuName']
        menu.price = request.form['editedMenuPrice']
        db.session.add(menu)
        db.session.commit()
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    elif request.method == 'GET':
        return render_template('editRestaurantMenuItem.html', restaurant_id=restaurant_id, menuItem_id=menuItem_id, menu=menu, restaurant=restaurant)


# Delete menu items from a restaurant
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menuItem_id>/delete', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menuItem_id):
    menu = MenuItem.query.filter_by(id = menuItem_id).one()
    if request.method == 'POST':
        if 'redirect' in request.form:
            return redirect(url_for('showMenu', restaurant_id=restaurant_id))
        elif 'delete' in request.form:
            db.session.delete(menu)
            db.session.commit()
            return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    elif request.method == 'GET':
        return render_template('deleteRestaurantMenu.html', restaurant_id='restaurant_id', menuItem_id=menuItem_id, menu=menu)


if __name__ == '__main__':
    app.secret_key = 'key'
    app.debug = True
    app.run(host = '192.168.50.4', port = 8080)
    