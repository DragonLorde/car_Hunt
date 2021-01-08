let btn = document.querySelector('.btn img');
localStorage.setItem('isMoon' , 'false');

let isMoon = false;

let graph = document.querySelector('.mid__mile-graph');

btn.addEventListener('click' , (e) => {
    if(!isMoon) {
        console.log('asfs');
        isMoon = true;
        btn.classList.add('rot');
        btn.setAttribute('src' , 'res/sun.svg')
       // graph.style.background = 'rgba(255, 255, 255, 0.8)';
    document.body.style.color = 'rgba(255, 255, 255, 0.8)'
    //a.style.color = 'rgba(0,0,0,.8)';
    // rgba(0,0,0,.8)
    document.body.style.background = 'rgba(0,0,0,.8)';
    } else {
        btn.classList.remove('rot');
        btn.setAttribute('src' , 'res/moon.svg')

        isMoon = false;
        document.body.style.color = 'rgba(0,0,0,.8)'
    // rgba(0,0,0,.8)
        document.body.style.background = 'rgba(255, 255, 255, 0.8)';
        //a.style.color = 'rgba(255, 255, 255, 0.8)';
    }
});




