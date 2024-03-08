// function to search and display bins
function search() {
    var date = document.getElementById("dateInput").value;
    var sel = document.getElementById("periodInput");
    var period = sel.options[sel.selectedIndex].text
    console.log(date, period);

    var data = { date: date, period: period };
    
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
                reserve(chromebook[0]); // Pass the ID of the chromebook
            };
            reserveButtonCell.appendChild(reserveButton);
            row.appendChild(reserveButtonCell);

            // Append the row to the table body
            tableBody.appendChild(row);
        });
    })
    .catch(error => {
        console.error('Error:', error);
    });
   
}      


function reserve() {
    console.log("TEST");
   
    var id = prompt("Enter ID:");
    var location = prompt("Enter Location:");
    var numOfBins = prompt("Enter Number of Bins Available:");
   
    console.log("id: " + id);
    console.log("location: " + location);
    console.log("numOfBins: " + numOfBins);
    // Do something with the inputs (e.g., validate, process)
    if (id && location && numOfBins) {
        alert("Reservation successful!");
    } else {
        alert("Please fill in all fields.");
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



