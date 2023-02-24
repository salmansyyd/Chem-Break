from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config=None):
    app = Flask(__name__)
    if config:
        app.config.from_object(config)

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        from . models import User, Post
        db.create_all()

    # test route
    @app.route('/')
    def index():
        return 'Hello World'

    # register blueprints
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
