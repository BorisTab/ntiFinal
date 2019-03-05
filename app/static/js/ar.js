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
        zoom: 13,
        disableDefaultUI: true
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

//Из БД вытаскиваем id эллемента, его фото и название, создаем для него блок

class ObjectsCell {
    constructor(cellId, img, name){
        this.cellId = cellId;
        this.img = img;
        this.name = name;
        this.htmlId = 'history-cell-' + this.cellId;
    }

    addObjectCell() {
        $('.history-block').append('<div class="history-cell" id="' + this.htmlId + '" data-cell-id="' + this.cellId +'">\n' +
            '            <img id="cell-photo" src="' + this.img + '" alt="">\n' +
            '            <p id="name-of-cell">' + this.name + '</p>\n' +
            '        </div>');
    }
}

$('document').ready(function () {

    $('.exit-button').click(function () {
        window.location= '/ar/login';
    });

    $.mask.definitions['~']='[+-]';
    $('#right_up, #left_bottom').mask('~999.99; ~999.99');

    $(".coordinate-send").submit(function() {
        $('#right_up_lat').val(rightUpLat);
        $('#right_up_lng').val(rightUpLng);
        $('#left_bottom_lat').val(leftDownLat);
        $('#left_bottom_lng').val(leftDownLng);

        let th = $(this);
        $.ajax({
            type: "POST",
            url: "",              //напишешь сюда обработчик
            data: th.serialize(),
            success: function() {
                $('.choose-zone-title').text('Вы может отправить новую зону');
                alert('Зона отправлена');
                setTimeout(function() {
                    th.trigger("reset");
                }, 100);
            },
            error: function (xhr, ajaxOptions, thrownError) {
                alert(xhr.status);
                alert(thrownError);
            }
        });
        return false;
    });


    ////////     UI     //////////

    $('.menu-button-close').click(function () {
        $('.form').css('left', '-320px');
        setTimeout(function () {
            $('.menu-button-open').css('display', 'inline-block');
        }, 1500);
    });
    $('.menu-button-open').click(function () {
        $('.form').css('left', '0');
        $(this).css('display', 'none');
    });

    $('.history-cell').click(function () {
        $(this).css('background-color', '#808080')
            .siblings().css('background-color', '#fff');

        $('#selected-object').val($(this).data('cell-id'));                        //отсылаю Id выбранной модели
    });
});