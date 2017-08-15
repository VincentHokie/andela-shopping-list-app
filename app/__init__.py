__author__ = 'MacUser'

# import a the class that will allow us initialize a flask application
from flask import Flask

# initialize the flask application
app = Flask(__name__)

# instruct the django application to use the config file to collect settings
app.config.from_object('config')


# when app is initialized, get our routes and functions to process requests
from . import views



