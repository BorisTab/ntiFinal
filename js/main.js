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

function smallMenu() {
    if( $('html').scrollTop() !== 0) {
        $('header').animate({
            height: '60px',
        }, 200);
        $('.home-button').css({
            '--height': '40px',
            '--width': '180px'
        });
    } else {
        $('header').animate({
            height: '100px',
        }, 200);
        $('.home-button').css({
            '--height': '70px',
            '--width': '210px'
        });
    }
}
setInterval(smallMenu, 210);

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
