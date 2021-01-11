let btn = document.querySelector('.btn img');
localStorage.setItem('isMoon' , 'false');

let menu = document.querySelector('.menu-par');

let arrow = document.querySelector('.mm');

let isMoon = false;

let dark = document.querySelectorAll('.dark');
let black = `
    .O {
        fill: none;
        stroke: rgba(255, 255, 255, 0.8)  !important;
        stroke-width: 0.5;
        stroke-linecap: round;
        stroke-miterlimit: 10;
    }
    .ct-label {
        fill: rgb(0 0 0 / 40%);
        color: rgb(255 255 255 / 40%);
    }
    .ct-grid {
        stroke: rgb(255 255 255 / 20%);
    }
    `;

let white = `
    .O {
        fill: none;
        stroke: rgba(0, 0, 0, 0.8)  !important;
        stroke-width: 0.5;
        stroke-linecap: round;
        stroke-miterlimit: 10;
    }
    .ct-grid {
        stroke: rgba(0,0,0,.2);
    }
    .ct-label {
        fill: rgba(0,0,0,.4);
        color: rgba(0,0,0,.4);
    }
    `;


btn.addEventListener('click' , (e) => {
    if(!isMoon) {
        console.log('asfs');
        isMoon = true;
        btn.classList.add('rot');
        btn.setAttribute('src' , 'res/sun.svg');
        arrow.setAttribute('src' , 'res/white__menu.svg')
        document.body.style.color = 'rgb(163, 163, 163)';
        menu.style.background = 'rgba(0, 0, 0, 0.8)';
        document.body.style.background = 'rgb(17,17,17)';

            head = document.querySelector('body');
            style = document.createElement('style');
        
            head.appendChild(style);
            
            style.type = 'text/css';
            if (style.styleSheet){
            // This is required for IE8 and below.
            style.styleSheet.cssText = black;
            } else {
            style.appendChild(document.createTextNode(black));
            }
        

        for(let prop of dark) {
           prop.classList.add('doun');
        }
        
    } else {
        
            head = document.querySelector('body');
            style = document.createElement('style');
        
            head.appendChild(style);
            
            style.type = 'text/css';
            if (style.styleSheet){
            // This is required for IE8 and below.
            style.styleSheet.cssText = white;
            } else {
            style.appendChild(document.createTextNode(white));
            }
        
        btn.classList.remove('rot');
        btn.setAttribute('src' , 'res/moon.svg')
        menu.style.background = 'white';
        isMoon = false;
        document.body.style.color = 'rgba(0,0,0,.8)'
        arrow.setAttribute('src' , 'res/menu (3).svg')
        document.body.style.background = 'rgba(255, 255, 255, 0.8)';
        for(let prop of dark) {
            console.log( prop.style.background = 'rgba(255, 255, 255, 0.8) !important');
            prop.style.background = 'rgba(255, 255, 255, 0.8) !important;'
        }
        for(let prop of dark) {
            prop.classList.remove('doun');
         }
    }
});




