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
