function updatePizzaToppings(toppings) {
    const pizzaToppings = document.getElementById('pizza-toppings');
    pizzaToppings.innerHTML = '';

    toppings.forEach(topping => {
        const pizzaToppingItem = document.createElement('label')

        pizzaToppingItem.innerHTML = `
        <input type="checkbox" name="toppingOptions" value="${topping.id}"> ${topping.name}</label><br>
        `;

        pizzaToppings.appendChild(pizzaToppingItem)
    })
}

function refreshPizzaOptions() {
    fetch('/toppings', {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => updatePizzaToppings(data))
    .catch(error => console.error('Error:', error));
}

function fetchPizzas() {
    fetch("/pizzas") // Assuming this is your API endpoint
        .then(response => response.json())
        .then(pizzas => {
            const container = document.getElementById("pizzas-container");
            container.innerHTML = ""; // Clear before re-rendering

            const displayView = container.querySelector()
            displayView.innerHTML = "";

            pizzas.forEach(pizza => {
                const pizzaDiv = document.createElement("div");
                pizzaDiv.className = "pizza";
                pizzaDiv.innerHTML = `
                    <h3>${pizza.name}</h3>
                    <p><strong>Toppings:</strong> ${pizza.toppings.join(", ")}</p>
                    <button onclick="editPizza('${pizza.id}')">Edit</button>
                `;
                displayView.appendChild(pizzaDiv);
            });
        });
}

function fetchPizzas() {
    // First, fetch the available toppings
    fetch("/toppings")
    .then(response => response.json())
    .then(toppings => {
        // After toppings are fetched, proceed to fetch pizzas
        fetch("/pizzas")
        .then(response => response.json())
        .then(pizzas => {
            const container = document.getElementById("pizzas-container");
            container.innerHTML = ""; // Clear existing content

            pizzas.forEach(pizza => {
                const pizzaDiv = document.createElement("div");
                pizzaDiv.className = "pizza-container";
                pizzaDiv.setAttribute("data-id", pizza.id); // Store the pizza ID on the container

                // Dynamically create the toppings checkboxes
                const toppingsCheckboxes = toppings.map(topping => {
                    const isChecked = pizza.toppings.includes(topping.name); // Check if this topping is part of the pizza
                    return `
                        <label><input type="checkbox" name="toppings" value="${topping.id}" ${isChecked ? "checked" : ""}> ${topping.name}</label><br>
                    `;
                }).join(""); // Join all toppings checkboxes into a single string                

                pizzaDiv.innerHTML = `
                    <div class="display-view">
                        <h3>${pizza.name}</h3>
                        <p><strong>Toppings:</strong> ${pizza.toppings.join(", ")}</p>
                        <button onclick="toggleEditView('${pizza.id}')">Edit</button>
                    </div>

                    <div class="edit-view" style="display: none;">
                        <form id="edit-pizza-form-${pizza.id}">
                            <label for="pizza-name-${pizza.id}">Pizza Name:</label>
                            <input type="text" id="pizza-name-${pizza.id}" value="${pizza.name}" required>

                            <fieldset id="pizza-toppings-${pizza.id}">
                                <legend>Select Toppings:</legend>
                                ${toppingsCheckboxes}
                            </fieldset>

                            <button type="button" onclick="updatePizza('${pizza.id}', event)">Save</button>

                        </form>
                    </div>
                `;

                container.appendChild(pizzaDiv); // Append the created pizza div
            });
        })
        .catch(error => console.error("Error fetching pizzas:", error)); // Handle potential errors
    })
    .catch(error => console.error("Error fetching toppings:", error)); // Handle errors for toppings fetch
}

function toggleEditView(pizzaId) {
    const pizzaContainer = document.querySelector(`.pizza-container[data-id='${pizzaId}']`);
    const displayView = pizzaContainer.querySelector(".display-view");
    const editView = pizzaContainer.querySelector(".edit-view");

    // Toggle the visibility of the views
    displayView.style.display = displayView.style.display === "none" ? "block" : "none";
    editView.style.display = editView.style.display === "none" ? "block" : "none";
}

function updatePizza(pizzaId, event) {
    event.preventDefault(); // Prevent form submission

    const form = document.getElementById(`edit-pizza-form-${pizzaId}`);
    const pizzaName = form.querySelector(`#pizza-name-${pizzaId}`).value;
    console.log(pizzaName);

    const toppingsCheckboxes = form.querySelectorAll(`#pizza-toppings-${pizzaId} input[type="checkbox"]`);

    const addToppingIds = [];
    const removeToppingIds = [];

    // Fetch the pizza by ID to get its current toppings
    fetch(`/pizzas/${pizzaId}`)
        .then(response => response.json())
        .then(pizza => {
            // Get the IDs of the current toppings
            const currentToppings = pizza.toppings.map(topping => topping.id);
            console.log(currentToppings);

            // Compare each checkbox with the current toppings
            toppingsCheckboxes.forEach(checkbox => {
                const toppingId = checkbox.value;

                if (checkbox.checked && !currentToppings.includes(toppingId)) {
                    // If checked and not already in the pizza's toppings, add it to the addToppingIds array
                    console.log("to add", toppingId)
                    addToppingIds.push(toppingId);
                } else if (!checkbox.checked && currentToppings.includes(toppingId)) {
                    // If unchecked and present in the pizza's toppings, add it to the removeToppingIds array
                    console.log("to delete", toppingId)
                    removeToppingIds.push(toppingId);
                }
            });

            // Make the PUT request to update the pizza
            fetch(`/pizzas/${pizzaId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    pizza_name: pizzaName,
                    add_topping_ids: addToppingIds,
                    remove_topping_ids: removeToppingIds,
                }),
            })
            .then(response => response.json())
            .then(updatedPizza => {
                console.log('Pizza updated:', updatedPizza);
                // Optionally, update the UI here with the updated pizza details
            })
            .catch(error => console.error('Error updating pizza:', error));
        })
        .catch(error => console.error('Error fetching pizza:', error));
}

// Add Pizza (POST request)
document.getElementById('add-pizza-form').addEventListener('submit', async function (event) {
    event.preventDefault();

    // Get pizza name
    const pizzaName = document.getElementById('pizza-name').value;

    // Get selected toppings
    const selectedToppings = Array.from(document.querySelectorAll('input[name="toppingOptions"]:checked'))
        .map(checkbox => checkbox.value);

    // Create the data object to send in the request body
    const pizzaData = {
        pizza_name: pizzaName,
        topping_ids: selectedToppings  // assuming the server expects topping names, or you can adjust to pass ids
    };

    try {
        // Send a POST request to create a new pizza with toppings
        const response = await fetch('/pizzas', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(pizzaData),  // Send the data as JSON
        });

        // Handle the response from the server
        if (response.ok) {
            const jsonResponse = await response.json();
            console.log('Pizza created:', jsonResponse);
            // Optionally, you can update the UI, e.g., show a success message or redirect
        } else {
            const errorResponse = await response.json();
            console.error('Error:', errorResponse);
            // Handle the error, display a message, etc.
        }
    } catch (error) {
        console.error('Network error:', error);
        // Handle network errors, display a message, etc.
    }
});

refreshPizzaOptions()
fetchPizzas()