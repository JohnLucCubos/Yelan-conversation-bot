// introduction
document.getElementById("DialogueBox").innerHTML = "Yelan: I'm listening";

var xhr = null;
getXmlHttpRequestObject = function () {
    if (!xhr) {
        // Create a new XMLHttpRequest object 
        xhr = new XMLHttpRequest();
    }
    return xhr;
};
function dataCallback() {
    // Check response is ready or not
    if (xhr.readyState == 4 && xhr.status == 200) {
        console.log("User data received!");
        dataDiv = document.getElementById('DialogueBox');
        // Set current data text
        dataDiv.innerHTML = xhr.responseText;
    }
}
function getUsers() {
    console.log("Get users...");
    xhr = getXmlHttpRequestObject();
    xhr.onreadystatechange = dataCallback;
    // asynchronous requests
    xhr.open("GET", "http://localhost:6969/respond", true);
    // Send the request over the network
    xhr.send(null);
}

function sendDataCallback() {
    // Check response is ready or not
    if (xhr.readyState == 4 && xhr.status == 201) {
        console.log("Data creation response received!");
        dataDiv = document.getElementById('DialogueBox');
        // Set current data text
        dataDiv.innerHTML = xhr.responseText;
    }
}
function sendData() {
    dataToSend = document.getElementById('UserInput').value;
    if (!dataToSend) {
        console.log("Data is empty.");
        return;
    }
    console.log("Sending data: " + dataToSend);
    xhr = getXmlHttpRequestObject();
    xhr.onreadystatechange = sendDataCallback;
    // asynchronous requests
    xhr.open("POST", "http://localhost:6969/respond", true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    // Send the request over the network
    xhr.send(JSON.stringify({"data": dataToSend}));
}