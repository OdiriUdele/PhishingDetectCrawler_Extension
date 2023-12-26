// background.js
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    console.log(request);
    // Send the URL to the Flask API
    fetch('http://127.0.0.1:5000/api/crawl_url', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({url: request.url}),
    })
    .then(response => {
        console.log(response);

        if (!response.ok) {
            console.error('Network response was not ok:', response.status, response.statusText);
            throw new Error('Network response was not ok');
        }

        return response.json();
    })
    .then(data => {
        console.error('data:', data);

        var response = { success: false, message: 'Phishing detection failed'};

        if (data.status && data.status !== "") {
            var msg = data.status;

            if (msg !== "legitimate") {
                msg = "Unsafe, phishing concerns";
                success = false
            } else {
                success = true
            }

            var finalMsg = 'Page is ' + msg;

            response = { success: success, message: finalMsg, data: data};
        }

        sendResponse(response);
    })
    .catch(error => {
        console.error('Error:', error);
        var response = { success: false, message: 'Error sending URL'};
        sendResponse(response);
    });

    // Returning true indicates that sendResponse will be called asynchronously
    return true;
});
