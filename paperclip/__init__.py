from flask import Flask

from .extensions import db, login_manager
from .routes.main import main
from .routes.auth import auth
from .commands import (
    create_tables,
    create_currencies,
    create_payments,
    create_categories,
    create_invoices,
    test_query,
)
from .models import User


def create_app(config_file="settings.py"):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    app.register_blueprint(main)
    app.register_blueprint(auth)

    app.cli.add_command(create_tables)
    app.cli.add_command(create_currencies)
    app.cli.add_command(create_payments)
    app.cli.add_command(create_categories)
    app.cli.add_command(create_invoices)
    app.cli.add_command(test_query)

    return app
