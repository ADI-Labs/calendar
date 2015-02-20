from flask import Flask, render_template
from schema import db, Event, User

app = Flask(__name__)
app.config.from_object('config.flask_config')

db.init_app(app)


@app.before_request
def before_request():
    """ Do something before every request """
    return


@app.after_request
def after_request(resp):
    """ Do something after every request """
    return resp


@app.errorhandler(404)
def page_not_found(e):
    return "Page not found"


@app.route('/')
def home():
    events = Event.query.order_by(Event.start).all()
    return render_template('index.html', events=events)
