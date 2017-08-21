__author__ = 'MacUser'

from flask import Flask

# initialize the flask application
app = Flask(__name__)
app.config.from_object('config_heroku')

import os
from flask import render_template, redirect, flash, session
from datetime import datetime

from forms import LoginForm, SignUpForm, ShoppingListForm, ShoppingListItemForm, DeleteShoppingListForm, DeleteShoppingListItemForm


class Abstract:

    def get_time(self, session_key):
        created_id = os.urandom(10).hex()
        while created_id in session[session_key]:
            created_id = os.urandom(10).hex()

        return created_id

# class definition to store a user object
class User(Abstract):
    def __init__(self, username, password, email):
        self.email = email
        self.username = username
        self.password = password
        self.id = self.get_time("users")


# class definition to store a shopping list object
class ShoppingList(Abstract):
    def __init__(self, name):
        self.name = str(name).title()
        self.time = datetime.now().strftime("%Y-%b-%d %H:%M")
        self.user_id = session["logged_in"]["id"]
        self.id = self.get_time("shopping-lists")


# class definition to store a shopping list item object
class ShoppingListItem(Abstract):
    def __init__(self, name, shopping_list):
        self.name = str(name).title()
        self.shopping_list = shopping_list
        self.user_id = session["logged_in"]["id"]
        self.checked = False
        self.id = self.get_time("shopping-list-items")
        self.time = datetime.now().strftime("%Y-%b-%d %H:%M")


# method definition to create the applications session
def create_application_session_keys():
    if "users" not in session:
        session["users"] = {}

    if "shopping-lists" not in session:
        session["shopping-lists"] = {}

    if "shopping-list-items" not in session:
        session["shopping-list-items"] = {}

    if "logged_in" not in session:
        session["logged_in"] = None


# method definition to keep logged in users from login and sign up pages
def logged_in_users_redirect():
    if "logged_in" in session and session["logged_in"] is not None:
        flash({
            "message":
            "You're already logged in!"
        })
        return True
    else:
        return False


# method definition to keep logged in users from login and sign up pages
def guest_users_redirect():
    if "logged_in" in session and session["logged_in"] is None:
        flash({
            "message":
            "You need to be logged in! Please do that first"
        })
        return True
    else:
        return False

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
    if logged_in_users_redirect():
        return redirect('/view/shopping-lists')

    create_application_session_keys()

    form = SignUpForm()

    if form.validate_on_submit():

        if form.password.data != form.password2.data:
            flash({"message": "Your passwords don't match!"})
            return render_template("auth/sign-up.html",
                               title='Create Profile',
                               form=form)

        new_user = User(
                form.username.data,
                form.password.data,
                form.email.data
            )
        session["users"][new_user.id] = vars(new_user)

        flash({"message": "You have successfully signed up! Login to continue"})

        return redirect('/login')

    return render_template("auth/sign-up.html",
                           title='Create Profile',
                           form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():

    # if the user is signed in, redirect and notify them
    if logged_in_users_redirect():
        return redirect('/view/shopping-lists')

    create_application_session_keys()

    form = LoginForm()

    if form.validate_on_submit():

        users = session["users"]
        for key in users:
            user = users[key]
            if user["username"] == form.username.data.strip() and user["password"] == form.password.data.strip():
                session["logged_in"] = {"username": form.username.data.strip().title(), "id": user["id"]}
                return redirect('/view/shopping-lists')

        flash({
            "message":
            'Login failed! Either your username or password are incorrect'
        })

        return redirect('/login')

    return render_template("auth/login.html",
                           title='Login',
                           form=form)


@app.route("/logout", methods=['GET'])
def logout():

    create_application_session_keys()
    session["logged_in"] = None

    flash({
            "message":
            'You have successfully logged out! Come back soon'
        })

    return redirect('/login')




# shopping list crud routes
@app.route("/create/shopping-list", methods=['GET', 'POST'])
def create_shopping_list():

    create_application_session_keys()

    # if the user is not signed in, redirect and notify them
    if guest_users_redirect():
        return redirect('/login')

    form = ShoppingListForm()

    if form.validate_on_submit():

        new_shopping_list = ShoppingList(form.name.data)
        session["shopping-lists"][new_shopping_list.id] = vars(new_shopping_list)

        flash({"message": "You have successfully created a shopping list! Select it to start adding items to it"})

        return redirect('/view/shopping-lists')

    return render_template("shopping-list/create.html",
                           title='Create Shopping List',
                           form=form)

@app.route("/update/shopping-list/<shopping_list_id>", methods=['GET', 'POST'])
def update_shopping_list(shopping_list_id):

    create_application_session_keys()

    # if the user is not signed in, redirect and notify them
    if guest_users_redirect():
        return redirect('/login')

    form = ShoppingListForm()

    if form.validate_on_submit():
        session["shopping-lists"][shopping_list_id]["name"] = form.name.data
        flash({"message":'Update Successful!'})
        return redirect('/view/shopping-lists')

    shopping_list = session["shopping-lists"][shopping_list_id]
    form = ShoppingListForm()

    return render_template("shopping-list/update.html",
                           title='Update Shopping List',
                           form=form,
                           name=shopping_list["name"],
                           shopping_list_id=shopping_list_id)


@app.route("/view/shopping-lists", methods=['GET', 'POST'])
def view_shopping_list():

    create_application_session_keys()

    form = DeleteShoppingListForm()
    form_item = ShoppingListItemForm()
    form_delete = DeleteShoppingListItemForm()

    # if the user is not signed in, redirect and notify them
    if guest_users_redirect():
        return redirect('/login')

    return render_template("shopping-list/view.html",
                           title='View Shopping Lists',
                           items=session["shopping-lists"],
                           items_of_list=session["shopping-list-items"],
                           form=form,
                           form_item=form_item,
                           form_delete=form_delete,
                           user=session["logged_in"]["id"])


@app.route("/delete/shopping-list", methods=['POST'])
def delete_shopping_list():

    form = DeleteShoppingListForm()
    create_application_session_keys()

    # if the user is not signed in, redirect and notify them
    if guest_users_redirect():
        return redirect('/login')

    if form.validate_on_submit():
        del session["shopping-lists"][form.id.data]
        flash({"message": 'Delete for item is successful!'})
        return redirect('/view/shopping-lists')

    return redirect('/view/shopping-lists')




# shopping list items crud routes
@app.route("/create/shopping-list/item", methods=['GET', 'POST'])
def create_shopping_list_item():

    create_application_session_keys()

    # if the user is not signed in, redirect and notify them
    if guest_users_redirect():
        return redirect('/login')

    form = ShoppingListItemForm()

    if form.validate_on_submit():

        new_shopping_list_item = ShoppingListItem(form.name.data, form.shopping_list.data)
        session["shopping-list-items"][new_shopping_list_item.id] = vars(new_shopping_list_item)

        flash({"message":
                "You have successfully created a shopping list item! "
                "Select the shopping list to see it"})

        return redirect('/view/shopping-lists')

    return render_template("shopping-list-item/create.html",
                           title='View Shopping List Items',
                           form=form)


@app.route("/update/shopping-list/item/<item_id>", methods=['GET', 'POST'])
def update_shopping_list_item(item_id):

    create_application_session_keys()

    # if the user is not signed in, redirect and notify them
    if guest_users_redirect():
        return redirect('/login')

    form = ShoppingListItemForm()

    if item_id not in session["shopping-list-items"]:
        flash({"message":'The item you want to update, does not exist!'})
        return redirect('/view/shopping-lists')

    if form.validate_on_submit():
        session["shopping-list-items"][item_id]["name"] = form.name.data

        flash({"message":'Update Successful!'})
        return redirect('/view/shopping-lists')

    return render_template("shopping-list-item/update.html",
                           title='Update Shopping List item',
                           form=form,
                           name=session["shopping-list-items"][item_id]["name"],
                           shopping_list_id=item_id)


@app.route("/view/shopping_list/items", methods=['GET', 'POST'])
def view_shopping_list_item(shopping_list):

    create_application_session_keys()

    # if the user is not signed in, redirect and notify them
    if guest_users_redirect():
        return redirect('/login')

    return render_template("shopping-list-item/view.html",
                           title='View Shopping List Items')


@app.route("/delete/shopping-list-item", methods=['POST'])
def delete_shopping_list_item():

    form = DeleteShoppingListItemForm()
    create_application_session_keys()

    # if the user is not signed in, redirect and notify them
    if guest_users_redirect():
        return redirect('/login')

    if form.validate_on_submit():
        del session["shopping-list-items"][form.id.data]
        flash({"message": 'Delete of a shopping list item is successful!'})
        return redirect('/view/shopping-lists')

return redirect('/view/shopping-lists')




if __name__ == "__main__":
	app.run()
