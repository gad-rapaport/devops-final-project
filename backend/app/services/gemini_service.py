import os
import json
import google.generativeai as genai


def _get_model():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.5-flash")


def generate_recipe(ingredients: list[str], preferences: str = "") -> dict:
    model = _get_model()

    ingredients_str = ", ".join(ingredients)
    pref_text = f"Dietary preferences/restrictions: {preferences}." if preferences else ""

    prompt = f"""You are a professional chef and nutritionist. Generate a detailed recipe using primarily these ingredients: {ingredients_str}.
{pref_text}

Respond ONLY with a valid JSON object (no markdown, no extra text) in this exact structure:
{{
  "title": "Recipe Name",
  "ingredients": "Full ingredient list with quantities, one per line",
  "instructions": "Step-by-step cooking instructions, numbered",
  "nutritional_info": "Approximate nutritional info per serving (calories, protein, carbs, fat)",
  "cuisine_type": "e.g. Italian, Mediterranean, Asian",
  "prep_time_minutes": 30
}}"""

    response = model.generate_content(prompt)
    text = response.text.strip()

    if text.startswith("```"):
        lines = text.split("\n")
        text = "\n".join(lines[1:-1]) if lines[-1].strip() == "```" else "\n".join(lines[1:])

    return json.loads(text)


def suggest_variations(recipe_title: str, original_ingredients: str) -> str:
    model = _get_model()

    prompt = f"""Given the recipe "{recipe_title}" with ingredients: {original_ingredients}

Suggest 3 creative variations or substitutions to make this recipe healthier, more budget-friendly, or suitable for different dietary needs.
Be concise — 2-3 sentences per variation."""

    response = model.generate_content(prompt)
    return response.text.strip()
