# Import Required libraries
import requests
import os
from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
 
# Define Request, Response and Error Models
class InstructionRequest(Model):
    recipe_name: str

class InstructuionResponse(Model):
    instructions : str

class ErrorResponse(Model):
    error : str

# Import api key from environment
NUTRITION_API_KEY = os.getenv('NUTRITION_API_KEY')

# Define function to check detailed instructions for recipes using API
async def instructions_analysis(recipe_name):
    headers = {
        "X-RapidAPI-Key": NUTRITION_API_KEY,
        "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }

    url_recipe = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/search"
    querystring = {"query": recipe_name}

    response_recipe = requests.get(url_recipe, headers=headers, params=querystring)
    data_recipe = response_recipe.json()
    recipe_id = data_recipe['results'][0]['id']

    url_instructions = f"https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{recipe_id}/analyzedInstructions"
    steps_list = []

    response_instructions = requests.get(url_instructions, headers=headers)
    data_instructions = response_instructions.json()

    for recipe in data_instructions:
        for step in recipe["steps"]:
            steps_list.append(f"{step['step']}")

    return steps_list
 
# Define ingredeint Agent
InstructionAgent = Agent(
    name="InstructionAgent",
    port=8002,
    seed="Instruction Agent secret phrase",
    endpoint=["http://127.0.0.1:8002/submit"],
)
 
# Registering agent on Almananc and funding it.
fund_agent_if_low(InstructionAgent.wallet.address())
 
# On agent startup printing address
@InstructionAgent.on_event('startup')
async def agent_details(ctx: Context):
    ctx.logger.info(f'Search Agent Address is {InstructionAgent.address}')

# On_query handler to ingredeint details of a recipe
@InstructionAgent.on_query(model=InstructionRequest, replies={InstructuionResponse})
async def query_handler(ctx: Context, sender: str, msg: InstructionRequest):
    try:
        ctx.logger.info(f'Fetching nutritions details for recipe : {msg.recipe_name}')
        instructions = await instructions_analysis(msg.recipe_name)
        ctx.logger.info(instructions)
        await ctx.send(sender, InstructuionResponse(instructions=str(instructions)))

    except Exception as e:
        error_message = f"Error fetching job details: {str(e)}"
        ctx.logger.error(error_message)
        # Ensure the error message is sent as a string
        await ctx.send(sender, ErrorResponse(response=str(error_message)))

# Starting agent
if __name__ == "__main__":
    InstructionAgent.run() 