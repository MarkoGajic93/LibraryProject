import os

from flask import Flask

import config
from db.db_service import close_db

app_env = os.environ.get("FLASK_ENV")

def create_app(config_env = app_env):
    app = Flask(__name__)
    app.config.from_object(f"config.{config_env.capitalize()}Config")
    app.teardown_appcontext(close_db)

    from app.home import home_bp
    app.register_blueprint(home_bp, url_prefix="/")

    from app.book import book_bp
    app.register_blueprint(book_bp, url_prefix="/books")

    from app.author import author_bp
    app.register_blueprint(author_bp, url_prefix="/authors")

    return app