from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from py_bife.config import Config

db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from py_bife.application.user_api import user_api_bp
    from py_bife.application.message_api import message_api_bp

    app.register_blueprint(user_api_bp, url_prefix="/user")
    app.register_blueprint(message_api_bp, url_prefix="/message")

    return app
