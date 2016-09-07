<h1>Catalog App</h1>

Version 1.0

URL: https://localhost:5000/

_Catalog App_ is a web application which shows a catalog with items of a specific category, their description and price.
Items can be seen by every user but only users who have logged in with their Google+ account can create new items. Items can be edited or deleted
only by the user who has created the item.

<h2>1. Content</h2>

    - CatalogItem
    |-- application.py
    |-- cliet_secrets.json
    |-- database_setup.py
    |-- init_db_items.py
    |-- Readme.md
    |-- static/
        |-- css_bootstrap-theme.min.css
        |-- css_main.css
        |-- js_tools.js
    |-- templates/
        |-- add_item.html
        |-- base.html
        |-- catalog_root_page.html
        |-- category_page.html
        |-- delete_item.html
        |-- edit_item.html
        |-- login.html

<h2>2. Prerequisites</h2>
_Catalog App_ uses the application server framework _Flask_ and the ORM framework _SQLAlchemy_.
Information on how Flask and SQLAlchemy can be installed can be found here: 
 - Flask: http://flask.pocoo.org/docs/0.11/installation/
 - SQLAlchemy: http://docs.sqlalchemy.org/en/latest/intro.html

<h2>3. Locally deploy the server</h2>
To create the http listeners and deploy the content on the local machine, open a terminal, navigate to the folder <i>CatalogApp</i> and run

    > python application.py .

When running the application for the first time no categories and items are in place because the local database is empty.
Test data can be deployed by running the Python script

    > python init_db_data.py

<h2>4. Features</h2>

<b>4.1. Signup with your Google+ account: </b>
    Users can login to the app by authenticating with their Google+ account.
    Click on the button _Login_ in the Navigation bar to get to the page http://localhost:5000/login to login.

<b>4.2. Categories: </b>
    Items in the catalog are grouped by different categories.
    Categories can be seen on the left side on http://localhost:5000/ or http://localhost:5000/catalog

<b>4.3. Items: </b>
    Items of a specific category can be seen by clicking on a category. Each shown item offers a link to the description pae of the item. 

<b>4.4. New Item: </b>
    Users who are logged in find the button _New Item_ in the Navigation bar.
    Users have to specify a name, description (optional) and price (optional) for a new item.
    Since the URL link to each item contains the item name no special characters are permitted.

<b>4.5. Edit/Delete: </b>
    The user who created a specific item has the option to delete and edit an item by navigating to the description page of the item and clicking on _edit_ or _delete_.
    
<b>4.6 REST API: </b>
    The app offers Read-Only endpoints to the user where catalog data can be read in JSON format.
    The following end-points can be accessed by the user:
    
     - http://localhost:5000/catalog.json
        -> Returns information about all items in the catalog
     - http://localhost:5000/catalog/<Category>.json
        -> Returns information about all items in the specified category
     - http://localhost:5000/catalog/<Category>/<Item>.json
        -> Returns only information about the specified item in the specified Category













