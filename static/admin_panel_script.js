function display() { 
    /**
     * Function that displays all users (except the admin) and creates buttons that 
     * allow for the banning, edit of verification status.
     */
    // calls the get-account route from app.py
    fetch('/get_account', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        var tableBody = document.getElementById('reservationTableBody');  
        // Clear existing table rows
        tableBody.innerHTML = '';
        var x = data.data;
        var isUserVerified = data.is_verified;

        if (x.length === 0) {
            // If no chromebooks available, display a message
            alert('No Reservations.');
        } 
        else {
            // Iterate over each array element and create table rows
            x.forEach(function(x) {
                if (x.includes('ADMIN')) return;
                var row = document.createElement('tr'); 
                // Create table data cells and populate with chromebook data
                x.forEach(function(value) {  
                    // Change the colour of unverified user 
                    if (value == 1 || value == 0){
                        if (value == 1){ 
                            row.childNodes[0].classList.add('verified-user');    
                        }else if (value == 0){
                            row.childNodes[0].classList.add('unverified-user');    
                        }
  
                    } else { 
                        var cell = document.createElement('td');  
                        cell.textContent = value; 
                        row.appendChild(cell); 
                    }

                });
                // Append the row to the table body
                var reserveButtonCell = document.createElement('td');
                var reserveButton = document.createElement('button');
                reserveButton.textContent = 'Remove User';

                if (isUserVerified) { 
                    reserveButton.onclick = function() {  
                        var userName = row.childNodes[0].textContent 
                        ban(userName); // Pass the ID of the chromebook
                    };
                } else {
                    // If user is not verified, button is disabled and grayed out
                    reserveButton.disabled = true;
                    reserveButton.style.opacity = 0.5; // Set opacity to visually indicate button is disabled
                }
                
                reserveButtonCell.appendChild(reserveButton); 
                row.appendChild(reserveButtonCell);
                tableBody.appendChild(row);

                // Insert button into its cell
                var cell = document.createElement('td');
                var button = document.createElement('button');
                button.textContent = 'Verify';

                if (isUserVerified) { 
                    button.onclick = function() {
                        var userName = row.childNodes[0].textContent 
                        verify(userName); // Pass the ID of the chromebook
                    }
                } else {
                    // If user is not verified, button is disabled and grayed out
                    button.disabled = true;
                    button.style.opacity = 0.5; // Set opacity to visually indicate button is disabled
                }
                cell.appendChild(button);
                row.appendChild(cell);
                tableBody.appendChild(row);
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

display();

function ban(userName) { 
    /**
     * Function that bans a user.
     * Args:
     *      userName: (string)
     */
    var data = { 
        userName: userName
    };   
    // calls the remove_account route from app.py
    fetch('/remove_account', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    }) 
    .then(response => {
        if (response.ok) {
            // Reload the current page if fetch request is successful
            window.location.reload();
        } else {
            // Handle error if needed
            console.error('Error cancelling reservation');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function verify(userName) {
    /**
     * Function that verifies a user.
     * Args:
     *      userName: string
     */
    var data = { 
        userName: userName
    };   
    // calls the verify_account route from app.py
    fetch('/verify_account', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    }) 
    .then(response => {
        if (response.ok) {
            // Reload the current page if fetch request is successful
            window.location.reload();
        } else {
            // Handle error if needed
            console.error('Error cancelling reservation');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    }); 
}

