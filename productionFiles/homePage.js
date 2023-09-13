$(document).ready(function() {
    $.ajaxSetup({
        headers: {
            'X-CSRFToken': CSRF_TOKEN
        }
    });
    const options = {
        enableHighAccuracy: true,
        timeout: 5000,
        maximumAge: 0,
    };
    
    navigator.geolocation.getCurrentPosition(success,error,options);   
})
                  
function error() {
    $('.stop-list').append('<p style="text-align: center">Unable to get nearest stops.<br>Are location services enabled?</p>')
}

function success(pos) {
    const c = pos.coords;
    console.log(pos)
    console.log(c)
    $.post('/nearby', {
        currLat : c.latitude,
        currLon : c.longitude,
    }, function(data, status) {
        console.log(data.stops)
        for (stop in data.stops) {
            var formContainer = "";
            if (data.stops[stop]['stopLetter'] == null ) {
                var stopLetter = " ";
            } else {
                var stopLetter = data.stops[stop]['stopLetter'];
            }
            
            var stopIndicator = `<div class='stop-indicator'><div id='stop-indicator-letter'>${stopLetter}</div></div>`
            var stopName = `<div class='stop-name'><h2>${ data.stops[stop]['name'] }</h2></div>`;
            var stopTopRow = `<div class='stop-top-row'>${stopIndicator}${stopName}</div>`;
            var stopWaypoint = `<div class='stop-towards'><h4>${ data.stops[stop]['waypoint'] }</h4></div>`;
            var stopRoutes = "";
            for (route in data.stops[stop]['routes']) {
                stopRoutes += ` <li class='route'>${ data.stops[stop]['routes'][route].toUpperCase() }</li>`
            }
            var formContainer = `<form id='form-${ stop }' method="post" action="/stop/${ data.stops[stop]['id'] }">
                <input type="hidden" name="csrfmiddlewaretoken" value="${CSRF_TOKEN}">
                <input type="hidden" id='name' name="name" value="${ data.stops[stop]['name'] }">
                <input type="hidden" id='stopLetter' name="stopLetter" value="${ stopLetter }">
                <input type="hidden" id='waypoint' name="waypoint" value="${ data.stops[stop]['waypoint'] }">
            </form>`
            var routeContainer = `<div class='stop-routes'><ul class='routes'>${stopRoutes}</ul></div>`
            var container = `<div class='stop' onclick="document.forms['form-${stop}'].submit()">${formContainer}${stopTopRow}${stopWaypoint}${routeContainer}</div>`;
            $('.stop-list').append(container)
        }
    }).fail(error)
}
                  