L.mapbox.accessToken = 'pk.eyJ1IjoiamFjcXVlcyIsImEiOiJuRm9TWGYwIn0.ndryRT8IT0U94pHV6o0yng';

var sw = L.latLng(47.4849, -122.4347),
    ne = L.latLng(47.7414, -122.2406),
    bounds = L.latLngBounds(sw, ne);

// Initialize map
var map = L.mapbox.map('map', 'jacques.la14ofjk', {
    center: [47.6105411, -122.329726],
    zoom: 13,
    zoomControl: false,
    attributionControl: false,
    maxBounds: bounds,
    maxZoom: 17,
    minZoom: 12
});

function graph() {
    try {
        dates = [];
        for (i = 0; i < bulk_data[0].length; i++) {
            dates.push(new Date(bulk_data[0][i]*1000*60*60*24));
        }


        data = [];
        for (i = 0; i < bulk_data[0].length; ++i) {
          data.push({
            'month': dates[i],
            'fire': bulk_data[1][0][i],
            'mvi': bulk_data[1][1][i],
            'crime': bulk_data[1][2][i]
          });
        }

        var w = 960,
            h = 500,
            p = [50, 40, 40, 20],
            x = d3.scale.ordinal().rangeRoundBands([0, w - p[1] - p[3]]),
            y = d3.scale.linear().range([0, h - p[0] - p[2]]),
            z = d3.scale.ordinal().range(["lightpink", "darkgray", "lightblue"])
            yx = d3.scale.linear().range([0, h - p[0] - p[2]]),
        // parse = d3.time.format("%m/%Y").parse,
            format = d3.time.format("%b %Y");

        var svg = d3.select(".graph").append("svg:svg")
            .attr("width", w)
            .attr("height", h)
            .append("svg:g")
            .attr("transform", "translate(" + p[3] + "," + (h - p[2]) + ")");

        // Transpose the data into layers by type.
        var incidents = d3.layout.stack()(["fire", "mvi", "crime"].map(function(incident) {
            return data.map(function(d) {
              return {x: d.month, y: +d[incident]};
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

        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(" + 0 + "," + h - p[2] + ")")
            .call(xAxis)
            .selectAll("text")
            .attr("y", 0)
            .attr("x", 9)
            .attr("dy", ".35em")
            .attr("transform", "rotate(90)")
            .style("text-anchor", "start")
            .text(format);

        var yAxis = d3.svg.axis()
            .scale(yx)
            .orient("left")
            .ticks(5);

        svg.append("g")
            .attr("class", "y axis")
            .attr("transform", "translate(" + (p[1] + p[3] - 12) + "," + -(h - p[2] - p[0]) + ")")
            .call(yAxis)
            .selectAll("text")
            .style("text-anchor", "start");

        // Add a group for each cause.
        var incident = svg.selectAll("g.incident")
            .data(incidents)
            .enter().append("svg:g")
            .attr("class", "incident")
            .style("fill", function(d, i) { return z(i); })
            .style("stroke", function(d, i) { return d3.rgb(z(i)).darker(); });

        // Add a rect for each date.
        var rect = incident.selectAll("rect")
            .data(Object)
            .enter().append("svg:rect")
            .attr("x", function(d) { return x(d.x); })
            .attr("y", function(d) { return -y(d.y0) - y(d.y); })
            .attr("height", function(d) { return y(d.y); })
            .attr("width", x.rangeBand());

        var legend_x = (w - p[1]*6),
            legend_y = 4*h/5;

        svg.append("text")
            .attr("transform", "translate(" + legend_x + "," + -legend_y + ")")
            .attr("dy", ".35em")
            .attr("text-anchor", "start")
            .style("fill", "lightpink")
            .text("Fire");

        svg.append("text")
            .attr("transform", "translate(" + legend_x + "," + -(legend_y + 20) + ")")
            .attr("dy", ".35em")
            .attr("text-anchor", "start")
            .style("fill", "darkgray")
            .text("Motor Vehicle Incident");

        svg.append("text")
            .attr("transform", "translate(" + legend_x + "," + -(legend_y + 40) + ")")
            .attr("dy", ".35em")
            .attr("text-anchor", "start")
            .style("fill", "lightblue")
            .text("Crime");


        incident.selectAll("rect")
        .on("mouseover", function(d){
            var xPos = parseFloat(d3.select(this).attr("x"));
            var yPos = parseFloat(d3.select(this).attr("y"));
            var height = parseFloat(d3.select(this).attr("height"))
            var coordinatesMouse = d3.mouse(this);
            var xMouse = coordinatesMouse[0];
            var yMouse = coordinatesMouse[1];

            d3.select(this)
                .attr("stroke","blue")
                .attr("stroke-width",0.8)
            svg.append("text")
                .attr("x",xMouse)
                .attr("y",yMouse)
                .attr("class","tooltip")
                .text(d.y);
        })
        .on("mouseout",function(){
            svg.select(".tooltip").remove();
            d3.select(this).attr("stroke","pink").attr("stroke-width",0.2);
        })
    }
    catch(err) {
        $(".graph").replaceWith('No data available.')
    }
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
    }).done(function(json) {
        $(".crime").children().replaceWith(json.percentages.crime);
        $(".fire").children().replaceWith(json.percentages.fire);
        $(".accidents").children().replaceWith(json.percentages.mvi);
        bulk_data = json.output;
        $(".graph").children().remove();
        graph();
    });
});

