document.addEventListener("DOMContentLoaded", () => {
    refreshPizzaOptions();
    fetchPizzas();
});

// Attach event listener to the refresh button directly
const refreshButton = document.getElementById('refresh-button');
refreshButton.addEventListener('click', () => {
    refreshPizzaOptions();
    fetchPizzas();
});

// Cache DOM elements
const pizzasContainer = document.getElementById("pizzas-container");
const pizzaForm = document.getElementById("add-pizza-form");
const pizzaNameInput = document.getElementById("pizza-name");

// Utility function for showing status messages
function showStatusMessage(message, isError = false) {
    const statusMessageElement = document.getElementById('status-message');
    statusMessageElement.textContent = message;
    statusMessageElement.style.color = isError ? 'red' : 'green';
    statusMessageElement.style.display = 'block';

    // Hide the message after 3 seconds
    setTimeout(() => {
        statusMessageElement.style.display = 'none';
    }, 3000);
}

async function fetchJson(url, options = {}) {
    try {
        const response = await fetch(url, options);
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error(`Fetch error (${url}):`, error);
        return null;
    }
}

// ** Load available toppings **
async function refreshPizzaOptions() {
    const toppings = await fetchJson('/toppings');

    const pizzaToppings = document.getElementById('pizza-toppings');
    pizzaToppings.innerHTML = ''; // Clear the current contents of the fieldset

    // Check if there are no toppings
    if (!toppings || toppings.length === 0) {
        const noToppingsMessage = document.createElement('p');
        noToppingsMessage.textContent = 'No toppings available.';

        noToppingsMessage.classList.add('no-toppings-message');

        pizzaToppings.appendChild(noToppingsMessage);
        return; // Exit the function early
    }

    // Add each topping as a checkbox within the fieldset
    toppings.forEach(topping => {
        const label = document.createElement('label');
        label.innerHTML = `
            <input type="checkbox" name="toppingOptions" value="${topping.id}"> ${topping.name}
        `;
        pizzaToppings.appendChild(label);
        pizzaToppings.appendChild(document.createElement('br'));
    });
}

// ** Fetch and display all pizzas **
async function fetchPizzas() {
    const [pizzasData, toppings] = await Promise.all([fetchJson("/pizzas"), fetchJson("/toppings")]);

    pizzasContainer.innerHTML = ""; // Clear before re-rendering

    if (!Array.isArray(pizzasData) || pizzasData.length === 0) {
        const noPizzasMessage = document.createElement("p");
        noPizzasMessage.textContent = "No pizzas available.";
        noPizzasMessage.classList.add("no-pizzas-message"); // Add the CSS class for styling
        pizzasContainer.appendChild(noPizzasMessage);
        return;
    }

    pizzasData.forEach(pizza => {
        pizzasContainer.appendChild(createPizzaElement(pizza, toppings));
    });
}

// ** Create a single pizza card **
function createPizzaElement(pizza, toppings) {
    const pizzaDiv = document.createElement("div");
    pizzaDiv.className = "pizza-container";
    pizzaDiv.dataset.id = pizza.id;

    // Convert toppings to a dictionary for faster lookup
    const toppingsDict = Object.fromEntries(toppings.map(t => [t.id, t.name]));
    const toppingNames = pizza.toppings.map(t => toppingsDict[t.id]).join(", ");

    // If no toppings, display "None"
    const toppingsDisplay = toppingNames || "None";

    pizzaDiv.innerHTML = `
        <div class="display-view">
            <h3>${pizza.name}</h3>
            <p><strong>Toppings:</strong> ${toppingsDisplay}</p>

            <button class="update-button" onclick="toggleEditView('${pizza.id}')">Update</button>
            <button class="delete-button" onclick="deletePizza('${pizza.id}')">Delete</button>
        </div>

        <div class="edit-view" style="display: none;">
            <form id="edit-pizza-form-${pizza.id}">
                <label for="pizza-name-${pizza.id}">Pizza Name:</label>
                <input type="text" id="pizza-name-${pizza.id}" value="${pizza.name}" required>

                <fieldset id="pizza-toppings-${pizza.id}">
                    <legend>Select Toppings:</legend>
                    ${toppings.map(topping => `
                        <label>
                            <input type="checkbox" name="toppings" value="${topping.id}" 
                            ${pizza.toppings.some(t => t.id === topping.id) ? "checked" : ""}> 
                            ${topping.name}
                        </label><br>
                    `).join("")}
                </fieldset>

                <button 
                    type="button" 
                    data-pizza-id="${pizza.id}" 
                    data-topping-ids='${JSON.stringify(pizza.toppings.map(t => t.id))}' 
                    onclick="updatePizza(this)"
                >
                    Save
                </button>

            </form>
        </div>
    `;

    return pizzaDiv;
}

// ** Toggle edit view **
function toggleEditView(pizzaId) {
    const pizzaContainer = document.querySelector(`.pizza-container[data-id='${pizzaId}']`);
    const displayView = pizzaContainer.querySelector(".display-view");
    const editView = pizzaContainer.querySelector(".edit-view");

    const isEditing = editView.style.display === "block";
    displayView.style.display = isEditing ? "block" : "none";
    editView.style.display = isEditing ? "none" : "block";
}

// ** Update pizza **
async function updatePizza(button) {
    const pizzaId = button.getAttribute('data-pizza-id');
    const toppingIdsJson = button.getAttribute('data-topping-ids');
    
    const form = document.getElementById(`edit-pizza-form-${pizzaId}`);
    const pizzaName = form.querySelector(`#pizza-name-${pizzaId}`).value;
    const toppingsCheckboxes = form.querySelectorAll(`input[name="toppings"]:checked`);
    const selectedToppings = Array.from(toppingsCheckboxes).map(cb => cb.value);

    const currentToppingIds = JSON.parse(toppingIdsJson);  // Convert back to an array

    const addToppingIds = selectedToppings.filter(id => !currentToppingIds.includes(id));
    const removeToppingIds = currentToppingIds.filter(id => !selectedToppings.includes(id));

    const response = await fetchJson(`/pizzas/${pizzaId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            pizza_name: pizzaName, 
            add_topping_ids: addToppingIds, 
            remove_topping_ids: removeToppingIds 
        }),
    });

    if (response) {
        fetchPizzas(); // Refresh list and get updates
        showStatusMessage("Pizza updated successfully!", false);
    } else {
        showStatusMessage("Pizza name already exists.", true);
    }
}

// ** Delete pizza **
async function deletePizza(pizzaId) {
    const response = await fetchJson(`/pizzas/${pizzaId}`, { method: 'DELETE' });

    if (response) {
        document.querySelector(`.pizza-container[data-id='${pizzaId}']`).remove();
        showStatusMessage("Pizza deleted successfully!", false);
    } else {
        showStatusMessage("Failed to delete pizza.", true);
    }
}

// ** Add Pizza **
pizzaForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const selectedToppings = Array.from(document.querySelectorAll('input[name="toppingOptions"]:checked'))
        .map(checkbox => checkbox.value);

    const response = await fetchJson('/pizzas', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pizza_name: pizzaNameInput.value, topping_ids: selectedToppings }),
    });

    if (response) {
        pizzaNameInput.value = ""; // Reset form
        document.querySelectorAll('input[name="toppingOptions"]:checked').forEach(cb => cb.checked = false);
        fetchPizzas();
        showStatusMessage("Pizza added successfully!", false);
    } else {
        showStatusMessage("Failed to add pizza.", true);
    }
});
