from cal import app
import logging
from logging import FileHandler, Formatter

if __name__ == "__main__":
    handler = FileHandler("cal/logs/test.log")
    format = '%(asctime)s %(levelname)s: %(message)s ' \
      '[in %(pathname)s:%(lineno)d]'
    handler.setFormatter(Formatter(format))

    if app.debug:
      handler.setLevel(logging.DEBUG)
    else:
      handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(debug=True, host=app.config["HOST"])
