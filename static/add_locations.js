/**
 * Checks that the bin ID inputted does not already exist.
 * Allows the admin to add the bin accordingly. 
 */
function checkInputs() {
    var location = document.getElementById("location").value.trim();  
    var amt = document.getElementById("amt").value.trim();
    var id = document.getElementById("binId").value.trim();

    // Check if all inputs are ok
    var isValid = location !== "" && amt !== "" && id !== "" && !isNaN(Number(amt));
     
    document.getElementById("submitBin").disabled = !isValid;

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
                alert('Duplicate bin found. Please choose a different one.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}

/**
 * Function that creates a new text-file for the inputted bin.
 */
async function submit() { 
    var location = document.getElementById("location").value;   
    var amt = document.getElementById("amt").value;
    var id = document.getElementById("binId").value;
    
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
    }
}
