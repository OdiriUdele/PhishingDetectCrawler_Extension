document.addEventListener('DOMContentLoaded', function() {
    var sendButton = document.getElementById('sendButton');

    sendButton.addEventListener('click', function() {
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            var currentTab = tabs[0];
            var currentUrl = currentTab.url;

            chrome.tabs.sendMessage(currentTab.id, { action: 'fromPopup', data: currentUrl }, function(response) {
                console.log(response);
            });
        });
    });
});