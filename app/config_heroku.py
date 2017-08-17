import os
basedir = os.path.abspath(os.path.dirname(__file__))


# make wft extension consider cross-site request forgery
WTF_CSRF_ENABLED = True

# required when the above config is enabled, this will be used to
# generate a scrf token..should be a string that cant be easily
# guessed in production
SECRET_KEY = 'youll-never-know-what-it-is-coz-its-secret'
