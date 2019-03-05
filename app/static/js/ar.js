let rectangle;
let map;
let rightUpLat;
let rightUpLng;
let leftDownLat;
let leftDownLng;
let maxLength = 0.5;
let maxWidth = 0.5;


function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 55.73, lng: 37.66},
        zoom: 13
    });

    let bounds = {
        north: 55.75,
        south: 55.72,
        east: 37.70,
        west: 37.65
    };

    // Define the rectangle and set its editable property to true.
    rectangle = new google.maps.Rectangle({
        bounds: bounds,
        editable: true,
        draggable: true
    });

    rectangle.setMap(map);

    // Add an event listener on the rectangle.
    getCoordinate();
    rectangle.addListener('bounds_changed', getCoordinate);
}
// Show the new coordinates for the rectangle in an info window.

function getCoordinate(event) {
    let ne = rectangle.getBounds().getNorthEast();
    let sw = rectangle.getBounds().getSouthWest();

    rightUpLat = ne.lat();
    rightUpLng = ne.lng();
    leftDownLat = sw.lat();
    leftDownLng = sw.lng();

    let rectangleLength = rightUpLng - leftDownLng;
    let rectangleWidth = rightUpLat - leftDownLat;
    let check = false;

    if (rectangleWidth > maxWidth) {

        let newBounds = {
            north: rightUpLat,
            south: rightUpLat - maxWidth + 0.02,
            east: rightUpLng,
            west: leftDownLng
        };

        rectangle.setBounds(newBounds);
        check = true;
    }

    if (rectangleLength > maxLength) {

        let newBounds = {
            north: rightUpLat,
            south: leftDownLat,
            east: rightUpLng,
            west: rightUpLng - maxLength + 0.02
        };

        rectangle.setBounds(newBounds);
        check = true;
    }


    if (check) {
        alert('Превышен максимальный размер области');
    }
}

function preloader(){
    $(() => {
        let preload =$('.preloader');
        setInterval(() => {
            preload.css('opacity', 0);
            setInterval(
                () => preload.remove(),
                parseInt(preload.css('--duration'))*1000
            );

        },1000);
    });
}

$('document').ready(function () {
    $(".coordinate-send").submit(function() {
        $('#right-up-lat').val(rightUpLat);
        $('#right-up-lng').val(rightUpLng);
        $('#left-bottom-lat').val(leftDownLat);
        $('#left-bottom-lng').val(leftDownLng);

        let th = $(this);
        $.ajax({
            type: "POST",
            url: "/ar/get_model",              //напишешь сюда обработчик
            data: th.serialize()
        }).done(function() {
            $('.choose-zone-title').text('Вы может отправить новую зону');
            alert('Зона отправлена');
            setTimeout(function() {
                th.trigger("reset");
            }, 100);
        });
        return false;
    });
});
