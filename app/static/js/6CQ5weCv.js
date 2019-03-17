let map;
let zoneCenter = {lat: 52.287, lng: 104.29};
var roadCoordinates;
var numberOfRoads;
var colors = [0, 0, 0, '#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff', '#00ffff'];

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: zoneCenter,
        zoom: 16,
        disableDefaultUI: true
    });
}

function makeIT(){
    var canvas = $('canvas')[0];
    var img = canvas.toDataURL('image/png');
    $('canvas').remove();

    $.ajax({
        type: "POST",
        url: "",
        data: img
    });
}

$.ajax({
    type: "POST",
    url: "",
}).done(function(data) {

    numberOfRoads = data.nGroups;
    switch (+(numberOfRoads)) {
        case 3:
            $.getJSON('../static/js/json-3person-litlecell.json', function (data) {
                var teamId = +(data.teamId);
                var Coordinates_1 = data.graphs[teamId];

                var Path_1 = new google.maps.Polyline({
                    path: Coordinates_1,
                    strokeColor: colors[3],
                    strokeOpacity: 1.0,
                    strokeWeight: 3
                });
                Path_1.setMap(map);
            });
            break;
        case 4:
            $.getJSON('../static/js/json-4person-litlecell.json', function (data) {
                var teamId = +(data.teamId);
                var Coordinates_1 = data.graphs[teamId];

                var Path_1 = new google.maps.Polyline({
                    path: Coordinates_1,
                    strokeColor: colors[4],
                    strokeOpacity: 1.0,
                    strokeWeight: 3
                });
                Path_1.setMap(map);
            });
            break;
        case 5:
            $.getJSON('../static/js/json-5person-litlecell.json', function (data) {
                var teamId = +(data.teamId);
                var Coordinates_1 = data.graphs[teamId];

                var Path_1 = new google.maps.Polyline({
                    path: Coordinates_1,
                    strokeColor: colors[5],
                    strokeOpacity: 1.0,
                    strokeWeight: 3
                });
                Path_1.setMap(map);
            });
            break;
        case 6:
            $.getJSON('../static/js/json-6person-litlecell.json', function (data) {
                var teamId = +(data.teamId);
                var Coordinates_1 = data.graphs[teamId];

                var Path_1 = new google.maps.Polyline({
                    path: Coordinates_1,
                    strokeColor: colors[6],
                    strokeOpacity: 1.0,
                    strokeWeight: 3
                });
                Path_1.setMap(map);
            });
            break;
        case 7:
            $.getJSON('../static/js/json-7person-litlecell.json', function (data) {
                var teamId = +(data.teamId);
                var Coordinates_1 = data.graphs[teamId];

                var Path_1 = new google.maps.Polyline({
                    path: Coordinates_1,
                    strokeColor: colors[7],
                    strokeOpacity: 1.0,
                    strokeWeight: 3
                });
                Path_1.setMap(map);
            });
            break;
    }

    $('body').html2canvas();
    setTimeout("makeIT()", 1000);


});