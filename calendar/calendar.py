from flask import Flask, g, jsonify, render_template, json, request
app = Flask(__name__)

# do import early to check that all env variables are present
app.config.from_object('config.flask_config')

# library imports here

@app.before_request
def before_request():
    """ Do something before every request """
    return


@app.after_request
def after_request(resp):
    """ Do something after every request """
    return


@app.errorhandler(404)
def page_not_found(e):
    return jsonify(error="Page not found")


@app.errorhandler(500)
@app.errorhandler(Exception)
def internal_error(e):
    return jsonify(error="Something went wrong.")


@app.route('/')
def home():
    return jsonify(message="Hello world!")


if __name__ == '__main__':
    app.run(host=app.config['HOST'])
