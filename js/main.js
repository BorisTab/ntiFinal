function menu(x) {
    x.classList.toggle("change");

    let verticalMenu = document.getElementsByClassName('vertical-menu');
    if (verticalMenu.style.display === 'none'){
        verticalMenu.style.display = 'block';
    }
    else {
        verticalMenu.style.display = 'none';
    }
}