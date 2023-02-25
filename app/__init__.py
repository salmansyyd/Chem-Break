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

    with app.app_context():
        from app.models import User, Breakage, Student, Apparatus, Bank, Record
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # test user
    def add_user(username, password):
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

    with app.app_context():
        add_user("salman", "salman")

    # test route
    @app.route('/')
    def index():
        return 'Hello World'

    # register blueprints
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # add_user("salman", "salman")

    return app
