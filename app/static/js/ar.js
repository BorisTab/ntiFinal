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

function getCoordinate(e) {
    let ne = rectangle.getBounds().getNorthEast();
    let sw = rectangle.getBounds().getSouthWest();
    rightUpLat = ne.lat();
    rightUpLng = ne.lng();
    leftDownLat = sw.lat();
    leftDownLng = sw.lng();

    $('#rightUp').val(rightUpLat.toFixed(3) + ';' + rightUpLng.toFixed(3));
    $('#leftBottom').val(leftDownLat.toFixed(3) + ';' + leftDownLng.toFixed(3));

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
        setTimeout(function () {
            alert('Превышен максимальный размер области');
        }, 100);
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
        window.location= '/login';
    });

    // $.mask.definitions['~']='[+-]';
    // $('#rightUp, #leftBottom').mask('~999.99; ~999.99');

    $.validator.addMethod("coordinate",
        function (val, el, args) {
        if (args) {
            let i = 0;
            let latitude = "";
            let longitude = "";
            while (val[i] !== ';') {
                if (i === val.length) {
                    return false;
                }
                latitude += val[i];
                i++;
                console.log(latitude);
            }
            i++;
            while (i < val.length) {
                longitude += val[i];
                i++;
                console.log(longitude, i, val.length);
            }
            let latVal = parseFloat(latitude).toFixed(3);
            let lngVal = parseFloat(longitude).toFixed(3);
            let latStr = "" + latVal;
            let lngStr = "" + lngVal;
            if (latStr !== latitude || lngStr !== longitude) return false;
            if (latVal >= -180 && latVal <= 180 && lngVal >= -180 && lngVal <= 180) return true;
            else return false;
        } else return false;
        });

    $('.coordinate-send').validate({
        rules: {
            right_up: {
                required: true,
                coordinate: true,
            },
            left_bottom: {
                required: true,
                coordinate: true,
            }
        },
        messages:{
            right_up:{
                required: "Поле обязательно к заполнению",
                coordinate: 'Введите координаты в формате: "число;число"'
            },
            left_bottom:{
                required: "Поле обязательно к заполнению",
                coordinate: 'Введите координаты в формате: "число;число"'
            }
        }
    });

    $(".coordinate-send").submit(function() {
        $.ajax({
            type: "POST",
            url: "",              //напишешь сюда обработчик
            data: {
                right_up: $('#rightUp').val(),
                left_bottom: $('#leftBottom').val()
            }
        }).done(function () {

        });
        return false;
    });


    ////////     UI     //////////

    $('.menu-button-open').click(function () {
        // $('.form').css('left', '100%');
        $('section').css('right', '0');
    });
    $('.menu-button-close').click(function () {
        $('.form').css('left', '0');
        $('section').css('right', '100%');
    });
    $('.map-button').click(function () {
        $('.form').css('left', '-500px');
        setTimeout(function () {
            $('.menu-mobile').css('display', 'inline-block');
        }, 1000);
    });
    $('.menu-mobile').click(function () {
        $('.menu-mobile').css('display', 'none');
        $('.form').css('left', '0');
    });

    let hideCheck = false;
    $('.hide-button').click(function () {
        if(!hideCheck) {
            $('.form').css('left', '-300px');
            $(this).css('left', '0');
            $('.arrow-block').css('transform', 'rotate(180deg)');
            hideCheck = true
        } else {
            $('.form').css('left', '0');
            $(this).css('left', '300px');
            $('.arrow-block').css('transform', 'rotate(0)');
            hideCheck = false;
        }
    });

    $('.history-cell').click(function () {
        $(this).css('background-color', '#808080')
            .siblings().css('background-color', '#0071f0');

        $('#selected-object').val($(this).data('cell-id'));                        //отсылаю Id выбранной модели
    });
});