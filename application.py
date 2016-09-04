import cgi
import jinja2
import os
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash

from database_setup import Base, Category, Item, User

# Initilize Flask
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



@app.route('/')
@app.route('/catalog')
def catalog_root_page():

    categories = session.query(Category).all()

    latest_items = session.query(Item).order_by(desc(Item.created_date)).limit(10).all()

    return render_template('catalog_root_page.html',
                           categories=categories,
                           latest_items=latest_items)


@app.route('/catalog/<string:category>')
def category_page(category):

    try:
        category_obj = session.query(Category).filter_by(name=category).one()
    except NoResultFound:
        flash("Invalid URL")
        return redirect(url_for('catalog_root_page'))

    category_items = session.query(Item).filter_by(category_id=category_obj.id).all()

    categories = session.query(Category).all()

    return render_template('category_page.html',
                           category_name=category,
                           categories=categories,
                           category_items=category_items)


@app.route('/catalog/<string:category_name>/<string:item_name>/')
def item_page(category_name, item_name):

    try:
        category_obj = session.query(Category).filter_by(name=category_name).one()
    except NoResultFound:
        flash("Invalid URL")
        return redirect(url_for('catalog_root_page'))

    item = session.query(Item).filter_by(name=item_name, category_id=category_obj.id).one()

    return render_template('item.html', item=item)


@app.route('/catalog/new', methods=['GET', 'POST'])
def add_item_page():

    if request.method == 'POST':

        # Get all request parameter
        item_name = request.form['item_name']
        item_description = request.form['item_description']
        item_price = request.form['item_price']
        item_category = request.form['item_category']

        # TODO: Query for user
        user_obj = session.query(User).filter_by(email="konrad.schieban@gmail.com").one()
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
        return render_template('add_item.html', categories=categories)


@app.route('/catalog/<string:category_name>/<string:item_name>/edit', methods=['GET', 'POST'])
def edit_item_page(category_name, item_name):

    if request.method == 'POST':

        # Get all request parameter
        item_name = request.form['item_name']
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

        return redirect(url_for('item_page', category_name=item_category, item_name=item_name))

    else:  # GET
        try:
            category_obj = session.query(Category).filter_by(name=category_name).one()
            item = session.query(Item).filter_by(name=item_name, category_id=category_obj.id).one()
        except NoResultFound:
            flash("Invalid URL")
            return redirect(url_for('catalog_root_page'))

        categories = session.query(Category).all()
        return render_template('edit_item.html', categories=categories, item=item)


@app.route('/catalog/<string:category_name>/<string:item_name>/delete', methods=['GET', 'POST'])
def delete_item_page(category_name, item_name):

    if request.method == 'POST':

        item_id = request.form['item_id']
        category_id = request.form['category_id']
        item = session.query(Item).filter_by(id=item_id, category_id=category_id).one()
        category_name = item.category.name
        session.delete(item)
        session.commit()

        flash("Menu item deleted.")

        return redirect(url_for('category_page', category=category_name))

    else:  # GET
        try:
            category_obj = session.query(Category).filter_by(name=category_name).one()
            item = session.query(Item).filter_by(name=item_name, category_id=category_obj.id).one()
        except NoResultFound:
            flash("Invalid URL")
            return redirect(url_for('catalog_root_page'))

        return render_template('delete_item.html', item=item)


if __name__ == '__main__':
    app.secret_key = "password1234."
    app.debug = True
    app.run(host='0.0.0.0', port=5000)