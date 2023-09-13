function getVehicleInfo(bus, currentStop, routeDestination) {
    $.ajaxSetup({
        headers:
            { 'X-CSRFToken': CSRF_TOKEN }
        })

    $.post('/vehicle', {
        vehicleId: bus,
        destination: routeDestination,
    }, function(data, status) {
        $('.main').css('overflow-x','hidden');
        $('#route-info').empty();
        $('#route-stops').empty();
        if (data.stops.length > 0) {
            var $routeInfo = `<h1 class='route-info-text'><span id='route-info-num'>${data.stops[0].route}</span> towards ${routeDestination}</h1>`;
            var stopFound = false;
            $('#route-info').append($routeInfo);
            $('#route-stops').append('<table id="route-stops-table"></table>')
            for (stop in data.stops) {
                var stopLetter = ""
                if (data.stops[stop].stopLetter != 'null') {
                    stopLetter = data.stops[stop].stopLetter
                }
                var newStop = `<td id="journey-stop-letter"><div id="stop-indicator-letter">${stopLetter}</div></td><td id="journey-stop-name">${data.stops[stop].name}</td><td id="journey-stop-time">${data.stops[stop].due}</td>`
                if (currentStop == data.stops[stop].id) {
                    var newTableRow = `<tr class='current-stop'>${newStop}</tr>`
                    stopFound = true
                } else if (stopFound == false) {
                    var newTableRow = `<tr class='before'>${newStop}</tr>`
                } else {
                    var newTableRow = `<tr class='after'>${newStop}</tr>`
                }
                
                $('#route-stops-table').append(newTableRow)
            }
            if (stopFound == false) {
                $('#route-stops').prepend('<h3>This bus has departed, please refresh the page.</h3>')
            }
        } else {
            $('#route-info').append('<p></p>').text("Sorry, journey information is not available for this departure.");
        }
        
        $('#overlay').show();
    })

}

$(document).ready(function() {
    $('.close-overlay').click(function() {
        $('.main').css('overflow-y','scroll');
        $('#overlay').hide();
    })
    

})