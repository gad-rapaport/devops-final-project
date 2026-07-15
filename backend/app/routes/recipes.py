from flask import Blueprint, jsonify, request
from app import db
from app.models import Recipe
from app.services.gemini_service import generate_recipe, suggest_variations

bp = Blueprint("recipes", __name__)


@bp.route("/recipes", methods=["GET"])
def list_recipes():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    cuisine = request.args.get("cuisine", None)

    query = Recipe.query.order_by(Recipe.created_at.desc())
    if cuisine:
        query = query.filter(Recipe.cuisine_type.ilike(f"%{cuisine}%"))

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        "recipes": [r.to_dict() for r in pagination.items],
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": page,
    })


@bp.route("/recipes/<int:recipe_id>", methods=["GET"])
def get_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return jsonify(recipe.to_dict())


@bp.route("/recipes/generate", methods=["POST"])
def generate():
    data = request.get_json()
    if not data or "ingredients" not in data:
        return jsonify({"error": "ingredients list is required"}), 400

    ingredients = data["ingredients"]
    if not isinstance(ingredients, list) or len(ingredients) == 0:
        return jsonify({"error": "ingredients must be a non-empty list"}), 400

    preferences = data.get("preferences", "")

    try:
        recipe_data = generate_recipe(ingredients, preferences)
    except Exception as e:
        return jsonify({"error": f"AI generation failed: {str(e)}"}), 500

    return jsonify({"generated": recipe_data}), 200


@bp.route("/recipes", methods=["POST"])
def save_recipe():
    data = request.get_json()
    required = ["title", "ingredients", "instructions"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"'{field}' is required"}), 400

    recipe = Recipe(
        title=data["title"],
        ingredients=data["ingredients"],
        instructions=data["instructions"],
        nutritional_info=data.get("nutritional_info"),
        cuisine_type=data.get("cuisine_type"),
        prep_time_minutes=data.get("prep_time_minutes"),
        rating=data.get("rating", 0.0),
    )
    db.session.add(recipe)
    db.session.commit()
    return jsonify(recipe.to_dict()), 201


@bp.route("/recipes/<int:recipe_id>", methods=["PUT"])
def update_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    data = request.get_json()

    for field in ["title", "ingredients", "instructions", "nutritional_info",
                  "cuisine_type", "prep_time_minutes", "rating"]:
        if field in data:
            setattr(recipe, field, data[field])

    db.session.commit()
    return jsonify(recipe.to_dict())


@bp.route("/recipes/<int:recipe_id>", methods=["DELETE"])
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    return jsonify({"message": "Recipe deleted"}), 200


@bp.route("/recipes/<int:recipe_id>/variations", methods=["GET"])
def get_variations(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    try:
        variations = suggest_variations(recipe.title, recipe.ingredients)
    except Exception as e:
        return jsonify({"error": f"AI variation failed: {str(e)}"}), 500
    return jsonify({"variations": variations})
