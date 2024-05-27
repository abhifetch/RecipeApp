# Import Required libraries
import requests
import os
from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
 
# Define Request, Response and Error Models
class NutritionRequest(Model):
    recipe_name: str

class NutritionResponse(Model):
    nutritions : str

class ErrorResponse(Model):
    error : str

# Import api key from environment
NUTRITION_API_KEY = os.getenv('NUTRITION_API_KEY')

# Define function to check nutritions for recipes using API
async def nutrition_analysis(recipe_name):
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

    url_nutrients = f"https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{recipe_id}/nutritionWidget.json"
    response_nutrients = requests.get(url_nutrients, headers=headers)
    nutrients = response_nutrients.json()

    # Collecting basic nutrition facts
    nutrition_list = []

    for nutrient in nutrients["nutrients"]:
        nutrition_list.append(f"{nutrient['name']}: {nutrient['amount']}{nutrient['unit']}")

    return nutrition_list

 
# Define nutrition Agent
NutritionAgent = Agent(
    name="NutritionAgent",
    port=8000,
    seed="Nutrition Agent secret phrase",
    endpoint=["http://127.0.0.1:8000/submit"],
)
 
# Registering agent on Almananc and funding it.
fund_agent_if_low(NutritionAgent.wallet.address())
 
# On agent startup printing address
@NutritionAgent.on_event('startup')
async def agent_details(ctx: Context):
    ctx.logger.info(f'nutrition Agent Address is {NutritionAgent.address}')

# On_query handler to check nutritions
@NutritionAgent.on_query(model=NutritionRequest, replies={NutritionResponse})
async def query_handler(ctx: Context, sender: str, msg: NutritionRequest):
    try:
        ctx.logger.info(f'Fetching nutritions details for recipe : {msg.recipe_name}')
        nutritions = await nutrition_analysis(msg.recipe_name)
        ctx.logger.info(nutritions)
        ctx.logger.info(sender)
        await ctx.send(sender, NutritionResponse(nutritions=str(nutritions)))

    except Exception as e:
        error_message = f"Error fetching job details: {str(e)}"
        ctx.logger.error(error_message)
        # Ensure the error message is sent as a string
        await ctx.send(sender, ErrorResponse(response=str(error_message)))

# Starting agent     
if __name__ == "__main__":
    NutritionAgent.run() 