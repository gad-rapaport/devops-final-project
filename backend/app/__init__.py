import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from prometheus_flask_exporter import PrometheusMetrics

db = SQLAlchemy()
migrate = Migrate()
metrics = PrometheusMetrics.for_app_factory()


def create_app(config=None):
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://smartrecipe:smartrecipe@db:3306/smartrecipe",
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")

    if config:
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)
    metrics.init_app(app)
    CORS(app)

    from app.routes.recipes import bp as recipes_bp
    from app.routes.health import bp as health_bp

    app.register_blueprint(recipes_bp, url_prefix="/api")
    app.register_blueprint(health_bp)

    return app
