function cancelAll() { 
    /**
     * Function that cancels the user's selected reservations.
     * Input is taken from HTML checkbox input.
     */
    var selectedBins = [];
    var checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');

    // console.log(checkboxes)
    checkboxes.forEach(function(checkbox) { 
        // console.log(checkbox.value[0])
        selectedBins.push(checkbox.value); 
    });

    if (selectedBins.length === 0) {
        alert('Please select at least one bin to cancel.');
        return;
    } 
    // Call the reserve function for each selected bin
    selectedBins.forEach(function(tmp) {  
        cancel(tmp.split(',')[0], tmp.split(',')[1], tmp.split(',')[2]);
    });
}

function display() {  
    /**
     * Function that displays a user's reservations and allows them to cancel them if needed.
     */
    fetch('/get_reserved', {
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
        // Iterate over each array element and create table rows
        data.forEach(function(chromebook) {
            var row = document.createElement('tr'); 
            // Create table data cells and populate with chromebook data
            chromebook.forEach(function(value) {
                var cell = document.createElement('td');
                cell.textContent = value; 
                row.appendChild(cell);
            });
            
            // checkbox
            var cell = document.createElement('td'); 
            var checkbox = document.createElement('input');                
            checkbox.type = 'checkbox';   
            checkbox.classList.add('largerCheckbox');
            tmp =  [row.childNodes[0].textContent, row.childNodes[2].textContent, row.childNodes[3].textContent]  
            checkbox.value = tmp
            cell.appendChild(checkbox);
            row.appendChild(cell);
            
            // Append the row to the table body
            tableBody.appendChild(row);
        }); 
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
display();

function cancel(id, date, period) {  
    /**
     * Function that cancels a reservation.
     * Args:
     *      id (string),
     *      date (string),
     *      period (string)
     */
    // console.log(id, date, period)
    var data = { 
        date: date, 
        period: period,
        id: id, 
    };   
    // calls the cancel_chromebook route from app.py.
    fetch('/cancel_chromebook', {
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

