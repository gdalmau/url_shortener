from config import app, db, configure_api, configure_db


if __name__ == '__main__':
    configure_api(app)
    configure_db(db)

    app.run(debug=False)
