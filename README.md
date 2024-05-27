# Recipe Integration with uAgents

Welcome to the Recipe Integration project using uAgents! This project leverages Fetch.ai's uAgents to provide detailed information about recipes, including nutrition, ingredients, instructions, and cost breakdown. The frontend is a React application that interacts with the uAgents backend to display this information to users.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [uAgents Endpoints](#uagents-endpoints)
- [Running the React App](#running-the-react-app)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Nutrition Information**: Get detailed nutritional content of any recipe.
- **Ingredients List**: View a comprehensive list of ingredients required for the recipe.
- **Cooking Instructions**: Access step-by-step instructions to prepare the dish.
- **Cost Breakdown**: Understand the cost associated with each ingredient and the total recipe.

## Installation

### Backend (uAgents)

1. **Clone the repository**:
    ```bash
    git clone https://github.com/abhifetch/your-repo-name.git
    cd your-repo-name
    ```

2. **Set up a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the uAgents backend**:
    ```bash
    python main.py
    ```

### Frontend (React)

1. **Navigate to the frontend directory**:
    ```bash
    cd frontend
    ```

2. **Install dependencies**:
    ```bash
    npm install
    ```

3. **Start the React app**:
    ```bash
    npm start
    ```

## Usage

1. **Ensure the uAgents backend is running**:
    ```bash
    python main.py
    ```

2. **Ensure the React frontend is running**:
    ```bash
    npm start
    ```

3. **Access the application**:
    Open your browser and navigate to `http://localhost:3000`.

## uAgents Endpoints

The uAgents handle specific types of requests related to recipes. Here are the main agents and their functionalities:

- **Nutrition Agent**: Handles requests for nutritional information.
- **Ingredients Agent**: Handles requests for ingredients.
- **Instructions Agent**: Handles requests for cooking instructions.
- **Cost Agent**: Handles requests for cost breakdown.

### Example Queries

- **Nutrition Information**: 
    ```
    GET /api/nutrition/<recipe_name>
    ```
    Response example:
    ```json
    {
        "calories": "200 kcal",
        "protein": "10 g",
        "fat": "5 g"
    }
    ```

- **Ingredients**:
    ```
    GET /api/ingredients/<recipe_name>
    ```
    Response example:
    ```json
    {
        "ingredient1": "200 g",
        "ingredient2": "100 ml"
    }
    ```

- **Instructions**:
    ```
    GET /api/instructions/<recipe_name>
    ```
    Response example:
    ```json
    [
        "Step 1: Preheat the oven.",
        "Step 2: Mix ingredients."
    ]
    ```

- **Cost Breakdown**:
    ```
    GET /api/cost/<recipe_name>
    ```
    Response example:
    ```json
    {
        "ingredient1": "$2.00",
        "ingredient2": "$1.50",
        "totalCost": "$3.50",
        "totalCostPerServing": "$1.75"
    }
    ```

## Running the React App

1. **Navigate to the frontend directory**:
    ```bash
    cd frontend
    ```

2. **Install dependencies**:
    ```bash
    npm install
    ```

3. **Start the React app**:
    ```bash
    npm start
    ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
