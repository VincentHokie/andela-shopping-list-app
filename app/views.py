__author__ = 'MacUser'

from flask import render_template, redirect, flash, session
from . import app
from .forms import LoginForm, SignUpForm, BucketListForm, BucketListItemForm



# class definition to store a user object
class User:
    def __init__(self, username, password, email):
        self.email = email
        self.username = username
        self.password = password
        self.id = len(session["users"]) + 1



# method definition to create the applications session
def create_application_session_keys():
    if "users" not in session:
        session["users"] = []


# method definition to keep logged in users from login and sign up pages
def logged_in_users_redirect():
    if "logged_in" in session and session["logged_in"] is not None:
        flash({
            "message":
            "You're already logged in!"
        })
        return redirect('/view/shopping-lists')


# home page route definition
@app.route("/")
@app.route("/index")
def index():
    create_application_session_keys()

    return render_template("index.html",
                           title='Home')



# authentication route definitions
@app.route("/sign-up", methods=['GET', 'POST'])
def sign_up():

    # if the user is signed in, redirect and notify them
    logged_in_users_redirect()

    create_application_session_keys()

    form = SignUpForm()

    if form.validate_on_submit():
        flash('Login requested for un="%s", pw=%s' %
              (form.username.data, str(form.password.data)))
        return redirect('/login')

    return render_template("auth/sign-up.html",
                           title='Create Profile',
                           form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():

    # if the user is signed in, redirect and notify them
    logged_in_users_redirect()

    create_application_session_keys()

    form = LoginForm()

    if form.validate_on_submit():

        flash(
            {
                "message": 'Login requested for un="%s", pw=%s' %
                           (form.username.data, str(form.password.data)),
                "class_name": "success"
            }
        )

        return redirect('/view/shopping-lists')

    return render_template("auth/login.html",
                           title='Login',
                           form=form)


@app.route("/logout", methods=['GET'])
def logout():
    return render_template("auth/logout.html",
                           title='Logout')
    create_application_session_keys()




# bucket list crud routes
@app.route("/create/shopping-list", methods=['GET', 'POST'])
def create_bucket_list():

    create_application_session_keys()

    form = BucketListForm()

    if form.validate_on_submit():
        flash('Login requested for un="%s", pw=%s' %
              (form.username.data, str(form.password.data)))
        return redirect('/index')

    return render_template("shopping-list/create.html",
                           title='Create Shopping List',
                           form=form)

@app.route("/update/shopping-list/<shopping_list_id>", methods=['GET', 'POST'])
def update_bucket_list(shopping_list_id):

    create_application_session_keys()

    form = BucketListForm()

    if form.validate_on_submit():
        flash('Login requested for un="%s", pw=%s' %
              (form.username.data, str(form.password.data)))
        return redirect('/index')

    return render_template("shopping-list/update.html",
                           title='Update Shopping List',
                           form=form)


@app.route("/view/shopping-lists", methods=['GET', 'POST'])
def view_bucket_list():

    create_application_session_keys()

    return render_template("shopping-list/view.html",
                           title='View Shopping Lists')


@app.route("/delete/shopping-list/<shopping_list_id>", methods=['POST'])
def delete_bucket_list(shopping_list_id):

    create_application_session_keys()

    return "Hello Worldj"





# bucket list items crud routes
@app.route("/create/<shopping_list>/item", methods=['GET', 'POST'])
def create_bucket_list_item(shopping_list):

    create_application_session_keys()

    form = BucketListItemForm()

    if form.validate_on_submit():
        flash('Login requested for un="%s", pw=%s' %
              (form.username.data, str(form.password.data)))
        return redirect('/index')

    return render_template("shopping-list-item/create.html",
                           title='View Shopping List Items',
                           form=form)


@app.route("/update/<shopping_list>/item/<item_id>", methods=['GET', 'POST'])
def update_bucket_list_item(shopping_list, item_id):

    create_application_session_keys()

    form = BucketListItemForm()

    if form.validate_on_submit():
        flash('Login requested for un="%s", pw=%s' %
              (form.username.data, str(form.password.data)))
        return redirect('/index')

    return render_template("shopping-list-item/update.html",
                           title='Update Shopping List item',
                           form=form)


@app.route("/view/<shopping_list>/items", methods=['GET', 'POST'])
def view_bucket_list_item(bucket_list):

    create_application_session_keys()

    return render_template("shopping-list-item/view.html",
                           title='View Shopping List Items')


@app.route("/delete/shopping-list-item/<item_id>", methods=['POST'])
def delete_bucket_list_item(item_id):

    create_application_session_keys()

    return "Hello Worldj"
