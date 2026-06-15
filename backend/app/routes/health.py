from flask import Blueprint, jsonify
from app import db
from sqlalchemy import text

bp = Blueprint("health", __name__)


@bp.route("/health")
def health_check():
    try:
        db.session.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return jsonify({"status": "ok", "database": db_status}), 200


@bp.route("/")
def index():
    return jsonify({"service": "SmartRecipe AI API", "version": "1.0.0"}), 200
