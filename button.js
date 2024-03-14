// script.js
document.addEventListener("DOMContentLoaded", function() {
    // Event listener for the button click
    document.getElementById("apiButton").addEventListener("click", function() {
        // Call the function to send the API request
        fetch('https://dev01.acrossmedical.co.uk/parser')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            document.getElementById('responseArea').textContent = JSON.stringify(data);
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
    });
});
