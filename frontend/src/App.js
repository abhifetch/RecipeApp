import React, { useState } from 'react';  // Import React and useState hook
import axios from 'axios';  // Import axios for making HTTP requests
import './App.css';  // Import the CSS file for styling

function App() {
    // Define state variables for recipe name, nutrition, ingredients, instructions, and cost
    const [recipeName, setRecipeName] = useState('');
    const [nutrition, setNutrition] = useState(null);
    const [ingredients, setIngredients] = useState(null);
    const [instructions, setInstructions] = useState(null);
    const [cost, setCost] = useState(null);

    // Function to fetch recipe details from the API
    const fetchRecipeDetails = async () => {
        try {
            // Fetch nutrition details
            console.log('Fetching nutrition...');
            const nutritionRes = await axios.get(`http://127.0.0.1:5000/api/nutrition/${recipeName}`);
            console.log('Nutrition fetched:', nutritionRes.data);
            setNutrition(nutritionRes.data);

            // Fetch ingredients details
            console.log('Fetching ingredients...');
            const ingredientsRes = await axios.get(`http://127.0.0.1:5000/api/ingredients/${recipeName}`);
            console.log('Ingredients fetched:', ingredientsRes.data);
            setIngredients(ingredientsRes.data);

            // Fetch instructions details
            console.log('Fetching instructions...');
            const instructionsRes = await axios.get(`http://127.0.0.1:5000/api/instructions/${recipeName}`);
            console.log('Instructions fetched:', instructionsRes.data);
            setInstructions(instructionsRes.data);

            // Fetch cost details
            console.log('Fetching cost...');
            const costRes = await axios.get(`http://127.0.0.1:5000/api/cost/${recipeName}`);
            console.log('Cost fetched:', costRes.data);
            setCost(costRes.data);
        } catch (error) {
            // Handle any errors during the API requests
            console.error('Error fetching recipe details:', error);
        }
    };

    return (
        <div className="App">
            <header className="App-header">
                <h1>Recipe Finder</h1>
                {/* Input field for recipe name */}
                <input
                    type="text"
                    value={recipeName}
                    onChange={(e) => setRecipeName(e.target.value)}
                    placeholder="Enter recipe name"
                />
                {/* Button to trigger fetching recipe details */}
                <button onClick={fetchRecipeDetails}>Get Recipe Details</button>
            </header>
            {/* Display recipe name if either nutrition or ingredients data is available */}
            {recipeName && (nutrition || ingredients) && (
                <section>
                    <h2>{recipeName}</h2>
                </section>
            )}
            {/* Display nutrition details if available */}
            {nutrition && (
                <section>
                    <h2>Nutrition</h2>
                    <div className="nutrition-grid">
                        {Object.entries(nutrition).map(([key, value]) => (
                            <div className="nutrition-item" key={key}>
                                <strong>{key}</strong> {value}
                            </div>
                        ))}
                    </div>
                </section>
            )}
            {/* Display ingredients details if available */}
            {ingredients && (
                <section>
                    <h2>Ingredients</h2>
                    <div className="nutrition-grid">
                        {Object.entries(ingredients).map(([key, value]) => (
                            <div className="ingredient-item" key={key}>
                                <strong>{key}</strong> {value}
                            </div>
                        ))}
                    </div>
                </section>
            )}
            {/* Display instructions details if available */}
            {instructions && (
                <section className="instructions">
                    <h2>Instructions</h2>
                    <ol>
                        {instructions.map((step, index) => (
                            <li key={index}>{step}</li>
                        ))}
                    </ol>
                </section>
            )}
            {/* Display cost details if available */}
            {cost && (
                <section>
                    <h2>Cost Breakdown</h2>
                    <ul>
                        {Object.entries(cost).map(([item, price], index) => (
                            item !== 'totalCost' && item !== 'totalCostPerServing' && (
                                <li key={index}>{item}: {price}</li>
                            )
                        ))}
                    </ul>
                    <div className="nutrition-grid">
                        <div className="nutrition-item">
                            <strong>Total Cost</strong> {cost.totalCost}
                        </div>
                        <div className="nutrition-item">
                            <strong>Total Cost Per Serving</strong> {cost.totalCostPerServing}
                        </div>
                    </div>
                </section>
            )}
        </div>
    );
}

export default App;
