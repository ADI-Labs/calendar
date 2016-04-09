import yaml

from cal import app, db, User
from scrapers import scrapers

with app.app_context():
    # It is important to call this before creating tables
    db.configure_mappers()

    # Create the tables
    db.create_all()

    # Populate the user database
    with open('cal/groups.yml') as fin:
        users = yaml.load(fin)
    for username, ids in users.items():
        if User.query.filter_by(name=username).first() is None:
            new_user = User(name=username)
            new_user.fb_id = ids.get('fb', None)
            db.session.add(new_user)

    db.session.commit()

    for scraper in scrapers:
        scraper()
