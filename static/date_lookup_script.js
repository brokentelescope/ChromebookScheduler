function reserveAll() {
    var selectedBins = [];
    var checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
    // console.log(checkboxes)
    checkboxes.forEach(function(checkbox) { 
        selectedBins.push(checkbox.value);
    });

    if (selectedBins.length === 0) {
        alert('Please select at least one bin to reserve.');
        return;
    }

    var date = document.getElementById("dateInput").value;
    var sel = document.getElementById("periodInput");
    var period = sel.options[sel.selectedIndex].text;

    // Call the reserve function for each selected bin
    selectedBins.forEach(function(binId) {
        reserve(binId, date, period);
    });
}

/**
 * Function to search for available bins at a certain date and period.
 * The function will display the available bins and create buttons to reserve them.
 * All inputs are taken from HTML inputs in string format.
 */

function search() {
    var date = document.getElementById("dateInput").value;
    var sel = document.getElementById("periodInput");
    var period = sel.options[sel.selectedIndex].text;

    var data = { 
        date: date, 
        period: period, 
    };
    
    // call the check_chromebooks route from app.py
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

        var chromebooks = data.chromebooks;
        
        if (chromebooks.length === 0) {
            // If no chromebooks available, display a message
            alert('No bins available.');
        } else {
            // Iterate over each array element and create table rows
            chromebooks.forEach(function(chromebook) {
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

                
                checkbox.value = row.childNodes[0].textContent; 
                cell.appendChild(checkbox);
                row.appendChild(cell);
                
                // Append the row to the table body
                tableBody.appendChild(row);
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

/**
 * Function to reserve a bin.
 * Input:
 *      id (string),
 *      date (string),
 *      period (string),
 *      using_custom_classroom (int (0 or 1))
 *
 */
function reserve(id, date, period) {
    var data = { 
        date: date, 
        period: period,
        id: id, 
    };

    // this first fetch is just to check if the chromebook bin has just been reserved or not
    // this check would only be useful if two users are trying to reserve the same chromebook bin at the exact same time (which is very unlikely)
    // also prevents users from booking a chromebook bin twice?
    // calls the check route from app.py
    fetch('/check', {method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); 
    })
    .then(responseData => {
        if (responseData == true) {
            // calls the edit_chromebook route from flask.
            fetch('/edit_chromebook', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data)})
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(responseData => {
                if (responseData == 'Success') {
                    alert('Your reservation of ' + id + ' at ' + date + ', period ' + period + ' was a success!');   
                }
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });
        }
        else {
            alert('The bin has just been reserved.');
        }
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
    search();
}


document.addEventListener("DOMContentLoaded", function(event) { // Reference Tracker 2
    // Reference Tracker 1
    // code to auto set the default values for the date input
    var today = new Date().toISOString().slice(0, 10);
    var date = document.getElementById("dateInput");
    date.value = today;
    date.min = today;


});