let swipe = document.querySelector('body');
let show = document.querySelector('.menu-par');
let menuBtn = document.querySelector('.mm');

let pageWidth = window.innerWidth || document.body.clientWidth;
let treshold = Math.max(1,Math.floor(0.01 * (pageWidth)));
let touchstartX = 0;
let touchstartY = 0;
let touchendX = 0;
let touchendY = 0;

let right = document.querySelector('.menu-slide ');

const limit = Math.tan(10 * 1.5 / 180 * Math.PI);
const gestureZone = document.getElementById('modalContent');



swipe.addEventListener('touchstart', function(event) {
    touchstartX = event.changedTouches[0].screenX;
    touchstartY = event.changedTouches[0].screenY;
}, false);

swipe.addEventListener('touchend', function(event) {
    touchendX = event.changedTouches[0].screenX;
    touchendY = event.changedTouches[0].screenY;
    handleGesture(event);
}, false);

function handleGesture(e) {
    let x = touchendX - touchstartX;
    let y = touchendY - touchstartY;
    let xy = Math.abs(x / y);
    let yx = Math.abs(y / x);
    if (Math.abs(x) > treshold || Math.abs(y) > treshold) {
        if (yx <= limit) {
            if (x < 0) {
                show.classList.add('menu-par-hide');
                menuBtn.classList.remove('menu-slide-img');
                right.style.opacity = '1';
                right.style.left = '5%';
            } else {
                right.style.opacity = '0';
                right.style.left = '25%';
                show.classList.remove('menu-par-hide');
                menuBtn.classList.add('menu-slide-img');
            }
        }
    } else {
        if(!show.classList.contains('menu-par-hide')) {
            menuBtn.classList.toggle('menu-slide-img');
        }
        right.style.opacity = '1';
        right.style.left = '5%';
        show.classList.add('menu-par-hide');
       
    }
}

right.addEventListener('click', () => {
    right.style.opacity = '0';
    right.style.left = '25%';
    show.classList.remove('menu-par-hide');
    menuBtn.classList.add('menu-slide-img');
});


//https://api.html2pdf.app/v1/generate?url=https://bsl-show.online/push/number/b1dbfa81d2ad475fa9dd6f1705d731f5.html&apiKey=wYSOkiicp66P70ukkgayvbUoF8tQ9oqWi8Caj7aJpchJZPTiAJXPx7qLXZZTt63I


//https://www.instagram.com/molodoy_perekup/📸