function menu(x) {
    x.classList.toggle('change');
}

function show(){
    let verticalMenu = document.getElementsByClassName('vertical-menu')[0];
    if (verticalMenu.style.display === 'block'){
        verticalMenu.style.display = 'none';
    } else {
        verticalMenu.style.display = 'block';
    }
}

function hide() {
    if (window.innerWidth >= 860) {
        document.getElementsByClassName('mobile-button')[0].classList.remove('change');
        document.getElementsByClassName('vertical-menu')[0].style.display = 'none';
    }
}

window.onresize = hide;

$('document').ready(function () {
    $('.logo').mouseover(function () {
        $('.logo').addClass('logo-change');
    });

    $('.arrow-down').click(function() {
        $('html, body').animate({
            scrollTop: $("#section-2").offset().top
        }, 800);
    });

    $('.portfolio-button').click(function () {
        $('html, body').animate({
            scrollTop: $('#section-2').offset().top
        }, 800);
    });

    $('.about-button').click(function () {
        $('html, body').animate({
            scrollTop: $('#section-3').offset().top
        }, 800);
    });

    $('.home-button').click(function () {
        $('html, body').animate({
            scrollTop: $('#section-1').offset().top
        }, 800);
    });
});
