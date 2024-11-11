async function getFoodData() {
    const foodQuery = document.getElementById("foodQuery").value;
    const grams = parseFloat(document.getElementById("foodGrams").value);

    try {
        const response = await fetch("/get_food_data", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ food_query: foodQuery, grams: grams })
        });

        if (!response.ok) {
            throw new Error("Network response was not ok.");
        }

        const data = await response.json();
        displayFoodData(data);  // Display the data on the page
    } catch (error) {
        console.error("Error fetching food data:", error);
    }
}


function displayFoodData(data) {
    const resultDiv = document.getElementById("foodDataResult");
    resultDiv.innerHTML = `
        <p>Calories: ${data.Calories}</p>
        <p>Fats: ${data.Fats}</p>
        <p>Sodium: ${data.Sodium}</p>
        <p>Carbohydrates: ${data.Carbohydrates}</p>
        <p>Protein: ${data.Protein}</p>
    `;
}


async function calculateCaloriesBurned() {
    const age = parseInt(document.getElementById("age").value);
    const height = parseFloat(document.getElementById("height").value);
    const weight = parseFloat(document.getElementById("weight").value);
    const gender = document.getElementById("gender").value;
    const distance = parseFloat(document.getElementById("distance").value);
    const difficulty = parseInt(document.getElementById("difficulty").value);

    try {
        const response = await fetch("/calculate_burned_calories", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ age, height, weight, gender, distance, difficulty })
        });

        if (!response.ok) {
            throw new Error("Network response was not ok.");
        }

        const data = await response.json();
        displayExerciseData(data);  // Display the calculated data
    } catch (error) {
        console.error("Error fetching burned calories:", error);
    }
}


function displayExerciseData(data) {
    const resultDiv = document.getElementById("exerciseDataResult");
    resultDiv.innerHTML = `
        <p>Calories Burned: ${data.calories_burned}</p>
    `;
}

