from cal import app
from cal.schema import db, User
from cal.fb import update_fb_events
import yaml

with app.app_context():
    db.create_all()
    with open('cal/groups.yml') as fin:
      users = yaml.load(fin)
    for username, ids in users.iteritems():
      if User.query.filter_by(name=username).first() is None:
        new_user = User(name=username)
        if 'fb' in ids:
          new_user.fb_id = ids['fb']
        db.session.add(new_user)
        db.session.commit()
    update_fb_events()
