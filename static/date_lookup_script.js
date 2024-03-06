// your code here


// function to search and display bins
function search() {
    var date = document.getElementById("dateInput").value;
    var sel = document.getElementById("periodInput");
    var period = sel.options[sel.selectedIndex].text
    console.log(date, period);


   
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



