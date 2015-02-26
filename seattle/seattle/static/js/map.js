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

    $.ajax('/', {
        type: 'POST',
        data: center
    });
    console.log(center);

});
