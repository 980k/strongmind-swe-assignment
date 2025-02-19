// API URL for toppings
const apiUrl = '/toppings';

// DOM elements
const toppingListElement = document.getElementById('topping-list');
const addToppingForm = document.getElementById('add-topping-form');
const toppingNameInput = document.getElementById('topping-name');
const statusMessageElement = document.getElementById('status-message');

// Helper function to show status message
function showStatusMessage(message, isError = false) {
    const statusMessageElement = document.getElementById('status-message');
    statusMessageElement.textContent = message;
    
    statusMessageElement.style.color = isError ? 'red' : 'green';
    
    statusMessageElement.style.visibility = 'visible';
    statusMessageElement.style.opacity = '1';

    // Hide the message after 3 seconds
    setTimeout(() => {
        statusMessageElement.style.opacity = '0';
        setTimeout(() => {
            statusMessageElement.style.visibility = 'hidden';
        }, 1000);
    }, 3000);
}

// Fetch toppings and update the list
async function fetchToppings() {
    try {
        const response = await fetch(`${apiUrl}/`, { method: 'GET', headers: { 'Content-Type': 'application/json' } });
        if (!response.ok) throw new Error('Failed to fetch toppings');
        
        const data = await response.json();
        updateToppingList(data);
    } catch (error) {
        console.error('Error:', error);
        showStatusMessage('Error fetching toppings', true);
    }
}

// Update the topping list in the UI
function updateToppingList(toppings) {
    toppingListElement.innerHTML = '';
    
    toppings.forEach(topping => {
        const listItem = document.createElement('li');
        listItem.setAttribute('data-id', topping.id);

        // Default view (visible name)
        const nameSpan = document.createElement('span');
        nameSpan.classList.add('topping-name');
        nameSpan.textContent = topping.name;

        // Editable input (hidden by default)
        const nameInput = document.createElement('input');
        nameInput.classList.add('edit-topping-input');
        nameInput.value = topping.name;
        nameInput.style.display = 'none';

        // Buttons (Edit & Delete)
        const updateButton = document.createElement('button');
        updateButton.classList.add('update-btn');
        updateButton.textContent = 'Update';

        const deleteButton = document.createElement('button');
        deleteButton.classList.add('delete-btn');
        deleteButton.textContent = 'Delete';

        // Append elements to the list item
        listItem.appendChild(nameSpan);
        listItem.appendChild(nameInput);
        listItem.appendChild(updateButton);
        listItem.appendChild(deleteButton);
        
        toppingListElement.appendChild(listItem);
    });
}

// Event delegation for dynamically created buttons (Update & Delete)
toppingListElement.addEventListener('click', async (event) => {
    const button = event.target;
    const listItem = button.closest('li');
    const toppingId = listItem.getAttribute('data-id');
    const nameSpan = listItem.querySelector('.topping-name');
    const nameInput = listItem.querySelector('.edit-topping-input');

    if (button.classList.contains('update-btn')) {
        // Toggle between the name span and input field for inline editing
        const isEditing = nameInput.style.display === 'inline-block';
        if (isEditing) {
            const newName = nameInput.value.trim();
            if (newName && newName !== nameSpan.textContent) {
                await updateTopping(toppingId, newName);
            }
            nameInput.style.display = 'none';
            nameSpan.style.display = 'inline-block';
            button.textContent = 'Update';
        } else {
            nameInput.style.display = 'inline-block';
            nameSpan.style.display = 'none';
            nameInput.focus();
            button.textContent = 'Save';
        }
    } else if (button.classList.contains('delete-btn')) {
            await deleteTopping(toppingId);
    }
});

// Add a new topping
async function addTopping(event) {
    event.preventDefault();
    const name = toppingNameInput.value.trim();
    
    if (!name) {
        showStatusMessage("Topping name cannot be empty.", true);
        return;
    }
    
    try {
        const response = await fetch(`${apiUrl}/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ topping_name: name })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || "Failed to add topping.");
        }
        
        toppingNameInput.value = "";
        showStatusMessage("Topping added successfully!");
        fetchToppings();
    } catch (error) {
        console.error("Error:", error);
        showStatusMessage(error.message, true);
    }
}

// Update an existing topping
async function updateTopping(toppingId, newName) {
    try {
        const response = await fetch(`${apiUrl}/${toppingId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ new_topping_name: newName })
        });
        
        if (!response.ok) throw new Error('Failed to update topping');
        
        showStatusMessage("Topping updated successfully!");
        fetchToppings();
    } catch (error) {
        console.error("Error:", error);
        showStatusMessage('Topping exists or invalid entry.', true);
    }
}

// Delete an existing topping
async function deleteTopping(toppingId) {
    try {
        const response = await fetch(`${apiUrl}/${toppingId}`, {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' }
        });
        
        if (!response.ok) throw new Error('Failed to delete topping');
        
        showStatusMessage("Topping deleted successfully!");
        fetchToppings();
    } catch (error) {
        console.error("Error:", error);
        showStatusMessage('Error deleting topping', true);
    }
}

// Initialize the page by fetching toppings
fetchToppings();

// Add event listener for adding a new topping
addToppingForm.addEventListener('submit', addTopping);
