// your code here
function search() {
    // Retrieve values from the inputs
    var month = document.getElementById('month_select').value;
    var day = document.getElementById('day_select').value;
    var period = document.getElementById('period_select').value;

    // Do something with the values
    console.log("Month: " + month);
    console.log("Day: " + day);
    console.log("Period: " + period);
    
    // You can further process or store these values as needed
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
    console.log(document.getElementById("dateInput"));
    var date = document.getElementById("dateInput");
    date.value = today;
    date.min = today;

    console.log(today);
});
