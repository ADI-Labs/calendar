import logging

from config import LOGFILE
from cal import app

if __name__ == "__main__":
    handler = logging.FileHandler(LOGFILE)
    format = '%(asctime)s %(levelname)s: %(message)s ' \
             '[in %(pathname)s:%(lineno)d]'
    handler.setFormatter(logging.Formatter(format))

    if app.config['DEBUG']:
        handler.setLevel(logging.DEBUG)
    else:
        handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    app.run(debug=app.config['DEBUG'], host=app.config["HOST"])
