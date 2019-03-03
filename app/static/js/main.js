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
    document.getElementsByClassName('mobile-button')[0].classList.remove('change');
    document.getElementsByClassName('vertical-menu')[0].style.display = 'none';
}
setInterval(function () {
    if(window.innerWidth >= 860) hide();
}, 200);

function portfolioChange() {
    let portfolioHeight = $('.portfolio').height();
    $('#section-2').css('height', portfolioHeight + 250);
}
window.onresize = portfolioChange;


$('document').ready(function () {
    portfolioChange();

    function smallMenu() {
        if( $(window).scrollTop() !== 0) {
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
            scrollTop: $("#section-2").offset().top + 1
        }, 800);
    });

    $('.home-button').click(function () {
        $('templates, body').animate({
            scrollTop: $('#section-1').offset().top
        }, 800);
    });

    $(".form").submit(function() {
        let th = $(this);
        $.ajax({
            type: "POST",
            url: "",
            data: th.serialize()
        }).done(function() {
            alert("Спасибо!");
            setTimeout(function() {
                th.trigger("reset");
            }, 1000);
        });
        return false;
    });

    $('.rus, .vertical-menu-rus').click(function () {
        window.location = '/';
    });
    $('.eng, .vertical-menu-eng').click(function () {
        window.location = '/en';
    });

    $('#section-2 .column').mouseover(function () {
        $(this).addClass('active-column').siblings().removeClass('active-column');
    });


    let lastId,
        topMenu = $('.menu'),
        // All list items
        menuItems = topMenu.find('a'),
        // Anchors corresponding to menu items
        scrollItems = menuItems.map(function(){
            let item = $($(this).attr("href"));
            if (item.length) return item;
        });
    menuItems.click(function(e){
        let href = $(this).attr("href"),
            offsetTop = href === "#" ? 0 : $(href).offset().top + 1;
        $('templates, body').stop().animate({
            scrollTop: offsetTop
        }, 800);
        e.preventDefault();
    });
    $(window).scroll(function(){
        // Get container scroll position
        let fromTop = $(this).scrollTop();

        // Get id of current scroll item
        let cur = scrollItems.map(function(){
            if ($(this).offset().top < fromTop)
                return this;
        });
        // Get the id of the current element
        cur = cur[cur.length-1];
        let id = cur && cur.length ? cur[0].id : "";

        if (lastId !== id) {
            lastId = id;
            // Set/remove active class
            menuItems
                .parent().removeClass("active-button")
                .end().filter("[href='#"+id+"']").parent().addClass("active-button");
        }
    });
});