async function addItem() {
  const list = document.getElementById('list');

  // Create new list item
  const newItem = document.createElement('li');
  newItem.classList.add('list-item'); // Add class for easy targeting

  // Add fields to the new item
  newItem.innerHTML = `  
    <button class="delete-btn" onclick="deleteChat(event)">x</button> <!-- Delete button -->
    <div class="entry-text">
      <label for="name">Name:</label>
      <input type="text" name="name" class="chat-name" placeholder="Enter Chat Name" />
    </div>

	<div class="entry-text">
	  <label for="account">Account:</label>
	  <select name="account" class="item-chat" onchange="redirectToAddAccount(this)">
	  </select>
	</div>

    <div class="entry-text">
      <label for="id">Messenger ID:</label>
      <input type="number" name="id" class="chat-id" placeholder="Enter User/Group ID" />
    </div>

    <div class="entry-text">
      <label for="messenger-type">Messenger Type:</label>
      <select name="messenger-type" class="chat-type">
        <option value="user">User</option>
        <option value="group">Group</option>
      </select>
    </div>
  `;

  // Append the new item to the list
  list.appendChild(newItem);
  
  // Populate the account select field with account options
  const accountSelect = newItem.querySelector('.item-chat');
  option = document.createElement('option');
  option.textContent = "Select Account";
  option.value = "-1";
  accountSelect.appendChild(option);
  
  accounts = await fetchAccountData();
  accounts.forEach(account => {
    option = document.createElement('option');
    option.textContent = account.name;  // Set display text to the account's name
    accountSelect.appendChild(option);
  });
  option = document.createElement('option');
  option.textContent = "+ Add New Account";
  option.value = "-1";
  accountSelect.appendChild(option);

  // Scroll to the bottom of the list
  newItem.scrollIntoView({ behavior: "smooth" });
}

// Function to delete an entry
function deleteChat(event) {
  const item = event.target.closest('li');
  item.remove();
}

function redirectToAddAccount(selectElement) {
  const value = selectElement.value;
  if (value === "+ Add New Account") {
    window.location.href = "/accounts";
  }
}

// Function to fetch account data and handle the response
function fetchAccountData() {
  return fetch('/get/accountnames')
    .then(response => response.json())
    .then(data => data.accounts)  // Return the list of account from the backend
    .catch(error => {
      console.error('Error fetching chat data:', error);
      return [];  // Return an empty array in case of an error
    });
}

// Function to upload items to database
function uploadItems() {
    const listItems = document.querySelectorAll('#list .list-item');
    
    // Prepare an array to hold all the data
    const allData = [];
    
    // Loop through each list item and gather the form data
    listItems.forEach(item => {
        const name = item.querySelector('.chat-name').value;   
        const account = item.querySelector('.item-chat').value;
		const MessengerID = item.querySelector('.chat-id').value;
		const type = item.querySelector('.chat-type').value

        // Push the collected data for each list item to the allData array
        allData.push({
            name: name,
			account: account,
			messenger_ID: MessengerID,
			type: type
        });		
    });

    // Send the data to the backend using fetch
    fetch('http://127.0.0.1:5000/chats/upload', {
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