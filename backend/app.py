from flask import Flask, jsonify, request  # Import Flask and its necessary modules
from flask_cors import CORS  # Import CORS for handling Cross-Origin Resource Sharing
from uagents.query import query  # Import the query function from uagents
from uagents import Model  # Import Model from uagents for defining request and response models
import json  # Import json for handling JSON data

# Initialize Flask application
app = Flask(__name__)
CORS(app)  # Enables CORS for all domains on all routes

# Define the addresses for different agents handling nutrition, ingredients, instructions, and cost queries
nutritions_address = 'agent1qfw5c3rdvpzmmt52ekwt6dqwl5ddv3lqdz35gp3k54wlcw9hcud77mxsgqx'
ingredients_address = 'agent1qdfw2xc4r87fhfflmc9rgex7h6qypq5zl9sfp9l3gxyv0v4rcw0ngqv4p7h'
instructions_address = 'agent1qvdr0cnsxlc9f8ds02plddqjrewt2t9m3kv4nrry792pe5kj97xs55t2rfq'
cost_address = 'agent1qt8klq98fxaa74jryfx88hqyvreeamk4d54aseq5k0xgzcnh2usz793fwpd'

# Define Request and Response Models for Nutrition
class NutritionRequest(Model):
    recipe_name: str

class NutritionResponse(Model):
    nutritions: str

# Define Request and Response Models for Ingredients
class IngredientRequest(Model):
    recipe_name: str

class IngredientResponse(Model):
    ingredients: str

# Define Request and Response Models for Instructions
class InstructionRequest(Model):
    recipe_name: str

class InstructionResponse(Model):
    instructions: str

# Define Request and Response Models for Cost Breakdown
class CostRequest(Model):
    recipe_name: str

class CostResponse(Model):
    breakdown: str

# Define Error Response Models for Cost Breakdown
class ErrorResponse(Model):
    error : str

# Define the home route
@app.route('/')
def home():
    return "Welcome to the Recipe API!"

# Define the route for getting nutrition information
@app.route('/api/nutrition/<string:recipe_name>', methods=['GET'])
async def get_nutrition(recipe_name):
    response = await query(destination=nutritions_address, message=NutritionRequest(recipe_name=recipe_name), timeout=15.0)
    data = json.loads(response.decode_payload())
    data["nutritions"] = data["nutritions"][1:-1]  # Clean up the response
    nutrient_list = data["nutritions"].split(',')
    nutrition_details = nutrient_list
    nutrition_dict = {}
    for item in nutrition_details:
        item = item[1:-1]
        name, value = item.split(": ")
        nutrition_dict[name.strip("' ")] = value
    print(nutrition_dict)
    return jsonify(nutrition_dict)

# Define the route for getting ingredients
@app.route('/api/ingredients/<string:recipe_name>', methods=['GET'])
async def get_ingredients(recipe_name):
    response = await query(destination=ingredients_address, message=IngredientRequest(recipe_name=recipe_name), timeout=15.0)
    data = json.loads(response.decode_payload())
    data["ingredients"] = data["ingredients"][1:-1]  # Clean up the response
    ingredients_list = data["ingredients"].split(',')
    ingredients_details = ingredients_list
    ingredients_dict = {}
    for item in ingredients_details:
        name, value = item.split(": ")
        ingredients_dict[name.strip("' ")] = value.strip("'")
    print(ingredients_dict)
    return jsonify(ingredients_dict)

# Define the route for getting instructions
@app.route('/api/instructions/<string:recipe_name>', methods=['GET'])
async def get_instructions(recipe_name):
    response = await query(destination=instructions_address, message=InstructionRequest(recipe_name=recipe_name), timeout=15.0)
    data = json.loads(response.decode_payload())
    raw_instruction = data['instructions'][1:-1].strip("' ")  # Clean up the response
    instructions_list = raw_instruction.split("', '")  # Split the instructions into a list
    instructions_list = [instruction.strip().strip("'") for instruction in instructions_list]  # Further clean each instruction
    print(instructions_list)
    return jsonify(instructions_list)

# Define the route for getting cost breakdown
@app.route('/api/cost/<string:recipe_name>', methods=['GET'])
async def get_cost(recipe_name):
    response = await query(destination=cost_address, message=CostRequest(recipe_name=recipe_name), timeout=15.0)
    data = json.loads(response.decode_payload())
    raw_breakdown = data['breakdown'][1:-1].strip("' ")  # Clean up the response
    breakdown_list = raw_breakdown.split("', '")  # Split the breakdown into a list
    cost_dict = {}
    for item in breakdown_list:
        name, value = item.split(": ")
        cost_dict[name.strip("' ")] = value.strip("'")
    print(cost_dict)
    return jsonify(cost_dict)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
