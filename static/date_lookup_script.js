// function to search and display bins
function search() {
    var date = document.getElementById("dateInput").value;
    var sel = document.getElementById("periodInput");
    var period = sel.options[sel.selectedIndex].text;
    console.log(date, period);

    var data = { 
        date: date, 
        period: period,
    };
    
    fetch('/check_chromebooks', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        var tableBody = document.getElementById('chromebookTableBody');
        // Clear existing table rows
        tableBody.innerHTML = '';

        if (data.length === 0) {
            // If no chromebooks available, display a message
            alert('No bins available.');
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

                var reserveButtonCell = document.createElement('td');
                var reserveButton = document.createElement('button');
                reserveButton.textContent = 'Reserve';
                reserveButton.onclick = function() {
                    reserve(chromebook[0], date, period); // Pass the ID of the chromebook
                };
                reserveButtonCell.appendChild(reserveButton);
                row.appendChild(reserveButtonCell);

                // Append the row to the table body
                tableBody.appendChild(row);
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}


function reserve(id, date, period) {
    var name = prompt("Enter your name:");
    console.log(id, date, period, name);

    var data = { 
        date: date, 
        period: period,
        id: id,
        name: name,
    };

    if (name) {
        fetch('/edit_chromebook', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        alert('Your reservation of ' + id + ' at ' + date + ', period ' + period + ' was a success!');
    }


}


document.addEventListener("DOMContentLoaded", function(event) { // Reference Tracker 2
    // Reference Tracker 1
    // code to auto set the default values for the date input
    var today = new Date().toISOString().slice(0, 10);
    var date = document.getElementById("dateInput");
    date.value = today;
    date.min = today;


});



