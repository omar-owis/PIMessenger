async function addItem() {
  const list = document.getElementById('list');

  // Create new list item
  const newItem = document.createElement('li');
  newItem.classList.add('list-item'); // Add class for easy targeting
  
    // Generate a unique ID for the server-defined ID
  const uniqueID = Date.now() + '-' + Math.floor(Math.random() * 1000);

  // Add fields to the new item
  newItem.innerHTML = `  
    <button class="delete-btn" onclick="deleteItem(event)">x</button> <!-- Delete button -->
    <div class="entry-text">
      <label for="type">Type:</label>
      <select name="type" class="item-type">
        <option value="reply">Reply</option>
        <option value="time">Time Event</option>
        <option value="reaction">Reaction</option>
      </select>
    </div>

    <div class="entry-text">
      <label for="name">Event Name:</label>
      <input type="text" name="name" class="item-name" placeholder="Enter Event Name" />
    </div>

    <div class="entry-text">
      <label for="id">ID (Server-defined):</label>
      <input type="text" name="id" class="item-id" value="${uniqueID}" disabled />
    </div>

	<div class="entry-text">
	  <label for="chat">Chat:</label>
	  <select name="chat" class="item-chat" onchange="redirectToAddChat(this)">
	  </select>
	</div>

    <div class="entry-text">
      <label for="message">Send Message:</label>
      <input type="text" name="message" class="item-message" placeholder="Enter Send Message" />
    </div>

    <div class="entry-text time-event">
      <label for="time">Trigger Time:</label>
      <input type="time" name="time" />
    </div>

    <div class="entry-text reply-data">
      <label for="reply-name">Reply To:</label>
      <input type="text" name="reply-name" placeholder="Enter Username" />

      <label for="trigger-message">Trigger Message:</label>
      <input type="text" name="trigger-message" placeholder="Enter Trigger Message" />

      <label for="limit-daily">Limit Daily:</label>
      <label class="toggle-btn">
        <input type="checkbox" name="limit-daily" />
        <span></span>
      </label>
    </div>

    <div class="entry-text">
      <label for="delay">Delay:</label>
      <input type="number" name="delay" placeholder="Enter Delay" value="0"/>
      <select name="delay-unit">
        <option value="sec">Sec</option>
        <option value="min">Min</option>
        <option value="hr">Hr</option>
      </select>
    </div>
  `;
  
  // Append the new item to the list
  list.appendChild(newItem);
  
  // Populate the chat select field with chat options
  const chatSelect = newItem.querySelector('.item-chat');
  option = document.createElement('option');
  option.textContent = "Select Chat";
  option.value = -1;
  chatSelect.appendChild(option);
  
  chats = await fetchChatData();
  chats.forEach(chat => {
    option = document.createElement('option');
    option.value = chat.id;  // Set value to the chat's ID
    option.textContent = chat.name;  // Set display text to the chat's name
    chatSelect.appendChild(option);
  });
  option = document.createElement('option');
  option.textContent = "+ Add New Chat";
  option.value = -1;
  chatSelect.appendChild(option);

  // Scroll to the bottom of the list
  newItem.scrollIntoView({ behavior: "smooth" });
}

// Function to delete an entry
function deleteItem(event) {
  const item = event.target.closest('li');
  item.remove();
}

// Function to filter the list based on input values
function filterList() {
  const nameFilter = document.getElementById('filter-name').value.toLowerCase();
  const idFilter = document.getElementById('filter-id').value.toLowerCase();
  const chatFilter = document.getElementById('filter-chat').value;
  const typeFilter = document.getElementById('filter-type').value;

  const items = document.querySelectorAll('.list-item');

  items.forEach(item => {
    const name = item.querySelector('.item-name').value.toLowerCase();
    const id = item.querySelector('.item-id').value.toLowerCase();
    const chat = item.querySelector('.item-chat').value;
    const type = item.querySelector('.item-type').value;

    const matchesName = name.includes(nameFilter);
    const matchesID = id.includes(idFilter);
    const matchesChat = chat.includes(chatFilter);
    const matchesType = type.includes(typeFilter);

    if (matchesName && matchesID && matchesChat && matchesType) {
      item.style.display = ''; // Show item
    } else {
      item.style.display = 'none'; // Hide item
    }});
}
// Function to toggle the dropdown visibility
function toggleFilterDropdown() {
  const dropdown = document.getElementById('filter-dropdown');
  dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
}

// Function to upload items to database
function uploadItems() {
    const listItems = document.querySelectorAll('#list .list-item');
    
    // Prepare an array to hold all the data
    const allData = [];
    
    // Loop through each list item and gather the form data
    listItems.forEach(item => {
        const type = item.querySelector('.item-type').value;   
        const name = item.querySelector('.item-name').value;
        const id = item.querySelector('.item-id').value; // Disabled input, but still readable
        const chat = item.querySelector('.item-chat').value;
        const message = item.querySelector('.item-message').value;
        const time = item.querySelector('[name="time"]').value;
        const replyName = item.querySelector('[name="reply-name"]').value;
        const triggerMessage = item.querySelector('[name="trigger-message"]').value;
        const limitDaily =  item.querySelector('[name="limit-daily"]').checked; // checkbox
        const delay = item.querySelector('[name="delay"]').value;
        const delayUnit = item.querySelector('[name="delay-unit"]').value;
		
		let delayInt = parseInt(delay, 10);
		switch(delayUnit) {
		  case 'min':
			delayInt = delayInt * 60;
			break;
		  case 'hr':
			delayInt = delayInt * 3600;
			break;
		}

        // Push the collected data for each list item to the allData array
        allData.push({
            type: type,
            name: name,
            id: id,
            chat_id: chat,
            message: message,
            execute_time: time,
            random_delay_sec: delayInt,
			reply_username: replyName,
			reply_trigger_message: triggerMessage,
			reply_limit_daily: limitDaily
        });		
    });

    // Send the data to the backend using fetch
    fetch('http://127.0.0.1:5000/events/upload', {
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

function redirectToAddChat(selectElement) {
  const value = selectElement.value;
  if (value === "+ Add New Chat") {
    window.location.href = "/chats"; // Redirect to the add new chat page
  }
}

// Function to fetch chat data and handle the response
function fetchChatData() {
  return fetch('/get/chatnames')
    .then(response => response.json())
    .then(data => data.chats)  // Return the list of chats from the backend
    .catch(error => {
      console.error('Error fetching chat data:', error);
      return [];  // Return an empty array in case of an error
    });
}