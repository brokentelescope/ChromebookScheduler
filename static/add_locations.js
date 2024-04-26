/**
 * Function that validates in the inputs taken from HTML inputs and disables/enables the submit button accordingly.
 * All inputs are taken from HTML inputs in string format.
 */
function checkInputs() {
    var location = document.getElementById("location").value.trim();  
    var amt = document.getElementById("amt").value.trim();
    var id = document.getElementById("binId").value.trim();

    // All inputs must not be blank.
    // The amount input must be a number.
    var isValid = location !== "" && amt !== "" && id !== "" && !isNaN(Number(amt));

    // Enable/disable the submit button depending on if the inputs are valid. 
    document.getElementById("submitBin").disabled = !isValid;

    // This code checks if the bin ID already exists.
    // If it does exist, disable the submit button.
    if (isValid) {
        fetch('/check_bin', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'binId=' + encodeURIComponent(id)
        })
        .then(response => response.json())
        .then(data => {
            if (data.is_duplicate) {
                // If bin is duplicate, disable submit button
                document.getElementById("submitBin").disabled = true;
                alert('This bin ID already exists. Enter a different one.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}

/**
 * Function that creates a new text-file for the inputted bin.
 * All inputs are taken from HTML inputs in string format.
 */
async function submit() { 
    var location = document.getElementById("location").value;   
    var amt = document.getElementById("amt").value;
    var id = document.getElementById("binId").value;
    
    // calls the create-chromebook-file route defined in app.py
    try {
        const response = await fetch('/create-chromebook-file', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                location: location,
                amt: amt, 
                id: id
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
        alert('An error occured.');
    }
}
