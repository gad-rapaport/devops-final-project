"""Tests for database insertion and retrieval via the live MySQL container."""
import pytest
from app.models import Recipe
from app import db as _db


def test_insert_recipe(db, app):
    with app.app_context():
        recipe = Recipe(
            title="Test Pasta",
            ingredients="pasta, tomato, basil",
            instructions="Boil pasta. Add sauce.",
            cuisine_type="Italian",
            prep_time_minutes=20,
            rating=4.5,
        )
        _db.session.add(recipe)
        _db.session.commit()
        assert recipe.id is not None


def test_retrieve_recipe(db, app):
    with app.app_context():
        recipe = Recipe(
            title="Retrieve Test",
            ingredients="eggs, butter",
            instructions="Fry eggs in butter.",
            cuisine_type="French",
            prep_time_minutes=5,
        )
        _db.session.add(recipe)
        _db.session.commit()

        fetched = Recipe.query.filter_by(title="Retrieve Test").first()
        assert fetched is not None
        assert fetched.ingredients == "eggs, butter"
        assert fetched.cuisine_type == "French"


def test_update_recipe(db, app):
    with app.app_context():
        recipe = Recipe(
            title="Update Test",
            ingredients="chicken",
            instructions="Grill chicken.",
        )
        _db.session.add(recipe)
        _db.session.commit()

        recipe.rating = 5.0
        _db.session.commit()

        updated = Recipe.query.get(recipe.id)
        assert updated.rating == 5.0


def test_delete_recipe(db, app):
    with app.app_context():
        recipe = Recipe(
            title="Delete Test",
            ingredients="bread",
            instructions="Toast bread.",
        )
        _db.session.add(recipe)
        _db.session.commit()
        rid = recipe.id

        _db.session.delete(recipe)
        _db.session.commit()

        assert Recipe.query.get(rid) is None


def test_recipe_to_dict(db, app):
    with app.app_context():
        recipe = Recipe(
            title="Dict Test",
            ingredients="sugar, flour",
            instructions="Mix and bake.",
            nutritional_info="200 kcal per serving",
        )
        _db.session.add(recipe)
        _db.session.commit()

        d = recipe.to_dict()
        assert d["title"] == "Dict Test"
        assert d["nutritional_info"] == "200 kcal per serving"
        assert "created_at" in d
