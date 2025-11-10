// Function to display the dog image for a given HTTP status code
function showDog() {
    var statusCode = document.getElementById('statusCode').value.trim();
    var resultDiv = document.getElementById('result');
    
    // Validate input
    if (!statusCode) {
        resultDiv.innerHTML = '<p class="error-message">Please enter a status code!</p>';
        return;
    }
    
    // Check if it's a valid number
    if (isNaN(statusCode) || statusCode < 100 || statusCode > 599) {
        resultDiv.innerHTML = '<p class="error-message">Please enter a valid HTTP status code (100-599)!</p>';
        return;
    }
    
    // Display the dog image
    displayDogImage(statusCode);
}

// Function to display the dog image
function displayDogImage(code) {
    var resultDiv = document.getElementById('result');
    var imageUrl = 'https://http.dog/' + code + '.jpg';
    
    // Create the HTML for displaying the image
    var html = '<div class="dog-container">';
    html += '<h2>HTTP ' + code + '</h2>';
    html += '<img src="' + imageUrl + '" alt="HTTP ' + code + ' Dog" onerror="handleImageError(this)" />';
    html += '</div>';
    
    resultDiv.innerHTML = html;
}

// Function to handle image load errors
function handleImageError(img) {
    var container = img.parentElement;
    container.innerHTML = '<p class="error-message">No dog found for this status code! 🐕‍🦺<br/>This status code might not have an image available.</p>';
}

// Function to set status code from button click
function setStatusCode(code) {
    document.getElementById('statusCode').value = code;
    showDog();
}

// Allow Enter key to trigger search
document.addEventListener('DOMContentLoaded', function() {
    var input = document.getElementById('statusCode');
    if (input) {
        input.addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                showDog();
            }
        });
    }
});
