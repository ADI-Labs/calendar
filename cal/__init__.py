from flask import Flask, jsonify, render_template
import flask.ext.whooshalchemy as whooshalchemy

from schema import db, Event, User
from cal.fb import update_fb_events
from celery import Celery

def make_celery(app):
    # Create the celery app.
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

def create_app():
    # Create the Flask app.
    app = Flask(__name__)
    app.config.from_object('config')
    db.init_app(app)
    whooshalchemy.whoosh_index(app, Event)
    return app

app = create_app()
celery = make_celery(app)

# Background task
@celery.task(name="cal.fb_task")
def fb_task_test():
    print "Starting FB update"
    update_fb_events()
    print "Finished FB update"
    fb_task_test.apply_async(countdown=30)

# Unfortunate hack, you will need to hit a url once to initialize the updater.
@app.before_first_request
def intiialize():
    fb_task_test.apply_async()

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

    sunday = [event for event in events if event.start.weekday() == 0]
    monday = [event for event in events if event.start.weekday() == 1]
    tuesday = [event for event in events if event.start.weekday() == 2]
    wednesday = [event for event in events if event.start.weekday() == 3]
    thursday = [event for event in events if event.start.weekday() == 4]
    fridau = [event for event in events if event.start.weekday() == 5]
    saturday = [event for event in events if event.start.weekday() == 6]

    events = [sunday, monday, tuesday, wednesday, thursday, friday, saturday]
    return render_template('index.html', events=events)


# TO REMOVE: Manual update route
@app.route('/update')
def update():
    update_fb_events()
    return jsonify({"success": True})


@app.route('/events')
def events():
    return jsonify({"events": map(lambda x: x.to_JSON(), Event.query.all())})
