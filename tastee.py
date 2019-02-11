#!/usr/bin/env python3.7.1
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask, request, url_for, render_template, redirect, session, make_response
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
import random, string, os, json, httplib2, requests


CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']


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


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    return render_template("login.html", STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid State'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data

    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentails = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response= make_response(json.dumps('Failed to upgrad auth code'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = credentails.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    h=httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    gplus_id = credentails.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps('Tokens user id does not match given user id'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response   

    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps('Tokens client id does not match apps'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response   

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print ("done!")
    return output