L.mapbox.accessToken = 'pk.eyJ1IjoiamFjcXVlcyIsImEiOiJuRm9TWGYwIn0.ndryRT8IT0U94pHV6o0yng';
// Initialize map
var map = L.mapbox.map('map', 'jacques.la14ofjk', {zoomControl: false });
// Set center and zoom
map.setView([47.6105411, -122.329726], 13);
// Create lat/lon url hash
var hash = L.hash(map);
