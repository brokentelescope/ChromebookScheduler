async function deleteAll() { 
    /**
     * Function to reserve all selected bins.
     * All input is taken from the checked checkbox values.
     * Input is in the form of a list of bins.
     */
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
    // Call the reserve function for each selected bin
    selectedBins.forEach(function(binId) {
        // Push each promise returned by reserve() into the array
        deleteBin(binId);
    }); 
}
function deleteBin(id){
    var data = {  
        id: id, 
    };
 
    fetch('/delete_chromebook', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data)})
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(responseData => {
        if (responseData == 'Success') {
            window.location.reload();
            // alert('Your reservation of ' + id + ' at ' + date + ', period ' + period + ' was a success!');   
            // search();
        }
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    }); 
}

function display() { 
    fetch('/get_chromebooks', {  
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        } 
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
            document.getElementById("headerRow").style.display = "table-row";
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


display();
function checkInputs() {
    /**
     * Function that validates in the inputs taken from HTML inputs and disables/enables the submit button accordingly.
     * All inputs are taken from HTML inputs in string format.
     */
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

async function submit() { 
    /**
     * Function that creates a new text-file for the inputted bin.
     * All inputs are taken from HTML inputs in string format.
     */
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
        window.location.reload();
    } 
    catch (error) {
        console.error('Error:', error.message);
        alert('An error occured.');
    }
}
