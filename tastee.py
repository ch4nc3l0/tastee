#!/usr/bin/env python3.7.1
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask, request, url_for, render_template, redirect, session, make_response, jsonify
from apiclient import discovery
from oauth2client import client
import random, string, os, httplib2


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
os.environ['DATABASE_URL'] = 'postgres://xoouzbxomnkewv:cda6adaed150127e02ff3fd307dbcbf26da99fc512809e0bc2ae5d8a63c8ec68@ec2-50-17-193-83.compute-1.amazonaws.com:5432/dfac869n1u1id'
app.static_folder = 'static'
db = SQLAlchemy(app)

from models import Restaurant, MenuItem

    
    
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


@app.route('/storeauthcode', methods=['GET', 'POST'])
def storeauthcode():
    if request.method == "POST":
        auth_code = request.json['authResult']
    

    if not request.headers.get('X-Requested-With'):
        redirect(url_for('restaurant'))

    CLIENT_SECRET_FILE = 'client_secrets.json'

    # Exchange auth code for access token, refresh token, and ID token
    credentials = client.credentials_from_clientsecrets_and_code(
    CLIENT_SECRET_FILE,
    ['https://www.googleapis.com/auth/drive.appdata', 'profile', 'email'],
    auth_code)

    # Call Google API
    http_auth = credentials.authorize(httplib2.Http())
    drive_service = discovery.build('drive', 'v3', http=http_auth)
    appfolder = drive_service.files().get(fileId='appfolder').execute()

    # Get profile info from ID token
    userid = credentials.id_token['sub']
    email = credentials.id_token['email']