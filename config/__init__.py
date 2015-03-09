"""
Collects settings from the environment and adds them to the app configuration.

Flask specific settings will be set here and we can store additional settings
in the config object as well.
"""


from os import environ, path, pardir
from sys import exit


try:
    # flask settings
    HOST = environ['HOST']
    PORT = environ['PORT']
    SECRET_KEY = environ['SECRET_KEY']
    DEBUG = True if environ['DEBUG'] == 'TRUE' else False
    FACEBOOK_ACCESS_TOKEN = environ['FACEBOOK_ACCESS_TOKEN']

    BASEDIR = path.abspath(path.join(path.dirname(__file__), pardir))
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + path.join(BASEDIR, "events.db")
    CELERY_BROKER_URL = 'sqlalchemy+' + SQLALCHEMY_DATABASE_URI
    LOGFILE = "logs/test.log"

except KeyError as e:
    """ Throw an error if a setting is missing """
    print "ERR MSG: {}".format(e.message)
    print ("Some of your settings aren't in the environment."
           "You probably need to run:"
           "\n\n\tsource config/<your settings file>")
    exit(1)
