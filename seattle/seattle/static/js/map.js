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
    // IE: Uncaught TypeError: Cannot read property 'lat' of undefined
    $.ajax({
        url: "/ajax/",
        dataType: "json",
        data: { 'lat_cen': lat, 'lon_cen': lng},
    }).done(function(json) {
        $(".crime").children().replaceWith(json.percentages.crime);
        $(".fire").children().replaceWith(json.percentages.fire);
        $(".accidents").children().replaceWith(json.percentages.mvi);
        bulk_data = json.output;
        graph();
        console.log('You look great today.');
    });

});

