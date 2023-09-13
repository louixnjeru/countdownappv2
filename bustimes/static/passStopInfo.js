function sendStopInfo(stopInfo) {
    console.log(CSRF_TOKEN)
    var stopForm = new FormData();
    stopForm.append('name', stopInfo['name']);
    stopForm.append('stopLetter', stopInfo['stopLetter']);
    stopForm.append('waypoint', stopInfo['waypoint']);
    console.log(stopForm.get('name'))
    
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/stop/'+stopInfo['id']);
    xhr.setRequestHeader('X-CSRFToken', CSRF_TOKEN);
    xhr.send(stopForm);
}

function getVehicleInfo(stopId) {
    
}