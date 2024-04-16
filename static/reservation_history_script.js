function display() {
    fetch('/get_history', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        var tableBody = document.getElementById('historyTableBody');
        // Clear existing table rows
        tableBody.innerHTML = '';
        if (data.length === 0) {
            // If no chromebooks available, display a message
            alert('No history.');
        } else {
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
                tableBody.appendChild(row);
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

display();