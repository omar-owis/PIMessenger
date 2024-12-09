function addItem() {
  const list = document.getElementById('list');

  // Create new list item
  const newItem = document.createElement('li');
  newItem.classList.add('list-item'); // Add class for easy targeting

  // Add fields to the new item
  newItem.innerHTML = `
    <button class="delete-btn" onclick="deleteItem(event)">x</button> <!-- Delete button -->
    
    <div class="entry-text">
      <label for="username">Username:</label>
      <input type="text" name="username" class="item-username" placeholder="User-defined string" />
    </div>

    <div class="entry-text">
      <label for="password">Password:</label>
      <input type="password" name="password" class="item-password" placeholder="***********" />
    </div>

    <div class="entry-text">
      <label for="show-password">Show Password:</label>
      <label class="toggle-btn">
        <input type="checkbox" name="show-password" onclick="togglePasswordVisibility(event)" />
        <span></span>
      </label>
    </div>
  `;

  // Append the new item to the list
  list.appendChild(newItem);

  // Scroll to the bottom of the list
  newItem.scrollIntoView({ behavior: "smooth" });
}

// Toggle password visibility
function togglePasswordVisibility(event) {
  const passwordInput = event.target.closest('li').querySelector('.item-password');
  if (event.target.checked) {
    passwordInput.type = 'text'; // Show password
  } else {
    passwordInput.type = 'password'; // Mask password
  }
}


// Function to delete an entry
function deleteItem(event) {
  const item = event.target.closest('li');
  item.remove();
}

// Function to upload items to database
function uploadItems() {
    const listItems = document.querySelectorAll('#list .list-item');
    
    // Prepare an array to hold all the data
    const allData = [];
    
    // Loop through each list item and gather the form data
    listItems.forEach(item => {
        const username = item.querySelector('.item-username').value;   
        const pass = item.querySelector('.item-password').value;

        // Push the collected data for each list item to the allData array
        allData.push({
            username: username,
            password: pass
        });		
    });

    // Send the data to the backend using fetch
    fetch('http://127.0.0.1:5000/accounts/upload', {
        method: 'POST', // HTTP method
        headers: {
            'Content-Type': 'application/json' // Set content type as JSON
        },
        body: JSON.stringify({ items: allData }) // Send the data as a JSON string
    })
    .then(response => response.json()) // Assuming the backend sends a JSON response
    .then(data => {
        console.log('Success:', data);
        alert('Data submitted successfully!');
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error submitting data.');
    });
}