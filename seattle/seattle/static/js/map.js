L.mapbox.accessToken = 'pk.eyJ1IjoiamFjcXVlcyIsImEiOiJuRm9TWGYwIn0.ndryRT8IT0U94pHV6o0yng';

// Initialize map
var map = L.mapbox.map('map', 'jacques.la14ofjk', {
    center: [47.6105411, -122.329726],
    zoom: 13,
    zoomControl: false,
    attributionControl: false
});

// Graph script


function graph() {
    var margin = {top: 50, right: 40, bottom: 30, left: 50},
        width = 960 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;

    // if (bulk_data.length === 0){
    //     bulk_data = {{output}};
    // };
    // var vals = [bulk_data[0], bulk_data[1][0]]

    dates = [];
    for (i = 0; i < bulk_data[0].length; i++) {
        dates.push(new Date(bulk_data[0][i]*1000*60*60*24));
    };

    data = []
    for (i = 0; i < bulk_data[0].length; ++i) {
      data.push({
        'month': dates[i],
        'fire': bulk_data[1][0][i],
        'mvi': bulk_data[1][1][i],
        'crime': bulk_data[1][2][i]
      });
    }

    // Set the ranges
    var x = d3.time.scale()
        .range([0, width]);


    var y = d3.scale.linear()
        .range([height, 0]);

    // Define the axes
    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom")
        .ticks(5);

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left")
        .ticks(5)

    // Define the lines
    var fireline = d3.svg.line()
        .interpolate("basis")
        .x(function(d) { return x(d.month); })
        .y(function(d) { return y(d.fire); });

    // Define the lines
    var mviline = d3.svg.line()
        .interpolate("basis")
        .x(function(d) { return x(d.month); })
        .y(function(d) { return y(d.mvi); });

    // Define the lines
    var crimeline = d3.svg.line()
        .interpolate("basis")
        .x(function(d) { return x(d.month); })
        .y(function(d) { return y(d.crime); });


    // Adds the svg canvas
    var svg = d3.select(".graph")
        .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
        .append("g")
            .attr("transform",
                  "translate(" + margin.left + "," + margin.top + ")");

    // Define the focus for the tooltip
    var focus = svg.append("g")
        .style("display", "none");

    // Scale the range of the data
    x.domain(d3.extent(data, function(d) { return d.month; }));
    y.domain([0, d3.max(data, function(d) { return d.fire; })]);

    // Add the line paths.
    svg.append("path")
        .attr("class", "line")
        .style("stroke", "red")
        .attr("d", fireline(data));

    svg.append("path")
        .attr("class", "line")
        .style("stroke", "blue")
        .attr("d", mviline(data));

    svg.append("path")
        .attr("class", "line")
        .style("stroke", "green")
        .attr("d", crimeline(data));

    svg.append("text")
    .attr("transform", "translate(" + (width/5) + "," + (height/8) + ")")
    .attr("dy", ".35em")
    .attr("text-anchor", "start")
    .style("fill", "red")
    .text("Fire");

    svg.append("text")
    .attr("transform", "translate(" + (1.75*width/4) + "," + (height/8) + ")")
    .attr("dy", ".35em")
    .attr("text-anchor", "start")
    .style("fill", "blue")
    .text("Motor Vehicle Incident");

    svg.append("text")
    .attr("transform", "translate(" + (4*width/5) + "," + (height/8) + ")")
    .attr("dy", ".35em")
    .attr("text-anchor", "start")
    .style("fill", "green")
    .text("Crime");

    // Add the X Axis
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    // Add the Y Axis
    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
        .append("text")
        .attr("transform", "translate(" + width/6 + "," + -height/8 + ")")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Incidents Per Month");
};
window.onload = graph();

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
        // success: graph()
    }).done(function(json) {
        $(".crime").children().replaceWith(json.percentages.crime);
        $(".fire").children().replaceWith(json.percentages.fire);
        $(".accidents").children().replaceWith(json.percentages.mvi);
        bulk_data = json.output;
        $(".graph").children().remove()
        graph();
        console.log('You look great today.');
    });

});

