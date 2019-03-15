let map;
let zoneCenter = {lat: 52.286066, lng: 104.294222};
let position;
var group_amount;

$.ajax({
    type : 'POST',
    url : '/ar/get/amount'
})
    .done(function(data) {
        group_amount = +(data.amount);
        switch (group_amount) {
            case 3: $.getJSON('../static/js/json-3person-litlecell.json', function (data) {
                        position[1] = data.graph_1.coords;
                        position[2] = data.graph_1.coords;
                        position[3] = data.graph_1.coords;
                    });
        }

        function initMap() {
            map = new google.maps.Map(document.getElementById('map'), {
                center: zoneCenter,
                zoom: 13,
                disableDefaultUI: true
            });

            for (let i = 1; i < group_amount + 1; i++){
                var marker = new google.maps.Marker({
                    position: position[i],
                    map: map,
                    title: 'Hello World!'
                });
            }

            //map.setOptions({styles: styles['hide']});
        }
    });



