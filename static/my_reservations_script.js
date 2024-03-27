function button(){  
    console.log(123)
    let userName = null; // Declare userName using let

    // Fetch data.json from the server route
    fetch('/get_data')
        .then(response => response.json())
        .then(data => {
            // Parse the JSON data
            userName = data.my_variable;
             
            console.log("My variable from Python:", userName);

            // Call a separate function to handle further logic
            handleUserName(userName);
        })
        .catch(error => console.error('Error fetching JSON:', error));

    // This console.log will execute before the fetch request is complete
    // console.log(userName);
}

async function handleUserName(userName) {
    console.log(userName)
    try { 
        const response = await fetch('/reload_reservation_history-file', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({  
                name:userName  
            })
        }); 
        if (!response.ok) {
            throw new Error('Failed to call Flask route');
        }

        const data = await response.text();
        alert(data);
    } 
    catch (error) { 
        console.error('Error:', error.message);
    }
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