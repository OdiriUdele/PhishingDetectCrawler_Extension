displayNotice();

function onReady() {
    var currentUrl = window.location.href;

    setTimeout(function() {
        chrome.runtime.sendMessage({url: currentUrl}, function(response) {
            console.log("Background response recieved ", response)
            display(response)
        })
    }, 5000);

    chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
        console.log('Content script received message:', request);
        if (request.action === 'fromPopup') {
            console.log('Content script received message from popup:', request.data);
    
            //makeBackgroundCall(request.data);
            // Process the message and send a response if needed
            sendResponse({ success: true, message: 'Content script received the message' });
            chrome.runtime.sendMessage({url: currentUrl}, function(response) {
                console.log("Background2 response recieved ", response)
                display(response)
            })
        }
    
    });
}

function hideDisplayNotice() {
    responseContainer = document.getElementById('extension-notice-response-container');
    if (responseContainer) {
        responseContainer.style.display = 'none';
    }
}

function displayNotice(response) {
    var responseContainer = document.createElement('div');
    responseContainer.id = 'extension-notice-response-container';
    document.body.appendChild(responseContainer);

    var responseClass = 'response-notice-popup';
    responseContainer.innerHTML = `
            <div class="${responseClass}">
                <span>Page is being scanned for phishing</span>
                <button id="closeNoticeButton">X</button>
            </div>`;

    var closeButton = responseContainer.querySelector('#closeNoticeButton');
  
    if (closeButton) {
        closeButton.style.border = 'none';
        closeButton.style.backgroundColor = 'transparent';
        closeButton.style.color = '#000';
        closeButton.style.fontSize = '16px';
        closeButton.style.cursor = 'pointer';

        closeButton.addEventListener('click', function() {
            responseContainer.style.display = 'none';
        });
    }

    // Hide the container after 3 seconds
    setTimeout(function() {
        responseContainer.style.display = 'none';
    }, 6000);
}


function display(response) {
    hideDisplayNotice();
    var responseContainer = document.createElement('div');
    responseContainer.id = 'extension-response-container';
    document.body.appendChild(responseContainer);

    var responseClass = response.success ? 'response-popup' : 'error-response-popup';
    responseContainer.innerHTML = `
            <div class="${responseClass}">
                <span>${response.message}</span>
                <button id="closeButton">X</button>
            </div>`;

    var closeButton = responseContainer.querySelector('#closeButton');
  
    if (closeButton) {
        closeButton.style.border = 'none';
        closeButton.style.backgroundColor = 'transparent';
        closeButton.style.color = '#000';
        closeButton.style.fontSize = '16px';
        closeButton.style.cursor = 'pointer';

        closeButton.addEventListener('click', function() {
            responseContainer.style.display = 'none';
        });
    }
}


if (document.readyState !== "loading") {
    onReady(); // Or setTimeout(onReady, 0); if you want it consistently async
} else {
    document.addEventListener("DOMContentLoaded", onReady);
}