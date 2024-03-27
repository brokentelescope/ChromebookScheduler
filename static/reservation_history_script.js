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
        
        // Accumulate data for the text file
        var textContent = '';

        if (data.length === 0) {
            // If no chromebooks available, display a message
            alert('No history.');
        } 
        else {
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

            // Create a new text file with the accumulated data
            createTextFile(textContent);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });

}

// function createTextFile(content) {
//     // Create a blob with the text content
//     var blob = new Blob([content], { type: 'text/plain' });

//     // Create a link element
//     var a = document.createElement('a');
//     a.download = 'reservation_history.txt';
//     a.href = URL.createObjectURL(blob);

//     // Append the link to the body
//     document.body.appendChild(a);

//     // Remove the link from the body
//     document.body.removeChild(a);
// }


display();