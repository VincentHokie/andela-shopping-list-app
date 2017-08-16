__author__ = 'MacUser'

from flask_wtf import Form
from wtforms import PasswordField, StringField, BooleanField, TextAreaField, DateField
from wtforms.validators import DataRequired


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class SignUpForm(Form):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    password2 = PasswordField('password2', validators=[DataRequired()])


class ShoppingListForm(Form):
    name = StringField('name', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])

class DeleteShoppingListForm(Form):
    id = StringField('id', validators=[DataRequired()])

class ShoppingListItemForm(Form):
    name = StringField('username', validators=[DataRequired()])
    date = DateField('password', validators=[DataRequired()])
