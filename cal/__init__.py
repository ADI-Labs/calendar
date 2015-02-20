from os import path

from flask import Flask, g, jsonify, render_template, json, request
from schema import db, Event

app = Flask(__name__)
app.config.from_object('config')

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
    events = Event.query.all()
    return render_template('index.html', events=events)


@app.route('/update')
def update():
    update_fb_events()
    return jsonify({"success": True})


@app.route('/events')
def events():
	events = Event.query.order_by(Event.start).all()
	return render_template('index.html', events=events)
