<h1>Catalog App</h1>

Version 1.0

URL: https://localhost:5000/

_Catalog App_ is a web application which shows a catalog with items of a specific category, their description and price.
Items can be seen by every user but only user who have logged in with their Google+ account can create new items. Items can be edited or deleted
only by the user who created the item

<h2>1. Content</h2>

    - Blog
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

<b>4.1. Signup with your Google+ account:</b>
    Users can login to the app by authenticating with their Google+ account.
    Click on the button _Login_ in the Navigation bar to get to the page http://localhost:5000/login to login.

<b>4.2. Categories</b>
    Items in the catalog are grouped by different categories.
    Categories can be sen on the left side on http://localhost:5000/ or http://localhost:5000/categories

<b>4.3. Logout:</b>
    Users log out at the URL https://blogks1.appspot.com/blog/logout. After logging out, the authentication cookie is cleared.

<b>4.4. Blog Page:</b>
    Blog posts can be seen at https://blogks1.appspot.com/blog/ . Posts that the current user created can be edited or deleted with the buttons
    below the post. However, only other users can user the buttons to like/dislike the post. A post can only liked or disliked once. If the user
    disobeys this rule, an error message occurs.
    Users can comment on posts that a other users created but they cannot comment on their own posts. Comments can be edited or deleted.

<b>4.5. Create New Posts:</b>
    Blog posts can be created at https://blogks1.appspot.com/blog/newPost. Every post needs a subject and a blog text. After creation of a new post,
    the user is redirected to a permalink, showing the new post.












