from cal import app, db, Event, User

if __name__ == "__main__":
    app.run(debug=True, host=app.config["HOST"])
