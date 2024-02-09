
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