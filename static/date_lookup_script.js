document.addEventListener("DOMContentLoaded", function() {
    fetch('/get_date_range')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        const startDate = new Date(data.start);
        const endDate = new Date(data.end);
        const formattedStartDate = `${startDate.getFullYear()}-${(startDate.getMonth() + 1).toString().padStart(2, '0')}-${startDate.getDate().toString().padStart(2, '0')}`;
        const formattedEndDate = `${endDate.getFullYear()}-${(endDate.getMonth() + 1).toString().padStart(2, '0')}-${endDate.getDate().toString().padStart(2, '0')}`;
        document.getElementById('yearRange').value = `${formattedStartDate} - ${formattedEndDate}`;
    })
    .catch(error => console.error('Error fetching date range:', error));
});

function showWarningModal() {
    document.getElementById("warning-modal").style.display = "block";
}

function hideWarningModal() {
    document.getElementById("warning-modal").style.display = "none";
}

function updateYear() {
    // Display the warning modal
    showWarningModal();
}

async function updateYearConfirmed() {
    fetch('/updateYear', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        } 
    })
    window.location.reload(); 
    hideWarningModal();
}

function search() {
    /**
     * Function to search for available bins at a certain date and period.
     * The function will display the available bins and create buttons to reserve them.
     * All inputs are taken from HTML inputs in string format.
     */
    var date = document.getElementById("dateInput").value;
    var sel = document.getElementById("periodInput");
    var period = sel.options[sel.selectedIndex].text;
    console.log(date, period);

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

function reserve(id, date, period) {
    /**
     * Function to reserve a bin.
     * Args:
     *      id (string),
     *      date (string),
     *      period (string),
     */
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
                    // window.location.reload();
                    // alert('Your reservation of ' + id + ' at ' + date + ', period ' + period + ' was a success!');   
                    // search();
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
}

function sleep(ms) {
    /**
     * Function that pauses the program.
     * Args:
     *      ms (int)
     *      time in milliseconds
     * Returns:
     *      (Promise)
     */
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function reserveAll() {
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

    var date = document.getElementById("dateInput").value;
    var sel = document.getElementById("periodInput");
    var period = sel.options[sel.selectedIndex].text;

    console.log(selectedBins)
    // Call the reserve function for each selected bin
    selectedBins.forEach(function(binId) {
        // Push each promise returned by reserve() into the array
        reserve(binId, date, period);
    });
    // waiting a bit before searching ensures that when the search function is called, the bins have finished reserving. 
    await sleep(1000);
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



//

document.addEventListener("DOMContentLoaded", function() {
    fetchDateRangeAndUpdate();
    checkAndUpdateDateRange();
    setDefaultDate();
});

function fetchDateRangeAndUpdate() { 
    fetch('/get_date_range')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        const displayText = `Maintaining ${data.start} to ${data.end}`;
        document.getElementById('yearRange').value = displayText;
    })
    .catch(error => console.error('Error fetching date range:', error)); 
}

// Helper function to introduce a delay
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

let isUpdating = false;

async function updateYearConfirmed() {
    if (isUpdating) {
        console.log('Update already in progress. Waiting for the delay to pass.');
        return;
    }

    isUpdating = true;

    try {
        await sleep(2000); // Wait for 2 seconds
        const response = await fetch('/updateYear', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        window.location.reload(); 
    } catch (error) {
        console.error('Error updating year:', error);
    } finally {
        hideWarningModal();
        isUpdating = false;
    }
}

function checkAndUpdateDateRange() {
    fetch('/get_date_range')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const currentDate = new Date();
            let startDate = new Date(data.start);
            let endDate = new Date(data.end);
            let midpoint = new Date((startDate.getTime() + endDate.getTime()) / 2); 
            // If the midpoint was before the current month, update the date range
            if (midpoint < new Date(currentDate.getFullYear(), currentDate.getMonth(), 1)) {

                updateYearConfirmed();
            }
        })
        .catch(error => console.error('Error checking date range:', error));
}

function setDefaultDate() {
    const today = new Date().toISOString().slice(0, 10);
    const dateInput = document.getElementById("dateInput");
    dateInput.value = today;
    dateInput.min = today;
}