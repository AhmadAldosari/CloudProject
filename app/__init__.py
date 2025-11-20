"""Application factory for the Flask project."""
from flask import Flask

from .config import get_config
from .extensions.database import db
from .routes import bp as dashboard_bp


def create_app(config_object=None) -> Flask:
    """Application factory used by AWS Elastic Beanstalk."""
    app = Flask(__name__)
    config_instance = config_object or get_config()
    app.config.from_object(config_instance)

    register_extensions(app)
    register_blueprints(app)
    register_shellcontext(app)

    with app.app_context():
        db.create_all()

    return app


def register_extensions(app: Flask) -> None:
    """Attach Flask extensions to the app instance."""
    db.init_app(app)


def register_blueprints(app: Flask) -> None:
    """Register route blueprints."""
    app.register_blueprint(dashboard_bp)


def register_shellcontext(app: Flask) -> None:
    """Expose objects in the interactive shell (``eb ssh`` or ``flask shell``)."""
    from .models import InventoryItem, User

    @app.shell_context_processor
    def _make_context():
        return {"db": db, "User": User, "InventoryItem": InventoryItem}
