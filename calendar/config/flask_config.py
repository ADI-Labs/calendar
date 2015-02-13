
"""
Collects settings from the environment and adds them to the app configuration.

Flask specific settings will be set here and we can store additional settings
in the config object as well.
"""


from os import environ
from sys import exit


try:
    # flask settings
    HOST = environ['HOST']
    PORT = environ['PORT']
    SECRET_KEY = environ['SECRET_KEY']
    DEBUG = True if environ['DEBUG'] == 'TRUE' else False

except KeyError as e:
    """ Throw an error if a setting is missing """
    print "ERR MSG: {}".format(e.message)
    print ("Some of your settings aren't in the environment."
           "You probably need to run:"
           "\n\n\tsource config/<your settings file>")
    exit(1)
