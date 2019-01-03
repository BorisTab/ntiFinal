function menu(x) {
    x.classList.toggle("change");
}

function show(){
    let verticalMenu = document.getElementsByClassName('vertical-menu')[0];
    if (verticalMenu.style.display === 'none'){
        verticalMenu.style.display = 'block';
    } else {
        verticalMenu.style.display = 'none';
    }
}

