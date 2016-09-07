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
_Catalog App_ uses the application server framework _Flask_ and the ORM framework _sqlacademy_.
Information on how Flask can be installed can be found here: 
 - Flask: http://flask.pocoo.org/docs/0.11/installation/
 - SQLAlchemy: http://docs.sqlalchemy.org/en/latest/intro.html

<h2>3. Locally deploy the server</h2>
To create the http listeners and deploy the content on the local machine, open a terminal, navigate to the folder <i>Blog</i> and run

    > python <path/to/google_app_engine>/dev_appserver.py .

<h2>4. Blog Features</h2>

<b>4.1. Signup as a new user:</b>
    New users have to signup on https://blogks1.appspot.com/blog/signup. Users who are currently not logged in and try to access the blog
    are automatically redirected to the signup page.
    Valid usernames are between 3 and 20 characters and may only contain alphabetical characters as well as a dash (-) and underscore (_).
    Valid passwords may contain all characters and are between 3 and 20 characters long.
    Note, that the email address is an optional input on the signup page.

<b>4.2. Login:</b>
    Users log in at the URL https://blogks1.appspot.com/blog/login. After successful login, a secure authentication cookie is created.

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












