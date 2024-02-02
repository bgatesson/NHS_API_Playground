// script.js

document.addEventListener("DOMContentLoaded", function() {
    // Event listener for the button click
    document.getElementById("apiButton").addEventListener("click", function() {
        // Call the function to send the API request
        sendApiRequest();
    });
});

// Function to send the API request
function sendApiRequest() {
    // You can use the Fetch API or any other method to make the API call
    // Here's a basic example using the Fetch API to fetch a sample JSON placeholder API
    fetch('https://jsonplaceholder.typicode.com/todos/1')
        .then(response => response.json())
        .then(data => {
            // Display the API response in the designated area
            document.getElementById("apiResponse").innerHTML = `<p>API Response: ${JSON.stringify(data)}</p>`;
        })
        .catch(error => {
            console.error('Error:', error);
            // Display an error message if the API call fails
            document.getElementById("apiResponse").innerHTML = `<p>Error: ${error.message}</p>`;
        });
}
