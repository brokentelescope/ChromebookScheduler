// function to search and display bins
function search() {
    var date = document.getElementById("dateInput").value;
    var sel = document.getElementById("periodInput");
    var period = sel.options[sel.selectedIndex].text;

    var data = { 
        date: date, 
        period: period,
    };
    fetch('/get_current_locations', { 
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        var tableBody = document.getElementById('t');   
        tableBody.innerHTML = '';
        if (data.length === 0) { 
            alert('No bins.');
        } 
        else {
            data.forEach(function(tmp) {
                var row = document.createElement('tr'); 
                tmp.forEach(function(value) {
                    var cell = document.createElement('td');
                    cell.textContent = value; 
                    row.appendChild(cell); 
                });
                tableBody.appendChild(row);
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
 
}



 
display();
 