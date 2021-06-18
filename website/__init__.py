from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_Name = 'sqlite:///databese.db'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'sdfkeu3-rghhuie4u32'
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_Name
    db.init_app(app) # initial the database --> then go to models.py to create models that needs to be stored inside the db.

    #register blueprints
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note
    create_db(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


    return app



def create_db(app):
    if not path.exists('website/' + DB_Name):
        db.create_all(app=app)
        print("db is created")
