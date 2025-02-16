class ToppingView {
    constructor() {
        this.toppingListElement = document.getElementById('topping-list');
        this.addToppingForm = document.getElementById('add-topping-form');
        this.toppingNameInput = document.getElementById('topping-name');
        this.apiUrl = '/toppings';

        // Bind event listeners
        this.attachEventListeners();

        // Initialize the topping list
        this.refreshToppingList();
    }

    updateToppingList(toppings) {
        this.toppingListElement.innerHTML = '';
        toppings.forEach(topping => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `${topping.name}
                <button class="update-btn" data-id="${topping.id}" data-name="${topping.name}">Update</button> 
                <button class="delete-btn" data-id="${topping.id}" data-name="${topping.name}">Delete</button>`; 
            this.toppingListElement.appendChild(listItem);
        });
        this.attachEventListeners();
    }    

    async refreshToppingList() {
        try {
            const response = await fetch(`${this.apiUrl}/`, {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' }
            });
    
            if (!response.ok) {
                throw new Error('Failed to fetch toppings');
            }
    
            const data = await response.json();
            this.updateToppingList(data);
        } catch (error) {
            console.error('Error:', error);
        }
    }
    
    attachEventListeners() {
        // Update buttons
        document.querySelectorAll('.update-btn').forEach(button => {
            button.addEventListener('click', () => {
                const toppingId = button.getAttribute('data-id');
                const oldName = button.getAttribute('data-name');
                const newName = prompt(`Enter new name for "${oldName}":`, oldName)?.trim();
                
                if (newName && newName !== oldName) {
                    this.updateTopping(toppingId, newName);
                }
            });
        });
    
        // Delete buttons
        document.querySelectorAll('.delete-btn').forEach(button => {
            button.addEventListener('click', () => {
                const toppingId = button.getAttribute('data-id');
                const toppingName = button.getAttribute('data-name');
                
                if (confirm(`Are you sure you want to delete "${toppingName}"?`)) {
                    this.deleteTopping(toppingId);
                }
            });
        });
    }
    
    async updateTopping(toppingId, newName) {
        try {
            const response = await fetch(`${this.apiUrl}/${toppingId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ new_topping_name: newName })
            });
    
            if (!response.ok) {
                throw new Error('Failed to update topping');
            }
    
            this.refreshToppingList();
        } catch (error) {
            console.error('Error:', error);
        }
    }
    
    async deleteTopping(toppingId) {
        try {
            const response = await fetch(`${this.apiUrl}/${toppingId}`, {
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' }
            });
    
            if (!response.ok) {
                throw new Error('Failed to delete topping');
            }
    
            this.refreshToppingList();
        } catch (error) {
            console.error('Error:', error);
        }
    }
    
    async addTopping(event) {
        event.preventDefault();
        const name = this.toppingNameInput.value.trim();
    
        if (!name) {
            alert("Topping name cannot be empty.");
            return;
        }
    
        try {
            const response = await fetch(`${this.apiUrl}/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ topping_name: name })
            });
    
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || "Failed to add topping.");
            }
    
            // Clear the input field if successful
            this.toppingNameInput.value = "";
    
            this.refreshToppingList();
        } catch (error) {
            console.error("Error:", error);
            alert(error.message);
        }
    }    
}

// Initialize the ToppingView
const toppingView = new ToppingView();

// Add event listener for the "Add Topping" form
toppingView.addToppingForm.addEventListener('submit', event => toppingView.addTopping(event));
