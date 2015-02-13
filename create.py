from cal import app
from cal.schema import db


with app.app_context():
    db.create_all()
