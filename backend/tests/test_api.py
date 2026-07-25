"""Tests for the REST API endpoints."""
import json
import pytest


def test_health_endpoint(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] == "ok"


def test_index_endpoint(client):
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["service"] == "SmartRecipe AI API"


def test_list_recipes_empty(client):
    resp = client.get("/api/recipes")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "recipes" in data
    assert isinstance(data["recipes"], list)


def test_save_recipe(client):
    payload = {
        "title": "API Test Recipe",
        "ingredients": "tomato, mozzarella, basil",
        "instructions": "Layer ingredients. Drizzle olive oil.",
        "cuisine_type": "Italian",
        "prep_time_minutes": 10,
    }
    resp = client.post("/api/recipes", json=payload)
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["title"] == "API Test Recipe"
    assert data["id"] is not None
    return data["id"]


def test_get_recipe(client):
    payload = {
        "title": "Get Test Recipe",
        "ingredients": "garlic, olive oil",
        "instructions": "Fry garlic in oil.",
    }
    create_resp = client.post("/api/recipes", json=payload)
    assert create_resp.status_code == 201
    recipe_id = create_resp.get_json()["id"]

    get_resp = client.get(f"/api/recipes/{recipe_id}")
    assert get_resp.status_code == 200
    assert get_resp.get_json()["id"] == recipe_id


def test_update_recipe(client):
    payload = {
        "title": "Update Me",
        "ingredients": "rice",
        "instructions": "Boil rice.",
    }
    create_resp = client.post("/api/recipes", json=payload)
    recipe_id = create_resp.get_json()["id"]

    update_resp = client.put(f"/api/recipes/{recipe_id}", json={"rating": 4.0})
    assert update_resp.status_code == 200
    assert update_resp.get_json()["rating"] == 4.0


def test_delete_recipe(client):
    payload = {
        "title": "Delete Me",
        "ingredients": "water",
        "instructions": "Boil water.",
    }
    create_resp = client.post("/api/recipes", json=payload)
    recipe_id = create_resp.get_json()["id"]

    del_resp = client.delete(f"/api/recipes/{recipe_id}")
    assert del_resp.status_code == 200

    get_resp = client.get(f"/api/recipes/{recipe_id}")
    assert get_resp.status_code == 404


def test_save_recipe_missing_field(client):
    resp = client.post("/api/recipes", json={"title": "Incomplete"})
    assert resp.status_code == 400


def test_generate_recipe_no_key(client, monkeypatch):
    def fake_generate_recipe(ingredients, preferences=""):
        raise ValueError("GEMINI_API_KEY environment variable is not set")

    monkeypatch.setattr("app.routes.recipes.generate_recipe", fake_generate_recipe)

    resp = client.post("/api/recipes/generate", json={"ingredients": ["chicken"]})
    assert resp.status_code == 500


def test_generate_recipe_missing_ingredients(client):
    resp = client.post("/api/recipes/generate", json={})
    assert resp.status_code == 400
