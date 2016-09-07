from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, make_response
from flask import session as login_session
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import jinja2
import httplib2
import json
import requests
import os
import random
import string

from database_setup import Base, Category, Item, User

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog App"

# Initialize Flask
app = Flask(__name__)

# Initialize Jinja2
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

# SETUP DATABASE
engine = create_engine('sqlite:///catalogApp.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


@app.route('/gdisconnect')
def gdisconnect():

    try:
        access_token = login_session['credentials']
    except KeyError:
        flash("Failed to get access token")
        return redirect('/')

    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['credentials']
    print url
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result

    del login_session['credentials']
    del login_session['gplus_id']
    del login_session['username']
    del login_session['email']
    del login_session['picture']

    flash("Successfully logged out.")

    return redirect('/')


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # Create New User if not already exists:
    user = session.query(User).filter_by(email=data['email']).first()
    if user:
        print user.email + " already exists."
    else:
        new_user = User(name=data['name'], email=data['email'], picture_url=data['picture'])
        session.add(new_user)
        session.commit()

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "asdf " + login_session['username']
    print "done!"
    return output


@app.route('/')
@app.route('/catalog')
def catalog_root_page():

    is_logged_in = None
    if 'username' in login_session:
        is_logged_in = True

    categories = session.query(Category).all()

    latest_items = session.query(Item).order_by(desc(Item.created_date)).limit(10).all()

    print login_session

    return render_template('catalog_root_page.html',
                           title="Catalog App",
                           is_logged_in=is_logged_in,
                           categories=categories,
                           latest_items=latest_items)


@app.route('/catalog.json')
def catalog_json():

    categories = session.query(Category).all()
    return jsonify(Catalog=[cat.serialize for cat in categories])


@app.route('/catalog/<string:category>')
def category_page(category):

    is_logged_in = None
    if 'username' in login_session:
        is_logged_in = True

    try:
        category_obj = session.query(Category).filter_by(name=category).one()
    except NoResultFound:
        flash("Invalid URL")
        return redirect(url_for('catalog_root_page'))

    category_items = session.query(Item).filter_by(category_id=category_obj.id).all()

    categories = session.query(Category).all()

    return render_template('category_page.html',
                           title="Categories",
                           is_logged_in=is_logged_in,
                           category_name=category,
                           categories=categories,
                           category_items=category_items)


@app.route('/catalog/<string:category>.json')
def category_json(category):

    categories = session.query(Category).filter_by(name=category).all()
    return jsonify(Catalog=[cat.serialize for cat in categories])


@app.route('/catalog/<string:category_name>/<string:item_name>')
def item_page(category_name, item_name):

    if 'email' in login_session:
        is_logged_in = True
        current_user_email = login_session['email']
    else:
        is_logged_in = None
        current_user_email = None

    try:
        category_obj = session.query(Category).filter_by(name=category_name).one()
    except NoResultFound:
        flash("Invalid URL")
        return redirect(url_for('catalog_root_page'))

    item = session.query(Item).filter_by(name=item_name, category_id=category_obj.id).one()

    return render_template('item.html',
                           title="Item",
                           is_logged_in=is_logged_in,
                           item=item,
                           current_user_email=current_user_email)


@app.route('/catalog/<string:category_name>/<string:item_name>.json')
def item_page_json(category_name, item_name):

    try:
        category_obj = session.query(Category).filter_by(name=category_name).one()
    except NoResultFound:
        return jsonify(Item=[])

    item = session.query(Item).filter_by(name=item_name, category_id=category_obj.id).one()

    return jsonify(Item=[item.serialize])


@app.route('/catalog/new', methods=['GET', 'POST'])
def add_item_page():

    if 'username' not in login_session:
        flash("User needs to login before authorized to create an item")
        return redirect('/')

    if request.method == 'POST':

        # Get all request parameter
        item_name = request.form['item_name']

        # Check name for invalid characters because it is part of the item URL
        invalid_chars = set(string.punctuation.replace("_", ""))
        if any(char in invalid_chars for char in item_name):
            flash("Name may not contain special characters")
            return redirect(url_for('add_item_page'))
        elif not item_name:
            flash("Name may not be empty")
            return redirect(url_for('add_item_page'))

        item_description = request.form['item_description']
        item_price = request.form['item_price']
        item_category = request.form['item_category']

        user_obj = session.query(User).filter_by(email=login_session['email']).one()
        category_obj = session.query(Category).filter_by(name=item_category).one()

        new_item = Item(name=item_name,
                        user=user_obj,
                        category=category_obj,
                        description=item_description,
                        price=item_price)
        session.add(new_item)
        session.commit()

        flash("new menu item created!")

        return redirect(url_for('item_page', category_name=item_category, item_name=item_name))

    else:
        categories = session.query(Category).all()
        return render_template('add_item.html',
                               is_logged_in=True,
                               title="Add Item",
                               categories=categories)


@app.route('/catalog/<string:category_name>/<string:item_name>/edit', methods=['GET', 'POST'])
def edit_item_page(category_name, item_name):

    if 'username' not in login_session:
        flash("User needs to login before authorized to create an item")
        return redirect('/')

    try:
        category_obj = session.query(Category).filter_by(name=category_name).one()
        item = session.query(Item).filter_by(name=item_name, category_id=category_obj.id).one()
    except NoResultFound:
        flash("Invalid URL")
        return redirect(url_for('catalog_root_page'))

    # if user has not created this item, redirect him
    if not item.user.email == login_session['email']:
        flash("Permission denied")
        return redirect(url_for('catalog_root_page'))

    if request.method == 'POST':

        # Get all request parameters
        item_name = request.form['item_name']

        # Check name for invalid characters because it is part of the item URL
        invalid_chars = set(string.punctuation.replace("_", ""))
        if any(char in invalid_chars for char in item_name):
            flash("Name may not contain special characters")
            return redirect(url_for('add_item_page'))
        elif not item_name:
            flash("Name may not be empty")
            return redirect(url_for('add_item_page'))

        item_description = request.form['item_description']
        item_price = request.form['item_price']
        item_category = request.form['item_category']
        item_id = request.form['item_id']

        category_obj = session.query(Category).filter_by(name=item_category).one()

        # Update of item attributes
        item = session.query(Item).filter_by(id=item_id).one()
        item.name = item_name
        item.description = item_description
        item.price = item_price
        item.category = category_obj

        session.add(item)
        session.commit()

        flash("Menu item updated!")

        return redirect(url_for('item_page',
                                is_logged_in=True,
                                title="Item",
                                category_name=item_category,
                                item_name=item_name))

    else:  # GET

        categories = session.query(Category).all()
        return render_template('edit_item.html',
                               is_logged_in=True,
                               title="Edit Item",
                               categories=categories,
                               item=item)


@app.route('/catalog/<string:category_name>/<string:item_name>/delete', methods=['GET', 'POST'])
def delete_item_page(category_name, item_name):

    if 'username' not in login_session:
        flash("User needs to login before authorized to delete an item")
        return redirect('/')

    try:
        category_obj = session.query(Category).filter_by(name=category_name).one()
        item = session.query(Item).filter_by(name=item_name, category_id=category_obj.id).one()
    except NoResultFound:
        flash("Invalid URL")
        return redirect(url_for('catalog_root_page'))

    # if user has not created this item, redirect him
    if not item.user.email == login_session['email']:
        flash("Permission denied")
        return redirect(url_for('catalog_root_page'))

    if request.method == 'POST':

        item_id = request.form['item_id']
        category_id = request.form['category_id']
        item = session.query(Item).filter_by(id=item_id, category_id=category_id).one()
        category_name = item.category.name
        session.delete(item)
        session.commit()

        flash("Menu item deleted.")

        return redirect(url_for('category_page',
                                title="Categories",
                                category=category_name))

    else:  # GET

        return render_template('delete_item.html',
                               is_logged_in=True,
                               title="Delete Item",
                               item=item)


# Create anti-forgery state token
@app.route('/login')
def show_login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


if __name__ == '__main__':
    app.secret_key = "password1234."
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
