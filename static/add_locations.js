// function submit(event){ 
//     event.preventDefault();
//     var location = document.getElementById("location").value;  
//     var admin = document.getElementById("admin").value;
//     var amt = document.getElementById("amt").value;
//     var id = document.getElementById("binId").value;

//     console.log(location, admin, amt, id);
// }

async function submit() {
    try {
        const response = await fetch('/create-chromebook-file', {
            method: 'POST'
        });

        if (!response.ok) {
            throw new Error('Failed to call Flask route');
        }

        const data = await response.text();
        console.log(data); // Log the response from Flask
    } catch (error) {
        console.error('Error:', error.message);
    }
}