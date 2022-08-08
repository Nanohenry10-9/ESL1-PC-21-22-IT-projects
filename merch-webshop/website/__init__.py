from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)

    """
    
    ================================================================================

    NOTE: replace the secret key below with something secure (and hopefully random)!
          If you fail to do this, client sessions' security cannot be guaranteed.

    ================================================================================

    """

    app.config['SECRET_KEY'] = '[password here, please!]'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views

    app.register_blueprint(views, url_prefix='/')


    create_database(app)

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
