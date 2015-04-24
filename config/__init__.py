"""
Collects settings from the environment and adds them to the app configuration.

Flask specific settings will be set here and we can store additional settings
in the config object as well.
"""


from os import environ, pardir
from os.path import join, abspath, dirname
from sys import exit

try:
    # flask settings
    HOST = environ['HOST']
    PORT = environ['PORT']
    SECRET_KEY = environ['SECRET_KEY']
    DEBUG = environ['DEBUG'] == 'TRUE'
    TESTING = environ['TESTING'] == 'TRUE'
    FACEBOOK_ACCESS_TOKEN = environ['FACEBOOK_ACCESS_TOKEN']

    BASEDIR = abspath(join(dirname(__file__), pardir))

    if not TESTING:
        SQLALCHEMY_DATABASE_URI = "sqlite:///" + join(BASEDIR, "events.db")
    else:
        SQLALCHEMY_DATABASE_URI = "sqlite://"   # in memory database
    CELERY_BROKER_URL = 'sqlalchemy+' + SQLALCHEMY_DATABASE_URI
    LOGFILE = join(BASEDIR, "logs/applog.log")

except KeyError as e:
    """ Throw an error if a setting is missing """
    exit("Some of your settings aren't in the environment."
         "You probably need to run:"
         "\n\tsource config/<your settings file>\n")
