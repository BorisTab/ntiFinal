let map;
let zoneCenter = {lat: 52.286066, lng: 104.294222};

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: zoneCenter,
        zoom: 13,
        disableDefaultUI: true
    });
}