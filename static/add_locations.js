function checkInputs() {
    var location = document.getElementById("location").value.trim();  
    var admin = document.getElementById("admin").value.trim();
    var amt = document.getElementById("amt").value.trim();
    var id = document.getElementById("binId").value.trim();

    // Check if all inputs are ok
    var isValid = location !== "" && admin !== "" && amt !== "" && id !== "" && typeof location === "string" && location.trim() !== "" && admin.trim() !== "" && !isNaN(Number(amt)) && !isNaN(Number(id)) && isNaN(Number(location));
     
    document.getElementById("submitBtn").disabled = !isValid;
}

async function submit() {
    var location = document.getElementById("location").value;  
    var admin = document.getElementById("admin").value;
    var amt = document.getElementById("amt").value;
    var id = document.getElementById("binId").value;
    
    console.log(location, admin, amt, id);
    
    try {
        const response = await fetch('/create-chromebook-file', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                location: location,
                admin: admin,
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