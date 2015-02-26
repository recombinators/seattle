L.mapbox.accessToken = 'pk.eyJ1IjoiamFjcXVlcyIsImEiOiJuRm9TWGYwIn0.ndryRT8IT0U94pHV6o0yng';

// Initialize map
var map = L.mapbox.map('map', 'jacques.la14ofjk', {
    center: [47.6105411, -122.329726],
    zoom: 13,
    zoomControl: false,
    attributionControl: false
});

// On move, recalculate center
map.on('moveend', function(e) {
    var center = map.getCenter();
    var lat = center.lat;
    var lng = center.lng;
    console.log(lat, lng);

    // With the AJAX request, we're only able to move once before this errors.
    // IE: Uncaught TypeError: Cannot read property 'lat' of undefined
    $.ajax({
        url: '/ajax/' + lat + '/' + lng,
        type: 'POST', // Unsure if necessary. Would GET work?
        data: center,
        dataType: 'json'
    }).done(function(json) {
        console.log('You look great today.');
    });

});
