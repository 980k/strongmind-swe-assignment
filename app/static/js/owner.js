function updateToppingList(toppings) {
    const toppingList = document.getElementById('topping-list');
    toppingList.innerHTML = '';

    toppings.forEach(topping => {
        const listItem = document.createElement('li');

        listItem.innerHTML = `${topping.name}
            <button class="update-btn" data-name="${topping.name}">Update</button> 
            <button class="delete-btn" data-name="${topping.name}">Delete</button>`;

        toppingList.appendChild(listItem);
    });

    attachEventListeners()
}

function refreshToppingList() {
    fetch('/toppings/get_toppings', {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => updateToppingList(data))
    .catch(error => console.error('Error:', error));
}

function attachEventListeners() {
    document.querySelectorAll('.update-btn').forEach(button => {
        button.addEventListener('click', function() {
            const oldName = button.getAttribute('data-name');
            const newName = prompt('Enter new name for topping:', oldName);

            if (newName) {
                fetch(`toppings/update_topping/${oldName}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ new_topping_name: newName })
                })
                .then(() => refreshToppingList())
                .catch(error => console.error('Error:', error));
            }
        });
    });

    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', function() {
            const name = button.getAttribute('data-name');

            fetch(`toppings/delete_topping/${name}`, {
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' }
            })
            .then(() => refreshToppingList())
            .catch(error => console.error('Error:', error));
        });
    });
}

// Add Topping (POST request)
document.getElementById('add-topping-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const name = document.getElementById('topping-name').value;

    fetch('toppings/add_topping', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topping_name: name })
    })
    .then(() => refreshToppingList())
    .catch(error => console.error('Error:', error));
});


refreshToppingList()
