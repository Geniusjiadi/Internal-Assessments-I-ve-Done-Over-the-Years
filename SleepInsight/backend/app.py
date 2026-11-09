from __future__ import annotations

from flask import Flask, jsonify, g

from .config import Config
from .db import Database
from .routes.sleep_routes import bp as sleep_bp
from .routes.lifestyle_routes import bp as lifestyle_bp
from .routes.analytics_routes import bp as analytics_bp
from .routes.goal_routes import bp as goal_bp


def create_app(config_override: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    if config_override:
        app.config.update(config_override)

    db = Database(app.config["DATABASE_URL"])
    db.create_all()
    app.extensions["sleepinsight_db"] = db

    @app.before_request
    def open_session():
        g.db = db.SessionLocal()

    @app.teardown_request
    def close_session(exc=None):
        session = g.pop("db", None)
        if session is not None:
            if exc is None:
                try:
                    session.commit()
                except Exception:
                    session.rollback()
                    raise
            else:
                # A handled 400 (e.g. duplicate-date IntegrityError) leaves the
                # session in "pending rollback"; roll back so the next request
                # gets a clean transaction.
                session.rollback()
            session.close()

    @app.after_request
    def add_cors_headers(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        return response

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok", "service": "SleepInsight"})

    app.register_blueprint(sleep_bp)
    app.register_blueprint(lifestyle_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(goal_bp)
    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5000, debug=True)
