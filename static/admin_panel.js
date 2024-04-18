function display() { 
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
        if (data.length === 0) {
            // If no chromebooks available, display a message
            alert('No Reservations.');
        } 
        else {
            // Iterate over each array element and create table rows
            data.forEach(function(chromebook) {
                var row = document.createElement('tr'); 
                // Create table data cells and populate with chromebook data
                chromebook.forEach(function(value) {
                    var cell = document.createElement('td');
                    cell.textContent = value; 
                    row.appendChild(cell); 
                });
                // Append the row to the table body

                var reserveButtonCell = document.createElement('td');
                var reserveButton = document.createElement('button');
                reserveButton.textContent = 'Remove User';
                reserveButton.onclick = function() {  
                    var userName = row.childNodes[0].textContent 
                    cancel(userName); // Pass the ID of the chromebook
                };
                reserveButtonCell.appendChild(reserveButton); 
                row.appendChild(reserveButtonCell);
                tableBody.appendChild(row);

                // Insert button into its cell
                var cell = document.createElement('td');
                var button = document.createElement('button');
                button.textContent = 'Verify';

                button.onclick = function() {
                    var userName = row.childNodes[0].textContent 
                    verify(userName); // Pass the ID of the chromebook
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

display()

function cancel(userName) { 
    var data = { 
        userName: userName
    };   
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
    var data = { 
        userName: userName
    };   
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
// document.addEventListener("DOMContentLoaded", function(event) { // Reference Tracker 2
//     // Reference Tracker 1
//     // code to auto set the default values for the date input
//     var today = new Date().toISOString().slice(0, 10);
//     var date = document.getElementById("dateInput");
//     date.value = today;
//     date.min = today;


// });

