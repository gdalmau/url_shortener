from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api
import os

SHORTCODE_LENGHT = 6

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
sqlite_uri = 'sqlite:////' + os.path.join(basedir, 'db/sqlite.db')
config = {
    'SQLALCHEMY_DATABASE_URI': sqlite_uri,
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
}
app.config.update(config)

api = Api(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)


def configure_api(app):
    from api import RESOURCES
    for resource in RESOURCES:
        api.add_resource(*resource)


def configure_db(database):
    import models
    database.create_all()
