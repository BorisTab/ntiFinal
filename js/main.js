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
//window.onresize = hide;



$('document').ready(function () {
    function smallMenu() {
        if( $('html').scrollTop() !== 0) {
            $('header').animate({
                height: '60px'
            }, 200);
            $('.home-button').css('transform', 'scale(0.75)');
            $('.vertical-menu').css('top', '60px');
        } else {
            $('header').animate({
                height: '100px',
            }, 200);
            $('.home-button').css('transform', 'scale(1)');
            $('.vertical-menu').css('top', '100px');
        }
    }
    setInterval(smallMenu, 210);

    $('.logo').mouseover(function () {
        $('.logo').addClass('logo-change');
    });

    $('.arrow-down').click(function() {
        $('html, body').animate({
            scrollTop: $("#section-2").offset().top
        }, 800);
    });

    $('.home-button').click(function () {
        $('html, body').animate({
            scrollTop: $('#section-1').offset().top
        }, 800);
    });

    $('.portfolio-button').click(function () {
        $('html, body').animate({
            scrollTop: $('#section-2').offset().top
        }, 1000);
    });

    $('.about-button').click(function () {
        $('html, body').animate({
            scrollTop: $('#section-3').offset().top
        }, 1000);
    });

    $('.contact-button').click(function () {
        $('html, body').animate({
            scrollTop: $('#section-5').offset().top
        }, 1000);
    });

    let slideWidth = $('#section-4').innerWidth();
    let sliderTimer;
    let numberOfSlides = 3;

    $('.viewport').css({
        'width': slideWidth
    });
    $('.slide').css({
        'width': slideWidth
    });
    /*setInterval(function () {
        let slideWidth = $('#section-4').innerWidth();
        $('.viewport').css({
            'width': slideWidth
        });
        $('.slide').css({
            'width': slideWidth
        });
    }, 1);*/

    $(function(){
        $('.slide-wrapper').width($('.slide-wrapper').children().length * slideWidth);
        sliderTimer=setInterval(nextSlide,5000);
        $('.slide-forward').click(function () {
            clearInterval(sliderTimer);
            nextSlide();
            sliderTimer = setInterval(nextSlide, 5000);
        });
        $('.slide-back').click(function () {
            clearInterval(sliderTimer);
            previousSlide();
            sliderTimer = setInterval(nextSlide, 5000);
        });
    });

    function nextSlide(){
        let currentSlide=parseInt($('.slide-wrapper').data('current'));
        currentSlide++;
        if(currentSlide >= numberOfSlides) {
            currentSlide = 0;
        }
        $('.slide-wrapper').animate({left: -currentSlide*slideWidth},1500).data('current',currentSlide);
    }

    function previousSlide() {
        let currentSlide=parseInt($('.slide-wrapper').data('current'));
        currentSlide--;
        if(currentSlide < 0) {
            currentSlide = numberOfSlides - 1;
        }
        $('.slide-wrapper').animate({left: -currentSlide*slideWidth},1500).data('current',currentSlide);
    }

    $(".form").submit(function() {
        let th = $(this);
        $.ajax({
            type: "POST",
            url: "../back/send.php",
            data: th.serialize()
        }).done(function() {
            alert("Спасибо!");
            setTimeout(function() {
                // Done Functions
                th.trigger("reset");
            }, 1000);
        });
        return false;
    });

    $('.rus').click(function () {
        window.location = 'index.html';
    });
    $('.eng').click(function () {
        window.location = 'index-eng.html';
    });

    $('html, body').scroll(function () {
        $('.menu-button:after').css('width', '95%');
    })
});