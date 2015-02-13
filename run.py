from flask import Flask, render_template, request, jsonify
from schema import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///events.db"
db.init_app(app)

@app.route("/", methods=["GET", "POST"])
def index():
    return "It runs!"

if __name__ == "__main__":
    app.run(debug=True)
