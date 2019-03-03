$(function() {
    let flag = true;
    $('.switch-button').on('click', function (e) {
        e.preventDefault();

        if(flag){
            console.log('cac');
            flag = false;
            $('.register').show('fast');
            $('.login').hide();
        } else {
            flag = true;
            $('.login').show('fast');
            $('.register').hide();
        }
    });
});

/*
$(function() {
  $('button.switch-button.secondary.login').bind('click', function() {
       $.getJSON('/ar/register',
           function(data) {
               window.location.replace = '/ar/register'
       });
       return true;
    });
});

$(function() {

    $('button.switch-button.secondary.register').bind('click', function() {
        $.getJSON('/ar/login',
            function(data) {
                window.location.replace = '/ar/login'
        });
        return true;
    });
 });*/