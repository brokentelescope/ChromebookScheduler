function display() {
    /**
     * Function that displays all reservation history.
     */
    // calls the get_history route from app.py
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
        
        // Accumulate data for the text file
        var textContent = '';

        if (data.length === 0) { 
        } else {
            // Create a table row for the buttons
            var buttonRow = document.createElement('tr');
            
            // Create a cell for the download button with colspan of 2
            var downloadCell = document.createElement('td');
            downloadCell.colSpan = 2;
            var downloadButton = document.createElement('button');
            downloadButton.textContent = 'Download Reservation History as CSV file';
            downloadButton.onclick = function() { createTextFile(textContent); };
            downloadCell.appendChild(downloadButton);
            
            // Create a cell for the clear button with colspan of 2
            var clearCell = document.createElement('td');
            clearCell.colSpan = 2;
            var clearButton = document.createElement('button');
            clearButton.textContent = 'Clear Reservation History';
            clearButton.onclick = function() { clear(); };
            clearCell.appendChild(clearButton);

            // Append cells to the button row
            buttonRow.appendChild(downloadCell);
            buttonRow.appendChild(clearCell);
            
            // Append the button row to the table body
            tableBody.appendChild(buttonRow);

            // Iterate over each array element and create table rows
            data.forEach(function(chromebook, rowIndex) {
                var row = document.createElement('tr');

                // Create table data cells and populate with chromebook data
                chromebook.forEach(function(value, colIndex) {
                    var cell = document.createElement('td');
                    cell.textContent = value;
                    row.appendChild(cell);

                    // Append data to textContent for the text file
                    textContent += value;
                    
                    // Check if it's the last value in the row
                    if (colIndex < chromebook.length - 1) {
                        // If not the last value, add a comma separator
                        textContent += ',';
                    }
                });
                
                // Append newline character after each row
                textContent += '\n';

                // Append the row to the table body
                tableBody.appendChild(row);
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function createTextFile(content) {
    /**
     * Function that creates a csv.file for the admin to download.
     * Args:
     *      content (string)
     */
    // Create a blob with the text content
    var blob = new Blob([content], { type: 'text/plain' });

    // Create a link element
    var a = document.createElement('a');
    a.download = 'history.csv';
    a.href = URL.createObjectURL(blob);

    // Append the link to the body
    document.body.appendChild(a);

    // Trigger a click event on the link to prompt download
    a.click();

    // Clean up: remove the link after download
    document.body.removeChild(a);
}

function clear() {
    /**
     * Function to clear reservation history by calling the server-side endpoint.
     */
    fetch('/clear_history', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.ok) {
            alert('Reservation history cleared.');
            window.location.reload();
        } else {
            alert('Failed to clear reservation history.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}


display();
