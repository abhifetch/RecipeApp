# Import Required libraries
import requests
import os
from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
 
# Define Request, Response and Error Models
class IngredeintRequest(Model):
    recipe_name: str

class IngredeintResponse(Model):
    ingredients : str

class ErrorResponse(Model):
    error : str

# Import api key from environment
NUTRITION_API_KEY = os.getenv('NUTRITION_API_KEY')

# Define function to check ingredients for recipes using API
async def ingredient_analysis(recipe_name):
    headers = {
        "X-RapidAPI-Key": NUTRITION_API_KEY,
        "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }

    url_recipe = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/search"
    querystring = {"query": recipe_name}

    response_recipe = requests.get(url_recipe, headers=headers, params=querystring)
    print(response_recipe)
    data_recipe = response_recipe.json()

    recipe_id = data_recipe['results'][0]['id']

    url_ingredients = f"https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{recipe_id}/ingredientWidget.json"
    ingredient_list = []

    response_ingredients = requests.get(url_ingredients, headers=headers)
    data_ingredients = response_ingredients.json()

    # For each ingredient format the string and add to list with cost
    for ingredient in data_ingredients["ingredients"]:
        name = ingredient["name"]
        amount_metric = ingredient["amount"]["metric"]
        ingredient_list.append(f"{name}: {amount_metric['value']} {amount_metric['unit']}")

    return ingredient_list
 
# Define Ingredient Agent
IngredeintAgent = Agent(
    name="IngredeintAgent",
    port=8001,
    seed="Ingredeint Agent secret phrase",
    endpoint=["http://127.0.0.1:8001/submit"],
)
 
# Registering agent on Almananc and funding it.
fund_agent_if_low(IngredeintAgent.wallet.address())
 
# On agent startup printing address
@IngredeintAgent.on_event('startup')
async def agent_details(ctx: Context):
    ctx.logger.info(f'Search Agent Address is {IngredeintAgent.address}')

# On_query handler to get ingredeint details
@IngredeintAgent.on_query(model=IngredeintRequest, replies={IngredeintResponse})
async def query_handler(ctx: Context, sender: str, msg: IngredeintRequest):
    try:
        ctx.logger.info(f'Fetching nutritions details for recipe : {msg.recipe_name}')
        ingredients = await ingredient_analysis(msg.recipe_name)
        ctx.logger.info(ingredients)
        await ctx.send(sender, IngredeintResponse(ingredients=str(ingredients)))

    except Exception as e:
        error_message = f"Error fetching job details: {str(e)}"
        ctx.logger.error(error_message)
        # Ensure the error message is sent as a string
        await ctx.send(sender, ErrorResponse(response=str(error_message)))

# Starting agent
if __name__ == "__main__":
    IngredeintAgent.run() 