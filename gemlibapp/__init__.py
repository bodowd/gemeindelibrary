from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from gemlibapp.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
# redirects to the login page if user is not logged in. Use with the @login_required decorator
login_manager.login_view = 'users.login'  # login is the `function` name of the route
login_manager.login_message_category = 'info'  # info is bootstrap class for a nice blue alert
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from gemlibapp.users.routes import users  # users is the instance of the Blueprint class
    from gemlibapp.main.routes import main
    from gemlibapp.errors.handlers import errors
    from gemlibapp.booklist.routes import booklist
    from gemlibapp.reminder.routes import reminder

    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(booklist)
    app.register_blueprint(reminder)

    return app

