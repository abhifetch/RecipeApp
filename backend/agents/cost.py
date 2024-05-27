# Import Required libraries
import requests
import os
from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
 
# Define Request, Response and Error Models
class CostRequest(Model):
    recipe_name: str

class CostResponse(Model):
    breakdown : str

class ErrorResponse(Model):
    error : str

# Import api key from environment
NUTRITION_API_KEY = os.getenv('NUTRITION_API_KEY')

# Define function to check price breakdown for recipes using API
async def price_analysis(recipe_name):
    headers = {
        "X-RapidAPI-Key": NUTRITION_API_KEY,
        "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }

    url_recipe = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/search"
    querystring = {"query": recipe_name}

    response_recipe = requests.get(url_recipe, headers=headers, params=querystring)
    data_recipe = response_recipe.json()
    recipe_id = data_recipe['results'][0]['id']

    url_price = f"https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{recipe_id}/priceBreakdownWidget.json"
    ingredient_price_list = []

    response_price = requests.get(url_price, headers=headers)
    data_price = response_price.json()
    
    # For each ingredient format the string and add to list with cost
    for ingredient in data_price["ingredients"]:
        name = ingredient["name"]
        price = ingredient["price"]
        ingredient_price_list.append(f"{name}: ₹{price:.2f}")

    ingredient_price_list.append(f"totalCost: ₹{data_price['totalCost']:.2f}")
    ingredient_price_list.append(f"totalCostPerServing: ₹{data_price['totalCostPerServing']:.2f}")

    return ingredient_price_list
 
# Create Cost Agent
CostAgent = Agent(
    name="CostAgent",
    port=8003,
    seed="Cost Agent secret phrase",
    endpoint=["http://127.0.0.1:8003/submit"],
)
 
# Registering agent on Almananc and funding it.
fund_agent_if_low(CostAgent.wallet.address())
 
# On agent startup printing address
@CostAgent.on_event('startup')
async def agent_details(ctx: Context):
    ctx.logger.info(f'Search Agent Address is {CostAgent.address}')

# On_query handler to check cost
@CostAgent.on_query(model=CostRequest, replies={CostResponse})
async def query_handler(ctx: Context, sender: str, msg: CostRequest):
    try:
        ctx.logger.info(f'Fetching nutritions details for recipe : {msg.recipe_name}')
        breakdown = await price_analysis(msg.recipe_name)
        ctx.logger.info(breakdown)
        await ctx.send(sender, CostResponse(breakdown=str(breakdown)))

    except Exception as e:
        error_message = f"Error fetching job details: {str(e)}"
        ctx.logger.error(error_message)
        # Ensure the error message is sent as a string
        await ctx.send(sender, ErrorResponse(response=str(error_message)))

# Starting agent
if __name__ == "__main__":
    CostAgent.run() 