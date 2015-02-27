L.mapbox.accessToken = 'pk.eyJ1IjoiamFjcXVlcyIsImEiOiJuRm9TWGYwIn0.ndryRT8IT0U94pHV6o0yng';

var sw = L.latLng(47.4849, -122.4347),
    ne = L.latLng(47.7414, -122.2406),
    bounds = L.latLngBounds(sw, ne);

// Initialize map
var map = L.mapbox.map('map', 'jacques.la14ofjk', {
    center: [47.6105411, -122.329726],
    zoom: 13,
    attributionControl: false,
    maxBounds: bounds,
    maxZoom: 17,
    minZoom: 12
});


// Disable scrollwheel zoom
map.scrollWheelZoom.disable();

function graph() {
    var w = 960,
        h = 500,
        p = [50, 40, 40, 20],
        x = d3.scale.ordinal().rangeRoundBands([0, w - p[1] - p[3]]),
        y = d3.scale.linear().range([0, h - p[0] - p[2]]),
        z = d3.scale.ordinal().range(["#FDE668", "#FFBE1A", "#E09200"])
        yx = d3.scale.linear().range([0, h - p[0] - p[2]]),
        format = d3.time.format("%b %Y");

    var tip = d3.tip()
        .attr('class', 'd3-tip')
        .offset([-10, 0])
        .html(function(d) {
            return "<span>" + d.y + "</span>";
        })

    var svg = d3.select(".graph").append("svg:svg")
        .attr("width", w)
        .attr("height", h)
        .append("svg:g")
        .attr("transform", "translate(" + p[3] + "," + (h - p[2]) + ")");

    svg.call(tip);

    // Transpose the data into layers by type.
    var incidents = d3.layout.stack()(["fire", "mvi", "crime"].map(function(incident) {
        return data.map(function(d) {
          return {x: new Date(d.month), y: +d[incident]};
        });
    }));

    // Compute the x-domain (by date) and y-domain (by top).
    x.domain(incidents[0].map(function(d) { return d.x; }));
    y.domain([0, d3.max(incidents[incidents.length - 1], function(d) { return d.y0 + d.y; })]);
    yx.domain([d3.max(incidents[incidents.length - 1], function(d) { return d.y0 + d.y; }), 0]);

    // Define the axes
    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom")
        .ticks(5);

    // svg.append("g")
    //     .attr("class", "x axis")
    //     .attr("transform", "translate(" + 0 + "," + h - p[2] + ")")
    //     .call(xAxis)
    //     .selectAll("text")
    //     .attr("y", 0)
    //     .attr("x", 9)
    //     .attr("dy", ".35em")
    //     .attr("transform", "rotate(90)")
    //     .style("text-anchor", "start")
    //     .text(format);

    var yAxis = d3.svg.axis()
        .scale(yx)
        .orient("left")
        .ticks(5);

    // svg.append("g")
    //     .attr("class", "y axis")
    //     .attr("transform", "translate(" + (p[1] + p[3] - 12) + "," + -(h - p[2] - p[0]) + ")")
    //     .call(yAxis)
    //     .selectAll("text")
    //     .style("text-anchor", "start");

    // Add a group for each cause.
    var incident = svg.selectAll("g.incident")
        .data(incidents)
        .enter().append("svg:g")
        .attr("class", "incident")
        .style("fill", function(d, i) { return z(i); });

    // Add a rect for each date.
    var rect = incident.selectAll("rect")
        .data(Object)
        .enter().append("svg:rect")
        .attr("x", function(d) { return x(d.x); })
        .attr("y", function(d) { return -y(d.y0) - y(d.y); })
        .attr("height", function(d) { return y(d.y); })
        .attr("width", x.rangeBand())
        .on('mouseover', tip.show)
        .on('mouseout', tip.hide);

}

function groupedbar() {
    var margin = {top: 20, right: 20, bottom: 30, left: 40},
        width = 960 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;

    var x0 = d3.scale.ordinal()
        .rangeRoundBands([0, width], .1);

    var x1 = d3.scale.ordinal();

    var y = d3.scale.linear()
        .range([height, 0]);

    var color = d3.scale.ordinal()
        .range(["#98abc5", "#8a89a6", "#7b6888", "#6b486b", "#a05d56", "#d0743c", "#ff8c00"]);

    var xAxis = d3.svg.axis()
        .scale(x0)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left")
        .tickFormat(d3.format(".2s"));

    var svg = d3.select(".groupedbar").append("svg:svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var incidentNames = d3.keys(compare_data[0]).filter(function(key) { return key !== "types"; });
    
    compare_data.forEach(function(d) {
        d.incidents = incidentNames.map(function(name) { return {name: name, value: +d[name]}; });
    });


    x0.domain(compare_data.map(function(d) { return d.types; }));
    x1.domain(incidentNames).rangeRoundBands([0, x0.rangeBand()]);
    y.domain([0, d3.max(compare_data, function(d) { return d3.max(d.incidents, function(d) { return d.value; }); })]);

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
        .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Incidents/Year");

    var types = svg.selectAll(".types")
        .data(compare_data)
        .enter().append("g")
        .attr("class", "g")
        .attr("transform", function(d) { return "translate(" + x0(d.types) + ",0)"; });

    types.selectAll("rect")
        .data(function(d) { return d.incidents; })
        .enter().append("rect")
        .attr("width", x1.rangeBand())
        .attr("x", function(d) { return x1(d.name); })
        .attr("y", function(d) { return y(d.value); })
        .attr("height", function(d) { return height - y(d.value); })
        .style("fill", function(d) { return color(d.name); });
}

window.onload = graph();
window.onload = groupedbar();

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
        // Update site contents with new data
        $(".crime").children().replaceWith(json.percentages.Crime);
        $(".fire").children().replaceWith(json.percentages.Fire);
        $(".accidents").children().replaceWith(json.percentages.MVI);
        $(".crime_count").contents().replaceWith(json.counts.Crime);
        $(".fire_count").contents().replaceWith(json.counts.Fire);
        $(".accidents_count").contents().replaceWith(json.counts.MVI);
        $(".count").contents().replaceWith(json.count);
        $(".lat").contents().replaceWith(json.lat);
        $(".lon").contents().replaceWith(json.lon);
        $(".neigh").contents().replaceWith(json.neigh);

        
        // Update graph
        compare_data = json.compare
        data = json.output;
        if (json.output.length === 0) {
            $(".graph").children().replaceWith('No data available.')
            $(".groupedbar").children().replaceWith('No data available.')
        } else {
            $(".graph").contents().remove();
            $(".groupedbar").contents().remove();
            graph();
        }


    });
});

